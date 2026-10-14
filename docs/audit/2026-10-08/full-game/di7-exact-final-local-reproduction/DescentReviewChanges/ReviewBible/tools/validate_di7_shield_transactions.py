"""Finite Shield histories; source-qualified premises are recorded, not hidden."""
from copy import deepcopy
from datetime import datetime, timezone
from apply_di7_ap_as_01 import G, R, A, info, encoded
from di7_cast_transactions import DI7Sources
from di7_shield_transactions import ShieldTransactions
from core_playtest_rules import LifeState, saving_throw
from redirection_playtest_rules import DamageRoot
import json


def main():
    output = A / 'DI7_SHIELD_TRANSACTIONS_CHECK.json'; assert not output.exists()
    sources = DI7Sources(); checks = []; histories = []
    def check(name, condition):
        assert condition, name
        checks.append(name)
    def reject(name, m, fn):
        before = m.snapshot()
        try: fn()
        except ValueError as error: check(name + '/rejected', bool(str(error)))
        else: raise AssertionError(name)
        check(name + '/atomic', before == m.snapshot())
    def record(name, m): histories.append({'id': name, 'final': m.snapshot()})
    def make(provider='Wizard', establish=True, target='target'):
        level = 13 if provider in {'Wizard', 'Cleric'} else 20
        actors = {}
        for aid, cls, lv, position in [('owner', provider, level, 0), ('donor', 'Wizard', 13, 10), ('counter', 'Wizard', 13, 20)]:
            actors[aid] = {'provider': cls, 'classLevel': lv, 'totalLevel': lv, 'abilityScore': 18,
                'attainmentPremise': 'Hypothetical ordinary-casting slice with attained level; not a complete acquired character or campaign playtest.',
                'heroPath': 'Soothsayer' if cls == 'Shaman' else 'Spellbinder' if cls == 'Wizard' else 'ordinary-provider-retained-premise',
                'specialization': 'Evocation', 'providerRetained': True, 'bookPresent': True, 'studyUninterrupted': True,
                'positionFeet': position, 'knownFactions': [], 'body': {'conscious': True, 'canAct': True,
                    'ordinarySpellProhibited': False, 'silenced': False, 'canSpeak': True, 'reactionLegal': True,
                    'hands': {'left': {'usable': True, 'holding': None}, 'right': {'usable': True, 'holding': 'focus/' + aid}},
                    'focus': {'id': 'focus/' + aid, 'owner': aid, 'qualifiedClasses': [cls], 'accessible': True}}}
        entities = {aid: {'kind': 'creature', 'positionFeet': pos, 'willing': True, 'alliedTo': {a: True for a in actors},
            'hands': deepcopy(actors[aid]['body']['hands']) if aid in actors else {'left': {'usable': True, 'holding': None}}, 'relatedQuestions': []}
            for aid, pos in [('owner', 0), ('donor', 10), ('counter', 20), ('target', 25), ('other', 30)]}
        world = {'entities': entities, 'alignmentActors': {a: {'underlying': {'order': 'Lawful', 'ethics': 'Good'},
            'immunities': [], 'permanentIdentity': {'id': a}, 'acquisitionSnapshots': [], 'usedAllowances': {}} for a in entities},
            'relations': {a + '>' + t: {'sourceFact': 'conditional-open-line', 'perceived': True, 'visible': True, 'lineOfEffect': True} for a in actors for t in entities},
            'establishedFactions': [], 'encounter': {'id': 'conditional-real-encounter', 'isRealEncounter': True}, 'identificationFacts': {}, 'triggerEvents': {}}
        m = ShieldTransactions(sources, actors, world)
        m.learn('owner', 'premonition-shield', level, 'owner/actual-selected-learning')
        m.learn('donor', 'premonition-shield', 13, 'donor/actual-selected-learning')
        m.learn('donor', 'fate-coin', 1, 'donor/earlier-coin-learning')
        m.learn('counter', 'counterspell', 5, 'counter/earlier-counter-learning')
        for aid, a in m.actors.items():
            if a['provider'] == 'Wizard': m.prepare_wizard(aid, list(a['learned']), aid + '/study', {'actor': aid, 'completedAt': 0, 'sourceEvent': 'conditional-completed-own-rest'})
        m.begin_turn('owner', 'owner/turn1')
        if establish:
            m.declare('owner', 'premonition-shield', 'ward', {'target': target}); m.resolve_shield('ward')
        return m
    def attack(m, aid, *, target='target', guardian=None, natural=12, amount=24, life=None, **kwargs):
        return m.weapon_attack(aid, target, natural=natural, modifier=5, armor_class=15, amount=amount,
            guardian=guardian, life=life or LifeState(100, 100, temp_hp=7),
            source_fact={'kind': 'conditional-upstream-legal-weapon-attack', 'id': aid,
                'retarget': 'conditional-legally-paid-Guardian-offer' if guardian else None}, **kwargs)
    def schedule(m, oid, *, components=3, origin=None, occasion='immediate', kind='spell-immediate', actual=True, direct='target', shares=None):
        receipt = {'id': oid, 'kind': kind, 'originId': origin or oid, 'occasionId': occasion,
            'actualResolution': actual, 'sourceFact': {'kind': 'conditional-source-qualified-upstream-occurrence',
                'scope': 'Incoming spell ownership/payment/scheduling supplied, not executed by this finite ward adapter.'},
            'components': [{'id': 'part' + str(i), 'rootId': oid + '/root' + str(i), 'directTargets': [direct] if direct else [], 'preShareTargets': shares or []} for i in range(components)]}
        m.register_occurrence(receipt); return receipt
    def packet(m, oid, i, *, amount=12, target='target', life=None, **kwargs):
        cid = 'part' + str(i); m.admit(oid, cid, target)
        root = DamageRoot(oid + '/root' + str(i), target, amount, 'force', attack_hit=True)
        result = m.resolve_packet(oid, cid, root, root.original_id, life or LifeState(100, 100, temp_hp=7), **kwargs)
        m.complete_component(oid, cid); return result

    for provider in ['Wizard', 'Cleric', 'Mirrorsage', 'Shaman']:
        m = make(provider); a = m.actors['owner']; w = m.wards['ward']
        check(provider + '/real-learning-own-RP-Action', a['learned']['premonition-shield']['atClassLevel'] == (13 if provider in {'Wizard', 'Cleric'} else 20) and a['rp'] == a['maxRP'] - 17 and a['actions'] == 0)
        check(provider + '/nonconcentration-two-unused-60seconds', a['concentration'] is None and w['remaining'] == 2 and w['deadline'] == 3660 and not w['claims'])
        check(provider + '/actual-class-strain', a['dissonance'] == (0 if provider == 'Wizard' else 2))
        record('paid-establishment-' + provider, m)
    m = make(); a, _, miss = attack(m, 'miss', natural=1)
    check('D7T05-miss-automatic-no-temp-loss', not miss['hit'] and m.wards['ward']['remaining'] == 1 and a.temp_hp == 7)
    a, event, hit = attack(m, 'hit', life_options={'maiming': True, 'wound_natural': 1, 'injury_d6': 3})
    check('D7T06-hit-Maiming-survives-zero-damage', hit['hit'] and event['actualDamageDealt'] == 0 and event['woundSaves'] == 1 and a.wounds == (3,) and a.temp_hp == 7)
    check('D7T05-second-completed-ends', m.wards['ward']['endedReason'] == 'second-occurrence-completed')
    a, event, _ = attack(m, 'third')
    check('D7T05-third-attack-unprotected', event['actualDamageDealt'] == 24 and a.hp == 83 and a.temp_hp == 0)
    record('miss-hit-Maiming-third-Multiattack-conditional-schedule', m)

    m = make(); schedule(m, 'saved', components=1)
    m.admit('saved', 'part0', 'target'); save = saving_throw(12, 5, 16)
    root = DamageRoot('saved/root0', 'target', 0 if save['success'] else 20, 'force', failed_save=not save['success'])
    _, event = m.resolve_packet('saved', 'part0', root, root.original_id, LifeState(100, 100))
    m.complete_component('saved', 'part0'); m.finish_occurrence('saved')
    check('D7T05-successful-zero-damage-save-consumes', save['success'] and m.wards['ward']['remaining'] == 1 and event['actualDamageDealt'] == 0)
    m.begin_turn('donor', 'donor/coin'); m.declare('donor', 'fate-coin', 'coin', {'target': 'target', 'hand': 'left'}); coin = m.resolve_fate_coin('coin')
    check('D7T05-actual-paid-beneficial-spell-consumes', coin['holder'] == 'target' and m.actors['donor']['rp'] == 46 and m.wards['ward']['ended'] and len(m.wards['ward']['claims']) == 2)
    record('save-and-actual-beneficial-FateCoin', m)
    m = make(); attack(m, 'zero-hit', amount=0)
    check('zero-damage-hit-consumes', m.wards['ward']['remaining'] == 1); record('zero-hit', m)

    m = make(); schedule(m, 'beams')
    for i in range(3): packet(m, 'beams', i)
    m.finish_occurrence('beams')
    check('D7T05-three-beams-one-use-distinct-roots', m.wards['ward']['remaining'] == 1 and len({x['root'] for x in m.packet_results}) == 3 and all(x['prevented'] == 12 for x in m.packet_results))
    schedule(m, 'tick', components=1, origin='beams', occasion='actual-source-tick1', kind='spell-scheduled'); packet(m, 'tick', 0); m.finish_occurrence('tick')
    check('D7T05-real-later-tick-second-use', m.wards['ward']['claims'] == ['beams', 'tick'] and m.wards['ward']['ended'])
    record('one-cast-three-roots-then-actual-scheduled-tick', m)
    m = make(); attack(m, 'first'); schedule(m, 'second')
    packet(m, 'second', 0); check('second-occurrence-held-open-with-zero-remaining', m.wards['ward']['remaining'] == 0 and not m.wards['ward']['ended'])
    _, event, _ = attack(m, 'interleaved-third')
    check('interleaved-third-cannot-borrow', event['actualDamageDealt'] == 24)
    packet(m, 'second', 1); packet(m, 'second', 2); m.finish_occurrence('second')
    check('second-later-components-still-prevented', [x['prevented'] for x in m.packet_results if x['occurrence'] == 'second'] == [12, 12, 12])
    record('second-group-interleaved-third', m)

    for guardian, intended, consumed in [('target', 'other', 1), ('other', 'target', 0)]:
        m = make(); _, event, result = attack(m, 'retarget', target=intended, guardian=guardian, natural=7)
        check('retarget-' + guardian + '/same-die-final-recipient', m.attack_results[-1]['natural'] == 7 and result['targetId'] == guardian and not result['hit'])
        check('retarget-' + guardian + '/only-final-ward', m.wards['ward']['remaining'] == 2 - consumed)
        record('retarget-to-' + guardian, m)
    m = make()
    for oid in ['canceled-attack', 'countered-spell', 'empty-space']:
        schedule(m, oid, components=1, actual=False); m.admit(oid, 'part0', 'target'); m.complete_component(oid, 'part0'); m.finish_occurrence(oid)
    schedule(m, 'covered-portion', components=1, direct=None)
    reject('excluded-total-cover-not-recipient', m, lambda: m.admit('covered-portion', 'part0', 'target'))
    m.complete_component('covered-portion', 'part0'); m.finish_occurrence('covered-portion')
    check('canceled-empty-covered-no-uses', m.wards['ward']['remaining'] == 2); record('nonoccurrences', m)

    bloodbond = 'crimson-agent.hero.bloodweaver.bloodbond'
    for protected in ['target', 'other']:
        m = make(target=protected); schedule(m, 'split', components=1, shares=['other']); m.admit('split', 'part0', 'target')
        root = DamageRoot('split/root0', 'target', 20, 'physical', attack_hit=True)
        root.transfer(bloodbond, 'conditional-qualified-bloodweaver', {'other': 5})
        _, direct_event = m.resolve_packet('split', 'part0', root, root.original_id, LifeState(100, 100))
        _, share_event = m.resolve_packet('split', 'part0', root, 'split/root0/transfer/1', LifeState(100, 100))
        m.complete_component('split', 'part0'); m.finish_occurrence('split')
        check('D7T06-split-' + protected + '/only-own-share', (direct_event['actualDamageDealt'], share_event['actualDamageDealt']) == ((0, 5) if protected == 'target' else (15, 0)))
        check('D7T06-split-' + protected + '/no-transferred-hit', not share_event['attackHit'] and share_event['transferred'] and m.wards['ward']['remaining'] == 1)
        record('actual20-to15and5-' + protected + '-protected-conditional-transfer-eligibility', m)
    m = make(target='other'); schedule(m, 'zero-share', components=1, shares=[]); m.admit('zero-share', 'part0', 'target')
    root = DamageRoot('zero-share/root0', 'target', 3, 'physical', attack_hit=True)
    # floor(3/4)=0 creates no transferred branch, operation or ward admission.
    m.resolve_packet('zero-share', 'part0', root, root.original_id, LifeState(100, 100)); m.complete_component('zero-share', 'part0'); m.finish_occurrence('zero-share')
    check('zero-share-no-branch-no-use', len(root.branches) == 1 and m.wards['ward']['remaining'] == 2); record('zero-share', m)
    m = make(target='other'); schedule(m, 'post', components=1, shares=[]); m.admit('post', 'part0', 'target')
    root = DamageRoot('post/root0', 'target', 20, 'physical', attack_hit=True); root.defend(root.original_id)
    root.transfer('monk.hero.enlightened-master.shared-breath', 'conditional-qualified-monk', {'other': 6}, scale=2, modifier=4)
    _, event = m.resolve_packet('post', 'part0', root, 'post/root0/transfer/1', LifeState(100, 100, temp_hp=2))
    root.resolve_living(root.original_id, LifeState(100, 100)); m.complete_component('post', 'part0'); m.finish_occurrence('post')
    check('D7T06-post-defense-skip-prevention-and-use', event['actualDamageDealt'] == 6 and event['tempAbsorbed'] == 2 and m.wards['ward']['remaining'] == 2 and not event['attackHit'])
    record('post-defense6-conditional-paid-source-eligibility', m)
    m = make(); attack(m, 'defenses', amount=24, defenses={'flat_reductions': (4, 6), 'resistant': True})
    check('defenses-before-Shield-before-tempHP', m.packet_results[-1]['afterDefenses'] == 9 and m.packet_results[-1]['prevented'] == 9 and m.packet_results[-1]['lifeAfter']['temp_hp'] == 7)
    record('strongest-flat-then-resistance-then-ward', m)

    for outcome in ['success', 'countered', 'invalidated']:
        m = make(); attack(m, 'old-use'); m.begin_turn('donor', 'replacement-turn'); m.declare('donor', 'premonition-shield', 'new', {'target': 'target'})
        if outcome == 'countered':
            m.declare('counter', 'counterspell', 'counter-new', {'pendingCast': 'new'}); m.resolve_counter('counter-new', 20)
        else:
            if outcome == 'invalidated': m.world['entities']['target']['willing'] = False
            m.resolve_shield('new')
        check('replacement-' + outcome, (m.wards['ward']['ended'] and m.wards['new']['remaining'] == 2 and m.current_wards['target'] == 'new') if outcome == 'success' else (not m.wards['ward']['ended'] and m.wards['ward']['remaining'] == 1 and m.current_wards['target'] == 'ward' and 'new' not in m.wards))
        check('replacement-' + outcome + '/all-costs-kept', m.actors['donor']['rp'] == 31 and m.casts['new']['refund'] == 0)
        record('replacement-' + outcome, m)
    m = make(); m.actors['owner']['body'].update(conscious=False, canAct=False); m.world['entities']['owner']['dead'] = True
    _, event, _ = attack(m, 'after-caster-death')
    check('caster-death-does-not-end', event['actualDamageDealt'] == 0 and not m.wards['ward']['ended'])
    m.world['entities']['target']['dead'] = True; m.advance(3601)
    check('recipient-death-ends', m.wards['ward']['endedReason'] == 'recipient-ended-or-removed'); record('caster-and-recipient-death', m)

    for termination in ['suppression', 'expiry', 'dispel']:
        m = make(); attack(m, 'first'); schedule(m, 'second'); packet(m, 'second', 0)
        if termination == 'suppression': m.suppress_ward('ward', True)
        elif termination == 'expiry': m.advance(3660)
        else: m.end_ward('ward', 'conditional-legally-resolved-dispel')
        packet(m, 'second', 1)
        if termination == 'suppression': m.suppress_ward('ward', False)
        packet(m, 'second', 2); m.finish_occurrence('second')
        check('per-component-' + termination, [x['prevented'] for x in m.packet_results if x['occurrence'] == 'second'] == ([12, 0, 12] if termination == 'suppression' else [12, 0, 0]))
        check('no-refund-' + termination, m.wards['ward']['remaining'] == 0 and m.actors['owner']['rp'] == 31)
        record('second-component-' + termination, m)
    m = make(); m.suppress_ward('ward', True); attack(m, 'suppressed-whole'); m.suppress_ward('ward', False)
    check('D7T07-suppression-no-use-clock-unchanged', m.wards['ward']['remaining'] == 2 and m.wards['ward']['deadline'] == 3660)
    m.advance(3660); _, event, _ = attack(m, 'exact-deadline')
    check('D7T07-half-open-deadline', event['actualDamageDealt'] == 24 and m.wards['ward']['remaining'] == 2 and m.wards['ward']['endedAt'] == 3660)
    record('suppressed-whole-and-exact-deadline', m)
    m = make(); receipt = schedule(m, 'real'); renamed = deepcopy(receipt); renamed['id'] = 'renamed'
    reject('renamed-packet-no-new-occurrence', m, lambda: m.register_occurrence(renamed))
    for kind in ['passive-query', 'direct-HP-payment', 'HP-assignment', 'environmental-fall', 'nonattack-nonspell']:
        bad = deepcopy(receipt); bad.update(id=kind, originId=kind, kind=kind)
        reject(kind + '-outside-ward', m, lambda bad=bad: m.register_occurrence(bad))
    record('identity-and-non-damage-boundaries', m)
    m = make(); m.suppress_ward('ward', True); schedule(m, 'ambiguous'); packet(m, 'ambiguous', 0); m.suppress_ward('ward', False)
    reject('open-seam-late-first-admission-fails-closed', m, lambda: m.admit('ambiguous', 'part1', 'target'))
    record('explicit-unresolved-late-first-admission', m)

    extra = [R / 'tools' / name for name in ['di7_shield_transactions.py', 'validate_di7_shield_transactions.py',
        'di7_fate_transactions.py', 'di7_cast_transactions.py', 'redirection_playtest_rules.py', 'core_playtest_rules.py', 'healing_playtest_rules.py']]
    extra += [R / 'docs/mechanics/DAMAGE_SHARING_PLAYTEST.md', R / 'data/playtest/spell_candidates/divination_rank7_exact_01_expectations.json']
    report = {'status': 'pass', 'recordedAtUtc': datetime.now(timezone.utc).isoformat(), 'checks': len(checks), 'historyCount': len(histories),
        'sourceBindings': sources.bindings + [info(p) for p in extra], 'checkLabels': checks, 'histories': histories, 'failures': [],
        'scope': 'Actual conditional Shield and Fate Coin learning/preparation/payment/counter plus finite ward lifecycle, fixed incoming occurrence grouping, existing damage-sharing/defense/life-state execution.',
        'conditionalPremises': ['Attained ordinary-provider character slices, body/world/target facts and completed initial rest.',
            'Incoming attack legality and Guardian eligibility/Reaction/use supplied; the unchanged die, final target, ward, damage and Maiming save are executed.',
            'Incoming damaging spell/beam/tick source schedule and finalized raw damage supplied, not whole source cast execution.',
            'Bloodbond/Shared Breath ownership, range, willingness, paid source action and cadence supplied; actual split/stages/branch identity/life are executed.',
            'Legal suppression/dispel events and independent recipient death are supplied campaign events.'],
        'openSeams': ['First component while suppressed/unavailable, later first ward admission during the same occurrence: explicitly rejected pending GPT clarification.',
            'Full acquisition/attack/source-feature schedulers and all ordinary spell payloads are not implemented by this report.',
            'Independent control, movement, item damage, lethal assignments and source-specific concentration endings beyond the executed Maiming/life interface remain source-owned.'],
        'candidateApproved': False, 'full49Fulfilled': False, 'humanPlaytest': False, 'spellPromotions': 0}
    output.write_bytes(encoded(report)); print(json.dumps({'report': info(output), 'checks': len(checks), 'histories': len(histories), 'status': 'pass'}))


if __name__ == '__main__': main()
