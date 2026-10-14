# Implemented disposition of exact control findings

All four material findings are fixed. Please inspect these exact updated helpers/tests and the changed binding excerpt, then explicitly give bounded closure if sound, or identify a remaining concrete defect. DD16/DD18, all-card execution, disease/curse catalogs, death/replacement/resurrection and other previously named broader work remain OPEN.

1. Guiding Star now exposes begin_ally_attack before rolling, consumes/returns the +2 and issues a unique mark-specific attack token. resolve_ally_attack resolves once after outcome; foreign/duplicate tokens reject. Suppression/illegal starts create no token/spend. Expiry/suppression before hit resolution grants no S; no refund to prior bonus. Tests include natural12+modifier1+pre-roll2 reachingAC15, miss then later hit, suppression and cross-mark replay.
2. Current-turn endpoint now returns ordered ClockMarker(seconds,phase): application/resolution10, expiry20, next event30; ordinary absolute timestamps usephase0. SpeedRecord operative/refresh and Balanced Elements extension understand phase ordering. A real SpeedRecord created at time3 during end-resolution is operative at(3,10), expiredat(3,20), gonebefore(3,30). No epsilon. Existing unrelated regular marker helpers remain unchanged. New tests exercise the actual lifecycle and Balanced Elements' connection to phased records.
3. All seven listed fallback components have conditional slowed-foe metadata. Spiral Opens has separate player-speed-zero component; forced-echo is not tagged. Binding validator asserts these memberships and exclusions.
4. Stars Revelation Mastery is HOOK. modifiers/reader references are separate fields; it authorizes a later enhanced Guiding Bolt component only when its option is selected. Actual Guiding Bolt lists that conditional component. Mage Arch Mastery explicitly modifies Coldflat/Glacier and all three already-reviewed Focus fire profiles (including Elemental Bolt). Flask BOOK wrapper references Burn/Root/Weaken, applies none itself. Enhanced Attunement and Balanced Elements have modifier links.

The two ordinary cold slows now have explicitly reviewed elemental tags. Fusion records the NEW missing Fire+Cold endpoint; Cascade's source clocks are explicit. The guide already correctly limits Carrion history to source-family/corpse, across owners. Corrected guide also preserves that Incapacitated by itself does NOT prohibit movement.

PASS123 interface cases +9,393 Speed states. PASS219 exact source objects; PASS219bindings/180component identities with modifier/reference link roles. Original source cards, books, spells untouched. Existing57custom/14hook/114source periodic registry unchanged except the reviewed JudgmentBrand3target-round endpoint clarification.

The next independent candidate inventory contains74classcards5engines and6dormant ordinary spell objects about healing/death. Those spells remain dormant, no operational promotion yet. After this bounded closure we will confer on death/zeroHP/HP-floor/recovery/resurrection/soul interfaces against those exact sources.

## Exact corrected files

### tools/control_playtest_rules.py

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


@dataclass(frozen=True, order=True)
class ClockMarker:
    seconds: int
    phase: int = 0

    def __post_init__(self):
        integer(self.seconds,'elapsed seconds',0)
        integer(self.phase,'ordered event phase',0)


END_EFFECT_APPLICATION=10
END_EFFECT_EXPIRY=20
NEXT_EVENT=30


def clock_marker(value):
    return value if isinstance(value,ClockMarker) else ClockMarker(value)


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
    expires: int | ClockMarker | None = None
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
            clock_marker(self.expires)
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
    expires: int
    s: int
    attack_bonus_available: bool = True
    hit_rider_available: bool = True
    active: bool = True
    _identity: str = field(default_factory=lambda:uuid4().hex,init=False,repr=False)
    _next_token: int = field(default=0,init=False,repr=False)
    _pending: set = field(default_factory=set,init=False,repr=False)

    def __post_init__(self):
        integer(self.s,'Oracle scaling S',1)
        clock_marker(self.expires)

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
    expires: int
    owner_rider_available: bool = True
    ally_rider_available: bool = True
    active: bool = True

    def trigger(self, *, actor, ally_of_owner, now, actual_damage,
                direct_attack_hit=False, base_dice_total=0, suppressed=False):
        integer(actual_damage,'actual damage',0)
        integer(base_dice_total,'unmodified rolled base dice',0)
        result={'fireBonus':0,'healD6':False,'wisdomSave':False}
        if not self.active or suppressed or now>=self.expires or actual_damage==0:
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
    integer(application_time,'application time',0)
    if actual_turn_end is None:
        return ClockMarker(application_time+6)
    integer(actual_turn_end,'current actual turn end',application_time)
    return ClockMarker(actual_turn_end,END_EFFECT_EXPIRY)


