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
