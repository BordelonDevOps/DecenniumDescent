"""Execute ACQ05's20 finite groups against a new conditional chronological model."""
from copy import deepcopy
from datetime import datetime, timezone
import json
from pathlib import Path
from feat_exact_01_companion_lifecycle import CompanionLifecycle, validate_ranger_receiving_history
from feat_exact_01_remaining_owned_chains import RemainingOwnedChains
from feat_exact_01_casting_credential_model import CastingSources
from validate_feat_exact_01_composite_casting import read, info, serial

R = Path(__file__).resolve().parents[1]; G = R.parents[1]
A = G / 'docs/audit/2026-10-08/full-game'; V = A / 'feat327-acq05-source'
HOUR = 3600; DAY = 86400


def main():
    target = A / 'FEAT327_ACQ_05_LIFECYCLE_CHECK.json'
    notes = A / 'FEAT327_ACQ_05_LIFECYCLE_NOTES.md'
    assert not target.exists() and not notes.exists()
    foundation_path = R / 'data/playtest/character_foundation.json'
    ancestry_path = R / 'data/playtest/ancestry_background_candidate.json'
    equipment_path = R / 'data/playtest/equipment_source_catalog.json'
    supplement_path = R / 'data/public/feat_candidates/exact_01/supplements.json'
    dependencies_path = R / 'data/public/feat_candidates/exact_01/spell_dependencies.json'
    wizard_path = R / 'data/public/class_playtests/wizard.json'
    ranger_path = R / 'data/public/class_playtests/ranger.json'
    contracts_path = A / 'FEAT_EXACT_01_ACQUISITION_CONTRACTS.json'
    source_actor_path = A / 'FEAT_EXACT_01_INITIATE_ACQUISITION_CHECK.json'
    expectation_path = V / 'ACQ05_ACCEPTANCE_EXPECTATIONS.json'
    protected = [foundation_path, ancestry_path, equipment_path, supplement_path, dependencies_path,
        wizard_path, ranger_path, contracts_path, source_actor_path, expectation_path,
        V / 'ACQ05_ANIMAL_COMPANION_OPERATIVE.txt', V / 'ACQ05_LIFECYCLE_RECORD_CONTRACT.json',
        V / 'FEAT327_ACQ05_CONTROLLING_ADDENDUM.md', A / 'FEAT327_ACQ_05_INDEPENDENT_DESCENDANT_CHECK.json',
        A / 'FEAT327_ACQ_05_DERIVED_OPERATIONS.json', A / 'FEAT_EXACT_01_COMPANION_ACQUISITION_CHECK.json',
        R / 'data/public/feat_candidates/exact_01/candidate.json',
        R / 'data/director/feat_candidates/exact_01/candidate.json',
        R / 'data/public/feat_candidates/exact_01/shared_rules.json',
        R / 'docs/mechanics/expedition/EXPEDITION_PLAYER_BOOK.md']
    protected += [R / 'tools' / n for n in ['feat_exact_01_companion_acquisition_model.py',
        'feat_exact_01_remaining_owned_chains.py', 'feat_exact_01_composite_casting_model.py',
        'feat_exact_01_casting_credential_model.py', 'feat_exact_01_initiate_acquisition_model.py',
        'feat_exact_01_training_prerequisite_model.py', 'feat_exact_01_acquisition_models.py',
        'feat_exact_01_companion_lifecycle.py', 'validate_feat_exact_01_composite_casting.py']]
    protected += [Path(__file__)]
    bindings = [info(p) for p in protected]
    foundation = read(foundation_path); classes = {x['class']: x for x in foundation['classes']}
    skills = {s: a for a, group in foundation['skillAbilities'].items() for s in group}
    ancestry = read(ancestry_path); backgrounds = {x['id']: x for x in ancestry['backgrounds']}
    equipment = {x['id']: x for x in read(equipment_path)['records']}
    supplements = {x['id']: x['value'] for x in read(supplement_path)['groups']}
    sources = CastingSources(G, read(dependencies_path)['spells'], supplements, read(wizard_path))
    contracts = {x['id']: x for x in read(contracts_path)['records']}
    actor_source = read(source_actor_path)['actorSourceProjection']
    expectations = read(expectation_path); results = []; traces = []; group = None
    support = {'evidenceMode': 'conditional_fixture', 'actualWork': True, 'uninterrupted': True,
        'noIncompatibleOverlap': True, 'withinWorkWatchAllowance': True, 'touch': True}

    def check(label, truth):
        results.append({'group': group, 'id': label, 'passed': bool(truth)})
        if not truth:
            raise AssertionError(f'{group}/{label}')

    def reject(label, world, function):
        before = world.snapshot()
        try:
            function()
        except (ValueError, KeyError) as error:
            check(label, world.snapshot() == before)
            results[-1]['rejection'] = str(error)
        else:
            check(label, False)

    def trace(label, world):
        traces.append({'group': group, 'id': label, 'state': world.snapshot(),
            'evidenceMode': 'conditional_fixture', 'campaignAuthenticated': False})

    def history(handling=True, earned=True):
        actor = deepcopy(actor_source)
        actor.update(firstClass='Warrior', classLevels={'Warrior': 1}, selectedClassSkills=['Animal Handling' if handling else 'Nature', 'Athletics'])
        h = RemainingOwnedChains(actor, classes, equipment, skills, ancestry, backgrounds, contracts, supplements, sources)
        h.advance(4)
        if earned:
            h.earn(4)
        return h

    def body(sid='owner', bid='animal', kind='ground', size=None, hp=5, maximum=10, senses=None):
        return {'id': bid, 'worldId': 'conditional-lifecycle-world', 'evidenceMode': 'conditional_fixture',
            'creatureType': 'Beast', 'size': size or {'ground': 'Small', 'flyer': 'Tiny', 'swimmer': 'Small'}[kind],
            'living': True, 'corrupted': False, 'abilities': {'STR': 8, 'DEX': 12, 'CON': 10, 'INT': 3, 'WIS': 10, 'CHA': 6},
            'ordinaryMaximumHP': maximum, 'ordinaryCurrentHP': hp, 'maximumHP': maximum, 'currentHP': hp,
            'nativeMovement': {'ground': {'walkFeet': 30}, 'flyer': {'walkFeet': 10, 'flyFeet': 30}, 'swimmer': {'swimFeet': 30}}[kind],
            'anatomy': {'ground': ['bite', 'legs'], 'flyer': ['peck', 'wings', 'legs'], 'swimmer': ['bite', 'fins']}[kind],
            'breathing': 'water' if kind == 'swimmer' else 'air', 'conditions': ['prior-condition'], 'injuries': ['prior-injury'],
            'relations': {sid: {'willing': True, 'tamed': False}}, 'lawfulAccess': [sid], 'custody': sid,
            'currentBonds': [], 'keenSenses': senses or [], 'version': 1, 'mode': 'ordinary',
            'activeProfile': None, 'controlOwner': None, 'pendingCommand': None,
            'budgets': {'round': 8, 'phaseSpent': True, 'attackSpent': True, 'movementFeetSpent': 20, 'reactionSpent': True},
            'mountFacts': {'tack': False, 'riderGeometryEligible': False, 'loadChecked': False}}

    def world(paid=True, animal=True, handling=True, earned=True):
        w = CompanionLifecycle('conditional-lifecycle-world', supplements['SUP-02'])
        w.add_owner('owner', history(handling, earned))
        if paid:
            w.purchase('owner', 0)
        if animal:
            w.add_body(body())
        return w

    def finish(w, sid='owner', start=0, bid='animal', template='feat-animal.ground', sense=None):
        w.start(sid, start, bid, template, sense)
        w.uninterrupted_work(sid, start + HOUR, support)
        w.complete(sid, start + HOUR, w.completion_evidence(sid))

    def rest(w, when=DAY, sid='owner', rid=None):
        r = {'id': rid or f'LR:{sid}:{when}', 'ownerId': sid, 'worldId': w.world_id,
            'start': when - 8 * HOUR, 'end': when, 'kind': 'LR', 'evidenceMode': 'conditional_fixture',
            'safe': True, 'supported': True, 'uninterrupted': True, 'beneficialEligible': True, 'debtOnly': False}
        w.beneficial_rest(sid, when, r); return r

    def release(w, start=HOUR, sid='owner'):
        w.start_release(sid, start)
        no_touch = {**support, 'touch': False}
        w.uninterrupted_work(sid, start + HOUR, no_touch, release=True)
        w.complete_release(sid, start + HOUR)

    group = 'ACQ05-T01'
    w = world(animal=False); o = w.owners['owner']
    check('paid-owned-one-attempt-no-body-or-rest', o['history'].pay.has('animal_companion') and o['attempts'] == 1 and not w.bodies and o['lastRest'] is None and o['bond'] is None)
    check('purchase-choice-has-no-locked-animal', o['grant']['record']['choice'] is None)
    trace('purchase-with-no-animal', w)

    group = 'ACQ05-T02'
    for label, handling, earned in [('missing-proficiency', False, True), ('missing-opportunity', True, False)]:
        w = world(paid=False, handling=handling, earned=earned)
        reject(label, w, lambda: w.purchase('owner', 0)); trace(label, w)
    w = world(); reject('duplicate-does-not-reinitialize', w, lambda: w.purchase('owner', 0))
    w.cancel_purchase_proposal('owner', 1)
    check('cancel-after-purchase-does-not-refund', len(w.owners['owner']['history'].pay.grants) == 1 and w.owners['owner']['attempts'] == 1)
    w = world(paid=False); w.cancel_purchase_proposal('owner', 0)
    check('cancel-before-purchase-no-payment', not w.owners['owner']['history'].pay.grants)
    w.purchase('owner', 1); trace('cancel-then-legitimate-purchase', w)

    group = 'ACQ05-T03'
    w = world(); ordinary = deepcopy(w.bodies['animal']); w.start('owner', 1, 'animal')
    check('attempt-spent-at-start-no-chassis', w.owners['owner']['attempts'] == 0 and w.bodies['animal'] == ordinary and w.owners['owner']['pending'] is not None)
    w.uninterrupted_work('owner', 1801, support)
    check('half-hour-no-bond', w.owners['owner']['bond'] is None)
    w.uninterrupted_work('owner', 3601, support); w.complete('owner', 3601, w.completion_evidence('owner'))
    check('one-bond-no-extra-payment-or-RP', w.owners['owner']['bond'] is not None and len(w.owners['owner']['history'].pay.grants) == 1 and w.owners['owner']['rp'] == 7)
    trace('ordered-paid-start-completion', w)

    group = 'ACQ05-T04'
    for kind, size, hp, maximum, senses, selected, expected in [
        ('ground', 'Small', 5, 10, [], None, 4), ('ground', 'Medium', 1, 20, ['hearing', 'smell'], 'smell', 1),
        ('flyer', 'Tiny', 3, 7, ['sight'], 'sight', 3), ('swimmer', 'Small', 7, 10, ['hearing'], 'hearing', 6)]:
        w = world(animal=False); w.add_body(body(kind=kind, size=size, hp=hp, maximum=maximum, senses=senses))
        finish(w, template='feat-animal.' + kind, sense=selected); b = w.bodies['animal']
        check(kind + size + '/ratio', (b['currentHP'], b['maximumHP']) == (expected, 9))
        check(kind + size + '/physical-preserved', b['injuries'] == ['prior-injury'] and b['conditions'] == ['prior-condition'] and b['activeProfile']['breathing'] == b['breathing'])
        w.growth('owner', 3601, 8)
        check(kind + size + '/growth-no-heal-or-reset', (b['currentHP'], b['maximumHP'], w.owners['owner']['attempts']) == (expected, 13, 0))
        trace(kind + size, w)

    group = 'ACQ05-T05'
    changes = {'missing-HP': lambda b: b.pop('ordinaryCurrentHP'), 'INT7': lambda b: b['abilities'].update(INT=7),
        'wrong-type': lambda b: b.update(creatureType='Construct'), 'size': lambda b: b.update(size='Large'),
        'native-movement': lambda b: b.update(nativeMovement={}), 'anatomy': lambda b: b.update(anatomy=['legs']),
        'access': lambda b: b.update(lawfulAccess=[]), 'relationship': lambda b: b.update(relations={}),
        'Ranger-bond': lambda b: b.update(currentBonds=['native-ranger-bond']),
        'feat-bond': lambda b: b.update(currentBonds=['another-owner-feat']), 'zero-HP': lambda b: b.update(currentHP=0, ordinaryCurrentHP=0),
        'corrupted': lambda b: b.update(corrupted=True), 'dead': lambda b: b.update(living=False),
        'wrong-world': lambda b: b.update(worldId='other-world')}
    for label, mutate in changes.items():
        w = world(); mutate(w.bodies['animal'])
        reject(label, w, lambda: w.start('owner', 1, 'animal'))
        check(label + '/prior-paid-grant-retained', w.owners['owner']['grant'] is not None and w.owners['owner']['attempts'] == 1)
        trace(label, w)
    w = world(); reject('invented-sense', w, lambda: w.start('owner', 1, 'animal', sense='smell'))
    w.start('owner', 1, 'animal'); reject('second-pending-start', w, lambda: w.start('owner', 2, 'animal'))
    w.add_owner('receiver', history()); w.purchase('receiver', 2)
    w.bodies['animal']['relations']['receiver'] = {'willing': True}; w.bodies['animal']['lawfulAccess'].append('receiver')
    reject('same-body-reservation', w, lambda: w.start('receiver', 2, 'animal')); trace('reservations', w)

    group = 'ACQ05-T06'
    for label in ['touch', 'access', 'both-relations', 'INT7', 'incapacitation', 'proficiency', 'abandonment', 'animal-death', 'owner-death']:
        w = world(); w.start('owner', 0, 'animal'); w.uninterrupted_work('owner', 1200, support)
        if label in ['touch', 'abandonment']:
            w.interrupt('owner', 1200, label)
        elif label == 'access':
            w.body_change('animal', 1200, {'lawfulAccess': []}, label)
        elif label == 'both-relations':
            w.body_change('animal', 1200, {'relations': {}}, label)
        elif label == 'INT7':
            w.body_change('animal', 1200, {'abilities': {**w.bodies['animal']['abilities'], 'INT': 7}}, label)
        elif label == 'animal-death':
            w.body_change('animal', 1200, {'currentHP': 0, 'living': False}, label)
        else:
            w.owner_change('owner', 1200, **{'incapacitation': {'able': False}, 'proficiency': {'handlingAvailable': False}, 'owner-death': {'alive': False}}[label])
        check(label + '/spent-and-no-chassis', w.owners['owner']['pending'] is None and w.owners['owner']['bond'] is None and w.owners['owner']['attempts'] == 0 and w.bodies['animal']['activeProfile'] is None)
        reject(label + '/no-resume', w, lambda: w.complete('owner', 3600, {})); trace(label, w)
    w = world(); w.bodies['animal']['relations']['owner']['tamed'] = True
    w.start('owner', 0, 'animal'); w.uninterrupted_work('owner', 1200, support)
    w.body_change('animal', 1200, {'relations': {'owner': {'willing': False, 'tamed': True}}}, 'willingness-only-lost')
    check('independent-tamed-alternative-still-valid', w.owners['owner']['pending'] is not None)
    w.uninterrupted_work('owner', HOUR, support); w.complete('owner', HOUR, w.completion_evidence('owner')); trace('literal-OR-retained', w)

    group = 'ACQ05-T07'
    w = world(); w.start('owner', 0, 'animal'); w.interrupt('owner', 1200, 'touch-loss')
    for n, label in enumerate(['scene', 'controller', 'date', 'location', 'target'], 1):
        w.event(1200 + n, 'label-change', label=label)
        if label == 'target':
            w.add_body(body(bid='another-animal'))
        reject(label + '/no-retry', w, lambda: w.start('owner', 1200 + n, 'another-animal' if label == 'target' else 'animal'))
    trace('no-label-reset', w)

    group = 'ACQ05-T08'
    rest(w); check('genuine-rest-sets-one', w.owners['owner']['attempts'] == 1 and w.bodies['animal']['currentHP'] == 5)
    finish(w, start=DAY); rest(w, 2 * DAY)
    check('repeated-genuine-rest-not-banked', w.owners['owner']['attempts'] == 1 and w.bodies['animal']['currentHP'] == 4)
    rest(w, 3 * DAY); check('never-two', w.owners['owner']['attempts'] == 1)
    check('failure-history-retained', any(x['outcome'].startswith('interrupted') for x in w.work)); trace('real-owner-recovery', w)

    group = 'ACQ05-T09'
    for label, patch in [('short-rest', {'kind': 'SR'}), ('debt-only', {'debtOnly': True}),
        ('unsupported', {'supported': False}), ('unsafe', {'safe': False}), ('ineligible', {'beneficialEligible': False}),
        ('interrupted', {'uninterrupted': False}), ('wrong-owner', {'ownerId': 'receiver'}), ('wrong-world', {'worldId': 'elsewhere'}),
        ('short-duration', {'start': DAY - 7 * HOUR})]:
        w = world(); w.start('owner', 0, 'animal'); w.interrupt('owner', 1200, 'touch')
        r = {'id': label, 'ownerId': 'owner', 'worldId': w.world_id, 'start': DAY - 8 * HOUR, 'end': DAY,
            'kind': 'LR', 'evidenceMode': 'conditional_fixture', 'safe': True, 'supported': True,
            'uninterrupted': True, 'beneficialEligible': True, 'debtOnly': False, **patch}
        reject(label, w, lambda: w.beneficial_rest('owner', DAY, r)); trace(label, w)
    w = world(); r = rest(w); w.start('owner', DAY, 'animal'); w.interrupt('owner', DAY, 'abandonment')
    reject('duplicate-receipt', w, lambda: w.beneficial_rest('owner', DAY, r))
    r = {**r, 'id': 'too-soon', 'start': 2 * DAY - 8 * HOUR - 1, 'end': 2 * DAY - 1}
    reject('23h59m59s-since-prior', w, lambda: w.beneficial_rest('owner', 2 * DAY - 1, r)); trace('epoch-boundaries', w)
    for releasing in [False, True]:
        w = world()
        if releasing:
            finish(w); w.start_release('owner', DAY - HOUR)
        else:
            w.start('owner', DAY - HOUR, 'animal')
        r = {'id': 'overlap', 'ownerId': 'owner', 'worldId': w.world_id, 'start': DAY - 8 * HOUR, 'end': DAY,
            'kind': 'LR', 'evidenceMode': 'conditional_fixture', 'safe': True, 'supported': True,
            'uninterrupted': True, 'beneficialEligible': True, 'debtOnly': False}
        reject('release-overlap' if releasing else 'bond-overlap', w, lambda: w.beneficial_rest('owner', DAY, r)); trace('overlap-' + str(releasing), w)

    group = 'ACQ05-T10'
    w = world(); finish(w); rest(w); w.add_body(body(bid='second'))
    bond = deepcopy(w.owners['owner']['bond'])
    reject('existing-bond-prevents-exchange', w, lambda: w.start('owner', DAY, 'second'))
    check('old-bond-and-unspent-charge-preserved', w.owners['owner']['bond'] == bond and w.owners['owner']['attempts'] == 1); trace('no-success-only-swap', w)

    group = 'ACQ05-T11'
    w.start_release('owner', DAY + 1); w.uninterrupted_work('owner', DAY + 1201, support, release=True)
    w.interrupt('owner', DAY + 1201, 'incapacity', release=True)
    check('interrupted-release-keeps-bond', w.owners['owner']['bond'] == bond and w.owners['owner']['attempts'] == 1)
    reject('cannot-resume-partial-release', w, lambda: w.complete_release('owner', DAY + 3601))
    release(w, DAY + 1201)
    check('new-full-hour-costs-no-charge-or-RP', w.owners['owner']['attempts'] == 1 and w.owners['owner']['rp'] == 7 and len(w.owners['owner']['history'].pay.grants) == 1)
    trace('fresh-release-no-touch-rule', w)

    group = 'ACQ05-T12'
    b = w.bodies['animal']; check('restored-4-of10-same-body', (b['currentHP'], b['maximumHP'], b['id'], b['custody']) == (4, 10, 'animal', 'owner'))
    check('restored-injury-and-condition', b['injuries'] == ['prior-injury'] and b['conditions'] == ['prior-condition'])
    reject('old-unused-attempt-not-post-end-rest', w, lambda: w.start('owner', DAY + 4801, 'animal'))
    rest(w, 2 * DAY); finish(w, start=2 * DAY)
    check('owned-feat-replacement-without-rebuy', len(w.owners['owner']['history'].pay.grants) == 1 and w.bodies['animal']['currentHP'] == 3); trace('post-release-gate', w)
    w = world(); finish(w); rest(w)
    w.body_change('animal', 2 * DAY, {'currentHP': 0, 'living': False}, 'death-during-owner-rest')
    # Rest began eight hours before the bond ended; completion is later in the
    # existing same-time event sequence. No owner work overlapped this interval.
    rest(w, 2 * DAY); w.add_body(body(bid='replacement'))
    w.start('owner', 2 * DAY, 'replacement')
    check('rest-completion-after-end-not-start-after-end', w.owners['owner']['pending'] is not None)
    trace('same-time-ordered-end-then-rest', w)

    group = 'ACQ05-T13'
    for mode in ['animal', 'owner']:
        w = world(); finish(w); budgets = deepcopy(w.bodies['animal']['budgets'])
        w.bodies['animal']['pendingCommand'] = 'previous-legal-unexecuted-command'
        if mode == 'animal':
            w.body_change('animal', 4000, {'currentHP': 0, 'living': False}, 'actual-lethal-damage')
        else:
            w.owner_change('owner', 4000, alive=False)
        b = w.bodies['animal']; o = w.owners['owner']
        check(mode + '/bond-end-no-charge-reset', o['bond'] is None and o['attempts'] == 0 and o['lastEnd'] is not None)
        check(mode + '/distinct-physical-outcome', (b['mode'], b['currentHP']) == (('corpse', 0) if mode == 'animal' else ('ordinary', 4)))
        check(mode + '/budgets-preserved-control-ended', b['budgets'] == budgets and b['pendingCommand'] is None and b['controlOwner'] is None)
        if mode == 'animal':
            rest(w); reject('corpse-no-rebond-after-rest', w, lambda: w.start('owner', DAY, 'animal'))
        trace(mode + '-death', w)

    group = 'ACQ05-T14'
    w = world(); finish(w); release(w); rest(w); w.start('owner', DAY, 'animal'); w.interrupt('owner', DAY + 1200, 'abandoned-replacement')
    check('old-bond-stays-ended-new-charge-spent', w.owners['owner']['bond'] is None and w.owners['owner']['attempts'] == 0 and w.bodies['animal']['mode'] == 'ordinary')
    reject('no-same-epoch-replacement-retry', w, lambda: w.start('owner', DAY + 1200, 'animal'))
    rest(w, 2 * DAY); finish(w, start=2 * DAY)
    check('same-physical-individual-rebond', len(w.bodies) == 1 and w.bodies['animal']['currentHP'] == 3 and len(w.owners['owner']['history'].pay.grants) == 1)
    trace('failure-and-later-rebond', w)

    group = 'ACQ05-T15'
    w = world(); w.add_owner('receiver', history()); w.purchase('receiver', 0)
    finish(w); release(w)
    w.body_change('animal', 7200, {'custody': 'receiver', 'lawfulAccess': ['receiver'], 'relations': {'receiver': {'willing': True}}}, 'conditional-lawful-custody-transfer')
    finish(w, sid='receiver', start=7200)
    check('receiver-own-payment-attempt-hour', len(w.owners['receiver']['history'].pay.grants) == 1 and w.owners['receiver']['attempts'] == 0)
    check('sender-cooldown-not-transferred', w.owners['owner']['lastEnd'] is not None and w.owners['owner']['lastRest'] is None and w.owners['receiver']['lastEnd'] is None)
    check('same-animal-receiving-profile-no-heal', len(w.bodies) == 1 and w.bodies['animal']['currentHP'] == 3); trace('existing-owner-receives', w)
    # A receiver with their own just-ended bond must clear their own gate.
    release(w, 10800, 'receiver')
    rest(w, DAY, 'owner')
    reject('sender-rest-cannot-clear-receiver-gate', w, lambda: w.start('receiver', DAY, 'animal'))
    trace('own-rest-history-required', w)

    group = 'ACQ05-T16'
    w = world(paid=False); reject('custody-not-feat-grant', w, lambda: w.start('owner', 0, 'animal'))
    w.purchase('owner', 0); finish(w); check('legitimate-first-purchase-route', len(w.owners['owner']['history'].pay.grants) == 1); trace('nonowner-first-purchase', w)
    card = read(ranger_path)['cards'][29]
    actor = {'id': 'ranger', 'evidenceMode': 'conditional_fixture', 'rangerLevel': 16, 'heroPath': 'Warder',
        'selectedFeature': {'featureId': card['id'], 'acquisition': 'selection', 'earnedSlot': 'conditional-source-qualified-Ranger16-Hero-choice', 'committed': True}}
    beast = body(sid='ranger'); beast['CR'] = 16
    work = {'ownerId': 'ranger', 'bodyId': 'animal', 'worldId': beast['worldId'], 'evidenceMode': 'conditional_fixture',
        'seconds': 3600, 'touchSeconds': 3600, 'interruptions': [], 'nativeAttemptAvailable': True, 'paidRP': 4, 'rpBefore': 7, 'rpAfter': 3}
    result = validate_ranger_receiving_history(card, actor, beast, work)
    check('conditional-selected-Ranger16-native-paid-hour', result['status'].endswith('established') and not result['rangerGrantCreated'] and not result['nativeChassisInstalled'])
    for label, area, patch in [('level15', 'actor', {'rangerLevel': 15}), ('wrong-Hero', 'actor', {'heroPath': 'Stalker'}),
        ('no-selected-feature', 'actor', {'selectedFeature': {}}), ('over-CR', 'beast', {'CR': 17}),
        ('still-bonded', 'beast', {'currentBonds': ['outgoing']}), ('dead', 'beast', {'living': False}),
        ('not-Beast', 'beast', {'creatureType': 'Construct'}), ('corrupted', 'beast', {'corrupted': True}),
        ('no-access', 'beast', {'lawfulAccess': []}), ('no-relationship', 'beast', {'relations': {}}),
        ('free-RP', 'work', {'paidRP': 0}), ('no-affordable-RP', 'work', {'rpBefore': 3, 'rpAfter': -1}),
        ('short-hour', 'work', {'seconds': 3599}), ('no-touch', 'work', {'touchSeconds': 0}),
        ('interrupted', 'work', {'interruptions': ['contact']}), ('already-used', 'work', {'nativeAttemptAvailable': False})]:
        parts = {'actor': deepcopy(actor), 'beast': deepcopy(beast), 'work': deepcopy(work)}; parts[area].update(patch)
        try:
            validate_ranger_receiving_history(card, parts['actor'], parts['beast'], parts['work'])
        except ValueError as error:
            check(label, True); results[-1]['rejection'] = str(error)
        else:
            check(label, False)
    traces.append({'group': group, 'id': 'Ranger-conditional-native-gates', 'actor': actor, 'beast': beast, 'paidWork': work,
        'result': result, 'limitation': 'Selected feature and native allowance are explicitly conditional prior facts; this is not a complete Ranger build, chassis simulation or invented Ranger payment/termination timing.'})

    group = 'ACQ05-T17'
    for engine in ['ranger', 'other-feat']:
        w = world(); w.bodies['animal']['currentBonds'] = [engine + '-actual-outgoing-bond']
        reject(engine + '/custody-insufficient', w, lambda: w.start('owner', 0, 'animal'))
        reject(engine + '/feat-cannot-release-outgoing-other-engine', w, lambda: w.start_release('owner', 0)); trace(engine, w)

    group = 'ACQ05-T18'
    w = world(); before = deepcopy(w.bodies['animal']); actor_budget = deepcopy(w.owners['owner']['actorBudgets'])
    w.start('owner', 0, 'animal'); stale = w.completion_evidence('owner'); w.uninterrupted_work('owner', 1200, support)
    w.body_change('animal', 1200, {'currentHP': 2, 'injuries': ['prior-injury', 'new-injury']}, 'real-damage-during-hour')
    w.growth('owner', 1200, 8); w.uninterrupted_work('owner', HOUR, support)
    reject('stale-body-version-not-reused', w, lambda: w.complete('owner', HOUR, stale))
    w.complete('owner', HOUR, w.completion_evidence('owner')); b = w.bodies['animal']
    check('latest-HP-and-owner-level', (b['currentHP'], b['maximumHP']) == (2, 13) and b['injuries'] == ['prior-injury', 'new-injury'])
    check('physical-budgets-and-mount-gates-unmodified', b['budgets'] == before['budgets'] and b['mountFacts'] == before['mountFacts'] and w.owners['owner']['actorBudgets'] == actor_budget)
    release(w)
    check('release-no-budget-refund', w.bodies['animal']['budgets'] == before['budgets'] and w.bodies['animal']['currentHP'] == 1)
    procedure = (V / 'ACQ05_ANIMAL_COMPANION_OPERATIVE.txt').read_text(encoding='utf-8')
    check('retained-explicit-phase-and-mount-contract', all(t in procedure for t in ['elects one compatible route before that round', 'actual load, tack, rider geometry', 'preserves all already-spent allowances']))
    trace('current-state-conservation', w)

    group = 'ACQ05-T19'
    for label in ['short', 'missing', 'wrong-body', 'wrong-owner', 'wrong-world', 'wrong-attempt', 'missing-continuity']:
        w = world(); w.start('owner', 0, 'animal'); evidence = w.completion_evidence('owner')
        if label not in ['short', 'missing-continuity']:
            w.uninterrupted_work('owner', HOUR, support)
        if label == 'missing': evidence = None
        for key, case in [('bodyId', 'wrong-body'), ('ownerId', 'wrong-owner'), ('worldId', 'wrong-world'), ('attemptId', 'wrong-attempt')]:
            if label == case: evidence[key] = 'different'
        reject(label, w, lambda: w.complete('owner', 3599 if label == 'short' else HOUR, evidence))
        check(label + '/paid-and-spent-history-retained', w.owners['owner']['attempts'] == 0 and len(w.owners['owner']['history'].pay.grants) == 1)
        trace(label, w)
    for key in ['actualWork', 'uninterrupted', 'noIncompatibleOverlap', 'withinWorkWatchAllowance', 'touch']:
        w = world(); w.start('owner', 0, 'animal')
        reject('unsupported-work/' + key, w, lambda: w.uninterrupted_work('owner', HOUR, {**support, key: False}))
        check('no-refund-after-rejected-work/' + key, w.owners['owner']['attempts'] == 0)
    w = world(); w.start('owner', 0, 'animal'); w.interrupt('owner', 1200, 'abandonment')
    reject('already-interrupted-no-completion', w, lambda: w.complete('owner', HOUR, {})); trace('interrupted-record-cannot-be-rewritten', w)

    group = 'ACQ05-T20'
    w = world(animal=False); h = w.owners['owner']['history']
    check('owned-parent-OR-node-without-animal', h.pay.has('animal_companion') and h.prerequisite('companion_training'))
    reject('child-cannot-reuse-paid-parent-opportunity', w, lambda: h.acquire_named('companion_training', 4))
    w.growth('owner', 1, 8); h.earn(8); h.acquire_named('companion_training', 8)
    check('separate-Warrior8-child-without-body', [g['opportunity'] for g in h.pay.grants] == ['Warrior:4', 'Warrior:8'] and not w.bodies)
    trace('owned-parent-separate-child', w)
    h = history(); h.acquire_named('companion_training', 4)
    check('independent-handling-alternative-retained', h.pay.has('companion_training') and not h.pay.has('animal_companion'))
    for bound in bindings:
        check('unchanged-source/' + bound['path'], info(G / bound['path']) == bound)
    preservation = read(A / 'FEAT327_ACQ_05_INDEPENDENT_DESCENDANT_CHECK.json')
    check('full-source-preservation-evidence-retained', preservation['checks'] == 272 and not preservation['failures'])
    coverage = [{'id': case['id'], 'title': case['title'], 'expectationStatus': case['executionStatus'],
        'localEvidenceStatus': 'EXECUTED_BOUNDED_CONDITIONAL_REFERENCE_AND_SOURCE_CHECKS',
        'checks': sum(r['group'] == case['id'] for r in results),
        'traces': [t['id'] for t in traces if t['group'] == case['id']]} for case in expectations['cases']]
    assert len(coverage) == 20 and all(row['checks'] and row['traces'] for row in coverage)
    limits = [
        'All animal, relationship, custody, work, rest, prior Ranger selection and class-level attainment facts are explicit conditional premises, not authenticated campaign records.',
        'The model executes named feat lifecycle chronology and HP/control conservation. It does not implement the CRPG, combat/commands, mounted action selection, general physiology, a taming system or all character builds.',
        'Work/rest safety, continuity and Watch-budget support are supplied conditional facts; existing EX58 scheduling is preserved, not reimplemented. Debt-only Rest is denied resource recovery; its separate lawful debt-clearing effects remain outside this model.',
        'The Ranger branch independently checks supplied native feature/eligibility/payment/hour evidence. Its actual prior Hero selection, native allowance and paid cost are conditional premises. No Ranger chassis, release authority, payment-stage timing or feature grant is invented.',
        'The mount interface checks unchanged physical/actor budgets and retained source gates. It does not substitute for the previously reviewed EX58 mounted-phase implementation or claim a mounted combat scenario.',
        'Owner/body changes are named conditional factual events, not new retraining, resurrection or damage-resolution rules. No full335 acquisition, original660-case completion, exact feat review, balance, whole-game approval or cosmology review is claimed.']
    report = {'createdAtUtc': datetime.now(timezone.utc).isoformat(), 'status': 'passed-twenty-bounded-ACQ05-acceptance-groups',
        'sourceBindings': bindings, 'expectationSource': info(expectation_path), 'groupCoverage': coverage,
        'checks': len(results), 'failures': [], 'results': results, 'traces': traces, 'limits': limits,
        'counts': {'groupsAccountedFor': 20, 'recordedTraces': len(traces), 'campaignRecordsAuthenticated': 0,
            'newPartialPrerequisiteIdentities': 0}, 'historicalModelPreserved': True,
        'newRulesAdopted': False, 'runtimeImplemented': False, 'candidateApproved': False,
        'sourceInformationDeleted': False, 'pushed': False, 'cosmologyReviewed': False}
    with target.open('x', encoding='utf-8', newline='\n') as f:
        json.dump(report, f, ensure_ascii=False, indent=2, default=serial); f.write('\n')
    with notes.open('x', encoding='utf-8', newline='\n') as f:
        f.write('# Animal Companion lifecycle — ACQ05 finite acceptance\n\n')
        f.write(f'{len(results)} checks pass across20 named groups and{len(traces)} recorded conditional traces. Purchase, spent start and completion/interruption are distinct ordered events. Release/replacement use the existing feat, and transfer follows the receiving owner’s own history. Four HP endpoints remain4/1/3/6 at maximum9; growth does not heal.\n\n')
        for limit in limits:
            f.write('- ' + limit + '\n')
    print(json.dumps({'report': info(target), 'notes': info(notes), 'checks': len(results),
        'groups': 20, 'traces': len(traces), 'failures': 0, 'runtimeImplemented': False}, indent=2))


if __name__ == '__main__':
    main()
