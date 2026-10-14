# Bound DI7 sources

All paths and hashes below are from the verified 58-payload dispatch. Quoted book rows are the supplied binding extracts, not a fresh inspection of a .docx absent from this packet. Current data/Core records were independently compared. Relevant complete class/counterpart records are included; no whole-class or whole-catalog semantic approval is claimed.

## S01

`DescentReviewChanges/ReviewBible/docs/mechanics/SPELL_INTEGRATION_RULES.md`
SHA-256: `256bb99fce3855a78b381577d7c4c1ec448c41d7cde79a6b238b01ca47ff35a3`
Location: lines 21–57
Ordinary acquisition/price/casting commitment/strain/concentration and independent Counterspell windows.

```text
## Select a spell

1. Choose the class through which you are learning/casting it. Check that class's school access and minimum **class** level on the card.
2. Use that class's spell rank and Core V2 cost. A different eligible class may receive the same spell at a different rank and level.
3. Record it in your allowed known, prepared or spellbook choices. An eligible catalog entry is not an automatic grant. Wizard and Druid keep their explicit preparation systems; fallback counts apply only where the class has no more specific rule.
4. Select only a spell marked `operational-playtest-draft` in this packet, or an operational spell expressly supplied by a class card. Other records stay visible in the unfinished queue.
5. A class card and an ordinary spell with the same name remain separate records with separate acquisition and costs. Knowing one does not grant the other. Oath spells, Matrix techniques and similar class spells use their own card.

Oracle uses RC and its Mystery/Curse system. Soldier and Warrior have no general Weave access. Dragoon first gains ordinary magic at class 3; Paladin at class 2. Sufficient RP, total character level, a class feature with the same name, or a borrowed spellbook cannot bypass a gate.

## Resolve a cast at the table

1. Verify the available Action/Bonus Action/Reaction, its exact trigger, components, targets, range and line of effect. No legal target means no activation or payment. A target in an area still needs the card's eligibility. Total cover blocks direct targeting unless expressly overridden.
2. Choose a spell from your actual repertoire. Determine its class-specific rank and RP cost: rank 0–9 costs **0/2/3/5/7/10/13/17/21/26**. Add explicitly printed extra costs; Resonance Shield adds 1 RP even when the caster receives it as a cantrip. Generic Overcast is excluded.
3. Read Dissonance **before** casting. Limit = max(4, 2 + PB + max(0, casting modifier)). At limit/limit+3/limit+6, ranked spells cost +1/+2/+3 RP. At limit+6 ordinary rank-1+ casting is blocked. Cantrips have no strain surcharge but still build Refrain. An expressly granted traumatic-casting exception pays the cost and its printed trauma; it grants neither rank nor repertoire access.
4. Commit the legal cast's RP, materials and other printed costs before any attack/save or interruption. Perform its components and establish concentration if required, ending incompatible prior concentration. An ordinary missed, saved-against or countered legal cast refunds nothing and never restores displaced concentration.
5. At this cast's beginning, apply ordinary Dissonance and Refrain once: 0 base for rank 0, 1 for ranks 1–5, 2 for ranks 6–9; consecutive same-named casts add Refrain +1/+2/+3, capped at +3. First cast or a different name adds +0. Apply the class's exact protected reduction, routing or vent and any hook whose printed trigger is beginning/casting. Weapon or idle turns do not reset the previous name/Refrain unless the class expressly says so. This chronological commitment occurs before the Counterspell window; a later Reaction cast updates its own history, and resuming the earlier cast does not update that history again.
6. Open legal cast-interruption Reactions, resolving nested counters last-in, first-out. A surviving cast then resolves its effect: spell attacks are d20 + PB + the actual casting ability modifier; save DC is 8 + PB + that modifier. Use the exact card's hit/failure/success results and ordinary damage/conditions. Outcome-dependent class hooks occur only at their printed timing and with the required actual result. No automatic cantrip scaling applies. A negated spell grants no success/hit/damage effect merely because its casting cost was paid.
7. Record concentration, exact expiration, per-rest use, summon and companion command obligations. A second spell cannot supply an ungranted Action, duplicate concentration or resource reset. A readied spell commits this casting sequence at preparation; release has no second cast, cost, cadence update or Counterspell window.

Countering requires an actual operational spell or class card, its repertoire/access and a legal remaining Reaction. The ordinary Counterspell is now reviewed; it is separate from the Mage and Wizard class cards. Dispel Minor, Dispel Resonance, Dispel Magic (Lesser) and Dispel Magic use their exact individual scopes. Rank-limited dispels inspect the original generating cast's spell rank, not RP cost or the dispeller's rank. Higher and unassigned source variants retain their own unfinished status.

## Counterspell checks and interruption

The [exact notebook review](../../../../docs/audit/2026-10-08/full-game/GPT_ABJURATION_RANK2_3_EXACT_REVIEW.md) confirms this authored timing interface and corrects the earlier binary-check proposal using the existing [Core roll rules](CORE_RESOLUTION_PLAYTEST.md). This is a tabletop procedure; the pricing helper does not implement nested reactions.

Ordinary Counterspell uses its casting class's actual spellcasting ability + PB against **DC 10 + twice the triggering spell's actual rank**. The class Wizard/Mage cards retain their printed Intelligence + PB check and their own acquisition, cost, rank and recharge. Apply the existing fixed-DC task degrees and natural shifts, then collapse Critical Success/Success to success and Failure/Critical Failure to failure. No extra critical counter effect is invented. It is neither a spell attack nor a saving throw.

| Natural d20 + modifier | DC | Existing task result | Counter result |
|---|---:|---|---|
| 20 + 0 | 22 | Failure improves to Success | Success |
| 1 + 9 | 10 | Success worsens to Failure | Failure |
| 1 + 20 | 10 | Critical Success worsens to Success | Success |

The target must be an actual pending spell with a recorded rank. The Director may use hidden source data without revealing the spell's identity/rank; attempting grants no free identification. An unassigned rank is not automatically zero. A source-defined technique is not counterable merely because it spends RP or resembles magic.

A creature normally attempts Counterspell once against a particular pending cast, across its ordinary and same-named class sources. Another Reaction alone does not supply another attempt. An exact source expressly granting an additional attempt against that same cast overrides the default. After failure, another eligible creature may react; after negation there is no further trigger. Counterspell is itself a spell and can be countered. Resolve nested counters last-in, first-out and resume surviving parents without recasting, paying again, or replaying their earlier Refrain/Dissonance. Negation refunds no costs and restores no prior concentration. Countering one spell is not whole-Action/turn hard denial and does not spend that combined ledger.
```

## S02

`DescentReviewChanges/ReviewBible/docs/mechanics/CLASS_PLAYTEST_RULES.md`
SHA-256: `adb2f4752b45dc70ce792a675bb30dda362aab5056588061bcde3ba31c4c8a81`
Location: lines 7–49
Class identity, real budgets, concentration, no duplicate copy-procs, ordinary strain and techniques.

```text
Use the class's own level, never total character level, for gates and effects. **L** means that class level; **S** is 1/2/3/4 at class levels 1/5/11/17. **M** means max(1, the class ability modifier), for effect a mounts only. Attacks use d20 + normal character proficiency + the actual appropriate ability modifier. Class save DC is 8 + normal proficiency + actual class ability modifier. Negative modifiers still apply to attacks and DCs. One tile is 5 ft. Fractions round down unless specified. Distances cannot be negative.

A weapon attack uses its usual ability, weapon die and damage type. A technique that says “make one weapon attack” replaces your Action with that attack; it does not also grant a normal Attack Action or Extra Attack. Generic attack-speed language has no effect beyond the exact attacks printed in the draft. A spell attack uses the class's stated casting ability. Natural 1 misses and natural 20 hits/critically doubles damage dice; flat bonuses do not double. A save succeeds at DC; “fails by 10” means the total is at least 10 below DC. Critical-range improvements never stack; use the broadest one.

An ability is known only if granted or selected by the draft schedule. Satisfy all printed prerequisites, target legality, action availability, recharge and resource costs before spending anything. A failed legal attack/save attempt still pays; an illegal activation spends nothing. No resource goes below 0 or above its cap. A class feature name shared with a spell does not grant both versions; use the version selected, with its own cost and timing. Names and source text are preserved; the current card is the operational draft.

## Action and timing limits

One regular Action, one Bonus Action if a feature permits it, normal movement and one Reaction between starts of your turns. A free trigger costs no Action only if expressly stated. All grants share **one extra full Action per creature per round**. An extra Action cannot grant another Action, recharge itself, or start another extra-Action grant. It supplies no extra Bonus Action or Reaction. A card granting additional attacks is not permission to repeat all class riders on every hit: obey each rider's frequency.

Recharge N sets a counter to N after use; reduce once at the start of the owner's regular initiative turn, whether able to act or not. Extra turns/Actions do not tick it. Outside combat tick once per 6 elapsed seconds, without double counting. Recharge 2 used on turn 1 is ready on turn 3. A positive counter can be reset/shortened at most once per ability per round. Zero counters are not legal reset targets and expend no reset use. Resets never restore RP or per-rest uses or grant an immediate activation.

An encounter is a genuine scene of uncertain opposition chosen by the Director, not a player declaration used to reset resources. No encounter gain from attacking allies, one's summons, harmless animals, helpless captives or reused corpses. Out-of-combat abilities retain all printed costs and time. Short-rest means a completed uninterrupted hour of permitted recovery; long-rest means a completed 8-hour Rest Watch. This time convention is a draft integration. Expedition pressure, supplies, safe locations and rest debt still matter. A long rest also refreshes short-rest uses; a short rest never refreshes long-rest uses. Weekly uses refresh after seven full in-world days, not repeated rests.

## Targets, concentration and control

Unless expressly stated, perceive the target, remain within range and have line of effect; total cover blocks targeting. “Ally” includes self unless it says OTHER. A list cannot contain a creature twice. Select up to the printed limit; an empty target list is not a valid way to farm activation benefits. Zones remain at their chosen point unless described as an aura; allies can leave and lose their benefits. An aura requires its owner conscious unless the card supplies a bounded exception. An effect ending at “end next turn” means the affected creature's next turn only when the card says target's; otherwise the user's.

One concentration slot for all spells, Chants, Veinweaves, forms or zones that require concentration. Starting another ends the old before the new effect resolves, except for an explicit limited linked-effect rule. Damage prompts CON save against max(10, floor(damage/2)); incapacitation or a failed save ends concentration. The round-down convention is a deliberate pilot interpretation. Concentration does not demand a Bonus Action unless maintenance says so. For a paid 3-pulse effect, start is pulse 1; pay maintenance on each of the next 2 regular turns by turn end for pulses 2/3. Missing payment ends it at that turn's end; otherwise it ends at start of turn 4. No repeated start triggers on maintenance.

Forced movement does not provoke opportunity attacks unless explicitly stated, cannot place a creature inside solid matter, and stops at an obstacle. Grapples use the card's save/DC, can be escaped with an Action and STR(Athletics) or DEX(Acrobatics) against that DC, and end beyond reach. A root sets Speed 0 but does not remove Actions. Slows reduce Speed to minimum 0. Silence blocks verbal spells/audible abilities, not all thought or all class features. Charmed effects never determine a player's beliefs; use only the printed action restrictions.

No repeated hard denial without a new save and cost. For this class suite, a creature can suffer **Stunned, compelled loss of its whole Action/turn, or equivalent hard denial from a given character at most once per encounter**, across that character's class features; later such riders fail while damage and soft riders resolve normally. Record source and target. This draft guard is broader than the older Oracle-only ceiling and is an explicit balance proposal. Reaction denial, Speed reduction, penalties and Frightened do not count as whole-turn loss. Do not silently waive boss immunities, legendary defenses or anatomy.

## Damage, healing, stacking and companions

Roll once for each shared area/pulse and apply saves/defenses to each target separately; separate attacks roll separately. Halve once for a successful save and apply resistance/immunity normally. Same-named conditions/bonuses do not stack unless a printed cap allows it; same-stat flat bonuses from these class techniques use the strongest. Different resources remain separate. Damage reduction from these class features uses the strongest flat reduction, then applies resistance; it cannot create negative damage or healing. Temporary HP never stack; choose the larger remaining amount. Immunity is not reduced resistance.

Repeated permanent HP recovery must consume finite RP, a per-rest use or another finite resource; a combat-generated gauge alone never enables unlimited healing. Healing cannot exceed maximum HP or erase Wounds, death consequences, debt or Corruption unless explicit. Downed is living at 0 HP; dead is different. Resurrection requires a willing soul and sufficiently intact body, obeys its time window, cannot create a duplicate and never refunds the feature on failure to meet known prerequisites. Sacrificial HP is actual unpreventable loss, cannot be redirected or paid with temporary HP, and is not damage for resource triggers. It cannot reduce the donor below 1 unless a card expressly grants a death-triggered effect.

No damage/healing copy repeats the source's costs, procs, resource generation, critical bonus dice, buffs, actions, cooldown resets or duration. Compute fractions once, capped at 100% of one stored source unless an explicit card states a separately priced higher amount. Copies still cause ordinary damage consequences, concentration checks and death. A copy cannot copy another copy. A target/source record must refer to an actual resolved event, not merely a known ability name.

Where a class card calls for a **standard companion** without a more specific profile, use: Small or Medium; AC 12+floor(PB/2); HP 2 L; walking Speed 30 ft; saves equal owner's PB; one melee or ranged attack (reach 5 ft/range 30 ft) at owner's class attack bonus, damage S d6 of the printed type. It has no independent class features, resources, loot, death triggers or extra turns. All companions belonging to one character share one Bonus Action command and **one damaging attack/action total per round** unless a specifically priced feature grants more. Without a command they move and Dodge. Act immediately after owner. A standard companion lasts 1 minute, disappears at 0 HP and cannot be healed for free by dismissing/resummoning. The creation cost must be paid again. Creature-specific stat blocks override this profile only where explicitly printed.

## Ordinary spells: one explicit test configuration

Use the manifest-owned **Core Systems Known Descent V 2** class RP tables and rank costs: rank 0–9 costs 0/2/3/5/7/10/13/17/21/26; Grand 32. Follow `src/data/class-spell-progression.js` for each class's rank gates and the existing spell catalog for class/school access. Having enough RP never bypasses a rank gate. Oracle has Revelation Charges, and Soldier/Warrior have no general RP spellcasting. Multiclass spell access is determined separately per class; do not add complete class pools or use total level to unlock a rank. This suite's printed pool tables are single-class; use the existing multiclass pool formula with the new constituent Core V 2 pools for mixed characters.

Four classes have no direct Core V 2 pool row. For this pilot, Crimson Agent uses the Cleric curve multiplied by 0.5; Dragoon, Monk and Thief use that curve multiplied by 0.35, rounded to nearest integer with halves upward, minimum 1. These fallback factors come from the preserved `src/data/resonance-economy.js`; they are explicitly distinguished from direct book tables. The generic Core V 2 Oracle RP row is rejected for this class suite because Oracle's protected class contract uses Revelation Charges only. Oracle never receives RP or ordinary spell access. Retune here means one recovery at the end of a completed short rest, not an unrestricted action.

For a reproducible pilot, retain the protected **Dissonance** layer with Core V 2 numeric RP costs. This combination is a new integration decision: do not also roll a second historical Burn/fizzle system on top of it. Limit=max(4, 2+PB+max(0, casting modifier)). Before a ranked cast, Dissonance at limit/limit+3/limit+6 adds 1/2/3 RP respectively; at limit+6 ordinary casters cannot cast rank 1+. At limit+3 ordinary Overcast is unavailable. A cast then adds base Dissonance 0 at rank 0, 1 at ranks 1–5, 2 at ranks 6–9. Immediate repeated casts of the same named spell add 1, 2, then 3 maximum. Another named spell resets the repeat counter but not accumulated strain. Apply the class's exact cadence reduction/vent; never infer a free RP reduction. Printed class techniques pay printed costs and cause no automatic spell Dissonance unless tagged or expressly described as spells, Echo releases or Matrix casts. For a Mage/Wizard class card tagged as a spell, use the rank printed in normalized data; its rank is fixed at acquisition and does not rise with S. Other techniques are not counterspell able unless their card says so.

Retune recovers max(0, round(max RP/4)+casting modifier), never above maximum, and clears Dissonance. A long rest restores RP and clears Dissonance. Optional 10-minute meditation once/day recovers positive casting modifier RP and reduces Dissonance by PB+positive modifier. A regular turn with no spell or magical class ability loses 1 Dissonance; an Action spent Grounding without casting loses PB instead (not both). Merely ending an encounter does not clear accumulated Dissonance. Refrain survives idle/weapon turns unless a class explicitly clears it. Lich/Necromancer may force ranked casts through Fracture; after resolution take direct unpreventable trauma equal to rank×1/2/3 at the three strained states, minimum 1, based on state before casting. This trauma cannot generate resources or trigger damage-sharing. They still pay RP and meet rank gates.
```

## S03

`DescentReviewChanges/ReviewBible/docs/mechanics/COMBAT_ACTION_PLAYTEST.md`
SHA-256: `f90d039142145fbd31c37992ebece70d7926dc4b6081e340f9a2fd9dc7237bc6`
Location: lines 27–70
Actual regular/extra turns, stable event order and absolute/marker clocks.

