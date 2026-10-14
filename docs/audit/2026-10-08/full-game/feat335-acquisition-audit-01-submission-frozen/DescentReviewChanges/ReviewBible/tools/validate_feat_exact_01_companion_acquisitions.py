"""Paid Animal Companion histories for the last partial prerequisite identity."""
from copy import deepcopy
from datetime import datetime, timezone
import json
from pathlib import Path
from feat_exact_01_companion_acquisition_model import CompanionAcquisition
from feat_exact_01_casting_credential_model import CastingSources
from validate_feat_exact_01_composite_casting import read, info, serial

R = Path(__file__).resolve().parents[1]; G = R.parents[1]
A = G / 'docs/audit/2026-10-08/full-game'


def main():
    output = A / 'FEAT_EXACT_01_COMPANION_ACQUISITION_CHECK.json'
    notes = A / 'FEAT_EXACT_01_COMPANION_ACQUISITION_NOTES.md'
    assert not output.exists() and not notes.exists()
    paths = [Path(__file__), R / 'tools/feat_exact_01_companion_acquisition_model.py',
        R / 'tools/feat_exact_01_remaining_owned_chains.py', R / 'tools/feat_exact_01_composite_casting_model.py',
        R / 'tools/feat_exact_01_training_prerequisite_model.py', R / 'tools/feat_exact_01_acquisition_models.py',
        R / 'tools/feat_exact_01_casting_credential_model.py', R / 'tools/feat_exact_01_initiate_acquisition_model.py',
        R / 'tools/validate_feat_exact_01_composite_casting.py',
        R / 'data/playtest/character_foundation.json', R / 'data/playtest/ancestry_background_candidate.json',
        R / 'data/playtest/equipment_source_catalog.json', R / 'data/public/class_playtests/wizard.json',
        R / 'data/public/feat_candidates/exact_01/spell_dependencies.json', R / 'data/public/feat_candidates/exact_01/supplements.json',
        R / 'data/public/feat_candidates/exact_01/shared_rules.json', A / 'FEAT_EXACT_01_ACQUISITION_CONTRACTS.json',
        A / 'FEAT_EXACT_01_INITIATE_ACQUISITION_CHECK.json', A / 'FEAT327_ACQ_04_EXTERNAL_CREDENTIAL_CHECK.json']
    bindings = [info(p) for p in paths]
    foundation = read(paths[9]); classes = {x['class']: x for x in foundation['classes']}
    skills = {s: a for a, group in foundation['skillAbilities'].items() for s in group}
    ancestry = read(paths[10]); backgrounds = {x['id']: x for x in ancestry['backgrounds']}
    equipment = {x['id']: x for x in read(paths[11])['records']}
    supplements = {x['id']: x['value'] for x in read(paths[14])['groups']}
    sources = CastingSources(G, read(paths[13])['spells'], supplements, read(paths[12]))
    contracts = {x['id']: x for x in read(paths[16])['records']}
    actor_source = read(paths[17])['actorSourceProjection']; previous = read(paths[18])
    results = []; histories = []

    def check(label, truth):
        results.append({'id': label, 'passed': bool(truth)})
        if not truth:
            raise AssertionError(label)

    def history(handling=True):
        actor = deepcopy(actor_source)
        actor.update(firstClass='Warrior', classLevels={'Warrior': 1}, selectedClassSkills=['Animal Handling' if handling else 'Nature', 'Athletics'])
        h = CompanionAcquisition(actor, classes, equipment, skills, ancestry, backgrounds, contracts, supplements, sources)
        h.advance(4); h.earn(4)
        return h

    def body(kind='ground', size=None, hp=5, maximum=10, senses=None):
        size = size or {'ground': 'Small', 'flyer': 'Tiny', 'swimmer': 'Small'}[kind]
        return {'id': 'existing-conditional-' + kind, 'worldId': 'conditional-body-world', 'evidenceMode': 'conditional_fixture',
            'creatureType': 'Beast', 'size': size, 'living': True, 'corrupted': False,
            'abilities': {'STR': 8, 'DEX': 12, 'CON': 10, 'INT': 3, 'WIS': 10, 'CHA': 6},
            'ordinaryMaximumHP': maximum, 'ordinaryCurrentHP': hp,
            'nativeMovement': {'ground': {'walkFeet': 30}, 'flyer': {'walkFeet': 10, 'flyFeet': 30}, 'swimmer': {'swimFeet': 30}}[kind],
            'anatomy': {'ground': ['bite', 'legs'], 'flyer': ['peck', 'wings', 'legs'], 'swimmer': ['bite', 'fins']}[kind],
            'breathing': 'water' if kind == 'swimmer' else 'air',
            'conditions': ['existing-condition-marker'], 'injuries': ['existing-injury-marker'],
            'controllerRelation': {'kind': 'willing', 'actorId': 'conditional-owner'}, 'currentBonds': [],
            'keenSenses': senses or []}

    def receipt(b, sense=None):
        return {'actorId': 'conditional-owner', 'worldId': b['worldId'], 'bodyId': b['id'], 'evidenceMode': 'conditional_fixture',
            'ordinaryProfileBefore': deepcopy(b), 'completedMinutes': 60, 'touchMinutes': 60, 'interruptions': [],
            'firstAttemptInEpoch': {'epoch': 'initial-acquisition', 'ordinal': 1}, 'opportunity': 'Warrior:4', 'keenSenseChoice': sense,
            'premises': 'Existing willing animal and actual access are explicitly conditional world premises, not feat-created stock or a real campaign claim.'}

    def reject(label, h, b, r, template='feat-animal.ground'):
        before = h.snapshot(); original_body = deepcopy(b); original_receipt = deepcopy(r)
        try:
            h.acquire_companion_from_completed_history(4, b, r, template)
        except (ValueError, KeyError) as error:
            results.append({'id': label, 'passed': True, 'reason': str(error)})
        else:
            check(label, False)
        check(label + '/no-mutation-of-rejected-evidence', h.snapshot() == before and b == original_body and r == original_receipt)
        histories.append({'id': label, 'scope': 'Rejected completed-history evidence, not a simulated interrupted attempt/refund', 'actor': before, 'ordinaryBody': b, 'receipt': r})

    for kind, size, hp, maximum, senses, selected in [
        ('ground', 'Small', 5, 10, [], None), ('ground', 'Medium', 1, 20, ['hearing', 'smell'], 'smell'),
        ('flyer', 'Tiny', 3, 7, ['sight'], 'sight'), ('swimmer', 'Small', 7, 10, ['hearing'], 'hearing')]:
        h = history(); b = body(kind, size, hp, maximum, senses); r = receipt(b, selected)
        before = h.snapshot(); h.acquire_companion_from_completed_history(4, b, r, 'feat-animal.' + kind)
        current = h.initializations['animal_companion']['currentBody']
        expected_hp = {('ground', 'Small'): 4, ('ground', 'Medium'): 1, ('flyer', 'Tiny'): 3, ('swimmer', 'Small'): 6}[(kind, size)]
        check(kind + size + '/actual-proportional-HP', current['maximumHP'] == 9 and current['currentHP'] == expected_hp)
        check(kind + size + '/same-body-size-breathing-and-history', current['id'] == b['id'] and current['size'] == size and current['breathing'] == b['breathing'] and current['conditions'] == b['conditions'] and current['injuries'] == b['injuries'])
        check(kind + size + '/one-real-parent-payment', h.pay.has('animal_companion') and h.pay.opportunities['Warrior:4']['spent'])
        check(kind + size + '/child-cannot-share-payment', not h.gate('companion_training', 'Warrior:4'))
        parent = deepcopy(h.initializations['animal_companion']); h.advance(8); h.earn(8)
        check(kind + size + '/growth-no-healing-or-attempt-refill', current['maximumHP'] == 13 and current['currentHP'] == expected_hp and h.initializations['animal_companion']['bondAttemptAllowance']['current'] == 0)
        check(kind + size + '/owned-parent-branch-is-actually-true', h.pay.has('animal_companion') and h.prerequisite('companion_training'))
        h.acquire_named('companion_training', 8)
        check(kind + size + '/separate-child-payment', [x['opportunity'] for x in h.pay.grants] == ['Warrior:4', 'Warrior:8'])
        check(kind + size + '/child-does-not-create-second-animal', list(h.initializations) == ['animal_companion'] and h.initializations['animal_companion']['ordinaryProfile'] == b)
        histories.append({'id': kind + '-' + size + '-completed-parent-child', 'before': before, 'ordinaryBody': b,
            'completedReceipt': r, 'initialBond': parent, 'afterChild': h.snapshot(),
            'scope': 'Source-qualified conditional successful hour, paid parent and paid child; no beast attack or command simulated.'})
        h.advance(12); h.earn(12); snap = h.snapshot()
        try:
            h.acquire_named('companion_training', 12)
        except ValueError:
            check(kind + size + '/child-nonrepeatable', h.snapshot() == snap)
        else:
            check(kind + size + '/child-nonrepeatable', False)

    mutations = {
        'ordinary-HP-missing': lambda b: b.pop('ordinaryCurrentHP'),
        'zero-HP': lambda b: b.update(ordinaryCurrentHP=0),
        'HP-above-maximum': lambda b: b.update(ordinaryCurrentHP=11),
        'INT7': lambda b: b['abilities'].update(INT=7),
        'non-Beast': lambda b: b.update(creatureType='Construct'),
        'dead-body': lambda b: b.update(living=False),
        'corrupted': lambda b: b.update(corrupted=True),
        'wrong-size': lambda b: b.update(size='Large'),
        'no-biting-anatomy': lambda b: b.update(anatomy=['legs']),
        'no-native-ground-movement': lambda b: b.update(nativeMovement={}),
        'not-willing-or-tamed': lambda b: b['controllerRelation'].update(kind='ordinary-ally'),
        'different-owner': lambda b: b['controllerRelation'].update(actorId='other-owner'),
        'existing-Ranger-bond': lambda b: b.update(currentBonds=['ranger-bond']),
        'existing-animal-feat-bond': lambda b: b.update(currentBonds=['animal-companion']),
    }
    for label, mutate in mutations.items():
        b = body(); mutate(b); reject(label, history(), b, receipt(b))
    for label, mutate in {
        '59-minutes': lambda r: r.update(completedMinutes=59),
        'touch-59-minutes': lambda r: r.update(touchMinutes=59),
        'interrupted-hour': lambda r: r.update(interruptions=['left-touch-range']),
        'wrong-physical-body': lambda r: r.update(bodyId='different-animal'),
        'wrong-world': lambda r: r.update(worldId='different-world'),
        'wrong-opportunity': lambda r: r.update(opportunity='Warrior:8'),
        'duplicate-attempt-evidence': lambda r: r['firstAttemptInEpoch'].update(ordinal=2),
        'invented-sense': lambda r: r.update(keenSenseChoice='sight'),
    }.items():
        b = body(); r = receipt(b); mutate(r); reject(label, history(), b, r)
    b = body(); reject('no-Animal-Handling', history(False), b, receipt(b))
    reject('dog-body-not-flight', history(), b, receipt(b), 'feat-animal.flyer')
    flying = body('flyer'); flying['nativeMovement'].pop('flyFeet')
    reject('no-native-flight', history(), flying, receipt(flying), 'feat-animal.flyer')
    swimmer = body('swimmer'); swimmer['nativeMovement'].pop('swimFeet')
    reject('no-native-swimming', history(), swimmer, receipt(swimmer), 'feat-animal.swimmer')
    # The independent proficiency route still requires no Animal Companion purchase/body.
    h = history(); h.acquire_named('companion_training', 4)
    check('independent-Animal-Handling-route', h.pay.has('companion_training') and not h.pay.has('animal_companion') and h.initializations == {})
    no = history(False)
    check('neither-parent-nor-proficiency', not no.prerequisite('companion_training'))
    check('last-partial-identity-only', len(previous['remaining']) == 1 and previous['remaining'][0]['id'] == 'companion_training')
    for binding in bindings:
        check('unchanged/' + binding['path'], info(G / binding['path']) == binding)
    report = {'createdAtUtc': datetime.now(timezone.utc).isoformat(), 'status': 'passed-conditional-paid-companion-acquisition-histories',
        'sourceBindings': bindings, 'completeContracts': [contracts[x] for x in ['animal_companion', 'companion_training']],
        'completeBodyTemplates': supplements['SUP-02'], 'histories': histories, 'checks': len(results), 'results': results, 'failures': [],
        'counts': {'newPartialPrerequisiteIdentities': 1, 'cumulativePartialPrerequisiteIdentities': 335,
            'remainingCredentialDependentIdentities': 0, 'recordedHistories': len(histories), 'positiveBodyHistories': 4},
        'remaining': [], 'limits': [
            'The ordinary animals and completed contact-hour facts are explicit conditional world premises, not actual campaign availability, a taming result, a newly reviewed bestiary species or a source-created animal.',
            'The parent-positive histories retain Animal Handling proficiency; the owned parent node itself is separately checked. No unsupported training-loss/retraining procedure is invented to isolate that OR branch.',
            'Rejected completed records do not define when an interrupted live attempt spends/refunds a feat opportunity or bond allowance. Only successful completed initial acquisition histories are represented.',
            'Bond replacements after later Long Rests, release, owner death, creature death/healing, command phases, attacks, mounting, custody transfer and Companion Training effects remain use-procedure work.',
            'All335 identities now have finite partial prerequisite evidence. This is not335 complete acquisitions, all permanent selections, full original-case execution, actual runtime or exact candidate approval.'],
        'all335CompleteAcquisitionsValidated': False, 'candidateReadyForSubmission': False,
        'sourceInformationDeleted': False, 'cosmologyReviewed': False, 'campaignRecordsAuthenticated': 0}
    with output.open('x', encoding='utf-8', newline='\n') as f:
        json.dump(report, f, ensure_ascii=False, indent=2, default=serial); f.write('\n')
    with notes.open('x', encoding='utf-8', newline='\n') as f:
        f.write(f'''# Animal Companion and Companion Training acquisition\n\n{len(results)} checks pass. Four successful conditional histories cover Small/Medium ground bodies, a native flyer and a native swimmer. Each preserves the existing body, ordinary HP record, conditions, injuries and breathing; applies the actual finite template; completes a stated uninterrupted touch hour; and pays a real Warrior4 opportunity. Warrior8 later pays Companion Training separately. Maximum-HP growth does not heal or refill the used bonding allowance.\n\nMissing HP, dead/corrupted/non-Beast bodies, INT7, incompatible anatomy/movement/size, absent consent, existing bonds and incomplete/mismatched work records cannot prove these acquisitions. A proficient character may independently acquire Companion Training without gaining an animal.\n\nThese are conditional completed-history projections. Rejected evidence does not define interruption refunds or simulate failed attempts. Commands, attacks, replacement/rest, release/death and mount interactions remain separate. The owned-parent examples also retain Animal Handling; no invented retraining history is used.\n\nFinite partial prerequisite coverage now accounts for all335 identities. Full335 acquisitions, remaining choices and actual-use validation are still unfinished.\n''')
    print(json.dumps({'report': info(output), 'notes': info(notes), 'checks': len(results), 'histories': len(histories),
        'failures': 0, 'partialPrerequisiteIdentities': 335, 'remaining': 0, 'fullAcquisitionsComplete': False}, indent=2))


if __name__ == '__main__':
    main()
