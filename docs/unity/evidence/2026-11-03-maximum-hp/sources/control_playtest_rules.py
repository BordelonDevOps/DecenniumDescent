"""Selected control interfaces. Callers validate actual sources, costs and clocks.

These helpers do not cast spells, apply all card effects, schedule turns, choose
targets, or grant actions. Printed application and endpoint rules remain in the
source-qualified registry and guide. No name-based condition inference occurs.
"""
from dataclasses import dataclass, field, replace
from fractions import Fraction
from uuid import uuid4
from spell_playtest_rules import integer, SpellRuleError
from combat_playtest_rules import marker_deadline


@dataclass(frozen=True, order=True)
class ClockMarker:
    seconds: Fraction
    phase: int = 0

    def __post_init__(self):
        if isinstance(self.seconds,bool) or not isinstance(self.seconds,(int,float,Fraction)):
            raise SpellRuleError('Invalid elapsed seconds')
        try:
            seconds=Fraction(self.seconds)
        except (ValueError,OverflowError):
            raise SpellRuleError('Elapsed seconds must be finite') from None
        if seconds<0:
            raise SpellRuleError('Elapsed seconds must be nonnegative')
        object.__setattr__(self,'seconds',seconds)
        integer(self.phase,'ordered event phase',0)


END_EFFECT_APPLICATION=10
END_EFFECT_EXPIRY=20
NEXT_EVENT=30


def clock_marker(value):
    return value if isinstance(value,ClockMarker) else ClockMarker(value)


def require_deadline(value):
    if not isinstance(value,ClockMarker):
        raise SpellRuleError('Choose an explicit absolute/start/end deadline marker')
    return value


def absolute_deadline(seconds):
    return ClockMarker(seconds)


def turn_end_deadline(seconds):
    return ClockMarker(seconds,END_EFFECT_EXPIRY)


def regular_control_endpoint(application_time, regular_marker_phase, *, count=1,
                             boundary='end', excluded_current_marker=None):
    """Adapt reviewed six-second virtual schedule to the correct event phase.

    Owner/target selection remains source-specific. Use end for every explicit
    current/future turn END and Nth target end, start for source/target START.
    Bare outside-initiative elapsed deadlines use absolute_deadline instead.
    """
    if boundary not in ('start','end'):
        raise SpellRuleError('Choose regular start or end boundary')
    seconds=marker_deadline(application_time,regular_marker_phase,count=count,
                            excluded_current_marker=excluded_current_marker)
    return turn_end_deadline(seconds) if boundary=='end' else absolute_deadline(seconds)


@dataclass(frozen=True)
class SpeedRecord:
    application_id: str
    owner: str
    target: str
    group: str
    profile: str
    mode: str
    amount: int = 0
    floor: int = 0
    expires: ClockMarker | None = None
    active: bool = True
    suppressed: bool = False
    slowed_hook: bool = True

    def __post_init__(self):
        for value in (self.application_id, self.owner, self.target, self.group, self.profile):
            if not isinstance(value, str) or not value:
                raise SpellRuleError('Record identities must be nonempty strings')
        if self.mode not in ('flat', 'half', 'half-minus', 'zero'):
            raise SpellRuleError('Unreviewed Speed transform')
        integer(self.amount, 'Speed reduction amount', 0)
        integer(self.floor, 'source minimum Speed', 0)
        if self.expires is not None:
            require_deadline(self.expires)
        if self.mode in ('half', 'zero') and (self.amount or self.floor):
            raise SpellRuleError('Half/zero profiles accept no flat amount or floor')

    def operative(self, now):
        marker=clock_marker(now)
        return self.active and not self.suppressed and (self.expires is None or marker < clock_marker(self.expires))

    def result(self, pre_control_speed):
        integer(pre_control_speed, 'Speed before hostile control', 0)
        if self.mode == 'zero':
            return 0
        if self.mode == 'half':
            value = pre_control_speed // 2
        elif self.mode == 'half-minus':
            value = pre_control_speed // 2 - self.amount
        else:
            value = pre_control_speed - self.amount
        # A minimum attached to a penalty must never increase an existing Speed.
        return min(pre_control_speed, max(self.floor, value, 0))


