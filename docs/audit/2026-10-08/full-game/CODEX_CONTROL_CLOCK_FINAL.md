# Final control clock correction — exact implementation

Your remaining future-end phase finding is corrected. Please give explicit bounded REVIEWED / reference-VALIDATED closure if sound; identify only concrete remaining defects within the supplied control interface scope. DD16/DD18 and the full game remain OPEN.

All reference consumers now require typed ClockMarker deadlines. SpeedRecord, GuidingStarMark, WrathfulBrand reject ambiguous numeric expiries. regular_control_endpoint adapts the unchanged reviewed combat marker_deadline helper to phase20 for ALL future turn ends (source, target, Nth), phase0 for starts. current_turn_endpoint uses phase20 for actual current ends. absolute_deadline usesphase0. Balanced Elements requires its following target end atphase20; governing source maximum retains its actual start/end/absolute phase.

Combat marker_deadline returns exact Fraction seconds. ClockMarker now preserves exact Fraction values (including fractional virtual markers) instead of truncating or rejecting them; finite nonnegative numeric times only, bool/NaN/infinity rejected. It orders by seconds thenphase. This adds event order, not an epsilon offset.

PASS148 control checks and9,393 Speed invariants. New lifecycle tests prove futuretarget/sourceend at(9,10) remains active, at(9,20) expires, at(9,30) absent; hostile2rounds gets(15,20); stronger expires after finalend effects thenweaker resumes; GuidingStar worksduringendphase10; fractional9.5markerspreserved. Old arithmetic tests explicitly use absolute_deadline rather than pretending to model turn ends.

219 exact sources/219bindings/180component identities and previously accepted fourfixes unchanged. Selected helpers are not a full card engine. The next source conference will address healing/death/zeroHP/resurrection.

## tools/control_playtest_rules.py

```python
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

    def trigger(self, *, actor, ally_of_owner, now, actual_damage,
                direct_attack_hit=False, base_dice_total=0, suppressed=False):
        integer(actual_damage,'actual damage',0)
        integer(base_dice_total,'unmodified rolled base dice',0)
        result={'fireBonus':0,'healD6':False,'wisdomSave':False}
        if not self.active or suppressed or clock_marker(now)>=self.expires or actual_damage==0:
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

    def trigger(self, *, qualifying, attack_roll=False, hit=False, actual_damage=0):
        integer(actual_damage,'actual damage',0)
        if self.trigger_kind not in ('attack','hit','damage'):
            raise SpellRuleError('Unregistered consumption trigger')
        met={'attack':attack_roll,'hit':hit,'damage':actual_damage>0}[self.trigger_kind]
        if not self.available or not qualifying or not met:
            return False
        self.available=False
        return True


@dataclass
class PerTurnReflection:
    cleric_level: int
    used_turn_ids: set = field(default_factory=set)

    def reflect(self, *, target_turn_id, actual_damage, on_target_turn):
        """Caller supplies distinct actual turns, target-declared damage-event order."""
        integer(actual_damage,'actual damage to another creature',0)
        integer(self.cleric_level,'Cleric level',1,20)
        if not on_target_turn or actual_damage==0 or target_turn_id in self.used_turn_ids:
            return 0
        self.used_turn_ids.add(target_turn_id)
        return min(self.cleric_level,max(1,actual_damage//2))


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

```

## tools/validate_control_playtests.py

