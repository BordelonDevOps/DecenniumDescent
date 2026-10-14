# Exact combat candidate review

The candidate below implements your first proposal as corrected by our counterexample exchange. Original books and class cards remain unchanged. Source integrity: two unchanged books, 217 exact paragraphs. Reference validation is bounded, not a complete event engine or balance claim. Whole DD03/17/18/19/20/21 remain open.

Please adversarially review the exact guide and helper code below. Identify material contradictions, missing costs, unlimited loops or misleading scope. These specific final interpretations need your disposition:

1. An explicit END OF NEXT target turn applied DURING its current turn excludes that current end. Your earlier next-end wording said strictly-after application (which alone would incorrectly include current end). I implemented skip_current_end for both bare future rounds and explicit next-turn ends. Confirm.
2. Bare N-round ALLY-targeted buffs lacking endpoint: source-start convention unless their text clearly makes a target clock? Confirm or give a different default.
3. Pin/Silence once-per-regular-turn cap: do you mean use only on OWN regular turn, or one attempt between OWN regular starts even when a legal attack occurs off-turn/extra turn? Your reply says extra turns do not replenish but doesn't expressly forbid use. I recommend interval budget usable on any legal qualifying attack, reset own regular start; no new uses from extra turns. Press and stance selection remain explicitly own-regular-turn-only. Need exact text before closing.
4. Ready casting occurs at preparation; I recommend ordinary spell effect duration begins at release, while held concentration and Ready expiry run during preparation. Concentration and RP/Dissonance/Refrain/cast triggers happen once at setup. Confirm no expired duration before effect first exists. Source expressly tied to CAST time can override only its explicit clock. Focused forbids ordinary Ready release; no free Reaction exception.
5. Source Secure Cargo says 'attach, lift, transfer, or protect up to one Extraction Load class'. It does NOT itself mean reduce a handling class. Existing Gameplay guide separates Load (approx10lb/unit; capacity STR with size modifiers) and Extraction Class0–6 (handling danger). I have explicitly left this term/interface open for the cargo audit; no broad cargo closure.
6. Simultaneous effects order is timestamp then stable creation sequence encoding printed same-source internal order. Caller arbitrates periodic families first, then dispatches actual winner packet at its sequence; no extra loser damage. Helper is scoped selected HP events, not all timer/cure/trigger dispatch. Is that sufficient reference scope?

Please give exact fixes for material findings; if this bounded source/action/timing pass can close after these clarifications, say so without closing the larger ledger rows. Then we continue Strain namespacing and remaining conditions/control, and source movement/extraction dependencies.

Current tests: PASS; 97 checks; 285 movement-cost states.


# EXACT FILE: docs/mechanics/COMBAT_ACTION_PLAYTEST.md

# Combat, actions and timing — provisional playtest integration

**Status: implemented candidate; exact review pending.** This reference covers the supplied combat/action/vision sources. It does not close all combat, movement, encounter or condition work. Original books, class cards and earlier drafts are preserved. The NEW decisions below apply to this candidate only.

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

**Surprise — V6 plus NEW Bonus Action clarification.** On a surprised creature's first regular turn it cannot voluntarily move or take an Action or Bonus Action. It cannot react until that turn ends. Its slot, durations, passive effects, concentration, periodic effects and recharge still occur. Surprise alone is not Incapacitated or Unconscious. Brief communication and an otherwise legal simple free interaction remain possible.

**Entry — NEW.** Standard end-round reinforcements roll/receive initiative and first act next round. An explicit midround entrant acts this round only if its complete ordered slot is still upcoming; entry during that exact slot counts as already passed. It has its initial Reaction unless prohibited. A summon-specific timing rule overrides this generic entry procedure.

After the final slot, resolve Core's end-round hazards, reinforcements, morale, objectives and boss phases. Conclude the scene with surrender, capture, pursuit, harvesting access and noise consequences under their own rules; winning initiative does not resolve those automatically.

## Time and event ordering — NEW

For a duration created in initiative, record the relevant original regular start/end marker. Existing effects keep that **virtual marker**, repeating every six seconds if the creature leaves or changes initiative. Reordering, rerolling, extra turns, death/removal or leaving/reentering initiative never restart an existing duration. New effects use the current schedule. Source death still ends concentration, a source-dependent aura/tether or an effect explicitly ending on death.

