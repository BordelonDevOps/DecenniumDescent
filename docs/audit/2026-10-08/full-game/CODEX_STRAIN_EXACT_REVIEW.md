# Exact Strain candidate review

The source-qualified Strain guide and helpers below implement our conference and corrections. Status IN_REVIEW. No source book or normalized class card changed. Namespacing correction is also made in the generic condition/recovery references: neither Strain track is global Exhaustion.

Please adversarially review for source drift, boundary bugs, recovery replay, maxHP/damage confusion, accidental class grants or changing the wrong track. Material points to confirm:

1. Level2 retains -1 attack/save exactly; your earlier level3 summary is corrected in the guide and tests. The actual ending-gain profile is Sanguine Surge; my earlier 'Regenerator' example was not a canonical source name and is not used in the implementation.
2. Dash during its own regular turn excludes the current end and locks through the NEXT future turn's end; I reused the corrected combat marker helper with explicit excluded_current_marker. Dash at1 during current turn ending3→lock through9. Off-turn Dash at4 with own end phase3→9. Outside Dash4→10; crossing initiative preserves original deadline. Please confirm this fixes the imprecise 'strictly after Dash' wording without letting same-turn end clear the lock.
3. RestHistory validates COMPLETED activity intervals and reward histories, not active project management/inventory. Caller owns real care/supplies, legal activities, ongoing interruptions and other rest rewards. It forbids overlapping ordinary activity intervals and overlapping Haven windows; a Haven care window may contain distinct sleep/recreation. Processing order must be chronological, completed IDs cannot replay. Ineligible activity isn't a RestWatch just because it lasts8h and therefore cannot clear Rest Debt. A legal but reward-capped safe RestWatch DOES clear Debt without changing long-rest/short-rest benefit clocks.
4. Ordinary point recovery requires chosen eligible point (or all for Haven). It never alters LifeState, so cannot revive/restoreHP; actual corpse rest/treatment legality is caller-owned. MaxHP projection preserves death counters/dead state and clamps without damage. True expedition death gain calls existing kill(). Collapse retains independently dying0HP state, and later lethal gain at collapsed6 kills despite storage cap.
5. The 30 bindings are NAMESPACE REFERENCES, not triggers: mapping Serum Tolerance to serum Strain does not apply gain or grant immunity. Unknown source IDs are rejected. All30 exact references/track contexts are checked. Broad source integrity separately verifies8engine references,17cards,3campaign sections,12Core paragraphs against unchanged files.
6. Helper track_penalties supplies selected numeric/flag projection, not every Exhaustion/condition/life/collapse effect. Caller adds independently applicable condition effects and derives actual walking/travel pace. No duplicate global Exhaustion immunity or auto-cure by similar name.

Return exact fixes for material findings. If this supplied namespace/recovery package can close after review, say so at bounded scope only; broader condition/all-source, travel/Expedition, rest reward, class grant and human balance gates remain open.

Validation: PASS; 101 total checks (71 transition checks plus30 source checks); 4949 maximumHP scenarios.


# EXACT FILE docs/mechanics/STRAIN_PLAYTEST.md

# Strain — source-qualified playtest reference

**Status: IN REVIEW.** The two names below refer to independent systems. This candidate preserves the Warrior engine and retains the Gameplay Loop's expedition track as a provisional campaign overlay. It does not promote that older table into the approved Core book.

Use [source bindings](../../data/playtest/strain_bindings.json), [source validation](STRAIN_SOURCE_VALIDATION.json), [combat timing](COMBAT_ACTION_PLAYTEST.md), [conditions](CONDITIONS_PLAYTEST.md) and [HP/Wounds](CORE_RESOLUTION_PLAYTEST.md). The [first GPT review](../../../../docs/audit/2026-10-08/full-game/GPT_STRAIN_FIRST_REVIEW.md) and [counterexample corrections](../../../../docs/audit/2026-10-08/full-game/GPT_STRAIN_COUNTEREXAMPLE_REVIEW.md) preserve the decisions. The latter corrects an earlier summary that misplaced the expedition attack/save penalties at level3; their source places them at level2.

## Identify the track first

| Mechanical ID | What it represents | Range | Generic recovery |
|---|---|---:|---|
| `warrior.serum-strain` | The Warrior serum/mutation engine, including an explicit Serum Sharing recipient | 0–3 | Beneficial completed1h Short Rest−1; beneficial completed8h Long Rest→0 |
| `expedition.strain` | Campaign attrition, Rest Debt, unsupported Supply, Quickglass crash and ordinary Wound-treatment critical failure | 0–6 | Secure beneficial Long Rest−1 eligible point; Morale Rest−1; qualifying Haven care removes all eligible ordinary points |

Neither is global `core.exhaustion`, Oracle Revelation backlash, Dissonance or historical Resonance Burn. A single cause applies multiple tracks only if its operative source explicitly says so. Serum3 never becomes expedition3, and serum overflow never becomes expedition6. A namespace binding identifies a reference; it does not itself apply any effect.

Inside the supplied Warrior engine/cards, Strain means serum Strain. In the supplied campaign references, Strain means expedition Strain. **Future ambiguous sources remain unbound until reviewed.** The source register records8 Warrior engine references,17 cards,3 campaign sections and12 exact Core paragraphs. Do not classify a new immunity or source by its name alone.