```python
"""Table examples and lifecycle boundaries for the bounded control interfaces."""
from pathlib import Path
from fractions import Fraction
from dataclasses import replace
import json
from control_playtest_rules import *

ROOT=Path(__file__).resolve().parents[1]


def main():
    checks=[]
    def check(name,actual,expected):
        assert actual==expected,(name,actual,expected)
        checks.append(name)
    def rejects(name,fn):
        try: fn()
        except SpellRuleError: checks.append(name)
        else: raise AssertionError(name)
    def slow(ident,mode='flat',amount=10,**kw):
        # Earlier arithmetic/lifecycle examples use explicit elapsed deadlines.
        if isinstance(kw.get('expires'),int):kw['expires']=absolute_deadline(kw['expires'])
        return SpeedRecord(ident,kw.pop('owner','mage-A'),'hero',kw.pop('group','cold-focus'),
                           kw.pop('profile',ident),mode,amount=amount,**kw)
    a=slow('cold',expires=12)
    b=slow('ray',owner='mage-B',group='ray-of-frost',expires=18)
    half=slow('crippling',mode='half',amount=0,expires=6)
    zero=slow('root',mode='zero',amount=0,expires=3)
    f=lambda rs,**kw:effective_control_speed(30,rs,target='hero',**kw)
    check('Two unrelated -10 effects retain records but produce Speed20',f([a,b]),20)
    check('Half beats -10 on Speed30 without adding both',f([a,half]),15)
    check('Exhaustion halves the arbitrated value once',f([a,half],global_multiplier=Fraction(1,2)),7)
    check('Independent Strain penalties occur before hostile arbitration',effective_control_speed(15,[a,half],target='hero'),5)
    check('Root sets zero without deleting other effects',f([a,zero]),0)
    check('Root expiry exposes still-active slow',f([a,zero],now=3),20)
    check('Stronger expiry exposes weaker candidate',f([a,half],now=6),20)
    check('All effects expire at exact boundary',f([a,b],now=18),30)
    check('Suppression does not participate in Speed arbitration',f([replace(a,suppressed=True)]),30)
    check('Suppression ending before expiry allows return',f([replace(a,suppressed=False)],now=4),20)
    check('Core Grappled remains Speed0 independently',f([a],core_speed_zero=True),0)
    check('Overshadowed adverse record still satisfies slowed-foe',slowed_foe([a,half],target='hero'),True)
    check('Suppressed slow does not satisfy hook',slowed_foe([replace(a,suppressed=True)],target='hero'),False)
    check('Expired slow does not satisfy hook',slowed_foe([a],target='hero',now=12),False)
    check('Core restriction alone carries no slowed hook',slowed_foe([],target='hero'),False)
    check('Other target never satisfies hook',slowed_foe([a],target='other'),False)
    rejects('Reject mixed-target Speed computation',lambda:f([replace(a,target='other')]))
    rejects('Reject duplicated application IDs',lambda:f([a,a]))
    rejects('Reject unreviewed transform',lambda:slow('x',mode='multiply'))
    rejects('Reject float multiplier',lambda:f([a],global_multiplier=0.5))
    leash=slow('iron-leash',floor=5)
    check('Iron Leash minimum never increases an existing Speed3',effective_control_speed(3,[leash],target='hero'),3)
    check('Iron Leash on Speed12 floors its reduction at5',effective_control_speed(12,[leash],target='hero'),5)
    check('Iron Leash floor never overrides Root',effective_control_speed(12,[leash,zero],target='hero'),0)
    master=slow('mastered-passive',amount=15,expires=12)
    glacier=slow('glacier',mode='half-minus',amount=5,expires=6)
    check('Mastered Glacier at30 is10, not5',f([master,glacier]),10)
    check('Ordinary passive beats unmastered Glacier atSpeed5',effective_control_speed(5,[a,half],target='hero'),0)
    check('Mastered passive and Glacier at10 do not go negative',effective_control_speed(10,[master,glacier],target='hero'),0)
    weaker=slow('later-passive',expires=18,profile='cold')
    refreshed=refresh_speed_record([a],weaker)
    check('One exact Focus profile refresh, not duplicate',len(refreshed),1)
    check('Refresh does not shorten its endpoint',refresh_speed_record(refreshed,replace(weaker,expires=absolute_deadline(9)))[0].expires,absolute_deadline(18))
    held=refresh_speed_record([glacier],weaker)
    check('Distinct magnitude candidates remain independent',len(held),2)
    check('Later weaker profile cannot erase strong Glacier',f(held),10)
    check('Weaker profile resumes after Glacier expires',f(held,now=6),20)
    check('Cold profile owner identity prevents merged durations',len(refresh_speed_record([a],replace(weaker,owner='mage-B'))),2)
    check('Refresh does not end suppression',refresh_speed_record([replace(a,suppressed=True)],weaker)[0].suppressed,True)
    star=GuidingStarMark('oracle','enemy',absolute_deadline(18),3)
    check('Star owner cannot spend ally entitlement',star.begin_ally_attack(actor='oracle',ally_of_owner=True,now=1),{'attackBonus':0,'attackToken':None})
    attempt=star.begin_ally_attack(actor='ally',ally_of_owner=True,now=1)
    check('First ally receives+2 before rolling',attempt['attackBonus'],2)
    check('First ally miss spends+2 only',star.resolve_ally_attack(attempt['attackToken'],hit=False,now=1),{'radiantBonus':0})
    rejects('One attack token cannot resolve twice',lambda:star.resolve_ally_attack(attempt['attackToken'],hit=True,now=1))
    attempt2=star.begin_ally_attack(actor='ally2',ally_of_owner=True,now=2)
    check('Later ally begins with no second+2',attempt2['attackBonus'],0)
    check('Later ally hit spendsS and ends mark',star.resolve_ally_attack(attempt2['attackToken'],hit=True,now=2),{'radiantBonus':3})
    check('Consumed star supplies no third attack token',star.begin_ally_attack(actor='ally',ally_of_owner=True,now=3),{'attackBonus':0,'attackToken':None})
    fresh=GuidingStarMark('oracle','enemy',absolute_deadline(18),3)
    check('Suppressed star does not spend entitlement',fresh.begin_ally_attack(actor='ally',ally_of_owner=True,now=1,suppressed=True),{'attackBonus':0,'attackToken':None})
    check('Suppressed entitlement remains',fresh.attack_bonus_available,True)
    check('Illegal attack spends no star',fresh.begin_ally_attack(actor='ally',ally_of_owner=True,now=1,legal=False),{'attackBonus':0,'attackToken':None})
    check('Star expires at exact endpoint',fresh.begin_ally_attack(actor='ally',ally_of_owner=True,now=18),{'attackBonus':0,'attackToken':None})
    pre=fresh.begin_ally_attack(actor='ally',ally_of_owner=True,now=2)
    hit_result=12+1+pre['attackBonus']>=15
    check('Pre-roll bonus can make the qualifying roll hit',hit_result,True)
    check('Hit resolution then addsS',fresh.resolve_ally_attack(pre['attackToken'],hit=hit_result,now=2),{'radiantBonus':3})
    foreign=GuidingStarMark('oracle','enemy',absolute_deadline(18),3)
    foreign_token=foreign.begin_ally_attack(actor='ally',ally_of_owner=True,now=2)['attackToken']
    rejects('Attack token cannot transfer between marks',lambda:fresh.resolve_ally_attack(foreign_token,hit=True,now=2))
    check('Suppression before hit resolution prevents damage rider',foreign.resolve_ally_attack(foreign_token,hit=True,now=2,suppressed=True),{'radiantBonus':0})
    check('Suppressed resolution preserves unspent hit entitlement',foreign.hit_rider_available,True)
    brand=WrathfulBrand('oracle','enemy',absolute_deadline(18))
    check('Fully prevented owner hit does not trigger damaging-hit rider',brand.trigger(actor='oracle',ally_of_owner=True,now=1,actual_damage=0,direct_attack_hit=True,base_dice_total=9)['fireBonus'],0)
    check('Brand damage uses unmodified rolled base dice',brand.trigger(actor='oracle',ally_of_owner=True,now=2,actual_damage=12,direct_attack_hit=True,base_dice_total=9)['fireBonus'],4)
    check('Brand owner bonus cannot recur',brand.trigger(actor='oracle',ally_of_owner=True,now=3,actual_damage=12,direct_attack_hit=True,base_dice_total=9)['fireBonus'],0)
    check('First ally damage receives distinct heal/save entitlement',brand.trigger(actor='ally',ally_of_owner=True,now=4,actual_damage=1),{'fireBonus':0,'healD6':True,'wisdomSave':True})
    check('Blocked healing does not refund spent Brand entitlement',brand.trigger(actor='ally',ally_of_owner=True,now=5,actual_damage=1),{'fireBonus':0,'healD6':False,'wisdomSave':False})
    check('Consumed Brand riders do not end timed Brand itself',brand.active,True)
    hit=OneShotRider('hit')
    check('Drake/Soldier hit-based rider is not spent on miss',hit.trigger(qualifying=True,attack_roll=True),False)
    check('Hit-based rider spends even if actual damage0',hit.trigger(qualifying=True,attack_roll=True,hit=True,actual_damage=0),True)
    scan=OneShotRider('attack')
    check('Scanner spent by attack roll even miss',scan.trigger(qualifying=True,attack_roll=True,hit=False),True)
    reflect=PerTurnReflection(12)
    check('No Divine Judgment on off-turn damage',reflect.reflect(target_turn_id='one',actual_damage=20,on_target_turn=False),0)
    check('Zero damage does not consume reflection',reflect.reflect(target_turn_id='one',actual_damage=0,on_target_turn=True),0)
    check('First damage on turn reflects half',reflect.reflect(target_turn_id='one',actual_damage=9,on_target_turn=True),4)
    check('Second victim on same turn does not reflect again',reflect.reflect(target_turn_id='one',actual_damage=8,on_target_turn=True),0)
    check('Separate extra turn can reflect once',reflect.reflect(target_turn_id='extra',actual_damage=40,on_target_turn=True),12)
    check('Small actual damage still minimum1',reflect.reflect(target_turn_id='two',actual_damage=1,on_target_turn=True),1)
    base=dict(restrained=True,physical=True,explicit_escape=False,fixed_endpoint=False,special_cure=False)
    check('Physical fallback missingDC uses10',physical_escape_fallback(**base)['dc'],10)
    check('Physical fallback selects one record',physical_escape_fallback(**base)['scope'],'one selected restraint record')
    check('Helper fallback uses Athletics only',physical_escape_fallback(**base,helper=True)['checks'],['STR(Athletics)'])
    check('Fixed-duration source receives no invented escape',physical_escape_fallback(**{**base,'fixed_endpoint':True}),None)
    check('Magical restraint receives no physical fallback',physical_escape_fallback(**{**base,'physical':False}),None)
    check('Root receives no Restrained fallback',physical_escape_fallback(**{**base,'restrained':False}),None)
    check('Special cure protection controls fallback',physical_escape_fallback(**{**base,'special_cure':True}),None)
    check('Explicit source escape controls fallback',physical_escape_fallback(**{**base,'explicit_escape':True}),None)
    check('Nonmagical disease immunity excludes magical disease',disease_immunity_covers(classified_disease=True,magical=True,ordinary=True,scope='nonmagical-disease'),False)
    check('Ordinary disease immunity includes ordinary magical disease',disease_immunity_covers(classified_disease=True,magical=True,ordinary=True,scope='ordinary-disease'),True)
    check('Name alone supplies no disease immunity hook',disease_immunity_covers(classified_disease=False,magical=False,ordinary=True,scope='all-disease'),False)
    check('Repeat-save cure invents no saving throw',repeat_affliction_save(actual_record=True,source_allows_save=False,current_save_legal=True),False)
    check('Repeat save needs currently legal source save',repeat_affliction_save(actual_record=True,source_allows_save=True,current_save_legal=False),False)
    curse=dict(classified_curse=True,intrinsic_class_state=False,special_cure=False,ordinary_removable=True,curse_tier=2,remover_tier=3)
    check('Ordinary within-tier curse removable',generic_curse_removable(**curse),True)
    check('Unknown curse tier is not silently assigned',generic_curse_removable(**{**curse,'curse_tier':None}),False)
    check('Oracle intrinsic Curse not ordinary cleanse target',generic_curse_removable(**{**curse,'intrinsic_class_state':True}),False)
    check('Special curse cure cannot be bypassed',generic_curse_removable(**{**curse,'special_cure':True}),False)
    detect=dict(success=True,magical=True,actual_curse_metadata=True,protected=False)
    check('Analyze exposes permitted actual curse metadata',curse_metadata_visible(detection_method='analyze-magic',**detect),True)
    check('Identify does not automatically reveal curse',curse_metadata_visible(detection_method='identify',**detect),False)
    check('Detect Magic has no curse-detail grant',curse_metadata_visible(detection_method='detect-magic',**detect),False)
    check('Protected class Curse stays protected',curse_metadata_visible(detection_method='arcane-sight',**{**detect,'protected':True}),False)
    check('Extra turn does not manufacture repeat save',regular_control_step(regular_turn=False),False)
    check('Regular turn advances control clock',regular_control_step(regular_turn=True),True)
    check('Hypermutation protects captured walking baseline after Exhaustion',effective_control_speed(15,[a],target='hero',global_multiplier=Fraction(1,2),hypermutation_baseline=30),15)
    check('Hypermutation never defeats explicit root',f([zero],hypermutation_baseline=30),0)
    check('Hypermutation never defeats Core immobilization',f([],hypermutation_baseline=30,core_speed_zero=True),0)
    check('Hypermutation grants no absent mode',f([],hypermutation_baseline=60,mode_possessed=False),0)
    check('Captured swim floor differs from walking',effective_control_speed(5,[a],target='hero',hypermutation_baseline=20),10)
    check('New mode without snapshot gains no floor',effective_control_speed(5,[a],target='hero'),0)
    check('Zero from numeric slow differs from explicit Speed0',effective_control_speed(5,[a],target='hero',hypermutation_baseline=30),15)
    check('Current-turn off-turn entry uses actual turn end',current_turn_endpoint(application_time=2,actual_turn_end=3),ClockMarker(3,END_EFFECT_EXPIRY))
    check('End-trigger slow expires after resolution at same end',current_turn_endpoint(application_time=3,actual_turn_end=3),ClockMarker(3,END_EFFECT_EXPIRY))
    check('No current turn uses six elapsed seconds',current_turn_endpoint(application_time=7),ClockMarker(13))
    end_slow=slow('end-trigger',expires=current_turn_endpoint(application_time=3,actual_turn_end=3))
    check('End-trigger slow exists during application resolution',f([end_slow],now=ClockMarker(3,END_EFFECT_APPLICATION)),20)
    check('End-trigger slow expires at later phase same timestamp',f([end_slow],now=ClockMarker(3,END_EFFECT_EXPIRY)),30)
    check('End-trigger slow is absent before next event phase',f([end_slow],now=ClockMarker(3,NEXT_EVENT)),30)
    check('Same-time later-phase expiry permits legitimate new application',len(refresh_speed_record([],end_slow,now=ClockMarker(3,END_EFFECT_APPLICATION))),1)
    rejects('Passed same-timestamp phase cannot be refreshed',lambda:refresh_speed_record([],end_slow,now=ClockMarker(3,NEXT_EVENT)))
    check('Absolute expiry at3 is earlier than end-resolution phase',f([replace(end_slow,expires=absolute_deadline(3))],now=ClockMarker(3,END_EFFECT_APPLICATION)),30)
    check('Balanced Elements extends from now not old deadline',balanced_elements_endpoint(turn_end_deadline(12),turn_end_deadline(18),owner_matches=True,elemental_control=True),turn_end_deadline(18))
    check('Repeated extension cannot add another turn recursively',balanced_elements_endpoint(turn_end_deadline(18),turn_end_deadline(18),owner_matches=True,elemental_control=True),turn_end_deadline(18))
    check('Longer existing deadline is never shortened by extension',balanced_elements_endpoint(turn_end_deadline(24),turn_end_deadline(18),owner_matches=True,elemental_control=True),turn_end_deadline(24))
    check('Balanced Elements cannot outlive governing concentration',balanced_elements_endpoint(turn_end_deadline(12),turn_end_deadline(24),owner_matches=True,elemental_control=True,source_maximum=turn_end_deadline(18)),turn_end_deadline(18))
    check('Balanced Elements cannot modify another owner record',balanced_elements_endpoint(turn_end_deadline(12),turn_end_deadline(18),owner_matches=False,elemental_control=True),turn_end_deadline(12))
    check('Balanced Elements can extend a phased current-turn elemental slow',balanced_elements_endpoint(turn_end_deadline(3),turn_end_deadline(9),owner_matches=True,elemental_control=True),turn_end_deadline(9))
    check('Balanced Elements respects same-time governing source expiry phase',balanced_elements_endpoint(turn_end_deadline(3),turn_end_deadline(9),owner_matches=True,elemental_control=True,source_maximum=turn_end_deadline(3)),turn_end_deadline(3))
    check('Mundane Root has no inferred elemental metadata',balanced_elements_endpoint(turn_end_deadline(12),turn_end_deadline(18),owner_matches=True,elemental_control=False),turn_end_deadline(12))
    check('Ash-bound forbids consenting to allied transport',ash_bound_teleport_allowed(willing=True,source_requires_willing=True,otherwise_legal=True),False)
    check('Ash-bound allows independently legal involuntary hostile displacement',ash_bound_teleport_allowed(willing=False,source_requires_willing=False,otherwise_legal=True),True)
    check('Ash-bound does not make illegal teleport legal',ash_bound_teleport_allowed(willing=False,source_requires_willing=False,otherwise_legal=False),False)
    records=[{'applicationId':'core','targetId':'hero','present':True,'tags':['classification.staggered']},
      {'applicationId':'monk','targetId':'hero','present':True,'suppressed':True,'tags':['classification.staggered']},
      {'applicationId':'plain-slow','targetId':'hero','present':True,'tags':['eligibility.slowed-foe']},
      {'applicationId':'other','targetId':'other','present':True,'tags':['classification.staggered']}]
    check('Sanctify removes suppressed Staggered but not unrelated slow',sanctify_staggered_records(records,target='hero'),['core','monk'])
    delay=lambda target,seq,snapshot=['a','b','c','d']:{'target':target,'applicationSequence':seq,'snapshot':snapshot}
    check('One initiative delay moves after next snapshot participant',delayed_round_order(['a','b','c','d'],[delay('b',1)]),['a','c','b','d'])
    check('Repeated delays on same target do not stack',delayed_round_order(['a','b','c','d'],[delay('b',1),delay('b',2)]),['a','c','b','d'])
    check('Removed neighbor skips to next surviving snapshot member',delayed_round_order(['a','b','d'],[delay('b',1)]),['a','d','b'])
    check('New entrant cannot become snapshot neighbor',delayed_round_order(['a','b','new','c','d'],[delay('b',1)]),['a','new','c','b','d'])
    check('Last participant delay leaves order unchanged',delayed_round_order(['a','b','c','d'],[delay('d',1)]),['a','b','c','d'])
    check('Chained delays use application sequence',delayed_round_order(['a','b','c','d'],[delay('b',2),delay('a',1)]),['a','c','b','d'])
    check('No pending delays restores canonical round',delayed_round_order(['a','b','c','d'],[]),['a','b','c','d'])
    rejects('Expired incoming record is not a legal refresh',lambda:refresh_speed_record([a],replace(weaker,expires=absolute_deadline(2)),now=3))
    target_end=regular_control_endpoint(1,3,excluded_current_marker=3)
    check('Next target end constructor preserves skipped current turn and expiry phase',target_end,ClockMarker(9,END_EFFECT_EXPIRY))
    target_slow=slow('target-end',expires=target_end)
    check('Future target-end slow remains during end resolution',f([target_slow],now=ClockMarker(9,END_EFFECT_APPLICATION)),20)
    check('Future target-end slow expires after resolution',f([target_slow],now=ClockMarker(9,END_EFFECT_EXPIRY)),30)
    check('Future target-end slow absent at next event phase',f([target_slow],now=ClockMarker(9,NEXT_EVENT)),30)
    source_end=regular_control_endpoint(4,3)
    source_slow=slow('source-end',expires=source_end)
    check('Source next-end is also phase20',source_end,turn_end_deadline(9))
    check('Source next-end remains through end resolution',f([source_slow],now=ClockMarker(9,END_EFFECT_APPLICATION)),20)
    second_end=regular_control_endpoint(1,3,count=2,excluded_current_marker=3)
    check('Bare hostile2rounds preserves future target-end phase',second_end,turn_end_deadline(15))
    check('Start boundary remains before start effects',regular_control_endpoint(4,3,boundary='start'),absolute_deadline(9))
    strong_end=slow('strong-future-end',amount=15,expires=target_end)
    weak_end=slow('weak-future-end',amount=5,expires=turn_end_deadline(15))
    check('Stronger source remains effective during final end effects',f([strong_end,weak_end],now=ClockMarker(9,END_EFFECT_APPLICATION)),15)
    check('Weaker source resumes at stronger end-expiry phase',f([strong_end,weak_end],now=ClockMarker(9,END_EFFECT_EXPIRY)),25)
    rejects('SpeedRecord rejects ambiguous untyped expiry',lambda:SpeedRecord('raw','owner','hero','group','profile','flat',amount=10,expires=9))
    rejects('GuidingStar rejects ambiguous untyped expiry',lambda:GuidingStarMark('oracle','enemy',9,3))
    rejects('WrathfulBrand rejects ambiguous untyped expiry',lambda:WrathfulBrand('oracle','enemy',9))
    rejects('Balanced Elements rejects wrong phase for following turn end',lambda:balanced_elements_endpoint(turn_end_deadline(3),absolute_deadline(9),owner_matches=True,elemental_control=True))
    star_end=GuidingStarMark('oracle','enemy',target_end,3)
    beginning=star_end.begin_ally_attack(actor='ally',ally_of_owner=True,now=ClockMarker(9,END_EFFECT_APPLICATION))
    check('GuidingStar at future end trigger grants pre-roll bonus before expiry',beginning['attackBonus'],2)
    check('GuidingStar same end-resolution hit can consume mark',star_end.resolve_ally_attack(beginning['attackToken'],hit=True,now=ClockMarker(9,END_EFFECT_APPLICATION)),{'radiantBonus':3})
    fractional_end=regular_control_endpoint(Fraction(1,2),Fraction(7,2),excluded_current_marker=Fraction(7,2))
    check('Fractional virtual marker remains exact',fractional_end,ClockMarker(Fraction(19,2),END_EFFECT_EXPIRY))
    check('Fractional current turn boundary remains exact',current_turn_endpoint(application_time=Fraction(1,2),actual_turn_end=Fraction(7,2)),turn_end_deadline(Fraction(7,2)))
    check('Fractional end is active before expiry phase',f([slow('fractional',expires=fractional_end)],now=ClockMarker(Fraction(19,2),END_EFFECT_APPLICATION)),20)
    check('Fractional end expires without rounding',f([slow('fractional',expires=fractional_end)],now=ClockMarker(Fraction(19,2),END_EFFECT_EXPIRY)),30)
    rejects('Clock rejects boolean seconds',lambda:ClockMarker(True))
    rejects('Clock rejects infinite seconds',lambda:ClockMarker(float('inf')))
    rejects('Clock rejects NaN seconds',lambda:ClockMarker(float('nan')))
    rejects('Clock rejects negative seconds',lambda:ClockMarker(Fraction(-1,2)))
    rejects('Current turn cannot end before application',lambda:current_turn_endpoint(application_time=2,actual_turn_end=1))
    invariant_states=0
    for speed in range(101):
        for reduction in range(31):
            rec=slow('invariant',amount=reduction)
            for mode in ('flat','half','half-minus'):
                other=slow('other',mode=mode,amount=0 if mode=='half' else 5)
                result=effective_control_speed(speed,[rec,other],target='hero')
                assert 0<=result<=speed
                assert result==min(rec.result(speed),other.result(speed))
                assert effective_control_speed(speed,[rec,other],target='hero',global_multiplier=Fraction(1,2))==result//2
                invariant_states+=1
    report={'status':'PASS','reviewStatus':'IN_REVIEW; selected helpers only',
        'scope':'Selected control lifecycle/arbitration interfaces, not full source/card execution or game-wide completion.',
        'checks':checks,'checkCount':len(checks),'speedInvariantStates':invariant_states}
    (ROOT/'docs/mechanics/CONTROL_PLAYTEST_VALIDATION.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(f"PASS {len(checks)} control checks; {invariant_states} Speed invariant states. Review pending.")


if __name__=='__main__': main()

```