```text
## Encounter and action resources

Establish terrain, light, hazards, objectives, exits and cargo; determine awareness; roll `d20 + DEX modifier + legal bonuses`. Highest first. Players choose player/player ties; the Director resolves ties involving NPCs. Keep the resulting ordered slots for the encounter. A round represents approximately six seconds. A **regular turn** is a creature's normal initiative slot even if it cannot act. An extra turn is distinct.

A turn normally permits movement, one Action, a Bonus Action when an actual rule grants a use, and one ordinary free object interaction. A second ordinary interaction or an Action-time object activation uses an Action. Brief communication is not an extra Action. Conditions and specific features may restrict these permissions.

The shared limit is one **extra full Action per creature per numbered round**. Such an Action cannot grant another extra Action, Bonus Action or Reaction. This cap is independent of Reaction timing. Extra turns do not by themselves refresh Reactions, recharge, periodic ticks, recovery ticks or the regular-turn allowances defined here.

**Reaction interpretation.** Begin an encounter with one available Reaction unless surprised or otherwise prohibited. Refresh at each regular own-turn start; never at the numbered round boundary or an extra turn. A late-initiative creature can therefore react before its first turn, refresh, and react again in the same numbered round. A legal trigger, available resource and all feature prerequisites are still required.

**Explicit additional Reactions.** A reviewed card can grant a separate limited use without refreshing the ordinary resource. Warrior Mind Shock supplies its stated once-per-duration non-attack Reaction; spending one resource does not consume/reset the other. Surprise, Incapacitated and Focused still restrict both. It grants no Counterspell knowledge or waived costs. Extra turns refresh neither. Per-dose reapplication/stacking and other specific grants remain part of the class semantic pass.

**Surprise — V6 plus NEW Bonus Action clarification.** On a surprised creature's first regular turn it cannot voluntarily move or take an Action or Bonus Action. It cannot react until that turn ends. Its slot, durations, passive effects, concentration, periodic effects and recharge still occur. Surprise alone is not Incapacitated or Unconscious. Brief communication and an otherwise legal simple free interaction remain possible.

**Entry — NEW.** Standard end-round reinforcements roll/receive initiative and first act next round. An explicit midround entrant acts this round only if its complete ordered slot is still upcoming; entry during that exact slot counts as already passed. It has its initial Reaction unless prohibited. A summon-specific timing rule overrides this generic entry procedure.

After the final slot, resolve Core's end-round hazards, reinforcements, morale, objectives and boss phases. Conclude the scene with surrender, capture, pursuit, harvesting access and noise consequences under their own rules; winning initiative does not resolve those automatically.

## Time and event ordering — NEW

For a duration created in initiative, record the relevant original regular start/end marker. Existing effects keep that **virtual marker**, repeating every six seconds if the creature leaves or changes initiative. Reordering, rerolling, extra turns, death/removal or leaving/reentering initiative never restart an existing duration. New effects use the current schedule. Source death still ends concentration, a source-dependent aura/tether or an effect explicitly ending on death.

- A bare hostile target-bound **N rounds** ends at the Nth future regular target-end marker. An in-progress target turn's current end does not count.
- A bare self/source buff, ally-targeted buff or source-controlled aura **N rounds** ends at the Nth future source-start marker. Explicit target-turn, pulse or absolute timing overrides this default. Activation during source turn 1 for three rounds ends at source turn 4's start.
- **Next turn** means the next future regular turn of the named creature, not the current turn's still-upcoming end. An unqualified next turn refers to source/user under the existing shared rule. Explicit “this turn” can include the current turn.
- An outside-initiative bare N-round effect instead gets an absolute application-time + N×6 seconds deadline. Entering initiative preserves that deadline.
- Explicit periodic profiles retain their registered clocks and tick counts. Never create a second timer merely because a generic duration rule also exists.

The [exact GPT review](../../../../docs/audit/2026-10-08/full-game/GPT_COMBAT_EXACT_FINDINGS.md) confirms ally-buff source clocks and excluding the current turn for explicit next-turn endpoints. The helper excludes a specific current-end marker only if that marker would otherwise be selected: application during a turn at time1 with end3 excludes3 and selects9; application at/after3 also selects9, without erroneously skipping again to15.

At a regular turn's **start**, resolve in this order:

1. Expire start-ending effects and apply immediate state changes from those expirations.
2. Refresh Reaction; tick regular-start recharge/non-action clocks.
3. Resolve already-due absolute state recovery if now legal, including a previously blocked Stable recovery deadline.
4. If still alive, dying and at 0 HP with death saves, make that turn's death save.
5. Resolve other start effects and periodic events in application order.
6. Begin voluntary turn decisions.

At **end**, resolve triggered effects, due damage, saves and maintenance before end-ending effects expire; then the slot finishes. No extra turn creates another regular marker. The caller must not reuse a resolved marker.

For simultaneous effects, earlier application timestamp precedes later. For simultaneous components of one source, its printed internal order controls; otherwise use stable application sequence, with source/mechanical ID as a final tie-break. Record that sequence when creating the effects. Beneficial/harmful labels do not change priority. Periodic family arbitration happens once per family/marker before its damage, retaining the family registry's consumed loser ticks.

Examples: dying at 0 rolls its death save before ordinary start-turn healing; a fatal death save is not undone by ordinary healing. Stable at 0 skips the save, then start-turn damage can break Stable. A natural 20 can restore 1 HP before a due Bleed drops it to 0 as a new drop event. If Decay expires while a Stable recovery deadline is already due, the old deadline resolves once without rerolling recovery time.
```

## S04

`DescentReviewChanges/ReviewBible/docs/mechanics/COMBAT_ACTION_PLAYTEST.md`
SHA-256: `f90d039142145fbd31c37992ebece70d7926dc4b6081e340f9a2fd9dc7237bc6`
Location: lines 97–111
Full generic Ready procedure: spell cast at preparation; no second outer cost/window at release.

```text
## Ready

Spend an Action to declare a perceivable trigger and one legal Action-time action or movement. It expires next regular own-turn start. **NEW:** only one pending Ready per creature; replacing it loses the prior setup and any paid held-spell costs. No Bonus Action/Reaction ability, long ritual or multi-minute activity can be prepared by generic Ready.

The trigger happens first, then the readied response immediately follows before later events, unless a specific effect explicitly interrupts. On release spend the normal Reaction and recheck target, range, sight/perception, line of effect, ammunition and other prerequisites. An invalid or declined occurrence spends no release resource; the Ready can wait for another valid occurrence before expiry. This does not undo setup costs. Once released, it is consumed.

For ordinary nonspell actions, feature/ammunition costs are paid on release unless text charges setup. A readied **Attack Action** gets its legally available ordinary attack count; a feature limited to your own turn does not thereby work off-turn. Core Overwatch is explicitly one ranged attack, not that full Attack Action and not Soldier's distinct engine.

A readied spell is actually **cast at preparation**: choose spell/mode, verify legality, pay RP/material/other costs, provide components, resolve Dissonance/Refrain and cast-trigger effects once. Counterspell/cast-interruption opportunity occurs then, not again at release. Every held spell requires concentration, even ordinarily non-concentration spells; incompatible prior concentration ends. Lost concentration loses the held spell and costs. NEW: select the legal target/area point at release and recheck legality without repaying. At release the hold continues as ordinary spell concentration if required, otherwise ends after resolution. Expired/replaced/countered held spells do not refund paid costs.

Ready movement grants a separate current-Speed budget on release, pays terrain costs and can provoke ordinary opportunity attacks. It grants no extra Action, Bonus Action or interaction.

Focused stance's Reaction restriction also blocks an ordinary Ready release; Ready does not create a Counterspell exception. Holding a spell does not waive any current Reaction prohibition.

**Spell-effect duration begins at release.** Its normal duration is anchored when the effect manifests, while Ready expiry and held concentration already run from preparation. A source explicitly tying a particular consequence to casting/preparation retains that consequence's stated clock. No casting cost, Refrain, Dissonance or cast trigger occurs a second time merely from release.
```

## S05

`DescentReviewChanges/ReviewBible/docs/mechanics/COMBAT_ACTION_PLAYTEST.md`
SHA-256: `f90d039142145fbd31c37992ebece70d7926dc4b6081e340f9a2fd9dc7237bc6`
Location: lines 154–180
Geometry remains partly open; range grid metric; learned location removes Hidden/Invisible-only modifiers without sight.

```text
## Movement and geometry

Track **spent movement cost**, not distance, for ordinary turn movement. Mode cap = `(1 + number of legal Dash actions this turn) × current Speed for that mode`; remaining = max(0, cap − spent cost). Switching modes never refunds cost. Recalculate cap on Speed changes, preserving spent cost. Stand from Prone costs floor(half current Speed) and requires nonzero Speed and enough budget. Dropping Prone costs no movement.

For each foot traveled, normal/difficult/severe terrain costs 1/2/3; use strongest terrain only. Add +1 for crawling and +1 for squeezing. Crawl in difficult =3:1; crawl+squeeze in difficult =4:1. A nonhostile occupied space counts as difficult terrain. Enter a hostile creature's space only with ≥two-size difference or an express feature; never willingly end in an occupied space. Squeeze through a space one size smaller, with own attack/DEX-save disadvantage and attacks-against advantage.

Walk10 through difficult spends20; switch to Fly30 leaves10. Stand with Speed30 spends15; switching to Fly30 leaves15. Two legal Dashes at Speed30 give cap90; prior expenditure still counts. Interpose/Press grant5 budget: they cannot enter a difficult 5-ft tile costing10. Their separate budgets never refill ordinary movement. Ready movement uses Speed at release; Withdraw uses half current Speed. All voluntary movement requires nonzero relevant Speed.

Forced movement does not use these ledgers or provoke ordinary opportunity attacks, cannot place creatures in solid matter, and stops at obstacles. Teleport does not traverse intervening terrain or spend Speed unless printed; it requires a legal destination. Speed0 alone does not block forced movement or teleport. Flight with Prone/Speed0/lost support causes Falling unless Hover or an explicit magical support exception applies; use the existing fixed Fall Marker procedure. Reaching support ends Falling.

NEW grid metric: each orthogonal or diagonal neighboring tile is 5 ft; use the same metric for ordinary ranges/areas. No diagonal cut through a corner when both adjacent orthogonal sides are completely blocked. Exact templates, 3D geometry, mounts, chases, jumping, climbing/swimming procedures and currents need further source review.

## Cover, sight, Hide and Search

Keep **visibility**, **known location**, and **line of effect** separate. Seeing through a barrier does not itself permit attacking through it. Best cover only: half +2 AC/DEX saves; three-quarters +5; total prevents direct targeting through that obstruction. Never add +2 and +5. For areas, evaluate line/cover from the area's origin to each target; total cover there excludes a creature unless the effect explicitly travels around/through the obstruction. The origin point itself must be legally targetable.

Within normal ranged range, no range penalty; beyond normal through long, disadvantage; beyond long, illegal. Ranged attacks also have disadvantage when within5ft of a non-Incapacitated hostile that can see the attacker, even if the attacker cannot see that hostile. All advantage/disadvantage follows the single cancellation rule.

NEW **Hide**: permitted only against observers unable to see you clearly or where a feature permits. Roll DEX Stealth once, record natural die and total. Against each observer's passive DC `10 + WIS Perception modifier including applicable proficiency`, use the Core four-degree task system. Meet DC succeeds before natural1/20 degree adjustment; Success/Critical Success establishes Hidden for that observer. No unsourced passive ±5 adjustment for advantage/disadvantage. Actual Search rolls use their normal modifiers.

Hidden means that observer cannot see you and does not know your location. Clear sight or learning your position ends Hidden for that observer. Moving between hiding places can retain Hidden only if no clear sight/revealing event occurs. A failed Hide cannot simply be rerolled unchanged; a materially new hiding position, concealment, distraction, sight-breaking event or express reroll feature is required. Hidden is not a generic immunity or a free stealth roll for every move.

**Search** Action: WIS Perception for sensory detection; INT Investigation for appropriate traces/deduction; Core Arcana/Engineering where relevant. Directly locating a Hidden creature defaults to Perception against its recorded final Stealth total as a static DC, using task degrees/natural shifts. Success reveals location only to the searcher and ends Hidden for that observer, without automatically granting sight. Communicate normally to inform others. Search can be repeated on later turns by paying the Action.

Attacks against unseen targets have disadvantage; unseen attackers have advantage, subject to the **Core Invisible exception**: once its position is known, Invisible's own attack modifiers end for that observer and cannot immediately return solely because it remains Invisible. Independent darkness, smoke, blindness or hiding can still supply modifiers.

Resolve an attack using pre-attack information; afterward reveal location to observers able to perceive its evidence. If an unseen target's location is unknown, do not directly choose it for a creature-target effect. A weapon/projectile can instead attack a suspected space: wrong space automatically misses; correct space uses unseen rules. A “creature you can see” requirement is never met by position knowledge alone. Area effects can target legal points under their own rules.
```

## S06

`DescentReviewChanges/ReviewBible/docs/mechanics/DAMAGE_SHARING_PLAYTEST.md`
SHA-256: `b298415146cba6453ec33f1310b4b668ac74e0e2d2681a08e077852c065d56e1`
Location: lines 7–29
Retargeting, pre-mitigation splitting, finite prevention and skipped post-defense mitigation.

```text
## Resolve the kind of protection first

Guardian Pulse changes the target of an attack before comparing its original roll with AC. The Guardian becomes the actual hit/miss and on-hit-rider target. One attack can be retargeted once. Multiple offers are chosen by the original intended target; only the selected Guardian spends its Reaction/use. After the incoming attack fully resolves, a surviving, eligible Guardian may make the printed counterattack against an attacker in reach whether the original attack hit or missed. This free attack cannot grant another free attack or Action. Retargeting does not spend the later damage-transfer opportunity.

Bloodbond and Veinlock Tether divide the finalized raw damage before either recipient's mitigation. Attack/save success, save-halving and critical dice have already determined that amount. Bloodbond transfers one quarter, rounded down; Veinlock instead chooses up to S+M. Each recipient applies its own eligible defenses once to its own share.

Other supplied damage transfers divide damage after the original target's defenses and legal pure prevention, before temporary HP. Their transferred portions keep damage type and skip another DR/resistance/immunity/prevention stage. Temporary HP, applicable HP floors, would-die replacements, Wounds, concentration and ordinary life consequences still apply. “Unmitigated damage” does not mean “death cannot be prevented.”

Pure prevention removes damage without creating a second recipient. Elemental Absorption adds its resistance during ordinary defenses. Aura of Bonds and Crown reductions use the strongest applicable class flat reduction, then resistance/immunity. Finite/reactive prevention such as Bloom and Ancestral Guardian follows those defenses before post-defense transfer and temporary HP. Verify additional item/spell sources before treating this as universal defense ordering.

Redirecting Palm prevents half the Monk's post-defense damage, rounded down. The Monk keeps the remainder. A second enemy distinct from the triggering melee attacker, within5feet, can receive new force damage equal to the prevented amount, capped at Monk level. That new damage gets its own defenses; it is not a transferred attack or critical hit. With no second enemy, the Monk still receives the reduction.

Direct HP payments from Blood Sacrifice, Flesh-to-RP, Profane Exchange and Channel Life stay outside the damage sequence. They bypass temporary HP, obey their own legal minimum HP and do not create damage/Wound/resource triggers from paying the cost. Healing-recipient substitution and excess-healing conversion also remain distinct operations.

## One transfer operation and exact amounts

A root here means one original recipient's damage packet. A shared area cast has a separate root for each original recipient, under the same cast/roll identity.

One such root accepts one damage-sharing operation across all owners. A pre-mitigation split locks both its retained original portion and transferred portions against later transfer. Burden Shared can divide one operation among up to two other explicitly willing recipients. It does not create two redirection events. No transferred recipient may be the original damage target.

**New stage-precedence integration:** consider pre-mitigation offers before applying defenses, and post-defense offers afterward. Within the same stage, select eligible positive mandatory/automatic protection before optional offers; competing mandatory claims are chosen by the original damage target. A legally chosen Bloodbond/Veinlock operation can therefore preempt later Aegis/Final Stand because that root is already claimed. Do not preview or consume defenses/Bloom to decide a later-stage preference. The helper accepts an already selected legal operation; it does not select Reactions or schedule automatic offers.

Optional transfer requires a positive chosen amount and available damage. Zero transfer cannot spend an optional Reaction/resource/use. A mandatory rounded-zero share does nothing and spends no transfer allowance. An independently legal prevention component can still occur.
```

## S07

`DescentReviewChanges/ReviewBible/docs/mechanics/DAMAGE_SHARING_PLAYTEST.md`
SHA-256: `b298415146cba6453ec33f1310b4b668ac74e0e2d2681a08e077852c065d56e1`
Location: lines 49–74
Real damage-root recipient/hit identity and source-specific branch restrictions.

```text
## Hit identity and final damage accounting

The original damage target retains its original hit, failed-save, critical and on-hit-rider identity even if all damage is transferred. A rider that requires positive damage must recheck the actual remaining packet. A transferred recipient was not hit by that attack and did not fail its save; it receives no attached poison/control/maiming/knockout rider merely because damage moved.

Accordingly, transferred damage from a critical attack gives an already0HP recipient the ordinary one damage failure, not two critical-hit failures. Concentration still sees the transferred recipient's resolved packet even if temporary HP absorbs all of it.

Use the [reviewed life-state interface](HEALING_DEATH_PLAYTEST.md) after resolving each final recipient. Numeric actual damage is temporary HP absorbed plus actual normal HP lost, excluding overkill and damage prevented by an HP floor. Sum each terminal recipient once. Do not also count the unsplit parent or unrelated counterdamage.

Physical root totals include every recipient. A healing/resource/reflection consumer sums only branches permitted for that consumer and qualifying for its own source's target predicate. For example, a meaningful-hostile-only drain does not automatically count damage transferred onto a friendly protector. Check all applicable flags for a compound trigger, such as a passive healing proc.

## Source-specific restrictions

All transfers prohibit another transfer. All supplied post-defense transfers prohibit another mitigation/prevention stage. Further restrictions differ:

| Source family | Additional restrictions on transferred damage |
|---|---|
| Paladin engine | No reflection or resource generation; does not universally prohibit other retaliation or healing |
| Protective Stance | Also no generic damage-trigger chains |
| Burden Shared | Also no derived healing |
| Oracle Life Linked | No reflection, resource/RC, passive, condition, action or copy generation; no recovery or retaliation |
| Guardian Tissue / Aegis | No BT generation; no invented ban on every other resource |
| Shared Breath | No additional generic trigger prohibition |
| Selfless Guardian / Emergency Protocols | No retaliation chain |
| Bloodbond / Veinlock | Each recipient still has its one defense stage; no additional blanket prohibition |

A no-derived-healing flag does not prevent unrelated later healing of the recipient.
```

## S08

`DescentReviewChanges/ReviewBible/docs/mechanics/CORE_RESOLUTION_PLAYTEST.md`
SHA-256: `69d0e64394de58c4d86a3ec57cf282978d131a1a9c1eaa21632bb7d3b72562da`
Location: lines 23–47
Binary saves vs task-degree counters and real damage/Wound consequences.

```text
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

```

## S09

`DescentReviewChanges/ReviewBible/docs/mechanics/CONTROL_STATES_PLAYTEST.md`
SHA-256: `f2c6263c7385d4a1487c0563227f537ea64e80da48fb8f3cd2255935a415e1f2`
Location: lines 7–17
Application records; typed phase-0 absolute deadlines; no global each-turn rewrite.

```text
## Records, clocks and precedence

Each application records its identity, exact source, owner character, target, selected mode/components, application order, recorded source DC, deadline/marker, concentration or attachment relationship, remaining uses, and applicable immunity/suppression. Display names never create conditions or prerequisites. An owner's mark cannot satisfy another owner's class hook. A corpse marker, map point, archived spell, intrinsic Oracle Curse and hard-denial history are distinct state types.

Explicit operative effect text controls over a less-specific summary duration field. Use preserved regular-turn markers for **next** turn and bare N-round durations as in the combat guide; an in-progress current turn is not the next turn. Unqualified next turn refers to the source; explicit its/target refers to the target. Bare hostile N rounds, including hostile marks, use N future target regular ends. Beneficial/self N rounds use source regular starts. Preserve virtual markers through initiative changes and absence. Out of initiative bare N rounds use application+6N seconds, retaining that deadline on entering initiative. Explicit source/concentration endings still apply.

**NEW current-turn bridge:** “end of that turn” or the supplied bare “end turn” effects end at the end of the actual turn containing the application event, including another creature's or an extra turn. With no current turn, use application+6 seconds. An application during end-turn resolution expires at that same end after resolving, rather than acquiring a fabricated next turn. This applies to Resonant Seed, Winter's Embrace, Frost Totem and Glue. It does not override an explicit next-turn endpoint.

The reference represents an expiry as an ordered `(seconds, phase)` marker, preserving exact rational seconds from the combat clock. Every turn-end deadline uses expiry phase 20: current actual turn, source/target next regular end, Nth future target regular end, and Balanced Elements' following target end. End-trigger application/resolution occurs at phase 10 and the next event slot at phase 30. The effect therefore remains during final end events and expires afterward at that same second. Turn-start and absolute elapsed deadlines use phase 0. Callers must choose an explicit typed deadline; bare numeric expiries are rejected. No fractional-second workaround or duplicate turn is created.

Repeat saves, ordinary duration expiry and previously reviewed periodic/recharge clocks use regular turns unless an explicit exception applies. This is **not** a global rule changing every “each turn” damage trigger. Zone entry/start application checks, repeat ending saves and once-per-numbered-round caps are distinct events. Follow each source's actual trigger and cap; concentration alone grants no recurring application save.
```