- A bare hostile target-bound **N rounds** ends at the Nth future regular target-end marker. An in-progress target turn's current end does not count.
- A bare self/source buff or source-controlled aura **N rounds** ends at the Nth future source-start marker. Activation during source turn 1 for three rounds ends at source turn 4's start.
- **Next turn** means the next future regular turn of the named creature, not the current turn's still-upcoming end. An unqualified next turn refers to source/user under the existing shared rule. Explicit “this turn” can include the current turn.
- An outside-initiative bare N-round effect instead gets an absolute application-time + N×6 seconds deadline. Entering initiative preserves that deadline.
- Explicit periodic profiles retain their registered clocks and tick counts. Never create a second timer merely because a generic duration rule also exists.

**Exact-review clarifications pending:** confirm ally-targeted bare buffs use source-start convention; confirm that excluding the in-progress turn applies to explicit “end of next turn” as its ordinary meaning requires. These are implemented interpretations, not claims that GPT explicitly resolved both phrases.

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

**Secure Cargo.** Action for one legal attach, lift, transfer or protective operation involving up to one Extraction Load class under Core 482. Actual load, handling class, hands, harnesses, checks, transfer limits and durability come from the equipment/extraction subsystem. It supplies neither extra capacity nor free equipment or automatic invulnerability. “Extraction Load class” still needs reconciliation with the separate Load and Extraction Class terms; this maneuver is not fully closed.

## Ready

Spend an Action to declare a perceivable trigger and one legal Action-time action or movement. It expires next regular own-turn start. **NEW:** only one pending Ready per creature; replacing it loses the prior setup and any paid held-spell costs. No Bonus Action/Reaction ability, long ritual or multi-minute activity can be prepared by generic Ready.

The trigger happens first, then the readied response immediately follows before later events, unless a specific effect explicitly interrupts. On release spend the normal Reaction and recheck target, range, sight/perception, line of effect, ammunition and other prerequisites. An invalid or declined occurrence spends no release resource; the Ready can wait for another valid occurrence before expiry. This does not undo setup costs. Once released, it is consumed.

For ordinary nonspell actions, feature/ammunition costs are paid on release unless text charges setup. A readied **Attack Action** gets its legally available ordinary attack count; a feature limited to your own turn does not thereby work off-turn. Core Overwatch is explicitly one ranged attack, not that full Attack Action and not Soldier's distinct engine.

A readied spell is actually **cast at preparation**: choose spell/mode, verify legality, pay RP/material/other costs, provide components, resolve Dissonance/Refrain and cast-trigger effects once. Counterspell/cast-interruption opportunity occurs then, not again at release. Every held spell requires concentration, even ordinarily non-concentration spells; incompatible prior concentration ends. Lost concentration loses the held spell and costs. NEW: select the legal target/area point at release and recheck legality without repaying. At release the hold continues as ordinary spell concentration if required, otherwise ends after resolution. Expired/replaced/countered held spells do not refund paid costs.

Ready movement grants a separate current-Speed budget on release, pays terrain costs and can provoke ordinary opportunity attacks. It grants no extra Action, Bonus Action or interaction.

Focused stance's Reaction restriction also blocks an ordinary Ready release; Ready does not create a Counterspell exception. Holding a spell does not waive any current Reaction prohibition.

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

**Pin and Silence the Caster — NEW tradeoff.** Declare before rolling, take **−2 to that attack roll**, one attempt of each maneuver per regular turn, no combining another optional tactical maneuver on that attack. Extra turns do not replenish these limits. These provisional numbers require table playtesting.

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

Remaining work includes cargo terminology/capacity/durability; detailed movement/environment/chases; area templates and sensory abilities; summons/boss full-turn examples; all-source class/spell semantic interactions; ordinary ally-buff timing confirmation; and the whole-game ledger's other acceptance gates.


# EXACT FILE: tools/combat_playtest_rules.py

"""Bounded combat reference helpers; callers supply legal actions, targets and clocks.

These do not form a live combat engine. See COMBAT_ACTION_PLAYTEST.md for source
precedence and the exact NEW provisional decisions represented here.
"""
from dataclasses import dataclass, field, replace
from fractions import Fraction
from core_playtest_rules import task_check, damage_event
from custom_condition_rules import (hp_recovery, death_save_with_hp_prohibition,
                                    stable_recovery_with_hp_prohibition)
from spell_playtest_rules import integer, SpellRuleError