Quickglass's crash adds1 expedition point and retains its independent one-hour DEX-check disadvantage. Ordinary Wound-treatment Critical Failure adds1 expedition point to the **patient**, without inventing another Wound or Exhaustion level. Morale Rest removes expedition Strain only. Serum Tolerance suppresses the profile side effects it names; it does not prevent serum Strain or its penalties.

## Warrior serum Strain

Preserve the source engine: normal Serum Injection/Mutagen Injection and Mutation Surge add1; Serum Cocktail/Mutation Overload add2 unless a printed modifier applies. Cap3. At2, Speed−5. At3, also AC−1 and saves−1; the source's voluntary serum/Cocktail/Overclock/Surge activation lock applies. All card costs, prepared doses, mutation limits and frequencies remain required.

For an activation explicitly illegal if it exceeds the cap, calculate its **final modified gain first**, including applicable Mutation Adaptation and the minimum1 for Cocktail/Overload where applicable. Reject a resulting value above3. Never clip a voluntary overcap cost into legality. A separate activation lock can still prohibit activation even if a gain modifier makes its cost small or zero.

Automatic later gains, such as the actual **Sanguine Surge** profile's ending side effect, clamp at3. They do not retroactively invalidate the original activation, cause overflow death or add expedition points.

**Serum Sharing — NEW integration.** Its willing recipient receives serum Strain even when not a Warrior. At recipient3, the attempted+1 clamps at3; this is not the recipient activating an otherwise locked class ability. The recipient retains all existing penalties and receives only the card's actual diluted effects and side effects. Source-owner Serum Tolerance does not protect the ally. Recipient Strain uses the same beneficial1h/8h recovery; no serum preparation, mutation slots or other Warrior powers are granted.

## Expedition Strain

NEW interpretation: rows are cumulative. Preserve the original placement of effects:

| Level | Additional consequence |
|---:|---|
| 0 | None |
| 1 | −1 initiative and expedition checks |
| 2 | Speed−10; −1 attacks and saving throws |
| 3 | Disadvantage on expedition checks; Dash lock below |
| 4 | Effective maximum HP×3/4 |
| 5 | Core Incapacitated plus the explicit movement restriction below |
| 6 | Deterministic death/collapse endpoint below |

Initiative−1 applies when a roll is made. Changing Strain does not reorder an established encounter. Ordinary advantage/disadvantage does not numerically stack from multiple sources.

Represent each point with `pointId`, `sourceId`, `ordinaryRemovable` and `removalGateMet`. Level is the active count, maximum6. Keep source history and attempted overflow even when no additional point can be stored. A generic recovery can select only points that are ordinary-removable **and** whose gate is met. A specific treatment can override only the source it expressly covers. Clearing a gate updates metadata; it does not silently delete a point.

**Level6 — NEW deterministic interpretation.** On every positive, unprevented expedition gain that would reach **or exceed6**, evaluate that gain's endpoint before clamping stored points at6. Default: ordinary Dead state. Only that gain's explicit reviewed nonlethal source can instead produce `expedition.collapse`. A living collapsed creature already at6 can die from a later ordinary gain; it is not protected by the cap. A prevented/zero gain causes no endpoint. Nonlethal gains or Strain removal never revive a corpse.

Collapse leaves the creature alive, Unconscious, Speed0 and unable to act/travel. It does not set HP0, grant Stable or create death saves by itself. Independently dying0HP creatures still follow their normal saves. Short/Long/Morale Rest cannot reduce expedition points while this level6 collapse persists; qualifying24h Haven care or explicit treatment may. Collapse ends only when the track falls below6. Other Unconscious sources remain independent. If all six points stay blocked, Haven care cannot clear the collapse by assertion.

## Independent penalties and maximum HP

Apply flat Speed changes first, floor at0, then applicable multipliers and floor normally. A rule setting Speed0 takes precedence. Serum2's−5 and expedition2's−10 coexist: base30 becomes15, then Exhaustion2's half Speed gives7. Mutation Adaptation's explicit serum Speed exception does not cancel expedition Speed loss.

Expedition2 and serum3 each impose saves−1, totaling−2. The class rule against stacking duplicate bonuses does not merge these independent tracks.

NEW maximum-HP composition: multiply applicable rational factors against the same otherwise-applicable maximum, floor **once**, minimum1. Expedition4×3/4 and Exhaustion4×1/2 produce37 from base100. Clamp currentHP down if necessary; that clamp is not damage and triggers no Wound, death-save failure or damage resource. Removing a modifier raises capacity without healing/resetting death counters. Critical Wounds' healing ceiling then uses `max(1, effectiveMaximumHP−1)`; it is not another maxHP multiplier.

The helper accepts other multipliers only after their compatibility has been established elsewhere. It does not decide whether unrelated gear/ancestry/spell modifiers stack.

## Dash lock — NEW

At expedition3–4, a legal Dash consumes the current opportunity and creates a lock. No other Dash is legal while locked, whether Action, Bonus Action, extra Action or extra turn. A non-Dash Action, round boundary or extra turn does not clear it.

