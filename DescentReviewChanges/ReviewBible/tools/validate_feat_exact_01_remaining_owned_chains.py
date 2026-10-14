"""Finite paid histories for Dark Binding, Trapcasting and Voltyros Pact.

Also checks Companion Training's independent Animal Handling branch and the
Berserker parent without claiming their other prerequisite branches complete.
"""
from collections import Counter
from copy import deepcopy
from datetime import datetime, timezone
from itertools import product
import json
from pathlib import Path
from feat_exact_01_casting_credential_model import CastingSources
from feat_exact_01_remaining_owned_chains import RemainingOwnedChains
from validate_feat_exact_01_composite_casting import read, info, serial

R = Path(__file__).resolve().parents[1]; G = R.parents[1]
A = G / 'docs/audit/2026-10-08/full-game'


def main():
    report_path = A / 'FEAT_EXACT_01_REMAINING_OWNED_CHAINS_CHECK.json'
    notes_path = A / 'FEAT_EXACT_01_REMAINING_OWNED_CHAINS_NOTES.md'
    assert not report_path.exists() and not notes_path.exists(), 'Preserve prior reports'
    paths = [Path(__file__), R / 'tools/feat_exact_01_remaining_owned_chains.py',
        R / 'tools/feat_exact_01_composite_casting_model.py', R / 'tools/feat_exact_01_casting_credential_model.py',
        R / 'tools/feat_exact_01_training_prerequisite_model.py', R / 'tools/feat_exact_01_initiate_acquisition_model.py',
        R / 'tools/feat_exact_01_acquisition_models.py', R / 'tools/validate_feat_exact_01_composite_casting.py',
        R / 'data/playtest/character_foundation.json', R / 'data/playtest/ancestry_background_candidate.json',
        R / 'data/playtest/equipment_source_catalog.json', R / 'data/public/class_playtests/wizard.json',
        R / 'data/public/feat_candidates/exact_01/spell_dependencies.json',
        R / 'data/public/feat_candidates/exact_01/supplements.json',
        R / 'data/public/feat_candidates/exact_01/shared_rules.json',
        A / 'FEAT_EXACT_01_ACQUISITION_CONTRACTS.json', A / 'FEAT_EXACT_01_INITIATE_ACQUISITION_CHECK.json',
        A / 'FEAT_EXACT_01_TINKERING_PROGRESSION_CHECK.json']
    bindings = [info(p) for p in paths]
    foundation = read(paths[8]); classes = {x['class']: x for x in foundation['classes']}
    skills = {s: a for a, group in foundation['skillAbilities'].items() for s in group}
    ancestry = read(paths[9]); backgrounds = {x['id']: x for x in ancestry['backgrounds']}
    equipment = {x['id']: x for x in read(paths[10])['records']}
    wizard = read(paths[11]); deps = read(paths[12])['spells']
    supplements = {x['id']: x['value'] for x in read(paths[13])['groups']}
    shared = {x['id']: x for x in read(paths[14])['rules']}
    contracts = {x['id']: x for x in read(paths[15])['records']}
    base_actor = read(paths[16])['actorSourceProjection']; previous = read(paths[17])
    sources = CastingSources(G, deps, supplements, wizard)
    human = next(x for x in ancestry['ancestries'] if x['id'] == 'human')
    imperial = next(x for x in human['variants'] if x['id'] == 'imperial-human')
    results = []; cases = []

    def check(label, truth, kind='paid-history'):
        results.append({'id': label, 'kind': kind, 'passed': bool(truth)})
        if not truth:
            raise AssertionError(label)

    def reject(label, h, operation):
        before = h.snapshot()
        try:
            operation()
        except (ValueError, KeyError) as exc:
            results.append({'id': label, 'kind': 'rejection', 'passed': True, 'reason': str(exc)})
        else:
            check(label, False, 'rejection')
        check(label + '/atomic', before == h.snapshot(), 'state-integrity')

    def history(nature=False, handling=False, academy=False, constitution=None):
        actor = deepcopy(base_actor)
        actor['firstClass'] = 'Warrior'; actor['classLevels'] = {'Warrior': 1}
        actor['selectedClassSkills'] = ['Nature' if nature else 'Animal Handling' if handling else 'Survival', 'Athletics']
        if academy:
            actor.update(background='arcane-academy-dropout', backgroundToolChoice=None, backgroundDuplicateSkillChoice=None)
        if constitution is not None:
            dice = next(d for d in product(range(1, 7), repeat=4)
                        if sum(d) - min(d) + imperial['combinedAbilityBonuses']['CON'] == constitution)
            actor['abilityRolls']['CON'] = list(dice); actor['permanentScores']['CON'] = constitution
        return RemainingOwnedChains(actor, classes, equipment, skills, ancestry, backgrounds, contracts, supplements, sources)

    def initiated(**kwargs):
        h = history(**kwargs); h.advance(4); h.earn(4); h.initiate()
        return h

    def capture(label, h, expectations):
        before = h.snapshot()
        for sid, expected in expectations.items():
            check(label + '/' + sid, h.prerequisite(sid) is expected, 'source-predicate')
        check(label + '/read-only', before == h.snapshot(), 'state-integrity')
        cases.append({'id': label, 'expectations': expectations, 'history': before})

    check('current-schedule-has-no-level6-bonus-feat', classes['Warrior']['asiClassLevels'] == [4, 8, 12, 16, 19], 'source-data')
    check('initial-finite-allowance-source', 'begins with its specified full finite allowance' in shared['FS-06']['wording'], 'source-data')
    for sid, excerpt in {
        'stormcaller': 'select the actual owned casting route at acquisition',
        'voltyros_pact': 'one actual casting ability selected at acquisition, or INT if no casting source',
        'trapcasting': 'Conjure Flora OR Verdant Bond qualifies for acquisition, but this feat supplies no missing plants',
        'dark_binding': 'Require Curse Channeling OR character 8',
        'conjure_flora': 'Choose its mode/burst type at creation',
    }.items():
        check('full-source-clause/' + sid, excerpt in contracts[sid]['completeOperativeProcedure'], 'source-data')

    # The total-level alternative is available with neither casting nor Curse Channeling.
    h = history(); h.advance(7)
    capture('Dark-level7-no-parent', h, {'dark_binding': False})
    reject('Dark-cannot-buy-before-level-or-parent', h, lambda: h.acquire_named('dark_binding', 4))
    h.advance(8)
    check('Dark-qualified-but-unearned', h.prerequisite('dark_binding') and not h.gate('dark_binding', 'Warrior:8'))
    h.earn(8); h.acquire_named('dark_binding', 8)
    check('Dark-no-weapon-or-curse-created', h.initializations['dark_binding'] == {'boundWeapon': None, 'bindingRitualCompleted': False})
    capture('Dark-level8-paid-without-parent', h, {'dark_binding': True})
    reject('Dark-spent-opportunity', h, lambda: h.acquire_named('lightning_affinity', 8))
    h.advance(12); h.earn(12)
    reject('Dark-nonrepeatable', h, lambda: h.acquire_named('dark_binding', 12))
    for route in ['Arcana', 'paid-casting']:
        h = history(academy=True) if route == 'Arcana' else initiated()
        h.advance(5); capture('Curse-' + route + '-level5', h, {'curse_channeling': False})
        h.advance(6); capture('Curse-' + route + '-level6', h, {'curse_channeling': True})
        reject('Curse-no-level6-opportunity-' + route, h, lambda: h.earn(6))
        h.advance(8); h.earn(8); h.acquire_named('curse_channeling', 8)
        check('Curse-zero-marks-' + route, h.initializations['curse_channeling']['marks'] == [])
        h.advance(12); h.remove_personal_routes(); h.earn(12); h.acquire_named('dark_binding', 12)
        capture('Dark-real-paid-parent-' + route, h, {'dark_binding': True})

    # Both named plant parents must themselves be earned with actual Nature AND casting.
    for parent in ['conjure_flora', 'verdant_bond']:
        h = history(nature=True); h.advance(4); h.earn(4)
        reject(parent + '-no-casting', h, lambda: h.acquire_named(parent, 4))
        h = initiated(); h.advance(8); h.earn(8)
        reject(parent + '-no-Nature', h, lambda: h.acquire_named(parent, 8))
        h = initiated(nature=True); h.advance(8); h.earn(8)
        capture('Trap-casting-and-Nature-without-parent-' + parent, h, {'trapcasting': False})
        h.acquire_named(parent, 8)
        check('Trap-parent-consumes-opportunity-' + parent, not h.gate('trapcasting', 'Warrior:8'))
        reject('Trap-cannot-share-parent-payment-' + parent, h, lambda: h.acquire_named('trapcasting', 8))
        before = deepcopy(h.initializations)
        h.advance(12); h.remove_personal_routes(); h.earn(12)
        capture('Trap-retained-parent-' + parent, h, {'trapcasting': True})
        h.acquire_named('trapcasting', 12)
        check('Trap-child-creates-no-new-resource-' + parent, 'trapcasting' not in h.initializations)
        if parent == 'conjure_flora':
            state = h.initializations[parent]
            check('Flora-capacity-growth-no-body-or-extra-use', state['plantCapacity'] == 2 and state['activePlants'] == [] and state['creationUses'] == before[parent]['creationUses'] and not state['additionalCreationPending'])
        else:
            check('Verdant-alone-no-conjured-flora', 'conjure_flora' not in h.initializations and h.initializations[parent] == before[parent])
        h.advance(16); h.earn(16)
        reject('Trap-nonrepeatable-' + parent, h, lambda: h.acquire_named('trapcasting', 16))

    # Nature-only Lightning Affinity legitimately permits INT fallback for Voltyros.
    h = history(nature=True); h.advance(4); h.earn(4); h.acquire_named('lightning_affinity', 4)
    check('Lightning-starts-with-no-stored-charges', h.initializations['lightning_affinity']['stormCharges'] == [])
    h.advance(5); capture('Voltyros-owned-parent-level5', h, {'voltyros_pact': False})
    h.advance(6); capture('Voltyros-owned-parent-level6', h, {'voltyros_pact': True})
    reject('Voltyros-level6-is-not-an-award', h, lambda: h.earn(6))
    h.advance(8); h.earn(8)
    for choice in [None, {'ability': 'CHA'}, {'ability': 'WIS'}, {'ability': 'INT', 'inventedRoute': True}]:
        reject('Voltyros-no-casting-invalid-choice-' + str(choice), h, lambda choice=choice: h.acquire_named('voltyros_pact', 8, choice))
    h.acquire_named('voltyros_pact', 8, {'ability': 'INT'})
    check('Voltyros-fixed-INT-full-one-use-no-weather', h.initializations['voltyros_pact'] == {
        'fixedAbility': 'INT', 'noCastingFallback': True, 'stormformUses': {'maximum': 1, 'current': 1},
        'eyeActive': False, 'stationaryInterval': None})
    capture('Voltyros-Nature-paid-Lightning-INT', h, {'voltyros_pact': True})
    h.advance(12); h.earn(12)
    reject('Voltyros-nonrepeatable', h, lambda: h.acquire_named('voltyros_pact', 12, {'ability': 'INT'}))
    h = initiated(nature=True); h.advance(8); h.earn(8)
    capture('Voltyros-no-parent-despite-Nature-and-casting', h, {'voltyros_pact': False})
    route = h.actual_casting_routes()[0]
    for choice in [None, {**route, 'grantId': 'unowned'}, {**route, 'ability': 'CHA'}, {'ability': 'INT'}]:
        reject('Storm-fixed-route-invalid-' + str(choice), h, lambda choice=choice: h.acquire_named('stormcaller', 8, choice))
    h.acquire_named('stormcaller', 8, route)
    check('Storm-two-separate-initial-pools', h.initializations['stormcaller']['staticFieldUses'] == {'maximum': 1, 'current': 1} and h.initializations['stormcaller']['stormstepUses'] == {'maximum': 1, 'current': 1})
    h.advance(12); h.earn(12)
    reject('Voltyros-present-casting-unowned-WIS', h, lambda: h.acquire_named('voltyros_pact', 12, {'ability': 'WIS'}))
    h.acquire_named('voltyros_pact', 12, {'ability': 'INT'})
    capture('Voltyros-paid-Stormcaller-actual-INT-route', h, {'voltyros_pact': True})
    check('Voltyros-real-route-not-fallback', not h.initializations['voltyros_pact']['noCastingFallback'])
    retained = deepcopy(h.initializations); h.remove_personal_routes()
    check('route-loss-keeps-fixed-acquisition-choices', h.initializations == retained and h.pay.has('stormcaller') and h.pay.has('voltyros_pact'))

    # A second real casting ability proves that the permanent choice is not always INT.
    h = history(nature=True); h.advance(4); h.earn(4); h.acquire_parent('forbidden_pact', 4, {'sigil': 'hex'})
    h.advance(8); h.earn(8); h.acquire_named('lightning_affinity', 8); h.advance(12); h.earn(12)
    reject('Voltyros-CHA-route-does-not-authorize-INT-fallback', h, lambda: h.acquire_named('voltyros_pact', 12, {'ability': 'INT'}))
    h.acquire_named('voltyros_pact', 12, {'ability': 'CHA'})
    capture('Voltyros-paid-Pact-Lightning-CHA', h, {'voltyros_pact': True})
    check('Voltyros-stored-CHA', h.initializations['voltyros_pact']['fixedAbility'] == 'CHA')

    # Independently useful branches; do not count these identities complete yet.
    h = history(handling=True); h.advance(4); h.earn(4); h.acquire_named('companion_training', 4)
    check('CompanionTraining-proficiency-creates-no-beast', h.initializations == {})
    capture('CompanionTraining-actual-first-class-proficiency', h, {'companion_training': True})
    h = history(); h.advance(4); h.earn(4)
    capture('CompanionTraining-no-proficiency-or-parent', h, {'companion_training': False})
    reject('CompanionTraining-no-credential', h, lambda: h.acquire_named('companion_training', 4))
    for score in [14, 15]:
        h = history(constitution=score); h.advance(4); h.earn(4)
        if score == 14:
            reject('Berserker-permanent-CON14', h, lambda: h.acquire_named('berserker', 4))
        else:
            h.acquire_named('berserker', 4)
            check('Berserker-CON15-one-initial-use-not-active', h.initializations['berserker'] == {'rageUses': {'maximum': 1, 'current': 1}, 'rageActive': False})
            capture('Berserker-paid-CON15-parent-only', h, {'berserker': True})

    cohort = {'dark_binding', 'trapcasting', 'voltyros_pact'}
    prior_remaining = {x['id'] for x in previous['remaining']}
    check('three-disjoint-new-partial-identities', len(prior_remaining) == 8 and cohort <= prior_remaining, 'coverage')
    remaining = [x for x in previous['remaining'] if x['id'] not in cohort]
    additional = [{'path': file, 'bytes': size, 'sha256': digest} for file, (size, digest, _) in sources.cache.items() if file not in {x['path'] for x in bindings}]
    for binding in bindings + additional:
        check('unchanged/' + binding['path'], info(G / binding['path']) == binding, 'source-integrity')
    report = {'createdAtUtc': datetime.now(timezone.utc).isoformat(), 'status': 'passed-finite-paid-remaining-owned-chains',
        'sourceBindings': bindings + additional, 'cohort': sorted(cohort),
        'completeSourceContracts': [contracts[sid] for sid in sorted(RemainingOwnedChains.IDS | {'forbidden_pact', 'magicInitiate'})],
        'counts': {'newPartialPrerequisiteIdentities': 3, 'cumulativePartialPrerequisiteIdentities': 330,
                   'remainingCredentialDependentIdentities': 5, 'recordedHistories': len(cases)},
        'cases': cases, 'checks': len(results), 'checkKinds': dict(Counter(x['kind'] for x in results)),
        'results': results, 'failures': [], 'remaining': remaining,
        'limits': [
            'Source-qualified conditional character slices; not real campaign acquisition, a complete character build or a feat-use runtime.',
            'Dark Binding paid Curse Channeling histories also satisfy level8. Supplied ordinary ASIs do not permit an independent below8 paid-parent witness; no extra award is invented.',
            'Companion Training covers the independent Animal Handling branch here. The paid Animal Companion branch and actual body/bond history remain outstanding; this identity is not added to the three-item cohort.',
            'Berserker parent payment and initial finite use are checked. Frenzied Rage and its class-feature alternative await ACQ-04 disposition; no new partial identity is counted for it.',
            'Fixed Stormcaller/Voltyros choices and named initial pools are represented; field, teleport, storm, lightning chain, plants, messages, cursed-weapon ritual and companion commands are not executed.',
            'No positive actual legacy Spellcraft history is supplied or created. Nature is the supplied Stormcaller alternative.',
            'Stored acquisition choices survive the explicit lawful-removal premise; ongoing use legality is not inferred from retained ownership.',
        ], 'all335CompleteAcquisitionsValidated': False, 'candidateReadyForSubmission': False,
        'newRulesAdopted': False, 'cosmologyReviewed': False, 'sourceInformationDeleted': False}
    with report_path.open('x', encoding='utf-8', newline='\n') as stream:
        json.dump(report, stream, ensure_ascii=False, indent=2, default=serial); stream.write('\n')
    with notes_path.open('x', encoding='utf-8', newline='\n') as stream:
        stream.write(f'''# Remaining paid feat chains\n\n{len(results)} checks pass across {len(cases)} captured source-qualified histories. Dark Binding preserves its independent level8 alternative; Trapcasting accepts either separately paid plant parent; Voltyros Pact retains its level6 AND named-parent prerequisite and actual permanent ability choice.\n\nStormcaller records an actual acquired casting route. Voltyros uses a real casting ability when present and INT only when none exists. Named finite allowances initialize once; Lightning Affinity starts with zero stored charges. No field, storm, curse, plant, animal or message is created by acquisition.\n\nThe Animal Handling branch of Companion Training and CON15 Berserker parent also pass, but their remaining child/ownership branches are not counted complete. Dark Binding's ordinary paid-parent histories also meet level8; no hypothetical earlier feat award is invented.\n\nThe disjoint partial prerequisite count is now330, with5 identities remaining. Full choices, actual-use procedures, whole-candidate review and software implementation remain separate. All bound source files are unchanged.\n''')
    print(json.dumps({'report': info(report_path), 'notes': info(notes_path), 'checks': len(results),
                      'histories': len(cases), 'failures': 0, 'partialIdentities': 330, 'remaining': len(remaining)}, indent=2))


if __name__ == '__main__':
    main()
