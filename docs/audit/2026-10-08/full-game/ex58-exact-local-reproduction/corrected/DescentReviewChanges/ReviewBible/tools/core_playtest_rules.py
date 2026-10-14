"""Reference calculations for the provisional core integration.

These helpers resolve declared legal rolls; they do not decide target legality,
actions, actual feature ownership, class triggers or advantage sources.
"""
from dataclasses import dataclass, replace
from spell_playtest_rules import integer, SpellRuleError

DEGREES = ['critical-failure', 'failure', 'success', 'critical-success']


def roll_inputs(natural, modifier):
    integer(natural, 'natural d20', 1, 20)
    if isinstance(modifier, bool) or not isinstance(modifier, int):
        raise SpellRuleError('Modifier must be an integer')
    return natural + modifier


def task_check(natural, modifier, dc):
    total = roll_inputs(natural, modifier)
    integer(dc, 'DC', 0)
    degree = 3 if total >= dc+10 else 2 if total >= dc else 0 if total <= dc-10 else 1
    degree = max(0, min(3, degree + (1 if natural == 20 else -1 if natural == 1 else 0)))
    return {'total':total, 'degree':DEGREES[degree], 'success':degree >= 2}


def attack_roll(natural, modifier, armor_class, critical_threshold=20):
    total = roll_inputs(natural, modifier)
    integer(armor_class, 'AC', 0)
    integer(critical_threshold, 'critical threshold', 2, 20)
    hit = natural != 1 and (natural == 20 or total >= armor_class)
    return {'total':total, 'hit':hit, 'critical':hit and natural >= critical_threshold}


def saving_throw(natural, modifier, dc):
    total = roll_inputs(natural, modifier)
    integer(dc, 'DC', 0)
    return {'total':total, 'success':total >= dc, 'failureMargin':max(0, dc-total)}


def opposed_check(actor_natural, actor_modifier, defender_natural, defender_modifier):
    actor = roll_inputs(actor_natural, actor_modifier)
    defender = roll_inputs(defender_natural, defender_modifier)
    return {'actorTotal':actor, 'defenderTotal':defender, 'changesState':actor > defender}


@dataclass
class LifeState:
    maximum_hp: int
    hp: int
    temp_hp: int = 0
    # One entry per Wound, containing its optional d6 Injury result.
    wounds: tuple = ()
    stable: bool = False
    dead: bool = False
    death_successes: int = 0
    death_failures: int = 0
    uses_death_saves: bool = True
    stable_until_seconds: int | None = None
    last_death_turn: int = 0

    def __post_init__(self):
        integer(self.maximum_hp, 'maximum HP', 1)
        integer(self.hp, 'HP', 0, self.maximum_hp)
        integer(self.temp_hp, 'temporary HP', 0)
        integer(self.death_successes, 'death successes', 0, 3)
        integer(self.death_failures, 'death failures', 0, 3)
        if len(self.wounds) > 3:
            raise SpellRuleError('No fourth Wound: later failed save is fatal')
        for injury in self.wounds:
            if injury is not None:
                integer(injury, 'Injury d6', 1, 6)
        if (self.dead or self.stable) and self.hp != 0:
            raise SpellRuleError('Dead or Stable requires zero HP')
        if self.dead and self.stable:
            raise SpellRuleError('Dead cannot also be Stable')
        if not self.dead and (self.death_successes >= 3 or self.death_failures >= 3):
            raise SpellRuleError('Threshold death counters require their completed state transition')
        if (self.hp > 0 or self.stable) and (self.death_successes or self.death_failures):
            raise SpellRuleError('Positive HP and Stable states have cleared death counters')


def kill(state):
    state.dead, state.stable, state.hp = True, False, 0
    state.stable_until_seconds = None


def stabilize(state, d4, now_seconds):
    integer(d4, 'Stable recovery d4', 1, 4)
    integer(now_seconds, 'elapsed seconds', 0)
    if state.dead or state.stable or state.hp != 0:
        raise SpellRuleError('Only a living dying creature can stabilize')
    state.stable = True
    state.death_successes = state.death_failures = 0
    state.stable_until_seconds = now_seconds + d4 * 3600


def healing_ceiling(state):
    return max(1, state.maximum_hp-1) if len(state.wounds)==3 else state.maximum_hp


def heal(state, amount):
    integer(amount, 'healing amount', 0)
    if state.dead:
        raise SpellRuleError('Ordinary healing cannot restore the dead')
    out = replace(state)
    gained = min(amount, max(0, healing_ceiling(out)-out.hp))
    out.hp += gained
    if gained > 0:
        out.stable = False
        out.stable_until_seconds = None
        out.death_successes = out.death_failures = 0
    return out


