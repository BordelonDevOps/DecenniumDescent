"""Execute all sixteen actual GPT ACQ-04 expectation groups with bound fixtures.

No fixture is a campaign record. Immutable content-addressed JSON records live
only in the audit fixture directory and never become selectable game content.
"""
from copy import deepcopy
from datetime import datetime, timezone
from hashlib import sha256
from itertools import product
import json
from pathlib import Path
from feat_exact_01_external_credential_model import ExternalCredentialEvidence, acquisition_gate
from feat_exact_01_remaining_owned_chains import RemainingOwnedChains
from feat_exact_01_casting_credential_model import CastingSources
from validate_feat_exact_01_composite_casting import read, info, serial

R = Path(__file__).resolve().parents[1]; G = R.parents[1]
A = G / 'docs/audit/2026-10-08/full-game'
FIXTURES = A / 'feat327-acq04-conditional-fixtures'


class ImmutableFixtures:
    def __init__(self):
        self.paths = set()

    def put(self, value):
        data = (json.dumps(value, ensure_ascii=False, indent=2, default=serial) + '\n').encode()
        digest = sha256(data).hexdigest(); path = FIXTURES / (digest + '.json')
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists():
            assert path.read_bytes() == data
        else:
            with path.open('xb') as f:
                f.write(data)
        self.paths.add(path)
        return {'path': path.relative_to(G).as_posix(), 'sha256': digest, 'pointer': ''}