def balanced_elements_endpoint(existing, following_target_end, *, owner_matches,
                               elemental_control, source_maximum=None):
    """Following endpoint is caller-computed from NOW, never old endpoint+6."""
    clock_marker(existing)
    clock_marker(following_target_end)
    if not owner_matches or not elemental_control:
        return existing
    end=max([existing,following_target_end],key=clock_marker)
    if source_maximum is not None:
        clock_marker(source_maximum)
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

### tools/validate_control_playtests.py

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
    check('Refresh does not shorten its endpoint',refresh_speed_record(refreshed,replace(weaker,expires=9))[0].expires,18)
    held=refresh_speed_record([glacier],weaker)
    check('Distinct magnitude candidates remain independent',len(held),2)
    check('Later weaker profile cannot erase strong Glacier',f(held),10)
    check('Weaker profile resumes after Glacier expires',f(held,now=6),20)
    check('Cold profile owner identity prevents merged durations',len(refresh_speed_record([a],replace(weaker,owner='mage-B'))),2)
    check('Refresh does not end suppression',refresh_speed_record([replace(a,suppressed=True)],weaker)[0].suppressed,True)
    star=GuidingStarMark('oracle','enemy',18,3)
    check('Star owner cannot spend ally entitlement',star.begin_ally_attack(actor='oracle',ally_of_owner=True,now=1),{'attackBonus':0,'attackToken':None})
    attempt=star.begin_ally_attack(actor='ally',ally_of_owner=True,now=1)
    check('First ally receives+2 before rolling',attempt['attackBonus'],2)
    check('First ally miss spends+2 only',star.resolve_ally_attack(attempt['attackToken'],hit=False,now=1),{'radiantBonus':0})
    rejects('One attack token cannot resolve twice',lambda:star.resolve_ally_attack(attempt['attackToken'],hit=True,now=1))
    attempt2=star.begin_ally_attack(actor='ally2',ally_of_owner=True,now=2)
    check('Later ally begins with no second+2',attempt2['attackBonus'],0)
    check('Later ally hit spendsS and ends mark',star.resolve_ally_attack(attempt2['attackToken'],hit=True,now=2),{'radiantBonus':3})
    check('Consumed star supplies no third attack token',star.begin_ally_attack(actor='ally',ally_of_owner=True,now=3),{'attackBonus':0,'attackToken':None})
    fresh=GuidingStarMark('oracle','enemy',18,3)
    check('Suppressed star does not spend entitlement',fresh.begin_ally_attack(actor='ally',ally_of_owner=True,now=1,suppressed=True),{'attackBonus':0,'attackToken':None})
    check('Suppressed entitlement remains',fresh.attack_bonus_available,True)
    check('Illegal attack spends no star',fresh.begin_ally_attack(actor='ally',ally_of_owner=True,now=1,legal=False),{'attackBonus':0,'attackToken':None})
    check('Star expires at exact endpoint',fresh.begin_ally_attack(actor='ally',ally_of_owner=True,now=18),{'attackBonus':0,'attackToken':None})
    pre=fresh.begin_ally_attack(actor='ally',ally_of_owner=True,now=2)
    hit_result=12+1+pre['attackBonus']>=15
    check('Pre-roll bonus can make the qualifying roll hit',hit_result,True)
    check('Hit resolution then addsS',fresh.resolve_ally_attack(pre['attackToken'],hit=hit_result,now=2),{'radiantBonus':3})
    foreign=GuidingStarMark('oracle','enemy',18,3)
    foreign_token=foreign.begin_ally_attack(actor='ally',ally_of_owner=True,now=2)['attackToken']
    rejects('Attack token cannot transfer between marks',lambda:fresh.resolve_ally_attack(foreign_token,hit=True,now=2))
    check('Suppression before hit resolution prevents damage rider',foreign.resolve_ally_attack(foreign_token,hit=True,now=2,suppressed=True),{'radiantBonus':0})
    check('Suppressed resolution preserves unspent hit entitlement',foreign.hit_rider_available,True)
    brand=WrathfulBrand('oracle','enemy',18)
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
    check('Absolute expiry at3 is earlier than end-resolution phase',f([replace(end_slow,expires=3)],now=ClockMarker(3,END_EFFECT_APPLICATION)),30)
    check('Balanced Elements extends from now not old deadline',balanced_elements_endpoint(12,18,owner_matches=True,elemental_control=True),18)
    check('Repeated extension cannot add another turn recursively',balanced_elements_endpoint(18,18,owner_matches=True,elemental_control=True),18)
    check('Longer existing deadline is never shortened by extension',balanced_elements_endpoint(24,18,owner_matches=True,elemental_control=True),24)
    check('Balanced Elements cannot outlive governing concentration',balanced_elements_endpoint(12,24,owner_matches=True,elemental_control=True,source_maximum=18),18)
    check('Balanced Elements cannot modify another owner record',balanced_elements_endpoint(12,18,owner_matches=False,elemental_control=True),12)
    check('Balanced Elements can extend a phased current-turn elemental slow',balanced_elements_endpoint(ClockMarker(3,END_EFFECT_EXPIRY),9,owner_matches=True,elemental_control=True),9)
    check('Balanced Elements respects same-time governing source expiry phase',balanced_elements_endpoint(ClockMarker(3,END_EFFECT_EXPIRY),9,owner_matches=True,elemental_control=True,source_maximum=ClockMarker(3,END_EFFECT_EXPIRY)),ClockMarker(3,END_EFFECT_EXPIRY))
    check('Mundane Root has no inferred elemental metadata',balanced_elements_endpoint(12,18,owner_matches=True,elemental_control=False),12)
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
    rejects('Expired incoming record is not a legal refresh',lambda:refresh_speed_record([a],replace(weaker,expires=2),now=3))
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