def damage_event(state, resolved_damage, *, constitution_save_modifier=0,
                 wound_natural=None, injury_d6=None, critical=False, maiming=False,
                 knockout=False, melee=False, stable_d4=None, now_seconds=0):
    """Resolve post-defense damage without mutating the input state.

    constitution_save_modifier includes ability/proficiency/other effects but NOT
    the Wound penalty, which this function applies once. The caller verifies
    actual Maiming/critical/knockout legality and all pre-damage protective features.
    """
    integer(resolved_damage, 'resolved damage', 0)
    if state.dead:
        raise SpellRuleError('Dead target is outside living-damage handling')
    if knockout and not melee:
        raise SpellRuleError('Knockout requires a melee attack')
    out = replace(state)
    before_hp, before_wounds = out.hp, len(out.wounds)
    absorbed = min(out.temp_hp, resolved_damage)
    post_temp = resolved_damage - absorbed
    out.temp_hp -= absorbed
    out.hp = max(0, before_hp-post_temp)
    events = {'postTempDamage':post_temp, 'tempAbsorbed':absorbed, 'woundSaves':0,
              'injuryRolls':0, 'instantDeath':False, 'deathFailuresAdded':0}
    if out.hp == 0 and post_temp-before_hp >= out.maximum_hp:
        kill(out)
        events['instantDeath'] = True
        return out, events
    trigger = (before_hp > 0 and out.hp == 0) or 2*post_temp >= out.maximum_hp or maiming
    if trigger:
        dc = max(10, post_temp//2)
        save = saving_throw(wound_natural, constitution_save_modifier-before_wounds, dc)
        events.update(woundSaves=1, woundDC=dc, woundTotal=save['total'])
        if not save['success']:
            if before_wounds == 3:
                kill(out)
                return out, events
            injury = None
            if save['failureMargin'] >= 5:
                integer(injury_d6, 'required Injury d6', 1, 6)
                injury = injury_d6
                events['injuryRolls'] = 1
            out.wounds += (injury,)
    if before_hp == 0 and post_temp > 0:
        out.stable = False
        out.stable_until_seconds = None
        if not out.uses_death_saves:
            kill(out)
            return out, events
        failures = 2 if critical else 1
        out.death_failures += failures
        events['deathFailuresAdded'] = failures
        if out.death_failures >= 3:
            out.death_failures = 3
            kill(out)
            return out, events
    if out.hp == 0 and before_hp > 0:
        if knockout:
            stabilize(out, stable_d4, now_seconds)
        elif not out.uses_death_saves:
            kill(out)
        else:
            out.stable = False
            out.stable_until_seconds = None
    return out, events


def death_save(state, natural, *, regular_turn_id, regular=True, modifier=0,
               stable_d4=None, now_seconds=0):
    total = roll_inputs(natural, modifier)
    integer(regular_turn_id, 'regular turn identifier', 1)
    if not regular or regular_turn_id <= state.last_death_turn:
        raise SpellRuleError('Death save needs a new regular-turn start')
    if state.dead or state.stable or state.hp != 0 or not state.uses_death_saves:
        raise SpellRuleError('Creature is not dying with death saves')
    out = replace(state, last_death_turn=regular_turn_id)
    if natural == 20:
        return heal(out, 1)
    if natural == 1:
        out.death_failures += 2
    elif total >= 10:
        out.death_successes += 1
    else:
        out.death_failures += 1
    if out.death_failures >= 3:
        out.death_failures = 3
        kill(out)
    elif out.death_successes >= 3:
        stabilize(out, stable_d4, now_seconds)
    return out


def stable_recovery(state, now_seconds):
    integer(now_seconds, 'elapsed seconds', 0)
    if state.stable and not state.dead and state.stable_until_seconds is not None and now_seconds >= state.stable_until_seconds:
        return heal(state, 1)
    return replace(state)


def remove_wounds(state, indices):
    if state.dead:
        raise SpellRuleError('Ordinary treatment requires a living patient')
    if not indices or len(set(indices)) != len(indices):
        raise SpellRuleError('Choose distinct existing Wounds')
    for index in indices:
        integer(index, 'Wound index', 0, len(state.wounds)-1)
    return replace(state, wounds=tuple(v for i,v in enumerate(state.wounds) if i not in indices))


def active_injuries(state):
    return set(x for x in state.wounds if x is not None)


def hit_dice_recovered(normal_recovery_maximum, wounds):
    integer(normal_recovery_maximum, 'normal Hit Dice recovery', 0)
    integer(wounds, 'Wounds', 0, 3)
    return max(0, normal_recovery_maximum-wounds)