In initiative, lock through the **end of the next future regular turn** of the creature. A Dash during its current turn excludes that current end, using the exact marker-exclusion rule from combat. Thus turn1 Dash blocks another that turn and turn2; turn2's end unlocks turn3. An off-turn Dash locks through the next regular turn's end. Extra turns cannot substitute for that marker.

Outside initiative, unlock at Dash time+6 seconds. Preserve whichever endpoint was recorded across initiative entry/exit/reorder; do not restart or convert it. Falling below expedition3 clears the restriction and stored lock immediately. Returning to3 begins unlocked until a new legal Dash. Expedition5 cannot Dash at all.

**Exact-review point:** the second GPT reply used “next regular-turn marker strictly after Dash” while also saying the next regular turn cannot Dash. This reference uses the established next-turn meaning and excludes a current in-progress turn's end; the exact tests will return that interpretation for confirmation.

## Expedition5 and assistance

Core Incapacitated denies Action/Bonus Action/Reaction and ends concentration. NEW expedition-specific restriction: no voluntary tactical movement in initiative. This does **not** redefine generic Incapacitated or automatically set the creature's actual Speed statistic to0. Forced movement, an external legal teleport and lawful carrying still work.

Outside combat, apply the slow-travel exception by halving the otherwise legal walking/travel pace once after applicable load/Speed/environment rules. Do not repeatedly halve per Watch or invent miles-per-hour values here. Detailed stacking with other travel-pace modifiers remains the travel review's responsibility.

Brief communication is possible if no other condition prevents it. The victim cannot use an Action-time consumable by itself. A legal willing recipient can be fed, given a potion or treated by someone paying the actual required Action/activity, supplies and costs. This creates no free administration or universal restraint/capture rule. Rest and Haven care remain possible when their eligibility requirements are met.

## Recovery and actual elapsed time

Preserve campaign limits: Short Rest1h, at most **two beneficial Short Rests between beneficial Long Rests**; Long Rest8h, at most **one beneficial Long Rest per24 elapsed hours**. Those limits apply to serum recovery too, including non-Warrior recipients. Exact completion timestamps and IDs prevent replay. Work, travel, short rest, sleep and recreation cannot spend the same active hours twice. Unfinished/interrupted activity provides no completion benefit.

**Rest Debt order.** First complete a qualifying safe8hRestWatch and clear debt it satisfies. Then evaluate beneficial Long Rest eligibility. If eligible, apply its sourced benefits, including serum reset and one eligible expedition point when secure. Persistent food/water/source blocks still prevent expedition reduction. An additional safe RestWatch inside the24h reward cap can discharge debt but cannot restore resources, remove expedition Strain, reset the beneficial-rest clock or reset short-rest counts.

**Secure Long Rest.** Remove one eligible expedition point chosen by the patient, once the rest qualifies and no reduction block remains. This is a separate benefit from serum reset, so one actual qualifying rest may do both. Class-only serum reduction never silently removes expedition points.

**Morale Rest — NEW endpoint.** Four consecutive safe hours of voluntarily chosen recreation, without forced substance use, work, expedition travel or simultaneous sleep/ShortRest. At most one beneficial Morale Rest per24 elapsed hours. Remove one eligible expedition point. It never removes a Wound. A distinct4hMoraleRest plus an eligible8hsecureLongRest can legitimately remove two points; there is no new shared one-point cap.

**Haven care.** One full day means24 consecutive hours under qualifying Haven care/location conditions, with real care, food and water supplied under campaign rules. One active care interval per patient; interrupted care gives no completion benefit and restarting requires a fresh24h window. At completion remove all eligible ordinary expedition points; blocked/special points remain. The care window may contain separate sleep, meals and4h recreation because it is not24h of active practitioner work. Incompatible practitioner activities cannot be double-counted.

The Strain reference does not replace HP/RP/RC rest rewards or settle all supply prices, travel limits or camp security. Those systems retain their source review gates.

## Immunity, suppression and removal

Only explicit source-qualified wording changes a track. Poison immunity, global Exhaustion immunity, serum-profile tolerance and expedition immunity do not automatically cover serum Strain. Exhaustion removal does not clear either track. An unqualified future “immune to Strain” remains unbound.

- “Cannot gain expedition Strain” blocks gains only.
- “Ignore expedition Strain penalties” retains the points; no implied prevention of gain or level6 endpoint.
- “Remove X expedition Strain” actually removes eligible points under that source.

These tracks do not inherit the generic condition-immunity suppression rule merely because their UI label resembles a condition.

## Reference scope

The implementation in `tools/strain_playtest_rules.py` covers selected namespace lookups, gain/cap/death transitions, point recovery, numeric composition, Dash deadlines and completed-rest accounting. It does not run the campaign, grant class abilities, create inventory, verify all care activities, dispatch conditions or perform resurrection. The caller supplies legality and source eligibility. Its penalty projection does not replace independent life-state, collapse, condition or travel rules.

The [validation report](STRAIN_PLAYTEST_VALIDATION.json) will record the exact bounded checks. This package remains IN REVIEW until the notebook reviews the implemented reference and counterexamples.


# EXACT FILE tools/strain_playtest_rules.py

"""Bounded Strain reference, IN REVIEW; not a live resource or travel engine.

Caller establishes source legality, pays costs and validates supplies/care. Source
binding is explicit. Distinct tracks never convert through matching display names.
"""
from dataclasses import dataclass, field, replace
from fractions import Fraction
from core_playtest_rules import kill
from combat_playtest_rules import marker_deadline
from spell_playtest_rules import integer, SpellRuleError