### tools/validate_control_bindings.py

```python
"""Integrity/coverage of supplied bindings, not proof of full mechanical execution."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
GAME=ROOT.parents[1]


def main():
 data=json.loads((ROOT/'data/playtest/control_state_bindings.json').read_text(encoding='utf-8'))
 coverage=json.loads((ROOT/'data/playtest/control_state_coverage.json').read_text(encoding='utf-8'))
 packets=[json.loads((GAME/'docs/audit/2026-10-08/full-game'/name).read_text(encoding='utf-8')) for name in ('CONTROL_STATE_SOURCE_PACKET.json','CONTROL_STATE_SUPPLEMENT_SOURCE_PACKET.json')]
 expected={}
 for packet in packets:
  for r in packet['records']:
   kind=r['kind'];owner=r.get('owner','ordinary')
   ident=r['card']['id'] if kind=='class-card' else r['engineIndex'] if kind=='class-engine' else r['spellId']
   key=f'{kind}:{owner}:{ident}'
   if kind=='class-card': procedure={k:r['card'].get(k) for k in ('name','activation','cost','rangeAndTarget','duration','frequency','effect','prerequisite')}
   elif kind=='class-engine':procedure={'effect':r['text']}
   else:procedure=r['operational']
   expected[key]=(r,procedure)
 bindings={b['bindingId']:b for b in data['bindings']}
 assert len(bindings)==len(data['bindings'])==219
 assert set(bindings)==set(expected)=={r['candidateId'] for r in coverage['candidates']}
 components={c['mechanicalId']:c for c in data['componentIndex']}
 assert len(components)==len(data['componentIndex'])
 definitions=json.loads((ROOT/'data/playtest/condition_playtests.json').read_text(encoding='utf-8'))['conditions']
 core={'core.'+d['id'] for d in definitions}
 counts={}
 for ident,b in bindings.items():
  source,procedure=expected[ident]
  assert b['sourcePath']==source['path'],ident
  assert b['sourceSha256']==source.get('sourceObjectSha256',source.get('textSha256',source.get('operationalSha256'))),ident
  assert b['sourceProcedure']==procedure,ident
  assert b['classification'] in ('STATE','APPLY','HOOK','BOOK','NONSTATE','DEFER','ALREADY'),ident
  counts[b['classification']]=counts.get(b['classification'],0)+1
  if b['classification'] in ('STATE','APPLY'):assert b['componentIds'],ident
  for component in b['componentIds']:
   assert component in components,(ident,component)
   assert ident in components[component]['applicationBindings'],(ident,component)
   if component.startswith('core.'):assert component in core,component
  for field,reverse in (('modifiesComponents','modifierBindings'),('referencesComponents','referenceBindings')):
   for component in b[field]:
    assert component in components,(ident,field,component)
    assert ident in components[component][reverse]
  for evidence in b['reviewEvidence']:assert (GAME/evidence).is_file(),evidence
 for c in components.values():
  assert len(c['applicationBindings'])==len(set(c['applicationBindings'])),c['mechanicalId']
  for ident in c['applicationBindings']:assert c['mechanicalId'] in bindings[ident]['componentIds']
  for field,reverse in (('modifiesComponents','modifierBindings'),('referencesComponents','referenceBindings')):
   for ident in c[reverse]:assert c['mechanicalId'] in bindings[ident][field]
 assert (ROOT/data['operationalGuide']).is_file()
 for ident in ('core.staggered','monk.echoing-guard.stagger','warrior.brutal-strike.stagger'):
  assert 'classification.staggered' in components[ident]['metadata']
 assert 'classification.elemental-control' not in components['shaman.flask.root']['metadata']
 assert 'eligibility.slowed-foe' not in components['core.restrained']['metadata']
 assert 'eligibility.slowed-foe' not in components['core.grappled']['metadata']
 for ident in ('oracle.bone-whisper.soft-fallback','oracle.ledger-command.soft-fallback','oracle.marquis-glimpse.soft-fallback','oracle.slumber-glimpse.soft-fallback','oracle.moments-pause.soft-fallback','paladin.decree-of-submission.soft-fallback','paladin.echo-of-ages.soft-fallback','oracle.spiral-opens.player-speed-zero'):
  assert 'eligibility.slowed-foe' in components[ident]['metadata'],ident
 assert 'eligibility.slowed-foe' not in components['oracle.spiral-opens.forced-echo']['metadata']
 for ident in ('ordinary.ray-of-frost.slow','ordinary.frost-arrow.slow'):
  assert 'classification.elemental-control' in components[ident]['metadata']
 stars=bindings['class-card:oracle:oracle.supplement.stars.stars-revelation-mastery']
 assert stars['classification']=='HOOK' and not stars['componentIds']
 assert 'oracle.guiding-bolt.enhanced-slow' in stars['modifiesComponents']
 flask=bindings['class-card:shaman:shaman.base.flask-use']
 assert not flask['componentIds'] and set(flask['referencesComponents'])=={'shaman.flask.burn','shaman.flask.root','shaman.flask.weaken'}
 arch=bindings['class-card:mage:mage.arch.elemental-mastery']
 assert not arch['componentIds'] and 'mage.cold-focus.glacier' in arch['modifiesComponents']
 report={'status':'PASS','scope':'219 supplied binding/source/coverage identities and component links. No complete-card execution, exhaustive-source or balance claim.',
         'sourceBindings':len(bindings),'componentIdentities':len(components),'classifications':counts,
         'issues':[],'reviewStatus':data['status']}
 (ROOT/'docs/mechanics/CONTROL_BINDING_VALIDATION.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
 print(f"PASS {len(bindings)} source bindings; {len(components)} component identities; exact procedures preserved.")


if __name__=='__main__':main()

```

