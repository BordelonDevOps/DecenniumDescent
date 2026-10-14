"""Execute all four finite alignment expectations through actual paid casts."""
from copy import deepcopy
from datetime import datetime, timezone
import json
from apply_di7_ap_as_01 import G, R, A, info, encoded
from di7_cast_transactions import DI7Sources
from di7_area_fixtures import make as area_fixture
from di7_alignment_transactions import AlignmentTransactions


def axes(order='Lawful', ethics='Good'):
    return {'order': order, 'ethics': ethics}


def main():
    output = A/'DI7_ALIGNMENT_TRANSACTIONS_CHECK.json'
    assert not output.exists()
    sources = DI7Sources()
    checks, histories = [], []

    def check(label, value):
        assert value, label
        checks.append(label)

    def make(provider='Wizard', target=None, immunities=None):
        base, _ = area_fixture(sources, provider=provider)
        actors, world = deepcopy(base.actors), deepcopy(base.world)
        for aid in ['good', 'other']:
            actors[aid] = deepcopy(actors['counter'])
            actors[aid]['body']['focus'].update(id='focus/'+aid, owner=aid)
            actors[aid]['body']['hands']['right']['holding'] = 'focus/'+aid
            world['entities'][aid] = deepcopy(world['entities']['counter'])
        world['entities']['target'] = {'kind': 'creature', 'positionFeet': 25, 'willing': True, 'alliedTo': {}, 'relatedQuestions': []}
        for aid in [*actors, 'target']:
            world['alignmentActors'][aid] = {'underlying': deepcopy(target if aid == 'target' and target is not None else axes('Chaotic', 'Evil') if aid == 'counter' else axes()),
                'immunities': deepcopy(immunities or []) if aid == 'target' else [],
                'permanentIdentity': {'id': aid, 'oath': 'conditional-existing-oath', 'lineage': 'conditional-existing-lineage'},
                'acquisitionSnapshots': ['conditional-existing-acquisition'], 'usedAllowances': {'existingUse': 1}}
        world['relations'] = {a+'>'+t: {'sourceFact': 'conditional-perceived-open-local-creature', 'perceived': True, 'visible': True, 'lineOfEffect': True} for a in actors for t in [*actors, 'target']}
        m = AlignmentTransactions(sources, actors, world)
        for aid, actor in m.actors.items():
            m.learn(aid, 'alignment-purge', actor['classLevel'], aid+'/actual-Purge-acquisition')
            if actor['provider'] in {'Wizard', 'Mirrorsage'}:
                m.learn(aid, 'alignment-suggestion', 1, aid+'/actual-Suggestion-acquisition')
            if actor['provider'] == 'Wizard':
                m.learn(aid, 'counterspell', 5, aid+'/actual-Counter-acquisition')
                m.prepare_wizard(aid, list(actor['learned']), aid+'/study', {'actor': aid, 'completedAt': 0, 'sourceEvent': 'conditional-completed-own-rest'})
        return m

    def cast(m, aid, sid, cid, *, target='target', face=16, modifier=0, at=None, counter=False):
        if at is not None:
            m.advance(at)
        m.begin_turn(aid, cid+'/conditional-legal-ordinary-turn')
        before = deepcopy(m.actors[aid])
        receipt = m.declare(aid, sid, cid, {'target': target})
        check(cid+'/actual-RP-payment', m.actors[aid]['rp'] == before['rp']-receipt['quote']['cost'])
        check(cid+'/actual-Action-strain-history', m.actors[aid]['actions'] == 0 and m.actors[aid]['previousSpell'] == sid and m.actors[aid]['dissonance'] == before['dissonance']+receipt['dissonanceAdded'])
        if counter:
            responder = 'other' if aid != 'other' else 'good'
            m.declare(responder, 'counterspell', cid+'/counter', {'pendingCast': cid})
            m.resolve_counter(cid+'/counter', 20)
            return None
        return m.resolve_alignment(cid, face=face, modifier=modifier)

    def record(label, m):
        for aid, actor in m.alignment.actors.items():
            original = m.world['alignmentActors'][aid]
            for field in ['permanentIdentity', 'acquisitionSnapshots', 'usedAllowances', 'immunities']:
                assert actor[field] == original[field], (label, aid, field)
        histories.append({'id': label, 'final': m.snapshot()})

    for face, modifier, applied in [(16, 0, True), (17, 0, False), (1, 20, False), (20, -10, True)]:
        m = make()
        result = cast(m, 'owner', 'alignment-purge', 'purge', face=face, modifier=modifier)
        check('binary/'+str(face)+'/'+str(modifier), ('purge' in m.alignment.effects) == applied and m.casts['purge']['dc'] == 17)
        check('binary-no-diagnostic/'+str(face)+'/'+str(modifier), result == {'resolutionComplete': True, 'informationGranted': False, 'refund': 0} and m.actors['owner']['rp'] == 31)
        record('paid-binary/'+str(face)+'/'+str(modifier), m)
    for scope, applied in [('charmed', True), ('alignment-alteration', False)]:
        m = make(immunities=[{'source': 'conditional-actual-scoped-defense', 'affects': scope}])
        cast(m, 'owner', 'alignment-purge', 'purge')
        check(scope+'/actual-scope-after-payment', ('purge' in m.alignment.effects) == applied and m.actors['owner']['rp'] == 31)
        record('paid-immunity/'+scope, m)
    for i, value in enumerate([axes(None, None), axes(None, 'Good'), axes('Lawful', None)]):
        m = make(target=value)
        result = cast(m, 'owner', 'alignment-purge', 'purge')
        check('undefined/'+str(i), not m.alignment.effects and m.alignment.effective('target') == value and result['informationGranted'] is False and m.actors['owner']['rp'] == 31)
        record('paid-undefined/'+str(i), m)
    for provider in ['Wizard', 'Cleric', 'Mirrorsage', 'Shaman']:
        m = make(provider, target=axes('Neutral', 'Neutral'))
        cast(m, 'owner', 'alignment-purge', 'purge', face=1)
        m.alignment.set_underlying('target', axes('Neutral', 'Evil'), 'conditional-independent-real-change')
        check(provider+'/already-neutral-covers-new-base', m.alignment.effective('target') == axes('Neutral', 'Neutral'))
        m.advance(3660)
        check(provider+'/original-clock-current-base', m.alignment.effective('target') == axes('Neutral', 'Evil') and m.actors['owner']['concentration'] is None)
        record('paid-already-neutral/'+provider, m)
    for order in ['suggestion-first', 'purge-first']:
        m = make()
        if order == 'suggestion-first':
            cast(m, 'counter', 'alignment-suggestion', 'suggestion', at=3600)
            cast(m, 'owner', 'alignment-purge', 'purge', at=3601)
        else:
            cast(m, 'owner', 'alignment-purge', 'purge', at=3600)
            cast(m, 'counter', 'alignment-suggestion', 'suggestion', at=3601)
        check(order+'/real-separate-concentrators', m.actors['owner']['concentration'] == 'purge' and m.actors['counter']['concentration'] == 'suggestion')
        check(order+'/target-baseline-excludes-both', m.alignment.effects['suggestion']['values'] == axes('Neutral', 'Neutral'))
        cast(m, 'good', 'alignment-suggestion', 'no-change', at=3602)
        check(order+'/paid-no-change-no-replacement', 'no-change' not in m.alignment.effects and m.alignment.effects['suggestion']['state'] == 'live' and m.actors['good']['rp'] == 46)
        m.alignment.set_underlying('target', axes('Neutral', 'Evil'), order+'/conditional-independent-underlying-change')
        m.end_alignment('purge', 'dispel', order+'/conditional-legal-dispel-Purge')
        check(order+'/Suggestion-survives', m.alignment.effective('target') == axes('Neutral', 'Neutral'))
        m.end_alignment('suggestion', 'voluntary-end', order+'/actual-caster-ends')
        check(order+'/current-base-not-snapshot', m.alignment.effective('target') == axes('Neutral', 'Evil'))
        record('paid-overlay-order/'+order, m)
    m = make()
    cast(m, 'owner', 'alignment-purge', 'purge-caster', target='good')
    cast(m, 'good', 'alignment-suggestion', 'suggestion', at=3601)
    check('actual-purged-caster-effective-snapshot', m.alignment.casts['suggestion']['orientationSnapshot'] == axes('Neutral', 'Neutral'))
    m.end_alignment('purge-caster', 'dispel', 'conditional-actual-caster-overlay-dispel')
    check('snapshot-does-not-recompute', m.alignment.effects['suggestion']['values'] == axes('Neutral', 'Neutral'))
    record('paid-purged-caster', m)
    for scenario in ['saved', 'countered', 'undefined', 'valid']:
        m = make()
        cast(m, 'owner', 'alignment-purge', 'old')
        if scenario == 'undefined':
            m.alignment.set_underlying('target', axes(None, 'Good'), 'conditional-real-axis-no-longer-defined')
        cast(m, 'good', 'alignment-purge', 'new', at=3602, face=17 if scenario == 'saved' else 16, counter=scenario == 'countered')
        check(scenario+'/only-valid-replaces-other-caster', (m.alignment.effects['old']['state'] == 'ended') == (scenario == 'valid'))
        check(scenario+'/old-clock-not-refreshed', m.alignment.effects['old']['deadline'] == 3660)
        check(scenario+'/paid-kept', m.actors['good']['rp'] == 31)
        if scenario == 'valid':
            check('valid/immediate-old-concentration-cleared', m.actors['owner']['concentration'] is None and m.actors['good']['concentration'] == 'new' and m.alignment.effects['new']['deadline'] == 3662)
        record('paid-replacement/'+scenario, m)
    for scenario in ['saved', 'countered', 'no-change']:
        m = make()
        cast(m, 'owner', 'alignment-purge', 'old')
        sid = 'alignment-suggestion' if scenario == 'no-change' else 'alignment-purge'
        cast(m, 'owner', sid, 'new', at=3606, face=17 if scenario == 'saved' else 16, counter=scenario == 'countered')
        check(scenario+'/cast-start-loss-never-restored', m.alignment.effects['old']['state'] == 'ended' and m.actors['owner']['concentration'] is None and m.alignment.effective('target') == axes())
        record('paid-same-caster/'+scenario, m)
    for change in ['moved', 'unperceived', 'blocked', 'incapacitated', 'lost-concentration']:
        m = make()
        m.begin_turn('owner', 'conditional-owner-turn')
        m.declare('owner', 'alignment-purge', 'pending', {'target': 'target'})
        if change == 'moved': m.world['entities']['target']['positionFeet'] = 121
        elif change == 'unperceived': m.world['relations']['owner>target']['perceived'] = False
        elif change == 'blocked': m.world['relations']['owner>target']['lineOfEffect'] = False
        elif change == 'incapacitated': m.actors['owner']['body']['canAct'] = False
        else: m.actors['owner']['concentration'] = None
        m.events.append({'kind': 'conditional-legal-intervening-world-event', 'sourceEvent': change, 'at': m.now})
        result = m.resolve_alignment('pending', face=16, modifier=0)
        check(change+'/actual-current-boundary-no-free-effect', not m.alignment.effects and m.casts['pending']['status'] == 'failed-payload-no-refund' and m.actors['owner']['rp'] == 31 and m.actors['owner']['concentration'] is None and result['informationGranted'] is False)
        record('paid-interruption/'+change, m)
    for ending in ['death', 'incapacitated', 'failed-concentration-save', 'voluntary-end']:
        m = make()
        cast(m, 'owner', 'alignment-purge', 'purge')
        m.end_alignment('purge', ending, 'conditional-source-qualified-ending/'+ending)
        check(ending+'/paid-effect-ends-no-refund', m.alignment.effective('target') == axes() and m.actors['owner']['concentration'] is None and m.actors['owner']['rp'] == 31)
        record('paid-ending/'+ending, m)
    coverage = {
        'D7T-13-01': [h['id'] for h in histories if h['id'].startswith(('paid-binary/', 'paid-immunity/', 'paid-undefined/'))],
        'D7T-13-02': ['paid-overlay-order/suggestion-first', 'paid-overlay-order/purge-first', 'paid-purged-caster'],
        'D7T-13-03': ['paid-overlay-order/suggestion-first', 'paid-overlay-order/purge-first'],
        'D7T-13-04': [h['id'] for h in histories if h['id'].startswith(('paid-replacement/', 'paid-same-caster/'))]}
    report = {'status': 'pass', 'recordedAtUtc': datetime.now(timezone.utc).isoformat(), 'checks': len(checks), 'historyCount': len(histories),
        'sourceBindings': sources.bindings+[info(p) for p in [R/'tools/di7_alignment_transactions.py', R/'tools/validate_di7_alignment_transactions.py', R/'tools/di7_alignment_clock.py', R/'tools/di7_alignment_component.py', R/'tools/di7_fate_transactions.py', R/'tools/di7_cast_transactions.py', R/'tools/di7_area_fixtures.py']],
        'checkLabels': checks, 'histories': histories, 'sourceExpectationCoverage': coverage, 'failures': [],
        'scope': 'All four D7T-13 finite expectations through real conditional repertoire, preparation, Action/RP/strain, counter and concentration histories; current target and body resolution boundary; immediate cross-caster family replacement releases old concentration.',
        'conditionalPremises': ['Attained class/body/rest slices and legal turn chronology are explicit upstream premises, not full character builds or initiative simulation.',
            'Actual immunities, independent underlying changes, movement, dispel, damage-save failure and source death/incapacity are conditional Director-established events; this module does not acquire or execute their originating powers.',
            'Current effective axes are exercised and permanent identity, acquisition snapshots, used allowances and immunity records are preserved in every history. Arbitrary future oath/item/feat dependencies are not implemented.',
            'Source-specific timing is separately exercised by DI7_ALIGNMENT_CLOCK_CHECK; no source text or old successful report is replaced.'],
        'remaining': ['Compile all93 expectations with precise executed/source-only/external-pending boundaries, then submit the actual seven complete candidates for separate GPT exact review.'],
        'candidateApproved': False, 'full49Fulfilled': False, 'humanPlaytest': False, 'spellPromotions': 0, 'newRuleAdoptions': 0}
    output.write_bytes(encoded(report))
    print(json.dumps({'report': info(output), 'checks': len(checks), 'histories': len(histories), 'expectations': len(coverage)}))


if __name__ == '__main__':
    main()