## S10

`DescentReviewChanges/ReviewBible/docs/mechanics/CONDITIONS_PLAYTEST.md`
SHA-256: `6f6278430d48d0c74dc8e3b928b01dea3cc97d5e45226b128a405ab37b1e7148`
Location: lines 188–210
Existing Corrupted underlying moral change; no forced conduct/oathbreak.

```text
## Corrupted

**Preserved Core text:** Healing is reduced, corruption-sensitive effects worsen, and long rests may shift behavior or form until cleansed.

**Effect:** Halve each healing effect's final potential HP once, rounded down, before the HP ceiling. Saves against spells/abilities from individually recorded Evil creatures have disadvantage; its aura can be detected by effects revealing evil. At each completed long rest make DC 15 WIS save or move one moral step Good to Neutral to Evil, leaving law/chaos unchanged. Already Evil remains Evil. Alignment does not compel conduct, party separation, PvP or automatic oathbreaking.

**Application:** Only effects that explicitly inflict Corrupted apply it.

**Duration and ending:** Persists until an explicit cleansing effect or the eight-hour cleansing project in CONDITION_RECOVERY_PLAYTEST.md succeeds. Long rest alone does not cleanse it. At a simultaneous cleansing/rest endpoint, resolve cleansing first and make the Corrupted rest save only if it remains.

**Stacking:** Corrupted does not stack with itself. Apply the generic half-healing reduction once; an effect does not halve again merely because it restates the same Corrupted penalty.

**Immunities and specific exceptions:** Natural-20 death-save recovery and recovered Stable 1-HP recovery are state-recovery rules rather than healing effects and still restore exactly 1 HP. Explicit cleansing or protection may override within scope.

**Compatible V6/source details:**

- V6: healing effects restore half normal HP; disadvantage on saves against spells/abilities from evil creatures; faint aura detectable by magic revealing evil; at end of each long rest make DC 15 Wisdom save or alignment shifts one step toward evil.

**Explicit integration decisions:**

- NEW: round half healing down once; guaranteed death-save/Stable one-HP state recovery is not a healing effect.
- Source-grounded: individual recorded alignment or Evil tag only; no ancestry/faction inference, forced behavior or automatic conduct violation.
- NEW: generic cleansing project supplies a finite recovery route.
```

## S11

`DescentReviewChanges/ReviewBible/docs/mechanics/SPELL_INTEGRATION_RULES.md`
SHA-256: `256bb99fce3855a78b381577d7c4c1ec448c41d7cde79a6b238b01ca47ff35a3`
Location: lines 145–179
Readable hidden facts/paid inquiries/actual protections; distant faction objective/source distinctions.

```text
## Reviewed Divination cantrip information boundaries

The [eleven-card review](../../../../docs/audit/2026-10-08/full-game/GPT_DIVINATION_CANTRIP_EXACT_REVIEW.md) and [final source clarification](../../../../docs/audit/2026-10-08/full-game/GPT_DIVINATION_CANTRIP_FINAL_CLARIFICATION.md) make each spell's information output explicit. Actual hidden facts may be revealed when a spell authorizes them; undefined records must not be invented. Sense Alignment distinguishes recorded axes, Indeterminate and genuinely unaligned objects. Detect Faction requires an actual affiliation/nonaffiliation record; absence of a field is not a negative finding. Resonance Sight reads current RP only, using ordinary visibility and actual pools; unreadability is not proof of no pool.

Protection from Scrying prevents new information about its subject within its actual generating-school scope, including new Far Echo retrieval. It does not erase events, ordinary recordings or known facts, nor grant blanket immunity to Foresight Flicker's roll modifier or Glimpse Future's initiative benefit. Soul Mark's record can remain while its directional information is blocked. The final clarification retains the source's creature eligibility: active creature-classified Undead/Construct targets are not excluded merely by type. Death/destruction/ended summoned existence ends the mark; ordinary shapechange or travel alone does not.

Omen Whisper limits materially equivalent inquiries across casters, while genuinely different material questions can receive another clue. Far Echo uses speech produced in its fixed capture sphere and actually audible at the center in the six seconds before casting. Read Surface Thoughts yields one actual current conscious thought after its save, not memories or forced truth. Detect Weather supplies an accurate current-trajectory forecast; a later actual new cause may alter it, with that cause recorded in the game. These are authored procedures, not a complete information/weather engine or balance certification. See [review status](DIVINATION_CANTRIP_REVIEW_STATUS.json).


## Mark Omen and Fate Coin: reviewed spell-specific rerolls

Mark Omen and Fate Coin share one guard: an original roll event and its entire replacement lineage may receive at most one reroll from either of these two spells, across all casters, coins, marks and recasts. Reserve this allowance at the first legal activation's commitment, not after the replacement die resolves. For a multi-die roll, the whole set/pool is one original roll event; the resulting attack's separate later damage roll is a different event. A shared area-damage roll remains one event even when applied to several creatures. Other exact class reroll features keep their own permissions and timing, but do not erase this guard or create a fresh lineage for these two spells. If competing declarations are simultaneous, use current initiative order; outside initiative use a fixed neutral table order chosen before the roll. Only the first legal commitment spends a mark/coin; a later declaration barred by this guard spends nothing. No new Action, roll event, cast, payment or duplicated outcome hook is created by replacing dice.

The [rank-1 Divination exact review](../../../../docs/audit/2026-10-08/full-game/GPT_DIVINATION_RANK1_EXACT_REVIEW.md) requires Fate Coin to wait until the **complete original roll event** is rolled and its faces are available under normal table information rules. It then replaces only one chosen die before consequences apply. Mark Omen replaces the caster’s complete attack d20 procedure before hit/miss resolution. Neither creates another attack/cast, rerolls an established resource reserve, reverses applied consequences or duplicates costs/hooks. A Well’s initial reserve die may be changed before the reserve is established. These two spell grants do not rewrite the Oracle, Mirrorsage or other class reroll contracts.

The same review preserves actual distant hearing, concealed-entrance revelation, creature sight through non-solid obscurity, willing memory-sharing, and actual faction/alignment/Corruption information. Warning Ward uses established hostility and an entry-triggered six-elapsed-second glow; it does not infer hostility from creature type or faction. Alignment Sense retains its source-defined rank-1 redundancy as an open balance question. [Review status](DIVINATION_RANK1_REVIEW_STATUS.json) records manuscript scope; no full information/roll-system runtime or human balance is certified.


## Rank-two Divination: paid information and preserved turn timing

The [exact review](../../../../docs/audit/2026-10-08/full-game/GPT_DIVINATION_RANK2_EXACT_REVIEW.md) requires **Locate Person, Faction Spy and Resonance Tracking** to resolve hidden person eligibility, plane/range conditions and trace existence after casting costs commit. Their legal Self inquiry/search must not reveal those facts through a free target-legality check. No-result feeds/bearings/searches do not diagnose the hidden reason or refund committed costs. This clarification is scoped to these exact card interfaces; other spells retain their printed target rules.

The [final timing clarification](../../../../docs/audit/2026-10-08/full-game/GPT_DIVINATION_RANK2_FINAL_CLARIFICATION.md) keeps **Vision Trap** consistent with the existing hostile/next-turn convention: its pending rider ends at the end of the target's first future regular turn, excluding the entire current target turn even if its end is still upcoming. An attack earlier than that endpoint can consume the rider normally. Existing virtual markers, outside-initiative six-second timing and end-phase-before-cleanup ordering remain unchanged.

Augury and Alignment Prediction supply bounded useful likelihood forecasts without forcing choices. Divine Perception requires actual divine provenance. Clairvoyance and Faction Spy provide only their specified fixed remote senses. Resonance Tracking preserves the original cast-start age of actual origin/path/endpoint traces; observing them creates no copied trail, new resource or refreshed age. [Review status](DIVINATION_RANK2_REVIEW_STATUS.json) records manuscript scope; wider information, provenance, runtime and numerical balance remain open.


## Rank-three Divination: initiative, remains and information

The [exact review](../../../../docs/audit/2026-10-08/full-game/GPT_DIVINATION_RANK3_EXACT_REVIEW.md) approves all eight cards without functional repairs. [Review status](DIVINATION_RANK3_REVIEW_STATUS.json) records their bounded manuscript scope.

**Future Echo** records a willing allied participant order and, at the next numbered round boundary, permutes surviving participants only among their existing regular baseline slots. Finish current end-round events, restore any prior Echo permutation while retaining legitimate other initiative changes, then apply pending schedules in stable application order. Earlier applications claim their eligible participants, including a singleton; later schedules skip those participants. Enemy/unselected slots stay fixed. A pending schedule suppressed or unavailable at its one execution boundary expires without makeup. Its execution commits a fixed one-round assignment rather than a state that can be dispelled midround to duplicate or skip turns. The baseline returns at the following boundary before another Echo is applied. Each participant still receives exactly one actual regular turn and its ordinary start/end procedure. Existing virtual duration, periodic, falling and absolute clocks do not migrate or replay. Outside initiative the spell has no scheduling effect. This is a tabletop procedure; the broader scheduler adapter and full Time Loop remain unimplemented/disabled as previously recorded.

**Speak with Dead** retains both school placements. Cast through Cleric, Mirrorsage, Ranger, Shaman, Wizard or Paladin as Divination; through Crimson Agent, Druid or Thief as Necromancy, under the actual selected class access. A Divination-only protection therefore does not automatically block its Necromancy placement. The spell uses a retained memory echo associated with actual remains/death context, not a summoned soul or resurrection. Old fragments do not automatically acquire memories from a later resurrected life. Hidden identity eligibility resolves after paid casting; currently living identities are ineligible. Five separate Action/question exchanges follow the casting Action within its one-minute window. Actual return to life or loss of the qualifying physical anchor ends the interview.

```

## S12

`DescentReviewChanges/ReviewBible/docs/mechanics/SPELL_INTEGRATION_RULES.md`
SHA-256: `256bb99fce3855a78b381577d7c4c1ec448c41d7cde79a6b238b01ca47ff35a3`
Location: lines 194–206
Reviewed Alignment Suggestion baseline and actual final Resonance Influence pricing.

```text
## Rank-one Enchantment: compulsion, alignment and final spell pricing

The [exact rank-one Enchantment review](../../../../docs/audit/2026-10-08/full-game/GPT_ENCHANTMENT_RANK1_EXACT_REVIEW.md) approves twelve cards without functional repairs. [Review status](ENCHANTMENT_RANK1_REVIEW_STATUS.json) records the manuscript scope and open runtime/balance work.

Mesmerize's Stunned package and unaware rider remain distinct. Sleep retains its no-save, ordered fixed24-current-HP budget; an attempted immune/guard-blocked target still spends its cost. A helper's physical rousing Action ends all ordinary Sleep applications on that creature, while unrelated Unconscious causes remain. Positive post-defense/pre-temp-HP damage wakes without undoing an already determined hit/critical. Confusing Flash and Command use actual existing Action/movement/interaction permissions, not added budgets, and replace their own pending same-spell applications rather than banking them. Their actual whole-Action components claim the shared source-character/target/encounter allowance when established; a blocked component receives no invented fallback.

Distract cancels a pending Action only after its commitment/beginning hooks and before its first main outcome, subject to its INT save and shared hard guard. Its independent opportunity-attack restriction ends with the current numbered round. If a nested effect already canceled the formerly valid parent, Distract cancels nothing and claims no hard allowance for that nonexistent cancellation. Costs/attempt history persist; Counterspell keeps its own reviewed scope. Hideous Laughter separately applies immediate Prone and maintained Incapacitated. Its repeat save occurs at every affected regular-turn END, including the current regular turn when affected; this is not its maximum-duration clock. Initially prevented hard control does not wait to activate later.

Pacify restricts voluntary attacks and selected damaging spell modes without a harm-ending clause. Voice of Peace snapshots its protected participating allies at application; actual recognition of the target's allies is checked when provocation occurs. Faction Charm keeps independent caster/target/faction affinity records, without stacked advantage or compelled allegiance. Enthrall affects all actual Perception checks of its up-to-three targets. Its separate Enchantment rank2/Core349 source remains preserved/unassigned, not an upcast or extra grant.

**Alignment Suggestion:** calculate each new one-step shift with all prior same-spell overlays ignored, retaining independent actual alignment changes. Only changed defined axes receive fixed overlay values. A no-change result creates no replacement; the caster's already-required concentration transition still occurs and never resurrects an old application. A valid changed-axis application replaces the previous same-spell application; replaced concentration maintains no remaining effect. Ending exposes the then-current underlying alignment, not a historical snapshot. No conduct, belief or oathbreaking is compelled.

**Resonance Influence:** compute ordinary legal spell price first, including mandatory extras, Dissonance, eligible source reductions/waivers and each feature's own minimum. Then apply final plus/minus1, minimum0. A feature's minimum1 reduction step is not a universal final-price floor. Ease can offset one RP of the resulting total, including a mandatory Resonance Shield extra. A genuine RP-priced spell reduced/waived to0 still qualifies; Burden makes it1. In Mage Spell Sharing, the Mage's earlier sharing payment is unchanged, while the ally's later actual shared spell is independently priced: Ease0/Burden1. An ally unable to pay cannot commit, leaves Influence pending, and still uses the original limited sharing window. Nonspell techniques and charge-only spells without an RP-price interface do not qualify merely because they have costs. Qualifying class discounts require their actual class/spell eligibility; examples do not reclassify nonspell techniques. No runtime implementation or numerical balance is certified by this manuscript ruling.
```

## S13

`DescentReviewChanges/ReviewBible/docs/mechanics/EQUIPMENT_ACQUISITION_PLAYTEST.md`
SHA-256: `406c68622102b444c6afb005e2d50cfd75171fe8d90db36a06d02df2d67bf27d`
Location: lines 19–62
Armor surcharge and true V/S/F/body/focus constraints.

```text
One usable equipped shield contributes its printed bonus: buckler +1, shield +2, tower shield +3. No second shield bonus. Elven weave's printed Stealth advantage uses ordinary advantage/disadvantage cancellation. Dwarven plate is AC 18; its descriptive superior protection adds nothing. Scale mail's description adds no slashing resistance. Tower shield adds no unprinted cover or additional movement penalty.

**Nonproficient worn armor.** Retain V6 disadvantage on STR/DEX ability checks, saving throws and attacks. Core replaces the older casting prohibition: spells remain permitted, but an RP-priced spell costs +1 RP once per cast and concentration checks/saves have disadvantage. Multiple nonproficient armor pieces never multiply this surcharge. A normal 0-RP spell using the RP price interface can cost 1 RP. Apply this ordinary price addition before the already reviewed eligible reductions and final Resonance Influence step.

**Nonproficient shield — new completion.** While using a shield without shield proficiency, apply the STR/DEX check/save/attack disadvantage. A shield alone adds neither Core's armor RP surcharge nor concentration disadvantage and does not prohibit casting. Core names worn armor for those casting penalties.

A charge-only ancestry spell, Oracle effect or other cast with no RP-price interface acquires no RP price or pool from nonproficient armor. Actual concentration still has disadvantage from nonproficient worn armor. Hands, spell components and other independent casting restrictions remain.

**Strength minimum — new completion.** If one or more equipped armor/shield records have a listed STR minimum you do not meet, reduce Speed by 10 feet total, minimum 0. This is not a minimum to equip; multiple deficient pieces do not stack the reduction. This penalty can coexist with Load/Burden.

The Dwarf's printed rule that Speed is not reduced by wearing heavy armor prevents this penalty when the deficient item is heavy armor. It does not waive Load/Burden, another movement penalty or a tower shield's separate STR minimum. If a table chooses V6's preserved optional encumbrance alternate, that alternate ignores the Armor Table Strength column; the active reviewed Load procedure is not that alternate.

| Equipment | Don | Doff |
|---|---|---|
| Light armor | 1 minute | 1 minute |
| Medium armor | 5 minutes | 1 minute |
| Heavy armor | 10 minutes | 5 minutes |
| Any shield | 1 Action | 1 Action |

One actual assisting creature halves doff time only; a shield still takes at least one Action. Additional helpers do not repeatedly halve it.

## Hands and focuses

A buckler straps to one forearm. Its partially available hand can carry a small nonweapon object, but supplies no free S hand, loading hand, second-weapon attack, two-handed weapon support or active focus manipulation. An ordinary shield or tower shield occupies one hand. Soldier Shield Trained is a specific selected-feature exception for its repeating-crossbow/strapped-shield use, with that feature's actual reload requirements.

A two-handed weapon requires both hands when attacking with it. Releasing one grip costs no Action; regripping is part of its next legal use. This does not free a hand already occupied by another object, restraint or incompatible anatomy.

F requires an actual focus legal for the casting source. A hand holding only that focus may manipulate it and supply S for the same cast; the focus itself is not a conflicting object. A weapon, shield, second object, loading requirement or other hand restriction can make that hand unavailable. An item independently serving as both weapon and focus can use this rule only when an actual source authorizes that item as the caster's focus.

A holy symbol may supply F while held, visibly worn or borne on a shield where that casting source permits holy symbols. A worn or shield-borne symbol does not supply a free S hand. V still requires actual audible speech, and neither a focus nor component pouch waives explicitly priced or consumed materials. The component pouch supplies its ordinary storage function; this guide does not give it a new universal F substitution.

The following focus assignments are **new class integration** for actual legal class spells requiring F. They grant no spells or resource pools. Exact class features may override their own focus rules.

| Casting class | Ordinary focus |
|---|---|
| Bard | One actual instrument |
| Cleric, Paladin | Holy symbol |
| Druid, Shaman, Ranger | Druidic focus |
| Mage, Wizard | Arcane focus |
| Mirrorsage | Steel mirror |
| Oracle | Divination token |
| Crimson Agent, Dragoon, Monk, Thief, Tinker | Token for that class |

Soldier and Warrior gain no spellcasting from focus ownership. An ancestry casting token remains ancestry-grant scoped and cannot substitute for a class focus. An explicitly granted ordinary background arcane focus or holy symbol retains its normal equipment function for a casting source already entitled to that focus category.
```

## S14

`DescentReviewChanges/ReviewBible/data/public/class_playtests/wizard.json`
SHA-256: `8ab2f4f43bcbced418fb266e5bd3216cff491b0c442c16f93438bd3556672c8b`
Location: /engine
Full actual Wizard engine: prepared-matrix exemption, copy/action guards, explicit concentration exceptions and source gates.

