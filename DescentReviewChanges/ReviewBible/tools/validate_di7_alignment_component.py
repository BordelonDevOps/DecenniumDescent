"""Exercise AP-AS-01 conditional effect histories; upstream casts remain open."""
from copy import deepcopy
from datetime import datetime, timezone
import json
from apply_di7_ap_as_01 import G, R, A, V, info, encoded
from di7_alignment_component import AlignmentComponent


def axes(order='Lawful', ethics='Good'):
    return {'order': order, 'ethics': ethics}


def main():
    output = A / 'DI7_ALIGNMENT_COMPONENT_CHECK.json'
    assert not output.exists()
    catalog_path = R / 'data/public/spell_playtests/catalog.json'
    candidate_path = R / 'data/public/spell_candidates/divination_rank7_exact_01.json'
    catalog = json.loads(catalog_path.read_bytes())
    candidate = json.loads(candidate_path.read_bytes())
    spell_index = next(i for i, x in enumerate(catalog['spells']) if x['id'] == 'alignment-suggestion')
    candidate_index = next(i for i, x in enumerate(candidate['cards']) if x['id'] == 'alignment-purge')
    bindings = {'alignment-suggestion': {**info(catalog_path), 'pointer': f'/spells/{spell_index}/operational'},
        'alignment-purge': {**info(candidate_path), 'pointer': f'/cards/{candidate_index}/operationalCandidate'}}
    checks, histories = [], []

    def check(label, condition):
        assert condition, label
        checks.append(label)

    def fresh(target=None, immunities=None):
        actors = {}
        for actor, value in [('target', target or axes()), ('good', axes()), ('evil', axes('Chaotic', 'Evil')), ('purger', axes()), ('other', axes())]:
            actors[actor] = {'underlying': deepcopy(value), 'immunities': [],
                'permanentIdentity': {'actorId': actor, 'oath': 'conditional-original-oath', 'lineage': 'conditional-original-lineage'},
                'acquisitionSnapshots': ['unchanged-existing-source'], 'usedAllowances': {'existingUse': 1}}
        actors['target']['immunities'] = deepcopy(immunities or [])
        return AlignmentComponent(actors, bindings)

    def start(m, spell, caster, target, event):
        m.begin_conditional_committed_cast({'castId': event, 'spellId': spell, 'sourceBinding': bindings[spell],
            'caster': caster, 'target': target, 'committedAt': m.now, 'clockMode': 'outside-initiative-elapsed',
            'paymentPremise': {'kind': 'conditional-upstream-commit-not-executed-here', 'fixtureId': 'conditional-paid/' + event}})

    def cast(m, spell, caster, target, event, face=16, modifier=0, dc=17):
        start(m, spell, caster, target, event)
        return m.resolve(event, face=face, modifier=modifier, dc=dc)

    def save(name, m, original):
        for actor_id, actor in m.actors.items():
            for field in ['permanentIdentity', 'acquisitionSnapshots', 'usedAllowances', 'immunities']:
                check(name + ':' + actor_id + ':' + field + '-preserved', actor[field] == original[actor_id][field])
        histories.append({'id': name, 'fixtureKind': 'conditional-effect-component-only', 'initialActors': original, 'final': m.snapshot()})

    for face, modifier, applied in [(16, 0, True), (17, 0, False), (1, 20, False), (20, -10, True)]:
        m = fresh(); initial = deepcopy(m.actors)
        public = cast(m, 'alignment-purge', 'purger', 'target', 'p', face, modifier)
        check(f'binary-{face}-{modifier}', ('p' in m.effects) == applied)
        check('no-natural-override', m.casts['p']['save']['succeeded'] == (face + modifier >= 17))
        check('no-eligibility-diagnostic', public == {'resolutionComplete': True, 'informationGranted': False, 'refund': 0})
        save(f'binary-{face}-{modifier}', m, initial)
    for scope, applied in [('charmed', True), ('alignment-alteration', False)]:
        m = fresh(immunities=[{'source': 'conditional-real-defense', 'affects': scope}]); initial = deepcopy(m.actors)
        cast(m, 'alignment-purge', 'purger', 'target', 'p')
        check('immunity-scope-' + scope, ('p' in m.effects) == applied)
        save('immunity-' + scope, m, initial)
    for value in [axes(None, None), axes(None, 'Good'), axes('Lawful', None)]:
        m = fresh(value); initial = deepcopy(m.actors)
        public = cast(m, 'alignment-purge', 'purger', 'target', 'p')
        check('undefined-no-fabrication', not m.effects and m.effective('target') == value)
        check('undefined-no-public-diagnostic', public == {'resolutionComplete': True, 'informationGranted': False, 'refund': 0})
        save('undefined-' + str(value), m, initial)

    m = fresh(axes('Neutral', 'Neutral')); initial = deepcopy(m.actors)
    cast(m, 'alignment-purge', 'purger', 'target', 'p')
    check('already-neutral-application', 'p' in m.effects)
    m.advance(20); m.set_underlying('target', axes('Neutral', 'Evil'), 'independent-20')
    check('already-neutral-covers-new-base', m.effective('target') == axes('Neutral', 'Neutral'))
    m.advance(60)
    check('deadline-is-exclusive', m.effective('target') == axes('Neutral', 'Evil') and m.effects['p']['state'] == 'ended')
    save('already-neutral-and-real-base-change', m, initial)

    for order in ['suggestion-first', 'purge-first']:
        m = fresh(); initial = deepcopy(m.actors)
        if order == 'suggestion-first':
            cast(m, 'alignment-suggestion', 'evil', 'target', 's')
            m.advance(1); cast(m, 'alignment-purge', 'purger', 'target', 'p')
        else:
            cast(m, 'alignment-purge', 'purger', 'target', 'p')
            m.advance(1); cast(m, 'alignment-suggestion', 'evil', 'target', 's')
        check(order + ':target-excludes-purge', m.effects['s']['values'] == axes('Neutral', 'Neutral'))
        check(order + ':purge-covers', m.effective('target') == axes('Neutral', 'Neutral'))
        m.advance(2); cast(m, 'alignment-suggestion', 'good', 'target', 'no-change')
        check(order + ':no-change-no-replacement', 'no-change' not in m.effects and m.effects['s']['state'] == 'live')
        m.set_underlying('target', axes('Neutral', 'Evil'), order + '-real-change')
        m.end('p', 'conditional-dispel')
        check(order + ':end-purge-exposes-fixed-suggestion', m.effective('target') == axes('Neutral', 'Neutral'))
        m.end('s', 'conditional-dispel')
        check(order + ':end-suggestion-exposes-current-base', m.effective('target') == axes('Neutral', 'Evil'))
        save(order, m, initial)

    m = fresh(); initial = deepcopy(m.actors)
    cast(m, 'alignment-purge', 'purger', 'good', 'p-on-caster')
    cast(m, 'alignment-suggestion', 'good', 'target', 's')
    check('purged-caster-snapshot', m.casts['s']['orientationSnapshot'] == axes('Neutral', 'Neutral'))
    check('purged-caster-really-shifts', m.effects['s']['values'] == axes('Neutral', 'Neutral'))
    m.end('p-on-caster', 'conditional-dispel')
    check('caster-later-change-no-recompute', m.effects['s']['values'] == axes('Neutral', 'Neutral'))
    save('purged-caster-current-effective-snapshot', m, initial)

    m = fresh(axes('Lawful', 'Neutral')); initial = deepcopy(m.actors)
    m.set_underlying('evil', axes('Lawful', 'Evil'), 'caster-direction')
    cast(m, 'alignment-suggestion', 'evil', 'target', 's')
    check('changed-axis-only', m.effects['s']['values'] == {'ethics': 'Evil'})
    m.set_underlying('target', axes('Chaotic', 'Good'), 'independent-changed-unoverlaid-axis')
    check('unoverlaid-axis-remains-live', m.effective('target') == axes('Chaotic', 'Evil'))
    cast(m, 'alignment-purge', 'purger', 'target', 'p')
    m.suppress('p', True)
    check('suppression-exposes-suggestion', m.effective('target') == axes('Chaotic', 'Evil'))
    m.advance(59.999); m.suppress('p', False)
    check('suppression-return-no-refresh', m.effective('target') == axes('Neutral', 'Neutral') and m.effects['p']['deadline'] == 60)
    m.advance(60)
    check('both-original-clocks-expire', m.effective('target') == axes('Chaotic', 'Good'))
    save('fixed-one-axis-suppression-and-expiry', m, initial)

    for scenario in ['saved', 'countered', 'undefined', 'valid-replacement']:
        m = fresh(); initial = deepcopy(m.actors)
        cast(m, 'alignment-purge', 'purger', 'target', 'old')
        m.advance(10)
        if scenario == 'undefined':
            m.set_underlying('target', axes(None, 'Good'), 'independent-axis-removed')
        if scenario == 'countered':
            start(m, 'alignment-purge', 'other', 'target', 'new'); m.counter_conditional_cast('new')
        else:
            cast(m, 'alignment-purge', 'other', 'target', 'new', face=17 if scenario == 'saved' else 16)
        check(scenario + ':only-valid-replaces', (m.effects['old']['state'] == 'ended') == (scenario == 'valid-replacement'))
        if scenario == 'valid-replacement':
            check('replacement-one-family-and-new-clock', m.effects['new']['deadline'] == 70 and 'purger' not in m.concentration)
        else:
            check(scenario + ':no-old-clock-extension', m.effects['old']['deadline'] == 60)
        check(scenario + ':no-refund', m.casts['new']['refund'] == 0)
        save('replacement-' + scenario, m, initial)

    for scenario in ['saved', 'countered', 'no-change-suggestion']:
        m = fresh(); initial = deepcopy(m.actors)
        cast(m, 'alignment-purge', 'purger', 'target', 'old')
        if scenario == 'countered':
            start(m, 'alignment-purge', 'purger', 'target', 'new'); m.counter_conditional_cast('new')
        elif scenario == 'saved':
            cast(m, 'alignment-purge', 'purger', 'target', 'new', face=17)
        else:
            cast(m, 'alignment-suggestion', 'purger', 'target', 'new')
        check('same-caster-no-restoration-' + scenario, m.effects['old']['state'] == 'ended' and m.effective('target') == axes())
        save('same-caster-' + scenario, m, initial)
    for ending in ['death', 'incapacitated', 'failed-concentration-save', 'voluntary-end']:
        m = fresh(); initial = deepcopy(m.actors)
        cast(m, 'alignment-purge', 'purger', 'target', 'p')
        m.caster_loses_concentration('purger', ending)
        check(ending + ':ends-purge', m.effects['p']['state'] == 'ended' and m.effective('target') == axes())
        save('caster-' + ending, m, initial)

    m = fresh(); initial = deepcopy(m.actors)
    cast(m, 'alignment-purge', 'purger', 'target', 'p')
    for label, action in [('duplicate-resolution', lambda: m.resolve('p', face=16, modifier=0, dc=17)),
            ('negative-time', lambda: m.advance(-1)), ('nonfinite-time', lambda: m.advance(float('nan'))),
            ('unknown-axis', lambda: m.set_underlying('target', axes('Unaligned', 'Good'), 'bad'))]:
        before = m.snapshot()
        try:
            action()
        except ValueError:
            check(label + ':rejected-without-mutation', m.snapshot() == before)
        else:
            raise AssertionError(label)
    save('invalid-component-requests', m, initial)
    report = {'recordedAtUtc': datetime.now(timezone.utc).isoformat(), 'status': 'pass', 'checks': len(checks), 'passedChecks': checks, 'failures': [],
        'sourceBindings': [info(catalog_path), info(candidate_path), info(V / 'ALIGNMENT_SUGGESTION_AP_AS_01.json'),
            info(R / 'tools/di7_alignment_component.py'), info(R / 'tools/validate_di7_alignment_component.py')],
        'historyCount': len(histories), 'histories': histories,
        'scope': 'Conditional AP-AS-01 effect resolution, binary save operands, named immunity, fixed overlays, concentration displacement/replacement and outside-initiative elapsed deadlines. Complete casting, source acquisition and payment are explicitly upstream premises, not executed here.',
        'expectationCoverage': [{'id': 'D7T-13-0' + str(i), 'status': 'component-evidence-only; complete-cast integration still required'} for i in range(1, 5)],
        'remaining': ['Source-qualified actual actor acquisition/repertoire and ordinary cast payment/components/target/counter sequence.',
            'Shared initiative/virtual-phase clock integration for the unchanged Alignment Suggestion duration.',
            'All other DI7 expectations and separate exact review of complete seven candidates.'],
        'all49FiniteVariantsFulfilled': False, 'exactCardsApproved': False, 'runtimeImplemented': False, 'humanPlaytested': False,
        'sourceInformationDeleted': 0, 'cosmologyReviewed': False, 'pushed': False}
    output.write_bytes(encoded(report))
    print(json.dumps({'report': info(output), 'checks': len(checks), 'histories': len(histories), 'all49FiniteVariantsFulfilled': False}))


if __name__ == '__main__':
    main()
