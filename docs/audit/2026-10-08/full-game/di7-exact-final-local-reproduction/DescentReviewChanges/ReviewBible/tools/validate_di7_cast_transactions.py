"""Execute source-qualified DI7 cast boundaries without certifying payloads."""
from copy import deepcopy
from datetime import datetime, timezone
import json
from apply_di7_ap_as_01 import G, R, A, info, encoded
from di7_cast_transactions import DI7Sources, DI7CastTransactions


def main():
    output = A / 'DI7_CAST_TRANSACTIONS_CHECK.json'
    assert not output.exists()
    sources = DI7Sources(); assertions = []; histories = []

    def check(label, value):
        assert value, label
        assertions.append(label)

    def reject(label, m, fn):
        before = m.snapshot()
        try:
            fn()
        except ValueError as e:
            check(label + ':rejected', bool(str(e)))
        else:
            raise AssertionError(label)
        check(label + ':atomic', m.snapshot() == before)

    def fixture(provider='Wizard', level=13, total=None):
        actor = {'provider': provider, 'classLevel': level, 'totalLevel': total or level, 'abilityScore': 18,
            'attainmentPremise': 'Hypothetical campaign attained the stated class/total levels; no level-up session is authenticated.',
            'heroPath': 'Soothsayer' if provider == 'Shaman' else 'Spellbinder' if provider == 'Wizard' else 'source-eligible-path-with-no-additional-cast-modifiers',
            'specialization': 'Evocation', 'providerRetained': True, 'bookPresent': True, 'studyUninterrupted': True,
            'positionFeet': 0, 'knownFactions': ['faction-A'],
            'body': {'conscious': True, 'canAct': True, 'ordinarySpellProhibited': False, 'silenced': False, 'canSpeak': True, 'reactionLegal': True,
                'hands': {'left': {'usable': True, 'holding': None}, 'right': {'usable': True, 'holding': 'focus-owner'}},
                'focus': {'id': 'focus-owner', 'owner': 'owner', 'qualifiedClasses': [provider], 'accessible': True}}}
        adversary = deepcopy(actor)
        adversary.update(provider='Wizard', classLevel=13, totalLevel=13, heroPath='Spellbinder', positionFeet=20)
        adversary['body']['focus'].update(id='focus-adversary', owner='adversary', qualifiedClasses=['Wizard'])
        actors = {'owner': actor, 'adversary': adversary}
        entities = {}
        for name, position in [('owner', 0), ('adversary', 20), ('target', 30)]:
            entities[name] = {'kind': 'creature', 'positionFeet': position, 'willing': True, 'alliedTo': {'owner': True, 'adversary': True},
                'relatedQuestions': ['Where is the archive key?'], 'hands': {'left': {'usable': True, 'holding': None}}}
        entities['point'] = {'kind': 'point', 'positionFeet': 120, 'relatedQuestions': []}
        relations = {a + '>' + t: {'sourceFact': 'conditional-straight-line-open-space/' + a + '/' + t,
            'perceived': True, 'visible': True, 'lineOfEffect': True} for a in actors for t in entities}
        world = {'entities': entities, 'relations': relations, 'establishedFactions': ['faction-A'],
            'encounter': {'id': 'conditional-real-encounter-1', 'isRealEncounter': True,
                'premise': 'Actual hypothetical opposition starts after completed study; not a manufactured resource refresh.'}}
        m = DI7CastTransactions(sources, actors, world)
        m.begin_turn('owner', 'owner-turn1')
        return m

    def learn(m, sid, actor='owner', at=None):
        level = m.actors[actor]['classLevel'] if at is None else at
        m.learn(actor, sid, level, actor + '/learn/' + sid)

    def prepare(m, actor='owner'):
        if m.actors[actor]['provider'] == 'Wizard':
            m.prepare_wizard(actor, list(m.actors[actor]['learned']), actor + '/study', {'actor': actor, 'completedAt': 0, 'sourceEvent': actor + '/conditional-real-long-rest'})

    def request(sid):
        if sid == 'mass-revelation':
            return {'direction': [1, 0, 0]}
        if sid == 'vision-quest':
            return {'target': 'target', 'question': 'Where is the archive key?'}
        if sid == 'faction-omniscience':
            return {'target': 'target', 'faction': 'faction-A'}
        if sid == 'resonance-sight-supreme':
            return {'target': 'point'}
        return {'target': 'target'}

    def record(label, m):
        histories.append({'id': label, 'conditionalPremises': 'Actor attainment/body/world/rest facts are hypothetical. Learning, preparation, transactions and counters shown below are executed.', 'final': m.snapshot()})

    # Each candidate gets its own legal acquisition slot, not seven free spells
    # learned simultaneously at a level with only one or five additions.
    for sid in sources.cards:
        for provider, level in [('Wizard', 13), ('Cleric', 13), ('Mirrorsage', 20), ('Shaman', 20)]:
            m = fixture(provider, level); learn(m, sid); prepare(m)
            card, op, binding, candidate = m.route('owner', sid)
            check(sid + '/' + provider + ':actual-recorded-route', candidate and card['classAccess'][provider]['rank'] == 7 and binding)
            if sid == 'fate-echo':
                reject(provider + ':no-standalone-Fate-bypass', m, lambda: m.declare('owner', sid, 'cast', {}))
            else:
                p = m.declare('owner', sid, 'cast', request(sid))
                check(sid + '/' + provider + ':commit-cost-budget', p['quote']['cost'] == 17 and m.actors['owner']['rp'] == m.actors['owner']['maxRP'] - 17 and m.actors['owner']['actions'] == 0)
                check(sid + '/' + provider + ':class-specific-strain', p['dissonanceAdded'] == (0 if provider == 'Wizard' else 2))
                result = m.take_payload_resolution('cast')
                check(sid + '/' + provider + ':payload-not-claimed-executed', result['status'] == 'ready-for-payload')
            record('source-qualified-' + provider + '-' + sid, m)

    for provider, level, total in [('Wizard', 12, 20), ('Cleric', 12, 20), ('Mirrorsage', 18, 20), ('Shaman', 18, 20)]:
        m = fixture(provider, level, total)
        reject(provider + ':total-level-no-rank-bypass', m, lambda: learn(m, 'alignment-purge'))
        record('below-source-class-gate-' + provider, m)
    for provider in ['Mirrorsage', 'Shaman']:
        m = fixture(provider, 19)
        # The minimum access row is19, but the shared repertoire fallback grants
        # additions at even levels. No invented level19 learning opportunity.
        check(provider + ':minimum-access19', sources.ordinary['alignment-purge']['classAccess'][provider]['minimumClassLevel'] == 19)
        reject(provider + ':rank-access-is-not-learning', m, lambda: learn(m, 'alignment-purge'))
        record(provider + '-19-unearned-repertoire', m)
    m = fixture(); reject('RP-and-level-not-repertoire', m, lambda: m.declare('owner', 'alignment-purge', 'no-learn', request('alignment-purge'))); record('not-acquired', m)
    m = fixture(); learn(m, 'alignment-purge'); reject('book-is-not-prepared', m, lambda: m.declare('owner', 'alignment-purge', 'no-prepare', request('alignment-purge'))); record('book-only', m)
    m = fixture('Shaman', 20); learn(m, 'alignment-purge'); m.actors['owner']['heroPath'] = 'Bloodcaller'
    reject('Bloodcaller-real-loss', m, lambda: m.declare('owner', 'alignment-purge', 'bad', request('alignment-purge'))); record('Bloodcaller-retains-pool-not-spells', m)

    mutations = [('silence', lambda a: a['body'].update(silenced=True)), ('speech', lambda a: a['body'].update(canSpeak=False)),
        ('somatic', lambda a: a['body']['hands']['left'].update(holding='sword')), ('wrong-focus-owner', lambda a: a['body']['focus'].update(owner='adversary')),
        ('wrong-focus-class', lambda a: a['body']['focus'].update(qualifiedClasses=['Oracle'])), ('focus-inaccessible', lambda a: a['body']['focus'].update(accessible=False)),
        ('no-RP', lambda a: a.update(rp=0)), ('Fractured', lambda a: a.update(dissonance=17)), ('lost-provider', lambda a: a.update(providerRetained=False)),
        ('incapacity', lambda a: a['body'].update(canAct=False)), ('no-action', lambda a: a.update(actions=0))]
    for label, mutate in mutations:
        m = fixture(); learn(m, 'alignment-purge'); prepare(m); mutate(m.actors['owner'])
        reject(label, m, lambda: m.declare('owner', 'alignment-purge', 'bad', request('alignment-purge'))); record('gate-' + label, m)
    for label, change in [('range', lambda m: m.world['entities']['target'].update(positionFeet=120.01)),
        ('line', lambda m: m.world['relations']['owner>target'].update(lineOfEffect=False)),
        ('perception', lambda m: m.world['relations']['owner>target'].update(perceived=False))]:
        m = fixture(); learn(m, 'alignment-purge'); prepare(m); change(m)
        reject('actual-target-' + label, m, lambda: m.declare('owner', 'alignment-purge', 'bad', request('alignment-purge'))); record('target-' + label, m)

    # No target alignment or institutional membership is queried at precommit.
    m = fixture(); learn(m, 'faction-omniscience'); prepare(m)
    m.world['entities']['target']['privateMembership'] = []
    p = m.declare('owner', 'faction-omniscience', 'paid', request('faction-omniscience'))
    check('hidden-nonmember-still-pays-before-payload', p['quote']['cost'] == 17 and m.actors['owner']['rp'] == 31)
    record('faction-public-preflight-not-membership-oracle', m)

    for d, expected_cost in [(0, 17), (11, 18), (14, 19)]:
        m = fixture(); learn(m, 'alignment-purge'); prepare(m); m.actors['owner']['dissonance'] = d
        p = m.declare('owner', 'alignment-purge', 'paid', request('alignment-purge'))
        check('actual-before-cast-surcharge-' + str(d), p['quote']['cost'] == expected_cost)
        record('price-band-' + str(d), m)
    m = fixture(); learn(m, 'mass-revelation'); prepare(m)
    m.declare('owner', 'mass-revelation', 'first', request('mass-revelation')); m.take_payload_resolution('first')
    m.begin_turn('owner', 'owner-turn2'); p = m.declare('owner', 'mass-revelation', 'second', request('mass-revelation'))
    check('same-family-refrain-not-new-exemption', p['quote']['refrain'] == 1 and p['dissonanceAdded'] == 3 and m.actors['owner']['rp'] == 14)
    record('prepared-family-repeat', m)

    def counter_scene():
        m = fixture(); learn(m, 'alignment-purge'); learn(m, 'counterspell', at=5); prepare(m)
        learn(m, 'counterspell', actor='adversary', at=5); prepare(m, 'adversary')
        m.actors['owner']['concentration'] = 'conditional-prior-concentration'
        m.declare('owner', 'alignment-purge', 'outer', request('alignment-purge'))
        return m

    for face, success in [(15, True), (14, False), (20, True), (1, False)]:
        m = counter_scene(); m.declare('adversary', 'counterspell', 'counter', {'pendingCast': 'outer'})
        result = m.resolve_counter('counter', face)
        check('counter-rank7-core-task-' + str(face), result['success'] == success and result['total'] == face + 9)
        check('counter-own-payment-no-parent-refund', m.actors['adversary']['rp'] == 43 and m.actors['owner']['rp'] == 31)
        check('old-concentration-never-restored', m.actors['owner']['concentration'] != 'conditional-prior-concentration')
        if success:
            reject('countered-no-payload', m, lambda: m.take_payload_resolution('outer'))
        else:
            m.actors['adversary']['reactions'] = 1  # Conditional distinct permission: no second attempt against same pending cast.
            reject('extra-Reaction-no-retry-same-cast', m, lambda: m.declare('adversary', 'counterspell', 'retry', {'pendingCast': 'outer'}))
            m.take_payload_resolution('outer')
        record('counter-face-' + str(face), m)
    m = counter_scene(); m.declare('adversary', 'counterspell', 'counter', {'pendingCast': 'outer'})
    m.declare('owner', 'counterspell', 'counter-counter', {'pendingCast': 'counter'})
    history = {k: deepcopy(m.actors['owner'][k]) for k in ['rp', 'previousSpell', 'refrain', 'dissonance']}
    m.resolve_counter('counter-counter', 12)
    check('nested-counter-negates-counter-only', m.casts['counter']['status'] == 'countered' and m.stack == ['outer'])
    m.take_payload_resolution('outer')
    check('parent-resumption-no-new-price-or-history', history == {k: m.actors['owner'][k] for k in history} and history['previousSpell'] == 'counterspell' and history['rp'] == 26)
    record('nested-LIFO-parent-history', m)
    m = counter_scene(); m.actors['owner']['body']['canAct'] = False
    r = m.take_payload_resolution('outer')
    check('postcommit-incapacity-keeps-costs', r['status'] == 'interrupted-no-refund' and m.actors['owner']['rp'] == 31 and m.actors['owner']['concentration'] is None)
    record('postcommit-incapacity', m)

    check('all-source-bytes-remain-current', all(info(G / x['path']) == x for x in sources.bindings))
    report = {'recordedAtUtc': datetime.now(timezone.utc).isoformat(), 'status': 'pass', 'checks': len(assertions), 'passedChecks': assertions, 'failures': [],
        'sourceBindings': sources.bindings + [info(R / 'tools/di7_cast_transactions.py'), info(R / 'tools/validate_di7_cast_transactions.py'),
            info(R / 'tools/spell_playtest_rules.py'), info(R / 'tools/core_playtest_rules.py')],
        'historyCount': len(histories), 'histories': histories,
        'scope': 'Recorded ranked learning and Wizard study/preparation; actual conditional RP/budget/components/target/public-reference checks, class-specific base strain, concentration displacement and nested ordinary Counterspell. Payload boundaries are explicitly ready-for-payload, never claimed resolved.',
        'sourceAccessFinding': 'Mirrorsage/Shaman rank7 minimum access is19, but the shared fallback provides no new ranked learning addition at odd level19. Positive learned-cast fixtures use the real level20 addition. A level19 route would need a separate actual source-qualified acquisition; no new learning rule or automatic repertoire is invented.',
        'candidatePermission': 'The seven unapproved complete candidates are evaluated only in hypothetical acceptance fixtures. The common quote helper receives a local status projection; actual source/card/index flags and exact-review status remain unchanged.',
        'remaining': ['Fate Echo atomic forecasting/reservation/child commitment and Ready exception.', 'Actual spell payload adapters and all49 complete expectations.',
            'Actual Shaman totem aura vent; these cases supply no totem and grant no class-only vent.', 'Full character build, general world geometry, source facts, initiative timing and real campaign evidence.'],
        'all49FiniteVariantsFulfilled': False, 'exactCardsApproved': False, 'runtimeImplemented': False, 'humanBalanceApproved': False, 'cosmologyReviewed': False, 'pushed': False}
    output.write_bytes(encoded(report))
    print(json.dumps({'report': info(output), 'checks': len(assertions), 'histories': len(histories), 'fullFiniteFulfilled': False}))


if __name__ == '__main__':
    main()