```json
[
  "PROVISIONAL PLAYTEST CONTRACT. Intelligence is the Wizard class ability. S = 1/2/3/4 at Wizard levels 1/5/11/17. M = max(1, Intelligence modifier). Wizard spell attack = d20 + normal character proficiency bonus + Intelligence modifier. Wizard spell save DC = 8 + normal character proficiency bonus + Intelligence modifier.",
  "The Wizard remains three distinct stages: Base Wizard at levels 1-2, Arch Arcanist at levels 3-9, and one Hero path at levels 10-20: Spellbinder, Elementalist or Necromancer. Hero paths are not additional starting classes and their features cannot be selected before their Wizard class-level gates.",
  "SPELLBOOK. At Wizard 1 your spellbook contains six chosen rank-1 Wizard spells. Arcane School Specialization also adds one legal rank-1 bonus spell of your chosen school without replacing one of those six. For this provisional progression, add 2 legal Wizard spells to the book at each Wizard level 2-4, 3 at each level 5-8, 4 at each level 9-12, 5 at each level 13-16 and 6 at each level 17-20. Level-up additions cost no money or scribing time.",
  "LEGAL RANKS. Maximum Wizard spell rank by Wizard class level is: rank 1 at levels 1-2, rank 2 at 3-4, rank 3 at 5-6, rank 4 at 7-8, rank 5 at 9-10, rank 6 at 11-12, rank 7 at 13-14, rank 8 at 15-16 and rank 9 at 17-20. Grand Tier at level 20 is a special casting permission, not a tenth ordinary rank. A Wizard may learn Wizard-list spells from any school up to the legal rank unless a spell itself has an additional prerequisite.",
  "PREPARED SPELL MATRIX. After a long rest, prepare a number of matrices equal to Wizard level + Intelligence modifier, minimum 1, selecting only spells currently recorded in your spellbook and within your legal rank. You cast ordinary Wizard spells only from prepared matrices unless a feature explicitly overrides that restriction. Preparing the full daily matrix set normally requires 1 hour of spellbook study. Matrix Efficiency reduces this to 45 minutes.",
  "DUPLICATE PREPARATION. You may prepare the same spell more than once, primarily to carry different Matrix Mastery configurations. Duplicate copies never create additional first-cast Dissonance exemptions. For Refrain and the protected strain rule, all prepared copies sharing the same underlying spell name belong to one matrix family regardless of modification.",
  "MIDDAY SUBSTITUTION. Once between long rests, you may perform a 10-minute Spellbook Study ritual to replace one prepared matrix with another legal spell from your spellbook. The replacement cannot exceed your legal Wizard rank. Sigil Rewrite and Matrix Mastery may improve this process as explicitly stated.",
  "SPELL ACQUISITION BY SCRIBING. A found Wizard spell may be copied into the spellbook if its rank is legal for you. Baseline scribing requires 2 hours and 50 gp of inks/materials per spell rank, treating rank 0 as 1 for this calculation. Spell Scribing halves both values to 1 hour and 25 gp per rank. Failure to finish the work consumes no spellbook entry but materials already expended during an interrupted hour are lost.",
  "SPELLBOOK LOSS. Losing the spellbook does not erase matrices currently prepared in memory; you may continue casting those prepared matrices until you next rebuild or change preparation. A blank replacement book can be seeded with your currently prepared spells at 1 hour and 25 gp per effective spell rank each. An unprepared spell you previously recorded can be reconstructed from memory with 8 hours, 100 gp per rank and an Intelligence (Arcana) check against DC 10 + spell rank. Failure consumes that attempt's time and half its materials; another attempt can be made after a long rest. Recovering the original book automatically restores access to its surviving entries.",
  "ARCANE SCHOOL SPECIALIZATION is automatic at Wizard 1. Choose exactly one of the eight schools. Your spell attacks with that school gain +1 and your Wizard save DC for that school's spells gains +1. You also add one legal rank-1 spell of that school to the spellbook. The source table explicitly supplies seven school passives; the eighth core school, Abjuration, is named elsewhere but its passive row is missing. Its provisional playtest passive is identified below rather than silently presented as recovered text.",
  "ABJURATION, provisional completion for the omitted eighth row: once per round after you cast an Abjuration spell, gain temporary HP equal to PB until the start of your next regular turn. CONJURATION: creatures summoned by your Wizard spells gain +1 maximum HP per Wizard level. DIVINATION: once per long rest reroll one failed saving throw and use the new result. ENCHANTMENT: when a creature fails its initial save against one of your Enchantment spells, a printed control duration of at least 1 round may last one additional round, but every normally allowed repeat save still occurs. EVOCATION: when casting an area Evocation spell, exclude one creature from its initial damaging area; that creature automatically succeeds and takes no damage if success normally halves damage. ILLUSION: gain +2 on concentration saves made to maintain Illusion spells. NECROMANCY: once per turn during a real encounter when a hostile non-summoned creature dies from your Necromancy spell, gain 1 temporary HP; it is not permanent healing. TRANSMUTATION: after casting a Transmutation spell, gain +5 feet Speed until the end of that turn.",
  "PROTECTED DISSONANCE INTERFACE. The first cast of each different prepared matrix family during an encounter generates 0 BASE Dissonance. This exemption affects only base strain. Refrain and explicitly printed strain costs still apply; the suite disables generic Overcast and does not layer historical Burn onto Dissonance. Repeating a matrix family follows normal Refrain immediately. Preparing duplicates or differently modified copies of the same underlying spell never refreshes the exemption.",
  "Core Systems V 2 Resonance Points and spell-rank RP costs are authoritative for Wizard spellcasting. There are no historical spell slots in this pilot. Wizard cards tagged wizard-spell are always-prepared class matrices once acquired, do not consume a daily prepared-matrix position and use the same RP, concentration, Refrain and protected first-distinct-matrix rules as other Wizard spells. Their printed RP cost replaces any generic rank cost; never pay both.",
  "RITUAL CASTING is automatic at Wizard 2. A Wizard spell in your spellbook with the Ritual tag can be cast from the book without being prepared by increasing its casting time by at least 10 minutes. A ritual cast costs 0 RP unless that ritual explicitly lists a consumed RP cost, cannot be used during an encounter and cannot generate or vent Dissonance through ordinary casting strain.",
  "Only one concentration effect can normally be maintained. Starting a second concentration effect ends the first. Damage uses the current Core Systems concentration rule; required half-damage rounding is down for this pilot. Spell Tether and the level-17 Tethered Cast are the only Wizard-specific exceptions in this draft, and each has an explicit RP price, duration and one-tether cap.",
  "MATRIX MASTERY MODIFICATIONS. After acquiring Matrix Mastery, each prepared ordinary spell matrix may carry at most one modification chosen during preparation. QUICK SUBSTITUTION: once per short rest, replace one matrix marked Quick Substitution with another spellbook spell of exactly the same rank using a 1-minute ritual instead of the normal 10-minute midday swap; the replacement loses the modification until the next long rest. COMPONENT ENHANCEMENT: when casting a damaging or healing matrix, spend 1 additional RP to add one extra die of the spell's primary damage or healing die to one roll; if the spell has no such die this modification has no effect. MATRIX LINKING: pair two different prepared matrix families during preparation; after legally casting one, the other costs 1 less RP, minimum 1, if cast before the end of your next regular turn, at most once per pair per round. STABILITY REINFORCEMENT: gain +2 on concentration saves caused by damage while maintaining that matrix. A matrix modification never creates another spell cast or proc event.",
  "All sources share a maximum of one additional full Action per creature per round. Additional Actions cannot grant another additional Action, Bonus Action or Reaction. Spell copies, Matrix Sharing, Arcane Fusion, Dual Cast and similar effects pay all explicitly required RP and do not produce duplicate resource, cast-proc or action-grant chains beyond their written resolution.",
  "Round recharge counters decrease once at the start of your regular initiative turn even if you cannot act. Extra Actions and extra turns do not tick recharge. Outside initiative, each uninterrupted 6 seconds counts as one tick. Only positive counters can be reset or shortened and each named ability can receive at most one reset or shortening per round.",
  "SUMMON COMMAND LIMIT. All Wizard-controlled conjured, raised and bound companions share one damaging/control Companion Command per Wizard regular turn. Spend one Bonus Action to command exactly one such creature to move up to its Speed and use one damaging or control action from its stat block. Uncommanded creatures may reposition defensively and take Dodge but cannot deal damage or impose conditions. No summoned or raised creature can create XP, treasure, RP, Dissonance relief, additional corpses or kill-resource farms.",
  "NECROMANCER STANDARD UNDEAD. Corpse Harvest and Auto-Raise share a maximum of three standard raised minions. Skeleton: AC 14, HP 6 + 2 × Wizard level, Speed 30; Bone Shot, range 30 feet, Wizard spell attack, 1d6+S necrotic. Zombie: AC 12, HP 10 + 3 × Wizard level, Speed 20; Slam, reach 5 feet, Wizard spell attack, 1d8+S necrotic. Goblin Thrall, available only from a goblinoid corpse: AC 13, HP 8 + 2 × Wizard level, Speed 30; Shiv, reach 5 feet, Wizard spell attack, 1d6+S necrotic. These are pre-Flesh-Ascendant statistics.",
  "NECROMANCER AUTO-RAISE. Once per round when one of your standard undead minions personally lands the killing blow on an eligible humanoid and your standard-minion count is below three, its corpse rises at the end of the current turn as the same mechanical minion type that scored the kill, if physically possible. A new minion cannot act during that same round. Auto-Raise costs no Action or RP but can never exceed the three-minion cap or generate a new resource, corpse chain, XP or treasure event. Without Infernal Pact only humanoids qualify.",
  "ELITE UNDEAD PETS. Necromancers may bind Boneflayer, Dreadblade and Wraithbound, at most one of each and three elite pets total. They use the same shared Companion Command limit as standard undead. Boneflayer: AC 14, HP 12 + 2 × Wizard level, Speed 30. Bone Shards: range 60, Wizard spell attack, 2d6+S necrotic. Fear Pulse replaces its attack: enemies within 10 feet make Wisdom saves; failure Frightened until end of next turn; recharge 3. Grave Miasma replaces its attack: 10-foot-radius point within 30 feet until start of your next turn; enemies entering or starting there take 1d6 necrotic once; recharge 3.",
  "Dreadblade: AC 16, HP 16 + 3 × Wizard level, Speed 30. Disrupting Blade: reach 5 feet, Wizard spell attack, 1d8+S necrotic; a concentrating target immediately makes its concentration save with disadvantage. On a natural 20 the target is Weakened until the end of its next turn, taking -1 on attack rolls. Dreadblade has advantage on saves against forced movement.",
  "Wraithbound: AC 14, HP 10 + 2 × Wizard level, Fly 40 and hover. While it has not attacked or imposed control since the end of its previous turn it is Invisible; attacking ends that state until the end of its next turn. Wraith Strike: reach 5 feet, Wizard spell attack, 1d8+S necrotic. On natural 20 the target makes a Constitution save against your Wizard DC; failure Stuns until the end of its next turn.",
  "Flesh Ascendant's bonus applies after the listed base statistics: every undead creature you control gains +2 maximum HP per Wizard level. If at least two of your undead creatures are active, each gains +1 AC and +1 on saving throws. This does not increase the standard-minion or elite-pet caps.",
  "DARK-TRAUMA INTERFACE. Necromancer features involving corpse desecration, infernal bargains, domination, body control or Mind Prison remain subject to the project's existing dark-content and trauma boundaries. A table may fade description to black without changing mechanics. No feature changes a player's real belief, permanently transfers ownership of a player character or silently retires a PC.",
  "PROPOSED ACQUISITION. Wizard 1 automatically gains Arcane School Specialization, Spell Matrix System and the starting spellbook, then chooses 4 selectable Base cards, at least 2 Active. Wizard 2 automatically gains Counterspell and Ritual Casting, then chooses 2 additional selectable Base cards. Counterspell is not also placed in the Arch selection pool.",
  "At Wizard 3 enter Arcanist, automatically gain Arcane Tradition as an upgrade of the SAME level-1 school rather than choosing another school, and choose 2 selectable Arch cards, at least 1 Active. Wizard 4 grants one eligible Base/Arch choice. Wizard 5 grants one Base/Arch choice plus automatic School Mastery. Wizard 6 grants one Base/Arch choice plus automatic Arcane Ward. Wizard 7 grants one eligible Arch choice. Wizard 8 grants one Base/Arch choice. Wizard 9 grants one eligible Arch choice plus automatic Dual Cast.",
  "At Wizard 10 choose Spellbinder, Elementalist or Necromancer and gain 2 Hero cards from that path. ELEMENTALIST EXCEPTION: Elemental Affinity is automatic at path selection and counts as one of those two level-10 Hero acquisitions, so an Elementalist chooses only one additional Hero card at level 10. Levels 11, 13, 15, 17 and 19 each grant one eligible unselected Base/Arch choice. Levels 12, 14, 16 and 18 each grant one Hero-path choice. The chosen Final Theorem is automatic at Wizard 20. School Mastery, Counterspell, Arcane Tradition and all progression-table automatic features are never duplicated as selections.",
  "All acquisition gates use Wizard class level rather than total character level. Normal proficiency bonus follows the game's ordinary total-character-level rule. A multiclass dip cannot unlock higher spell ranks, Arcanist cards, Hero cards, Final Theorems or progression-table features.",
  "Class matrices tagged wizard-spell receive a rank in normalized card data equal to maximum ordinary Wizard rank at their minimum class-level gate (cap 9). Printed RP cost replaces generic rank cost. Counterspell is rank 1 at its explicit level 2 automatic grant. This explicit convention closes rank-dependent Counterspell/Dissonance interactions without inventing extra costs.",
  "Cantrip completion: know 3 Wizard cantrips at 1, 4 at 4, 5 at 10, using the shared missing-repertoire fallback. Cantrips are known directly and do not consume prepared matrices. Always-prepared class matrices are additional cards, not extra arbitrary ordinary spells. Class spell ranks and the normalized activation field resolve incomplete source terminology."
]
```

## S15

`DescentReviewChanges/ReviewBible/data/public/class_playtests/shaman.json`
SHA-256: `c88fcad8c14734cc852a95aee7b3686fd64ea2a8cfb9d014f4297b7efec94a62`
Location: /engine
Actual Shaman ordinary-spell totem reduction and Bloodcaller loss of ordinary casting.

```json
[
  "Wisdom is the class ability. Choose Elemental Affinity automatically at 1: Fire, Ice, Air or Earth. Spellcasting/RP remain separate from Totem objects and flasks. Totem capacity 1, rises 2 at 13; any third replaces one of your existing totems. A totem is a visible Tiny magical object: AC 12+PB, HP 2 L, immobile, immune to poison/psychic/conditions, vulnerable to ordinary weapon and other damage. At 0 HP its aura ends. A new totem appears within 30 ft; cannot occupy a creature's space, serve as a bridge, trap a creature without a save or move through walls.",
  "Totem Casting is Action 2 RP, duration 3 of your turns, 15 ft aura. Choose Flame, Stone, Frost, Spirit or Renewal. Benefits require an ally/target in the aura, maximum 3 creatures benefiting per pulse/round chosen by you. Flame adds 1 fire to an ally's first direct weapon hit per round; on critical that target Burns 1d4 next turn. Stone reduces damage by 1 and gives enemies-1 to STR checks to shove. Frost: enemy first entering/starting each round makes CON save or Speed-10 ft until end its turn. Spirit: first necrotic/hex damage per target per round adds 1. Renewal: on start and each of next 2 turns with Bonus Action+1 RP maintenance, up to 3 allies regain 2 HP. Thus Renewal total cost 4 RP for 3 pulses; no free healing on entry. All totems share one concentration burden; losing it ends all. Other concentration effects replace them. Non-Renewal auras need no Bonus Action upkeep. Multiple same-name/stat auras do not stack.",
  "On your turn you may spend Bonus Action to move one totem up to 15 ft along unobstructed ground, remaining within 60 ft. This competes with healing maintenance, companion commands and advanced flasks. Moving an aura over a creature cannot trigger its once/round effect repeatedly. Totem destruction creates no resource return. Once per round, the first ordinary spell cast while inside your own active totem aura generates 1 less Dissonance, minimum 0; no RP reduction.",
  "The book places Flask Use at Base but describes advanced flask casting as Theurgist/Soothsayer-only. For this draft, Base Flask Use grants mundane prepared tactical flasks thrown with an Action; at Hero 10 only Theurgist/Soothsayer gain magical Bonus Action flasks. Bloodcaller retains mundane alchemical knowledge, not the advanced flask subsystem. At long rest prepare 2 flasks, rising to 3 at 5 and 4 at 11; no encounter refill or stockpiling, total carry cap 4, unused contents become inert when preparing a new batch. This finite-rest supply replaces encounter-based free heal farming.",
  "Flask tier uses S. Mundane Base modes: Burn=one enemy 30 ft DEX save S d6 fire half, failure 1d4 fire next turn; Root=one ground enemy 30 ft STR save Speed 0 until end its next turn; Weaken=one enemy 30 ft CON save or-1 attack damage until end its next turn. Advanced Hero modes additionally: Stun=one enemy 30 ft CON save or no Reactions, failure by 10 Stunned until end its next turn; Heal=one living ally 30 ft S d6+M HP; Restore=end Frightened or Poisoned on one ally 30 ft. Every thrown flask consumes one prepared unit and 2 RP for advanced magic (Base mundane flasks cost 0 RP). Changing payload requires no separate crafting action when throwing. No flask leaves harvestable poison or another flask.",
  "Choose Fire/Ice/Air/Earth bonuses through affinity card; Ember/Cold/Shock damage are fire/cold/lightning, Earth uses bludgeoning. Summoned elemental spirits use one standard companion each, maximum one normally; Elemental Chorus expressly summons a package of 4 but all share one Bonus Action command and a printed combined pulse. Companions cannot generate RP, trigger flask refunds or create corpse/kill farms.",
  "Bloodcaller at Hero 10 transforms permanently into Hagraven, with the player choosing this class path and its stated loss of ordinary Shaman spellcasting. It does NOT lose its RP reservoir: printed Hagraven/Totem techniques still pay RP, but it cannot cast ordinary Shaman spells or advanced magical flasks. It retains prior totem/technique selections. The change is a class choice, not permission for involuntary player-character conversion; ancestry identity and player control remain. At long rest it can prepare mundane flasks only if Base Flask Use is known.",
  "Shaman Base 1–2, Spiritwalker Arch 3–9, and Theurgist/Soothsayer/Bloodcaller Hero 10–20 remain separate stages. Elemental Affinity is automatic 1, not an extra selection cost. No explicit Arch capstone in source:9 has its ordinary choice. At 20 your selected Hero's last active ultimate gains the explicit new capstone improvement below; no new generic Hero class is invented."
]
```

## S16

`DescentReviewChanges/ReviewBible/data/public/class_playtests/mirrorsage.json`
SHA-256: `9179729dd39e0a81f4f6d78b9fbb0c7fb296fb5d418aaa238d7ff6aa02b2bd3a`
Location: /engine
Different class Echo archive/release, bounded copying and no resources/recursive echoes.

