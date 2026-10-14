"""Paid half-feat score/training choices with source class HP/capacity history."""
from copy import deepcopy
from datetime import datetime, timezone
import json
from pathlib import Path
from feat_exact_01_half_feat_choices import HalfFeatChoices, MENUS
from validate_feat_exact_01_composite_casting import read, info, serial

R = Path(__file__).resolve().parents[1]; G = R.parents[1]; A = G/'docs/audit/2026-10-08/full-game'


def main():
    output = A/'FEAT_EXACT_01_HALF_FEAT_CHOICES_CHECK.json'; notes = A/'FEAT_EXACT_01_HALF_FEAT_CHOICES_NOTES.md'
    assert not output.exists() and not notes.exists()
    paths = [Path(__file__), R/'tools/feat_exact_01_half_feat_choices.py', R/'tools/feat_exact_01_acquisition_models.py',
             R/'tools/feat_exact_01_training_prerequisite_model.py', R/'data/playtest/character_foundation.json',
             R/'data/playtest/ancestry_background_candidate.json', R/'data/playtest/equipment_source_catalog.json',
             R/'data/playtest/equipment_acquisition_candidate.json', R/'docs/mechanics/CHARACTER_CREATION_PLAYTEST.md',
             R/'docs/mechanics/MAXIMUM_HP_PLAYTEST.md', A/'FEAT_EXACT_01_ACQUISITION_CONTRACTS.json',
             A/'FEAT_EXACT_01_INITIATE_ACQUISITION_CHECK.json', R/'data/public/feat_candidates/exact_01/candidate.json',
             R/'data/public/feat_candidates/exact_01/shared_rules.json']
    bindings = [info(p) for p in paths]
    foundation = read(paths[4]); classes = {r['class']: r for r in foundation['classes']}
    skills = {s: a for a, group in foundation['skillAbilities'].items() for s in group}
    ancestry = read(paths[5]); backgrounds = {r['id']: r for r in ancestry['backgrounds']}
    equipment = {r['id']: r for r in read(paths[6])['records']}; items = read(paths[7])['items']
    contracts = {r['id']: r for r in read(paths[10])['records']}
    actor = deepcopy(read(paths[11])['actorSourceProjection'])
    actor.update(firstClass='Warrior', classLevels={'Warrior': 1}, selectedClassSkills=['Animal Handling', 'Athletics'])
    checks = []; traces = []

    def check(label, truth):
        checks.append({'id': label, 'passed': bool(truth)})
        if not truth:
            raise AssertionError(label)

    def history(custom=None):
        return HalfFeatChoices(custom or actor, classes, equipment, skills, ancestry, backgrounds, contracts, items)

    def reject(label, h, sid, level, ability, weapons=None):
        before = h.snapshot()
        try:
            h.acquire(sid, level, ability, weapons)
        except ValueError as error:
            checks.append({'id': label, 'passed': True, 'reason': str(error)})
        else:
            check(label, False)
        check(label + '/atomic-rejection', before == h.snapshot())
        traces.append({'id': label, 'kind': 'rejected-command', 'before': before, 'unchangedAfter': h.snapshot()})

    def record(label, before, h, scope='Actual Human/Imperial first-class ability/training, real earned ASI/feat history and fixed class HP-base slice; not a complete class build or campaign record'):
        traces.append({'id': label, 'scope': scope, 'before': before, 'after': h.snapshot()})

    weapon_ids = sorted(history().weapon_choices); check('40-reviewed-current-weapon-profiles', len(weapon_ids) == 40)
    check('reviewed-new-weapon-completions-included-unarmed-excluded', {'new.kama', 'new.nunchaku', 'new.repeating-heavy-crossbow'} <= set(weapon_ids) and 'simple-melee-weapons.unarmed-strike' not in weapon_ids)
    selected_weapons = weapon_ids[:4]
    # Three score boundaries derive from actual ASI histories, rather than
    # editing the permanent score after character generation.
    for sid, menu in MENUS.items():
        for ability in menu:
            for target in [16, 19, 20]:
                h = history(); other = 'DEX' if ability != 'DEX' else 'STR'
                if target >= 19:
                    h.advance(4); h.earn(4); h.asi(4, {ability: 2})
                    h.advance(8); h.earn(8); h.asi(8, {ability: 2} if target == 20 else {ability: 1, other: 1})
                if sid == 'moderately_armored':
                    # Actual Warrior has Medium/Heavy, not Light. Acquire its
                    # Light prerequisite lawfully and separately at a real ASI.
                    light_level = 12 if target >= 19 else 4
                    h.advance(light_level); h.earn(light_level); h.acquire('lightly_armored', light_level, other)
                    level = 16 if target >= 19 else 8
                else:
                    level = 12 if target >= 19 else 4
                h.advance(level); h.earn(level)
                before = h.snapshot(); check(sid + ability + str(target) + '/true-pre-acquisition-score', h.pay.scores[ability] == target)
                event = h.acquire(sid, level, ability, selected_weapons if sid == 'weapon_master' else None)
                label = sid + '/' + ability + '/from' + str(target)
                check(label + '/actual-half-score-increase', h.pay.scores[ability] == min(20, target+1) and event['actualScoreIncrease'] == (0 if target == 20 else 1))
                check(label + '/one-new-real-payment', len(h.pay.grants) == len(before['payment']['grants'])+1 and h.pay.opportunities['Warrior:'+str(level)]['spent'])
                check(label + '/capacity-change-is-not-recovery', h.hp_current == before['hp']['current'] and h.hit_dice_unspent == before['resources']['unspentHitDice'] and h.rp_current == before['resources']['currentRP'] and h.wounds == before['hp']['wounds'])
                check(label + '/no-free-equipment', h.actor['physicalInventory'] == [] and event['equipmentGranted'] == [])
                if sid == 'resilient':
                    check(label + '/exact-one-save-union', h.saves == set(before['saves']) | {ability})
                if sid in {'lightly_armored', 'moderately_armored', 'heavily_armored'}:
                    given = {'lightly_armored': {'light', 'shields'}, 'moderately_armored': {'medium', 'shields'}, 'heavily_armored': {'heavy'}}[sid]
                    check(label + '/exact-armor-union', h.armor == set(before['armor']) | given)
                if sid == 'weapon_master':
                    check(label + '/exact-four-profile-union', h.weapons == set(before['weapons']) | set(selected_weapons))
                record(label, before, h)
                future = next(n for n in classes['Warrior']['asiClassLevels'] if n > level)
                h.advance(future); h.earn(future)
                reject(label + '/same-identity-choice-not-repeatable', h, sid, future, ability, selected_weapons if sid == 'weapon_master' else None)

    # Show that a real odd CON modifier boundary raises capacity, without
    # creating ordinary HP healing or recharging existing resources.
    odd = deepcopy(actor); odd['abilityRolls']['CON'] = [1, 4, 6, 6]; odd['permanentScores']['CON'] = 17
    for sid in ['durable', 'resilient']:
        h = history(odd); h.advance(4); h.earn(4); before = h.snapshot(); h.acquire(sid, 4, 'CON')
        check(sid + '/CON17-to18-per-level-recomputation', before['hp']['maximum'] == 45 and h.hp_max == 49 and h.hp_current == 15)
        record(sid + '/real-CON-modifier-boundary', before, h)
    h = history(); h.advance(4); h.earn(4); h.acquire('resilient', 4, 'STR')
    h.advance(8); h.earn(8); before = h.snapshot(); h.acquire('resilient', 8, 'DEX')
    check('Resilient-different-save-repeat-legal', h.saves == {'STR', 'CON', 'DEX'} and len(h.pay.grants) == 2 and h.pay.scores['STR'] == 17 and h.pay.scores['DEX'] == 17)
    record('different-Resilient-repeat', before, h)
    h.advance(12); h.earn(12); reject('Resilient-original-save-repeat-rejected', h, 'resilient', 12, 'STR')

    # Exercise every current reviewed weapon profile in an actual four-choice
    # selection, including already-trained Martial and newly gained Simple.
    for profile in weapon_ids:
        h = history(); h.advance(4); h.earn(4); selected = [profile] + [p for p in weapon_ids if p != profile][:3]
        before = h.snapshot(); h.acquire('weapon_master', 4, 'DEX', selected)
        check(profile + '/source-profile-selection', set(selected) <= h.weapons and h.weapons == set(before['weapons']) | set(selected))
        check(profile + '/no-profession-expertise-or-item', h.actor['physicalInventory'] == [] and h.pay.scores['DEX'] == 17)
        record('weapon-choice/' + profile, before, h)
    for label, selected in [('too-few', weapon_ids[:3]), ('too-many', weapon_ids[:5]), ('duplicate', [weapon_ids[0]]*4),
                            ('unarmed-umbrella', ['unarmed']+weapon_ids[:3]), ('natural-umbrella', ['all-natural-weapons']+weapon_ids[:3]),
                            ('unknown-special', ['invented-special']+weapon_ids[:3]), ('tool-is-not-weapon', ['tools.smith-s-tools']+weapon_ids[:3])]:
        h = history(); h.advance(4); h.earn(4); reject('WeaponMaster/' + label, h, 'weapon_master', 4, 'STR', selected)
    for sid, menu in MENUS.items():
        h = history(); h.advance(4); h.earn(4)
        bad = next((a for a in ['STR', 'DEX', 'CON', 'INT', 'WIS', 'CHA'] if a not in menu), 'Agility')
        reject(sid + '/wrong-ability-menu', h, sid, 4, bad, selected_weapons if sid == 'weapon_master' else None)
        reject(sid + '/missing-permanent-ability-choice', h, sid, 4, None, selected_weapons if sid == 'weapon_master' else None)
    h = history(); h.advance(4); h.earn(4); reject('Warrior-medium-does-not-imply-light', h, 'moderately_armored', 4, 'STR')
    monk = deepcopy(actor); monk.update(firstClass='Monk', classLevels={'Monk': 1}, selectedClassSkills=['Acrobatics', 'Athletics'], classToolChoices=['tools.tinker-s-tools'])
    h = history(monk); h.advance(4); h.earn(4); reject('Monk-no-medium-prerequisite', h, 'heavily_armored', 4, 'STR')
    before = h.snapshot(); h.acquire('lightly_armored', 4, 'DEX')
    h.advance(8); h.earn(8); h.acquire('moderately_armored', 8, 'STR')
    h.advance(12); h.earn(12); h.acquire('heavily_armored', 12, 'STR')
    check('Monk-three-armor-feats-have-real-separate-history', h.armor == {'light', 'medium', 'heavy', 'shields'} and [g['opportunity'] for g in h.pay.grants] == ['Monk:4', 'Monk:8', 'Monk:12'])
    check('Monk-capacity-growth-never-refills-existing-RP', h.rp_max == 9 and h.rp_current == 1)
    record('Monk-Light4-Medium8-Heavy12', before, h)
    h = history(); h.advance(4); h.earn(4); before = h.snapshot(); h.acquire('observant', 4, 'INT')
    check('Observant-exact-two-passive-recipients', h.passive('Perception') == 18 and h.passive('Investigation') == 18)
    record('Observant-two-untrained-passive-recipients', before, h)
    h = history(); h.advance(4); reject('no-earned-choice-no-half-feat', h, 'durable', 4, 'CON')
    # Explicitly conditional above-ceiling premise tests non-reduction, not an
    # unsupported ordinary source of a score greater than 20.
    h = history(); h.advance(4); h.earn(4); h.pay.scores['CON'] = 21; h.recalculate()
    before = h.snapshot(); h.acquire('durable', 4, 'CON')
    check('conditional-above-cap-never-reduced', h.pay.scores['CON'] == 21 and h.events[-1]['actualScoreIncrease'] == 0)
    record('conditional-above-cap', before, h, 'Conditional separately authorized above-20 score premise only; no such grant is created or authenticated')
    public = {r['id']: r for r in read(paths[12])['feats']}
    for sid in MENUS:
        check(sid + '/full-procedure-equality', public[sid]['operationalRules'] == contracts[sid]['completeOperativeProcedure'])
    check('bound-sources-preserved', bindings == [info(p) for p in paths])
    report = {'createdAtUtc': datetime.now(timezone.utc).isoformat(), 'status': 'eight-half-feat-acquisition-choice-pass',
              'checks': len(checks), 'failures': [], 'results': checks, 'sourceBindings': bindings,
              'cohort': list(MENUS), 'menus': MENUS, 'actorSourceProjection': actor, 'weaponProfiles': weapon_ids,
              'traces': traces, 'counts': {'identities': 8, 'permanentAbilityMenuEntries': sum(len(m) for m in MENUS.values()),
                                        'ordinaryScoreBoundaries': [16, 19, 20], 'currentReviewedWeaponProfiles': 40,
                                        'recordedTraces': len(traces), 'newPartialPrerequisiteIdentities': 0},
              'limits': ['Actual source-derived first-class/ability/ASI/training and fixed HP-base slice, not all class cards, complete builds or campaign authentication.',
                         'All 40 current reviewed catalog weapon profiles are exercised; unprovided Special or natural profiles remain unestablished, not deleted from the source permission.',
                         'Use permissions, armor/equipment legality, movement, passive examination, Hit Die healing and other full feat effects are not simulated by this acquisition pass.',
                         'The above-20 case is explicitly conditional; no new score-cap exception is created.',
                         'No full335-acquisition acceptance, exact GPT approval, runtime, balance, publication or cosmology approval claimed.'],
              'sourceInformationDeleted': False, 'newRulesAdopted': False, 'fullCandidateApproved': False}
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2, default=serial)+'\n', encoding='utf-8', newline='\n')
    notes.write_text('# Eight half-feat acquisition choices\n\n'
        f'{len(checks)} checks passed across {len(traces)} traces. Athlete, Durable, Heavily Armored, Lightly Armored, Moderately Armored, Observant, Resilient and Weapon Master '
        'are exercised with their actual ability menus, real class ASIs and permanent score boundaries 16, 19 and 20. '
        'The capped branch grants zero ability increase while retaining the other actual training grants.\n\n'
        'Includes separate armor-prerequisite purchases, Resilient different-save repetition, every one of the 40 current reviewed catalog weapon profiles in four-choice selections, '
        'and actual class HP-base recomputation without healing/resource refills. The above-20 boundary is expressly conditional.\n\n'
        'This is an acquisition/capacity slice, not a complete build, equipment-use or combat simulation. Unprovided special/natural weapon sources are not invented. '
        'All original procedures and flags are preserved; full feat effects, all335 acquisitions and exact GPT candidate review remain open.\n', encoding='utf-8', newline='\n')
    print(json.dumps({'checks': len(checks), 'failures': 0, 'counts': report['counts'], 'report': info(output), 'notes': info(notes)}, indent=2))


if __name__ == '__main__':
    main()
