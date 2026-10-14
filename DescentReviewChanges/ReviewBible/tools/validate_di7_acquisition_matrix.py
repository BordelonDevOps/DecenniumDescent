"""All-seven ACQ19 checks; rank upper-bound proof is distinguished from histories."""
from copy import deepcopy
from datetime import datetime, timezone
import json
from apply_di7_ap_as_01 import G, R, A, info, encoded
from di7_cast_transactions import DI7Sources
from di7_acquisition_transactions import AcquisitionTransactions, same_or_lower


def main():
    output = A / 'DI7_ALL_SEVEN_ACQUISITION_CHECK.json'; assert not output.exists()
    sources = DI7Sources(); checks = []; histories = []; rank_proofs = []
    def check(label, value):
        assert value, label; checks.append(label)
    def reject(label, m, fn, message=None):
        before = m.snapshot()
        try: fn()
        except ValueError as error: check(label + '/rejected', bool(str(error)) and (message is None or message in str(error)))
        else: raise AssertionError(label)
        check(label + '/no-resource-history-or-repertoire-mutation', m.snapshot() == before)
    def fixture(provider, level):
        actor = {'provider': provider, 'classLevel': level, 'totalLevel': 20, 'abilityScore': 18,
            'attainmentPremise': 'Conditional attained class/total level ordinary-provider slice, no authenticated campaign advancement.',
            'heroPath': 'Soothsayer' if provider == 'Shaman' else 'ordinary-provider-retained', 'specialization': 'Evocation',
            'providerRetained': True, 'bookPresent': True, 'studyUninterrupted': True, 'positionFeet': 0, 'knownFactions': [],
            'body': {'conscious': True, 'canAct': True, 'ordinarySpellProhibited': False, 'silenced': False,
                'canSpeak': True, 'reactionLegal': True, 'hands': {'left': {'usable': True, 'holding': None},
                    'right': {'usable': True, 'holding': 'focus'}},
                'focus': {'id': 'focus', 'owner': 'owner', 'qualifiedClasses': [provider], 'accessible': True}}}
        m = AcquisitionTransactions(sources, {'owner': actor}, {'entities': {}, 'relations': {}, 'establishedFactions': [],
            'encounter': {'id': 'conditional-genuine-encounter', 'isRealEncounter': True}})
        m.begin_turn('owner', 'turn1'); return m
    def rest(rid='rest1'): return {'kind': 'conditional-actually-completed-own-long-rest', 'actor': 'owner', 'id': rid, 'completedAt': 3600}
    def record(label, m): histories.append({'id': label, 'final': m.snapshot()})

    ids = list(sources.cards)
    for sid in ids:
        expected = {provider: {'rank': 7, 'minimumClassLevel': lv, 'school': 'Divination', 'baseRpCost': 17}
            for provider, lv in [('Cleric', 13), ('Wizard', 13), ('Mirrorsage', 19), ('Shaman', 19)]}
        check(sid + '/original-and-candidate-placements', sources.ordinary[sid]['classAccess'] == expected == sources.cards[sid]['operationalCandidate']['classAccess'])
        for provider, level in [('Cleric', 12), ('Wizard', 12), ('Mirrorsage', 18), ('Shaman', 18)]:
            m = fixture(provider, level)
            reject(sid + '/' + provider + '/below-class-gate-with-total20', m, lambda: m.learn('owner', sid, level, 'no-grant'), 'not legal')
            record('below-class-gate/' + provider + '/' + sid, m)
        for provider in ['Mirrorsage', 'Shaman']:
            m = fixture(provider, 19)
            reject(sid + '/' + provider + '/no19-learning-addition', m, lambda: m.learn('owner', sid, 19, 'invalid19'), 'No unspent')
            reject(sid + '/' + provider + '/unlearned-cast-no-commit', m, lambda: m.declare('owner', sid, 'no-cast', {}), 'matching actual learning history')
            m.learn('owner', 'fate-coin', 1, 'actual-earlier-selected-spell')
            for rid in ['rest1', 'rest2']:
                reject(sid + '/' + provider + '/' + rid + '/no-upgrade-known-rank1', m, lambda rid=rid: m.replace_known('owner', 'fate-coin', sid, rest(rid)), 'cannot increase rank')
            record('19-repertoire-and-actual-lower-known-replacement/' + provider + '/' + sid, m)
            maximum_prior = max(sources.classes[provider]['maxSpellRankByClassLevel'][:18])
            check(sid + '/' + provider + '/rank6-upper-bound', maximum_prior == 6)
            proof = {'spellId': sid, 'provider': provider, 'evidenceKind': 'Universal rank-predicate proof, not a fabricated known rank6 spell or executed long-rest history.',
                'maximumOrdinaryRankBefore19': maximum_prior, 'requestedRank': 7,
                'allPossibleLowerRankInputs': [{'oldRank': rank, 'allowed': same_or_lower(rank, 7)} for rank in range(maximum_prior + 1)]}
            check(sid + '/' + provider + '/no0-through6-replacement-to7', not any(x['allowed'] for x in proof['allPossibleLowerRankInputs']))
            rank_proofs.append(proof)
            m = fixture(provider, 20); m.learn('owner', sid, 20, 'actual-selected20/' + sid)
            card, _, binding, candidate = m.route('owner', sid)
            check(sid + '/' + provider + '/one-actual20-selection', candidate and len(m.actors['owner']['learned']) == 1 and m.actors['owner']['learned'][sid]['event'] == 'actual-selected20/' + sid)
            other = next(x for x in ids if x != sid)
            reject(sid + '/' + provider + '/no-second-free20-selection', m, lambda: m.learn('owner', other, 20, 'second-free'), 'No unspent')
            before = m.snapshot(); m.actors['owner']['providerRetained'] = False
            reject(sid + '/' + provider + '/lost-provider', m, lambda: m.route('owner', sid), 'no longer retained')
            m.actors['owner']['providerRetained'] = True
            check(sid + '/' + provider + '/restore-premise-preserves-original-history', m.snapshot() == before)
            if provider == 'Shaman':
                m.actors['owner']['heroPath'] = 'Bloodcaller'
                reject(sid + '/Bloodcaller20-no-ordinary-route', m, lambda: m.route('owner', sid), 'lost ordinary Shaman')
                m.actors['owner']['heroPath'] = 'Soothsayer'
            record('actual20-selection-provider-loss/' + provider + '/' + sid, m)
            credential = m.replace_known('owner', sid, other, rest())
            check(sid + '/' + provider + '/legal-same-rank20-replacement', set(m.actors['owner']['learned']) == {other} and credential['rank'] == 7 and m.replacement_history[0]['oldCredential']['spellId'] == sid)
            reject(sid + '/' + provider + '/same-rest-only-one-replacement', m, lambda: m.replace_known('owner', other, sid, rest()), 'One replacement')
            reject(sid + '/' + provider + '/replacement-no-refilled-learning-slot', m, lambda: m.learn('owner', sid, 20, 'refill'), 'No unspent')
            record('20-same-rank-positive-control/' + provider + '/' + sid, m)
        m = fixture('Shaman', 19); m.actors['owner']['heroPath'] = 'Bloodcaller'
        reject(sid + '/Bloodcaller19-no-ordinary-route', m, lambda: m.route('owner', sid), 'lost ordinary Shaman')
        record('Bloodcaller19/' + sid, m)

    extra = [A / 'DI7_ACQ19_RECEIVED.json', R / 'tools/di7_cast_transactions.py', R / 'tools/di7_acquisition_transactions.py',
        R / 'tools/validate_di7_acquisition_matrix.py', R / 'data/playtest/spell_candidates/divination_rank7_exact_01_expectations.json']
    report = {'status': 'pass', 'recordedAtUtc': datetime.now(timezone.utc).isoformat(), 'checks': len(checks), 'historyCount': len(histories),
        'sourceBindings': sources.bindings + [info(p) for p in extra], 'checkLabels': checks, 'histories': histories,
        'rankUpperBoundProofs': rank_proofs, 'failures': [], 'allSevenIdsCovered': ids,
        'scope': 'Each actual source placement, below-class gate, no19 learning/cast, actual lower-known replacement rejection, one selected20, no automatic second selection, retained-provider/Bloodcaller gates, legal same-rank replacement and unrefilled acquisition slot.',
        'qualification': 'Rank6-to7 is demonstrated as an exhaustive source-bound rank upper-bound/predicate proof, not a manufactured learned rank6 Mirrorsage card. Actual replacement histories use genuinely learned Fate Coin or an actually selected conditional rank7 at20. Rest completion is a supplied conditional campaign premise; rest activity, class advancement sessions and combat spell payloads are not simulated here.',
        'independentLevel19GrantInvented': False, 'candidateApproved': False, 'full49Fulfilled': False, 'humanPlaytest': False, 'spellPromotions': 0}
    output.write_bytes(encoded(report)); print(json.dumps({'report': info(output), 'checks': len(checks), 'histories': len(histories), 'status': 'pass'}))


if __name__ == '__main__': main()