```json
[
  "Intelligence is the class ability; use d8 Hit Die from the detailed book, recording the older runtime d6 as superseded for this draft. You begin with 3 empty Echo Slots. Expansion II raises ordinary capacity 5; Sacred/Floating memory features may add one restricted slot, but total concurrent stored Echoes never exceeds 6. Slots are storage, not spell slots. Releasing normally empties that record. Rest restores RP, not spent Echoes. Starting a new encounter does not duplicate the archive.",
  "Mirrorbind is an Action, once per encounter, against a creature within 60 ft whose eligible ability you saw resolve since the start of your previous turn. Target must have INT 6 or lower, not be a boss or possess unique/legendary status unless an encounter script explicitly permits copying. It makes WIS save versus class DC; failure captures one witnessed ability into an empty slot. No copying from allies, your companions, another copy, a corpse, a recharge-limited legendary power or an at-will source that itself restores resources. You can voluntarily erase a slot without an action on your turn, permanently losing its record.",
  "Record source creature/name, witnessed ability, category, damage type, allowed rank, capture encounter and whether first release has occurred. For this pilot, capture copies the observed role into ONE bounded profile: Strike=one target 60 ft class spell attack S d8 observed damage type; Burst=up to 3 enemies in 10 ft radius within 30 ft DEX save S d6, half on success; Mend=one living ally 30 ft S d6+M HP; Ward=one ally 30 ft S d6+M temporary HP for 1 minute; Hindrance=one enemy 30 ft WIS save or Speed-10 ft and no Reactions until end its next turn. Choose only a profile actually expressed by the observed source; physical attack cannot become healing. Rank is max(1, ceil(source challenge rating/2)); if source lacks a rating the Director assigns a rank before the encounter, not after seeing a desirable ability. Rank cannot exceed your Mirrorsage learnable rank; no copying character levels from a creature. Damage/targets/control are capped by these profiles, not source boss dice.",
  "Echo Release costs the Core V 2 RP cost of the recorded rank, minimum 2, consumes its record and counts as a spell for Dissonance and Refrain. Spell attack/DC use your own stats. First release of a newly captured record ignores Refrain addition only; base strain remains. Any preserved subsequent release uses ordinary repeated-spell strain. All released Echoes, pet replays, fusions and reflections share ONE release action per round; a specifically combined package counts once but pays for every component and has its printed damage cap. Copies cannot create resources or recursive Echoes.",
  "One Mirror Beast OR Reflective Companion, never both. Mirror Beast uses standard companion stats, initially copies appearance only, and costs a Bonus Action to command. You may command it to make its normal attack OR originate your round's Echo Release from its position, paying RP and consuming the record normally; not both. You still supply an Action for release unless a feature specifically changes that action cost. A shifted appearance grants no extra actions/stats. Destroying/dismissing it grants no capture, corpse, XP or recovery. Charm Bind is 1/long rest, 3 rounds, concentration, INT 6-or-lower target WIS save and repeat at each turn end/when harmed by your side; never a player character or boss without explicit encounter permission. A charmed companion uses its own ordinary attack with damage capped at standard companion S d6; unique spells/powers remain unavailable.",
  "Focus Point is a separate resource: when Mimicry Focus is known, receive 1 at encounter start, maximum 1, lost at encounter end. It can modify one Echo without generating another release, recapture or resource refund. No stacking damage doublings; use the printed modest die/range boost. Healing/support copies always consume RP and cannot restore RP or duplicate limited-use features.",
  "Standard acquisition applies; baseline Mirrorbind, Echo Release and summon procedure become usable by selecting their cards. Echo Channeling and Mirrorcall are upgrades, not duplicate mandatory unlocks. The contradiction between source initial 3 slots and Expansion I 2→3 is reconciled as an archive-safety upgrade below. Perfect Reflection automatic 9, Hero choice 10, corresponding Final 20. The finale does not override copy eligibility or the shared release cap."
]
```

## S17

`DescentReviewChanges/ReviewBible/data/public/class_playtests/cleric.json`
SHA-256: `25387b0dcfae0d53d689486d4b05d8ef5b24bed1b70f0baab970a82dbd370f89`
Location: /engine
Actual Cleric abilities/RP and independent Conviction/casting predicates.

```json
[
  "PROVISIONAL PLAYTEST CONTRACT. Wisdom is the Cleric class ability. S = 1/2/3/4 at Cleric levels 1/5/11/17. M = max(1, Wisdom modifier) unless a feature explicitly substitutes another ability. Cleric technique attack = d20 + normal character proficiency bonus + Wisdom modifier. Cleric technique save DC = 8 + normal character proficiency bonus + Wisdom modifier.",
  "Conviction is separate from Resonance Points. Base Conviction maximum is 3, automatically becoming 5 at Cleric 9; after a long rest you begin at your current maximum. A completed short rest restores 1 spent Conviction, to the maximum. A completed long rest restores all Conviction. Conviction Pool raises the maximum by 2. Conviction persists between encounters; simply declaring prayer, repeating a Rite, or performing harmless actions outside a real encounter never generates Conviction.",
  "Only explicit features generate Conviction. Sacred Chant, Sermon of Purpose, Doctrine Shield, Dark Conviction and other printed cards are valid generators. A feature cannot generate more Conviction than its text permits, and Conviction can never exceed the current maximum. Summoned creatures, friendly creatures, trivial creatures, repeated corpse manipulation and staged out-of-combat actions cannot be used to farm Conviction.",
  "Cleric techniques use only their printed RP and Conviction costs. All RP is paid from the Cleric's Core Systems V 2 Resonance Point pool. A Cleric technique is not automatically an ordinary spell-rank cast and does not receive Overcast, spell-slot, cost-discount or spell-proc benefits unless a feature explicitly says otherwise. Ordinary spells continue to use Core V 2 spellcasting rules.",
  "Protected Dissonance interaction: once on each of your regular turns, when you spend at least 2 Conviction on a Rite or Invocation, reduce Dissonance by 1, minimum 0. The expenditure must actually occur; waived Conviction costs do not vent Dissonance. A single feature expenditure vents at most once even if it spends more than 2 Conviction. No Cleric card automatically adds Dissonance unless explicitly written.",
  "One concentration effect may be maintained at a time. Starting another concentration effect immediately ends the previous one. Damage uses the current Core Systems concentration rule; for this pilot, if a division requires rounding, half damage is rounded down. Sustained Cleric effects use their printed maintenance cost and Bonus Action. A control effect that persists for multiple pulses or rounds gives the target a new save at each printed pulse or at the end of each affected turn as stated.",
  "Round recharge counters are set after resolution and decrease once at the start of the Cleric's regular initiative turn, even if the Cleric cannot act. Extra Actions and extra turns do not create extra recharge ticks. Outside initiative, each uninterrupted 6 seconds counts as one recharge tick. Only a positive counter may be reset or shortened, and a named ability can receive at most one reset or shortening per round.",
  "Healing cannot exceed maximum HP, does not remove Wounds, and does not restore a dead creature unless a card explicitly says it resurrects. No Cleric feature provides unlimited permanent HP or resource restoration outside encounters. Temporary HP does not stack with itself; use the higher value. Resurrection and corpse-based effects have explicit use limits and cannot generate repeatable corpses, XP, loot or Conviction.",
  "Invocation Attunement is gained automatically at Cleric level 2. Choose exactly one Invocation Path: Radiance, Judgment, Renewal, Flame, Veil or Echoes. Only the selected path bonus becomes active. Divine Invocation uses the mode belonging to that selected path unless another feature explicitly permits a different mode. Changing Invocation Path requires a future explicit retraining rule; this draft provides none.",
  "PROPOSED ACQUISITION FOR PLAYTEST. Cleric 1: gain the Divine Favor engine and choose 4 Base cards, at least 2 Active. Cleric 2: automatically gain Invocation Attunement and the selected Invocation Path bonus, then choose 2 additional Base cards. Cleric 3: enter Bishop and choose 2 Arch cards, at least 1 Active. Levels 4-8 each grant one eligible Base/Arch choice, respecting each card's minimum class level. Level 9 grants one eligible Arch choice plus Bishop's Mandate automatically. Level 10 choose Saint, Priest or Cultist and gain 2 Hero choices from that path. Levels 12, 14, 16 and 18 each grant one additional Hero choice; levels 11, 13, 15, 17 and 19 grant one eligible unselected Base/Arch choice. The chosen Hero Finale is automatic at Cleric 20. ASI/feat milestones remain separate and do not consume these choices.",
  "All acquisition gates use Cleric class level, not total character level. Proficiency bonus still follows normal total-character-level rules. A multiclass character cannot use non-Cleric levels to unlock Bishop, Hero, Invocation or Finale features. Divine commands, visions and social abilities can influence actions only to the extent their exact mechanical text states; no Cleric feature can force a player character to adopt, abandon or profess a belief.",
  "Capacity clarification: the automatic level 9 Conviction increase is a new draft completion so every Hero can pay its 5-Conviction Finale without buying Conviction Pool. Conviction Pool adds 2 at any level, yielding 5 early or 7 from 9. It never fills gained capacity immediately."
]
```

## S18-alignment-suggestion

`CURRENT_DIVINATION_RANK7_REVIEW_INPUT.json`
SHA-256: `0f6a122b915e8bceb7c7ae9eb9243fcf2ec51b28bd1c3f4c4a686e02a79e89d8`
Location: /completeCurrentCounterparts/1/completeCurrentAuthoredRecord/operational
Complete reviewed counterpart; source status and exact scope retained, no promotion from comparison.

```json
{
  "id": "alignment-suggestion",
  "activation": "Action",
  "rangeFeet": 30,
  "targets": "One creature you perceive within30feet and line of effect. No requirement that its alignment be known; hidden canonical axes are resolved after paid casting.",
  "duration": "Concentration, up to1minute. In initiative, expires at the caster's tenth future regular-start marker after application; an already-passed start never counts. Outside initiative, expires after 60 elapsed seconds. Retain the original virtual phase or absolute deadline through initiative changes, absence and planar travel; moving between timing modes does not reset it.",
  "concentration": true,
  "components": [
    "V",
    "S",
    "F"
  ],
  "resolution": "The target makes a Wisdom save. Success: no new overlay. Failure: snapshot your actual current alignment orientation. For each axis defined both for you and for the target, compute one step toward your snapshotted value along Lawful–Neutral–Chaotic and Good–Neutral–Evil. Compute the target baseline without any previous Alignment Suggestion overlay on that target, retaining all independent actual alignment effects/records. An already matching or undefined axis gains no changed-value overlay. If at least one axis changes, replace the prior same-spell overlay with the new recorded axis values/deadline. A failed-save cast that changes no defined axis creates no new overlay and does not itself replace a valid older one; mandatory concentration transitions remain independent.",
  "effect": "The changed values are the target’s actual effective canonical alignment for rules that query those axes during the overlay, including real alignment-gated spells/items. Example: baseline Chaotic Evil targeted by a Lawful Good caster becomes Neutral Neutral; one such overlay never jumps two steps. Its values remain fixed until expiry/removal/replacement and do not recompute every time another underlying record changes. Unchanged/unoverlaid axes follow their actual underlying records. An independent effect such as Corrupted can change underlying alignment while this spell persists; that change remains and is exposed when the applicable overlay ends. One Alignment Suggestion overlay per target across casters; recasting cannot use its old overlay as a staircase for another same-spell step.",
  "scaling": "None. No automatic increase in range, targets, duration, magnitude or uses.",
  "limitations": "The spell grants no automatic knowledge of either character’s axes, including whether a value changed. Actual information protections still govern observations. It never compels matching behavior, belief, confession, loyalty, PvP, personality or oathbreaking; conduct clauses still judge actual conduct. Ending removes only this overlay, without restoring an old alignment snapshot, deleting independent changes or reviving a replaced overlay. Caster orientation is fixed at application, not tracked through later caster changes. Ward tag creates no ward. More specific alignment-changing effects retain their actual interaction rules; this card does not invent a general priority engine for every unrelated overlay. Actual class access/repertoire, costs, components, Dissonance/Refrain, concentration transitions and cast/counter order follow SPELL_INTEGRATION_RULES.md. Pay a legal cast before effect resolution; failure/countering refunds nothing and restores no displaced concentration. V is audible, S requires the ordinary usable hand, and F is the normal class focus. Saves use the actual casting class's spell DC and binary save rules. Creature type alone supplies no mental immunity; Charmed-only immunity does not block effects that never impose Charmed. Actual broader defenses retain their written scope. No automatic scaling, generic upcast or free identification of hidden eligibility.",
  "designNotes": "PRESERVED: Action/30feet/V,S,M/F as focus, WIS, concentration minute and actual push toward caster alignment. NEW: temporary canonical one-step overlay on both eligible axes. Exact-review proposals: compute without previous same-spell overlay to prevent recast ratcheting, overlay only genuinely changed axes, fixed values, and no new application when no defined axis changes; independent base changes survive ending.",
  "implementationStatus": "REVIEWED authored operational PLAYTEST manuscript; runtime, human balance and broader Enchantment/social-control integration pending",
  "sourcePlacements": [
    {
      "name": "Alignment Suggestion",
      "school": "Enchantment",
      "level": 1,
      "summary": "Subtly push target toward your alignment (WIS save)."
    }
  ],
  "sourceCoreEntries": [
    {
      "index": 340,
      "original": {
        "school": "Enchantment",
        "level": 1,
        "name": "Alignment Suggestion",
        "effect": "Subtly push target toward your alignment (WIS save).",
        "source_paragraph": 9400,
        "casting_time": "1 action",
        "range": "30 feet",
        "duration": "Concentration, up to 1 minute",
        "components": "V, S, M/F",
        "resolution": "Wisdom save",
        "tags": [
          "Ward",
          "Alignment"
        ],
        "rp_cost": 2
      }
    }
  ],
  "classAccessEvidence": {
    "Bard": {
      "rank": 1,
      "minimumClassLevel": 1,
      "school": "Enchantment",
      "baseRpCost": 2
    },
    "Crimson Agent": {
      "rank": 1,
      "minimumClassLevel": 2,
      "school": "Enchantment",
      "baseRpCost": 2
    },
    "Mirrorsage": {
      "rank": 1,
      "minimumClassLevel": 1,
      "school": "Enchantment",
      "baseRpCost": 2
    },
    "Thief": {
      "rank": 1,
      "minimumClassLevel": 3,
      "school": "Enchantment",
      "baseRpCost": 2
    },
    "Wizard": {
      "rank": 1,
      "minimumClassLevel": 1,
      "school": "Enchantment",
      "baseRpCost": 2
    },
    "Paladin": {
      "rank": 1,
      "minimumClassLevel": 2,
      "school": "Enchantment",
      "baseRpCost": 2
    }
  },
  "sourceReview": [
    "docs/audit/2026-10-08/full-game/GPT_ENCHANTMENT_RANK1_SOURCE_CONFERENCE.md",
    "docs/audit/2026-10-08/full-game/GPT_ENCHANTMENT_RANK1_EXACT_REVIEW.md"
  ],
  "reviewEvidence": [
    "docs/audit/2026-10-08/full-game/GPT_ENCHANTMENT_RANK1_EXACT_REVIEW.md"
  ],
  "authoringFile": "data/playtest/spell_drafts/batch_enchantment_rank1.json"
}
```

## S18-counterspell

`CURRENT_DIVINATION_RANK7_REVIEW_INPUT.json`
SHA-256: `0f6a122b915e8bceb7c7ae9eb9243fcf2ec51b28bd1c3f4c4a686e02a79e89d8`
Location: /completeCurrentCounterparts/4/completeCurrentAuthoredRecord/operational
Complete reviewed counterpart; source status and exact scope retained, no promotion from comparison.

```json
{
  "id": "counterspell",
  "activation": "Reaction — when another creature you can perceive within range and line of effect begins casting a spell, after its casting costs and cadence are committed but before its effect resolves",
  "rangeFeet": 60,
  "targets": "One pending spell cast by the triggering creature. The spell needs an actual recorded rank; the Director may know that rank without revealing it to you.",
  "duration": "Instantaneous",
  "concentration": false,
  "components": [
    "V",
    "S",
    "F"
  ],
  "resolution": "make a spellcasting-ability check using the actual ability for the class through which you cast Counterspell, adding PB once, against DC 10 + twice the triggering spell's actual rank (rank 0 contributes 0). Use CORE_RESOLUTION_PLAYTEST.md's fixed-DC task degrees and natural shifts: at least DC+10 Critical Success, at least DC Success, at most DC-10 Critical Failure, otherwise Failure; natural 20 improves one degree and natural 1 worsens one. Collapse both upper degrees to success and both lower degrees to failure; invent no additional critical effect. This is not a spell attack or saving throw.",
  "effect": "Success negates the selected pending spell after its costs were committed; failure lets it continue. Every interruptible cast first commits its RP/material/other costs, components, concentration transition, Dissonance/Refrain and exact beginning/casting hooks once, then opens the interruption window. A surviving cast later resolves its effect and outcome-dependent hooks. Negation gives no refund, no successful-effect trigger and no restoration of old concentration. Counterspell is itself a spell and can be countered. Resolve nested counters last-in, first-out; if a counter is negated, the earlier pending spell resumes without paying or casting again. Resuming a parent never rewrites the later nested cast's Refrain/Dissonance history.",
  "scaling": "None. No automatic success against lower ranks and no generic upcast.",
  "limitations": "One attempt per creature against a particular pending cast, shared across ordinary, Wizard, Mage and other same-named Counterspell sources. An exact source that expressly grants an additional Counterspell attempt against the same pending cast overrides this default; merely granting another Reaction does not. After a failed attempt another eligible creature may react; once negated, the spell supplies no further interruption trigger. All reactions need their own legal remaining resource, components, range and current source permissions. Attempting does not reveal spell identity/rank; never treat an unassigned rank as 0 or estimate it from RP. Ready opens its cast-interruption window at preparation, not release. Countering is not whole-Action/turn hard denial and does not spend that ledger. Ordinary Counterspell requires ordinary repertoire/class access and rank-3 cost; Wizard/Mage same-named class cards keep their own separate acquisition, printed costs, ranks, recharge and text. Apply SPELL_INTEGRATION_RULES.md for actual class access and repertoire, costs before resolution, components, concentration, Dissonance/Refrain and exact source cadence. No automatic scaling or generic upcast.",
  "designNotes": "PRESERVED: both Abjuration/Universal rank-3 placements, Reaction, 60 feet, V/S/F and instantaneous interruption. NEW: actual casting ability+PB against DC 10+2*rank, one attempt per pending cast, hidden-rank handling and nested timing. REVIEWED SOURCE CORRECTION: the earlier binary-check proposal is superseded by the existing Core fixed-DC task rule, with natural shifts and collapsed success/failure outcomes. Exact source permission may override the shared attempt limit; another Reaction alone cannot.",
  "implementationStatus": "REVIEWED authored operational-playtest manuscript; runtime and balance validation pending",
  "sourceCoreEntries": [
    {
      "index": 40,
      "original": {
        "school": "Abjuration",
        "level": 3,
        "name": "Counterspell",
        "effect": "Interrupt a creature casting a spell.",
        "source_paragraph": 9029,
        "casting_time": "1 reaction",
        "range": "60 feet",
        "duration": "Instantaneous",
        "components": "V, S, F",
        "resolution": "Automatic or opposed as described",
        "tags": [
          "Utility"
        ],
        "rp_cost": 5
      }
    },
    {
      "index": 876,
      "original": {
        "school": "Universal",
        "level": 3,
        "name": "Counterspell",
        "effect": "Interrupt a creature casting a spell.",
        "source_paragraph": 10065,
        "casting_time": "1 reaction",
        "range": "60 feet",
        "duration": "Instantaneous",
        "components": "V, S, F",
        "resolution": "Automatic or opposed as described",
        "tags": [
          "Utility"
        ],
        "rp_cost": 5
      }
    }
  ],
  "sourcePlacements": [
    {
      "name": "Counterspell",
      "school": "Abjuration",
      "level": 3,
      "summary": "Interrupt a creature casting a spell."
    },
    {
      "name": "Counterspell",
      "school": "Universal",
      "level": 3,
      "summary": "Interrupt a creature casting a spell."
    }
  ],
  "classAccessEvidence": {
    "Bard": {
      "rank": 3,
      "minimumClassLevel": 7,
      "school": "Universal",
      "baseRpCost": 5
    },
    "Cleric": {
      "rank": 3,
      "minimumClassLevel": 5,
      "school": "Abjuration",
      "baseRpCost": 5
    },
    "Druid": {
      "rank": 3,
      "minimumClassLevel": 5,
      "school": "Abjuration",
      "baseRpCost": 5
    },
    "Mage": {
      "rank": 3,
      "minimumClassLevel": 5,
      "school": "Abjuration",
      "baseRpCost": 5
    },
    "Monk": {
      "rank": 3,
      "minimumClassLevel": 13,
      "school": "Abjuration",
      "baseRpCost": 5
    },
    "Mirrorsage": {
      "rank": 3,
      "minimumClassLevel": 7,
      "school": "Universal",
      "baseRpCost": 5
    },
    "Tinker": {
      "rank": 3,
      "minimumClassLevel": 10,
      "school": "Abjuration",
      "baseRpCost": 5
    },
    "Wizard": {
      "rank": 3,
      "minimumClassLevel": 5,
      "school": "Abjuration",
      "baseRpCost": 5
    },
    "Paladin": {
      "rank": 3,
      "minimumClassLevel": 9,
      "school": "Abjuration",
      "baseRpCost": 5
    }
  },
  "sourceReview": [
    "docs/audit/2026-10-08/full-game/GPT_ABJURATION_RANK2_3_SOURCE_CONFERENCE.md",
    "docs/audit/2026-10-08/full-game/GPT_ABJURATION_RANK2_3_EXACT_REVIEW.md"
  ],
  "reviewEvidence": [
    "docs/audit/2026-10-08/full-game/GPT_ABJURATION_RANK2_3_EXACT_REVIEW.md"
  ],
  "authoringFile": "data/playtest/spell_drafts/batch_abjuration_rank2_3.json"
}
```

