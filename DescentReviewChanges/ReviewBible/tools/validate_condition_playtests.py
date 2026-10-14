"""Cross-system regression checks for the bounded condition reference helpers."""
import json
from pathlib import Path
from core_playtest_rules import LifeState, death_save, stabilize, stable_recovery
from condition_playtest_rules import (
    exhaustion_maximum, update_exhaustion, effective_speed, action_permissions,
    attack_condition_modifiers, restore_hp, petrified_damage, prone_movement_cost,
    standing_cost,
    select_generic_periodic, intoxication_score, tolerance_event,
    recovery_project_ready, emergency_care,
)
from spell_playtest_rules import SpellRuleError

ROOT = Path(__file__).resolve().parents[1]
checks = []


def check(name, actual, expected):
    checks.append({'name': name, 'pass': actual == expected, 'actual': actual, 'expected': expected})


def rejects(name, function):
    try:
        function()
    except SpellRuleError:
        check(name, True, True)
    else:
        check(name, False, True)


def main():
    check('Odd maximum floors once', exhaustion_maximum(31, 4), 15)
    check('Maximum HP one does not become zero', exhaustion_maximum(1, 4), 1)
    state = update_exhaustion(LifeState(31, 28), 31, 4)
    check('Losing maximum clamps HP', (state.maximum_hp, state.hp), (15, 15))
    state = update_exhaustion(state, 31, 5)
    check('Next level does not halve again', (state.maximum_hp, state.hp), (15, 15))
    state = update_exhaustion(state, 41, 5)
    check('Maximum buff recomputes from unhalved input without healing', (state.maximum_hp, state.hp), (20, 15))
    state = update_exhaustion(state, 41, 3)
    check('Recovery raises ceiling without healing', (state.maximum_hp, state.hp), (41, 15))
    dead = update_exhaustion(state, 41, 6)
    check('Exhaustion six is death', (dead.dead, dead.hp), (True, 0))
    check('Removing Exhaustion does not revive corpse', update_exhaustion(dead, 41, 0).dead, True)
    check('Flat penalties before halving Speed', effective_speed(30, -15, exhaustion=2), 7)
    check('Grapple overrides positive bonuses', effective_speed(30, 100, conditions=['grappled']), 0)
    check('Exhaustion five overrides bonuses', effective_speed(30, 100, exhaustion=5), 0)
    check('Ordinary Incapacitated leaves movement', effective_speed(30, conditions=['incapacitated']), 30)
    check('Unconscious stops movement', effective_speed(30, conditions=['unconscious']), 0)
    check('Dazed applied after movement forbids Action', action_permissions(['dazed'], voluntary_speed_spent=5)['action'], False)
    check('Dazed applied after Action forbids movement', action_permissions(['dazed'], actions_taken=1)['movement'], False)
    check('Dazed blocks additional granted Action', action_permissions(['dazed'], actions_taken=1)['action'], False)
    check('Dazed retains Reaction', action_permissions(['dazed'])['reaction'], True)
    check('Dazed blocks Bonus Action', action_permissions(['dazed'])['bonusAction'], False)
    check('Dazed retains concentration', action_permissions(['dazed'])['concentrationMayContinue'], True)
    check('Dazed new turn requires a mode', action_permissions(['dazed'])['mustChooseActionOrMovement'], True)
    check('Paralyzed inherits Incapacitated concentration loss', action_permissions(['paralyzed'])['concentrationMayContinue'], False)
    check('Staggered removes Reaction', action_permissions(['staggered'])['reaction'], False)
    check('Incapacitated cannot use Bonus Action', action_permissions(['incapacitated'])['bonusAction'], False)
    check('Prone ranged at five feet follows Core', attack_condition_modifiers(target_conditions=['prone'], kind='ranged')['rollMode'], 'disadvantage')
    check('Prone melee at five feet follows Core', attack_condition_modifiers(target_conditions=['prone'])['rollMode'], 'advantage')
    check('Reach attack beyond five feet against Prone', attack_condition_modifiers(target_conditions=['prone'], distance=10)['rollMode'], 'disadvantage')
    check('Opposing condition modifiers cancel once', attack_condition_modifiers(['poisoned', 'prone'], ['restrained'])['rollMode'], 'normal')
    check('Known invisible location removes condition attack bonus', attack_condition_modifiers(['invisible'], attacker_invisible_location_known=True)['rollMode'], 'normal')
    check('Unknown invisible location grants condition attack bonus', attack_condition_modifiers(['invisible'])['rollMode'], 'advantage')
    check('True perception removes invisible attack bonus', attack_condition_modifiers(['invisible'], target_sees_invisible_attacker=True)['rollMode'], 'normal')
    check('Known invisible target location removes condition defense bonus', attack_condition_modifiers(target_conditions=['invisible'], target_invisible_location_known=True)['rollMode'], 'normal')
    check('Seeing invisible target removes condition defense bonus', attack_condition_modifiers(target_conditions=['invisible'], attacker_sees_invisible_target=True)['rollMode'], 'normal')
    check('Adjacent hit on Unconscious is critical', attack_condition_modifiers(target_conditions=['unconscious'])['criticalIfHit'], True)
    check('Distant hit on Unconscious is not automatically critical', attack_condition_modifiers(target_conditions=['unconscious'], distance=10)['criticalIfHit'], False)
    check('Hidden fear source gives no check disadvantage', attack_condition_modifiers(['frightened'])['rollMode'], 'normal')
    check('Visible fear source gives attack disadvantage', attack_condition_modifiers(['frightened'], frightened_source_visible=True)['rollMode'], 'disadvantage')
    check('Corrupted halves odd healing down', restore_hp(LifeState(20, 2), 5, corrupted=True).hp, 4)
    check('One-point healing can become zero', restore_hp(LifeState(20, 0), 1, corrupted=True).hp, 0)
    check('Guaranteed death recovery remains one', restore_hp(LifeState(20, 0), 1, corrupted=True, kind='death-natural-20').hp, 1)
    check('Core death helper preserves guaranteed one', death_save(LifeState(20, 0), 20, regular_turn_id=1).hp, 1)
    stable = LifeState(20, 0)
    stabilize(stable, 1, 0)
    check('Core Stable helper preserves guaranteed one', stable_recovery(stable, 3600).hp, 1)
    check('Critical Wound ceiling still limits healing', restore_hp(LifeState(20, 18, wounds=(None, None, None)), 10, corrupted=True).hp, 19)
    rejects('No ordinary healing revival', lambda: restore_hp(LifeState(20, 0, dead=True), 20, corrupted=True))
    check('Petrified resists ordinary damage once', petrified_damage(11, 'fire', other_resistance=True), 5)
    check('Petrified does not resist Corruption', petrified_damage(11, 'corruption'), 11)
    check('Explicit Corruption protection applies', petrified_damage(11, 'corruption', explicit_corruption_resistance=True), 5)
    check('Immunity still prevents ordinary damage', petrified_damage(11, 'fire', immune=True), 0)
    check('Crawling costs twice distance', prone_movement_cost(5), 10)
    check('Difficult crawling costs three times distance', prone_movement_cost(5, difficult=True), 15)
    check('Standing uses half current Speed', standing_cost(30, 15), 15)
    rejects('Zero Speed cannot stand for zero cost', lambda: standing_cost(0, 0))
    rejects('Insufficient movement cannot stand', lambda: standing_cost(30, 14))
    rejects('Reject invalid Exhaustion level', lambda: exhaustion_maximum(20, 7))
    generic = {'id': 'generic', 'timing': 'generic-regular-end', 'flat': 3, 'dc': 12, 'order': 1}
    custom = {'id': 'custom-start', 'timing': 'start-next-two-turns', 'flat': 100, 'dc': 20, 'order': 2}
    die = {'id': 'generic-die', 'timing': 'generic-regular-end', 'dice_count': 1, 'die_sides': 6, 'dc': 10, 'order': 3}
    check('Specific periodic timing excluded from generic selection', select_generic_periodic([generic, custom])['id'], 'generic')
    check('Specific-only records do not produce generic tick', select_generic_periodic([custom]), None)
    check('Expected damage chosen before roll, not DC', select_generic_periodic([generic, die])['id'], 'generic-die')
    check('Whole selected record keeps its own DC', select_generic_periodic([generic, die])['dc'], 10)
    higher_dc = dict(generic, id='higher-dc', dc=14, order=10)
    check('Unified arbitration: equal damage uses earliest, not higher DC', select_generic_periodic([generic, higher_dc])['id'], 'generic')
    later = dict(generic, id='later', order=20)
    check('Tie uses earliest application regardless list order', select_generic_periodic([later, generic])['id'], 'generic')
    check('Timed direct Intoxicated remains floor two', intoxication_score(0, 2), 2)
    check('Floor does not erase independent score four', intoxication_score(4, 2), 4)
    rejects('Reject generic timed floor four', lambda: intoxication_score(0, 4))
    rejects('Reject generic timed floor five', lambda: intoxication_score(0, 5))
    check('Third ordinary dose not shortened', tolerance_event(2)['durationHalved'], False)
    check('Third completed dose activates tolerance afterward', tolerance_event(2)['toleranceAfter'], True)
    check('Fourth ordinary dose shortened', tolerance_event(3)['durationHalved'], True)
    check('Double dose retains duration while tolerant', tolerance_event(3, doubled=True)['durationHalved'], False)
    check('Double dose counts two but at most one save event', tolerance_event(1, doubled=True), {'durationHalved': False, 'toleranceAfter': True, 'completedDosesAfter': 3, 'maximumDependenceSavesForEvent': 1})
    check('Anchor cannot finish at one minute before 72 hours', recovery_project_ready('anchor', 50, 50+72*3600-60, [120]*3, [0, 1, 2]), False)
    check('Anchor at 72 hours with work and costs qualifies', recovery_project_ready('anchor', 50, 50+72*3600, [120]*3, [0, 1, 2]), True)
    check('Missing Anchor supply blocks completion', recovery_project_ready('anchor', 0, 72*3600, [120]*3, [0, 1]), False)
    check('Interrupted Anchor cannot complete', recovery_project_ready('anchor', 0, 72*3600, [120]*3, [0, 1, 2], interrupted=True), False)
    rejects('Duplicate payment day rejected', lambda: recovery_project_ready('anchor', 0, 72*3600, [120]*3, [0, 0, 2]))
    check('Seven-day dependence project has actual 168-hour floor', recovery_project_ready('dependence', 0, 167*3600, [60]*7, list(range(7))), False)
    check('Seven-day dependence project completion', recovery_project_ready('dependence', 0, 168*3600, [60]*7, list(range(7))), True)
    check('Missing daily work prevents recovery', recovery_project_ready('dependence', 0, 168*3600, [60]*6+[59], list(range(7))), False)
    cared, event = emergency_care(LifeState(20, 10), 100, 100+2999, success=True)
    check('Successful care just before deadline survives with one Wound', (cared.dead, len(cared.wounds), event['score']), (False, 1, 4))
    cared, event = emergency_care(LifeState(20, 10), 100, 100+3000, success=True)
    check('Care exactly at deadline loses to death', (cared.dead, event['outcome']), (True, 'deadline-death'))
    cared, event = emergency_care(LifeState(20, 10), 100, 100+1800, success=False)
    check('Failed care cannot refresh emergency deadline', event['emergencyDeadline'], 3700)
    cared, event = emergency_care(LifeState(20, 10, wounds=(1, None, None)), 100, 100, success=True)
    check('Three-Wound care exception prevents fourth Wound without removing old ones', (cared.dead, cared.wounds), (False, (1, None, None)))
    cared, event = emergency_care(LifeState(20, 0), 100, 100, success=True)
    check('Emergency care does not heal or stabilize zero HP', (cared.hp, cared.stable), (0, False))
    cared, event = emergency_care(LifeState(20, 10), 100, 100, success=True, wound_immune=True)
    check('Explicit Wound immunity prevents treatment Wound', cared.wounds, ())
    scenarios = 0
    for maximum in range(1, 201):
        for hp in (0, maximum // 2, maximum):
            for level in range(7):
                current = update_exhaustion(LifeState(maximum, hp), maximum, level)
                again = update_exhaustion(current, maximum, level)
                assert current == again
                assert 0 <= current.hp <= current.maximum_hp
                assert current.maximum_hp == (max(1, maximum // 2) if level >= 4 else maximum)
                assert current.dead == (level == 6)
                cleared = update_exhaustion(current, maximum, 0)
                assert cleared.hp == current.hp and cleared.dead == current.dead
                scenarios += 1
    issues = [x for x in checks if not x['pass']]
    report = {'status': 'PASS' if not issues else 'FAIL', 'checks': len(checks),
              'exhaustionStateScenarios': scenarios, 'issues': issues, 'results': checks,
              'scope': 'Condition calculations and selected interactions only; no claim of complete combat, every application, human play balance or live-app integration.'}
    (ROOT / 'docs/mechanics/CONDITION_PLAYTEST_VALIDATION.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(f"{report['status']}: {len(checks)} checks; {scenarios} Exhaustion-state scenarios; {len(issues)} issues")
    if issues:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
