"""Source-qualified weapon choices plus expressly bounded modifier histories."""
from copy import deepcopy
from datetime import datetime, timezone
import json
from pathlib import Path
from feat_exact_01_weapon_profile_choices import WeaponProfileChoices, UNARMED, resolve_kept_attack
from validate_feat_exact_01_composite_casting import read, info, serial

R = Path(__file__).resolve().parents[1]; G = R.parents[1]
A = G / 'docs/audit/2026-10-08/full-game'


def main():
    output = A / 'FEAT_EXACT_01_WEAPON_PROFILE_CHOICES_CHECK.json'
    notes = A / 'FEAT_EXACT_01_WEAPON_PROFILE_CHOICES_NOTES.md'
    assert not output.exists() and not notes.exists(), 'Existing evidence is immutable'
    paths = [Path(__file__), R / 'tools/feat_exact_01_weapon_profile_choices.py',
        R / 'tools/feat_exact_01_half_feat_choices.py', R / 'tools/feat_exact_01_acquisition_models.py',
        R / 'tools/feat_exact_01_training_prerequisite_model.py',
        R / 'data/playtest/character_foundation.json', R / 'data/playtest/ancestry_background_candidate.json',
        R / 'data/playtest/equipment_source_catalog.json', R / 'data/playtest/equipment_acquisition_candidate.json',
        A / 'FEAT_EXACT_01_ACQUISITION_CONTRACTS.json', A / 'FEAT_EXACT_01_INITIATE_ACQUISITION_CHECK.json',
        R / 'data/public/feat_candidates/exact_01/candidate.json', R / 'data/public/feat_candidates/exact_01/shared_rules.json',
        R / 'docs/mechanics/CHARACTER_CREATION_PLAYTEST.md', R / 'docs/mechanics/EQUIPMENT_ACQUISITION_PLAYTEST.md',
        R / 'docs/mechanics/CORE_RESOLUTION_PLAYTEST.md', R / 'docs/mechanics/ANCESTRY_BACKGROUND_PLAYTEST.md',
        A / 'FEAT327_ACQ_01_GPT_ADDENDUM.md']
    bindings = [info(p) for p in paths]
    foundation = read(paths[5]); classes = {x['class']: x for x in foundation['classes']}
    skills = {s: a for a, group in foundation['skillAbilities'].items() for s in group}
    ancestry = read(paths[6]); backgrounds = {x['id']: x for x in ancestry['backgrounds']}
    equipment = {x['id']: x for x in read(paths[7])['records']}; items = read(paths[8])['items']
    contracts = {x['id']: x for x in read(paths[9])['records']}
    actor = deepcopy(read(paths[10])['actorSourceProjection'])
    actor.update(firstClass='Warrior', classLevels={'Warrior': 1}, selectedClassSkills=['Animal Handling', 'Athletics'])
    public = {x['id']: x for x in read(paths[11])['feats']}
    checks = []; traces = []

    def check(label, truth):
        checks.append({'id': label, 'passed': bool(truth)})
        if not truth: raise AssertionError(label)

    def history(custom=None):
        return WeaponProfileChoices(custom or actor, classes, equipment, skills, ancestry, backgrounds, contracts, items)

    def opportunity(h, level):
        h.advance(level); h.earn(level)

    def rejection(label, h, callback):
        before = h.snapshot()
        try: callback()
        except ValueError as error:
            checks.append({'id': label, 'passed': True, 'reason': str(error)})
        else: check(label, False)
        check(label + '/no-payment-or-state-mutation', before == h.snapshot())

    def record(label, before, h, **extra):
        traces.append({'id': label, 'before': before, 'after': h.snapshot(), **extra})

    for sid in ['weaponFocus', 'weapon_mastery', 'weapon_master', 'precision_throw']:
        check(sid + '/current-exact-procedure', contracts[sid]['completeOperativeProcedure'] == public[sid]['operationalRules'])
    check('Focus-express-unarmed-qualification', 'unarmed-strike profile' in contracts['weaponFocus']['completeOperativeProcedure'])
    check('Mastery-keeps-acquisition-and-use-distinct', 'At acquisition' in contracts['weapon_mastery']['completeOperativeProcedure'] and
          'while that proficiency remains operative' not in contracts['weapon_mastery']['completeOperativeProcedure'])
    profiles = sorted(history().weapon_choices)
    check('40-current-reviewed-equipment-profiles', len(profiles) == 40)
    check('40-menu-includes-new-completions', {'new.kama', 'new.nunchaku', 'new.repeating-heavy-crossbow'} <= set(profiles))
    check('Warrior-Monk-distinct-source-grants', classes['Warrior']['weapons'] == 'Martial weapons' and classes['Monk']['weapons'].startswith('Simple weapons;'))
    check('unarmed-source-and-reviewed-noninventory-treatment', equipment[UNARMED]['category'] == 'Simple melee weapons' and
          'Unarmed strike is an attack option, not an inventory object.' in paths[14].read_text(encoding='utf-8'))
    class_supported = 0; purchased_training = 0
    for profile in profiles:
        h = history(); start = h.snapshot()
        if profile in h.weapons:
            focus_level, mastery_level = 4, 8; class_supported += 1
        else:
            opportunity(h, 4)
            rejection(profile + '/possession-not-proficiency', h, lambda: h.acquire_profile('weaponFocus', 4, profile))
            choices = [profile] + [p for p in profiles if p != profile][:3]
            h.acquire_half('weapon_master', 4, 'DEX', choices)
            focus_level, mastery_level = 8, 12; purchased_training += 1
        opportunity(h, focus_level); event = h.acquire_profile('weaponFocus', focus_level, profile)
        opportunity(h, mastery_level); master = h.acquire_profile('weapon_mastery', mastery_level, profile)
        check(profile + '/permanent-exact-matching-choices', event['selectedProfile'] == master['selectedProfile'] == profile)
        check(profile + '/actual-grant-snapshots', event['proficiencyReceipt'] == master['proficiencyReceipt'] and not event['proficiencyReceipt']['conditional'])
        check(profile + '/real-separate-earned-payments', event['grant']['opportunity'] == 'Warrior:' + str(focus_level) and
              master['grant']['opportunity'] == 'Warrior:' + str(mastery_level) and
              all(o['spent'] for o in h.pay.opportunities.values()))
        check(profile + '/selection-grants-no-item-or-extra-proficiency', event['equipmentGranted'] == master['equipmentGranted'] == [] and
              event['proficiencyGranted'] == master['proficiencyGranted'] == [] and h.actor['physicalInventory'] == [])
        row = h.profile(profile); props = (row.get('sourceFields') or {}).get('Properties', row.get('profile', '')).lower()
        delivery = 'melee' if 'melee' in row['category'].lower() else 'thrown' if 'thrown' in props else 'projectile'
        adjustments = h.adjustments(profile, delivery)
        check(profile + '/chosen-profile-modifiers', adjustments == {
            'focusAttackBonus': 1, 'precisionThrowAttackBonus': 0, 'totalModeledFeatAttackBonus': 1,
            'flatDamageBonus': 0, 'criticalThreshold': 19, 'attackOrDamagePerformed': False})
        other = next(p for p in profiles if p != profile)
        other_row = h.profile(other); other_props = (other_row.get('sourceFields') or {}).get('Properties', other_row.get('profile', '')).lower()
        other_delivery = 'melee' if 'melee' in other_row['category'].lower() else 'thrown' if 'thrown' in other_props else 'projectile'
        check(profile + '/no-spill-to-another-profile', h.adjustments(other, other_delivery)['focusAttackBonus'] == 0 and
              h.adjustments(other, other_delivery)['criticalThreshold'] == 20)
        retained = deepcopy(h.pay.grants); payments = deepcopy(h.pay.opportunities)
        h.conditional_proficiency_state(profile, False)
        lost = h.adjustments(profile, delivery)
        check(profile + '/Focus-suppressed-Mastery-keeps-own-use-rule', lost['focusAttackBonus'] == 0 and lost['criticalThreshold'] == 19)
        check(profile + '/suppression-does-not-refund-or-erase', h.pay.grants == retained and h.pay.opportunities == payments)
        h.conditional_proficiency_state(profile, True)
        check(profile + '/same-receipt-restoration-no-repurchase', h.adjustments(profile, delivery) == adjustments and h.pay.grants == retained)
        for branch, kwargs in [('generic-improvised', {'retains_profile': False}), ('unavailable-profile', {'usable': False})]:
            result = h.adjustments(profile, delivery, **kwargs)
            check(profile + '/' + branch, result['focusAttackBonus'] == 0 and result['criticalThreshold'] == 20)
        if 'thrown' in props:
            check(profile + '/native-thrown-retains-choice', h.adjustments(profile, 'thrown')['focusAttackBonus'] == 1 and
                  h.adjustments(profile, 'thrown')['criticalThreshold'] == 19)
        check(profile + '/no-damage-or-resource-recovery', h.hp_current == start['hp']['current'] and h.rp_current == start['resources']['currentRP'])
        record('equipment/' + profile, start, h, modeledAttackModifiers=adjustments,
               usePremise='Conditional legal equipped attack; no physical item, attack or damage is created')

    sword = 'martial-melee-weapons.longsword'; axe = 'martial-melee-weapons.battleaxe'
    h = history(); opportunity(h, 4); before = h.snapshot(); h.acquire_profile('weaponFocus', 4, sword)
    opportunity(h, 8)
    rejection('same-Focus-profile-not-repeatable', h, lambda: h.acquire_profile('weaponFocus', 8, sword))
    h.acquire_profile('weaponFocus', 8, axe)
    check('different-Focus-profiles-separately-paid', [g['choice'] for g in h.pay.grants] == [sword, axe])
    check('two-Focus-grants-never-plus2-on-one-profile', h.adjustments(sword, 'melee')['focusAttackBonus'] == h.adjustments(axe, 'melee')['focusAttackBonus'] == 1)
    opportunity(h, 12); h.acquire_profile('weapon_mastery', 12, sword)
    opportunity(h, 16)
    rejection('Mastery-nonrepeatable-even-different-profile', h, lambda: h.acquire_profile('weapon_mastery', 16, axe))
    record('repeatability-distinction', before, h)
    h = history(); opportunity(h, 4)
    rejection('Mastery-before-total6-rejected', h, lambda: h.acquire_profile('weapon_mastery', 4, sword))
    h.advance(6)
    rejection('Warrior-level6-has-no-new-ASI', h, lambda: h.earn(6))
    rejection('no-invented-Warrior6-payment', h, lambda: h.acquire_profile('weapon_mastery', 6, sword))
    # An earlier legitimately unspent opportunity remains available at level6.
    before = h.snapshot(); h.acquire_profile('weapon_mastery', 4, sword)
    check('level6-may-spend-real-earlier-unspent-choice', h.events[-1]['totalCharacterLevel'] == 6 and h.pay.grants[-1]['opportunity'] == 'Warrior:4')
    record('real-delayed-opportunity-at-level6', before, h)
    h = history(); h.advance(4)
    rejection('no-earned-opportunity-no-Focus', h, lambda: h.acquire_profile('weaponFocus', 4, sword))
    h.earn(4)
    for invalid in [None, '', 'all weapons', 'all natural attacks', 'slashing', 'tools.smith-s-tools', [sword, axe]]:
        rejection('invalid-exact-choice/' + str(invalid), h, lambda p=invalid: h.acquire_profile('weaponFocus', 4, p))

    monk = deepcopy(actor)
    monk.update(firstClass='Monk', classLevels={'Monk': 1}, selectedClassSkills=['Acrobatics', 'Athletics'], classToolChoices=['tools.tinker-s-tools'])
    h = history(monk); opportunity(h, 4); before = h.snapshot(); event = h.acquire_profile('weaponFocus', 4, UNARMED)
    check('Monk-exact-unarmed-Focus-has-real-simple-proficiency', event['proficiencyReceipt']['grant'] == 'Monk/first-class-weapons' and not event['proficiencyReceipt']['conditional'])
    check('specific-unarmed-Focus-no-inventory-grant', h.adjustments(UNARMED, 'melee')['focusAttackBonus'] == 1 and h.actor['physicalInventory'] == [])
    check('specific-unarmed-is-not-every-weapon', h.adjustments('simple-melee-weapons.club', 'melee')['focusAttackBonus'] == 0)
    record('Monk-source-unarmed-Focus', before, h, scope='Specific unarmed Focus only; no general ruling on unarmed Mastery or all natural attacks')
    h = history(); opportunity(h, 4)
    rejection('Warrior-unarmed-proficiency-not-assumed', h, lambda: h.acquire_profile('weaponFocus', 4, UNARMED))

    troll = next(x for x in ancestry['ancestries'] if x['id'] == 'troll')
    claws = next(x for x in troll['traits'] if x['id'] == 'troll--claws')
    for sid in ['weaponFocus', 'weapon_mastery']:
        h = history(); opportunity(h, 8); before = h.snapshot()
        h.conditional_natural_body(claws)
        rejection(sid + '/natural-profile-alone-does-not-prove-proficiency', h, lambda: h.acquire_profile(sid, 8, claws['id']))
        h.conditional_natural_body(claws, {'profile': claws['id'], 'conditionalSeparatelyAuthorizedProficiency': True})
        event = h.acquire_profile(sid, 8, claws['id'])
        check(sid + '/explicit-conditional-natural-profile-preserved', event['proficiencyReceipt']['conditional'] and
              event['acquisitionProfile']['trait'] == claws)
        result = h.adjustments(claws['id'], 'melee')
        check(sid + '/conditional-exact-natural-use', result['focusAttackBonus'] == (1 if sid == 'weaponFocus' else 0) and
              result['criticalThreshold'] == (19 if sid == 'weapon_mastery' else 20))
        record(sid + '/conditional-specific-natural-profile', before, h,
               scope='Real Troll Claws text; conditional external body and independently authorized exact proficiency only. No actual ancestry, form, or proficiency grant is authenticated or created.')

    dagger = 'simple-melee-weapons.dagger'
    h = history(monk); opportunity(h, 4); h.acquire_profile('weaponFocus', 4, dagger)
    opportunity(h, 8); h.acquire_profile('weapon_mastery', 8, dagger)
    opportunity(h, 12); before = h.snapshot(); h.acquire_precision_throw(12)
    thrown = h.adjustments(dagger, 'thrown'); melee = h.adjustments(dagger, 'melee')
    check('Focus-plus-real-paid-PrecisionThrow-distinct-families', thrown['totalModeledFeatAttackBonus'] == 2 and melee['totalModeledFeatAttackBonus'] == 1)
    check('PrecisionThrow-adds-no-flat-damage', thrown['flatDamageBonus'] == 0)
    generic = h.adjustments(dagger, 'thrown', retains_profile=False)
    check('generic-object-does-not-inherit-Thrown-profile', generic['totalModeledFeatAttackBonus'] == 0 and generic['criticalThreshold'] == 20)
    fixed = deepcopy(h.pay.grants)
    h.pay.suppress('weaponFocus')
    check('Focus-suppression-does-not-suppress-Precision', h.adjustments(dagger, 'thrown')['totalModeledFeatAttackBonus'] == 1)
    h.pay.suppress('weaponFocus', False)
    check('Focus-restored-no-reacquisition', h.adjustments(dagger, 'thrown') == thrown and fixed == h.pay.grants)
    opportunity(h, 16)
    rejection('PrecisionThrow-duplicate-not-stacked', h, lambda: h.acquire_precision_throw(16))
    record('paid-Focus-Mastery-PrecisionThrow', before, h, melee=melee, thrown=thrown)

    # Deterministic Core hit classification for explicitly conditional legal
    # attacks: no action, inventory, die roller or downstream damage simulation.
    h = history(); opportunity(h, 4); h.acquire_profile('weaponFocus', 4, sword)
    opportunity(h, 8); h.acquire_profile('weapon_mastery', 8, sword); before = h.snapshot()
    mod = h.adjustments(sword, 'melee')
    outcomes = {}
    for label, die, ordinary, ac, hit, crit in [
        ('natural19-meets-AC', 19, 0, 20, True, True),
        ('natural19-misses-AC', 19, 0, 21, False, False),
        ('natural20-auto-hit', 20, -100, 100, True, True),
        ('natural1-auto-miss', 1, 100, 1, False, False),
        ('natural18-high-margin-not-critical', 18, 10, 10, True, False)]:
        result = resolve_kept_attack(die, ordinary, ac, mod); outcomes[label] = result
        check(label, result['hit'] == hit and result['critical'] == crit and not result['damageResolved'])
    for thresholds, expected in [([], 19), ([20], 19), ([19], 19), ([18], 18), ([18, 19], 18)]:
        result = h.adjustments(sword, 'melee', other_critical_thresholds=thresholds)
        check('conditional-critical-ranges/' + str(thresholds), result['criticalThreshold'] == expected)
    check('queries-have-no-mutation-or-damage', before == h.snapshot())
    record('Core-kept-die-and-range-comparison', before, h, outcomes=outcomes,
           scope='Other ranges are explicit conditional independently applicable effects, not new grants; no damage executed')
    check('bound-sources-unchanged', bindings == [info(p) for p in paths])
    report = {'createdAtUtc': datetime.now(timezone.utc).isoformat(),
        'status': 'weapon-profile-acquisition-and-bounded-modifier-pass',
        'checks': len(checks), 'failures': [], 'results': checks, 'sourceBindings': bindings,
        'cohort': ['weaponFocus', 'weapon_mastery'], 'supportingPaidFeat': 'precision_throw',
        'actorSourceProjection': actor, 'weaponProfiles': profiles, 'traces': traces,
        'counts': {'identities': 2, 'currentReviewedEquipmentProfiles': len(profiles),
            'WarriorClassProficiencyHistories': class_supported, 'paidWeaponMasterTrainingHistories': purchased_training,
            'sourceQualifiedUnarmedFocusHistories': 1, 'conditionalNaturalProfileHistories': 2,
            'recordedTraces': len(traces), 'newPartialPrerequisiteIdentities': 0},
        'limits': [
            'Source-derived Human/Imperial Warrior or Monk first-class/ASI/training slice, not a complete character or all class cards.',
            'All40 reviewed equipment profiles support actual paid Focus/Mastery selections. Monk specific unarmed Focus uses its actual Simple training and the retained exact unarmed profile.',
            'Troll Claws is a real preserved profile, but its two positive histories explicitly assume an external eligible body and separately authorized exact proficiency. Neither source is authenticated; no transformation or training is created.',
            'Specific unarmed Mastery is outside this pass, not declared illegal. No umbrella natural/unarmed or damage-type choice is created.',
            'Attack modifier queries assume legal equipment/body/actions/targets/ranges. No physical attack, damage, critical dice, resource trigger or full Precision Throw range execution is performed.',
            'Proficiency suppression/restoration and other critical ranges are conditional boundary premises, not new powers or authenticated campaign events.',
            'No all335-acquisition, exact assembled GPT, runtime, human balance, publication or cosmology approval claimed.'],
        'sourceInformationDeleted': False, 'newRulesAdopted': False, 'fullCandidateApproved': False}
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2, default=serial) + '\n', encoding='utf-8', newline='\n')
    notes.write_text('# Weapon Focus and Weapon Mastery choices\n\n'
        f'{len(checks)} checks passed across {len(traces)} recorded histories. All40 current reviewed equipment weapon profiles '
        'have actual permanent Focus/Mastery selections paid from real Warrior opportunities; Simple profiles first receive a separate paid Weapon Master grant. '
        'Distinct Focus repetition, nonrepeatable Mastery, total6 acquisition with an earlier unspent opportunity, and exact proficiency receipts are recorded.\n\n'
        'Focus requires operative proficiency at use; Mastery retains its own use predicates without importing that extra restriction. '
        'Loss/restoration preserves paid choices. Native melee/thrown profiles retain the choices; generic improvised use does not. '
        'A paid Precision Throw history adds its distinct attack bonus. Core natural19 must meet AC, natural20 automatically hits and critical ranges use the broadest eligible threshold. No damage is executed.\n\n'
        'Monk specific unarmed Focus has an actual Simple-training witness. Troll Claws positives are explicitly conditional on an external eligible body and independently authorized exact proficiency; those grants are not authenticated or created. '
        'Specific unarmed Mastery remains outside this evidence slice, not prohibited. Full equipment/action/body/range and damage interactions, remaining acquisition initialization and assembled GPT review remain open.\n', encoding='utf-8', newline='\n')
    print(json.dumps({'checks': len(checks), 'failures': 0, 'counts': report['counts'], 'report': info(output), 'notes': info(notes)}, indent=2))


if __name__ == '__main__':
    main()