## S18-faction-divination

`CURRENT_DIVINATION_RANK7_REVIEW_INPUT.json`
SHA-256: `0f6a122b915e8bceb7c7ae9eb9243fcf2ec51b28bd1c3f4c4a686e02a79e89d8`
Location: /completeCurrentCounterparts/6/completeCurrentAuthoredRecord/operational
Complete reviewed counterpart; source status and exact scope retained, no promotion from comparison.

```json
{
  "id": "faction-divination",
  "activation": "Action",
  "rangeFeet": 0,
  "targets": "Self; choose one exact known canonical factionId.",
  "duration": "Instantaneous private institutional inquiry",
  "concentration": false,
  "components": [
    "V",
    "S",
    "F"
  ],
  "resolution": "No roll. Privately learn one actual current major institutional objective of the chosen faction. No physical representative, positive reputation, membership, Faction Seal permission, geographic distance or planar anchor is required.",
  "effect": "A qualifying objective is a concrete established goal pursued or prioritized by the institution or its recognized governing authority, such as securing a trade route, recovering a stolen archive or removing a named governor from office. A member’s private wish, reputation inference or the Director’s preferred plot is not an institutional objective. If several objectives are genuinely coequal, the Director records one stable priority selection while that institutional state remains materially unchanged. Equivalent repeat casts across casters/rephrasing do not rotate through hidden coequal goals. Report No Current Major Objective only for genuine established absence; undefined or specifically protected institutional information reports Indeterminate. Independently readable portions of a meaningful goal may be stated while protected details remain Indeterminate, without identifying which ward or hidden record caused the limit.",
  "scaling": "None. No automatic increase in range, duration, targets, uses or information.",
  "limitations": "Protection of one leader’s personal information does not erase an independently established institutional objective, and a protected private plan does not become institutional merely to evade protection. A subfaction must have its own actual canonical identity to be selected separately; invented subdivisions are not extra inquiries. The spell does not directly reveal an operational plan, member list, exact locations, timetable, secret agents, resources or every subordinate objective. A goal can naturally mention a readable subject as necessary to make it concrete, but supplies no additional dossier. It changes neither reputation nor faction intent and forces no action. Actual class access, repertoire, V/S/F components, costs, Dissonance/Refrain, beginning hooks, concentration transitions and interruption follow SPELL_INTEGRATION_RULES.md. Commit costs before the counter window; failed, blocked and countered effects do not refund costs or restore prior concentration. Use the actual casting class's school and rank. Specific information protections apply to their actual subjects and generating-source scope. Hidden unprotected facts are readable; undefined facts are not invented. No automatic scaling or generic upcast.",
  "designNotes": "PRESERVED: Action/V,S,F/instantaneous and one current major faction objective. CONFLICT RULING: Self abstract informational casting replaces raw 60-foot metadata. NEW: exact institutional predicate, no geographic/planar anchor, stable coequal objective, and truthful absence versus undefined/protected output.",
  "implementationStatus": "REVIEWED authored operational PLAYTEST manuscript; runtime, numerical balance and broader system validation pending",
  "sourcePlacements": [
    {
      "name": "Faction Divination",
      "school": "Divination",
      "level": 3,
      "summary": "Learn a faction's current major objective."
    }
  ],
  "sourceCoreEntries": [
    {
      "index": 253,
      "original": {
        "school": "Divination",
        "level": 3,
        "name": "Faction Divination",
        "effect": "Learn a faction's current major objective.",
        "source_paragraph": 9292,
        "casting_time": "1 action",
        "range": "60 feet",
        "duration": "Instantaneous",
        "components": "V, S, F",
        "resolution": "Automatic or opposed as described",
        "tags": [
          "Faction"
        ],
        "rp_cost": 5
      }
    }
  ],
  "classAccessEvidence": {
    "Cleric": {
      "rank": 3,
      "minimumClassLevel": 5,
      "school": "Divination",
      "baseRpCost": 5
    },
    "Mirrorsage": {
      "rank": 3,
      "minimumClassLevel": 7,
      "school": "Divination",
      "baseRpCost": 5
    },
    "Ranger": {
      "rank": 3,
      "minimumClassLevel": 9,
      "school": "Divination",
      "baseRpCost": 5
    },
    "Shaman": {
      "rank": 3,
      "minimumClassLevel": 7,
      "school": "Divination",
      "baseRpCost": 5
    },
    "Wizard": {
      "rank": 3,
      "minimumClassLevel": 5,
      "school": "Divination",
      "baseRpCost": 5
    },
    "Paladin": {
      "rank": 3,
      "minimumClassLevel": 9,
      "school": "Divination",
      "baseRpCost": 5
    }
  },
  "sourceReview": [
    "docs/audit/2026-10-08/full-game/GPT_DIVINATION_RANK3_SOURCE_CONFERENCE.md",
    "docs/audit/2026-10-08/full-game/GPT_DIVINATION_RANK3_EXACT_REVIEW.md"
  ],
  "reviewEvidence": [
    "docs/audit/2026-10-08/full-game/GPT_DIVINATION_RANK3_EXACT_REVIEW.md"
  ],
  "authoringFile": "data/playtest/spell_drafts/batch_divination_rank3.json"
}
```

## S18-faction-insight

`CURRENT_DIVINATION_RANK7_REVIEW_INPUT.json`
SHA-256: `0f6a122b915e8bceb7c7ae9eb9243fcf2ec51b28bd1c3f4c4a686e02a79e89d8`
Location: /completeCurrentCounterparts/7/completeCurrentAuthoredRecord/operational
Complete reviewed counterpart; source status and exact scope retained, no promotion from comparison.

```json
{
  "id": "faction-insight",
  "activation": "Action",
  "rangeFeet": 30,
  "targets": "One creature you perceive within 30 feet and line of effect. Choose one exact canonical factionId you know.",
  "duration": "Instantaneous",
  "concentration": false,
  "components": [
    "V",
    "S",
    "F"
  ],
  "resolution": "No save. Privately learn the target’s actual current standing score for that faction, plus the corresponding standing category only if current canonical faction data defines one. Undefined or specifically protected information reports Indeterminate.",
  "effect": "Director-held hidden standing is legitimate information when unprotected. Use the actual current record and current reputation authority, normally -3 through+3 under REPUTATION.md. The absence of an established standing record is not zero. If a numeric score is known but no canonical category is defined, report that score without inventing a title.",
  "scaling": "None. No automatic increase in targets, range, duration, uses or information.",
  "limitations": "This supplies no membership, loyalty, intentions, institutional rank, credential, legal authority, prices, social history or other faction standings. No save or positive-standing caster gate is added. It changes no reputation and does not import the historical -5..+5 scale. Creature type alone does not exclude an actual creature with a standing record; the record may be part of established Director fiction rather than a software character file. Actual class access, repertoire, V/S/F components, costs, Dissonance/Refrain, beginning hooks, concentration transitions and interruption follow SPELL_INTEGRATION_RULES.md. Costs commit before the counter window without refunds or restoration of prior concentration. Explicit remote-destination/concealment exceptions override ordinary originating line of effect only as printed. Specific information protections apply to their actual subject and generating-source scope; hidden but unprotected facts are valid information, and missing facts are never invented. No automatic scaling or upcast.",
  "designNotes": "PRESERVED: Action/30feet/V,S,F/instantaneous and standing with one faction. NEW: exact known-faction selection, actual numeric/category output, missing/protected Indeterminate and creature eligibility without biological restriction.",
  "implementationStatus": "REVIEWED authored operational-playtest manuscript; runtime, numerical balance and broader information/roll-system validation pending",
  "sourcePlacements": [
    {
      "name": "Faction Insight",
      "school": "Divination",
      "level": 1,
      "summary": "Learn target's standing with one faction."
    }
  ],
  "sourceCoreEntries": [
    {
      "index": 234,
      "original": {
        "school": "Divination",
        "level": 1,
        "name": "Faction Insight",
        "effect": "Learn target's standing with one faction.",
        "source_paragraph": 9269,
        "casting_time": "1 action",
        "range": "30 feet",
        "duration": "Instantaneous",
        "components": "V, S, F",
        "resolution": "Automatic or opposed as described",
        "tags": [
          "Detection",
          "Faction"
        ],
        "rp_cost": 2
      }
    }
  ],
  "classAccessEvidence": {
    "Cleric": {
      "rank": 1,
      "minimumClassLevel": 1,
      "school": "Divination",
      "baseRpCost": 2
    },
    "Mirrorsage": {
      "rank": 1,
      "minimumClassLevel": 1,
      "school": "Divination",
      "baseRpCost": 2
    },
    "Ranger": {
      "rank": 1,
      "minimumClassLevel": 2,
      "school": "Divination",
      "baseRpCost": 2
    },
    "Shaman": {
      "rank": 1,
      "minimumClassLevel": 1,
      "school": "Divination",
      "baseRpCost": 2
    },
    "Wizard": {
      "rank": 1,
      "minimumClassLevel": 1,
      "school": "Divination",
      "baseRpCost": 2
    },
    "Paladin": {
      "rank": 1,
      "minimumClassLevel": 2,
      "school": "Divination",
      "baseRpCost": 2
    }
  },
  "sourceReview": [
    "docs/audit/2026-10-08/full-game/GPT_DIVINATION_RANK1_SOURCE_CONFERENCE.md",
    "docs/audit/2026-10-08/full-game/GPT_DIVINATION_RANK1_EXACT_REVIEW.md"
  ],
  "reviewEvidence": [
    "docs/audit/2026-10-08/full-game/GPT_DIVINATION_RANK1_EXACT_REVIEW.md"
  ],
  "authoringFile": "data/playtest/spell_drafts/batch_divination_rank1.json"
}
```

## S18-resonance-sight-greater

`CURRENT_DIVINATION_RANK7_REVIEW_INPUT.json`
SHA-256: `0f6a122b915e8bceb7c7ae9eb9243fcf2ec51b28bd1c3f4c4a686e02a79e89d8`
Location: /completeCurrentCounterparts/12/completeCurrentAuthoredRecord/operational
Complete reviewed counterpart; source status and exact scope retained, no promotion from comparison.

```json
{
  "id": "resonance-sight-greater",
  "activation": "Action",
  "rangeFeet": 0,
  "targets": "Self; magical effects within 60 feet on your plane and in line of effect.",
  "duration": "Instantaneous private snapshot",
  "concentration": false,
  "components": [
    "V",
    "S",
    "F"
  ],
  "resolution": "No roll. Detect every currently existing qualifying magical effect with a readable portion in the area. Ordinary non-solid visual concealment and lack of mundane visibility, including Hidden/Invisible status, do not hide the effect itself. Solid total cover blocks the unreadable portion. This informational detection does not require ordinary visual sight of the effect.",
  "effect": "For each qualifying effect, privately receive its readable local location/footprint, actual effect/spell/property identity when explicitly established and unprotected (otherwise its established broad magical category), and recorded readable proximate generating source. Undefined/protected identity and provenance fields independently report Indeterminate, without erasing other readable fields. Proximate source means the specific originating spell cast/caster identity, item producing an active property, creature/feature producing an aura, or site/zone/ritual generating that effect. A locally qualifying effect can disclose its recorded source identity even when that source is now beyond 60 feet, but not that source’s current remote location, condition or inventory. Record source identity as it actually exists; a missing personal name is not invented. A footprint is clipped to the readable area, rather than exposing the entire remote extent of a partially local effect.",
  "scaling": "None. No automatic increase in range, duration, targets, uses or information.",
  "limitations": "Active intrinsic magic requires an actual presently active magical effect/aura record; a creature’s species/theme or RP pool alone is not one. A permanent item qualifies through a currently active property/effect, not a dormant historical enchantment with no active record. An existing ongoing record that is suppressed remains detectable as suppressed if that state is readable; an ended/removed effect or mere extinguished residue does not qualify. Resonance Tracking separately governs one-hour spell traces. A copy is identified as the actual copied effect and its proximate copying source, not a fresh original cast. Readable explicitly recorded provenance may identify the immediate source relationship but grants no independent recursive search through upstream controllers or histories. An attached aura can reveal its creature’s location through ordinary inference without granting sight of that body. Actual subject information protections can withhold attached-magic details, while independent environmental magic remains separately readable. No universal spell-rank/slot/charge/RP total, recipe, full stat block, dispel, control, extraction, copied spell, remote attack/casting origin or permanent map is granted. Remembering or writing a permitted snapshot uses ordinary memory and tools. Actual class access, repertoire, V/S/F components, costs, Dissonance/Refrain, beginning hooks, concentration transitions and interruption follow SPELL_INTEGRATION_RULES.md. Commit costs before the counter window; failed, blocked and countered effects do not refund costs or restore prior concentration. Use the actual casting class's school and rank. Specific information protections apply to their actual subjects and generating-source scope. Hidden unprotected facts are readable; undefined facts are not invented. No automatic scaling or generic upcast.",
  "designNotes": "PRESERVED: Action/V,S,F/instantaneous and all magical effects and their sources within 60 feet. CONFLICT RULING: Self with a 60-foot same-plane/line-of-effect sensing radius. NEW: local readable footprint, effect identity/category and proximate provenance, non-solid concealment bypass, actual ongoing suppressed versus ended/dormant distinctions and no direct remote-current-location report.",
  "implementationStatus": "REVIEWED authored operational PLAYTEST manuscript; runtime, numerical balance and broader system validation pending",
  "sourcePlacements": [
    {
      "name": "Resonance Sight (Greater)",
      "school": "Divination",
      "level": 3,
      "summary": "See all magical effects and their sources within 60 feet."
    }
  ],
  "sourceCoreEntries": [
    {
      "index": 255,
      "original": {
        "school": "Divination",
        "level": 3,
        "name": "Resonance Sight (Greater)",
        "effect": "See all magical effects and their sources within 60 feet.",
        "source_paragraph": 9294,
        "casting_time": "1 action",
        "range": "60 feet",
        "duration": "Instantaneous",
        "components": "V, S, F",
        "resolution": "Automatic or opposed as described",
        "tags": [
          "Detection",
          "Resonance"
        ],
        "rp_cost": 5
      }
    }
  ],
  "classAccessEvidence": {
    "Cleric": {
      "rank": 3,
      "minimumClassLevel": 5,
      "school": "Divination",
      "baseRpCost": 5
    },
    "Mirrorsage": {
      "rank": 3,
      "minimumClassLevel": 7,
      "school": "Divination",
      "baseRpCost": 5
    },
    "Ranger": {
      "rank": 3,
      "minimumClassLevel": 9,
      "school": "Divination",
      "baseRpCost": 5
    },
    "Shaman": {
      "rank": 3,
      "minimumClassLevel": 7,
      "school": "Divination",
      "baseRpCost": 5
    },
    "Wizard": {
      "rank": 3,
      "minimumClassLevel": 5,
      "school": "Divination",
      "baseRpCost": 5
    },
    "Paladin": {
      "rank": 3,
      "minimumClassLevel": 9,
      "school": "Divination",
      "baseRpCost": 5
    }
  },
  "sourceReview": [
    "docs/audit/2026-10-08/full-game/GPT_DIVINATION_RANK3_SOURCE_CONFERENCE.md",
    "docs/audit/2026-10-08/full-game/GPT_DIVINATION_RANK3_EXACT_REVIEW.md"
  ],
  "reviewEvidence": [
    "docs/audit/2026-10-08/full-game/GPT_DIVINATION_RANK3_EXACT_REVIEW.md"
  ],
  "authoringFile": "data/playtest/spell_drafts/batch_divination_rank3.json"
}
```

## S18-alignment-revelation

`CURRENT_DIVINATION_RANK7_REVIEW_INPUT.json`
SHA-256: `0f6a122b915e8bceb7c7ae9eb9243fcf2ec51b28bd1c3f4c4a686e02a79e89d8`
Location: /completeCurrentCounterparts/0/completeCurrentAuthoredRecord/operational
Complete reviewed counterpart; source status and exact scope retained, no promotion from comparison.