SERUM='warrior.serum-strain'
EXPEDITION='expedition.strain'


@dataclass(frozen=True)
class StrainPoint:
    point_id: str
    source_id: str
    ordinary_removable: bool = True
    removal_gate_met: bool = True


@dataclass
class StrainState:
    serum: int = 0
    points: tuple = ()
    collapsed: bool = False
    processed_gains: tuple = ()

    def __post_init__(self):
        integer(self.serum,'serum Strain',0,3)
        if len(self.points)>6 or len({p.point_id for p in self.points})!=len(self.points):
            raise SpellRuleError('Expedition points require unique IDs and cap6')
        if self.collapsed and len(self.points)<6:
            raise SpellRuleError('Expedition collapse requires level6')

    @property
    def expedition(self):
        return len(self.points)


def bind_strain(source_id, explicit_bindings):
    track=explicit_bindings.get(source_id)
    if track not in (SERUM,EXPEDITION):
        raise SpellRuleError('Unbound or ambiguous Strain source')
    return track


def serum_gain(state, proposed_gain, *, reduction=0, minimum_gain=0,
               explicit_overcap_illegal=False, activation_locked=False):
    for name,value in [('proposed gain',proposed_gain),('reduction',reduction),('minimum gain',minimum_gain)]:
        integer(value,name,0)
    if activation_locked:
        raise SpellRuleError('Source activation is prohibited at current serum Strain')
    gain=max(minimum_gain,max(0,proposed_gain-reduction))
    if explicit_overcap_illegal and state.serum+gain>3:
        raise SpellRuleError('Voluntary Strain cost cannot be clipped into legality')
    return replace(state,serum=min(3,state.serum+gain))


def expedition_gain(state, life, amount, *, event_id, source_id,
                     prevented=False, nonlethal_source=False,
                     ordinary_removable=True, removal_gate_met=True):
    integer(amount,'Expedition gain',0)
    if life.dead:
        raise SpellRuleError('Strain gain is not resurrection or living-target application to a corpse')
    if event_id in state.processed_gains:
        raise SpellRuleError('Gain event already resolved')
    out=replace(state,processed_gains=state.processed_gains+(event_id,))
    hp=replace(life)
    if prevented or amount==0:
        return out,hp,{'attempted':amount,'added':0,'endpoint':'none'}
    endpoint='none'
    if state.expedition+amount>=6:
        if nonlethal_source:
            endpoint='collapse'
            out.collapsed=True
        else:
            endpoint='death'
            out.collapsed=False
            kill(hp)
    added=min(amount,6-state.expedition)
    new_points=tuple(StrainPoint(f'{event_id}:{i+1}',source_id,ordinary_removable,removal_gate_met) for i in range(added))
    if {p.point_id for p in state.points}&{p.point_id for p in new_points}:
        raise SpellRuleError('New point ID collides with existing provenance')
    out.points=out.points+new_points
    return out,hp,{'attempted':amount,'added':added,'endpoint':endpoint}


def ordinary_recovery(state, kind, *, selected_point=None, reduction_blocked=False):
    if kind not in ('long','morale','haven'):
        raise SpellRuleError('Unknown ordinary Expedition recovery')
    if reduction_blocked or (state.collapsed and kind!='haven'):
        return replace(state),[]
    eligible=[p.point_id for p in state.points if p.ordinary_removable and p.removal_gate_met]
    if kind=='haven':
        removed=eligible
    elif not eligible:
        removed=[]
    elif selected_point not in eligible:
        raise SpellRuleError('Patient must select one legally removable point')
    else:
        removed=[selected_point]
    points=tuple(p for p in state.points if p.point_id not in removed)
    return replace(state,points=points,collapsed=state.collapsed and len(points)==6),removed


