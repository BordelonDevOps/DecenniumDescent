"""Bounded reference calculations for the condition integration draft.

Callers own application legality, independent source records, immunity, duration,
visibility/detection, actual dice, class exceptions and the world clock. This is
not a combat engine and does not apply a condition merely because its name exists.
"""
from dataclasses import replace
from core_playtest_rules import heal, kill
from spell_playtest_rules import integer, SpellRuleError

INCAPACITATING = {'incapacitated', 'paralyzed', 'petrified', 'stunned', 'unconscious'}
IMMOBILE = {'paralyzed', 'petrified', 'stunned', 'unconscious'}


def exhaustion_maximum(otherwise_maximum, level):
    """Input must exclude this Exhaustion reduction; never feed the output back."""
    integer(otherwise_maximum, 'otherwise applicable maximum HP', 1)
    integer(level, 'Exhaustion level', 0, 6)
    return max(1, otherwise_maximum // 2) if level >= 4 else otherwise_maximum


def update_exhaustion(state, otherwise_maximum, level):
    maximum = exhaustion_maximum(otherwise_maximum, level)
    out = replace(state, maximum_hp=maximum, hp=min(state.hp, maximum))
    if level == 6:
        kill(out)
    return out


def effective_speed(base, flat=0, *, exhaustion=0, conditions=()):
    integer(base, 'base Speed', 0)
    integer(exhaustion, 'Exhaustion level', 0, 6)
    if isinstance(flat, bool) or not isinstance(flat, int):
        raise SpellRuleError('Flat Speed adjustment must be an integer')
    if exhaustion >= 5 or set(conditions) & (IMMOBILE | {'grappled', 'restrained'}):
        return 0
    speed = max(0, base + flat)
    return speed // 2 if exhaustion >= 2 else speed


def action_permissions(conditions, *, actions_taken=0, voluntary_speed_spent=0):
    """A Dazed choice remains necessary when both action/movement are available.

    Counts include actions/movement earlier in this turn before becoming Dazed.
    Moving expressly within a permitted Action is not voluntary Speed expenditure.
    """
    integer(actions_taken, 'Actions taken this turn', 0)
    integer(voluntary_speed_spent, 'voluntary Speed spent this turn', 0)
    active = set(conditions)
    incapacitated = bool(active & INCAPACITATING)
    dazed = 'dazed' in active
    return {
        'action': not incapacitated and (not dazed or (actions_taken == 0 and voluntary_speed_spent == 0)),
        'bonusAction': not incapacitated and not dazed,
        'reaction': not incapacitated and 'staggered' not in active,
        'movement': not bool(active & IMMOBILE) and (not dazed or actions_taken == 0),
        'concentrationMayContinue': not incapacitated,
        'mustChooseActionOrMovement': dazed and not incapacitated and actions_taken == 0 and voluntary_speed_spent == 0,
    }


def attack_condition_modifiers(attacker_conditions=(), target_conditions=(), *,
                               distance=5, kind='melee', exhaustion=0,
                               attacker_invisible_location_known=False,
                               target_invisible_location_known=False,
                               target_sees_invisible_attacker=False,
                               attacker_sees_invisible_target=False,
                               frightened_source_visible=False,
                               other_advantage=False, other_disadvantage=False):
    """Return condition-only modifiers for an otherwise legal attack.

    Generic unseen modifiers caused solely by Invisible must NOT be supplied
    again as other_advantage/disadvantage after Core's location endpoint.
    A target's actual sight matters separately from merely knowing a location.
    """
    integer(distance, 'attack distance in feet', 0)
    integer(exhaustion, 'Exhaustion level', 0, 6)
    if kind not in ('melee', 'ranged'):
        raise SpellRuleError('Attack kind must be melee or ranged')
    attacker, target = set(attacker_conditions), set(target_conditions)
    adv, dis = bool(other_advantage), bool(other_disadvantage)
    dis |= bool(attacker & {'blinded', 'poisoned', 'prone', 'restrained'}) or exhaustion >= 3
    dis |= 'frightened' in attacker and frightened_source_visible
    adv |= bool(target & {'blinded', 'paralyzed', 'petrified', 'restrained', 'stunned', 'unconscious'})
    if 'prone' in target:
        adv |= kind == 'melee' and distance <= 5
        dis |= kind == 'ranged' or distance > 5
    adv |= 'invisible' in attacker and not attacker_invisible_location_known and not target_sees_invisible_attacker
    dis |= 'invisible' in target and not target_invisible_location_known and not attacker_sees_invisible_target
    return {'advantagePresent': adv, 'disadvantagePresent': dis,
            'rollMode': 'normal' if adv == dis else 'advantage' if adv else 'disadvantage',
            'criticalIfHit': bool(target & {'paralyzed', 'unconscious'}) and distance <= 5,
            'attackerAbleToAct': not bool(attacker & INCAPACITATING)}


def restore_hp(state, potential_amount, *, corrupted=False, kind='healing-effect'):
    integer(potential_amount, 'potential HP restoration', 0)
    if kind not in ('healing-effect', 'death-natural-20', 'stable-recovery'):
        raise SpellRuleError('Unknown restoration kind')
    if kind != 'healing-effect' and potential_amount != 1:
        raise SpellRuleError('Death/Stable state recovery restores exactly one HP')
    amount = potential_amount // 2 if corrupted and kind == 'healing-effect' else potential_amount
    return heal(state, amount)


def petrified_damage(damage, damage_type, *, explicit_corruption_resistance=False,
                     other_resistance=False, immune=False):
    """Input is after earlier flat reductions/saves; apply resistance once."""
    integer(damage, 'damage before resistance', 0)
    if immune:
        return 0
    resisted = damage_type.lower() != 'corruption' or explicit_corruption_resistance
    # Generic all-damage/other resistance also fails Core's Corruption exception.
    return damage // 2 if resisted else damage


def prone_movement_cost(distance, *, difficult=False):
    integer(distance, 'distance crawled', 0)
    return distance * (3 if difficult else 2)


def standing_cost(speed, remaining):
    integer(speed, 'current Speed', 0)
    integer(remaining, 'remaining movement', 0)
    cost = speed // 2
    if speed == 0 or remaining < cost:
        raise SpellRuleError('Standing needs nonzero Speed and enough remaining movement')
    return cost


def select_generic_periodic(records):
    """Return a generic-only candidate, NEVER a separately resolved extra tick.

    Damage is represented by nonnegative dice_count/die_sides/flat. Record order
    is the stable application sequence, not the list's current sorting order.
    Caller supplies only active records of ONE condition. In a combined game,
    every due generic/custom stack group must enter periodic_marker_arbitration;
    this convenience selector is not a second damage-resolution layer.
    """
    eligible = []
    for record in records:
        if record['timing'] != 'generic-regular-end':
            continue
        count = integer(record.get('dice_count', 0), 'dice count', 0)
        sides = integer(record.get('die_sides', 1), 'die sides', 1)
        flat = integer(record.get('flat', 0), 'flat periodic damage', 0)
        integer(record['dc'], 'ending DC', 0)
        order = integer(record['order'], 'application order', 0)
        eligible.append(((count * (sides + 1) + 2 * flat, -order), record))
    return max(eligible, key=lambda pair: pair[0])[1] if eligible else None


def intoxication_score(dose_driven, direct_floor=0):
    integer(dose_driven, 'dose-driven Intoxication', 0, 5)
    if direct_floor not in (0, 2) or isinstance(direct_floor, bool):
        raise SpellRuleError('Only a generic timed floor of two is defined')
    return max(dose_driven, direct_floor)


def tolerance_event(completed_doses_in_window, *, tolerance_active=False, doubled=False):
    integer(completed_doses_in_window, 'completed doses in seven days', 0)
    active_before = tolerance_active or completed_doses_in_window >= 3
    completed_after = completed_doses_in_window + (2 if doubled else 1)
    return {'durationHalved': active_before and not doubled,
            'toleranceAfter': active_before or completed_after >= 3,
            'completedDosesAfter': completed_after,
            'maximumDependenceSavesForEvent': 1}


def recovery_project_ready(kind, start_seconds, now_seconds, daily_minutes,
                           supply_days, *, interrupted=False):
    """Check one recorded project; inventory and nonoverlapping work are external.

    daily_minutes has one total per project day, not per calendar date. supply_days
    lists distinct zero-based days paid for THIS project; duplicate days are invalid.
    """
    if kind not in ('dependence', 'anchor'):
        raise SpellRuleError('Unknown multi-day recovery project')
    integer(start_seconds, 'project start', 0)
    integer(now_seconds, 'current time', start_seconds)
    days, needed_minutes = (7, 60) if kind == 'dependence' else (3, 120)
    if len(daily_minutes) != days or len(supply_days) != len(set(supply_days)):
        raise SpellRuleError('Project records need exact day count and distinct payments')
    for minutes in daily_minutes:
        integer(minutes, 'daily work minutes', 0)
    for day in supply_days:
        integer(day, 'paid project day', 0, days-1)
    return (not interrupted and now_seconds-start_seconds >= days*86400
            and all(minutes >= needed_minutes for minutes in daily_minutes)
            and set(supply_days) == set(range(days)))


def emergency_care(state, emergency_started, attempt_started, *, success, wound_immune=False):
    """Paid legal 10-minute attempt on an existing level-5 emergency.

    Caller verifies kit expenditure, helper availability and completed task result.
    No input here can extend the emergency deadline. A surviving successful patient
    still needs the new level-4 d4 timer and poison save; this is NOT HP stabilization.
    """
    integer(emergency_started, 'emergency start', 0)
    integer(attempt_started, 'attempt start', emergency_started)
    if state.dead:
        raise SpellRuleError('Emergency care cannot revive a dead patient')
    out = replace(state)
    deadline = emergency_started + 3600
    if attempt_started + 600 >= deadline:
        kill(out)
        return out, {'score': 5, 'emergencyDeadline': deadline, 'outcome': 'deadline-death'}
    if not success:
        return out, {'score': 5, 'emergencyDeadline': deadline, 'outcome': 'failed-care'}
    if len(out.wounds) < 3 and not wound_immune:
        out.wounds += (None,)
    return out, {'score': 4, 'emergencyDeadline': None, 'outcome': 'treated-needs-level4-timer'}