```json
{
  "id": "alignment-revelation",
  "activation": "Action",
  "rangeFeet": 60,
  "targets": "One creature you perceive within 60 feet and line of effect.",
  "duration": "Instantaneous public visual revelation",
  "concentration": false,
  "components": [
    "V",
    "S",
    "F"
  ],
  "resolution": "The target makes a Charisma save against your spell DC. Success: no revelation. Failure: magic displays two self-luminous symbolic sigils immediately around the target, one for its actual Lawful/Neutral/Chaotic axis and one for its actual Good/Neutral/Evil axis. Each readable axis displays its true current value; each undefined or specifically protected axis displays Indeterminate. Only an exact masking rule can alter a displayed result.",
  "effect": "The sigils exist only during resolution, long enough to be ordinarily perceived, then vanish. An observer must actually be able to see the target to see and understand the corresponding symbolic revelation; no language or hearing is required. Blindness, solid visual obstruction or inability to see the target prevents that observation. The sigils emit no meaningful surrounding illumination and do not themselves grant sight of an Invisible/Hidden or otherwise unseen body. An observer who can see the target through another actual permitted sense can read them. The magic reveals the value; it does not make the target speak, confess, interpret a command or verify a lie.",
  "scaling": "None. No automatic increase in range, duration, targets, uses or information.",
  "limitations": "This grants no alignment change, behavior control, oathbreaking, compulsory PvP, crime/motive information or future-action guarantee. “True” does not silently bypass a written information protection. The failure creates only the public information event; known information is not erased when the sigils vanish. No automatic recording item, repeated-use immunity or daily cap is added. Its higher-rank price and CHA-save requirement remain despite overlap with lower-rank private readers; public disclosure is the reviewed distinction, not invented ward-piercing power. Actual class access, repertoire, V/S/F components, costs, Dissonance/Refrain, beginning hooks, concentration transitions and interruption follow SPELL_INTEGRATION_RULES.md. Commit costs before the counter window; failed, blocked and countered effects do not refund costs or restore prior concentration. Use the actual casting class's school and rank. Specific information protections apply to their actual subjects and generating-source scope. Hidden unprotected facts are readable; undefined facts are not invented. No automatic scaling or generic upcast.",
  "designNotes": "PRESERVED: Action/60 feet/V,S,F/instantaneous, true alignment revelation and CHA save negation. NEW: two publicly readable nonlinguistic sigils with actual observer sight requirements, independent readable/Indeterminate axes and no compelled speech. Relative balance against private lower-rank alignment spells remains open.",
  "implementationStatus": "REVIEWED authored operational PLAYTEST manuscript; runtime, numerical balance and broader system validation pending",
  "sourcePlacements": [
    {
      "name": "Alignment Revelation",
      "school": "Divination",
      "level": 3,
      "summary": "Force a creature to reveal their true alignment (CHA save negates)."
    }
  ],
  "sourceCoreEntries": [
    {
      "index": 254,
      "original": {
        "school": "Divination",
        "level": 3,
        "name": "Alignment Revelation",
        "effect": "Force a creature to reveal their true alignment (CHA save negates).",
        "source_paragraph": 9293,
        "casting_time": "1 action",
        "range": "60 feet",
        "duration": "Instantaneous",
        "components": "V, S, F",
        "resolution": "Charisma save",
        "tags": [
          "Detection",
          "Alignment"
        ],
        "rp_cost": 5
      }
    }
  ],
  "classAccessEvidence": {
    "Cleric": {
      "rank": 3,
      "minimumClassLevel": 5,
      "school": "Divination",
      "baseRpCost": 5
    },
    "Mirrorsage": {
      "rank": 3,
      "minimumClassLevel": 7,
      "school": "Divination",
      "baseRpCost": 5
    },
    "Ranger": {
      "rank": 3,
      "minimumClassLevel": 9,
      "school": "Divination",
      "baseRpCost": 5
    },
    "Shaman": {
      "rank": 3,
      "minimumClassLevel": 7,
      "school": "Divination",
      "baseRpCost": 5
    },
    "Wizard": {
      "rank": 3,
      "minimumClassLevel": 5,
      "school": "Divination",
      "baseRpCost": 5
    },
    "Paladin": {
      "rank": 3,
      "minimumClassLevel": 9,
      "school": "Divination",
      "baseRpCost": 5
    }
  },
  "sourceReview": [
    "docs/audit/2026-10-08/full-game/GPT_DIVINATION_RANK3_SOURCE_CONFERENCE.md",
    "docs/audit/2026-10-08/full-game/GPT_DIVINATION_RANK3_EXACT_REVIEW.md"
  ],
  "reviewEvidence": [
    "docs/audit/2026-10-08/full-game/GPT_DIVINATION_RANK3_EXACT_REVIEW.md"
  ],
  "authoringFile": "data/playtest/spell_drafts/batch_divination_rank3.json"
}
```

## S18-corruption-insight

`CURRENT_DIVINATION_RANK7_REVIEW_INPUT.json`
SHA-256: `0f6a122b915e8bceb7c7ae9eb9243fcf2ec51b28bd1c3f4c4a686e02a79e89d8`
Location: /completeCurrentCounterparts/3/completeCurrentAuthoredRecord/operational
Complete reviewed counterpart; source status and exact scope retained, no promotion from comparison.

```json
{
  "id": "corruption-insight",
  "activation": "Action",
  "rangeFeet": 30,
  "targets": "One creature you perceive within 30 feet and line of effect; alternatively, a fixed10-foot-radius sphere centered on a point you perceive within30feet and line of effect.",
  "duration": "Instantaneous",
  "concentration": false,
  "components": [
    "V",
    "S",
    "F"
  ],
  "resolution": "No save. Examine one current qualifying Corruption record and privately report its actual type and proximate causal source. The two fields independently report Indeterminate when undefined or specifically protected. Report No Corruption only when no actual Corruption is present and no relevant protection prevents determining that fact.",
  "effect": "Creature mode examines Corruption actually affecting that creature. Area mode examines environmental Corruption belonging to the selected area itself, within the sphere and line of effect to its center; it does not inspect every occupant merely for standing there. Type means the actual recorded category, type or name. Source means the immediate established cause responsible for that record, such as a spell, curse, artifact, creature effect, site or environmental source. An explicit Corrupted condition can supply that actual type, but does not by itself invent who or what caused it. If the caster already distinguishes a qualifying current record, they may select it. Otherwise the Director uses a fixed deterministic order recorded for those applications before answering; materially unchanged repeat casts return that record rather than rotating through hidden applications. A distinct known record can be selected on a later cast.",
  "scaling": "None. No automatic increase in targets, range, duration, uses or information.",
  "limitations": "Do not extrapolate an immediate cause into an upstream conspirator, current owner/controller location, complete history or unknown actor identity. A source actor protected against the information cannot be exposed merely through its causal association; report the permissible cause/type fields without the protected detail. Undefined data is not proof of absence. No new numeric Corruption track, save DC, full statistics, cure, cleansing, alignment report, poison/disease/species inference, suppression or harvest permission. The spell supplies information only. Actual class access, repertoire, V/S/F components, costs, Dissonance/Refrain, beginning hooks, concentration transitions and interruption follow SPELL_INTEGRATION_RULES.md. Costs commit before the counter window without refunds or restoration of prior concentration. Explicit remote-destination/concealment exceptions override ordinary originating line of effect only as printed. Specific information protections apply to their actual subject and generating-source scope; hidden but unprotected facts are valid information, and missing facts are never invented. No automatic scaling or upcast.",
  "designNotes": "PRESERVED: Action/30feet/V,S,F/instantaneous and source/type of Corruption affecting a creature or area. NEW:10-foot environmental-area mode, one-record deterministic selection, proximate-source meaning, independent known/protected fields and clipped center-LoE. Existing Corrupted definition is evidence, not a new universal cause or taxonomy.",
  "implementationStatus": "REVIEWED authored operational-playtest manuscript; runtime, numerical balance and broader information/roll-system validation pending",
  "sourcePlacements": [
    {
      "name": "Corruption Insight",
      "school": "Divination",
      "level": 1,
      "summary": "Determine source and type of corruption affecting a creature or area."
    }
  ],
  "sourceCoreEntries": [
    {
      "index": 239,
      "original": {
        "school": "Divination",
        "level": 1,
        "name": "Corruption Insight",
        "effect": "Determine source and type of corruption affecting a creature or area.",
        "source_paragraph": 9274,
        "casting_time": "1 action",
        "range": "30 feet",
        "duration": "Instantaneous",
        "components": "V, S, F",
        "resolution": "Automatic or opposed as described",
        "tags": [
          "Detection",
          "Corruption"
        ],
        "rp_cost": 2
      }
    }
  ],
  "classAccessEvidence": {
    "Cleric": {
      "rank": 1,
      "minimumClassLevel": 1,
      "school": "Divination",
      "baseRpCost": 2
    },
    "Mirrorsage": {
      "rank": 1,
      "minimumClassLevel": 1,
      "school": "Divination",
      "baseRpCost": 2
    },
    "Ranger": {
      "rank": 1,
      "minimumClassLevel": 2,
      "school": "Divination",
      "baseRpCost": 2
    },
    "Shaman": {
      "rank": 1,
      "minimumClassLevel": 1,
      "school": "Divination",
      "baseRpCost": 2
    },
    "Wizard": {
      "rank": 1,
      "minimumClassLevel": 1,
      "school": "Divination",
      "baseRpCost": 2
    },
    "Paladin": {
      "rank": 1,
      "minimumClassLevel": 2,
      "school": "Divination",
      "baseRpCost": 2
    }
  },
  "sourceReview": [
    "docs/audit/2026-10-08/full-game/GPT_DIVINATION_RANK1_SOURCE_CONFERENCE.md",
    "docs/audit/2026-10-08/full-game/GPT_DIVINATION_RANK1_EXACT_REVIEW.md"
  ],
  "reviewEvidence": [
    "docs/audit/2026-10-08/full-game/GPT_DIVINATION_RANK1_EXACT_REVIEW.md"
  ],
  "authoringFile": "data/playtest/spell_drafts/batch_divination_rank1.json"
}
```

## S18-sense-magic

`CURRENT_DIVINATION_RANK7_REVIEW_INPUT.json`
SHA-256: `0f6a122b915e8bceb7c7ae9eb9243fcf2ec51b28bd1c3f4c4a686e02a79e89d8`
Location: /completeCurrentCounterparts/13/completeCurrentAuthoredRecord/operational
Complete reviewed counterpart; source status and exact scope retained, no promotion from comparison.

```json
{
  "id": "sense-magic",
  "activation": "Action",
  "rangeFeet": 10,
  "targets": "Self; sense qualifying active magic within 10 feet and line of effect.",
  "duration": "If applied in initiative, expires at the caster's first future regular-start marker after application; preserve that virtual marker through initiative changes. If applied outside initiative, expires 6 seconds after application; entering initiative preserves that absolute deadline. An already-passed start never counts.",
  "concentration": false,
  "components": [
    "V",
    "S"
  ],
  "resolution": "Automatic after legal casting; no spell attack or saving throw.",
  "effect": "You know only whether at least one active magical aura or ongoing magical effect is within the sensing area.",
  "scaling": "None.",
  "limitations": "Total cover blocks the sense. It supplies no direction, count, distance, owner, school, spell identity, rank, properties, creature identity, hidden curse, dormant enchantment, alignment or statistics. Nonmagical concealment or invisibility creates no magical signal. Known/prepared access, class level, legal components, line of effect, payment, concentration transitions, Refrain and class cadence follow SPELL_INTEGRATION_RULES.md. No automatic level scaling.",
  "designNotes": "PRESERVED: Action, 10 feet, V/S, one-round presence detection. NEW: Self, exact endpoint, no concentration, line of effect and yes/no information boundary.",
  "implementationStatus": "REVIEWED authored operational-playtest draft; runtime and balance validation pending",
  "sourceReview": [
    "docs/audit/2026-10-08/full-game/GPT_BODY_FINAL_AND_ABJURATION_CONFERENCE.md",
    "docs/audit/2026-10-08/full-game/GPT_ABJURATION_CANTRIP_EXACT_REVIEW.md"
  ],
  "sourceCoreEntries": [
    {
      "index": 3,
      "original": {
        "school": "Abjuration",
        "level": 0,
        "name": "Sense Magic",
        "effect": "Detect presence of magic within 10 ft for 1 round.",
        "source_paragraph": 8986,
        "casting_time": "1 action",
        "range": "10 feet",
        "duration": "1 round",
        "components": "V, S",
        "resolution": "Automatic or opposed as described",
        "tags": [
          "Detection"
        ],
        "rp_cost": 0
      }
    }
  ],
  "reviewEvidence": [
    "docs/audit/2026-10-08/full-game/GPT_ABJURATION_CANTRIP_FINAL_CLOSURE.md"
  ],
  "authoringFile": "data/playtest/spell_drafts/batch_abjuration_cantrips.json"
}
```

## S19

`DescentReviewChanges/ReviewBible/docs/mechanics/expedition/EXPEDITION_PLAYER_BOOK.md`
SHA-256: `4c58b9f7063e562b785b8db6006699d3c4f68edd0e697d06db69662ba9b7e480`
Location: lines 1146–1160
Current source-version/score/absence/null handling; divination grants no standing or eligibility rewrite.

```text

<a id="rp-a02"></a>
### RP-A02 — Preserve missing, hidden and invalid data distinctly

An unrecorded relationship, an explicit Neutral 0, a hidden relationship and an unresolved old value are different states. None should silently replace another.

Keep unknown institution names and any additional fields when carrying a record forward. Preserve the exact original document, including duplicate keys, number spelling and formatting, alongside any derived view. If a document cannot be parsed, keep it and the error; do not substitute an empty map.

Active numerical standing needs a supported known policy, a finite integral score in range, resolved subject and institution, and compatible version/history. A text “1”, false, null, 1.7 or invalid text does not become a score by rounding or coercion. Unknown or conflicting entries remain unresolved with a reason. They grant no newly inferred skill, discount, spell or access.

A correction records the exact original value/version, intended interpretation and reason as a new event. It must identify the expected prior state; a stale, replayed or conflicting change does not apply. Unrelated and unknown entries stay intact.

A compact character-sheet or companion display is a view, not the full save. Export and reimport must preserve the complete original record and the separately added interpretation/history. Hiding a neutral row for readability does not erase its recorded zero.

<a id="rp-a03"></a>
```

## S20

`DescentReviewChanges/ReviewBible/docs/mechanics/expedition/EXPEDITION_PLAYER_BOOK.md`
SHA-256: `4c58b9f7063e562b785b8db6006699d3c4f68edd0e697d06db69662ba9b7e480`
Location: lines 1190–1204
Actual institution identity and private membership boundaries; no cosmology inference.

```text

An individual NPC's attitude, a broad campaign reputation summary and one institution's score are separate. Learning a report changes the viewer's knowledge, not necessarily the subject's standing. A display must not reveal a hidden institution or membership merely because a private numeric field exists.

<a id="rp-a05"></a>
### RP-A05 — Bind relationships to real institutions

Give each actual campaign institution a stable identity and record its public name, scope/jurisdiction, authorized agents, relationship to the character, source references, visibility and actual resources/obligations. Link it to source categories only where the relationship is established.

Similar category names are not automatic aliases. Religious orders, mainstream faith and good temples can refer to different groups; so can arcane guilds, arcane institutions and academic factions. The same applies to nature and Druidic circles, indigenous tribes and peoples, or the underworld and someone's former criminal associates. A person may belong to more than one institution without merging those institutions' scores.

An alias needs evidence that two labels identify the same actual institution, with its effective source/version and originals preserved. Changing a display name keeps identity and history. A political split or merger is a new event with real relationships, not a command to sum scores or keep the highest.

An unknown saved key can later be bound to a real local institution, or remain unsupported, without being discarded. New local institutions can use this ordinary record once their actual facts are supplied. A name alone does not establish world history, allies, enemies, doctrine or special powers.

Public information includes only identities and relationships the audience may know. Private membership, backers and dossiers remain private. Literal faith, planar, prophecy and resonance references create no inferred spell, RC, RP or cosmological effect.
```

## D1

`CURRENT_DIVINATION_RANK7_REVIEW_INPUT.json`
SHA-256: `0f6a122b915e8bceb7c7ae9eb9243fcf2ec51b28bd1c3f4c4a686e02a79e89d8`
Location: /records/0/fullSourceAndCurrentAccessRecord
Complete historical spell/catalog/Core/class-access source and null operative status.

```json
{
  "id": "mass-revelation",
  "name": "Mass Revelation",
  "schools": [
    "Divination"
  ],
  "status": "blocked-pending-operational-review",
  "visibility": "public-source-review",
  "classAccess": {
    "Cleric": {
      "rank": 7,
      "minimumClassLevel": 13,
      "school": "Divination",
      "baseRpCost": 17
    },
    "Mirrorsage": {
      "rank": 7,
      "minimumClassLevel": 19,
      "school": "Divination",
      "baseRpCost": 17
    },
    "Shaman": {
      "rank": 7,
      "minimumClassLevel": 19,
      "school": "Divination",
      "baseRpCost": 17
    },
    "Wizard": {
      "rank": 7,
      "minimumClassLevel": 13,
      "school": "Divination",
      "baseRpCost": 17
    }
  },
  "operational": null,
  "additionalRpCost": 0,
  "source": {
    "catalogPath": "src/data/spells.js",
    "catalogSha256": "3358a2e1afcbc340dbafd92e45e39a7d2d0a24fed5c0719a3d233263ce530078",
    "catalogKey": "mass-revelation",
    "original": {
      "name": "Mass Revelation",
      "level": 7,
      "resonanceRank": 7,
      "school": "Divination",
      "schools": [
        "Divination"
      ],
      "placements": [
        {
          "name": "Mass Revelation",
          "school": "Divination",
          "level": 7,
          "summary": "Reveal hidden traps, enemies, magic, and lies in 60-ft cone."
        }
      ],
      "classLevels": {
        "Cleric": 7,
        "Mirrorsage": 7,
        "Shaman": 7,
        "Wizard": 7
      },
      "classRanks": {
        "Cleric": 7,
        "Mirrorsage": 7,
        "Shaman": 7,
        "Wizard": 7
      },
      "classLearnLevels": {
        "Cleric": 13,
        "Mirrorsage": 19,
        "Shaman": 19,
        "Wizard": 13
      },
      "classSchools": {
        "Cleric": "Divination",
        "Mirrorsage": "Divination",
        "Shaman": "Divination",
        "Wizard": "Divination"
      },
      "castingTime": "Not specified in current rulebook",
      "range": "Not specified in current rulebook",
      "components": "Not specified in current rulebook",
      "duration": "Not specified in current rulebook",
      "description": "Reveal hidden traps, enemies, magic, and lies in 60-ft cone.",
      "alternateSummaries": [],
      "classes": [
        "Cleric",
        "Mirrorsage",
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
        "index": 280,
        "original": {
          "school": "Divination",
          "level": 7,
          "name": "Mass Revelation",
          "effect": "Reveal hidden traps, enemies, magic, and lies in 60-ft cone.",
          "source_paragraph": 9327,
          "casting_time": "1 action",
          "range": "60 feet",
          "duration": "Instantaneous",
          "components": "V, S, F",
          "resolution": "Automatic or opposed as described",
          "tags": [
            "Detection"
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
```

## D2

