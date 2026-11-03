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


def marker_deadline(application_time, marker_phase, count=1, *, excluded_current_marker=None):
    """Preserve original virtual marker phase, recurring every six seconds.

    Times are rational abstract encounter seconds; start/end ordering is supplied
    by the scheduler. Exclude the specific in-progress turn's end, not an arbitrary
    next future marker. Initiative changes never rewrite the returned deadline.
    """
    integer(count, 'marker count', 1)
    now, phase = Fraction(application_time), Fraction(marker_phase)
    cycle = (now - phase) // 6 + 1
    first = phase + cycle * 6
    if excluded_current_marker is not None and first == Fraction(excluded_current_marker):
        first += 6
    return first + (count - 1) * 6


def absolute_duration(application_time, rounds):
    integer(rounds, 'duration rounds', 1)
    return Fraction(application_time) + rounds * 6


def ready_effect_deadline(prepared_at, released_at, rounds, *, marker_phase=None,
                          excluded_current_marker=None):
    """Caller checks unexpired legal Ready release; this only anchors its effect."""
    if Fraction(released_at) < Fraction(prepared_at):
        raise SpellRuleError('Ready cannot release before preparation')
    if marker_phase is None:
        return absolute_duration(released_at, rounds)
    return marker_deadline(released_at, marker_phase, rounds,
                           excluded_current_marker=excluded_current_marker)


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
    """Boolean Hidden state only; does not retain each observer's task degree."""
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
class ManeuverAttempts:
    used: set = field(default_factory=set)
    last_regular_start: int = -1

    def regular_start(self, marker):
        integer(marker, 'regular start ordinal', 0)
        if marker <= self.last_regular_start:
            raise SpellRuleError('Regular marker cannot refresh twice')
        self.last_regular_start = marker
        self.used.clear()

    def declare_and_roll(self, maneuver, *, legal_attack=True, other_optional_maneuver=False):
        if maneuver not in ('pin', 'silence-the-caster'):
            raise SpellRuleError('Unsupported ordinary maneuver budget')
        if not legal_attack or other_optional_maneuver or maneuver in self.used:
            raise SpellRuleError('Illegal maneuver declaration')
        self.used.add(maneuver)
        return -2

    def extra_turn(self):
        pass

    def round_boundary(self):
        pass


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
    This helper does not perform family arbitration, cure processing, trigger
    generation, duration expiration, target legality, damage-defense calculation
    or general simultaneous-event dispatch.
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
