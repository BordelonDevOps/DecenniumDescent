"""Paid provider and parent histories for FAA01/02, without feat-use execution."""
from pathlib import Path
from copy import deepcopy
from datetime import datetime, timezone
import json
from feat_exact_01_flora_acquisition import FloraAcquisition
from feat_exact_01_remaining_owned_chains import RemainingOwnedChains
from feat_exact_01_initiate_acquisition_model import InitiateAcquisitions
from feat_exact_01_casting_credential_model import CastingSources
from validate_feat_exact_01_composite_casting import read, info, serial

R = Path(__file__).resolve().parents[1]
G = R.parents[1]
A = G / 'docs/audit/2026-10-08/full-game'


def main():
    output = A / 'FEAT335_FAA01_FAA02_PROVIDER_CHECK.json'
    assert not output.exists()
    paths = [R / 'data/playtest/character_foundation.json', R / 'data/playtest/ancestry_background_candidate.json',
             R / 'data/playtest/equipment_source_catalog.json', R / 'data/public/feat_candidates/exact_01/supplements.json',
             R / 'data/public/feat_candidates/exact_01/spell_dependencies.json', R / 'data/public/class_playtests/wizard.json',
             A / 'FEAT_EXACT_01_ACQUISITION_CONTRACTS.json', A / 'FEAT_EXACT_01_INITIATE_ACQUISITION_CHECK.json',
             R / 'data/director/magic_core_feat_operating_proposal_internal.json',
             R / 'data/public/feat_candidates/exact_01/shared_rules.json', Path(__file__),
             *[R / 'tools' / name for name in ['feat_exact_01_flora_acquisition.py', 'feat_exact_01_remaining_owned_chains.py',
                 'feat_exact_01_casting_selections.py', 'feat_exact_01_composite_casting_model.py',
                 'feat_exact_01_initiate_acquisition_model.py', 'feat_exact_01_casting_credential_model.py',
                 'feat_exact_01_training_prerequisite_model.py', 'feat_exact_01_acquisition_models.py']]]
    bindings = [info(p) for p in paths]
    foundation, ancestry, equipment_envelope, supplement_envelope, dependency_envelope, wizard, contract_envelope, prior, core_proposal = [read(p) for p in paths[:9]]
    classes = {c['class']: c for c in foundation['classes']}
    skills = {s: ability for ability, names in foundation['skillAbilities'].items() for s in names}
    equipment = {e['id']: e for e in equipment_envelope['records']}
    backgrounds = {b['id']: b for b in ancestry['backgrounds']}
    supplements = {s['id']: s['value'] for s in supplement_envelope['groups']}
    contracts = {c['id']: c for c in contract_envelope['records']}
    dependencies = dependency_envelope['spells']
    sources = CastingSources(G, dependencies, supplements, wizard)
    results, histories = [], []

    def check(label, result):
        results.append({'id': label, 'passed': bool(result)})
        assert result, label

    def reject(label, h, operation):
        before = h.snapshot()
        try:
            operation()
        except (ValueError, KeyError) as error:
            results.append({'id': label, 'passed': True, 'reason': str(error)})
        else:
            check(label, False)
        check(label + '/atomic', h.snapshot() == before)

    def make(curriculum=None, nature=True, attained=8, model=FloraAcquisition):
        actor = deepcopy(prior['actorSourceProjection'])
        actor.update(firstClass='Warrior', classLevels={'Warrior': 1},
                     selectedClassSkills=['Nature' if nature else 'Survival', 'Athletics'])
        h = model(actor, classes, equipment, skills, ancestry, backgrounds, contracts, supplements, sources)
        if isinstance(h, FloraAcquisition):
            h.configure_choice_sources(core_proposal)
        if curriculum:
            paid = InitiateAcquisitions(actor, classes, equipment, skills, ancestry, backgrounds, contracts, supplements['SUP-04'], dependencies)
            paid.advance(4); paid.earn(4)
            ability, cantrips, rank1 = prior['authoredCurriculumChoices'][curriculum]
            choice = {'curriculum': curriculum, 'cantrips': cantrips, 'rank1': rank1}
            paid.acquire('magicInitiate', 4, choice)
            h.advance(4); h.pay = paid.pay; h.casting.import_initiate(paid, 4)
            check(curriculum + '/actual-curriculum-ability', ability == supplements['SUP-04'][curriculum]['featCastingAbility'])
        h.advance(attained); h.earn(8)
        return h

    def record(label, h, **extra):
        histories.append({'id': label, 'state': h.snapshot(), **extra,
                          'scope': 'Source-qualified partial synthetic paid acquisition history, not a full character or real campaign.'})

    routes = [('Dragoon', 'STR'), ('Monk', 'DEX'), ('Thief', 'DEX'), ('Wizard', 'INT'), ('Cleric', 'WIS'), ('Bard', 'CHA')]
    for curriculum, ability in routes:
        h = make(curriculum)
        provider = h.actual_casting_routes()[0]
        check(curriculum + '/retained-route-is-actual-source', provider['ability'] == ability and provider['sourceClass'] == curriculum)
        check(curriculum + '/route-is-feat-not-new-class', h.pay.current_classes == {'Warrior': 8})
        for label, choice in [('missing', None), ('unowned', {**provider, 'grantId': 'not-earned'}),
                              ('invented-CON', {**provider, 'ability': 'CON'}), ('bare-ability', {'ability': ability}),
                              ('wrong-source', {**provider, 'sourceClass': 'Invented'})]:
            reject(curriculum + '/Flora/' + label, h, lambda choice=choice: h.acquire_named('conjure_flora', 8, choice))
        casting_before = h.casting.snapshot()
        h.casting.use_state.update(rp=0, temporaryBlocks=['conditional-Incapacitated'])
        blocked_before = h.casting.snapshot()
        h.acquire_named('conjure_flora', 8, provider)
        flora = h.initializations['conjure_flora']
        check(curriculum + '/complete-Flora-initial-state', flora == {'fixedCastingRoute': provider,
            'creationUses': {'maximum': 1, 'current': 1}, 'plantCapacity': 1, 'activePlants': [], 'additionalCreationPending': False})
        check(curriculum + '/no-cast-resource-or-block-change', h.casting.snapshot() == blocked_before)
        check(curriculum + '/DC-from-actual-current-stat', h.flora_dc_projection()['dc'] == 8 + 3 + (h.pay.scores[ability] - 10) // 2)
        reject(curriculum + '/parent-payment-not-child-payment', h, lambda: h.acquire_named('trapcasting', 8))
        flora['creationUses']['current'] = 0  # Explicit conditional prior spending, no plant-use execution.
        h.advance(10)
        check(curriculum + '/capacity-growth-no-refill', flora['plantCapacity'] == 2 and flora['creationUses']['current'] == 0 and not flora['activePlants'])
        h.advance(12); h.earn(12); h.remove_personal_routes()
        initial_before_child = deepcopy(h.initializations)
        h.acquire_named('trapcasting', 12)
        check(curriculum + '/paid-Trapcasting-retains-complete-parent-without-use-grant', h.initializations == initial_before_child and
              h.pay.has('trapcasting') and h.initializations['conjure_flora']['fixedCastingRoute'] == provider)
        record(curriculum + '/Flora-to-Trapcasting', h, conditionalPriorUse='Creation allowance spent conditionally to verify growth does not refill; no creation was simulated.')

        h = make(curriculum, nature=False)
        reject(curriculum + '/Flora-still-requires-Nature', h, lambda: h.acquire_named('conjure_flora', 8, h.actual_casting_routes()[0]))
        h = make(curriculum)
        provider = h.actual_casting_routes()[0]
        reject(curriculum + '/Storm-missing-provider', h, lambda: h.acquire_named('stormcaller', 8))
        h.acquire_named('stormcaller', 8, provider)
        check(curriculum + '/Storm-source-and-separate-empty-output', h.initializations['stormcaller'] == {
            'fixedCastingRoute': provider, 'staticFieldUses': {'maximum': 1, 'current': 1},
            'stormstepUses': {'maximum': 1, 'current': 1}, 'activeFields': [], 'afterimage': None})
        h.advance(12); h.earn(12)
        wrong = 'INT' if ability != 'INT' else 'DEX'
        reject(curriculum + '/Voltyros-no-false-fallback-or-unowned-choice', h, lambda: h.acquire_named('voltyros_pact', 12, {'ability': wrong}))
        h.acquire_named('voltyros_pact', 12, {'ability': ability})
        check(curriculum + '/Voltyros-actual-source-not-fallback', h.initializations['voltyros_pact']['fixedAbility'] == ability and not h.initializations['voltyros_pact']['noCastingFallback'])
        h.advance(16); h.earn(16)
        h.acquire_casting_selection('telekinetic', 16, {'ability': 'CHA' if ability != 'CHA' else 'INT'})
        check(curriculum + '/later-route-never-reselects-fixed-ability', h.initializations['voltyros_pact']['fixedAbility'] == ability)
        record(curriculum + '/Stormcaller-to-Voltyros', h)

        h = make(curriculum)
        provider = h.providers()[0]
        reject(curriculum + '/Soul-Cage-guessed-provider', h, lambda: h.acquire_casting_selection('soul_cage', 8, {'provider': {**provider, 'ability': 'CON'}}))
        cast_before = h.casting.snapshot()
        h.acquire_casting_selection('soul_cage', 8, {'provider': provider})
        check(curriculum + '/Soul-Cage-fixed-route-empty-pool-no-crystal', h.initializations['soul_cage'] == {'fixedProvider': provider, 'actualBlackCrystalRef': None} and
              h.initializations['sharedSoulCharges'] == {'maximum': 3, 'current': 0, 'evaluatedDeathEvents': [], 'bodyEpochEntitlements': []} and h.casting.snapshot() == cast_before)
        record(curriculum + '/Soul-Cage-provider', h)

    # Saved older opportunities must use current attained total for capacity in both entry points.
    for model in [RemainingOwnedChains, FloraAcquisition]:
        for attained in [9, 10, 12]:
            h = make('Dragoon', attained=attained, model=model)
            provider = h.actual_casting_routes()[0]
            h.acquire_named('conjure_flora', 8, provider)
            check(model.__name__ + '/saved-opportunity-at-level' + str(attained),
                  h.initializations['conjure_flora']['plantCapacity'] == (2 if attained >= 10 else 1) and h.initializations['conjure_flora']['fixedCastingRoute'] == provider)
            record(model.__name__ + '/saved-opportunity/' + str(attained), h)

    h = make('Wizard')
    h.acquire_named('verdant_bond', 8)
    parent = deepcopy(h.initializations)
    h.advance(12); h.earn(12); h.remove_personal_routes(); h.acquire_named('trapcasting', 12)
    check('Verdant-only-parent-retained-without-Flora-or-provider-menu', h.initializations == parent and 'conjure_flora' not in h.initializations)
    record('Verdant-only-to-Trapcasting', h)
    h = make()
    reject('Flora-no-casting-cannot-create-default-Wisdom', h, lambda: h.acquire_named('conjure_flora', 8, {'ability': 'WIS'}))
    h.acquire_named('lightning_affinity', 8); h.advance(12); h.earn(12)
    reject('Nature-only-Voltyros-rejects-DEX', h, lambda: h.acquire_named('voltyros_pact', 12, {'ability': 'DEX'}))
    h.acquire_named('voltyros_pact', 12, {'ability': 'INT'})
    check('True-no-casting-fallback-kept', h.initializations['voltyros_pact']['fixedAbility'] == 'INT' and h.initializations['voltyros_pact']['noCastingFallback'])
    record('Nature-only-Lightning-to-Voltyros-fallback', h)

    # The general provider fix must not widen explicitly narrower feat menus.
    h = make('Dragoon')
    for sid in ['arcane_pulse', 'feyTouched', 'shadow_touched', 'telekinetic', 'telepathic', 'ritual_caster', 'hemocraft']:
        for forbidden in ['STR', 'DEX']:
            choice = {'ability': forbidden}
            if sid in {'feyTouched', 'shadow_touched'}:
                choice['rank1'] = {'spellId': 'unused-before-ability-admission', 'school': 'Universal', 'sourceClass': 'Wizard'}
            reject(sid + '/retained-explicit-menu/' + forbidden, h, lambda sid=sid, choice=choice: h.acquire_casting_selection(sid, 8, choice))
    check('Seven-narrow-menus-never-consume-opportunity', not h.pay.opportunities['Warrior:8']['spent'])
    record('Narrow-menus-remain-narrow', h)
    for before in bindings:
        check('Source-preserved/' + before['path'], info(G / before['path']) == before)
    result = {'recordedAtUtc': datetime.now(timezone.utc).isoformat(), 'findings': ['FAA-01', 'FAA-02'],
        'acceptanceGroups': ['AA-01', 'AA-02', 'AA-03', 'AA-04'], 'status': 'Passed bounded source-qualified provider and paid-parent acquisition histories.',
        'checks': len(results), 'failures': [], 'results': results, 'histories': histories, 'sourceBindings': bindings,
        'counts': {'actualCurricula': 6, 'physicalAbilityCurricula': 3, 'distinctActualAbilities': 5, 'affectedProviderInterfaces': 4,
                   'recordedHistories': len(histories), 'explicitNarrowMenusPreserved': 7},
        'limits': ['Partial synthetic class/feat histories, not complete character builds or authenticated campaigns.',
                   'Conditional spent Flora allowance verifies no refill; no plants, trap, field, crystal, body, cast, rest or damage is executed.',
                   'Fixed provider preservation after route loss proves historical acquisition only, not ongoing operation without actual use predicates.',
                   'The full335 feat candidate and other initial-state/use gates remain open.'],
        'newGameRules': 0, 'fullFeatCandidateApproved': False, 'sourceInformationDeleted': 0}
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2, default=serial) + '\n', encoding='utf-8')
    print(json.dumps({'report': info(output), 'checks': len(results), 'histories': len(histories), 'failures': 0}, indent=2))


if __name__ == '__main__':
    main()