def main():
    output = A / 'FEAT327_ACQ_04_EXTERNAL_CREDENTIAL_CHECK.json'
    notes = A / 'FEAT327_ACQ_04_EXTERNAL_CREDENTIAL_NOTES.md'
    assert not output.exists() and not notes.exists(), 'Do not overwrite immutable acceptance evidence'
    paths = [Path(__file__), R / 'tools/feat_exact_01_external_credential_model.py',
        R / 'tools/feat_exact_01_remaining_owned_chains.py', R / 'tools/feat_exact_01_composite_casting_model.py',
        R / 'tools/feat_exact_01_training_prerequisite_model.py', R / 'tools/feat_exact_01_acquisition_models.py',
        R / 'tools/feat_exact_01_casting_credential_model.py', R / 'tools/feat_exact_01_initiate_acquisition_model.py',
        R / 'tools/validate_feat_exact_01_composite_casting.py',
        R / 'data/playtest/character_foundation.json', R / 'data/playtest/ancestry_background_candidate.json',
        R / 'data/playtest/equipment_source_catalog.json', R / 'data/public/class_playtests/wizard.json',
        R / 'data/public/feat_candidates/exact_01/spell_dependencies.json', R / 'data/public/feat_candidates/exact_01/supplements.json',
        R / 'data/public/feat_candidates/exact_01/shared_rules.json',
        A / 'FEAT_EXACT_01_ACQUISITION_CONTRACTS.json', A / 'FEAT_EXACT_01_INITIATE_ACQUISITION_CHECK.json',
        A / 'FEAT_EXACT_01_REMAINING_OWNED_CHAINS_CHECK.json', A / 'FEAT327_ACQ_04_EXTERNAL_CREDENTIAL_POLICY.json',
        A / 'FEAT327_ACQ_04_INDEPENDENT_DESCENDANT_CHECK.json', A / 'FEAT327_ACQ_04_DERIVED_OPERATIONS.json',
        A / 'feat327-acq04-source/ACQ04_ACCEPTANCE_CASES.json', A / 'feat327-acq04-source/BOUND_SOURCE_EXCERPTS.json',
        A / 'feat327-acq04-source/SUBMITTED_PACKAGE_MANIFEST.json']
    bindings = [info(p) for p in paths]
    foundation = read(paths[9]); classes = {x['class']: x for x in foundation['classes']}
    skills = {s: ability for ability, group in foundation['skillAbilities'].items() for s in group}
    ancestry = read(paths[10]); backgrounds = {x['id']: x for x in ancestry['backgrounds']}
    equipment = {x['id']: x for x in read(paths[11])['records']}
    supplements = {x['id']: x['value'] for x in read(paths[14])['groups']}
    sources = CastingSources(G, read(paths[13])['spells'], supplements, read(paths[12]))
    contracts_document = read(paths[16]); contracts = {x['id']: x for x in contracts_document['records']}
    base_actor = read(paths[17])['actorSourceProjection']; previous = read(paths[18]); policy = read(paths[19])
    expectations = read(paths[22])['cases']; excerpts = read(paths[23])['references']
    store = ImmutableFixtures(); results = []; cases = []; groups = {x['id']: [] for x in expectations}
    imperial = next(v for a in ancestry['ancestries'] if a['id'] == 'human' for v in a['variants'] if v['id'] == 'imperial-human')

    def bound(path, pointer=''):
        return {'path': path.relative_to(G).as_posix(), 'sha256': info(path)['sha256'], 'pointer': pointer}

    contract_refs = {sid: bound(paths[16], '/records/' + str(i)) for i, row in enumerate(contracts_document['records']) if (sid := row['id']) in policy['dispositions']}
    rage_ids = {'druid.hero.moon.mooncursed', 'druid.base.bear-form-tank', 'warrior.supplement.berserker-brew',
        'paladin.supplement.oath-of-vengeance.vengeful-smite', 'cleric.hero.cultist.zealot-s-fervor',
        'crimson-agent.hero.thirstborn.blood-frenzy', 'crimson-agent.hero.thirstborn.veinweave-blood-frenzy'}
    rage_rejections = [{k: row[k] for k in ['path', 'sha256', 'pointer']} for row in excerpts if isinstance(row['value'], dict) and row['value'].get('id') in rage_ids]
    assert len(rage_rejections) == 7
    for ref in rage_rejections:
        path = G / ref['path']
        if path not in paths:
            paths.append(path); bindings.append(info(path))

    def check(group, label, truth):
        record = {'group': group, 'id': label, 'passed': bool(truth)}
        results.append(record); groups[group].append(label)
        if not truth:
            raise AssertionError(label)

    def history(scores=None, level=8, earn=True):
        actor = deepcopy(base_actor)
        actor.update(firstClass='Warrior', classLevels={'Warrior': 1}, selectedClassSkills=['Animal Handling', 'Athletics'])
        for ability, score in (scores or {}).items():
            dice = next(d for d in product(range(1, 7), repeat=4) if sum(d) - min(d) + imperial['combinedAbilityBonuses'][ability] == score)
            actor['abilityRolls'][ability] = list(dice); actor['permanentScores'][ability] = score
        h = RemainingOwnedChains(actor, classes, equipment, skills, ancestry, backgrounds, contracts, supplements, sources)
        h.advance(level)
        if earn:
            h.earn(level)
        return h

    def fixture(sid, branch=None, h=None, edit_main=None, edit_authority=None, edit_character=None,
                edit_sources=None, class_source_override=None, main_source_override=None,
                no_class=False, no_main=False, select_rage=False, duplicate_selection=False,
                event_at=None, type_choice='cold'):
        branch = branch or {'frenzied_rage': 'class_rage', 'divine_favor': 'worship', 'elemental_body': 'exposure', 'dragon_blood': 'Dragonborn'}[sid]
        h = h or history(); mode = 'conditional_fixture'; world_id = 'ACQ04-opaque-test-world'; actor_id = 'ACQ04-test-actor'
        source_data = {
            'deity': {'recordType': 'opaque_referent', 'referentKind': 'deity', 'opaqueId': 'test-reference-d1', 'evidenceMode': mode},
            'plane': {'recordType': 'opaque_referent', 'referentKind': 'elemental_plane', 'opaqueId': 'test-reference-p1', 'evidenceMode': mode},
            'lineage': {'recordType': 'lineage', 'name': 'Dragonborn', 'damageType': 'cold', 'evidenceMode': mode},
            'otherLineage': {'recordType': 'lineage', 'name': 'Dragonborn', 'damageType': 'fire', 'evidenceMode': mode},
            'rageClass': {'recordType': 'class', 'name': 'Conditional External Class', 'featureIds': ['conditional-rage-feature'],
                'featureSelections': [{'id': 'conditional-slot1', 'minimumClassLevel': 1, 'allowedFeatureIds': ['conditional-rage-feature']}], 'evidenceMode': mode},
            'rageFeature': {'recordType': 'class_feature', 'id': 'conditional-rage-feature', 'className': 'Conditional External Class',
                'minimumClassLevel': 1, 'requiredPath': 'conditional-path', 'grantedState': 'rage',
                'acquisition': 'selection' if select_rage else 'automatic', 'evidenceMode': mode},
            'sorcerer': {'recordType': 'class', 'name': 'Sorcerer', 'bloodlineIds': ['conditional-draconic'], 'evidenceMode': mode},
            'bloodline': {'recordType': 'bloodline', 'id': 'conditional-draconic', 'className': 'Sorcerer',
                'bloodlineKind': 'draconic', 'damageType': 'cold', 'evidenceMode': mode}}
        if edit_sources:
            edit_sources(source_data)
        source_root = store.put(source_data)
        refs = {key: {**source_root, 'pointer': '/' + key} for key in source_data}
        all_sources = list(refs.values())
        for ref in [class_source_override, main_source_override]:
            if ref is not None and ref not in all_sources:
                all_sources.append(ref)
        authority = {'recordType': 'authority', 'id': 'ACQ04-fixture-record-authority', 'worldId': world_id, 'evidenceMode': mode,
            'subjects': [actor_id], 'predicateScopes': [sid + '/' + branch], 'effectiveFrom': {'elapsed': 0, 'sequence': 0}}
        if edit_authority:
            edit_authority(authority)
        authority_ref = store.put(authority)
        common = {'worldId': world_id, 'characterId': actor_id, 'evidenceMode': mode, 'authorityRef': authority_ref,
                  'at': event_at or {'elapsed': 5, 'sequence': 1}, 'version': 1}
        character = {'recordType': 'character', 'worldId': world_id, 'characterId': actor_id, 'evidenceMode': mode,
            'permanentScores': deepcopy(h.pay.scores), 'classLevels': deepcopy(h.pay.current_classes), 'lineage': 'Human'}
        admitted_credentials = []; choices = None
        if sid == 'frenzied_rage' or branch == 'Sorcerer':
            class_name = 'Conditional External Class' if sid == 'frenzied_rage' else 'Sorcerer'
            character['classLevels'][class_name] = 1
            class_assignment = {**common, 'recordType': 'class_assignment', 'at': {'elapsed': 3, 'sequence': 1},
                'className': class_name, 'classLevel': 1, 'sourceRef': class_source_override or refs['rageClass' if sid == 'frenzied_rage' else 'sorcerer']}
            class_ref = store.put(class_assignment)
            if not no_class:
                admitted_credentials.append(class_ref)
        if sid == 'frenzied_rage':
            main = {**common, 'recordType': 'class_feature_assignment', 'featureRef': main_source_override or refs['rageFeature'],
                'classAssignmentRef': class_ref if not no_class else None, 'path': 'conditional-path',
                'acquisition': 'selection' if select_rage else 'automatic', 'rageActive': False}
            if select_rage:
                selection = {**common, 'recordType': 'class_feature_selection', 'at': {'elapsed': 4, 'sequence': 1},
                    'classAssignmentRef': class_ref, 'featureId': 'conditional-rage-feature', 'slotId': 'conditional-slot1'}
                selection_ref = store.put(selection); admitted_credentials.append(selection_ref); main['selectionRef'] = selection_ref
                if duplicate_selection:
                    duplicate = deepcopy(selection); duplicate['at']['sequence'] = 2
                    admitted_credentials.append(store.put(duplicate))
        elif sid == 'divine_favor':
            main = {**common, 'recordType': 'worship_relationship', 'relationship': 'worship', 'deityRef': refs['deity']}
        elif sid == 'elemental_body':
            main = {**common, 'recordType': 'exposure_event', 'predicate': 'exposure_to_elemental_plane', 'planeRef': refs['plane']}
            choices = {'permanentType': type_choice}
        elif branch == 'Dragonborn':
            character['lineage'] = 'Dragonborn'
            lineage_ref = main_source_override or refs['lineage']; type_ref = {**lineage_ref, 'pointer': lineage_ref['pointer'] + '/damageType'}
            main = {**common, 'recordType': 'lineage_assignment', 'lineage': 'Dragonborn', 'sourceRef': lineage_ref, 'damageTypeRef': type_ref}
            choices = {'damageType': type_choice, 'sourceRef': type_ref, 'characterId': actor_id}
        else:
            type_ref = {**refs['bloodline'], 'pointer': '/bloodline/damageType'}
            main = {**common, 'recordType': 'bloodline_assignment', 'classAssignmentRef': class_ref if not no_class else None,
                    'sourceRef': refs['bloodline'], 'damageTypeRef': type_ref}
            choices = {'damageType': type_choice, 'sourceRef': type_ref, 'characterId': actor_id}
        if edit_character:
            edit_character(character)
        if edit_main:
            edit_main(main, refs)
        main_ref = store.put(main)
        if not no_main:
            admitted_credentials.append(main_ref)
        char_ref = store.put(character)
        world = {'recordType': 'world', 'worldId': world_id, 'evidenceMode': mode, 'characterRefs': [char_ref],
            'authorityRefs': [authority_ref], 'sourceRefs': all_sources, 'credentialRefs': admitted_credentials,
            'scope': 'Isolated authored test premises only; no actual campaign authority or content option.'}
        world_ref = store.put(world)
        paid_ref = store.put({'evidenceMode': mode, 'scope': 'Source-qualified conditional paid history', 'history': h.snapshot()})
        acquisition = {'recordType': 'acquisition_snapshot', 'worldRef': world_ref, 'characterRef': char_ref,
            'worldId': world_id, 'characterId': actor_id, 'evidenceMode': mode, 'featId': sid, 'at': {'elapsed': 10, 'sequence': 5},
            'permanentScores': deepcopy(character['permanentScores']), 'classLevels': deepcopy(character['classLevels']),
            'paidHistoryRef': paid_ref, 'opportunity': 'Warrior:' + str(h.pay.current_classes['Warrior'])}
        if choices is not None:
            acquisition['choices'] = choices
        acq_ref = store.put(acquisition)
        evidence = {'evidenceMode': mode, 'worldId': world_id, 'characterId': actor_id, 'acquisitionRef': acq_ref,
            'predicate': {'featId': sid, 'branch': branch, 'contractRef': contract_refs[sid]},
            'authorityRef': authority_ref, 'credentialRefs': [main_ref] if not no_main else []}
        if choices is not None:
            evidence['choiceBindings'] = deepcopy(choices)
        admitted = [{'evidenceMode': mode, 'worldRef': world_ref}]
        model = ExternalCredentialEvidence(G, admitted, contract_refs, rage_rejections)
        return {'evidence': evidence, 'model': model, 'history': h, 'acquisition': acquisition,
                'admittedWorlds': admitted, 'sourceRefs': refs, 'main': main, 'character': character}

    def run(group, label, f, expected='CONDITIONAL_ONLY', mutate=None, expected_gate=None):
        evidence = deepcopy(f['evidence'])
        if mutate:
            mutate(evidence)
        before = f['history'].snapshot(); original_evidence = deepcopy(evidence)
        result = f['model'].evaluate(evidence)
        check(group, label + '/external-outcome', result['outcome'] == expected)
        gate = acquisition_gate(evidence['predicate']['featId'], result, f['history'].pay,
            f['acquisition']['opportunity'], f['acquisition'])
        if expected_gate is not None:
            check(group, label + '/acquisition-gate', gate['decision'] == expected_gate)
        check(group, label + '/no-mutation', f['history'].snapshot() == before and evidence == original_evidence)
        check(group, label + '/no-campaign-claim', not result['campaignAcquisitionEstablished'] and not gate['campaignAcquisitionEstablished'])
        cases.append({'group': group, 'id': label, 'evidence': evidence, 'admittedWorlds': f['admittedWorlds'],
            'expectedExternalOutcome': expected, 'result': result, 'acquisitionGate': gate})
        return result

    for ref in rage_rejections:
        run('ACQ04-T01', 'current-class-card/' + ref['pointer'] + '/' + Path(ref['path']).stem,
            fixture('frenzied_rage', main_source_override=ref), 'CONTRADICTED', expected_gate='DENIED')

    h = history(scores={'CON': 15}, level=4); h.acquire_named('berserker', 4)
    h.advance(8); h.earn(8)
    before = h.snapshot()
    result = {'outcome': 'UNESTABLISHED', 'reason': 'No external class rage supplied'}
    paid_gate = acquisition_gate('frenzied_rage', result, h.pay, 'Warrior:8', {'permanentScores': deepcopy(h.pay.scores)}, owned_berserker=True)
    check('ACQ04-T02', 'paid-Berserker-and-separate-opportunity', paid_gate['decision'] == 'CONDITIONAL_ACQUISITION_CASE')
    check('ACQ04-T02', 'rage-need-not-be-active', not h.initializations['berserker']['rageActive'])
    check('ACQ04-T02', 'gate-does-not-spend', before == h.snapshot())
    h.pay.commit('frenzied_rage', 'Warrior:8', prerequisites_met=paid_gate['decision'] == 'CONDITIONAL_ACQUISITION_CASE')
    check('ACQ04-T02', 'two-distinct-real-payments', [g['opportunity'] for g in h.pay.grants] == ['Warrior:4', 'Warrior:8'])
    again = acquisition_gate('frenzied_rage', result, h.pay, 'Warrior:8', {'permanentScores': deepcopy(h.pay.scores)}, owned_berserker=True)
    check('ACQ04-T02', 'spent-nonrepeatable-acquisition-denied', again['decision'] == 'DENIED')
    paid_history_ref = store.put({'before': before, 'gate': paid_gate, 'after': h.snapshot(), 'repeatGate': again, 'evidenceMode': 'conditional_fixture'})
    cases.append({'group': 'ACQ04-T02', 'id': 'lawful-parent-and-child-payments', 'completeHistoryRef': paid_history_ref})

    cf = history(scores={'STR': 16, 'CON': 15}, level=12)
    cf.pay.commit('berserker_rage', 'Warrior:12', prerequisites_met=cf.prerequisite('berserker_rage'))
    cf.advance(16); cf.earn(16)
    cf_gate = acquisition_gate('frenzied_rage', result, cf.pay, 'Warrior:16', {'permanentScores': deepcopy(cf.pay.scores)}, owned_berserker=True)
    check('ACQ04-T03', 'CF03-owned-is-not-Berserker-parent', cf_gate['decision'] == 'DENIED' and not cf.pay.has('berserker'))
    check('ACQ04-T03', 'CF03-operating-clause-preserved', "This is a rage for Frenzied Rage's operating trigger" in contracts['berserker_rage']['completeOperativeProcedure'])
    cases.append({'group': 'ACQ04-T03', 'id': 'paid-CF03-not-acquisition-parent', 'completeHistoryRef': store.put(cf.snapshot()), 'gate': cf_gate})
    for sid in ['berserker_rage', 'frenzied_rage']:
        index = next(i for i, row in enumerate(contracts_document['records']) if row['id'] == sid)
        run('ACQ04-T03', 'feat-procedure-not-class-grant/' + sid, fixture('frenzied_rage', main_source_override=bound(paths[16], '/records/' + str(index))), 'CONTRADICTED')

    run('ACQ04-T04', 'conditional-automatic-class-rage', fixture('frenzied_rage'), expected_gate='CONDITIONAL_ACQUISITION_CASE')
    run('ACQ04-T04', 'conditional-selected-class-rage', fixture('frenzied_rage', select_rage=True))
    run('ACQ04-T04', 'source-without-actor-assignment', fixture('frenzied_rage', no_main=True), 'UNESTABLISHED')
    run('ACQ04-T04', 'feature-without-class-assignment', fixture('frenzied_rage', no_class=True), 'UNESTABLISHED')
    run('ACQ04-T04', 'wrong-class-feature-path', fixture('frenzied_rage', edit_main=lambda x, r: x.update(path='different')), 'UNESTABLISHED')
    run('ACQ04-T04', 'below-feature-source-level', fixture('frenzied_rage', edit_sources=lambda x: x['rageFeature'].update(minimumClassLevel=2)), 'UNESTABLISHED')
    run('ACQ04-T04', 'duplicate-feature-selection', fixture('frenzied_rage', select_rage=True, duplicate_selection=True), 'UNESTABLISHED')
    run('ACQ04-T05', 'bound-opaque-worship-no-favor-award', fixture('divine_favor', h=history(scores={'CHA': 15})), expected_gate='CONDITIONAL_ACQUISITION_CASE')
    run('ACQ04-T06', 'deity-source-without-relationship', fixture('divine_favor', no_main=True), 'UNESTABLISHED')
    run('ACQ04-T06', 'worship-ended-before-acquisition', fixture('divine_favor', edit_main=lambda x, r: x.update(endedAt={'elapsed': 9, 'sequence': 1})), 'CONTRADICTED')
    for damage_type in ['acid', 'cold', 'fire', 'lightning', 'thunder']:
        run('ACQ04-T07', 'prior-exposure-choice/' + damage_type, fixture('elemental_body', type_choice=damage_type, h=history(scores={'CON': 15})), expected_gate='CONDITIONAL_ACQUISITION_CASE')
    run('ACQ04-T07', 'invalid-elemental-type', fixture('elemental_body', type_choice='psychic'), 'UNESTABLISHED')
    for false_fact in ['elemental_damage', 'resistance', 'Drakari_variant', 'class_spell', 'generic_visit']:
        run('ACQ04-T08', 'not-exposure/' + false_fact,
            fixture('elemental_body', edit_main=lambda x, r, fact=false_fact: x.update(recordType=fact, predicate=fact)), 'UNESTABLISHED')
    for sid, ability in [('divine_favor', 'CHA'), ('elemental_body', 'CON')]:
        run('ACQ04-T09', sid + '/permanent14', fixture(sid, h=history(scores={ability: 14})), expected_gate='DENIED')
        run('ACQ04-T09', sid + '/no-earned-opportunity', fixture(sid, h=history(earn=False)), expected_gate='DENIED')
        spent = history(); spent.pay.commit('alert', 'Warrior:8', prerequisites_met=spent.prerequisite('alert'))
        run('ACQ04-T09', sid + '/spent-opportunity', fixture(sid, h=spent), expected_gate='DENIED')

    subjects = [('frenzied_rage', 'class_rage'), ('divine_favor', 'worship'), ('elemental_body', 'exposure'), ('dragon_blood', 'Dragonborn'), ('dragon_blood', 'Sorcerer')]
    for sid, branch in subjects:
        prefix = sid + '/' + branch
        f = fixture(sid, branch)
        absent = run('ACQ04-T10', prefix + '/absent-authority', f, 'UNESTABLISHED', lambda e: e.pop('authorityRef'))
        null = run('ACQ04-T10', prefix + '/null-authority', f, 'UNESTABLISHED', lambda e: e.update(authorityRef=None))
        check('ACQ04-T10', prefix + '/raw-absence-null-distinct', absent['referenceFieldState'] == 'absent' and null['referenceFieldState'] == 'null')
        run('ACQ04-T10', prefix + '/missing-path', f, 'UNESTABLISHED', lambda e: e['authorityRef'].update(path='docs/audit/does-not-exist.json'))
        run('ACQ04-T10', prefix + '/wrong-hash', f, 'UNESTABLISHED', lambda e: e['authorityRef'].update(sha256='0' * 64))
        run('ACQ04-T10', prefix + '/wrong-pointer', f, 'UNESTABLISHED', lambda e: e['authorityRef'].update(pointer='/not-a-record'))
        run('ACQ04-T10', prefix + '/resolved-wrong-pointer', f, 'UNESTABLISHED', lambda e: e['authorityRef'].update(pointer='/subjects'))
        run('ACQ04-T10', prefix + '/wrong-version', f, 'UNESTABLISHED', lambda e: e['credentialRefs'][0].update(version=99))
        run('ACQ04-T10', prefix + '/wrong-actor', fixture(sid, branch, edit_main=lambda x, r: x.update(characterId='someone-else')), 'UNESTABLISHED')
        run('ACQ04-T10', prefix + '/wrong-world', fixture(sid, branch, edit_main=lambda x, r: x.update(worldId='other-world')), 'UNESTABLISHED')
        run('ACQ04-T10', prefix + '/no-authority-scope', fixture(sid, branch, edit_authority=lambda x: x.update(predicateScopes=[])), 'UNESTABLISHED')
        run('ACQ04-T10', prefix + '/wrong-contract', f, 'UNESTABLISHED', lambda e: e['predicate']['contractRef'].update(pointer='/records/0'))
        for timing, expected, name in [({'elapsed': 11, 'sequence': 0}, 'UNESTABLISHED', 'later'),
            ({'elapsed': 10, 'sequence': 5}, 'UNESTABLISHED', 'same-unordered'),
            ({'elapsed': 10, 'sequence': 4}, 'CONDITIONAL_ONLY', 'same-earlier-sequence')]:
            run('ACQ04-T11', prefix + '/' + name, fixture(sid, branch, event_at=timing), expected)
        run('ACQ04-T15', prefix + '/fixture-relabelled-campaign', f, 'UNESTABLISHED', lambda e: e.update(evidenceMode='campaign_record'))
        run('ACQ04-T15', prefix + '/mixed-campaign-support', fixture(sid, branch, edit_main=lambda x, r: x.update(evidenceMode='campaign_record')), 'UNESTABLISHED')
        forged = acquisition_gate(sid, {'eligible': True}, f['history'].pay, 'Warrior:8', f['acquisition'])
        check('ACQ04-T15', prefix + '/unqualified-Boolean-not-evidence', forged['decision'] == 'DENIED')

    drakari_index = next(i for i, row in enumerate(ancestry['ancestries']) if row['name'] == 'Drakari')
    mage_index = next(i for i, row in enumerate(foundation['classes']) if row['class'] == 'Mage')
    run('ACQ04-T12', 'actual-Drakari-not-Dragonborn', fixture('dragon_blood', main_source_override=bound(paths[10], '/ancestries/' + str(drakari_index))), 'CONTRADICTED')
    run('ACQ04-T12', 'actual-Mage-not-Sorcerer', fixture('dragon_blood', 'Sorcerer', class_source_override=bound(paths[9], '/classes/' + str(mage_index))), 'CONTRADICTED')
    curriculum_ref = bound(paths[14], '/groups/3/value/Sorcerer')
    run('ACQ04-T12', 'feat-curriculum-is-not-class', fixture('dragon_blood', 'Sorcerer', class_source_override=curriculum_ref), 'CONTRADICTED')
    run('ACQ04-T12', 'literacy-is-not-lineage', fixture('dragon_blood', edit_main=lambda x, r: x.update(recordType='language_grant', language='Draconic')), 'UNESTABLISHED')
    run('ACQ04-T12', 'unbound-class-label', fixture('dragon_blood', 'Sorcerer', no_class=True), 'UNESTABLISHED')
    for branch, group in [('Dragonborn', 'ACQ04-T13'), ('Sorcerer', 'ACQ04-T14')]:
        f = fixture('dragon_blood', branch)
        run(group, branch + '/conditional-import', f, expected_gate='CONDITIONAL_ACQUISITION_CASE')
        run(group, branch + '/missing-type', f, 'UNESTABLISHED', lambda e: e.pop('choiceBindings'))
        run(group, branch + '/null-type', f, 'UNESTABLISHED', lambda e: e.update(choiceBindings=None))
        run(group, branch + '/type-value-mismatch', f, 'UNESTABLISHED', lambda e: e['choiceBindings'].update(damageType='fire'))
        run(group, branch + '/type-other-character', f, 'UNESTABLISHED', lambda e: e['choiceBindings'].update(characterId='other-actor'))
        run(group, branch + '/type-other-source', f, 'UNESTABLISHED', lambda e: e['choiceBindings']['sourceRef'].update(pointer='/otherLineage/damageType'))
        run(group, branch + '/missing-qualifying-grant', fixture('dragon_blood', branch, no_main=True), 'UNESTABLISHED')
    run('ACQ04-T14', 'Sorcerer-missing-class', fixture('dragon_blood', 'Sorcerer', no_class=True), 'UNESTABLISHED')
    run('ACQ04-T14', 'Sorcerer-classlevel-zero', fixture('dragon_blood', 'Sorcerer', edit_character=lambda x: x['classLevels'].update(Sorcerer=0)), 'UNESTABLISHED')
    run('ACQ04-T14', 'Sorcerer-nondraconic-bloodline', fixture('dragon_blood', 'Sorcerer', edit_sources=lambda x: x['bloodline'].update(bloodlineKind='other')), 'UNESTABLISHED')

    # Fresh reverse differences rather than treating a previous green report as proof.
    operations = read(paths[21]); preservation = {x['after']['path']: x['before'] for x in operations['changes']}
    current_contracts = read(paths[16]); saved = read(G / preservation[paths[16].relative_to(G).as_posix()]['preservedCopy'])
    restored = deepcopy(current_contracts)
    for row in restored['records']:
        if row['id'] in policy['dispositions']:
            check('ACQ04-T16', 'exact-reference/' + row['id'], row.pop('externalCredentialPolicyRef') == paths[19].relative_to(G).as_posix() + '#/dispositions/' + row['id'])
    check('ACQ04-T16', 'all-existing-contract-fields-retained', restored == saved)
    for change in operations['changes']:
        check('ACQ04-T16', 'current-descendant/' + change['after']['path'], info(G / change['after']['path']) == change['after'])
        old = change['before']
        check('ACQ04-T16', 'preserved-old-bytes/' + old['path'], info(G / old['preservedCopy'])['sha256'] == old['sha256'])
    for rel, binding in read(paths[24]).items():
        if rel not in preservation:
            check('ACQ04-T16', 'unchanged-submitted/' + rel, all(info(G / rel)[k] == binding[k] for k in ['bytes', 'sha256']))
    for binding in bindings:
        check('ACQ04-T16', 'unchanged-pass-input/' + binding['path'], info(G / binding['path']) == binding)
    check('ACQ04-T16', 'all-sixteen-groups-executed', len(groups) == 16 and all(groups.values()))
    for ref in store.paths:
        assert sha256(ref.read_bytes()).hexdigest() == ref.stem
    report = {'createdAtUtc': datetime.now(timezone.utc).isoformat(), 'status': 'passed-all-sixteen-finite-ACQ04-acceptance-groups',
        'sourceBindings': bindings, 'fixtureBindings': [info(p) for p in sorted(store.paths)],
        'completeAcceptanceExpectations': expectations, 'groups': groups, 'cases': cases,
        'checks': len(results), 'failures': [], 'results': results,
        'counts': {'acceptanceGroups': 16, 'recordedCases': len(cases), 'immutableFixtureFiles': len(store.paths),
            'newPartialPrerequisiteIdentities': 4, 'cumulativePartialPrerequisiteIdentities': 334, 'remainingCredentialDependentIdentities': 1},
        'remaining': [x for x in previous['remaining'] if x['id'] not in policy['dispositions']],
        'limits': ['All admitted roots are explicitly conditional fixtures. No actual campaign positive is supplied, authenticated or promoted; ESTABLISHED_FOR_SNAPSHOT is not claimed as executed positive evidence.',
            'Hypothetical external class, class-feature, lineage and bloodline records exist solely within the audit fixtures. No such option is added to current catalogs or runtime selectors.',
            'The external actor/class assignments are controlled conditional premises, not complete multiclass character builds. Real Warrior ASI/feat payment slices and permanent ability rolls are separately source-derived.',
            'Required source clauses, actor/world/authority bindings, effective chronology, selected-feature history, permanent choices and source-bound damage types are checked; no cosmology meaning is supplied.',
            'CF-03 remains a distinct paid feat whose operating interaction is preserved textually. Rage attacks, durations, charges, elemental damage, resistance and Divine Favor use resolution are not executed here.',
            'The new four-identity count concerns partial prerequisite interfaces, not four complete feat uses, all335 acquisitions or exact candidate approval. Companion Training ownership/body history remains outstanding.'],
        'all335CompleteAcquisitionsValidated': False, 'candidateReadyForSubmission': False,
        'campaignRecordsAuthenticated': 0, 'cosmologyReviewed': False, 'sourceInformationDeleted': False}
    assert len(report['remaining']) == 1 and report['remaining'][0]['id'] == 'companion_training'
    with output.open('x', encoding='utf-8', newline='\n') as f:
        json.dump(report, f, ensure_ascii=False, indent=2, default=serial); f.write('\n')
    with notes.open('x', encoding='utf-8', newline='\n') as f:
        f.write(f'''# ACQ-04 finite external credential acceptance\n\nAll16 actual GPT expectation groups pass: {len(results)} checks and {len(cases)} recorded cases. Seven current class cards do not grant a rage state; separately paid Berserker qualifies without active rage. CF-03 and prospective benefits do not supply that acquisition prerequisite.\n\nOpaque conditional worship/exposure fixtures, both hypothetical legacy Dragon Blood branches, and automatic/selected external class-rage histories exercise the adopted record interface. Missing/null/unresolved references, hash/version/pointer mismatches, wrong actors/worlds/authority scopes, later or unordered events, false aliases and wrong source damage types are rejected. Equal timestamps with an authoritative earlier sequence may qualify. Permanent ability, actual earned payment and required choices remain independent.\n\nEvery admitted world is a conditional fixture. It cannot be relabeled as campaign evidence; no actual-world positive, selectable class/lineage, deity, plane interpretation or gameplay implementation is created. Original contracts/procedures, class/ancestry sources, existing ACQ01–03 provisions and approval flags remain preserved through measured additions.\n\nThe partial prerequisite ledger reaches334/335; Companion Training's paid Animal Companion branch remains. This is finite acquisition-interface evidence, not full335 acquisitions, feat-use validation, exact-candidate approval or human balance.\n''')
    print(json.dumps({'report': info(output), 'notes': info(notes), 'checks': len(results),
        'groups': len(groups), 'cases': len(cases), 'fixtureFiles': len(store.paths), 'failures': 0, 'remaining': report['remaining']}, indent=2))


if __name__ == '__main__':
    main()