`CURRENT_DIVINATION_RANK7_REVIEW_INPUT.json`
SHA-256: `0f6a122b915e8bceb7c7ae9eb9243fcf2ec51b28bd1c3f4c4a686e02a79e89d8`
Location: /records/1/fullSourceAndCurrentAccessRecord
Complete historical spell/catalog/Core/class-access source and null operative status.

```json
{
  "id": "premonition-shield",
  "name": "Premonition Shield",
  "schools": [
    "Divination"
  ],
  "status": "blocked-pending-operational-review",
  "visibility": "public-source-review",
  "classAccess": {
    "Cleric": {
      "rank": 7,
      "minimumClassLevel": 13,
      "school": "Divination",
      "baseRpCost": 17
    },
    "Mirrorsage": {
      "rank": 7,
      "minimumClassLevel": 19,
      "school": "Divination",
      "baseRpCost": 17
    },
    "Shaman": {
      "rank": 7,
      "minimumClassLevel": 19,
      "school": "Divination",
      "baseRpCost": 17
    },
    "Wizard": {
      "rank": 7,
      "minimumClassLevel": 13,
      "school": "Divination",
      "baseRpCost": 17
    }
  },
  "operational": null,
  "additionalRpCost": 0,
  "source": {
    "catalogPath": "src/data/spells.js",
    "catalogSha256": "3358a2e1afcbc340dbafd92e45e39a7d2d0a24fed5c0719a3d233263ce530078",
    "catalogKey": "premonition-shield",
    "original": {
      "name": "Premonition Shield",
      "level": 7,
      "resonanceRank": 7,
      "school": "Divination",
      "schools": [
        "Divination"
      ],
      "placements": [
        {
          "name": "Premonition Shield",
          "school": "Divination",
          "level": 7,
          "summary": "You or an ally takes no damage from next 2 attacks or spells."
        }
      ],
      "classLevels": {
        "Cleric": 7,
        "Mirrorsage": 7,
        "Shaman": 7,
        "Wizard": 7
      },
      "classRanks": {
        "Cleric": 7,
        "Mirrorsage": 7,
        "Shaman": 7,
        "Wizard": 7
      },
      "classLearnLevels": {
        "Cleric": 13,
        "Mirrorsage": 19,
        "Shaman": 19,
        "Wizard": 13
      },
      "classSchools": {
        "Cleric": "Divination",
        "Mirrorsage": "Divination",
        "Shaman": "Divination",
        "Wizard": "Divination"
      },
      "castingTime": "Not specified in current rulebook",
      "range": "Not specified in current rulebook",
      "components": "Not specified in current rulebook",
      "duration": "Not specified in current rulebook",
      "description": "You or an ally takes no damage from next 2 attacks or spells.",
      "alternateSummaries": [],
      "classes": [
        "Cleric",
        "Mirrorsage",
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
        "index": 282,
        "original": {
          "school": "Divination",
          "level": 7,
          "name": "Premonition Shield",
          "effect": "You or an ally takes no damage from next 2 attacks or spells.",
          "source_paragraph": 9329,
          "casting_time": "1 action",
          "range": "120 feet",
          "duration": "Instantaneous",
          "components": "V, S, F",
          "resolution": "Automatic or opposed as described",
          "tags": [
            "Damage",
            "Ward"
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
```

## D3

`CURRENT_DIVINATION_RANK7_REVIEW_INPUT.json`
SHA-256: `0f6a122b915e8bceb7c7ae9eb9243fcf2ec51b28bd1c3f4c4a686e02a79e89d8`
Location: /records/2/fullSourceAndCurrentAccessRecord
Complete historical spell/catalog/Core/class-access source and null operative status.

```json
{
  "id": "fate-echo",
  "name": "Fate Echo",
  "schools": [
    "Divination"
  ],
  "status": "blocked-pending-operational-review",
  "visibility": "public-source-review",
  "classAccess": {
    "Cleric": {
      "rank": 7,
      "minimumClassLevel": 13,
      "school": "Divination",
      "baseRpCost": 17
    },
    "Mirrorsage": {
      "rank": 7,
      "minimumClassLevel": 19,
      "school": "Divination",
      "baseRpCost": 17
    },
    "Shaman": {
      "rank": 7,
      "minimumClassLevel": 19,
      "school": "Divination",
      "baseRpCost": 17
    },
    "Wizard": {
      "rank": 7,
      "minimumClassLevel": 13,
      "school": "Divination",
      "baseRpCost": 17
    }
  },
  "operational": null,
  "additionalRpCost": 0,
  "source": {
    "catalogPath": "src/data/spells.js",
    "catalogSha256": "3358a2e1afcbc340dbafd92e45e39a7d2d0a24fed5c0719a3d233263ce530078",
    "catalogKey": "fate-echo",
    "original": {
      "name": "Fate Echo",
      "level": 7,
      "resonanceRank": 7,
      "school": "Divination",
      "schools": [
        "Divination"
      ],
      "placements": [
        {
          "name": "Fate Echo",
          "school": "Divination",
          "level": 7,
          "summary": "Copy one non-damaging spell cast in last 3 rounds."
        }
      ],
      "classLevels": {
        "Cleric": 7,
        "Mirrorsage": 7,
        "Shaman": 7,
        "Wizard": 7
      },
      "classRanks": {
        "Cleric": 7,
        "Mirrorsage": 7,
        "Shaman": 7,
        "Wizard": 7
      },
      "classLearnLevels": {
        "Cleric": 13,
        "Mirrorsage": 19,
        "Shaman": 19,
        "Wizard": 13
      },
      "classSchools": {
        "Cleric": "Divination",
        "Mirrorsage": "Divination",
        "Shaman": "Divination",
        "Wizard": "Divination"
      },
      "castingTime": "Not specified in current rulebook",
      "range": "Not specified in current rulebook",
      "components": "Not specified in current rulebook",
      "duration": "Not specified in current rulebook",
      "description": "Copy one non-damaging spell cast in last 3 rounds.",
      "alternateSummaries": [],
      "classes": [
        "Cleric",
        "Mirrorsage",
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
        "index": 283,
        "original": {
          "school": "Divination",
          "level": 7,
          "name": "Fate Echo",
          "effect": "Copy one non-damaging spell cast in last 3 rounds.",
          "source_paragraph": 9330,
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
```

## D4

`CURRENT_DIVINATION_RANK7_REVIEW_INPUT.json`
SHA-256: `0f6a122b915e8bceb7c7ae9eb9243fcf2ec51b28bd1c3f4c4a686e02a79e89d8`
Location: /records/3/fullSourceAndCurrentAccessRecord
Complete historical spell/catalog/Core/class-access source and null operative status.

```json
{
  "id": "vision-quest",
  "name": "Vision Quest",
  "schools": [
    "Divination"
  ],
  "status": "blocked-pending-operational-review",
  "visibility": "public-source-review",
  "classAccess": {
    "Cleric": {
      "rank": 7,
      "minimumClassLevel": 13,
      "school": "Divination",
      "baseRpCost": 17
    },
    "Mirrorsage": {
      "rank": 7,
      "minimumClassLevel": 19,
      "school": "Divination",
      "baseRpCost": 17
    },
    "Shaman": {
      "rank": 7,
      "minimumClassLevel": 19,
      "school": "Divination",
      "baseRpCost": 17
    },
    "Wizard": {
      "rank": 7,
      "minimumClassLevel": 13,
      "school": "Divination",
      "baseRpCost": 17
    }
  },
  "operational": null,
  "additionalRpCost": 0,
  "source": {
    "catalogPath": "src/data/spells.js",
    "catalogSha256": "3358a2e1afcbc340dbafd92e45e39a7d2d0a24fed5c0719a3d233263ce530078",
    "catalogKey": "vision-quest",
    "original": {
      "name": "Vision Quest",
      "level": 7,
      "resonanceRank": 7,
      "school": "Divination",
      "schools": [
        "Divination"
      ],
      "placements": [
        {
          "name": "Vision Quest",
          "school": "Divination",
          "level": 7,
          "summary": "Enter a trance to receive guidance about a specific question."
        }
      ],
      "classLevels": {
        "Cleric": 7,
        "Mirrorsage": 7,
        "Shaman": 7,
        "Wizard": 7
      },
      "classRanks": {
        "Cleric": 7,
        "Mirrorsage": 7,
        "Shaman": 7,
        "Wizard": 7
      },
      "classLearnLevels": {
        "Cleric": 13,
        "Mirrorsage": 19,
        "Shaman": 19,
        "Wizard": 13
      },
      "classSchools": {
        "Cleric": "Divination",
        "Mirrorsage": "Divination",
        "Shaman": "Divination",
        "Wizard": "Divination"
      },
      "castingTime": "Not specified in current rulebook",
      "range": "Not specified in current rulebook",
      "components": "Not specified in current rulebook",
      "duration": "Not specified in current rulebook",
      "description": "Enter a trance to receive guidance about a specific question.",
      "alternateSummaries": [],
      "classes": [
        "Cleric",
        "Mirrorsage",
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
        "index": 284,
        "original": {
          "school": "Divination",
          "level": 7,
          "name": "Vision Quest",
          "effect": "Enter a trance to receive guidance about a specific question.",
          "source_paragraph": 9331,
          "casting_time": "1 action",
          "range": "120 feet",
          "duration": "Instantaneous",
          "components": "V, S, F",
          "resolution": "Automatic or opposed as described",
          "tags": [
            "Detection"
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
```

## D5

`CURRENT_DIVINATION_RANK7_REVIEW_INPUT.json`
SHA-256: `0f6a122b915e8bceb7c7ae9eb9243fcf2ec51b28bd1c3f4c4a686e02a79e89d8`
Location: /records/4/fullSourceAndCurrentAccessRecord
Complete historical spell/catalog/Core/class-access source and null operative status.

```json
{
  "id": "faction-omniscience",
  "name": "Faction Omniscience",
  "schools": [
    "Divination"
  ],
  "status": "blocked-pending-operational-review",
  "visibility": "public-source-review",
  "classAccess": {
    "Cleric": {
      "rank": 7,
      "minimumClassLevel": 13,
      "school": "Divination",
      "baseRpCost": 17
    },
    "Mirrorsage": {
      "rank": 7,
      "minimumClassLevel": 19,
      "school": "Divination",
      "baseRpCost": 17
    },
    "Shaman": {
      "rank": 7,
      "minimumClassLevel": 19,
      "school": "Divination",
      "baseRpCost": 17
    },
    "Wizard": {
      "rank": 7,
      "minimumClassLevel": 13,
      "school": "Divination",
      "baseRpCost": 17
    }
  },
  "operational": null,
  "additionalRpCost": 0,
  "source": {
    "catalogPath": "src/data/spells.js",
    "catalogSha256": "3358a2e1afcbc340dbafd92e45e39a7d2d0a24fed5c0719a3d233263ce530078",
    "catalogKey": "faction-omniscience",
    "original": {
      "name": "Faction Omniscience",
      "level": 7,
      "resonanceRank": 7,
      "school": "Divination",
      "schools": [
        "Divination"
      ],
      "placements": [
        {
          "name": "Faction Omniscience",
          "school": "Divination",
          "level": 7,
          "summary": "Know all current activities of a faction for 1 minute."
        }
      ],
      "classLevels": {
        "Cleric": 7,
        "Mirrorsage": 7,
        "Shaman": 7,
        "Wizard": 7
      },
      "classRanks": {
        "Cleric": 7,
        "Mirrorsage": 7,
        "Shaman": 7,
        "Wizard": 7
      },
      "classLearnLevels": {
        "Cleric": 13,
        "Mirrorsage": 19,
        "Shaman": 19,
        "Wizard": 13
      },
      "classSchools": {
        "Cleric": "Divination",
        "Mirrorsage": "Divination",
        "Shaman": "Divination",
        "Wizard": "Divination"
      },
      "castingTime": "Not specified in current rulebook",
      "range": "Not specified in current rulebook",
      "components": "Not specified in current rulebook",
      "duration": "Not specified in current rulebook",
      "description": "Know all current activities of a faction for 1 minute.",
      "alternateSummaries": [],
      "classes": [
        "Cleric",
        "Mirrorsage",
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
        "index": 285,
        "original": {
          "school": "Divination",
          "level": 7,
          "name": "Faction Omniscience",
          "effect": "Know all current activities of a faction for 1 minute.",
          "source_paragraph": 9332,
          "casting_time": "1 action",
          "range": "120 feet",
          "duration": "1 minute",
          "components": "V, S, F",
          "resolution": "Automatic or opposed as described",
          "tags": [
            "Faction"
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
```

## D6

`CURRENT_DIVINATION_RANK7_REVIEW_INPUT.json`
SHA-256: `0f6a122b915e8bceb7c7ae9eb9243fcf2ec51b28bd1c3f4c4a686e02a79e89d8`
Location: /records/5/fullSourceAndCurrentAccessRecord
Complete historical spell/catalog/Core/class-access source and null operative status.

```json
{
  "id": "alignment-purge",
  "name": "Alignment Purge",
  "schools": [
    "Divination"
  ],
  "status": "blocked-pending-operational-review",
  "visibility": "public-source-review",
  "classAccess": {
    "Cleric": {
      "rank": 7,
      "minimumClassLevel": 13,
      "school": "Divination",
      "baseRpCost": 17
    },
    "Mirrorsage": {
      "rank": 7,
      "minimumClassLevel": 19,
      "school": "Divination",
      "baseRpCost": 17
    },
    "Shaman": {
      "rank": 7,
      "minimumClassLevel": 19,
      "school": "Divination",
      "baseRpCost": 17
    },
    "Wizard": {
      "rank": 7,
      "minimumClassLevel": 13,
      "school": "Divination",
      "baseRpCost": 17
    }
  },
  "operational": null,
  "additionalRpCost": 0,
  "source": {
    "catalogPath": "src/data/spells.js",
    "catalogSha256": "3358a2e1afcbc340dbafd92e45e39a7d2d0a24fed5c0719a3d233263ce530078",
    "catalogKey": "alignment-purge",
    "original": {
      "name": "Alignment Purge",
      "level": 7,
      "resonanceRank": 7,
      "school": "Divination",
      "schools": [
        "Divination"
      ],
      "placements": [
        {
          "name": "Alignment Purge",
          "school": "Divination",
          "level": 7,
          "summary": "Temporarily neutralize a creature's alignment (WIS save negates)."
        }
      ],
      "classLevels": {
        "Cleric": 7,
        "Mirrorsage": 7,
        "Shaman": 7,
        "Wizard": 7
      },
      "classRanks": {
        "Cleric": 7,
        "Mirrorsage": 7,
        "Shaman": 7,
        "Wizard": 7
      },
      "classLearnLevels": {
        "Cleric": 13,
        "Mirrorsage": 19,
        "Shaman": 19,
        "Wizard": 13
      },
      "classSchools": {
        "Cleric": "Divination",
        "Mirrorsage": "Divination",
        "Shaman": "Divination",
        "Wizard": "Divination"
      },
      "castingTime": "Not specified in current rulebook",
      "range": "Not specified in current rulebook",
      "components": "Not specified in current rulebook",
      "duration": "Not specified in current rulebook",
      "description": "Temporarily neutralize a creature's alignment (WIS save negates).",
      "alternateSummaries": [],
      "classes": [
        "Cleric",
        "Mirrorsage",
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
        "index": 286,
        "original": {
          "school": "Divination",
          "level": 7,
          "name": "Alignment Purge",
          "effect": "Temporarily neutralize a creature's alignment (WIS save negates).",
          "source_paragraph": 9333,
          "casting_time": "1 action",
          "range": "120 feet",
          "duration": "Instantaneous",
          "components": "V, S, F",
          "resolution": "Wisdom save",
          "tags": [
            "Alignment"
          ],
          "rp_cost": 17
        }
      }
    ],
    "possibleHistoricalAliases": []
  },
  "reviewFlags": [
    "Not selectable in this spell playtest packet until individual operational review"
  ]
}
```

## D7

`CURRENT_DIVINATION_RANK7_REVIEW_INPUT.json`
SHA-256: `0f6a122b915e8bceb7c7ae9eb9243fcf2ec51b28bd1c3f4c4a686e02a79e89d8`
Location: /records/6/fullSourceAndCurrentAccessRecord
Complete historical spell/catalog/Core/class-access source and null operative status.

```json
{
  "id": "resonance-sight-supreme",
  "name": "Resonance Sight (Supreme)",
  "schools": [
    "Divination"
  ],
  "status": "blocked-pending-operational-review",
  "visibility": "public-source-review",
  "classAccess": {
    "Cleric": {
      "rank": 7,
      "minimumClassLevel": 13,
      "school": "Divination",
      "baseRpCost": 17
    },
    "Mirrorsage": {
      "rank": 7,
      "minimumClassLevel": 19,
      "school": "Divination",
      "baseRpCost": 17
    },
    "Shaman": {
      "rank": 7,
      "minimumClassLevel": 19,
      "school": "Divination",
      "baseRpCost": 17
    },
    "Wizard": {
      "rank": 7,
      "minimumClassLevel": 13,
      "school": "Divination",
      "baseRpCost": 17
    }
  },
  "operational": null,
  "additionalRpCost": 0,
  "source": {
    "catalogPath": "src/data/spells.js",
    "catalogSha256": "3358a2e1afcbc340dbafd92e45e39a7d2d0a24fed5c0719a3d233263ce530078",
    "catalogKey": "resonance-sight-supreme",
    "original": {
      "name": "Resonance Sight (Supreme)",
      "level": 7,
      "resonanceRank": 7,
      "school": "Divination",
      "schools": [
        "Divination"
      ],
      "placements": [
        {
          "name": "Resonance Sight (Supreme)",
          "school": "Divination",
          "level": 7,
          "summary": "See all past and present magical effects in an area."
        }
      ],
      "classLevels": {
        "Cleric": 7,
        "Mirrorsage": 7,
        "Shaman": 7,
        "Wizard": 7
      },
      "classRanks": {
        "Cleric": 7,
        "Mirrorsage": 7,
        "Shaman": 7,
        "Wizard": 7
      },
      "classLearnLevels": {
        "Cleric": 13,
        "Mirrorsage": 19,
        "Shaman": 19,
        "Wizard": 13
      },
      "classSchools": {
        "Cleric": "Divination",
        "Mirrorsage": "Divination",
        "Shaman": "Divination",
        "Wizard": "Divination"
      },
      "castingTime": "Not specified in current rulebook",
      "range": "Not specified in current rulebook",
      "components": "Not specified in current rulebook",
      "duration": "Not specified in current rulebook",
      "description": "See all past and present magical effects in an area.",
      "alternateSummaries": [],
      "classes": [
        "Cleric",
        "Mirrorsage",
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
        "index": 287,
        "original": {
          "school": "Divination",
          "level": 7,
          "name": "Resonance Sight (Supreme)",
          "effect": "See all past and present magical effects in an area.",
          "source_paragraph": 9334,
          "casting_time": "1 action",
          "range": "120 feet",
          "duration": "Instantaneous",
          "components": "V, S, F",
          "resolution": "Automatic or opposed as described",
          "tags": [
            "Detection",
            "Resonance"
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
```