def effective_control_speed(pre_control_speed, records, *, target, now=0,
                            global_multiplier=Fraction(1), core_speed_zero=False,
                            hypermutation_baseline=None, mode_possessed=True):
    """Strongest adverse transform against ONE common baseline, then multiplier.

    Systemic flat penalties were already applied to the input; terrain is not
    included. Core Grappled/Restrained and other independently established zero
    states are passed separately. Explicit exceptional stacking/floors require
    their own reviewed adapter and are not silently guessed here.
    """
    integer(pre_control_speed, 'Speed before hostile control', 0)
    clock_marker(now)
    if not isinstance(global_multiplier, Fraction) or not 0 <= global_multiplier <= 1:
        raise SpellRuleError('Use an exact reviewed reduction multiplier')
    ids = [r.application_id for r in records]
    if len(ids) != len(set(ids)):
        raise SpellRuleError('Duplicate application ID')
    if any(r.target != target for r in records):
        raise SpellRuleError('One target per calculation')
    eligible = [r for r in records if r.operative(now)]
    speed = min([pre_control_speed] + [r.result(pre_control_speed) for r in eligible])
    speed = speed * global_multiplier.numerator // global_multiplier.denominator
    if hypermutation_baseline is not None:
        integer(hypermutation_baseline,'captured normal mode Speed',0)
        speed=max(speed,hypermutation_baseline//2)
    immobilized=core_speed_zero or any(r.mode=='zero' for r in eligible)
    return 0 if immobilized or not mode_possessed else speed


def slowed_foe(records, *, target, now=0):
    """Overshadowed is still active; suppressed/expired never grants the hook."""
    return any(r.target == target and r.slowed_hook and r.operative(now) for r in records)


def refresh_speed_record(records, incoming, *, now=0):
    """One owner/target/group/exact profile refreshes without adding magnitude.

    Differing transform/magnitude profiles keep separate deadlines, so a later
    weaker slow cannot erase an earlier strong one. No expired record is revived
    except by this caller-validated new application. This is not a free refresh.
    """
    marker=clock_marker(now)
    if incoming.expires is not None and clock_marker(incoming.expires)<=marker:
        raise SpellRuleError('A new refresh cannot have an already-passed deadline')
    key = lambda r: (r.owner, r.target, r.group, r.profile, r.mode, r.amount, r.floor)
    result = list(records)
    matching = [i for i,r in enumerate(result)
                if key(r)==key(incoming) and r.active and (r.expires is None or clock_marker(r.expires)>marker)]
    if len(matching)>1:
        raise SpellRuleError('Aggregate duplicate exact profiles before refreshing')
    if matching:
        i=matching[0]
        old=result[i]
        end=None if old.expires is None or incoming.expires is None else max([old.expires,incoming.expires],key=clock_marker)
        # Retain the existing component suppression; application did not grant immunity removal.
        result[i]=replace(old,expires=end)
    else:
        if any(r.application_id==incoming.application_id for r in result):
            raise SpellRuleError('A new application needs a unique identity')
        result.append(incoming)
    return result


@dataclass
class GuidingStarMark:
    owner: str
    target: str
    expires: ClockMarker
    s: int
    attack_bonus_available: bool = True
    hit_rider_available: bool = True
    active: bool = True
    _identity: str = field(default_factory=lambda:uuid4().hex,init=False,repr=False)
    _next_token: int = field(default=0,init=False,repr=False)
    _pending: set = field(default_factory=set,init=False,repr=False)

    def __post_init__(self):
        integer(self.s,'Oracle scaling S',1)
        require_deadline(self.expires)

    def begin_ally_attack(self, *, actor, ally_of_owner, now, legal=True, suppressed=False):
        """Commit one legal qualifying attack roll, obtain bonus BEFORE rolling.

        Caller checks all attack legality before beginning. A started roll spends
        the bonus entitlement; no resource/roll refund is granted by this helper.
        """
        if (not self.active or suppressed or clock_marker(now)>=clock_marker(self.expires) or not legal
                or actor==self.owner or not ally_of_owner):
            return {'attackBonus':0,'attackToken':None}
        bonus=2 if self.attack_bonus_available else 0
        self.attack_bonus_available=False
        self._next_token+=1
        token=(self._identity,self._next_token)
        self._pending.add(token)
        return {'attackBonus':bonus,'attackToken':token}

    def resolve_ally_attack(self, token, *, hit, now, suppressed=False):
        """Resolve this mark's previously begun attack exactly once."""
        if token not in self._pending:
            raise SpellRuleError('Unknown, foreign or already-resolved attack token')
        self._pending.remove(token)
        if (self.active and not suppressed and clock_marker(now)<clock_marker(self.expires)
                and hit and self.hit_rider_available):
            self.hit_rider_available=False
            self.active=False
            return {'radiantBonus':self.s}
        return {'radiantBonus':0}


@dataclass
class WrathfulBrand:
    owner: str
    target: str
    expires: ClockMarker
    owner_rider_available: bool = True
    ally_rider_available: bool = True
    active: bool = True

    def __post_init__(self):
        require_deadline(self.expires)

    def trigger(self, *, actor, ally_of_owner, now, resolved_damage,
                direct_attack_hit=False, base_dice_total=0, suppressed=False):
        integer(resolved_damage,'resolved damage before temporary HP',0)
        integer(base_dice_total,'unmodified rolled base dice',0)
        result={'fireBonus':0,'healD6':False,'wisdomSave':False}
        if not self.active or suppressed or clock_marker(now)>=self.expires or resolved_damage==0:
            return result
        if actor==self.owner and direct_attack_hit and self.owner_rider_available:
            self.owner_rider_available=False
            result['fireBonus']=max(1,base_dice_total//2)
        elif actor!=self.owner and ally_of_owner and self.ally_rider_available:
            self.ally_rider_available=False
            result.update(healD6=True,wisdomSave=True)
        return result


@dataclass
class OneShotRider:
    trigger_kind: str
    available: bool = True

    def trigger(self, *, qualifying, attack_roll=False, hit=False, resolved_damage=0):
        integer(resolved_damage,'resolved damage before temporary HP',0)
        if self.trigger_kind not in ('attack','hit','damage'):
            raise SpellRuleError('Unregistered consumption trigger')
        met={'attack':attack_roll,'hit':hit,'damage':resolved_damage>0}[self.trigger_kind]
        if not self.available or not qualifying or not met:
            return False
        self.available=False
        return True


@dataclass
class PerTurnReflection:
    cleric_level: int
    used_turn_ids: set = field(default_factory=set)

    def reflect(self, *, target_turn_id, positive_damage_event, actual_damage_dealt, on_target_turn):
        """Caller supplies distinct actual turns, target-declared damage-event order."""
        integer(actual_damage_dealt,'temp absorption plus actual HP damage',0)
        if not isinstance(positive_damage_event,bool) or (actual_damage_dealt>0 and not positive_damage_event):
            raise SpellRuleError('Numeric damage requires a positive damage event')
        integer(self.cleric_level,'Cleric level',1,20)
        if not on_target_turn or not positive_damage_event or target_turn_id in self.used_turn_ids:
            return 0
        self.used_turn_ids.add(target_turn_id)
        return min(self.cleric_level,max(1,actual_damage_dealt//2))


def physical_escape_fallback(*, restrained, physical, explicit_escape,
                             fixed_endpoint, special_cure, source_dc=None, helper=False):
    if not restrained or not physical or explicit_escape or fixed_endpoint or special_cure:
        return None
    dc=10 if source_dc is None else integer(source_dc,'source DC',1)
    return {'activation':'Action','dc':dc,
            'checks':['STR(Athletics)'] if helper else ['STR(Athletics)','DEX(Acrobatics)'],
            'scope':'one selected restraint record'}


def disease_immunity_covers(*, classified_disease, magical, ordinary, scope):
    if scope not in ('all-disease','nonmagical-disease','ordinary-disease'):
        raise SpellRuleError('Unreviewed immunity scope')
    return classified_disease and (scope=='all-disease'
        or scope=='nonmagical-disease' and not magical
        or scope=='ordinary-disease' and ordinary)


def repeat_affliction_save(*, actual_record, source_allows_save, current_save_legal):
    return actual_record and source_allows_save and current_save_legal


def generic_curse_removable(*, classified_curse, intrinsic_class_state,
                            special_cure, ordinary_removable, curse_tier,
                            remover_tier=None):
    if not classified_curse or intrinsic_class_state or special_cure or not ordinary_removable:
        return False
    if remover_tier is None:
        return True
    integer(remover_tier,'remover tier',0)
    return curse_tier is not None and integer(curse_tier,'actual source tier',0)<=remover_tier


def curse_metadata_visible(*, detection_method, success, magical,
                          actual_curse_metadata, protected):
    if detection_method not in ('analyze-magic','arcane-sight','identify','detect-magic','aura-glimpse'):
        raise SpellRuleError('Unreviewed detection method')
    return (detection_method in ('analyze-magic','arcane-sight') and success
            and magical and actual_curse_metadata and not protected)


def regular_control_step(*, regular_turn, explicit_extra_turn_exception=False):
    """Only control repeat saves/expiry/pulses; not a universal proc rule."""
    return regular_turn or explicit_extra_turn_exception


def current_turn_endpoint(*, application_time, actual_turn_end=None):
    """Explicit 'that turn'/reviewed bare 'end turn', not a NEXT-turn rule."""
    application_time=absolute_deadline(application_time).seconds
    if actual_turn_end is None:
        return ClockMarker(application_time+6)
    actual_turn_end=absolute_deadline(actual_turn_end).seconds
    if actual_turn_end<application_time:
        raise SpellRuleError('Current turn cannot end before application')
    return ClockMarker(actual_turn_end,END_EFFECT_EXPIRY)


def balanced_elements_endpoint(existing, following_target_end, *, owner_matches,
                               elemental_control, source_maximum=None):
    """Following endpoint is caller-computed from NOW, never old endpoint+6."""
    require_deadline(existing)
    require_deadline(following_target_end)
    if following_target_end.phase!=END_EFFECT_EXPIRY:
        raise SpellRuleError('Following target END must use end-expiry phase')
    if not owner_matches or not elemental_control:
        return existing
    end=max([existing,following_target_end],key=clock_marker)
    if source_maximum is not None:
        require_deadline(source_maximum)
        if clock_marker(existing)>clock_marker(source_maximum):
            raise SpellRuleError('Existing record already exceeds governing source maximum')
        end=min([end,source_maximum],key=clock_marker)
    return end


def ash_bound_teleport_allowed(*, willing, source_requires_willing, otherwise_legal):
    return otherwise_legal and not willing and not source_requires_willing


def sanctify_staggered_records(records, *, target):
    """Cure all PRESENT classified records, including suppressed ones."""
    return [r['applicationId'] for r in records if r['targetId']==target
            and r.get('present',False) and 'classification.staggered' in r.get('tags',[])]


def delayed_round_order(canonical_order, delays):
    """Construct ONE round. Caller selects pending delays for that round only.

    Each record contains target, canonical snapshot, applicationSequence. The
    return value changes actual order only; virtual clocks are not inputs.
    """
    if len(canonical_order)!=len(set(canonical_order)):
        raise SpellRuleError('Canonical order requires distinct participants')
    order=list(canonical_order)
    delayed=set()
    for record in sorted(delays,key=lambda r:(r['applicationSequence'],r['target'])):
        integer(record['applicationSequence'],'stable application sequence',0)
        target=record['target']; snapshot=record['snapshot']
        if len(snapshot)!=len(set(snapshot)) or target not in snapshot:
            raise SpellRuleError('Delay snapshot must contain target exactly once')
        if target not in order or target in delayed:
            continue
        delayed.add(target)
        following=snapshot[snapshot.index(target)+1:]
        neighbor=next((person for person in following if person in order),None)
        if neighbor is not None:
            order.remove(target)
            order.insert(order.index(neighbor)+1,target)
    return order
