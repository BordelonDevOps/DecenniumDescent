"""Finite AA-05..09 histories using real source lineage, training and payments."""
from copy import deepcopy
from datetime import datetime, timezone
import json
from pathlib import Path
from feat335_source_unarmed_choices import SourceUnarmedChoices, CLAWS
from feat_exact_01_weapon_profile_choices import WeaponProfileChoices, UNARMED, resolve_kept_attack
from validate_feat_exact_01_composite_casting import read, info, serial

R = Path(__file__).resolve().parents[1]
G = R.parents[1]
A = G / 'docs/audit/2026-10-08/full-game'


def main():
    output = A / 'FEAT335_FAA03_UNARMED_PROFILE_CHECK.json'
    assert not output.exists(), 'Existing evidence is immutable'
    paths = [Path(__file__), R/'tools/feat335_source_unarmed_choices.py',
             R/'tools/feat_exact_01_weapon_profile_choices.py', R/'tools/feat_exact_01_acquisition_models.py',
             R/'tools/feat_exact_01_half_feat_choices.py', R/'tools/feat_exact_01_training_prerequisite_model.py',
             R/'tools/feat_exact_01_lineage_prerequisite_model.py',
             R/'data/playtest/character_foundation.json', R/'data/playtest/ancestry_background_candidate.json',
             R/'data/playtest/equipment_source_catalog.json', R/'data/playtest/equipment_acquisition_candidate.json',
             R/'data/public/class_playtests/monk.json', A/'FEAT_EXACT_01_ACQUISITION_CONTRACTS.json',
             R/'data/public/feat_candidates/exact_01/candidate.json',
             R/'data/public/feat_candidates/exact_01/shared_rules.json',
             R/'docs/mechanics/EQUIPMENT_ACQUISITION_PLAYTEST.md',
             R/'docs/mechanics/CORE_RESOLUTION_PLAYTEST.md',
             A/'FEAT335_FAA03_PROFILE_BRIDGE_DERIVED_OPERATIONS.json',
             A/'feat335-acquisition-audit-01-verdict/ACCEPTANCE_EXPECTATIONS.json',
             A/'FEAT_EXACT_01_INITIATE_ACQUISITION_CHECK.json']
    bindings = [info(p) for p in paths]
    foundation = read(paths[7]); classes = {x['class']: x for x in foundation['classes']}
    ancestry = read(paths[8]); equipment = {x['id']: x for x in read(paths[9])['records']}
    items = read(paths[10])['items']; monk = read(paths[11])
    contracts = {x['id']: x for x in read(paths[12])['records']}
    public = {x['id']: x for x in read(paths[13])['feats']}
    shared = read(paths[14])['rules'][1]['wording']
    checks = []; histories = []

    def check(label, actual, expected=True):
        row = {'id': label, 'actual': deepcopy(actual), 'expected': deepcopy(expected), 'passed': actual == expected}
        checks.append(row)
        if not row['passed']: raise AssertionError(label)

    def rejection(label, h, callback, reason):
        before = h.snapshot()
        try: callback()
        except ValueError as error:
            check(label+'/specific-rejection', reason in str(error))
        else: check(label+'/reject', False)
        check(label+'/no-payment-or-state-mutation', h.snapshot(), before)

    def actor(first, ancestry_id='human', variant_id='imperial-human'):
        base = next(x for x in ancestry['ancestries'] if x['id'] == ancestry_id)
        variant = next(x for x in base['variants'] if x['id'] == variant_id)
        rolls = {a: [4, 4, 4, 4] for a in ['STR', 'DEX', 'CON', 'INT', 'WIS', 'CHA']}
        return {'firstClass': first, 'classLevels': {first: 1}, 'priorFeatChoices': [],
                'ancestryId': ancestry_id, 'variantId': variant_id, 'abilityRolls': rolls,
                'permanentScores': {a: 12+variant['combinedAbilityBonuses'].get(a, 0) for a in rolls},
                'physicalInventory': [], 'projection': 'Selected source lineage and first-class training; not a complete character sheet'}

    def new(first='Monk', ancestry_id='human', variant_id='imperial-human'):
        return SourceUnarmedChoices(actor(first, ancestry_id, variant_id), ancestry, classes, equipment, contracts, monk['engine'][17])

    def opportunity(h, level):
        h.advance(level); h.earn(level)

    def record(label, start, h, **extra):
        histories.append({'id': label, 'before': start, 'after': h.snapshot(), **extra})

    for sid in ['weaponFocus', 'weapon_mastery', 'weapon_master', 'tavern_brawler']:
        check(sid+'/exact-public-contract', contracts[sid]['completeOperativeProcedure'], public[sid]['operationalRules'])
    for phrase in ['specific unarmed-strike profile is an eligible choice', 'Claws alone grants no proficiency',
                   'No separate external training credential is necessary', 'die progression alone is not a new paid profile',
                   'without a new ongoing-proficiency gate']:
        check('actual-FS02/'+phrase, phrase in shared)
    check('actual-unarmed-source-category', equipment[UNARMED]['category'], 'Simple melee weapons')
    check('unarmed-not-inventory', 'Unarmed strike is an attack option, not an inventory object.' in paths[15].read_text(encoding='utf-8'))
    check('actual-Monk-Simple-weapons', classes['Monk']['weapons'], 'Simple weapons; kama; nunchaku; staff')
    check('actual-Warrior-does-not-grant-Simple', classes['Warrior']['weapons'], 'Martial weapons')
    check('Monk-source-binding', info(paths[11])['sha256'], classes['Monk']['classCandidateSha256'])
    check('actual-Monk-progression', monk['engine'][17], 'Unarmored Flow completion: while wearing no armor or shield, AC=10+DEX modifier+WIS modifier, or ordinary armorless AC if higher, never both. Unarmed strikes use DEX for attack/damage and 1d6 at 1, 1d8 at 5, 1d10 at 11, 1d12 at 17. This is a new numeric completion; no automatic Extra Attack beyond printed techniques.')

    # Specific source profiles, never a broad natural/unarmed family label.
    for first, lineage, variant, profile, train in [
        ('Monk', 'human', 'imperial-human', UNARMED, False),
        ('Thief', 'human', 'imperial-human', UNARMED, True),
        *[(c, 'troll', v, CLAWS, c == 'Warrior') for c in ['Monk', 'Warrior']
          for v in ['swamp-troll', 'stone-troll', 'blood-troll']]]:
        h = new(first, lineage, variant); start = h.snapshot(); tag = first+'/'+variant+'/'+profile
        check(tag+'/no-item-or-free-feat', [h.actor['physicalInventory'], h.pay.grants], [[], []])
        if lineage == 'troll':
            check(tag+'/actual-trait-and-lineage', h.source_unarmed_profiles[CLAWS]['lineageReceipt']['variantId'], variant)
            check(tag+'/no-external-credential-required', 'conditionalSeparatelyAuthorizedProficiency' not in json.dumps(h.snapshot(), default=serial))
        opportunity(h, 4)
        if train:
            for sid in ['weaponFocus', 'weapon_mastery']:
                rejection(tag+'/'+sid+'/body-alone-not-training', h, lambda sid=sid: h.acquire_profile(sid, 4, profile), 'Actual selected-profile proficiency')
            h.acquire_tavern_brawler(4)
            check(tag+'/real-paid-training', h.profile_receipts[profile]['grant']['identity'], 'tavern_brawler')
            rejection(tag+'/cannot-reuse-training-payment', h, lambda: h.acquire_profile('weaponFocus', 4, profile), 'No unspent earned opportunity')
            focus_level, mastery_level = 8, 12
            opportunity(h, focus_level)
        else:
            check(tag+'/real-class-training', h.profile_receipts[profile]['grant'], 'Monk/first-class-weapons')
            rejection(tag+'/Mastery-below-level-six', h, lambda: h.acquire_profile('weapon_mastery', 4, profile), 'Actual selected-profile proficiency')
            focus_level, mastery_level = 4, 8
        focus = h.acquire_profile('weaponFocus', focus_level, profile)
        opportunity(h, mastery_level)
        mastery = h.acquire_profile('weapon_mastery', mastery_level, profile)
        check(tag+'/separate-paid-selections', [focus['grant']['opportunity'], mastery['grant']['opportunity']],
              [first+':'+str(focus_level), first+':'+str(mastery_level)])
        check(tag+'/no-free-proficiency', [focus['proficiencyGranted'], mastery['proficiencyGranted']], [[], []])
        check(tag+'/covering-receipt-fixed', focus['proficiencyReceipt'], mastery['proficiencyReceipt'])
        mods = h.adjustments(profile, 'melee')
        check(tag+'/Focus-and-Mastery', [mods['focusAttackBonus'], mods['criticalThreshold'], mods['flatDamageBonus']], [1, 19, 0])
        saved_grants = deepcopy(h.pay.grants); saved_payment = deepcopy(h.pay.opportunities)
        h.conditional_proficiency_state(profile, False)
        lost = h.adjustments(profile, 'melee')
        check(tag+'/conditional-training-loss-Focus-only', [lost['focusAttackBonus'], lost['criticalThreshold']], [0, 19])
        h.conditional_proficiency_state(profile, True)
        check(tag+'/restore-no-repurchase', [h.pay.grants, h.pay.opportunities], [saved_grants, saved_payment])
        for kwargs in [{'usable': False}, {'retains_profile': False}]:
            absent = h.adjustments(profile, 'melee', **kwargs)
            check(tag+'/missing-body-or-profile/'+str(kwargs), [absent['focusAttackBonus'], absent['criticalThreshold']], [0, 20])
        before_query = h.snapshot()
        outcomes = [resolve_kept_attack(19, 0, 21, mods), resolve_kept_attack(19, 0, 20, mods), resolve_kept_attack(20, -100, 100, mods)]
        check(tag+'/19-misses-19-hits-20-auto', [(x['hit'], x['critical']) for x in outcomes], [(False, False), (True, True), (True, True)])
        check(tag+'/broadest-not-additive', h.adjustments(profile, 'melee', other_critical_thresholds=(18,))['criticalThreshold'], 18)
        check(tag+'/queries-create-no-attacks', h.snapshot(), before_query)
        if profile == CLAWS:
            ordinary = h.adjustments(UNARMED, 'melee')
            check(tag+'/specific-Claws-not-all-unarmed', [ordinary['focusAttackBonus'], ordinary['criticalThreshold']], [0, 20])
        opportunity(h, 16)
        rejection(tag+'/Mastery-cannot-repeat', h, lambda: h.acquire_profile('weapon_mastery', 16, UNARMED), 'Nonrepeatable identity already acquired')
        rejection(tag+'/Focus-same-profile-cannot-repeat', h, lambda: h.acquire_profile('weaponFocus', 16, profile), 'Choose another actually proficient weapon profile')
        for alias in ['unarmed', 'Monk', 'all natural weapons', 'all unarmed strikes']:
            rejection(tag+'/umbrella/'+alias, h, lambda alias=alias: h.acquire_profile('weapon_mastery', 16, alias), 'outside this evidence slice')
        record(tag, start, h, conditionalUseOutcomes=outcomes,
               scope='Source-authenticated selection/training/payments. Proficiency loss, usable body, target AC and other range are conditional probes, not campaign events.')

    h = new(); start = h.snapshot()
    rejection('unearned-opportunity', h, lambda: h.acquire_profile('weaponFocus', 4, UNARMED), 'No unspent earned opportunity')
    opportunity(h, 4); h.advance(6)
    rejection('level-six-is-not-a-free-opportunity', h, lambda: h.earn(6), 'No actual class-scheduled opportunity')
    acquired = h.acquire_profile('weapon_mastery', 4, UNARMED)
    check('saved-level4-opportunity-at-attained6', [acquired['grant']['opportunity'], acquired['totalCharacterLevel']], ['Monk:4', 6])
    record('attained-six-uses-real-banked-four', start, h)

    h = new(); start = h.snapshot(); progression = [h.monk_unarmed_statistics()]
    opportunity(h, 4); h.acquire_profile('weaponFocus', 4, UNARMED)
    h.advance(5); progression.append(h.monk_unarmed_statistics())
    opportunity(h, 8); h.acquire_profile('weapon_mastery', 8, UNARMED)
    grants = deepcopy(h.pay.grants); paid = deepcopy(h.pay.opportunities)
    for level in [11, 17]:
        h.advance(level); progression.append(h.monk_unarmed_statistics())
        check('Monk-progression-no-repurchase/'+str(level), [h.pay.grants, h.pay.opportunities], [grants, paid])
        check('Monk-progression-retains-benefits/'+str(level), h.adjustments(UNARMED, 'melee')['criticalThreshold'], 19)
    check('actual-die-progression-same-profile', [(p['classLevel'], p['dieSides'], p['profile']) for p in progression],
          [(1, 6, UNARMED), (5, 8, UNARMED), (11, 10, UNARMED), (17, 12, UNARMED)])
    record('actual-Monk-progression-not-new-profile', start, h, progression=progression)

    # A real Human has no acquired Troll body, even after acquiring unarmed training.
    h = new('Thief'); start = h.snapshot(); opportunity(h, 4); h.acquire_tavern_brawler(4); opportunity(h, 8)
    rejection('Human-cannot-name-absent-Troll-body', h, lambda: h.acquire_profile('weaponFocus', 8, CLAWS), 'outside this evidence slice')
    record('training-does-not-create-body', start, h)

    # Exercise the existing full first-class helper as well as the finite lineage adapter.
    skills = {s: a for a, group in foundation['skillAbilities'].items() for s in group}
    backgrounds = {x['id']: x for x in ancestry['backgrounds']}
    original_actor = deepcopy(read(paths[19])['actorSourceProjection'])
    original_actor.update(firstClass='Monk', classLevels={'Monk': 1}, selectedClassSkills=['Acrobatics', 'Athletics'],
                          classToolChoices=[next(k for k, v in equipment.items() if v.get('group') == "Artisan's Tools")])
    full = WeaponProfileChoices(original_actor, classes, equipment, skills, ancestry, backgrounds, contracts, items)
    start = full.snapshot(); opportunity(full, 8)
    full.acquire_profile('weapon_mastery', 8, UNARMED)
    check('existing-helper-admits-trained-unarmed-Mastery', full.adjustments(UNARMED, 'melee')['criticalThreshold'], 19)
    opportunity(full, 12)
    menu = sorted(full.weapon_choices)
    check('Weapon-Master-inventory-menu-unchanged', len(menu), 40)
    for extra in [UNARMED, CLAWS]:
        rejection('Weapon-Master-no-unarmed-menu-expansion/'+extra, full,
                  lambda extra=extra: full.acquire_half('weapon_master', 12, 'DEX', [extra]+menu[:3]), 'four distinct actual complete current catalog')
    record('existing-helper-and-unchanged-Weapon-Master-menu', start, full)

    # All 40 prior inventory profiles remain selectable under the original exact training gates.
    regression = []
    for profile in menu:
        legacy_actor = deepcopy(original_actor)
        legacy_actor.update(firstClass='Warrior', classLevels={'Warrior': 1},
                            selectedClassSkills=['Animal Handling', 'Athletics'], classToolChoices=[])
        h = WeaponProfileChoices(legacy_actor, classes, equipment, skills, ancestry, backgrounds, contracts, items)
        if profile not in h.weapons:
            opportunity(h, 4); h.acquire_half('weapon_master', 4, 'DEX', [profile]+[p for p in menu if p != profile][:3])
            focus_level, mastery_level = 8, 12
        else: focus_level, mastery_level = 4, 8
        opportunity(h, focus_level); f = h.acquire_profile('weaponFocus', focus_level, profile)
        opportunity(h, mastery_level); m = h.acquire_profile('weapon_mastery', mastery_level, profile)
        check('inventory-regression/'+profile, [f['selectedProfile'], m['selectedProfile']], [profile, profile])
        regression.append({'profile': profile, 'focus': f, 'mastery': m})

    check('all-input-bindings-unchanged', [info(p) for p in paths], bindings)
    result = {'createdUtc': datetime.now(timezone.utc).isoformat(),
              'scope': 'FAA-03 and AA-05 through AA-09 finite source-qualified profile/payment and conditional modifier evidence; not full characters, attacks, damage, playtesting or campaign event proof.',
              'acceptanceGroups': ['AA-05', 'AA-06', 'AA-07', 'AA-08', 'AA-09'],
              'checks': len(checks), 'failed': sum(not x['passed'] for x in checks),
              'historyCount': len(histories), 'inventoryRegressionCount': len(regression),
              'sourceBindings': bindings, 'results': checks, 'histories': histories, 'inventoryRegressions': regression,
              'preservedLimitations': ['Other natural bodies still need their own actual source and covering grant. No general natural proficiency is supplied.',
                  'No combined Monk/Claws damage formula, attack, item, transformation or class promotion is supplied.',
                  'Conditional proficiency loss and body-use inputs are bounded probes, not actual campaign events.',
                  'All candidate selection flags, owner gates and cosmology deferrals remain unchanged.']}
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2, default=serial)+'\n', encoding='utf-8')
    print(json.dumps({'checks': result['checks'], 'failed': result['failed'], 'histories': len(histories), 'report': info(output)}))


if __name__ == '__main__':
    main()