def movement_cost(distance, terrain='normal', *, crawling=False, squeezing=False):
    integer(distance, 'distance', 0)
    if terrain not in ('normal', 'difficult', 'severe'):
        raise SpellRuleError('Unknown terrain')
    return distance * (dict(normal=1, difficult=2, severe=3)[terrain] + int(crawling) + int(squeezing))


@dataclass
class MovementLedger:
    spent: int = 0
    dashes: int = 0

    def __post_init__(self):
        integer(self.spent, 'spent movement', 0)
        integer(self.dashes, 'legal Dash count', 0)

    def remaining(self, speed):
        integer(speed, 'current mode Speed', 0)
        return max(0, (1 + self.dashes) * speed - self.spent)

    def spend(self, cost, speed):
        integer(cost, 'movement cost', 0)
        if cost > self.remaining(speed):
            raise SpellRuleError('Insufficient movement for current mode')
        self.spent += cost

    def stand(self, speed):
        if speed == 0:
            raise SpellRuleError('Cannot stand at Speed 0')
        self.spend(speed // 2, speed)

    def dash(self):
        """Caller must already have paid a legal Dash action."""
        self.dashes += 1


def special_movement_budget(kind, speed):
    integer(speed, 'current Speed', 0)
    if kind not in ('ready', 'withdraw', 'interpose', 'press'):
        raise SpellRuleError('Unknown special movement grant')
    if speed == 0:
        return 0
    return speed if kind == 'ready' else speed // 2 if kind == 'withdraw' else 5


def can_special_move(kind, speed, distance, terrain='normal', **modifiers):
    return movement_cost(distance, terrain, **modifiers) <= special_movement_budget(kind, speed)


@dataclass
class ReactionClock:
    available: bool = True
    surprise_pending: bool = False
    last_regular_start: int = -1

    def regular_start(self, marker):
        integer(marker, 'regular start ordinal', 0)
        if marker <= self.last_regular_start:
            raise SpellRuleError('Regular start cannot repeat or go backwards')
        self.last_regular_start = marker
        self.available = True

    def end_first_regular_turn(self):
        self.surprise_pending = False

    def spend(self, *, prohibited=False):
        if not self.available or self.surprise_pending or prohibited:
            raise SpellRuleError('Reaction unavailable')
        self.available = False

    def extra_turn(self):
        pass

    def round_boundary(self):
        pass


@dataclass
class ExtraActionClock:
    spent_rounds: set = field(default_factory=set)

    def spend(self, round_number, *, granted_by_extra_action=False):
        integer(round_number, 'numbered round', 1)
        if granted_by_extra_action or round_number in self.spent_rounds:
            raise SpellRuleError('Extra full Action cap or recursive grant')
        self.spent_rounds.add(round_number)


def reinforcement_first_round(current_round, *, slot_still_upcoming, end_round_entry=False):
    integer(current_round, 'round', 1)
    return current_round + int(end_round_entry or not slot_still_upcoming)


def marker_deadline(application_time, marker_phase, count=1, *, skip_current_end=False):
    """Preserve original virtual marker phase, recurring every six seconds.

    Times are rational abstract encounter seconds; start/end ordering is supplied
    by the scheduler. skip_current_end excludes an in-progress turn's end for a
    future/next-turn duration. Initiative changes never rewrite returned deadline.
    """
    integer(count, 'marker count', 1)
    now, phase = Fraction(application_time), Fraction(marker_phase)
    cycle = (now - phase) // 6 + 1
    first = phase + cycle * 6
    if skip_current_end:
        first += 6
    return first + (count - 1) * 6


def absolute_duration(application_time, rounds):
    integer(rounds, 'duration rounds', 1)
    return Fraction(application_time) + rounds * 6


def ordered_effects(records):
    """Input sequence must encode printed within-source order before stable ties."""
    ids=[r['applicationId'] for r in records]
    if len(ids)!=len(set(ids)):
        raise SpellRuleError('Duplicate application ID')
    return sorted(records, key=lambda r: (r['appliedAt'], r['applicationSequence'], r['mechanicalId'], r['applicationId']))


def pin_state(records):
    live=[r for r in records if r.get('active', True) and not r.get('suppressed', False)]
    if not live:
        return {'speedPenalty':0, 'dc':None}
    for r in live:
        integer(r['dc'], 'Pin DC', 0)
    return {'speedPenalty':10, 'dc':max(r['dc'] for r in live)}


def silence_concentration(damage, *, concentrating):
    integer(damage, 'post-mitigation damage', 0)
    return {'saves':int(concentrating), 'dc':max(10, damage//2) if concentrating else None}


def passive_perception(modifier):
    if isinstance(modifier, bool) or not isinstance(modifier, int):
        raise SpellRuleError('Perception modifier must be an integer')
    return 10 + modifier


def hide_results(natural, modifier, observers):
    return {o['id']: bool(o['canAttemptHide'] and task_check(natural, modifier, passive_perception(o['perceptionModifier']))['success']) for o in observers}


def best_cover(covers):
    values={'none':0, 'half':2, 'three-quarters':5, 'total':None}
    if any(c not in values for c in covers):
        raise SpellRuleError('Unknown cover')
    if 'total' in covers:
        return {'directTargetLegal':False,'bonus':None}
    return {'directTargetLegal':True,'bonus':max((values[c] for c in covers),default=0)}


def ranged_range(distance, normal, long):
    for name,value in [('distance',distance),('normal range',normal),('long range',long)]:
        integer(value,name,0)
    if long < normal:
        raise SpellRuleError('Long range below normal range')
    return {'legal':distance <= long, 'disadvantage':normal < distance <= long}


def opportunity_trigger(*, seen, hostile, voluntary, exits_reach, teleported=False, disengaged=False):
    return bool(seen and hostile and voluntary and exits_reach and not teleported and not disengaged)


def mobile_base_dice(dice):
    steps={12:10,10:8,8:6,6:4,4:4}
    if any(d not in steps for d in dice):
        raise SpellRuleError('Unsupported base weapon die')
    return [steps[d] for d in dice]


@dataclass
class ReadyController:
    """Small state model of one Ready and spell RP/holding concentration only.

    Caller validates spell access, components, legal Action cost and all external
    effects. cast_events counts cast opportunities, not automatic proc success.
    """
    rp: int
    concentration: str | None = None
    pending: dict | None = None
    cast_events: int = 0
    setup_actions: int = 0

    def __post_init__(self):
        integer(self.rp, 'RP', 0)

    def cancel(self):
        if self.pending and self.pending['kind'] == 'spell' and self.concentration == self.pending['id']:
            self.concentration = None
        self.pending = None

    def prepare(self, identity, kind, *, activation='Action', rp_cost=0,
                ordinary_attack_count=1, ongoing_concentration=False):
        if activation != 'Action' or kind not in ('spell', 'attack', 'movement'):
            raise SpellRuleError('Generic Ready requires a legal Action or movement')
        integer(rp_cost, 'spell RP cost', 0)
        integer(ordinary_attack_count, 'ordinary attack count', 1)
        if kind != 'spell' and rp_cost:
            raise SpellRuleError('This model charges only spell setup RP')
        if rp_cost > self.rp:
            raise SpellRuleError('Insufficient RP')
        self.cancel()
        self.setup_actions += 1
        self.pending = {'id':identity, 'kind':kind, 'attacks':ordinary_attack_count,
                        'ongoingConcentration':ongoing_concentration}
        if kind == 'spell':
            self.rp -= rp_cost
            self.cast_events += 1
            self.concentration = identity

    def lose_concentration(self):
        self.concentration = None
        if self.pending and self.pending['kind'] == 'spell':
            self.pending = None

    def release(self, reaction, *, trigger_matches, legal_target=True, reaction_prohibited=False):
        if not self.pending or not trigger_matches or not legal_target:
            return None
        if not reaction.available or reaction.surprise_pending or reaction_prohibited:
            return None
        out = dict(self.pending)
        reaction.spend()
        if out['kind'] == 'spell' and not out['ongoingConcentration']:
            self.concentration = None
        self.pending = None
        return out


@dataclass
class PressState:
    target: str | None = None
    consumed: bool = False

    def regular_start(self):
        self.target, self.consumed = None, False

    def arm(self, target, *, own_regular_turn, qualifying_melee_hit):
        if not own_regular_turn or not qualifying_melee_hit or self.consumed:
            raise SpellRuleError('No legal Press arming allowance')
        self.target = target

    def follow(self, target, *, voluntary_retreat, legal_movement):
        if self.target != target or not voluntary_retreat or not legal_movement or self.consumed:
            return False
        self.target, self.consumed = None, True
        return True


@dataclass
class GuardState:
    active: bool = False
    first_attack_bonus: bool = False

    def activate(self):
        self.active, self.first_attack_bonus = True, True

    def attacked(self, *, guarded_stance=False):
        bonus = (2 if self.active and self.first_attack_bonus else 0) + int(guarded_stance)
        self.first_attack_bonus = False
        return bonus

    def end(self):
        self.active, self.first_attack_bonus = False, False


def start_life_sequence(state, *, regular_turn_id, now_seconds, death_natural=None,
                        stable_d4=None, hp_prohibited=False,
                        prohibition_expires=False, effects=()):
    """Selected living HP transitions only, after other start expirations/clocks.

    Caller supplies legal, already-arbitrated damage/healing effects. No automatic
    resurrection and no second death save after a start effect newly drops to 0.
    """
    prohibited = hp_prohibited and not prohibition_expires
    out = stable_recovery_with_hp_prohibition(state, now_seconds, prohibited=prohibited)
    log=[]
    if out.hp != state.hp:
        log.append('due-stable-recovery')
    if not out.dead and not out.stable and out.hp == 0 and out.uses_death_saves:
        if death_natural is None:
            raise SpellRuleError('Dying creature requires its start death save')
        out = death_save_with_hp_prohibition(out, death_natural,
            prohibited=prohibited, regular_turn_id=regular_turn_id,
            stable_d4=stable_d4, now_seconds=now_seconds)
        log.append('death-save')
    for e in ordered_effects(effects):
        if e['kind'] not in ('damage','heal'):
            raise SpellRuleError('HP sequence supports only damage and healing')
        if out.dead:
            log.append(e['applicationId']+':dead-target-skipped')
            continue
        if e['kind']=='heal':
            out=hp_recovery(out,e['amount'],prohibited=prohibited)
        else:
            out,_=damage_event(out,e['amount'],now_seconds=now_seconds,**e.get('damageOptions',{}))
        log.append(e['applicationId'])
    return out, log


# EXACT FILE: tools/validate_combat_playtests.py

"""Adversarial checks for the bounded combat reference, not a full game engine."""
from pathlib import Path
from fractions import Fraction
import hashlib
import json
from combat_playtest_rules import *
from core_playtest_rules import LifeState, task_check, opposed_check

ROOT=Path(__file__).resolve().parents[1]


def main():
    results=[]
    def check(name,actual,expected):
        results.append({'name':name,'pass':actual==expected,'actual':actual,'expected':expected})
    def rejects(name,operation):
        try:
            operation()
        except SpellRuleError:
            check(name,True,True)
        else:
            check(name,False,True)

    clock=ReactionClock()
    clock.spend()
    check('Initial reaction can be spent before first regular turn',clock.available,False)
    clock.regular_start(0)
    clock.spend()
    check('First regular start refreshes despite same numbered round',clock.available,False)
    clock.round_boundary()
    clock.extra_turn()
    check('Neither round boundary nor extra turn refreshes Reaction',clock.available,False)
    rejects('Repeated regular marker cannot refresh twice',lambda:clock.regular_start(0))
    surprised=ReactionClock(surprise_pending=True)
    surprised.regular_start(0)
    rejects('Surprised first turn refresh does not permit Reaction',surprised.spend)
    surprised.end_first_regular_turn()
    surprised.spend()
    check('Surprise ending unlocks one available Reaction',surprised.available,False)
    extra=ExtraActionClock()
    extra.spend(1)
    rejects('Second extra full Action in same numbered round rejected',lambda:extra.spend(1))
    rejects('Extra Action cannot recursively grant another',lambda:extra.spend(2,granted_by_extra_action=True))
    extra.spend(2)
    check('New numbered round allows a separately granted extra Action',extra.spent_rounds,{1,2})
    check('Midround entrant with upcoming slot acts now',reinforcement_first_round(3,slot_still_upcoming=True),3)
    check('Exact/passed slot entrant waits until next round',reinforcement_first_round(3,slot_still_upcoming=False),4)
    check('End-round entry always first acts next round',reinforcement_first_round(3,slot_still_upcoming=True,end_round_entry=True),4)

    move=MovementLedger()
    move.spend(movement_cost(10,'difficult'),30)
    check('Difficult terrain cost retained on switch to Fly30',move.remaining(30),10)
    move.dash()
    check('First legal Dash adds another current Speed',move.remaining(30),40)
    move.dash()
    check('Second legal Dash adds Speed again',move.remaining(30),70)
    move=MovementLedger()
    move.stand(30)
    check('Standing expenditure is retained on switching modes',move.remaining(30),15)
    move=MovementLedger(spent=20)
    check('Speed reduction does not create negative remaining budget',move.remaining(15),0)
    check('Restored Speed restores only genuinely unspent budget',move.remaining(30),10)
    check('Speed increase expands cap without refunding spent cost',move.remaining(40),20)
    rejects('Over-budget movement is rejected',lambda:move.spend(11,30))
    check('Rejected movement leaves ledger unchanged',move.spent,20)
    rejects('Cannot stand at Speed0',lambda:move.stand(0))
    check('Crawl and squeeze in difficult terrain add costs',movement_cost(5,'difficult',crawling=True,squeezing=True),20)
    check('Severe plus crawling costs4 per foot',movement_cost(5,'severe',crawling=True),20)
    check('Interpose5 cannot enter difficult tile costing10',can_special_move('interpose',30,5,'difficult'),False)
    check('Press5 can follow one normal tile',can_special_move('press',30,5),True)
    check('Speed0 blocks positive special movement',can_special_move('press',0,5),False)
    check('Interpose may stay in place at Speed0 if legally positioned',can_special_move('interpose',0,0),True)
    check('Ready movement uses current Speed at release',special_movement_budget('ready',20),20)
    check('Withdraw odd Speed uses floor half budget',special_movement_budget('withdraw',25),12)
    check('Separate movement grant leaves ordinary ledger unchanged',move.spent,20)

    # Independent invariant: mode changes cannot reduce the paid-cost ledger.
    movement_states=0
    for spent in range(0,91,5):
        for speed in (0,5,15,30,60):
            for dashes in (0,1,2):
                m=MovementLedger(spent,dashes)
                old_spent=m.spent
                cap=(1+dashes)*speed
                remaining=m.remaining(speed)
                assert remaining>=0 and remaining<=cap
                assert remaining+spent==max(cap,spent)
                m.remaining(0)
                m.remaining(60)
                assert m.spent==old_spent
                movement_states+=1

    check('Two future target ends count two preserved markers',marker_deadline(1,3,2),9)
    check('Current in-progress target end excluded from two-turn duration',marker_deadline(1,3,2,skip_current_end=True),15)
    check('Three-round self effect during turn1 expires at turn4 start',marker_deadline(Fraction(1,2),0,3),18)
    check('Exact application/start tie means next future start',marker_deadline(0,0,1),6)
    check('Explicit next-turn end excludes current in-progress end',marker_deadline(1,3,1,skip_current_end=True),9)
    deadline=marker_deadline(1,3,2)
    check('Leaving initiative preserves original absolute marker deadline',deadline,9)
    check('Out-of-initiative duration remains absolute through entry',absolute_duration(2,3),20)

    ready=ReadyController(10,concentration='old-spell')
    ready.prepare('held','spell',rp_cost=3)
    check('Ordinarily nonconcentration held spell replaces old concentration',ready.concentration,'held')
    check('Readied spell pays RP and casts at preparation', (ready.rp,ready.cast_events),(7,1))
    rx=ReactionClock()
    check('Illegal release leaves pending spell and Reaction intact',ready.release(rx,trigger_matches=True,legal_target=False),None)
    check('Invalid release does not refund or repay', (ready.rp,ready.pending['id'],rx.available),(7,'held',True))
    out=ready.release(rx,trigger_matches=True)
    check('Nonconcentration spell releases holding concentration',(out['id'],ready.concentration),('held',None))
    check('Release consumes Reaction but does not recast',(rx.available,ready.rp,ready.cast_events),(False,7,1))
    check('No second release from consumed Ready',ready.release(ReactionClock(),trigger_matches=True),None)
    ready.prepare('sustained','spell',rp_cost=2,ongoing_concentration=True)
    ready.release(ReactionClock(),trigger_matches=True)
    check('Concentration spell continues seamlessly after release',ready.concentration,'sustained')
    ready.prepare('discarded','spell',rp_cost=1)
    ready.prepare('replacement','attack',ordinary_attack_count=2)
    check('Replacing held spell loses costs and held concentration',(ready.rp,ready.concentration),(4,None))
    attacks=ready.release(ReactionClock(),trigger_matches=True)
    check('Readied ordinary Attack retains legal multiple attacks',attacks['attacks'],2)
    ready.prepare('expired','spell',rp_cost=1)
    ready.cancel()
    check('Ready expiry loses held spell without refund',(ready.pending,ready.rp,ready.concentration),(None,3,None))
    rejects('Cannot Ready a Bonus Action spell',lambda:ready.prepare('bad','spell',activation='Bonus Action'))
    check('Failed prepare does not charge setup action',ready.setup_actions,5)
    ready.prepare('lost','spell',rp_cost=1)
    ready.lose_concentration()
    check('Lost concentration loses held spell and costs',(ready.pending,ready.rp),(None,2))
    ready.prepare('wait','attack')
    spent_rx=ReactionClock(available=False)
    check('Used Reaction prevents Ready release',ready.release(spent_rx,trigger_matches=True),None)
    check('Unreleased action remains pending',ready.pending['id'],'wait')
    check('Focused Reaction restriction also blocks ordinary Ready release',ready.release(ReactionClock(),trigger_matches=True,reaction_prohibited=True),None)
    check('Blocked Ready release retains its pending state',ready.pending['id'],'wait')

    guard=GuardState()
    guard.activate()
    check('Guard and Guarded combine for first attack',guard.attacked(guarded_stance=True),3)
    check('Miss also consumes Guard first-attack benefit',guard.attacked(guarded_stance=True),1)
    check('Spent first-attack bonus preserves Interpose Guard state',guard.active,True)
    guard.end()
    check('Break Formation/end clears Guard state',guard.active,False)
    press=PressState()
    press.arm('A',own_regular_turn=True,qualifying_melee_hit=True)
    press.arm('B',own_regular_turn=True,qualifying_melee_hit=True)
    check('Unspent Press can change target',press.target,'B')
    check('Forced retreat cannot trigger Press',press.follow('B',voluntary_retreat=False,legal_movement=True),False)
    check('Legal voluntary retreat consumes Press',press.follow('B',voluntary_retreat=True,legal_movement=True),True)
    rejects('Cannot rearm spent Press on same regular turn',lambda:press.arm('A',own_regular_turn=True,qualifying_melee_hit=True))
    rejects('Extra turn cannot arm fresh Press',lambda:PressState().arm('A',own_regular_turn=False,qualifying_melee_hit=True))
    check('Multiple Pins use single penalty and highest DC',pin_state([{'dc':12},{'dc':16}]),{'speedPenalty':10,'dc':16})
    check('Suppressed Pin does not raise effective DC',pin_state([{'dc':12},{'dc':16,'suppressed':True}]),{'speedPenalty':10,'dc':12})
    check('Silence hit at zero damage forces one DC10 concentration save',silence_concentration(0,concentrating=True),{'saves':1,'dc':10})
    check('Silence positive damage produces one concentration save',silence_concentration(31,concentrating=True),{'saves':1,'dc':15})
    check('No concentration means no gratuitous concentration check',silence_concentration(31,concentrating=False),{'saves':0,'dc':None})
    check('Opposed Grapple tie preserves state',opposed_check(15,3,12,6)['changesState'],False)
    check('Mobile steps base dice only and keeps d4 floor',mobile_base_dice([6,6,4]),[4,4,4])

    observers=[{'id':'A','canAttemptHide':True,'perceptionModifier':4},
               {'id':'B','canAttemptHide':True,'perceptionModifier':8},
               {'id':'C','canAttemptHide':False,'perceptionModifier':0}]
    check('One Hide roll resolves observer DCs and eligibility separately',hide_results(10,4,observers),{'A':True,'B':False,'C':False})
    check('Natural1 shifts meet-DC Hide to failure',hide_results(1,13,observers)['A'],False)
    check('Natural20 may lift below-DC result to success',hide_results(20,-3,observers)['B'],True)
    check('Search static-DC tie succeeds before natural adjustment',task_check(10,4,14)['success'],True)
    check('Search natural1 can downgrade static-DC success',task_check(1,13,14)['success'],False)
    check('Cover uses best value, never adds2and5',best_cover(['half','three-quarters']),{'directTargetLegal':True,'bonus':5})
    check('Total cover from actual origin bars target',best_cover(['half','total'])['directTargetLegal'],False)
    check('Normal range boundary legal without range disadvantage',ranged_range(60,60,120),{'legal':True,'disadvantage':False})
    check('Long range boundary legal with disadvantage',ranged_range(120,60,120),{'legal':True,'disadvantage':True})
    check('Beyond long range illegal',ranged_range(125,60,120)['legal'],False)
    oa=dict(seen=True,hostile=True,voluntary=True,exits_reach=True)
    check('Seen voluntary exit provokes',opportunity_trigger(**oa),True)
    check('Forced exit does not provoke',opportunity_trigger(**dict(oa,voluntary=False)),False)
    check('Teleport does not provoke',opportunity_trigger(**oa,teleported=True),False)
    check('Disengage prevents ordinary opportunity trigger',opportunity_trigger(**oa,disengaged=True),False)
    check('Unseen exit does not provoke ordinary opportunity attack',opportunity_trigger(**dict(oa,seen=False)),False)

    def effect(identity,kind,amount,order=0,**opts):
        return {'applicationId':identity,'mechanicalId':identity,'appliedAt':0,
                'applicationSequence':order,'kind':kind,'amount':amount,'damageOptions':opts}
    s,log=start_life_sequence(LifeState(20,0),regular_turn_id=1,now_seconds=6,death_natural=5,effects=[effect('heal','heal',4)])
    check('Dying death save precedes ordinary start healing',log,['death-save','heal'])
    check('Later start healing restores HP and clears failed death save',(s.hp,s.death_failures),(4,0))
    s,log=start_life_sequence(LifeState(20,0,death_failures=2),regular_turn_id=1,now_seconds=6,death_natural=5,effects=[effect('heal','heal',4)])
    check('Fatal death save cannot be reversed by later ordinary healing',(s.dead,log),(True,['death-save','heal:dead-target-skipped']))
    s,log=start_life_sequence(LifeState(20,0,stable=True,stable_until_seconds=3600),regular_turn_id=1,now_seconds=6,effects=[effect('bleed','damage',1)])
    check('Stable victim skips death save before start damage',(log,s.stable,s.death_failures),(['bleed'],False,1))
    s,log=start_life_sequence(LifeState(20,0),regular_turn_id=1,now_seconds=6,death_natural=20,effects=[effect('bleed','damage',1,wound_natural=20)])
    check('Natural20 then Bleed is new drop not already-zero failure',(s.hp,s.death_failures,log),(0,0,['death-save','bleed']))
    stable=LifeState(20,0,stable=True,stable_until_seconds=5)
    s,log=start_life_sequence(stable,regular_turn_id=1,now_seconds=6,hp_prohibited=True,prohibition_expires=True)
    check('Expired prohibition permits due Stable recovery before death phase',(s.hp,log),(1,['due-stable-recovery']))
    s,log=start_life_sequence(stable,regular_turn_id=1,now_seconds=6,hp_prohibited=True)
    check('Still-blocked Stable timer retains original deadline',(s.hp,s.stable_until_seconds,log),(0,5,[]))
    healing=effect('first-heal','heal',2,0)
    damage=effect('later-damage','damage',3,1,wound_natural=20)
    s,log=start_life_sequence(LifeState(20,1),regular_turn_id=1,now_seconds=6,effects=[damage,healing])
    check('Application sequence overrides caller list order',log,['first-heal','later-damage'])
    check('Start effect newly dropping to0 does not add second start save',(s.hp,s.last_death_turn),(0,0))
    rejects('Duplicate application cannot dispatch twice',lambda:ordered_effects([healing,healing]))

    failed=[r['name'] for r in results if not r['pass']]
    report={'status':'FAIL' if failed else 'PASS','reviewStatus':'IMPLEMENTED; EXACT REVIEW PENDING',
            'scope':'Selected combat reference budgets, marker calculations, Ready state and HP ordering. Not a full engine, all-source semantic audit or balance test.',
            'checks':len(results),'movementInvariantStates':movement_states,'failed':failed,'results':results,
            'artifacts':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [ROOT/'tools/combat_playtest_rules.py',ROOT/'docs/mechanics/COMBAT_ACTION_PLAYTEST.md']}}
    (ROOT/'docs/mechanics/COMBAT_PLAYTEST_VALIDATION.json').write_text(json.dumps(report,indent=2,default=lambda v:sorted(v) if isinstance(v,set) else str(v))+'\n',encoding='utf-8')
    print(f"{report['status']}: {len(results)} checks; {movement_states} movement-cost invariant states")
    for name in failed:
        print('FAIL:',name)
    if failed:
        raise SystemExit(1)


if __name__=='__main__':
    main()

