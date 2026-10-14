"""Institution-wide conditional paid feed histories and private-field boundaries."""
from copy import deepcopy
from datetime import datetime, timezone
import json
from apply_di7_ap_as_01 import G, R, A, info, encoded
from di7_cast_transactions import DI7Sources
from di7_faction_transactions import FactionTransactions


def main():
    output = A / 'DI7_FACTION_TRANSACTIONS_CHECK.json'; assert not output.exists()
    sources = DI7Sources(); checks = []; histories = []
    def check(label, value):
        assert value, label; checks.append(label)
    def reject(label, m, fn):
        before = m.snapshot()
        try: fn()
        except ValueError as error: check(label + '/rejected', bool(str(error)))
        else: raise AssertionError(label)
        check(label + '/atomic', before == m.snapshot())
    def record(label, m): histories.append({'id': label, 'final': m.snapshot()})
    def fact(fid, value, *, subject='guild-office', category='institutional', at=3000):
        return {'id': fid, 'subject': subject, 'category': category, 'actualTime': at, 'establishedAt': at,
            'authorityVersion': 'conditional-world-v1', 'authorityEvent': 'Director-established/' + fid, 'publicFields': {'value': value}}
    def activity(aid, *, basis='orders', kind='project', start=3000, end=9000, remote=False, personal=False):
        fields = {'objective': 'Objective of ' + aid, 'participantsAndRoles': ['Actual assigned role for ' + aid],
            'location': 'Remote branch two hundred miles away' if remote else 'Local office', 'stage': 'underway', 'immediateActivity': 'Actual work on ' + aid}
        facts = {aid + '/exists': fact(aid + '/exists', True, subject=aid, category='activity-existence', at=start)}
        for name, value in fields.items(): facts[aid + '/' + name] = fact(aid + '/' + name, value, subject='agent-' + aid if name == 'participantsAndRoles' else 'guild-office', at=start)
        participation = {} if personal else {'guild': {'basis': basis, 'actualCausalAuthority': 'conditional-actual-office-resource-order-link/' + aid,
            'readableKind': kind, 'existenceFact': aid + '/exists', 'fieldFacts': {name: aid + '/' + name for name in fields}}}
        row = {'id': aid, 'startsAt': start, 'endsAt': end, 'worldAuthorityVersion': 'conditional-world-v1', 'authorityEvent': 'actual-institutional-activity/' + aid,
            'institutionalParticipation': participation, 'reportedToLeadership': not remote, 'officiallyAuthorized': basis != 'resources', 'privateNonFactionDossier': 'DO-NOT-LEAK-UNRELATED-DOSSIER'}
        return row, facts
    def protect(subject, category='institutional', **overrides):
        result = {'id': 'private-scope/' + subject, 'nativeScopePremise': {'kind': 'conditional-actual-native-protection-scope', 'sourceVersion': 'conditional-native-v1',
            'sourceGrantEvent': 'conditional-actual-upstream-protection', 'completeScopeText': 'Conditional native source protects only the named subject/category/value from this rank7 Divination query in the supplied time interval; no player protection ability is created.'},
            'mode': 'block', 'activeFrom': 3000, 'activeUntil': 9000, 'subjects': [subject], 'querySchools': ['Divination'],
            'minimumQueryRank': 0, 'maximumQueryRank': 7, 'categories': [category], 'factTimeFrom': 0, 'factTimeUntil': 9000,
            'protectsExistence': True, 'fields': ['value'], 'maskedFields': {}}
        result.update(overrides); return result
    def make(provider='Wizard', *, start=True, count=0, protections=None):
        level = 13 if provider in {'Wizard', 'Cleric'} else 20; actors = {}
        for aid, cls, lv, position in [('owner', provider, level, 0), ('donor', 'Wizard', 13, 10)]:
            actors[aid] = {'provider': cls, 'classLevel': lv, 'totalLevel': lv, 'abilityScore': 18,
                'attainmentPremise': 'Conditional actual attained ordinary-casting slice; not a full character or campaign record.',
                'heroPath': 'Soothsayer' if cls == 'Shaman' else 'ordinary-provider-retained', 'specialization': 'Evocation', 'providerRetained': True,
                'bookPresent': True, 'studyUninterrupted': True, 'positionFeet': position, 'knownFactions': ['guild'],
                'body': {'conscious': True, 'canAct': True, 'ordinarySpellProhibited': False, 'silenced': False, 'canSpeak': True, 'reactionLegal': True,
                    'hands': {'left': {'usable': True, 'holding': None}, 'right': {'usable': True, 'holding': 'focus/' + aid}},
                    'focus': {'id': 'focus/' + aid, 'owner': aid, 'qualifiedClasses': [cls], 'accessible': True}}}
        entities = {aid: {'kind': 'creature', 'positionFeet': pos, 'willing': True, 'alliedTo': {a: True for a in actors}, 'relatedQuestions': []}
            for aid, pos in [('owner', 0), ('donor', 10), ('reference', 120)]}
        entities['reference'].update(membershipFacts={'guild': 'actual-member'}, badge=True, claimedMembership=True, partyStanding=3)
        world = {'entities': entities, 'relations': {a + '>' + t: {'sourceFact': 'conditional-open-local-reference', 'perceived': True, 'visible': True, 'lineOfEffect': True} for a in actors for t in entities},
            'alignmentActors': {a: {'underlying': {'order': 'Chaotic', 'ethics': 'Evil'} if a == 'reference' else {'order': 'Lawful', 'ethics': 'Good'},
                'immunities': [], 'permanentIdentity': {'id': a}, 'acquisitionSnapshots': [], 'usedAllowances': {}} for a in entities},
            'establishedFactions': ['guild'], 'encounter': {'id': 'conditional-genuine-encounter', 'isRealEncounter': True},
            'identificationFacts': {}, 'triggerEvents': {}, 'institutionalPermissions': {'owner': {'membership': False, 'standing': 0, 'authority': [], 'actions': 0}},
            'factionCheckpoint': {'lastActualDay': 0, 'jobsExecuted': 0}}
        facts = {'actual-member': fact('actual-member', {'factionId': 'guild', 'current': True}, subject='reference', category='membership')}; activities = {}
        for aid, options in [('patrol', {'kind': 'patrol'}), ('unreported-resources', {'basis': 'resources', 'kind': 'transaction', 'remote': True}),
            ('organizing', {'basis': 'coordinated-institutional-task', 'kind': 'project'}), ('joint-operation', {'kind': 'operation'}),
            ('personal-family', {'personal': True}), ('imagined-future', {'start': 8000})]:
            row, f = activity(aid, **options); activities[aid] = row; facts.update(f)
        activities['joint-operation']['institutionalParticipation']['rival'] = {'privateDossier': 'DO-NOT-LEAK-RIVAL-WHOLE-INSTITUTION'}
        for i in range(count):
            row, f = activity('large-project-' + str(i), kind='project', remote=True); activities[row['id']] = row; facts.update(f)
        data = {'kind': 'explicit-conditional-Director-established-world', 'facts': facts, 'protections': protections or [], 'questions': {}, 'canonicalQuestions': {}, 'steps': {}}
        institutions = {'guild': {'id': 'guild', 'exists': True, 'continuityAuthority': 'actual-existing-guild-identity'},
            'successor': {'id': 'successor', 'exists': True, 'continuityAuthority': 'different-new-institution'}}
        m = FactionTransactions(sources, actors, world, dossier=data, institutions=institutions, activities=activities)
        m.learn('owner', 'faction-omniscience', level, 'actual-owner-selected-faction')
        if provider == 'Wizard': m.learn('owner', 'alignment-suggestion', 1, 'actual-earlier-Suggestion')
        m.learn('donor', 'counterspell', 5, 'actual-donor-counter'); m.learn('donor', 'faction-omniscience', 13, 'actual-donor-selected-faction')
        for aid, actor in m.actors.items():
            if actor['provider'] == 'Wizard': m.prepare_wizard(aid, list(actor['learned']), aid + '/study', {'actor': aid, 'completedAt': 0, 'sourceEvent': 'conditional-completed-own-rest'})
        m.begin_turn('owner', 'owner/turn1')
        if start: m.declare('owner', 'faction-omniscience', 'feed', {'target': 'reference', 'faction': 'guild'}); m.resolve_faction('feed')
        return m
    def entries(m, actor='owner'): return [e for group in m.public_notices(actor)[-1]['register']['groups'].values() for e in group]
    def change(m, *, at, fid, value, eid):
        event = {'id': eid, 'at': at, 'phase': 0, 'applicationAt': 3000, 'applicationSequence': len(m.activity_events) + 1,
            'authorityEvent': 'actual-new-world-event/' + eid, 'kind': 'change-fact', 'factId': fid,
            'expectedVersion': m.information.data['facts'][fid]['authorityVersion'], 'newVersion': eid, 'newPublicFields': {'value': value}}
        m.activity_event(event); return event
    def begin(m, aid, at, end=9000):
        row, facts = activity(aid, start=at, end=end, remote=True)
        event = {'id': 'begin/' + aid, 'at': at, 'phase': 0, 'applicationAt': at, 'applicationSequence': len(m.activity_events) + 1,
            'authorityEvent': 'actual-new-world-event/' + aid, 'kind': 'begin-activity', 'activity': row, 'newFacts': facts}
        m.activity_event(event); return event

    for provider in ['Wizard', 'Cleric', 'Mirrorsage', 'Shaman']:
        m = make(provider); before = deepcopy(m.world['institutionalPermissions']); checkpoint = deepcopy(m.world['factionCheckpoint'])
        check(provider + '/own-paid-nonconcentration60', m.actors['owner']['rp'] == m.actors['owner']['maxRP'] - 17 and m.actors['owner']['concentration'] is None and m.feeds['feed']['deadline'] == 3660)
        check(provider + '/four-real-business-records', len(entries(m)) == 4 and any(e['location'].startswith('Remote branch') for e in entries(m)))
        public = json.dumps(m.public_notices('owner'))
        check(provider + '/no-personal-future-or-other-dossier', all(x not in public for x in ['personal-family', 'imagined-future', 'DO-NOT-LEAK']))
        check(provider + '/private-no-automatic-authority', not m.public_notices('donor') and m.world['institutionalPermissions'] == before and m.world['factionCheckpoint'] == checkpoint)
        record('paid-institutional-register-' + provider, m)
    m = make(count=125)
    check('large-hierarchy-retains-every-readable-record', len(entries(m)) == 129 and len(m.public_notices('owner')[-1]['register']['groups']['project']) == 126)
    record('129-actual-activities-no-arbitrary-cap', m)
    for label in ['false-member', 'undefined-member', 'protected-member']:
        m = make(start=False)
        if label == 'false-member': m.information.data['facts']['actual-member']['publicFields']['value']['current'] = False
        elif label == 'undefined-member': del m.information.data['facts']['actual-member']
        else: m.information.data['protections'].append(protect('reference', 'membership'))
        m.declare('owner', 'faction-omniscience', 'feed', {'target': 'reference', 'faction': 'guild'})
        check(label + '/hidden-test-after-17-paid', m.actors['owner']['rp'] == 31 and m.casts['feed']['status'] == 'pending')
        m.resolve_faction('feed')
        check(label + '/same-nondiagnostic-no-refund', not m.feeds and not m.public_notices('owner') and m.casts['feed']['publicResult'] == 'No usable institutional reading.' and m.actors['owner']['rp'] == 31)
        record(label, m)
    m = make(start=False); m.world['entities']['reference']['willing'] = False
    m.declare('owner', 'faction-omniscience', 'feed', {'target': 'reference', 'faction': 'guild'}); m.resolve_faction('feed')
    check('actual-membership-not-consent-standing-or-badge', bool(m.feeds)); record('unwilling-actual-member', m)
    for label, mutation in [('unperceived', lambda m: m.world['relations']['owner>reference'].update(perceived=False)),
        ('out-of-range', lambda m: m.world['entities']['reference'].update(positionFeet=120.001)),
        ('total-cover', lambda m: m.world['relations']['owner>reference'].update(lineOfEffect=False)),
        ('unknown-faction', lambda m: m.actors['owner'].update(knownFactions=[])),
        ('no-existing-faction', lambda m: m.world.update(establishedFactions=[]))]:
        m = make(start=False); mutation(m)
        reject(label, m, lambda: m.declare('owner', 'faction-omniscience', 'feed', {'target': 'reference', 'faction': 'guild'})); record(label, m)
    m = make(start=False); m.declare('owner', 'faction-omniscience', 'feed', {'target': 'reference', 'faction': 'guild'})
    m.declare('donor', 'counterspell', 'counter-feed', {'pendingCast': 'feed'}); m.resolve_counter('counter-feed', 20)
    check('actual-countered-cast-no-feed-no-refund', not m.feeds and not m.notices and m.actors['owner']['rp'] == 31)
    record('actual-counterspell', m)
    m = make(start=False); m.world['entities']['reference']['positionFeet'] = 30
    m.declare('owner', 'alignment-suggestion', 'Suggestion', {'target': 'reference'}); m.resolve_alignment('Suggestion', face=1, modifier=0)
    m.begin_turn('owner', 'owner/turn2'); m.declare('owner', 'faction-omniscience', 'feed', {'target': 'reference', 'faction': 'guild'}); m.resolve_faction('feed')
    check('nonconcentration-does-not-replace-actual-Suggestion', m.actors['owner']['concentration'] == 'Suggestion' and m.actors['owner']['rp'] == 29)
    record('independent-existing-paid-concentration', m)

    m = make(); event = change(m, at=3610, fid='unreported-resources/stage', value='unreported-transfer-completed', eid='actual-remote-change')
    check('remote-unreported-material-change-received', len(m.public_notices('owner')) == 2 and any(e['stage'] == 'unreported-transfer-completed' for e in entries(m)))
    reject('actual-world-event-not-replayed', m, lambda: m.activity_event(event))
    m.world['entities']['reference'].update(positionFeet=10000, dead=True, membershipFacts={})
    change(m, at=3611, fid='patrol/location', value='New patrol station', eid='after-reference-death')
    check('reference-death-movement-does-not-retarget', m.feeds['feed']['institution'] == 'guild' and any(e['location'] == 'New patrol station' for e in entries(m)))
    record('actual-updates-and-reference-death', m)
    for interruption in ['suppression', 'incapacity']:
        m = make(); m.advance(3610)
        m.receipt_state('feed', **({'suppressed': True} if interruption == 'suppression' else {'can_act': False}))
        begin(m, 'missed-brief-activity', 3620, end=3630)
        change(m, at=3625, fid='patrol/stage', value='MISS-THIS-INTERMEDIATE-STAGE', eid='missed-middle-stage')
        change(m, at=3640, fid='patrol/stage', value='Current resumed stage', eid='current-stage')
        check(interruption + '/no-usable-notices-during-gap', len(m.public_notices('owner')) == 1)
        m.receipt_state('feed', **({'suppressed': False} if interruption == 'suppression' else {'can_act': True}))
        public = json.dumps(m.public_notices('owner'))
        check(interruption + '/current-register-no-backfill', len(m.public_notices('owner')) == 2 and 'missed-brief-activity' not in public and 'MISS-THIS' not in public and 'Current resumed stage' in public)
        check(interruption + '/original-clock-no-refund', m.feeds['feed']['deadline'] == 3660 and m.actors['owner']['rp'] == 31)
        m.advance(3660); m.receipt_state('feed', suppressed=False, can_act=True)
        check(interruption + '/expiry-not-restart', m.feeds['feed']['status'] == 'ended' and len(m.public_notices('owner')) == 2)
        record('pause-and-current-only-resume-' + interruption, m)
    m = make(); count = len(m.public_notices('owner')); begin(m, 'exact-deadline-new-task', 3660)
    check('half-open-expiry-before-new-notice', m.feeds['feed']['endedAt'] == 3660 and len(m.public_notices('owner')) == count)
    record('exact-deadline-no-notice', m)
    m = make(); begin(m, 'scheduled-brief-activity', 3610, end=3620); m.advance(3640)
    check('real-scheduled-ending-retains-actual-timestamp', [x['at'] for x in m.public_notices('owner')] == [3600, 3610, 3620] and not any('scheduled-brief' in e['objective'] for e in entries(m)))
    record('actual-source-end-boundary', m)
    for ending in ['caster-death', 'dispel', 'institution-ceased']:
        m = make(); m.advance(3610)
        if ending == 'caster-death': m.world['entities']['owner']['dead'] = True; m.advance(3610)
        elif ending == 'dispel': m.end_feed('feed', 'conditional-actual-legal-dispel')
        else: m.institutions['guild']['exists'] = False; m.advance(3610)
        change(m, at=3620, fid='patrol/stage', value='NOT-RECEIVED-AFTER-END', eid='after-end')
        check(ending + '/ends-no-refresh-no-successor', m.feeds['feed']['status'] == 'ended' and len(m.public_notices('owner')) == 1 and m.feeds['feed']['institution'] == 'guild')
        check(ending + '/prior-memory-kept', len(entries(m)) == 4 and 'NOT-RECEIVED' not in json.dumps(m.public_notices('owner')))
        record('feed-ending-' + ending, m)

    m = make(protections=[protect('agent-unreported-resources', protectsExistence=False)])
    remote = next(e for e in entries(m) if e['location'].startswith('Remote branch'))
    check('personal-field-not-revealed-by-institutional-relabeling', remote['participantsAndRoles'] == 'Indeterminate' and remote['objective'] == 'Objective of unreported-resources')
    check('independent-institutional-fields-remain-useful', remote['stage'] == 'underway' and len(entries(m)) == 4)
    record('personal-field-protection', m)
    m = make(protections=[protect('unreported-resources', 'activity-existence')])
    check('protected-existence-no-entry-placeholder-or-key-gap', len(entries(m)) == 3 and sorted(e['reference'] for e in entries(m)) == ['activity-1', 'activity-2', 'activity-3'])
    before = deepcopy(m.public_notices('owner')); change(m, at=3610, fid='unreported-resources/stage', value='SECRET-HIDDEN-CHANGE', eid='hidden-only-change')
    check('protected-only-change-no-diagnostic-notice', m.public_notices('owner') == before and 'SECRET' not in json.dumps(m.public_notices('owner')))
    record('existence-and-update-side-channel', m)
    m = make(start=False); del m.information.data['facts']['patrol/participantsAndRoles']
    m.declare('owner', 'faction-omniscience', 'feed', {'target': 'reference', 'faction': 'guild'}); m.resolve_faction('feed')
    check('undefined-participants-not-invented-or-zero', next(e for e in entries(m) if e['kind'] == 'patrol')['participantsAndRoles'] == 'Indeterminate')
    record('undefined-field', m)
    m = make(); m.begin_turn('donor', 'donor/turn1'); m.declare('donor', 'faction-omniscience', 'second-feed', {'target': 'reference', 'faction': 'guild'}); m.resolve_faction('second-feed')
    check('equivalent-overlapping-paid-feeds-consistent', m.public_notices('owner')[0]['register'] == m.public_notices('donor')[0]['register'] and m.actors['donor']['rp'] == 31)
    change(m, at=3610, fid='patrol/stage', value='Same real new stage', eid='same-world-change')
    check('overlapping-feeds-use-same-world-update', m.public_notices('owner')[-1]['register'] == m.public_notices('donor')[-1]['register'])
    record('two-casters-same-world-paid-feeds', m)
    bindings = sources.bindings + [info(p) for p in [R / 'tools/di7_faction_transactions.py', R / 'tools/validate_di7_faction_transactions.py',
        R / 'tools/di7_vision_transactions.py', R / 'tools/di7_fate_transactions.py', R / 'tools/di7_cast_transactions.py',
        R / 'docs/mechanics/COMBAT_ACTION_PLAYTEST.md', R / 'data/playtest/spell_candidates/divination_rank7_exact_01_expectations.json']]
    report = {'status': 'pass', 'recordedAtUtc': datetime.now(timezone.utc).isoformat(), 'checks': len(checks), 'historyCount': len(histories),
        'sourceBindings': bindings, 'checkLabels': checks, 'histories': histories, 'failures': [],
        'scope': 'Paid four-provider Faction Omniscience, hidden post-payment actual membership, uncapped structured remote current activity, ordinary existing concentration retained, actual versioned ordered world updates, half-open60-second lifecycle and private receipt gating.',
        'conditionalPremises': ['Actual attained ordinary-provider casting/body/rest slices and local visible/perceived reference geometry.',
            'Director-established actual institution/membership/continuity, activity/fact versions and causal office/resource/order participation; source-semantic truth is a supplied hypothetical world premise.',
            'Native protection source grants and exact subject/field/school/rank/time scopes remain explicit upstream conditional interfaces, not authored selectable protection powers.',
            'Incapacity, suppression, dispel and death are actual upstream world events here; their originating attacks/abilities are not executed.'],
        'remaining': ['Original source says perceived reference and elsewhere visible creature; these histories use both, without resolving the perceived-but-unseen edge case.',
            'Native protection acquisition/casting and overlapping protection arbitration; communication uses its actual separate source and is not automatically granted by these notices.',
            'Mass/Supreme geometry question is pending GPT; their payloads, Suggestion initiative clock and actual Shaman ordinary totem remain unfinished.'],
        'candidateApproved': False, 'full49Fulfilled': False, 'humanPlaytest': False, 'spellPromotions': 0, 'newRuleAdoptions': 0}
    output.write_bytes(encoded(report)); print(json.dumps({'report': info(output), 'checks': len(checks), 'histories': len(histories), 'status': 'pass'}))


if __name__ == '__main__': main()
