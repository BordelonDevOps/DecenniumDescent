"""Fate Echo conditional paid composites, actual source outcomes and Ready traces."""
from copy import deepcopy
from datetime import datetime, timezone
from apply_di7_ap_as_01 import G, R, A, info, encoded
from di7_cast_transactions import DI7Sources
from di7_fate_transactions import FateTransactions
import json


def main():
    output = A / 'DI7_FATE_TRANSACTIONS_CHECK.json'; assert not output.exists()
    sources = DI7Sources(); checks = []; histories = []

    def check(label, value):
        assert value, label
        checks.append(label)

    def reject(label, m, fn):
        before = m.snapshot()
        try: fn()
        except ValueError as error: check(label + '/rejected', bool(str(error)))
        else: raise AssertionError(label)
        check(label + '/atomic', before == m.snapshot())

    def make(provider='Wizard', *, original_sid='fate-coin', ready_original=False, owner_knows_child=False):
        level = 13 if provider in {'Wizard', 'Cleric'} else 20
        actors = {}
        for actor_id, cls, lv, position in [('owner', provider, level, 0), ('donor', 'Wizard', 13, 10), ('counter', 'Wizard', 13, 20)]:
            actors[actor_id] = {'provider': cls, 'classLevel': lv, 'totalLevel': lv, 'abilityScore': 18,
                'attainmentPremise': 'Explicit hypothetical attained-level ordinary-casting slice; not a full character build or campaign record.',
                'heroPath': 'Soothsayer' if cls == 'Shaman' else 'Spellbinder' if cls == 'Wizard' else 'ordinary-provider-retained-no-extra-modifier-premise',
                'specialization': 'Evocation', 'providerRetained': True, 'bookPresent': True, 'studyUninterrupted': True, 'positionFeet': position, 'knownFactions': [],
                'body': {'conscious': True, 'canAct': True, 'ordinarySpellProhibited': False, 'silenced': False, 'canSpeak': True, 'reactionLegal': True,
                    'hands': {'left': {'usable': True, 'holding': None}, 'right': {'usable': True, 'holding': 'focus/' + actor_id}},
                    'focus': {'id': 'focus/' + actor_id, 'owner': actor_id, 'qualifiedClasses': [cls], 'accessible': True}}}
        entities = {}
        for actor_id, position in [('owner', 0), ('donor', 10), ('counter', 20), ('originalRecipient', 15), ('target', 25)]:
            entities[actor_id] = {'kind': 'creature', 'positionFeet': position, 'willing': True, 'alliedTo': {x: True for x in actors}, 'relatedQuestions': [],
                'hands': deepcopy(actors[actor_id]['body']['hands']) if actor_id in actors else {'left': {'usable': True, 'holding': None}, 'right': {'usable': True, 'holding': None}}}
        alignments = {k: {'underlying': {'order': 'Lawful', 'ethics': 'Good'}, 'immunities': [],
            'permanentIdentity': {'id': k}, 'acquisitionSnapshots': [], 'usedAllowances': {}} for k in entities}
        alignments['donor']['underlying'] = {'order': 'Chaotic', 'ethics': 'Evil'}
        alignments['target']['underlying'] = {'order': 'Chaotic', 'ethics': 'Evil'}
        world = {'entities': entities, 'alignmentActors': alignments, 'establishedFactions': [],
            'relations': {a + '>' + t: {'sourceFact': 'conditional-open-straight-line/' + a + '/' + t, 'perceived': True, 'visible': True, 'lineOfEffect': True} for a in actors for t in entities},
            'encounter': {'id': 'actual-conditional-encounter', 'isRealEncounter': True}, 'identificationFacts': {}, 'triggerEvents': {}}
        m = FateTransactions(sources, actors, world)
        m.learn('owner', 'fate-echo', level, 'owner/actual-level-addition/fate')
        if provider != 'Shaman': m.learn('owner', 'counterspell', 5 if provider in {'Wizard', 'Cleric'} else 8, 'owner/earlier-counter-addition')
        if owner_knows_child: m.learn('owner', 'fate-coin', 1, 'owner/earlier-coin-addition')
        m.learn('donor', original_sid, 1, 'donor/actual-source-addition')
        m.learn('counter', 'counterspell', 5, 'counter/actual-source-addition')
        for actor_id, actor in m.actors.items():
            if actor['provider'] == 'Wizard': m.prepare_wizard(actor_id, list(actor['learned']), actor_id + '/actual-study', {'actor': actor_id, 'completedAt': 0, 'sourceEvent': actor_id + '/conditional-completed-rest'})
        m.begin_turn('donor', 'donor/original-turn')
        if ready_original: m.begin_readied_coin_original('donor', 'original', 'bell')
        else: m.declare('donor', original_sid, 'original', {'target': 'originalRecipient', **({'hand': 'left'} if original_sid == 'fate-coin' else {})})
        m.world['identificationFacts']['direct-original'] = {'observer': 'owner', 'castId': 'original', 'kind': 'conditional-actual-direct-identification'}
        m.observe_cast('owner', 'original', 'direct-original')
        if ready_original: m.hold_readied_coin_original('original')
        elif original_sid == 'fate-coin': m.resolve_fate_coin('original')
        else: m.resolve_alignment('original', face=10, modifier=0)
        m.begin_turn('owner', 'owner/echo-turn')
        return m

    def begin(m, *, ready=False, target='target'):
        return m.begin_fate('owner', 'echo', 'original', None if ready else {'target': target, 'hand': 'left'}, ready_trigger='bell' if ready else None)

    def record(label, m):
        histories.append({'id': label, 'evidenceKind': 'Executed conditional composite, using specified hypothetical actor/world facts and real source-bound learning/preparation history.', 'final': m.snapshot()})

    def trigger(m, at, name='bell-event', actor='owner'):
        m.advance(at); m.world['triggerEvents'][name] = {'trigger': 'bell', 'at': at, 'perceivedBy': {actor: True}}
        return name

    # The actual original has its own payment, components, history and object.
    m = make(); donor_rp = m.actors['donor']['rp']; original_coin = deepcopy(m.coins['coin/original'])
    m.advance(3618); begin(m)
    check('outer-reserves-not-spends-child', m.actors['owner']['rp'] == 31 and m.reservations['echo']['rp'] == 2 and m.actors['owner']['dissonance'] == 0)
    c = m.finish_fate_outer('echo'); coin = m.resolve_fate_coin(c['id'])
    check('D7T09-first-matrix17plus2', m.actors['owner']['rp'] == 29 and m.actors['owner']['dissonance'] == 1 and m.actors['owner']['actions'] == 0)
    check('original-cost-and-object-not-replayed', m.actors['donor']['rp'] == donor_rp == 46 and m.coins['coin/original'] == original_coin)
    check('copied-result-own-lineage-deadline', coin['caster'] == 'owner' and coin['deadline'] == 7218 and coin['copyLineage'] == {'outer': 'echo', 'original': 'original'})
    check('no-permanent-repertoire-or-matrix-grant', 'fate-coin' not in m.actors['owner']['learned'] and 'fate-coin' not in m.actors['owner']['prepared'] and m.actors['owner']['wizardFamilies'] == ['fate-echo'])
    record('inclusive18-actual-cast-and-new-coin', m)
    for initial_d, expected_rp, expected_d in [(0, 29, 3), (9, 28, 12)]:
        m = make(); m.actors['owner'].update(dissonance=initial_d, wizardFamilies=['fate-echo']); begin(m); c = m.finish_fate_outer('echo'); m.resolve_fate_coin(c['id'])
        check('spent-outer-exemption-' + str(initial_d), m.actors['owner']['rp'] == expected_rp and m.actors['owner']['dissonance'] == expected_d)
        record('spent-matrix-initialD' + str(initial_d), m)
    m = make(owner_knows_child=True); begin(m); c = m.finish_fate_outer('echo'); m.resolve_fate_coin(c['id'])
    check('prepared-same-name-child-still-copy-route', c['route'] == 'fate-echo-copy' and c['dissonanceAdded'] == 1 and not c['classHooks'] and 'fate-coin' not in m.actors['owner']['wizardFamilies'])
    record('child-is-not-prepared-matrix-even-if-known', m)
    for provider in ['Cleric', 'Mirrorsage', 'Shaman']:
        m = make(provider); maximum = m.actors['owner']['maxRP']; begin(m); c = m.finish_fate_outer('echo'); m.resolve_fate_coin(c['id'])
        check(provider + ':own-pool-stats-and-no-class-waiver', m.actors['owner']['rp'] == maximum - 19 and m.actors['owner']['dissonance'] == 3 and c['provider'] == provider and c['scalingClassLevel'] == m.actors['owner']['classLevel'] and c['classHooks'] == [])
        record('copy-provider-' + provider, m)

    for label, mutate in [('too-old', lambda m: m.advance(3618.001)),
        ('no-observation', lambda m: m.observations.clear()), ('history-not-direct', lambda m: m.observations['owner/original'].update(kind='Supreme-history-query')),
        ('unresolved', lambda m: m.casts['original'].update(status='held-original')),
        ('copy-descendant', lambda m: m.casts['original'].update(copyLineage={'someParent': 'prior'})),
        ('null-rank', lambda m: m.casts['original'].update(rank=None)), ('wrong-source-version', lambda m: m.casts['original']['sourceBinding'].update(sha256='wrong')),
        ('future-original-record', lambda m: m.casts['original'].update(castingCompletedAt=3601))]:
        m = make(); mutate(m); reject(label, m, lambda: begin(m)); record('rejected-original-' + label, m)
    for label, d, rp in [('known-child-block', 15, 48), ('known-child-unaffordable', 9, 19)]:
        m = make(); m.actors['owner'].update(dissonance=d, rp=rp, wizardFamilies=['fate-echo'])
        reject(label, m, lambda: begin(m)); record(label, m)
    m = make(); m.actors['owner']['rp'] = 19; begin(m)
    m.declare('counter', 'counterspell', 'counter-outer', {'pendingCast': 'echo'})
    reject('child-reservation-not-spendable-by-counter', m, lambda: m.declare('owner', 'counterspell', 'bad', {'pendingCast': 'counter-outer'}))
    m.resolve_counter('counter-outer', 15)
    check('outer-counter-no-child-payment-or-history', m.actors['owner']['rp'] == 2 and m.actors['owner']['previousSpell'] == 'fate-echo' and not m.reservations and 'echo/child' not in m.casts)
    record('exclusive-reservation-and-outer-counter', m)
    m = make(); begin(m); c = m.finish_fate_outer('echo'); m.declare('counter', 'counterspell', 'counter-child', {'pendingCast': c['id']}); m.resolve_counter('counter-child', 10)
    check('child-counter-keeps-both-casts-paid', m.actors['owner']['rp'] == 29 and m.actors['owner']['dissonance'] == 1 and m.actors['owner']['previousSpell'] == 'fate-coin' and len(m.coins) == 1)
    record('child-counter-no-result-no-refund', m)

    for label, initial_d, rp, expected in [('repriced', 10, 48, 23), ('repriced-unaffordable', 10, 24, 2), ('now-Fractured', 16, 48, 22)]:
        m = make(); m.actors['owner'].update(dissonance=initial_d, rp=rp, wizardFamilies=['counterspell'])
        begin(m); forecast = m.composites['echo']['forecastChildQuote']['cost']
        m.declare('counter', 'counterspell', 'counter-outer', {'pendingCast': 'echo'})
        m.declare('owner', 'counterspell', 'counter-counter', {'pendingCast': 'counter-outer'}); m.resolve_counter('counter-counter', 12)
        c = m.finish_fate_outer('echo')
        if label == 'repriced':
            check('actual-intervening-cast-reprices-child', forecast == 2 and c['quote']['cost'] == 3); m.resolve_fate_coin(c['id'])
            check('parent-history-not-overwritten-after-child', m.actors['owner']['previousSpell'] == 'fate-coin' and m.actors['owner']['dissonance'] == 12)
        else:
            check(label + ':no-child-and-later-counter-history-kept', c is None and 'echo/child' not in m.casts and m.actors['owner']['previousSpell'] == 'counterspell' and not m.reservations)
        check(label + ':actual-costs-kept', m.actors['owner']['rp'] == expected)
        record(label + '-after-actual-counter-counter', m)
    for label, mutate in [('lost-child-components', lambda m: m.actors['owner']['body'].update(silenced=True)),
        ('moved-child-target', lambda m: m.world['entities']['target'].update(positionFeet=31)),
        ('occupied-child-hand', lambda m: m.world['entities']['target']['hands']['left'].update(holding='conditional-new-object'))]:
        m = make(); begin(m); mutate(m); c = m.finish_fate_outer('echo')
        check(label, c is None and m.actors['owner']['rp'] == 31 and m.actors['owner']['previousSpell'] == 'fate-echo' and not m.reservations)
        record(label + '-conditional-intervening-world-event', m)

    m = make(original_sid='alignment-suggestion'); m.actors['owner']['concentration'] = 'conditional-real-prior-effect'; begin(m)
    check('outer-does-not-end-prior-concentration', m.actors['owner']['concentration'] == 'conditional-real-prior-effect')
    c = m.finish_fate_outer('echo')
    check('child-commit-ends-prior-concentration', m.actors['owner']['concentration'] == c['id'] and m.actors['owner']['endConcentrationHistory'][-1]['reason'] == 'Fate-child-commit')
    m.declare('counter', 'counterspell', 'counter-child', {'pendingCast': c['id']}); m.resolve_counter('counter-child', 10)
    check('countered-child-never-restores-prior', m.actors['owner']['concentration'] is None and m.alignment.concentration.get('owner') is None)
    record('concentration-child-commit-and-counter', m)
    m = make(original_sid='alignment-suggestion'); begin(m); c = m.finish_fate_outer('echo'); m.resolve_alignment(c['id'], face=16, modifier=0)
    check('fresh-child-save-and-own-orientation', c['dc'] == 17 and m.alignment.effective('target') == {'order': 'Neutral', 'ethics': 'Neutral'})
    check('original-and-copy-distinct-effects', 'original' in m.alignment.effects and c['id'] in m.alignment.effects)
    record('paid-child-actual-alignment-result', m)

    m = make(); m.advance(3618); begin(m, ready=True); m.finish_fate_outer('echo'); before = deepcopy(m.actors['owner'])
    event = trigger(m, 3623)
    m.world['entities']['target']['positionFeet'] = 31
    r = m.release_fate_ready('owner', event, {'target': 'target', 'hand': 'left'})
    check('invalid-release-retains-hold-and-no-Reaction', not r['released'] and m.actors['owner']['reactions'] == 1 and m.actors['owner']['rp'] == 31 and 'owner' in m.holds)
    m.world['entities']['target']['positionFeet'] = 25
    r = m.release_fate_ready('owner', event, {'target': 'target', 'hand': 'left'}, declined=True)
    check('declined-release-no-spend', not r['released'] and m.actors['owner']['reactions'] == 1)
    r = m.release_fate_ready('owner', event, {'target': 'target', 'hand': 'left'}); m.resolve_fate_coin(r['child']['id'])
    check('Ready-keeps-preparation-age-no-outer-recast', r['released'] and m.composites['echo']['originalAgeAtSelection'] == 18 and m.actors['owner']['rp'] == 29 and m.actors['owner']['reactions'] == 0 and m.actors['owner']['actions'] == before['actions'] == 0)
    check('Ready-new-child-deadline-at-release', m.coins['coin/echo/child']['deadline'] == 7223 and len([x for x in m.casts.values() if x['spellId'] == 'fate-echo']) == 1)
    reject('Ready-only-one-copy', m, lambda: m.release_fate_ready('owner', event, {'target': 'target', 'hand': 'right'}))
    record('Ready-invalid-declined-then-valid-release-after18', m)
    for label in ['expiry', 'concentration-loss', 'incapacity']:
        m = make(); begin(m, ready=True); m.finish_fate_outer('echo')
        if label == 'expiry': m.begin_turn('owner', 'owner/next-regular-start')
        elif label == 'concentration-loss': m.actors['owner']['concentration'] = None; m.advance(3601)
        else: m.actors['owner']['body']['canAct'] = False; m.advance(3601)
        check(label + ':hold-costs-retained-reservation-only-released', m.actors['owner']['rp'] == 31 and not m.holds and not m.reservations and 'echo/child' not in m.casts)
        record('Ready-' + label, m)
    m = make(); begin(m, ready=True); m.finish_fate_outer('echo'); event = trigger(m, 3601)
    m.actors['owner']['body']['reactionLegal'] = False
    r = m.release_fate_ready('owner', event, {'target': 'target', 'hand': 'left'})
    check('Ready-no-Reaction-exception', not r['released'] and m.actors['owner']['reactions'] == 1 and 'owner' in m.holds)
    record('Ready-prohibited-Reaction', m)

    m = make(ready_original=True); reject('unreleased-original-not-eligible', m, lambda: begin(m))
    event = trigger(m, 3615, actor='donor'); m.release_readied_coin_original('donor', event, {'target': 'originalRecipient', 'hand': 'left'})
    check('original-Ready-casting-clock-not-release', m.casts['original']['castingCompletedAt'] == 3600 and m.casts['original']['resolvedAt'] == 3615)
    m.advance(3619); reject('readied-release-does-not-freshen-original', m, lambda: begin(m)); record('readied-original-age-rejection', m)
    m = make(); begin(m, target='owner'); c = m.finish_fate_outer('echo'); coin = m.resolve_fate_coin(c['id'])
    check('own-coin-has-actual-body-hand-custody', m.actors['owner']['body']['hands']['left']['holding'] == coin['id'])
    m.advance(7200)
    check('coin-expiry-clears-custody-no-refund', m.coins[coin['id']]['state'] == 'expired' and m.actors['owner']['body']['hands']['left']['holding'] is None and m.actors['owner']['rp'] == 29)
    record('copy-coin-physical-hand-and-expiry', m)
    check('all-game-source-bindings-unchanged', all(info(G / b['path']) == b for b in sources.bindings))
    report = {'recordedAtUtc': datetime.now(timezone.utc).isoformat(), 'status': 'pass', 'checks': len(checks), 'passedChecks': checks, 'failures': [],
        'sourceBindings': sources.bindings + [info(R / 'tools/di7_cast_transactions.py'), info(R / 'tools/di7_fate_transactions.py'), info(R / 'tools/di7_alignment_component.py'),
            info(R / 'tools/validate_di7_fate_transactions.py'), info(R / 'tools/core_playtest_rules.py'), info(R / 'tools/spell_playtest_rules.py'), info(R / 'docs/mechanics/COMBAT_ACTION_PLAYTEST.md')],
        'historyCount': len(histories), 'histories': histories,
        'scope': 'Actual conditional original learning/preparation/cast/outcome and direct identified observation, then Fate outer/child forecast, exclusive funding, separate payments/history/counter windows, child-owned source outcomes, concentration and actual Ready preparation/release/next-start expiry.',
        'completedChildModes': ['fate-coin', 'alignment-suggestion'],
        'limits': ['These are explicit hypothetical actors/worlds and legal repertoire subsets, not complete character builds or authenticated campaigns.',
            'Only two complete reviewed nondamaging Action modes are implemented. Other ranks/modes/materials/independent charges, broader universal modifiers and arbitrary copied payloads require their actual adapters; none are silently supplied.',
            'The alignment component executes resolution and concentration integration with its existing elapsed-time fixture clock. Full Suggestion initiative/virtual-phase timing remains open.',
            'Some intervening movement/component/custody changes are explicit conditional external world events; nested Counterspell changes to price/history are executed.',
            'No Shaman totem is supplied; ordinary outer totem-vent integration remains separate. No child receives ordinary-spell-only totem or prepared-matrix benefits.',
            'Full seven-spell49-variant acceptance and separate exact-card review remain; this report is finite behavior evidence only.'],
        'all49FiniteVariantsFulfilled': False, 'exactCardsApproved': False, 'runtimeImplemented': False, 'humanBalanceApproved': False, 'sourceInformationDeleted': 0, 'cosmologyReviewed': False, 'pushed': False}
    output.write_bytes(encoded(report)); print(json.dumps({'report': info(output), 'checks': len(checks), 'histories': len(histories)}))


if __name__ == '__main__': main()