## Changed application/modifier/reference bindings and metadata

```json
[
  {
    "bindingId": "class-card:oracle:oracle.supplement.stars.guiding-bolt",
    "classification": "STATE",
    "componentIds": [
      "oracle.guiding-bolt.enhanced-slow",
      "oracle.guiding-bolt.star-mark"
    ],
    "modifiesComponents": [],
    "referencesComponents": [],
    "operationalOverrides": [
      "Two independent entitlements: next ally-other-than-owner attack+2 spends on roll; next qualifying ally hit addsS and ends mark, including after a prior miss. Paid reapplication resets both without stacking.",
      "Enhanced-slow component applies only if the relevant Stars Revelation Mastery enhancement is selected; no unmodified Guiding Bolt slow."
    ]
  },
  {
    "bindingId": "class-card:oracle:oracle.supplement.stars.stars-revelation-mastery",
    "classification": "HOOK",
    "componentIds": [],
    "modifiesComponents": [
      "oracle.constellation-mark",
      "oracle.guiding-bolt.enhanced-slow",
      "oracle.guiding-bolt.star-mark"
    ],
    "referencesComponents": [],
    "operationalOverrides": [
      "Passive mastery selection; only a later legal Guiding Bolt with the relevant enhancement selected applies the downstream slow. Other selected mastery upgrades retain exact source rules."
    ]
  },
  {
    "bindingId": "class-card:shaman:shaman.base.flask-use",
    "classification": "BOOK",
    "componentIds": [],
    "modifiesComponents": [],
    "referencesComponents": [
      "shaman.flask.burn",
      "shaman.flask.root",
      "shaman.flask.weaken"
    ],
    "operationalOverrides": [
      "BOOK wrapper references all three Base profiles. Actual application is source engine[4] selected mode, never duplicate wrapper+engine states."
    ]
  },
  {
    "bindingId": "class-card:shaman:shaman.arch.enhanced-elemental-attunement",
    "classification": "HOOK",
    "componentIds": [],
    "modifiesComponents": [
      "shaman.elemental-affinity.ice-slow"
    ],
    "referencesComponents": [],
    "operationalOverrides": []
  },
  {
    "bindingId": "ordinary-spell:ordinary:ray-of-frost",
    "classification": "STATE",
    "componentIds": [
      "ordinary.ray-of-frost.slow"
    ],
    "modifiesComponents": [],
    "referencesComponents": [],
    "operationalOverrides": []
  },
  {
    "bindingId": "ordinary-spell:ordinary:frost-arrow",
    "classification": "STATE",
    "componentIds": [
      "ordinary.frost-arrow.slow"
    ],
    "modifiesComponents": [],
    "referencesComponents": [],
    "operationalOverrides": []
  },
  {
    "bindingId": "class-card:mage:mage.arch.elemental-mastery",
    "classification": "HOOK",
    "componentIds": [],
    "modifiesComponents": [
      "mage.cold-focus.flat",
      "mage.cold-focus.glacier",
      "mage.elemental-bolt.burn",
      "mage.fire-focus.burn",
      "mage.inferno-lance.burn"
    ],
    "referencesComponents": [],
    "operationalOverrides": []
  },
  {
    "bindingId": "class-card:mage:mage.hero.elementalist.elemental-fusion",
    "classification": "STATE",
    "componentIds": [
      "mage.elemental-fusion.burn",
      "mage.elemental-fusion.opportunity-denial",
      "mage.elemental-fusion.reaction-denial",
      "mage.elemental-fusion.slow"
    ],
    "modifiesComponents": [],
    "referencesComponents": [],
    "operationalOverrides": [
      "NEW missing-endpoint bridge: Fire+Cold slow ends target next regular END; Cold+Lightning slow/opportunity denial same target-END; Fire+Lightning Reaction denial target next regular START. Non-Focus secondary profiles do not receive Arch Mastery."
    ]
  },
  {
    "bindingId": "class-card:mage:mage.hero.elementalist.cascade-storm",
    "classification": "STATE",
    "componentIds": [
      "mage.cascade-storm.burn",
      "mage.cascade-storm.cold-slow",
      "mage.cascade-storm.reaction-denial"
    ],
    "modifiesComponents": [],
    "referencesComponents": [],
    "operationalOverrides": [
      "Printed cold slow ends SOURCE next regular END; printed lightning Reaction denial SOURCE next regular START. Current-Cold passive may independently trigger on positive cold damage with its own target-END deadline."
    ]
  },
  {
    "bindingId": "class-card:mage:mage.hero.elementalist.elemental-mastery",
    "classification": "HOOK",
    "componentIds": [],
    "modifiesComponents": [],
    "referencesComponents": [],
    "operationalOverrides": []
  },
  {
    "bindingId": "class-card:oracle:oracle.supplement.time.the-spiral-opens",
    "classification": "STATE",
    "componentIds": [
      "oracle.spiral-opens.forced-echo",
      "oracle.spiral-opens.player-speed-zero"
    ],
    "modifiesComponents": [],
    "referencesComponents": [],
    "operationalOverrides": []
  },
  {
    "bindingId": "class-card:shaman:shaman.hero.soothsayer.balanced-elements",
    "classification": "HOOK",
    "componentIds": [],
    "modifiesComponents": [
      "dragoon.drakestorm-dive.cold-slow",
      "dragoon.elemental-lance.cold-slow",
      "mage.cascade-storm.cold-slow",
      "mage.cold-focus.flat",
      "mage.cold-focus.glacier",
      "mage.elemental-fusion.slow",
      "ordinary.frost-arrow.slow",
      "ordinary.ray-of-frost.slow",
      "shaman.elemental-affinity.ice-slow",
      "shaman.elemental-chorus.slow",
      "shaman.frost-totem.slow",
      "shaman.ice-wisp.speed-zero"
    ],
    "referencesComponents": [],
    "operationalOverrides": [
      "Owned explicitly classified elemental control may include legal multiclass sources. No Shaman-class-only restriction. Extend from NOW to target following regular end, max with existing endpoint, capped by governing source/concentration maximum; no recursive deadline addition. Actual elemental membership in guide/metadata."
    ]
  }
]
```

