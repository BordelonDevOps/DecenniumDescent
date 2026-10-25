# Combat, actions and timing — provisional playtest integration

**Status: REVIEWED / reference-VALIDATED within the supplied combat/action/timing/vision scope.** [GPT's disposition](../../../../docs/audit/2026-10-08/full-game/GPT_STRAIN_FIRST_REVIEW.md) confirms the corrected candidate. This does not close all combat, movement, encounter or condition work. Original books, class cards and earlier drafts are preserved. The NEW decisions below apply to this candidate only.

Read alongside [core resolution and injury](CORE_RESOLUTION_PLAYTEST.md), [conditions](CONDITIONS_PLAYTEST.md), [custom riders](CUSTOM_CONDITION_BINDINGS.md), [spell integration](SPELL_INTEGRATION_RULES.md) and [shared class rules](CLASS_PLAYTEST_RULES.md). This document explicitly supersedes conflicting provisional clauses only where listed. A specific reviewed feature retains its printed costs, prerequisites and exceptions.

## Source decisions

The [exact packet](../../../../docs/audit/2026-10-08/full-game/COMBAT_ACTION_VISION_SOURCE_PACKET.json) contains 217 paragraphs from unchanged Core V2 and V6 books. Paragraph indices are zero-based all Word XML `w:p` descendants. [Source validation](COMBAT_SOURCE_VALIDATION.json) verifies quotations and whole-book hashes. The [first GPT proposal](../../../../docs/audit/2026-10-08/full-game/GPT_COMBAT_ACTION_TIMING_FIRST_REVIEW.md), [counterexamples](../../../../docs/audit/2026-10-08/full-game/CODEX_COMBAT_COUNTEREXAMPLES.md) and [revised decisions](../../../../docs/audit/2026-10-08/full-game/GPT_COMBAT_COUNTEREXAMPLE_REVIEW.md) preserve the conference.

| Topic | Source / conflict | Candidate decision |
|---|---|---|
| Initiative, action list, encounter clock | Core 373–418 | Core controls; compatible V6 8066–8244 supplies detailed procedures. |
| Reaction | Core/V6 summarize one per round; V6 and class integration refresh own turn | NEW explicit interpretation: one resource between regular own-turn starts; no global-round reset. |
| Stances | Core 419–435; extra-turn ambiguity | Keep listed effects; NEW regular-turn selection and finite allowances. |
| Movement | Core 436–458; V6 mode switching subtracts physical distance | NEW spent-cost ledger prevents terrain/standing refunds; multiple legal Dashes each add Speed. |
| Maneuvers | Core 460–486 | Preserve sourced effects; NEW declaration, costs and endpoints fill missing execution details. |
| Grapple/Shove | V6 opposed procedure vs older shared-class generic DC | Ordinary maneuvers use V6 opposed rolls. Printed card saves/DCs retain their scope. |
| Prone and Invisible | Core/V6 conflicts already reviewed | Current condition reference controls, including Core ranged Prone disadvantage and Invisible position-reveal exception. |
| Round duration / simultaneous events | Sources do not give complete ordering | NEW preserved virtual markers and explicit start/end sequence below. |
| Ready | V6 casts and holds spell; generic Action or movement | Preserve that procedure; NEW one pending state and preparation/release details. |
| Hide/Search | Core lists actions; V6 unseen attacks | NEW passive DC and observer-specific Hidden procedure using Core task degrees. |
| Diagonals / terrain composition | 5-ft tile convention; missing full composition | NEW equal orthogonal/diagonal metric and additive movement costs. |
| Periodic and falling clocks | Existing reviewed overlays | Remain authoritative in their stated scope; no extra-turn tick or duplicated fall step. |
| Equipment, cargo and Sunder | Core delegates actual object/cargo systems | No invented durability, capacity or automatic cargo protection. These dependencies remain open. |

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

## Standard Actions

| Action | Procedure |
|---|---|
| Attack | Make the attacks legally granted by class and weapon. Replacing one attack does not replace the entire Action unless specified. |
| Cast | Use an Action-time spell or Resonance technique; all known/prepared, cost, component and target requirements apply. |
| Dash | Add one current Speed to each mode's turn cap; see movement ledger. Speed 0 grants none. A second legally paid Dash adds another Speed. |
| Disengage | Voluntary movement does not provoke opportunity attacks for the rest of that turn. |
| Dodge | Until next regular start, attacks from attackers you can see have disadvantage; your DEX saves have advantage. Benefit fails while Incapacitated or Speed 0. |
| Guard | +2 AC against the first attack against you before next regular start; consumed on that attack hit or miss. Guard state and Interpose permission remain until expiry even after the +2 is spent. |
| Aim | Action; no prior voluntary movement this turn, and no subsequent voluntary movement that turn. +2 to one ranged/spell attack before turn end. Forced movement does not cancel it. It grants no attack; a legal Bonus Action/extra Action/express attack must supply one. |
| Help | Advantage on a relevant ally check before next regular start, or assist an attack against a foe within 5 ft: the helped ally's first attack before that deadline has advantage. Assistance must be physically possible. |
| Hide / Search | Use the observer-specific procedures below. |
| Ready | Prepare an Action or movement; release uses Reaction as detailed below. |
| Use Object | Pay for the second ordinary interaction or an object's required Action activation. No extra hands/capacity are granted. |
| Improvise | Director declares ability, applicable proficiency, DC/opposed method and intended consequence before rolling. Success does not create unannounced conditions/actions. |

**Brace — NEW.** Action, choose one mode until next regular start. **Intercept:** choose a breach/doorway edge or current melee reach; when a hostile creature charges/leaps/breaches into it and enters legal reach, spend Reaction for one legal melee weapon attack after entry and before later movement/actions. **Hold Ground:** spend Reaction on the first applicable discrete push/pull/shove/knockback to reduce displacement 5 ft, minimum 0. It does not reduce damage, prevent independent Prone, stop gravity/fall steps, currents, conveyors, collapsing ground or teleportation, or grant support/hover. One Brace supplies one opportunity, not an extra Reaction.

**Rally — NEW.** Action; choose one ally within 30 ft able to perceive the rally and one active source-qualified Frightened record. CHA check at that record's source DC, otherwise 10; Success/Critical Success ends only that record. A later reviewed morale rule can supply a separate specific interaction. No automatic temporary HP, loyalty, belief or advantage.

**Withdraw.** Action; separate half-current-Speed movement budget, normal terrain costs, no opportunity attacks from that movement and +2 AC only while that movement resolves. Speed 0 grants none. Moving zero grants no lingering +2. Ordinary movement before/after remains separate. The separate budget is NEW interpretation of Core 480.

**Secure Cargo.** Core 482 preserves the wording “up to one Extraction Load class.” The subsequently reviewed [body and carrying guide](BODY_EQUIPMENT_PLAYTEST.md) supplies the provisional interpretation: spend an Action on one legal attach, lift, transfer or protective operation involving one actual cargo unit or physically constituted bundle with an assigned Extraction Class. Load measures burden; Extraction Class measures danger and logistics. Apply actual capacity, custody, hands, harnesses, checks and durability. The Action grants no extra capacity, equipment, automatic success, invulnerability or reduction in Extraction Class. Full equipment and extraction catalogs remain open.

## Ready

Spend an Action to declare a perceivable trigger and one legal Action-time action or movement. It expires next regular own-turn start. **NEW:** only one pending Ready per creature; replacing it loses the prior setup and any paid held-spell costs. No Bonus Action/Reaction ability, long ritual or multi-minute activity can be prepared by generic Ready.

The trigger happens first, then the readied response immediately follows before later events, unless a specific effect explicitly interrupts. On release spend the normal Reaction and recheck target, range, sight/perception, line of effect, ammunition and other prerequisites. An invalid or declined occurrence spends no release resource; the Ready can wait for another valid occurrence before expiry. This does not undo setup costs. Once released, it is consumed.

For ordinary nonspell actions, feature/ammunition costs are paid on release unless text charges setup. A readied **Attack Action** gets its legally available ordinary attack count; a feature limited to your own turn does not thereby work off-turn. Core Overwatch is explicitly one ranged attack, not that full Attack Action and not Soldier's distinct engine.

A readied spell is actually **cast at preparation**: choose spell/mode, verify legality, pay RP/material/other costs, provide components, resolve Dissonance/Refrain and cast-trigger effects once. Counterspell/cast-interruption opportunity occurs then, not again at release. Every held spell requires concentration, even ordinarily non-concentration spells; incompatible prior concentration ends. Lost concentration loses the held spell and costs. NEW: select the legal target/area point at release and recheck legality without repaying. At release the hold continues as ordinary spell concentration if required, otherwise ends after resolution. Expired/replaced/countered held spells do not refund paid costs.

Ready movement grants a separate current-Speed budget on release, pays terrain costs and can provoke ordinary opportunity attacks. It grants no extra Action, Bonus Action or interaction.

Focused stance's Reaction restriction also blocks an ordinary Ready release; Ready does not create a Counterspell exception. Holding a spell does not waive any current Reaction prohibition.

**Spell-effect duration begins at release.** Its normal duration is anchored when the effect manifests, while Ready expiry and held concentration already run from preparation. A source explicitly tying a particular consequence to casting/preparation retains that consequence's stated clock. No casting cost, Refrain, Dissonance or cast trigger occurs a second time merely from release.

## Stances

Choose one stance during a **regular** own turn before the first event that would use any stance benefit/restriction: attack, spell, relevant check/save or movement. If none occurs, choose before turn end. No retroactive selection. It lasts until next regular start. NEW: extra turns preserve the stance and spent allowances; they cannot choose/replenish it.

| Stance | Effect |
|---|---|
| Aggressive | +2 damage once per qualifying weapon attack's damage packet; −2 AC. Not periodic or copied damage. |
| Guarded | +1 AC, advantage on explicit roll/contest resisting Shove, Speed −5 (minimum 0). Its +1 can coexist with Guard's first-attack +2, giving +3 then +1. This combination is explicitly allowed here. |
| Mobile | First 5 ft of actual voluntary movement does not provoke; no free movement is granted. Your opportunity attacks reduce each base weapon die one step: d12→d10→d8→d6→d4 (minimum d4). Rider dice unchanged. Die sequence is NEW. |
| Focused | Choose +1 save DC for one spell OR +1 to one attack roll from one spell. After use, no-Reaction-except-Counterspell restriction remains through expiry. This grants no Counterspell knowledge, free cost or extra Reaction. |
| Carrying | Choose one actual currently applicable cargo penalty to ignore; choice fixed through expiry. It does not increase capacity or erase all load limits. DEX saves have disadvantage. |

## Maneuvers and ordinary attacks

All opposed checks use Core total comparison: higher wins, exact tie preserves state. No natural-20 automatic victory or hidden task-degree effect on an opposed tie. A printed save-based class maneuver keeps its own method.

| Maneuver | Execution |
|---|---|
| Grapple | Replace one Attack Action attack; reach and target ≤one size larger. STR Athletics vs defender STR Athletics/DEX Acrobatics. Escape Action uses same opposed contest. NEW one free usable grasping hand/appendage per target; release freely on own turn. Ends if required reach breaks or grappler becomes Incapacitated. No concentration required. Dragging halves Speed unless target ≥two sizes smaller. Magical/card exceptions remain source-specific. |
| Shove | Replace one attack; same reach/size/contest limits; success pushes 5 ft away or knocks Prone. |
| Trip | Replace one melee attack, Athletics vs Athletics/Acrobatics, success Prone. NEW same one-size-larger cap. |
| Disarm | Replace one attack, Athletics or weapon check vs Athletics/Acrobatics. Item must be held and reachable. Attacker chooses legal adjacent unoccupied drop space, otherwise target's own space. Explicit non-droppable bonds prevent it; magic/curse alone does not. No severed attunement/ownership/curse. |
| Feint | Bonus Action Deception vs Insight; success advantage on next melee attack this turn only. |
| Sunder | Attack an object/shield/armor component/construct joint using its actual durability system rather than creature HP. Unspecified durability remains an equipment dependency. |
| Break Formation | Special Shove replacing one attack, same reach/size contest with attacker disadvantage. Success pushes 10 ft; snapshot target's adjacent allies before push and remove their Guard Action benefits. Does not remove Guarded stance or target's own Guard. |
| Overwatch | Ready one ranged attack against movement in a named lane. Reaction and ammunition paid at release. Distinct from Soldier's class engine. |

**Pin and Silence the Caster — NEW tradeoff.** Declare before rolling and take **−2 to that attack roll**. Each creature has one Pin token and one Silence the Caster token between starts of its regular turns. An unused token may be spent on any otherwise legal qualifying attack, including off-turn, extra-turn or readied attacks. A legal declaration followed by an attack roll consumes the token even on a miss; an illegal declaration rejected before rolling consumes nothing. Tokens refresh only at regular own-turn start, never on an extra turn or numbered-round boundary. One attack cannot combine another optional tactical maneuver. These provisional numbers require table playtesting.

Pin uses a ranged weapon attack. On hit deal ordinary damage and apply Speed −10 (floor 0), DC `8 + PB + attack ability modifier`. Ordinary Pins do not stack the penalty. At target's regular start, one optional STR Athletics task check against the highest active ordinary Pin DC ends all ordinary Pins on Success/Critical Success. Alternatively one Action removes all automatically. Source-specific card Pins do not silently acquire this generic definition or removal scope.

Silence the Caster uses a melee attack. On hit prevent verbal-component Reactions until target's next regular start. If concentrating, make exactly one CON concentration save at `max(10, floor(post-mitigation damage/2))`, including DC10 when damage is zero. This fulfills, rather than duplicates, the normal damage concentration check. It is not Core Silenced: speech and Action-time verbal casting remain possible.

**Interpose.** While Guarding, after an adjacent ally becomes an attack target but before its roll, spend Reaction and become target if legal for that attack (range/type/line/cover). NEW may move **up to** 5 ft using a separate terrain-paying budget, including zero if already legally positioned. Speed0 permits the zero-movement case only. It redirects one attack without cancelling or duplicating it. Guard's unspent +2 applies if this is the first attack against you. Voluntary movement has ordinary opportunity-attack consequences.

**Press.** On a melee hit during your regular turn, arm one target until next regular start. While unconsumed, another qualifying hit during that turn may replace it. If the target voluntarily retreats from an adjacent space, follow up to 5 ft into the vacated space using a separate terrain-paying budget; no Action/BA/Reaction. It can provoke ordinary opportunity attacks. No following teleport/forced movement. Once used, cannot rearm before next regular turn, including during an extra turn. Speed0 prevents movement.

**Opportunity attack.** Spend Reaction for one melee attack against a seen hostile creature voluntarily leaving reach, immediately **before** exit. Forced movement/teleport do not trigger; Disengage suppresses it for its stated turn. Specific reviewed triggers may override these conditions.

**Two-weapon fighting.** After taking Attack and attacking with a Light melee weapon in one hand, spend Bonus Action for one attack with a different Light melee weapon in the other hand. Do not add a positive ability modifier to that attack's damage; include a negative modifier. This grants neither another Bonus Action nor a class feature.

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

## Scope and validation

[Reference checks](COMBAT_PLAYTEST_VALIDATION.json) exercise selected budgets, clocks and edge cases. They do not implement map visibility, inventory, feature legality, complete event dispatch, all maneuvers or a live application. No claim of encounter balance or human playtest completion follows from a passing report.

`start_life_sequence` receives already-resolved/arbitrated HP events; it does not perform condition-family arbitration, cure processing, trigger generation, duration expiry, target legality, defense calculations or general simultaneous-event dispatch. `hide_results` answers only whether Hidden is established, collapsing the two success degrees and two failure degrees; it does not retain the full task-degree record. The Reaction helper models the ordinary resource, not additional Reaction grants printed on specific cards.

Remaining work includes cargo terminology/capacity/durability; detailed movement/environment/chases; area templates and sensory abilities; summons/boss full-turn examples; all-source class/spell semantic interactions and specific resource grants; and the whole-game ledger's other acceptance gates.
