"""All finite acquisition menus for five martial/metamagic/elemental feats."""
from copy import deepcopy
from datetime import datetime, timezone
from itertools import combinations
import json
from pathlib import Path
from feat_exact_01_fixed_menus import FixedMenus, ELEMENTS, METAMAGIC, IDS
from feat_exact_01_casting_credential_model import CastingSources
from validate_feat_exact_01_composite_casting import read, info, serial

R = Path(__file__).resolve().parents[1]; G = R.parents[1]
A = G / 'docs/audit/2026-10-08/full-game'


def main():
    target = A / 'FEAT_EXACT_01_FIXED_MENUS_CHECK.json'
    notes = A / 'FEAT_EXACT_01_FIXED_MENUS_NOTES.md'
    assert not target.exists() and not notes.exists()
    source_paths = {
        'foundation': R / 'data/playtest/character_foundation.json',
        'ancestry': R / 'data/playtest/ancestry_background_candidate.json',
        'equipment': R / 'data/playtest/equipment_source_catalog.json',
        'wizard': R / 'data/public/class_playtests/wizard.json',
        'mage': R / 'data/public/class_playtests/mage.json',
        'dependencies': R / 'data/public/feat_candidates/exact_01/spell_dependencies.json',
        'supplements': R / 'data/public/feat_candidates/exact_01/supplements.json',
        'shared': R / 'data/public/feat_candidates/exact_01/shared_rules.json',
        'contracts': A / 'FEAT_EXACT_01_ACQUISITION_CONTRACTS.json',
        'actor': A / 'FEAT_EXACT_01_INITIATE_ACQUISITION_CHECK.json',
        'currentPublic': R / 'data/public/feat_candidates/exact_01/candidate.json',
        'currentInternal': R / 'data/director/feat_candidates/exact_01/candidate.json'}
    paths = list(source_paths.values()) + [Path(__file__)]
    paths += [R / 'tools' / n for n in ['feat_exact_01_fixed_menus.py', 'feat_exact_01_remaining_owned_chains.py',
        'feat_exact_01_composite_casting_model.py', 'feat_exact_01_casting_credential_model.py',
        'feat_exact_01_training_prerequisite_model.py', 'feat_exact_01_acquisition_models.py',
        'feat_exact_01_initiate_acquisition_model.py', 'validate_feat_exact_01_composite_casting.py']]
    bindings = [info(p) for p in paths]
    foundation = read(source_paths['foundation']); classes = {x['class']: x for x in foundation['classes']}
    skills = {s: a for a, group in foundation['skillAbilities'].items() for s in group}
    ancestry = read(source_paths['ancestry']); backgrounds = {x['id']: x for x in ancestry['backgrounds']}
    equipment = {x['id']: x for x in read(source_paths['equipment'])['records']}
    supplements = {x['id']: x['value'] for x in read(source_paths['supplements'])['groups']}
    dependencies = read(source_paths['dependencies'])['spells']
    sources = CastingSources(G, dependencies, supplements, read(source_paths['wizard']))
    contracts = {x['id']: x for x in read(source_paths['contracts'])['records']}
    actor_source = read(source_paths['actor'])['actorSourceProjection']
    maneuvers = [r['id'] for r in supplements['SUP-03']]
    results = []; traces = []; seen_base = set(); seen_advanced = set(); seen_modes = set(); seen_elements = set()

    def check(label, truth):
        results.append({'id': label, 'passed': bool(truth)})
        if not truth:
            raise AssertionError(label)

    def capture(label, h, premises=None):
        traces.append({'id': label, 'state': h.snapshot(), 'conditionalPremises': premises or [],
            'scope': 'Source-qualified acquisition/initialization slice; not a complete class build or authenticated campaign.'})

    def reject(label, h, call):
        before = h.snapshot()
        try:
            call()
        except (ValueError, KeyError) as error:
            check(label, True); results[-1]['rejection'] = str(error)
        else:
            check(label, False)
        check(label + '/atomic-rejection', h.snapshot() == before)

    def history(first='Warrior', level=4, earned=True):
        actor = deepcopy(actor_source)
        actor.update(firstClass=first, classLevels={first: 1}, selectedClassSkills=['Animal Handling', 'Athletics'])
        if first == 'Wizard':
            actor['selectedClassSkills'] = ['Insight', 'Investigation']
            actor['scope'] = 'Explicit ability/class-level/repertoire subset; no full Wizard book or class-card acquisition history claimed.'
        h = FixedMenus(actor, classes, equipment, skills, ancestry, backgrounds, contracts, supplements, sources)
        h.advance(level)
        if earned:
            h.earn(level)
        return h

    def wizard(level=8, prepared=True, rank3=True):
        h = history('Wizard', level)
        h.wizard(['friends', 'arcane-ray'], ['dispel-magic'] if rank3 else ['find-familiar'],
            ['dispel-magic'] if rank3 and prepared else [])
        return h

    def initiate():
        h = history(); h.initiate(); h.advance(8); h.earn(8); return h

    check('six-distinct-finite-maneuvers', len(maneuvers) == len(set(maneuvers)) == 6)
    check('exact-three-mode-source', all(name + ':' in contracts['metamagicAdept']['completeOperativeProcedure'] for name in METAMAGIC))
    check('five-element-source-menu', all('acid,cold,fire,lightning or thunder' in contracts[sid]['completeOperativeProcedure'] for sid in ['elementalAdept', 'elemental_mastery']))
    for base in combinations(maneuvers, 2):
        seen_base.add(base)
        for advanced in combinations([x for x in maneuvers if x not in base], 2):
            seen_advanced.add((base, advanced))
            for previously_spent in [False, True]:
                h = history(); before_casting = deepcopy(h.casting.snapshot())
                h.acquire_menu('martialAdept', 4, list(base))
                p = h.initializations['feat_superiority']
                check('base/' + str(base) + '/initial-one-d6/' + str(previously_spent) + str(advanced), (p['maximum'], p['current'], p['dieSides']) == (1, 1, 6))
                premises = []
                if previously_spent:
                    p['current'] = 0
                    premises.append('An earlier genuinely legal committed maneuver spent the original die. Its attack/task/action outcome is outside this acquisition slice; no refund or recharge is assumed.')
                h.advance(8); h.earn(8)
                check('growth-does-not-refill/' + str((base, advanced, previously_spent)), p['current'] == (0 if previously_spent else 1))
                h.acquire_menu('martial_adept_advanced', 8, list(advanced)); p = h.initializations['feat_superiority']
                check('advanced-four-distinct/' + str((base, advanced, previously_spent)), set(p['maneuvers']) == set(base + advanced) and len(p['maneuvers']) == 4)
                check('only-new-die-available/' + str((base, advanced, previously_spent)), (p['maximum'], p['current'], p['dieSides']) == (2, 1 if previously_spent else 2, 6))
                check('two-separate-actual-opportunities/' + str((base, advanced, previously_spent)), [x['opportunity'] for x in h.pay.grants] == ['Warrior:4', 'Warrior:8'])
                check('no-casting-or-class-grant/' + str((base, advanced, previously_spent)), h.casting.grants == before_casting['grants'] and set(h.pay.current_classes) == {'Warrior'})
                capture('martial/' + str((base, advanced, previously_spent)), h, premises)
    check('all15base-and90advanced-combinations', len(seen_base) == 15 and len(seen_advanced) == 90)
    for sid in ['martialAdept', 'martial_adept_advanced']:
        for bad in [None, [], [maneuvers[0]], [maneuvers[0], maneuvers[0]], maneuvers[:3], ['class-Battle-Master', maneuvers[1]], 'two maneuvers']:
            h = history()
            if sid == 'martial_adept_advanced':
                h.acquire_menu('martialAdept', 4, maneuvers[:2]); h.advance(8); h.earn(8)
            reject(sid + '/invalid/' + str(bad), h, lambda: h.acquire_menu(sid, 8 if sid.endswith('advanced') else 4, bad))
        h = history(); h.acquire_menu('martialAdept', 4, maneuvers[:2]); h.advance(8); h.earn(8)
        if sid.endswith('advanced'):
            reject('advanced-cannot-duplicate-parent-choice', h, lambda: h.acquire_menu(sid, 8, [maneuvers[0], maneuvers[2]]))
            h.acquire_menu(sid, 8, maneuvers[2:4]); h.advance(12); h.earn(12)
            reject('advanced-nonrepeatable', h, lambda: h.acquire_menu(sid, 12, maneuvers[4:6]))
        else:
            reject('base-nonrepeatable-different-menu', h, lambda: h.acquire_menu(sid, 8, maneuvers[2:4]))
        capture(sid + '/nonrepeatable', h)
    h = history(); reject('advanced-without-parent', h, lambda: h.acquire_menu('martial_adept_advanced', 4, maneuvers[:2]))
    h = history(earned=False); reject('base-without-earned-payment', h, lambda: h.acquire_menu('martialAdept', 4, maneuvers[:2]))
    h = history(); h.acquire_menu('martialAdept', 4, maneuvers[:2])
    reject('parent-and-child-cannot-share-opportunity', h, lambda: h.acquire_menu('martial_adept_advanced', 4, maneuvers[2:4]))

    for modes in combinations(METAMAGIC, 2):
        seen_modes.add(modes)
        for route in ['paid-Initiate', 'current-Wizard']:
            h = initiate() if route == 'paid-Initiate' else wizard()
            prior_casting = deepcopy(h.casting.snapshot()); prior_scores = deepcopy(h.pay.scores)
            h.casting.use_state['rp'] = 0
            h.acquire_menu('metamagicAdept', 8, list(modes))
            p = h.initializations['metamagicAdept']
            check(route + str(modes) + '/initial-two-points-fixed-choices', p['modes'] == list(modes) and p['sorceryPoints'] == {'maximum': 2, 'current': 2})
            check(route + str(modes) + '/no-Mage-RP-or-score-grant', not p['classMetaspellGranted'] and 'Mage' not in h.pay.current_classes and h.casting.use_state['rp'] == 0 and h.pay.scores == prior_scores)
            check(route + str(modes) + '/no-new-spell-access', h.casting.grants == prior_casting['grants'])
            h.initializations['metamagicAdept']['sorceryPoints']['current'] = 0
            h.advance(12); h.earn(12)
            check(route + str(modes) + '/growth-no-refill', h.initializations['metamagicAdept']['sorceryPoints']['current'] == 0)
            reject(route + str(modes) + '/nonrepeatable', h, lambda: h.acquire_menu('metamagicAdept', 12, ['Reach', 'Sculpt']))
            capture(route + '/metamagic/' + str(modes), h, ['Two earlier legally committed mode uses spent both points; cast legality/damage/refund behavior is not executed in this acquisition pass.'])
    check('three-mode-pairs', len(seen_modes) == 3)
    for bad in [None, [], ['Reach'], ['Reach', 'Reach'], ['Reach', 'Widen', 'Sculpt'], ['Quickened', 'Subtle'], ['Reach', 'class-Metaspell']]:
        h = initiate(); reject('invalid-mode-menu/' + str(bad), h, lambda: h.acquire_menu('metamagicAdept', 8, bad))
    h = history(); reject('no-personal-spellcasting', h, lambda: h.acquire_menu('metamagicAdept', 4, ['Reach', 'Widen']))
    h = history('Wizard', 3, earned=False); h.wizard(['friends'], ['find-familiar'], [])
    check('total3-before-metamagic-gate', not h.prerequisite('metamagicAdept'))
    h.advance(4); h.earn(4); h.acquire_menu('metamagicAdept', 4, ['Reach', 'Sculpt'])
    check('actual-Wizard4-earliest-earned-gate', h.pay.grants[-1]['opportunity'] == 'Wizard:4'); capture('Wizard3-to4-metamagic', h)

    for sid in ['elementalAdept', 'elemental_mastery']:
        for element in ELEMENTS:
            seen_elements.add((sid, element)); h = initiate() if sid == 'elementalAdept' else wizard()
            prior = deepcopy(h.casting.snapshot()); h.casting.use_state['rp'] = 0
            h.acquire_menu(sid, 8, element)
            check(sid + '/' + element + '/fixed-type-only', h.initializations[sid] == {'chosenDamageType': element})
            check(sid + '/' + element + '/no-new-cast-or-resource', h.casting.grants == prior['grants'] and h.casting.use_state['rp'] == 0)
            h.advance(12); h.earn(12)
            reject(sid + '/' + element + '/nonrepeatable-other-type', h, lambda: h.acquire_menu(sid, 12, ELEMENTS[(ELEMENTS.index(element) + 1) % 5]))
            capture(sid + '/' + element, h)
        for bad in [None, 'force', 'necrotic', 'poison', 'radiant', ['fire', 'cold'], 'all-elements', 'Fire']:
            h = wizard(); reject(sid + '/invalid/' + str(bad), h, lambda: h.acquire_menu(sid, 8, bad))
    check('all-ten-elemental-menu-entries', len(seen_elements) == 10)
    h = history(); reject('elemental-adept-no-casting', h, lambda: h.acquire_menu('elementalAdept', 4, 'fire'))
    for h, label in [(initiate(), 'rank1-not-rank3'), (wizard(prepared=False), 'unprepared-rank3-not-access'), (wizard(rank3=False), 'capacity-not-learned-rank3')]:
        reject(label, h, lambda: h.acquire_menu('elemental_mastery', 8, 'cold')); capture(label, h)
    h = wizard(); h.acquire_menu('elementalAdept', 8, 'fire'); h.advance(12); h.earn(12)
    h.acquire_menu('elemental_mastery', 12, 'cold')
    check('separate-feats-separate-fixed-types-and-payments', h.initializations['elementalAdept']['chosenDamageType'] == 'fire' and h.initializations['elemental_mastery']['chosenDamageType'] == 'cold' and [g['opportunity'] for g in h.pay.grants] == ['Wizard:8', 'Wizard:12'])
    capture('independent-elemental-choices', h)
    for bound in bindings:
        check('unchanged/' + bound['path'], info(G / bound['path']) == bound)
    limits = [
        'This is finite permanent selection/payment/initialization evidence, not complete five-feat use or all335 acquisitions.',
        'The Warrior/paid-Initiate histories use actual class schedules and training projections. Wizard witnesses are explicit ability/class-level/repertoire subsets; a complete book/class-card acquisition history is not claimed.',
        'Prepared reviewed Dispel Magic establishes the Wizard rank3 access witness. Sufficient RP, total level, an unprepared entry or rank1 Initiate access does not.',
        'Previously spent superiority dice and sorcery points are explicit conditional prior-use premises. This pass does not execute maneuver actions, cast commitment, attack/task outcomes, beneficial-rest recovery or refund rules.',
        'Elemental damage conversion/resistance/die-floor effects and stacking with actual spell packets remain use-procedure work. Metamagic range/area/save effects, Mage source arbitration and spell costs remain separate.',
        'No class feature, animal, physical item, extra resource pool, spell access, source promotion, actual campaign event, human balance or software implementation is created.']
    report = {'createdAtUtc': datetime.now(timezone.utc).isoformat(), 'status': 'passed-five-fixed-acquisition-menus',
        'checks': len(results), 'failures': [], 'results': results, 'sourceBindings': bindings, 'cohort': sorted(IDS),
        'completeProcedures': {sid: contracts[sid]['completeOperativeProcedure'] for sid in IDS},
        'completeManeuverMenu': supplements['SUP-03'], 'traces': traces, 'limits': limits,
        'counts': {'identities': 5, 'baseManeuverPairs': len(seen_base), 'advancedPairCombinations': len(seen_advanced),
            'martialHistoriesWithAvailableAndSpentParents': 180, 'metamagicPairs': len(seen_modes),
            'elementalMenuEntries': len(seen_elements), 'recordedTraces': len(traces), 'newPartialPrerequisiteIdentities': 0},
        'sourceInformationDeleted': False, 'newRulesAdopted': False, 'fullCandidateApproved': False}
    with target.open('x', encoding='utf-8', newline='\n') as f:
        json.dump(report, f, ensure_ascii=False, indent=2, default=serial); f.write('\n')
    with notes.open('x', encoding='utf-8', newline='\n') as f:
        f.write('# Martial, metamagic and elemental permanent choices\n\n')
        f.write(f'{len(results)} checks pass across{len(traces)} captured histories. All15 base maneuver pairs and90 legal Advanced extensions are covered with both an available and a spent parent die. The newly granted die adds one current use without refilling the old die. All3 metamagic mode pairs and10 elemental selections are covered.\n\n')
        for limit in limits:
            f.write('- ' + limit + '\n')
    print(json.dumps({'report': info(target), 'notes': info(notes), 'checks': len(results), 'traces': len(traces), 'failures': 0}, indent=2))


if __name__ == '__main__':
    main()