```json
[
  {
    "mechanicalId": "oracle.bone-whisper.soft-fallback",
    "applicationBindings": [
      "class-card:oracle:oracle.supplement.bones.bone-whisper"
    ],
    "applicationRule": "Only the exact source procedure and selected mode may apply this component. IDs do not imply unconditional or simultaneous application.",
    "metadata": [
      "eligibility.slowed-foe"
    ],
    "activeHookRule": "Only while the printed fallback Speed0/half-Speed component actually applies and is not suppressed/expired; Reaction denial or Charmed alone is insufficient.",
    "modifierBindings": [],
    "referenceBindings": []
  },
  {
    "mechanicalId": "oracle.marquis-glimpse.soft-fallback",
    "applicationBindings": [
      "class-card:oracle:oracle.supplement.shadow.marquis-s-glimpse"
    ],
    "applicationRule": "Only the exact source procedure and selected mode may apply this component. IDs do not imply unconditional or simultaneous application.",
    "metadata": [
      "eligibility.slowed-foe"
    ],
    "activeHookRule": "Only while the printed fallback Speed0/half-Speed component actually applies and is not suppressed/expired; Reaction denial or Charmed alone is insufficient.",
    "modifierBindings": [],
    "referenceBindings": []
  },
  {
    "mechanicalId": "ordinary.ray-of-frost.slow",
    "applicationBindings": [
      "ordinary-spell:ordinary:ray-of-frost"
    ],
    "applicationRule": "Only the exact source procedure and selected mode may apply this component. IDs do not imply unconditional or simultaneous application.",
    "metadata": [
      "eligibility.slowed-foe",
      "classification.elemental-control"
    ],
    "activeHookRule": "Only when this adverse Speed component actually applies and is not suppressed/expired. Numeric overshadowing does not deactivate it.",
    "metadataProvenance": "NEW exact-source semantic classification approved in GPT_CONTROL_EXACT_FINDINGS; not a global cold-spell inference.",
    "modifierBindings": [
      "class-card:shaman:shaman.hero.soothsayer.balanced-elements"
    ],
    "referenceBindings": []
  },
  {
    "mechanicalId": "ordinary.frost-arrow.slow",
    "applicationBindings": [
      "ordinary-spell:ordinary:frost-arrow"
    ],
    "applicationRule": "Only the exact source procedure and selected mode may apply this component. IDs do not imply unconditional or simultaneous application.",
    "metadata": [
      "eligibility.slowed-foe",
      "classification.elemental-control"
    ],
    "activeHookRule": "Only when this adverse Speed component actually applies and is not suppressed/expired. Numeric overshadowing does not deactivate it.",
    "metadataProvenance": "NEW exact-source semantic classification approved in GPT_CONTROL_EXACT_FINDINGS; not a global cold-spell inference.",
    "modifierBindings": [
      "class-card:shaman:shaman.hero.soothsayer.balanced-elements"
    ],
    "referenceBindings": []
  },
  {
    "mechanicalId": "oracle.ledger-command.soft-fallback",
    "applicationBindings": [
      "class-card:oracle:oracle.supplement.bones.ledger-s-command"
    ],
    "applicationRule": "Only the exact source procedure and selected mode may apply this component. IDs do not imply unconditional or simultaneous application.",
    "metadata": [
      "eligibility.slowed-foe"
    ],
    "activeHookRule": "Only while the printed fallback Speed0/half-Speed component actually applies and is not suppressed/expired; Reaction denial or Charmed alone is insufficient.",
    "modifierBindings": [],
    "referenceBindings": []
  },
  {
    "mechanicalId": "oracle.slumber-glimpse.soft-fallback",
    "applicationBindings": [
      "class-card:oracle:oracle.supplement.dream.slumber-glimpse"
    ],
    "applicationRule": "Only the exact source procedure and selected mode may apply this component. IDs do not imply unconditional or simultaneous application.",
    "metadata": [
      "eligibility.slowed-foe"
    ],
    "activeHookRule": "Only while the printed fallback Speed0/half-Speed component actually applies and is not suppressed/expired; Reaction denial or Charmed alone is insufficient.",
    "modifierBindings": [],
    "referenceBindings": []
  },
  {
    "mechanicalId": "oracle.moments-pause.soft-fallback",
    "applicationBindings": [
      "class-card:oracle:oracle.supplement.time.moment-s-pause"
    ],
    "applicationRule": "Only the exact source procedure and selected mode may apply this component. IDs do not imply unconditional or simultaneous application.",
    "metadata": [
      "eligibility.slowed-foe"
    ],
    "activeHookRule": "Only while the printed fallback Speed0/half-Speed component actually applies and is not suppressed/expired; Reaction denial or Charmed alone is insufficient.",
    "modifierBindings": [],
    "referenceBindings": []
  },
  {
    "mechanicalId": "oracle.spiral-opens.forced-echo",
    "applicationBindings": [
      "class-card:oracle:oracle.supplement.time.the-spiral-opens"
    ],
    "applicationRule": "Only the exact source procedure and selected mode may apply this component. IDs do not imply unconditional or simultaneous application.",
    "metadata": [],
    "modifierBindings": [],
    "referenceBindings": []
  },
  {
    "mechanicalId": "paladin.decree-of-submission.soft-fallback",
    "applicationBindings": [
      "class-card:paladin:paladin.supplement.oath-of-dominion.decree-of-submission"
    ],
    "applicationRule": "Only the exact source procedure and selected mode may apply this component. IDs do not imply unconditional or simultaneous application.",
    "metadata": [
      "eligibility.slowed-foe"
    ],
    "activeHookRule": "Only while the printed fallback Speed0/half-Speed component actually applies and is not suppressed/expired; Reaction denial or Charmed alone is insufficient.",
    "modifierBindings": [],
    "referenceBindings": []
  },
  {
    "mechanicalId": "paladin.echo-of-ages.soft-fallback",
    "applicationBindings": [
      "class-card:paladin:paladin.supplement.oath-of-the-ancients.echo-of-ages"
    ],
    "applicationRule": "Only the exact source procedure and selected mode may apply this component. IDs do not imply unconditional or simultaneous application.",
    "metadata": [
      "eligibility.slowed-foe"
    ],
    "activeHookRule": "Only while the printed fallback Speed0/half-Speed component actually applies and is not suppressed/expired; Reaction denial or Charmed alone is insufficient.",
    "modifierBindings": [],
    "referenceBindings": []
  },
  {
    "mechanicalId": "oracle.spiral-opens.player-speed-zero",
    "applicationBindings": [
      "class-card:oracle:oracle.supplement.time.the-spiral-opens"
    ],
    "modifierBindings": [],
    "metadata": [
      "eligibility.slowed-foe"
    ],
    "applicationRule": "Only the actual selected player Speed0 branch. Not NPC Forced Echo or a player choosing to repeat the action type.",
    "activeHookRule": "Actual Speed0 branch active and unsuppressed only.",
    "referenceBindings": []
  }
]
```
