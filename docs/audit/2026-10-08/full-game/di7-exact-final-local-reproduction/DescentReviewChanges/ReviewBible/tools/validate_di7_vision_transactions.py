"""Vision actual conditional casting/lifecycle; explicit semantic/protection premises."""
from copy import deepcopy
from datetime import datetime, timezone
import json
from apply_di7_ap_as_01 import G, R, A, info, encoded
from di7_cast_transactions import DI7Sources
from di7_vision_transactions import VisionTransactions


def main():
    output = A / 'DI7_VISION_TRANSACTIONS_CHECK.json'; assert not output.exists()
    sources = DI7Sources(); checks = []; histories = []
    q = 'Where is the archive key?'; alias = 'How can I obtain the archive key?'; future = 'How can our expedition leave this month?'
    def check(label, value):
        assert value, label; checks.append(label)
    def reject(label, m, fn):
        before = m.snapshot()
        try: fn()
        except ValueError as error: check(label + '/rejected', bool(str(error)))
        else: raise AssertionError(label)
        check(label + '/atomic', m.snapshot() == before)
    def record(label, m): histories.append({'id': label, 'final': m.snapshot()})
    def dossier():
        facts = {}
        for fid, category, text in [
            ('keeper', 'custody', 'The archive keeper holds the key and accepts appointment requests.'),
            ('appointment', 'practical-step', 'Request an appointment with the keeper.'),
            ('crew', 'capacity', 'An available crew can prepare this expedition if the group secures supplies.'),
            ('uncertainty', 'causal-uncertainty', 'Weather remains uncertain; choosing another departure day can change the route.'),
            ('supply', 'practical-step', 'Ask the established outfitter for a supply quotation.'),
            ('weather', 'practical-step', 'Check the local forecast before choosing a departure day.'),
            ('route', 'practical-step', 'Compare the two established road routes.'),
            ('fourth', 'practical-step', 'Ask an available guide about the road.'),
            ('too-late', 'practical-step', 'Wait for the distant winter convoy.')]:
            facts[fid] = {'id': fid, 'subject': 'archive' if fid in {'keeper', 'appointment'} else 'expedition',
                'category': category, 'authorityVersion': 'conditional-world-v1', 'authorityEvent': 'Director-established/' + fid,
                'establishedAt': 3000, 'actualTime': 3000, 'publicFields': {'text': text}}
        steps = {sid: {'instructionFact': sid, 'requiredReadableFacts': ['keeper' if sid == 'appointment' else 'crew'],
            'actualFeasibilityEvent': 'conditional-established-capacity-and-available-request/' + sid, 'feasible': True,
            'earliestActionAt': 3660 + (31 * 86400 if sid == 'too-late' else 0)}
            for sid in ['appointment', 'supply', 'weather', 'route', 'fourth', 'too-late']}
        return {'kind': 'explicit-conditional-Director-established-world', 'facts': facts, 'protections': [], 'steps': steps,
            'questions': {q: {'canonicalQuestion': 'archive-key'}, alias: {'canonicalQuestion': 'archive-key'}, future: {'canonicalQuestion': 'expedition-month'}},
            'canonicalQuestions': {'archive-key': {'centralFact': 'keeper', 'future': False, 'orderedPracticalSteps': ['appointment']},
                'expedition-month': {'centralFact': 'crew', 'future': True, 'uncertaintyFact': 'uncertainty', 'orderedPracticalSteps': ['too-late', 'supply', 'weather', 'route', 'fourth']}}}
    def make(*, provider='Wizard', start=True, question=q, anchor='target', data=None):
        level = 13 if provider in {'Wizard', 'Cleric'} else 20; actors = {}
        for aid, cls, lv, pos in [('owner', provider, level, 0), ('donor', 'Wizard', 13, 10)]:
            actors[aid] = {'provider': cls, 'classLevel': lv, 'totalLevel': lv, 'abilityScore': 18,
                'attainmentPremise': 'Explicit hypothetical ordinary-provider attained-level slice, not full character/campaign history.',
                'heroPath': 'Soothsayer' if cls == 'Shaman' else 'ordinary-provider-retained', 'specialization': 'Evocation',
                'providerRetained': True, 'bookPresent': True, 'studyUninterrupted': True, 'positionFeet': pos, 'knownFactions': [],
                'body': {'conscious': True, 'canAct': True, 'ordinarySpellProhibited': False, 'silenced': False, 'canSpeak': True, 'reactionLegal': True,
                    'hands': {'left': {'usable': True, 'holding': None}, 'right': {'usable': True, 'holding': 'focus/' + aid}},
                    'focus': {'id': 'focus/' + aid, 'owner': aid, 'qualifiedClasses': [cls], 'accessible': True}}}
        entities = {aid: {'kind': 'creature', 'positionFeet': pos, 'willing': True, 'alliedTo': {a: True for a in actors},
            'relatedQuestions': [q, alias, future], 'hands': deepcopy(actors[aid]['body']['hands'])} for aid, pos in [('owner', 0), ('donor', 10)]}
        entities['target'] = {'kind': 'object', 'positionFeet': 120, 'relatedQuestions': [q, alias, future]}
        world = {'entities': entities, 'relations': {a + '>' + t: {'sourceFact': 'conditional-actual-open-line', 'perceived': True, 'visible': True, 'lineOfEffect': True} for a in actors for t in entities},
            'alignmentActors': {a: {'underlying': {'order': 'Lawful', 'ethics': 'Good'}, 'immunities': [], 'permanentIdentity': {'id': a}, 'acquisitionSnapshots': [], 'usedAllowances': {}} for a in actors},
            'establishedFactions': [], 'encounter': {'id': 'conditional-genuine-encounter', 'isRealEncounter': True}, 'identificationFacts': {}, 'triggerEvents': {},
            'activityCredits': {'rest': 0, 'research': 0, 'training': 0, 'journey': 0}, 'communicationEvents': {}}
        m = VisionTransactions(sources, actors, world, dossier=dossier() if data is None else data)
        m.learn('owner', 'vision-quest', level, 'actual-selected-vision')
        m.learn('owner', 'fate-coin', 1, 'actual-earlier-coin')
        if provider != 'Shaman': m.learn('owner', 'counterspell', 5 if provider in {'Wizard', 'Cleric'} else 8, 'actual-earlier-counter')
        m.learn('donor', 'fate-coin', 1, 'donor-actual-coin'); m.learn('donor', 'counterspell', 5, 'donor-actual-counter')
        for aid, actor in m.actors.items():
            if actor['provider'] == 'Wizard': m.prepare_wizard(aid, list(actor['learned']), aid + '/study', {'actor': aid, 'completedAt': 0, 'sourceEvent': 'conditional-completed-own-rest'})
        m.begin_turn('owner', 'owner/turn1')
        if start:
            m.declare('owner', 'vision-quest', 'vision', {'target': anchor, 'question': question}); m.resolve_vision('vision')
        return m
    def event(m, kind, *, at=3640, application=3601, sequence=2, phase=0, source=None, **payload):
        m.event(at=at, phase=phase, applied_at=application, application_sequence=sequence,
            source_id=source or 'conditional-actual-' + kind, kind=kind, actor='owner', **payload)
    def answer(m): return m.public_memory('owner')[0]['answer']
    def protection(**overrides):
        p = {'id': 'private-protection-record', 'nativeScopePremise': {'kind': 'conditional-actual-native-protection-scope',
            'sourceVersion': 'explicit-conditional-scope-v1', 'sourceGrantEvent': 'conditional-actual-upstream-source-application',
            'completeScopeText': 'For this conditional interface scenario, an actually granted native source blocks the specified archive custody text from Divination rank0..7 during the given query and fact-time intervals. This fixture creates no selectable game ability.'},
            'mode': 'block', 'activeFrom': 3000, 'activeUntil': 4000, 'subjects': ['archive'], 'querySchools': ['Divination'],
            'minimumQueryRank': 0, 'maximumQueryRank': 7, 'categories': ['custody'], 'factTimeFrom': 0, 'factTimeUntil': 4000,
            'protectsExistence': True, 'fields': ['text'], 'maskedFields': {}}
        p.update(overrides); return p

    for provider in ['Wizard', 'Cleric', 'Mirrorsage', 'Shaman']:
        m = make(provider=provider); before_work = deepcopy(m.world['activityCredits'])
        check(provider + '/actual-paid-and-concentrating', m.actors['owner']['rp'] == m.actors['owner']['maxRP'] - 17 and m.actors['owner']['concentration'] == 'vision' and not m.memories)
        m.advance(3659.999); check(provider + '/no-early-answer', not m.memories)
        m.advance(3660); check(provider + '/normal-deadline-answer-once', m.trances['vision']['status'] == 'completed' and m.actors['owner']['concentration'] is None and len(m.public_memory('owner')) == 1)
        check(provider + '/actual-central-fact-and-real-step', answer(m)['text'].startswith('The archive keeper holds the key') and answer(m)['steps'] == ['Request an appointment with the keeper.'])
        m.advance(3700); check(provider + '/no-replay-work-or-refund', len(m.public_memory('owner')) == 1 and m.world['activityCredits'] == before_work and m.actors['owner']['rp'] == m.actors['owner']['maxRP'] - 17)
        record('paid-complete-' + provider, m)
    m = make(anchor='owner'); m.advance(3660)
    check('self-anchor-allowed', m.trances['vision']['anchor'] == 'owner' and bool(answer(m))); record('actual-related-self-anchor', m)
    for label, mutate in [('unrelated', lambda m: m.world['entities']['target'].update(relatedQuestions=[])),
        ('outside120', lambda m: m.world['entities']['target'].update(positionFeet=120.001)),
        ('blocked-line', lambda m: m.world['relations']['owner>target'].update(lineOfEffect=False)),
        ('commit-Silence', lambda m: m.actors['owner']['body'].update(silenced=True))]:
        m = make(start=False); mutate(m)
        reject(label, m, lambda: m.declare('owner', 'vision-quest', 'vision', {'target': 'target', 'question': q})); record(label, m)
    m = make(start=False); m.declare('owner', 'vision-quest', 'vision', {'target': 'target', 'question': q})
    m.declare('donor', 'counterspell', 'counter-vision', {'pendingCast': 'vision'}); m.resolve_counter('counter-vision', 20); m.advance(3660)
    check('actual-counter-no-trance-no-refund', not m.trances and not m.memories and m.actors['owner']['rp'] == 31 and m.casts['vision']['status'] == 'countered')
    record('actual-countered-Vision', m)

    for kind in ['forced-movement', 'incapacitated', 'suppression', 'lose-concentration']:
        m = make(); event(m, kind, **({'position': 5} if kind == 'forced-movement' else {})); m.advance(3660)
        check(kind + '/ends-without-answer-refund', m.trances['vision']['status'] == 'interrupted' and not m.memories and m.actors['owner']['rp'] == 31)
        check(kind + '/no-parallel-work', not any(m.world['activityCredits'].values()))
        record('trance-interruption-' + kind, m)
    m = make(); event(m, 'silence'); m.advance(3660)
    check('later-Silence-not-continuous-component', m.actors['owner']['body']['silenced'] and m.trances['vision']['status'] == 'completed'); record('later-Silence', m)
    for damage, natural, modifier, completes in [(4, 8, 2, True), (24, 10, 2, True), (24, 9, 2, False), (1, 1, 20, True), (48, 20, 2, False)]:
        m = make(); event(m, 'damage', resolvedDamage=damage, natural=natural, constitutionSaveModifier=modifier); m.advance(3660)
        check('damage-save-' + str((damage, natural, modifier)), bool(m.memories) == completes and len(m.trances['vision']['concentrationChecks']) == 1)
        check('damage-life-retained-' + str(damage) + '-' + str(natural), m.life['owner'].temp_hp == max(0, 5 - damage) and m.life['owner'].hp == 100 - max(0, damage - 5))
        record('damage-concentration-' + str((damage, natural, modifier)), m)
    for application, expected in [(3500, 'interrupted'), (3601, 'completed')]:
        m = make(); event(m, 'forced-movement', at=3660, application=application, position=5)
        m.advance(3660)
        check('same-time-order-' + str(application), m.trances['vision']['status'] == expected and bool(m.memories) == (expected == 'completed'))
        reject('ordered-event-not-replayed-' + str(application), m, lambda: event(m, 'forced-movement', at=3660, application=application, position=10))
        record('same-time-application-order-' + str(application), m)
    m = make(); m.advance(3660)
    reject('backdated-interruption-cannot-erase-answer', m, lambda: event(m, 'forced-movement', at=3660, application=3500, position=5))
    record('completed-answer-stays', m)
    m = make(); m.begin_turn('donor', 'donor/turn1'); m.declare('donor', 'fate-coin', 'donor-coin', {'target': 'donor', 'hand': 'left'})
    reject('cannot-keep-trance-and-react', m, lambda: m.declare('owner', 'counterspell', 'no-counter', {'pendingCast': 'donor-coin'}))
    m.end_trance('vision', 'voluntary-end-before-Reaction'); m.declare('owner', 'counterspell', 'real-counter', {'pendingCast': 'donor-coin'}); m.resolve_counter('real-counter', 20)
    m.advance(3660)
    check('voluntary-end-then-actual-paid-Reaction', not m.memories and m.actors['owner']['reactions'] == 0 and m.actors['owner']['rp'] == 26 and m.casts['donor-coin']['status'] == 'countered')
    record('voluntary-end-before-real-Counterspell', m)

    m = make(question=future); m.advance(3660); out = answer(m)
    check('future-three-feasible-steps-within30days', len(out['steps']) == 3 and 'winter' not in out['text'] and 'guide' not in out['text'] and out['guidanceHorizonEndsAt'] == 3660 + 30 * 86400)
    check('future-uncertainty-150words-no-success-grant', 'uncertain' in out['text'] and len(out['text'].split()) <= 150 and not any(m.world['activityCredits'].values()))
    record('future-finite-guidance', m)
    data = dossier(); data['facts']['crew']['forecastForTime'] = 3660 + 31 * 86400
    m = make(question=future, data=data); m.advance(3660)
    check('no-central-forecast-beyond30days', answer(m)['text'] == 'The inquiry supplies no actionable answer.'); record('outside-future-horizon', m)
    data = dossier(); data['facts']['fourth']['publicFields']['text'] = ' '.join(['supported'] * 151)
    data['canonicalQuestions']['expedition-month']['orderedPracticalSteps'] = ['fourth', 'supply']
    m = make(question=future, data=data); m.advance(3660)
    check('word-ceiling-no-truncated-fact', len(answer(m)['text'].split()) <= 150 and answer(m)['steps'] == ['Ask the established outfitter for a supply quotation.'])
    record('word-bound-selects-complete-supported-step', m)

    public_answers = []
    for label in ['unknown', 'protected-existence', 'protected-text']:
        data = dossier()
        if label == 'unknown': del data['facts']['keeper']
        else:
            data['protections'] = [protection(protectsExistence=label == 'protected-existence')]
            data['facts']['keeper']['publicFields']['text'] = 'SECRET-KEEPER-IDENTITY-DO-NOT-LEAK'
        m = make(data=data); m.advance(3660); public_answers.append(answer(m))
        check(label + '/no-reason-id-count-or-private-text', 'SECRET' not in json.dumps(m.public_memory('owner')) and answer(m)['steps'] == [])
        record('information-' + label, m)
    check('unknown-and-protected-indistinguishable-public-result', all(x == public_answers[0] for x in public_answers))
    for label, override in [('other-school', {'querySchools': ['Enchantment']}), ('rank0to6-only', {'maximumQueryRank': 6}),
        ('other-subject', {'subjects': ['different-subject']}), ('other-field', {'protectsExistence': False, 'fields': ['unrequested-field']}),
        ('expired', {'activeUntil': 3660}), ('other-fact-time', {'factTimeUntil': 2999})]:
        data = dossier(); data['protections'] = [protection(**override)]
        m = make(data=data); m.advance(3660)
        check('native-scope-' + label, answer(m)['text'].startswith('The archive keeper holds the key'))
        record('protection-scope-' + label, m)
    data = dossier(); p = protection(mode='mask', protectsExistence=False, maskedFields={'text': 'The stated custody result is inconsistent.'})
    p['nativeScopePremise']['explicitlyAuthorizesAlteredResult'] = True; data['protections'] = [p]
    m = make(data=data); m.advance(3660)
    check('native-authorized-mask-not-forced-truth', answer(m)['text'].startswith('The stated custody result is inconsistent.')); record('conditional-native-mask', m)
    data = dossier(); data['facts']['keeper']['publicFields']['text'] = 'The established key shelf is empty.'; data['canonicalQuestions']['archive-key']['orderedPracticalSteps'] = []
    m = make(data=data); m.advance(3660)
    check('established-readable-absence-can-be-reported', answer(m)['text'] == 'The established key shelf is empty.'); record('actual-established-absence', m)

    first = make(); first.advance(3660); second = make(question=alias, provider='Cleric'); second.advance(3660)
    check('paid-equivalent-question-different-caster-consistency', answer(first) == answer(second) and first.actors['owner']['rp'] == 31 and second.actors['owner']['rp'] == 19)
    changed = dossier(); changed['facts']['keeper'].update(authorityVersion='conditional-world-v2', authorityEvent='actual-new-custody-event', establishedAt=3650)
    changed['facts']['keeper']['publicFields']['text'] = 'The keeper has returned the key to the archive desk.'
    third = make(data=changed); third.advance(3660)
    check('genuine-new-world-event-changes-answer', answer(third) != answer(first)); record('equivalent-paid-query', second); record('new-world-event', third)
    check('private-answer-not-auto-shared', not first.public_memory('donor'))
    reject('no-free-communication-channel', first, lambda: first.communicate('owner', 'donor', 'vision', 'nonexistent'))
    first.world['communicationEvents']['spoken'] = {'speaker': 'owner', 'listener': 'donor', 'at': 3660, 'actuallyReceivedUnderstood': True,
        'sourceFact': 'conditional-actual-audible-understood-spoken-message-after-trance'}
    first.communicate('owner', 'donor', 'vision', 'spoken')
    check('actual-channel-shares-only-delivered-answer', first.public_memory('donor')[0]['answer'] == answer(first) and 'privateInformationDossier' not in json.dumps(first.public_memory('donor')))
    reject('communication-event-not-replayed', first, lambda: first.communicate('owner', 'donor', 'vision', 'spoken')); record('private-knowledge-and-real-channel', first)

    extra = [R / 'tools' / name for name in ['di7_vision_transactions.py', 'validate_di7_vision_transactions.py', 'di7_cast_transactions.py',
        'di7_fate_transactions.py', 'core_playtest_rules.py', 'healing_playtest_rules.py']]
    extra += [R / 'docs/mechanics/COMBAT_ACTION_PLAYTEST.md', R / 'docs/mechanics/BARD_PLAYTEST_v0_1.md',
        R / 'data/playtest/spell_candidates/divination_rank7_exact_01_expectations.json', A / 'di7-joint-review-01-verdict/DI7_FIELD_CONTRACTS.json']
    report = {'status': 'pass', 'recordedAtUtc': datetime.now(timezone.utc).isoformat(), 'checks': len(checks), 'historyCount': len(histories),
        'sourceBindings': sources.bindings + [info(p) for p in extra], 'checkLabels': checks, 'histories': histories, 'failures': [],
        'scope': 'Four actual conditional paid provider routes, fixed question/related anchor, source concentration,60-second ordered normal completion/interruption, actual paid Counterspell choice, life damage/binary concentration save, private bounded supported answer and actual communication event.',
        'conditionalPremises': ['Attained provider and initial completed-rest/body/world/HP slices.',
            'Incoming forced movement/conditions/suppression and post-defense damage source eligibility and canonical application order are provided upstream.',
            'Director-established actual facts, semantic equivalence of supplied questions, source-supported concise projections and genuine practical-step feasibility are explicit conditional world premises.',
            'Generic native protection scope/grant and altered-result entitlement are explicit upstream conditional interfaces, not authenticated named player abilities or a newly authored protection source. The evaluator applies their precise subject/field/school/rank/query-time/fact-time scope.'],
        'remaining': ['Complete native protection acquisition/casting and multi-protection arbitration; natural-language fact/causality adjudication is not automated.',
            'Mass Revelation, Faction Omniscience, Supreme Sight and their exact payload interfaces remain unfinished.',
            'Suggestion initiative clock, ordinary Shaman totem vent and full49+4 compilation/exact review remain open.'],
        'candidateApproved': False, 'full49Fulfilled': False, 'humanPlaytest': False, 'spellPromotions': 0, 'newRuleAdoptions': 0}
    output.write_bytes(encoded(report)); print(json.dumps({'report': info(output), 'checks': len(checks), 'histories': len(histories), 'status': 'pass'}))


if __name__ == '__main__': main()