def combined_maximum_hp(base_maximum, *, expedition, exhaustion, other_factors=()):
    integer(base_maximum,'otherwise applicable maximumHP',1)
    integer(expedition,'Expedition Strain',0,6)
    integer(exhaustion,'Exhaustion',0,6)
    value=Fraction(base_maximum)
    for factor in other_factors:
        factor=Fraction(factor)
        if factor<=0:
            raise SpellRuleError('MaximumHP multiplier must be positive')
        value*=factor
    if expedition>=4:
        value*=Fraction(3,4)
    if exhaustion>=4:
        value*=Fraction(1,2)
    return max(1,value.numerator//value.denominator)


def apply_effective_maximum(life, maximum):
    integer(maximum,'effective maximumHP',1)
    return replace(life,maximum_hp=maximum,hp=min(life.hp,maximum))


def track_penalties(base_speed, *, serum, expedition, exhaustion=0,
                    other_flat_speed=0, ignore_serum_speed=False):
    integer(base_speed,'base Speed',0)
    integer(serum,'serum Strain',0,3)
    integer(expedition,'Expedition Strain',0,6)
    integer(exhaustion,'Exhaustion',0,6)
    speed=max(0,base_speed+other_flat_speed-(10 if expedition>=2 else 0)
              -(5 if serum>=2 and not ignore_serum_speed else 0))
    if exhaustion>=2:
        speed//=2
    if exhaustion>=5:
        speed=0
    return {'speed':speed,'initiativeModifier':-int(expedition>=1),
            'expeditionCheckModifier':-int(expedition>=1),
            'expeditionCheckDisadvantage':expedition>=3,
            'attackModifier':-int(expedition>=2),
            'saveModifier':-int(expedition>=2)-int(serum>=3),
            'armorClassModifier':-int(serum>=3),
            'incapacitated':expedition>=5,
            'tacticalVoluntaryMovementAllowed':expedition<5,
            'slowTravelMultiplier':Fraction(1,2) if expedition>=5 else Fraction(1),
            'canDashByTrack':expedition<5}


@dataclass
class ExpeditionDashLock:
    until: Fraction | None = None

    def reconcile(self, level, now):
        integer(level,'Expedition Strain',0,6)
        if level<3 or (self.until is not None and Fraction(now)>=self.until):
            self.until=None

    def dash(self, level, now, *, in_initiative, end_marker_phase=None,
             excluded_current_end=None):
        self.reconcile(level,now)
        if level>=5 or self.until is not None:
            raise SpellRuleError('Expedition track currently prevents Dash')
        if level>=3:
            if in_initiative:
                if end_marker_phase is None:
                    raise SpellRuleError('Initiative Dash needs preserved regular-end marker')
                self.until=marker_deadline(now,end_marker_phase,
                                           excluded_current_marker=excluded_current_end)
            else:
                self.until=Fraction(now)+6
        return self.until


@dataclass
class RestHistory:
    """Completed intervals only. Caller owns active/interruptible project state.

    Haven is a care/location window and can contain distinct rest/recreation.
    Other activity intervals cannot overlap, and completed IDs cannot replay.
    """
    last_long_end: int | None = None
    last_morale_end: int | None = None
    short_count: int = 0
    intervals: list = field(default_factory=list)

    def complete(self, state, *, identity, kind, start, end, safe=True,
                 eligible_activity=True, secure=False, food_water=True,
                 rest_debt=False, other_reduction_block=False,
                 interrupted=False, selected_point=None):
        hours={'short':1,'long':8,'morale':4,'haven':24}
        if kind not in hours:
            raise SpellRuleError('Unknown recovery interval')
        integer(start,'activity start',0)
        integer(end,'activity end',start)
        if self.intervals and end<max(r['end'] for r in self.intervals):
            raise SpellRuleError('Resolve completion events chronologically')
        if any(r['id']==identity for r in self.intervals):
            raise SpellRuleError('Completion cannot replay')
        if any(max(start,r['start'])<min(end,r['end']) and
               ((kind=='haven')==(r['kind']=='haven')) for r in self.intervals):
            raise SpellRuleError('Incompatible activity intervals overlap')
        complete=not interrupted and end-start>=hours[kind]*3600
        if complete and eligible_activity and kind=='long' and safe:
            rest_debt=False
        out=replace(state)
        removed=[]
        benefit=False
        block=rest_debt or not food_water or other_reduction_block
        next_short=self.short_count
        next_long=self.last_long_end
        next_morale=self.last_morale_end
        if complete and eligible_activity:
            if kind=='short' and self.short_count<2:
                out.serum=max(0,out.serum-1)
                next_short+=1
                benefit=True
            elif kind=='long' and (self.last_long_end is None or end-self.last_long_end>=86400):
                out.serum=0
                next_long=end
                next_short=0
                benefit=True
                if secure:
                    out,removed=ordinary_recovery(out,'long',selected_point=selected_point,reduction_blocked=block)
            elif kind=='morale' and safe and (self.last_morale_end is None or end-self.last_morale_end>=86400):
                out,removed=ordinary_recovery(out,'morale',selected_point=selected_point,reduction_blocked=block)
                benefit=bool(removed)
                if benefit:
                    next_morale=end
            elif kind=='haven' and safe:
                out,removed=ordinary_recovery(out,'haven',reduction_blocked=block)
                benefit=bool(removed)
        # Commit history only after all selected-point/legality checks succeed.
        self.short_count,self.last_long_end,self.last_morale_end=next_short,next_long,next_morale
        self.intervals.append({'id':identity,'kind':kind,'start':start,'end':end})
        return out,{'beneficial':benefit,'removedPointIds':removed,'restDebt':rest_debt}


# EXACT FILE tools/validate_strain_playtests.py

"""Bounded source/transition tests for the Strain candidate, not full game validation."""
from pathlib import Path
import hashlib
import json
from strain_playtest_rules import *
from core_playtest_rules import LifeState, healing_ceiling

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
    def points(n):
        return tuple(StrainPoint(f'p{i+1}','test-source') for i in range(n))
    bindings=json.loads((ROOT/'data/playtest/strain_bindings.json').read_text(encoding='utf-8'))
    packet=json.loads((ROOT.parents[1]/'docs/audit/2026-10-08/full-game/STRAIN_SOURCE_BINDINGS.json').read_text(encoding='utf-8'))
    warrior=json.loads((ROOT/packet['warriorPath']).read_text(encoding='utf-8'))
    live_cards={c['id']:c for c in warrior['cards']}
    exact_references=0
    for row in bindings['bindings']:
        source=row['source']
        if source['kind']=='engine':
            actual=warrior['engine'][source['index']]
            match=(actual==source['text'] and hashlib.sha256(actual.encode()).hexdigest()==source['textSha256'])
            expected_track=SERUM
        elif source['kind']=='card':
            actual=live_cards.get(source['card']['id'])
            match=(actual==source['card'] and hashlib.sha256(json.dumps(actual,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()==source['sourceObjectSha256'])
            expected_track=SERUM
        elif source['kind']=='core-paragraph':
            original=next(r for r in packet['core']['paragraphs'] if r['paragraph']==source['paragraph'])
            match=(original['text']==source['text'] and hashlib.sha256((ROOT.parents[1]/source['path']).read_bytes()).hexdigest()==source['bookSha256'])
            expected_track=EXPEDITION
        elif source['kind']=='campaign-reference':
            match=hashlib.sha256((ROOT/source['path']).read_bytes()).hexdigest()==source['sha256']
            expected_track=EXPEDITION
        else:
            match=False
            expected_track=None
        check('Exact reference and namespace: '+row['sourceId'],bool(match and row['trackId']==expected_track and row['role']=='namespace-reference'),True)
        exact_references+=1
    lookup={r['sourceId']:r['trackId'] for r in bindings['bindings']}
    check('Binding IDs unique',len(lookup),len(bindings['bindings']))
    check('Quickglass crash explicitly binds expedition',bind_strain('core.quickglass.crash',lookup),EXPEDITION)
    check('Treatment Critical Failure binds patient expedition track',bind_strain('recovery.wound-treatment.critical-failure',lookup),EXPEDITION)
    check('Serum Sharing reference binds recipient serum track',bind_strain('warrior.hero.wardborn.serum-sharing',lookup),SERUM)
    check('Serum Tolerance references serum track without granting immunity',bind_strain('warrior.base.serum-tolerance',lookup),SERUM)
    rejects('Ambiguous future Strain immunity cannot infer namespace',lambda:bind_strain('future.strain-immunity',lookup))
    rejects('Global Exhaustion source is not silently converted',lambda:bind_strain('core.exhaustion',lookup))

    state=StrainState(serum=3,points=points(2))
    automatic=serum_gain(state,1)
    check('Automatic serum overflow clamps independently',(automatic.serum,automatic.expedition),(3,2))
    rejects('Voluntary overcap cost cannot be clipped',lambda:serum_gain(StrainState(serum=2),2,explicit_overcap_illegal=True))
    reduced=serum_gain(StrainState(serum=2),2,reduction=1,minimum_gain=1,explicit_overcap_illegal=True)
    check('Legal gain modifier applies before voluntary cap check',reduced.serum,3)
    minimum=serum_gain(StrainState(),2,reduction=10,minimum_gain=1,explicit_overcap_illegal=True)
    check('Cocktail/Overload minimum gain remains1',minimum.serum,1)
    rejects('Activation lock persists even for zero computed gain',lambda:serum_gain(StrainState(serum=3),1,reduction=1,activation_locked=True))
    check('Sharing recipient at3 accepts clamped attempted gain',serum_gain(StrainState(serum=3),1).serum,3)

    alive=LifeState(20,12)
    s,hp,event=expedition_gain(StrainState(serum=3,points=points(5)),alive,1,event_id='six',source_id='ordinary')
    check('Sixth ordinary expedition point causes death',(hp.dead,hp.hp,s.expedition,s.serum),(True,0,6,3))
    check('Death endpoint report preserves attempted gain',event,{'attempted':1,'added':1,'endpoint':'death'})
    s,hp,event=expedition_gain(StrainState(points=points(5)),alive,1,event_id='collapse',source_id='explicit-nonlethal',nonlethal_source=True)
    check('Explicit nonlethal source preserves HP without granting Stable',(s.collapsed,hp.hp,hp.stable,hp.dead),(True,12,False,False))
    original=s
    s,hp,event=expedition_gain(s,hp,1,event_id='overflow',source_id='ordinary')
    check('Already collapsed6 can die from later ordinary overflow',(s.expedition,hp.dead,event['added']),(6,True,0))
    rejects('Nonlethal gain cannot revive dead creature',lambda:expedition_gain(s,hp,1,event_id='revive',source_id='nonlethal',nonlethal_source=True))
    s,hp,event=expedition_gain(original,alive,1,event_id='blocked',source_id='ordinary',prevented=True)
    check('Prevented overflow does not trigger death',(s.expedition,hp.dead,event['endpoint']),(6,False,'none'))
    rejects('Resolved gain event cannot replay',lambda:expedition_gain(s,hp,1,event_id='blocked',source_id='ordinary'))
    s,hp,event=expedition_gain(StrainState(points=points(5)),LifeState(20,0,death_failures=1),1,event_id='dying-collapse',source_id='nonlethal',nonlethal_source=True)
    check('Collapse leaves independent dying state and counters intact',(hp.hp,hp.stable,hp.death_failures,s.collapsed),(0,False,1,True))
    rejects('Point ID collision cannot duplicate record',lambda:expedition_gain(StrainState(points=(StrainPoint('event:1','old'),)),alive,1,event_id='event',source_id='new'))
    s,hp,event=expedition_gain(StrainState(),alive,20,event_id='large',source_id='ordinary')
    check('Large gain stores no seventh point',(s.expedition,event['attempted'],event['added'],hp.dead),(6,20,6,True))

    p=track_penalties(30,serum=2,expedition=2,exhaustion=2)
    check('Independent flat Speed reductions precede Exhaustion half',p['speed'],7)
    check('Source-correct expedition2 already penalizes attacks',p['attackModifier'],-1)
    check('Source-correct expedition2 already penalizes saves',p['saveModifier'],-1)
    check('Serum3 and expedition2 save penalties both apply',track_penalties(30,serum=3,expedition=2)['saveModifier'],-2)
    check('Mutation Adaptation ignores only serum Speed penalty',track_penalties(30,serum=3,expedition=2,ignore_serum_speed=True)['speed'],20)
    p=track_penalties(30,serum=0,expedition=5)
    check('Expedition5 blocks tactical movement without rewriting Speed',(p['speed'],p['incapacitated'],p['tacticalVoluntaryMovementAllowed']),(20,True,False))
    check('Expedition5 supplies one slow-travel multiplier',p['slowTravelMultiplier'],Fraction(1,2))
    check('Exhaustion5 separately sets Speed0',track_penalties(30,serum=0,expedition=2,exhaustion=5)['speed'],0)
    check('MaximumHP multiplies exact factors and floors once',combined_maximum_hp(100,expedition=4,exhaustion=4),37)
    check('Combined maximum has floor1',combined_maximum_hp(1,expedition=4,exhaustion=4),1)
    hp=apply_effective_maximum(LifeState(100,100,wounds=(None,None,None)),37)
    check('MaxHP clamp changes no Wounds',(hp.hp,hp.maximum_hp,len(hp.wounds)),(37,37,3))
    check('Critical healing ceiling applies after effective maximum',healing_ceiling(hp),36)
    hp=apply_effective_maximum(hp,100)
    check('Restoring maximum capacity does not heal',hp.hp,37)
    corpse=apply_effective_maximum(LifeState(100,0,dead=True),37)
    check('Maximum change cannot revive dead state',(corpse.dead,corpse.hp),(True,0))
    dying=apply_effective_maximum(LifeState(100,0,death_failures=2),37)
    check('Maximum change does not reset dying counters',dying.death_failures,2)
    invariant_states=0
    for base in range(1,102):
        for expedition in range(7):
            for exhaustion in range(7):
                maximum=combined_maximum_hp(base,expedition=expedition,exhaustion=exhaustion)
                old=LifeState(base,base)
                once=apply_effective_maximum(old,maximum)
                twice=apply_effective_maximum(once,maximum)
                restored=apply_effective_maximum(twice,base)
                assert 1<=maximum<=base and once.hp==twice.hp==restored.hp
                assert not once.wounds and not once.dead
                invariant_states+=1

    lock=ExpeditionDashLock()
    check('Own-turn Dash excludes current end3 and locks through9',lock.dash(3,1,in_initiative=True,end_marker_phase=3,excluded_current_end=3),9)
    rejects('Second same-turn Dash blocked',lambda:lock.dash(3,2,in_initiative=True,end_marker_phase=3,excluded_current_end=3))
    lock.reconcile(3,6)
    check('Round/extra-turn time before original endpoint does not clear',lock.until,9)
    lock.reconcile(3,9)
    check('Original next-turn end clears lock',lock.until,None)
    off=ExpeditionDashLock()
    check('Off-turn Dash locks through upcoming own regular end',off.dash(3,4,in_initiative=True,end_marker_phase=3),9)
    off.reconcile(3,8)
    check('Leaving initiative preserves original shorter remaining time',off.until,9)
    outside=ExpeditionDashLock()
    check('Out-of-initiative Dash records absolute six-second endpoint',outside.dash(3,4,in_initiative=False),10)
    outside.reconcile(3,9)
    check('Entering initiative does not reanchor outside lock',outside.until,10)
    outside.reconcile(2,9)
    check('Dropping below3 clears lock',outside.until,None)
    check('Returning to3 permits one new Dash',outside.dash(3,9,in_initiative=False),15)
    rejects('Expedition5 forbids Dash even if unlocked',lambda:ExpeditionDashLock().dash(5,0,in_initiative=False))

    gated=StrainState(points=(StrainPoint('free','ordinary'),StrainPoint('gate','illness',True,False),StrainPoint('special','curse',False,True)))
    recovered,removed=ordinary_recovery(gated,'haven')
    check('Haven removes only ordinary ungated points',(removed,[p.point_id for p in recovered.points]),(['free'],['gate','special']))
    rejects('Cannot choose blocked point for ordinary one-point cure',lambda:ordinary_recovery(gated,'long',selected_point='gate'))
    recovered,removed=ordinary_recovery(original,'long',selected_point='p1')
    check('Nonlethal collapsed6 cannot use generic Long Rest reduction',(recovered.expedition,removed),(6,[]))
    recovered,removed=ordinary_recovery(original,'haven')
    check('Eligible Haven care lowers below6 and ends only own collapse',(recovered.expedition,recovered.collapsed),(0,False))
    all_gated=StrainState(points=tuple(StrainPoint(f'b{i}','locked',True,False) for i in range(6)),collapsed=True)
    recovered,removed=ordinary_recovery(all_gated,'haven')
    check('All six blocked points keep collapse through Haven care',(recovered.expedition,recovered.collapsed),(6,True))

    history=RestHistory()
    state=StrainState(serum=3,points=points(4))
    state,event=history.complete(state,identity='short1',kind='short',start=0,end=3600,rest_debt=True)
    check('Serum Short Rest reduction does not remove expedition points',(state.serum,state.expedition,event['restDebt']),(2,4,True))
    state,event=history.complete(state,identity='short2',kind='short',start=3600,end=7200)
    state,event=history.complete(state,identity='short3',kind='short',start=7200,end=10800)
    check('Third Short Rest gives no extra serum recovery',(state.serum,history.short_count,event['beneficial']),(1,2,False))
    state,event=history.complete(state,identity='long1',kind='long',start=10800,end=39600,secure=True,rest_debt=True,selected_point='p1')
    check('Same safe RestWatch pays debt before its own reduction',(state.serum,state.expedition,event['restDebt']),(0,3,False))
    check('Beneficial Long Rest resets short-rest count',history.short_count,0)
    state=serum_gain(state,2)
    state,event=history.complete(state,identity='long-no-reward',kind='long',start=39600,end=68400,secure=True,rest_debt=True,selected_point='p2')
    check('Extra RestWatch clears debt but grants no second long reward',(state.serum,state.expedition,event['restDebt'],event['beneficial']),(2,3,False,False))
    check('Nonbeneficial watch does not move beneficial Long Rest clock',history.last_long_end,39600)
    rejects('Rest completion ID cannot replay',lambda:history.complete(state,identity='long1',kind='long',start=68400,end=97200))
    state,event=history.complete(state,identity='long2',kind='long',start=97200,end=126000,secure=True,selected_point='p2')
    check('Exactly24h between Long Rest completions permits benefit',(state.serum,state.expedition,event['beneficial']),(0,2,True))
    rejects('Activity overlap cannot grant repeat recovery',lambda:history.complete(state,identity='overlap',kind='morale',start=125000,end=140000,selected_point='p3'))
    rejects('Backdated completion cannot reset histories',lambda:history.complete(state,identity='backdated',kind='short',start=0,end=3600))

    care=RestHistory()
    state=StrainState(serum=3,points=points(4))
    state,event=care.complete(state,identity='recreation',kind='morale',start=0,end=14400,selected_point='p1')
    state,event=care.complete(state,identity='sleep',kind='long',start=14400,end=43200,secure=True,selected_point='p2')
    check('Separate Morale and secure Long Rest remove2 expedition points',(state.serum,state.expedition),(0,2))
    state,event=care.complete(state,identity='care-day',kind='haven',start=0,end=86400)
    check('Haven location-care window may contain distinct sleep/recreation',state.expedition,0)
    rejects('Two overlapping Haven windows cannot double-pay',lambda:care.complete(state,identity='overlap-care',kind='haven',start=43200,end=129600))

    interrupted=RestHistory()
    state,event=interrupted.complete(StrainState(points=points(2)),identity='broken-care',kind='haven',start=0,end=23*3600,interrupted=True)
    check('Interrupted23h care removes nothing',(state.expedition,event['beneficial']),(2,False))
    state,event=interrupted.complete(state,identity='restarted-care',kind='haven',start=23*3600,end=47*3600)
    check('Fresh complete24h care after interruption works',state.expedition,0)
    blocked=RestHistory()
    state,event=blocked.complete(StrainState(serum=3,points=points(2)),identity='food-block',kind='long',start=0,end=28800,secure=True,food_water=False,selected_point='p1')
    check('Persistent food/water block prevents expedition reduction',state.expedition,2)
    invalid=RestHistory()
    state,event=invalid.complete(StrainState(points=points(2)),identity='not-rest',kind='long',start=0,end=28800,safe=True,eligible_activity=False,rest_debt=True)
    check('Non-rest activity cannot pay Rest Debt merely by lasting8h',event['restDebt'],True)

    failures=[r['name'] for r in results if not r['pass']]
    report={'status':'FAIL' if failures else 'PASS','reviewStatus':'IN_REVIEW',
            'scope':'Supplied Strain namespaces, selected cap/HP/Dash/recovery transitions and source metadata. Not full rest, travel, class, inventory or condition dispatch.',
            'namespaceBindings':len(lookup),'exactSourceReferences':exact_references,'checks':len(results),'transitionChecks':len(results)-exact_references,'maximumHpInvariantStates':invariant_states,
            'failures':failures,'results':results,
            'artifacts':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [ROOT/'tools/strain_playtest_rules.py',ROOT/'docs/mechanics/STRAIN_PLAYTEST.md',ROOT/'data/playtest/strain_bindings.json']}}
    (ROOT/'docs/mechanics/STRAIN_PLAYTEST_VALIDATION.json').write_text(json.dumps(report,indent=2,default=str)+'\n',encoding='utf-8')
    print(f"{report['status']}: {len(results)} checks; {invariant_states} maximumHP invariant states; {len(lookup)} namespace bindings; IN_REVIEW")
    for name in failures:
        print('FAIL:',name)
    if failures:
        raise SystemExit(1)


if __name__=='__main__':
    main()

