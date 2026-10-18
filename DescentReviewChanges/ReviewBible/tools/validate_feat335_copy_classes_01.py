"""Actual class credentials, shared resources, paid totems and Mirror cap tests."""
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
import ast, json, sys
from feat335_copy_class_fixtures import ClassCopyFixtures, R, G, A
from feat335_copy_class_release import SharedClassWallet
from creature_lifecycle_playtest_rules import CreatureWorld, SourceStats, CommandLedger
from control_playtest_rules import ClockMarker
from validate_feat335_copy_payloads_01 import clean
from validate_feat_exact_01_composite_casting import info


def main():
    write = sys.argv[1:] == ['--write-report']
    if sys.argv[1:] and not write: raise ValueError('Use no arguments or --write-report')
    output = A / 'FEAT335_COPY_CLASSES_01_CHECK.json'
    if write: assert not output.exists(), 'Preserve prior successful evidence'
    f = ClassCopyFixtures(); checks = []; histories = []
    paths = f.paths + [Path(__file__), R/'data/public/class_playtests/shaman.json',
        R/'data/public/class_playtests/mirrorsage.json', R/'docs/mechanics/CLASS_PLAYTEST_RULES.md',
        R/'docs/mechanics/SPELL_INTEGRATION_RULES.md', R/'data/public/feat_candidates/exact_01/shared_rules.json',
        A/'feat335-copy-release-source-addendum-01/FEAT335_COPY_RELEASE_SOURCE_ADDENDUM_01.json',
        A/'FEAT335_COPY_RELEASE_SOURCE_01_RECEIVED_DECISION.json', A/'DI7_SHAMAN_VENT_RECEIVED.json',
        A/'FEAT335_COPY_RELEASE_01_CHECK.json', A/'FEAT335_COPY_PAYLOADS_01_CHECK.json']
    # Actual Shaman sources include dependencies used to construct its ordinary
    # caster interface; an included candidate is not approved by these tests.
    from di7_shaman_transactions import ShamanSources
    ds = ShamanSources()
    paths += [G/b['path'] for b in ds.bindings if G/b['path'] not in paths]
    pending = [p for p in paths if p.suffix == '.py']; seen = set()
    while pending:
        p = pending.pop()
        if p in seen: continue
        seen.add(p)
        for node in ast.walk(ast.parse(p.read_text('utf8'))):
            names = [node.module] if isinstance(node, ast.ImportFrom) else [a.name for a in node.names] if isinstance(node, ast.Import) else []
            for name in names:
                dep = R/'tools'/((name or '').split('.')[0]+'.py')
                if dep.exists():
                    if dep not in paths: paths.append(dep)
                    pending.append(dep)
    bindings = [info(p) for p in paths]
    def check(label, ok):
        assert ok, label
        checks.append({'id': label, 'passed': True})
    def reject(label, m, fn):
        before = m.snapshot()
        try: fn()
        except ValueError as e: check(label+'/rejected', bool(str(e)))
        else: raise AssertionError(label)
        check(label+'/atomic', m.snapshot() == before)
    def record(label, m, extra=None):
        histories.append({'id': label, 'state': m.snapshot(), 'additionalEvidence': extra})
    def next_round(m):
        n = m.captures.regular_ordinal + 1
        m.captures.end_regular(m.captures.current_turn, actual_regular_end=True)
        m.captures.start_regular('turn'+str(n), n, n, actual_new_regular_start=True)
        m.action_account.update(actions=1, turnId='turn'+str(n), bonus_action=True, reaction=True)
    def resolve(m, profile):
        if profile in {'mend', 'ward'}: rolls = {'nativeDice': [4, 4]}
        elif profile == 'strike': rolls = {'nativeDice': [4], 'targets': {'target': {'faces': [12], 'core': f.core()}}}
        elif profile == 'burst': rolls = {'nativeDice': [4, 4], 'targets': {'target': {'faces': [1], 'core': f.core()}}}
        elif profile == 'hindrance': rolls = {'faces': [1]}
        else: rolls = {}
        return m.resolve('cast', rolls=rolls)

    for name in ['Shaman', 'Mirrorsage']:
        h = f.class_acquisition(name)
        check(name+'/actual-paid-class-ASIs', [r['opportunity'] for r in h.pay.grants] == [name+':4', name+':8', name+':12'])
        check(name+'/never-Wizard-or-full-training', not h.casting.wizard_level and 'Wizard/class-engine' not in h.casting.grants and h.training_projection is None)
        check(name+'/native-route-is-not-personal-feat', all(r['kind'] == 'native-known' for r in h.casting.native_routes))
        for level in [1, 3, 4, 7, 10, 13, 16, 19, 20]:
            h = f.class_acquisition(name, level)
            maximum = h.class_source['maxSpellRankByClassLevel'][level-1]
            check(name+'/ceiling/'+str(level), h.provider(name+'/class-engine', maximum)['maximumLearnableRank'] == maximum)
            reject(name+'/over-ceiling/'+str(level), h, lambda: h.provider(name+'/class-engine', maximum+1))
        h = f.class_acquisition(name, 1, learn=False)
        reject(name+'/class-level-alone-not-casting-credential', h, lambda: h.provider(name+'/class-engine', 0))
        reject(name+'/foreign-spell-not-native', h, lambda: h.native_known([{'spellId': 'arcane-ray', 'atClassLevel': 1, 'event': 'bad'}], 'bad'))
        reject(name+'/premature-rank3-learning', h, lambda: h.native_known([{'spellId': 'slow', 'atClassLevel': 1, 'event': 'bad'}], 'bad'))
        h = f.class_acquisition(name, 1); h.advance(4); h.earn(4)
        h.casting.grants[name+'/class-engine']['removedAt'] = 4
        reject(name+'/removed-route-no-feat-prerequisite', h, lambda: h.acquire_copy('eldritch_echo', 4))
        for profile in ['strike', 'burst', 'mend', 'ward', 'hindrance', 'boon', 'step']:
            m, _ = f.class_make(name); f.capture_class(m, profile)
            prior_routes = m.captures.acquired.casting.snapshot()
            rp = m.pool['rp']; cast = f.declare_class(m, profile)
            check(name+'/'+profile+'/actual-ability', cast['provider']['ability'] == ('WIS' if name == 'Shaman' else 'INT') and cast['spellAttack'] == 8 and cast['spellDC'] == 16)
            check(name+'/'+profile+'/one-payment-no-protected-engine', m.pool['rp'] == rp-cast['quote']['cost'] and not cast['quote']['classHooksApplied'] and cast['quote']['limit'] == 12 and m.pool['actions'] == 0)
            check(name+'/'+profile+'/payload-executed', resolve(m, profile)['resolved'])
            check(name+'/'+profile+'/no-original-learning', m.captures.acquired.casting.snapshot() == prior_routes and not cast['newRepertoire'])
            record(name+'/'+profile, m)
        m, _ = f.class_make(name); f.capture_class(m, 'mend')
        m.captures.acquired.native_state['providerRetained'] = False
        reject(name+'/provider-lost-after-capture', m, lambda: f.declare_class(m, 'mend'))
        m, _ = f.class_make(name); f.capture_class(m, 'mend'); m.pool['rp'] = 1
        reject(name+'/insufficient-real-RP', m, lambda: f.declare_class(m, 'mend'))
        m, _ = f.class_make(name); f.capture_class(m, 'mend'); m.pool['maxRP'] += 1
        reject(name+'/cannot-create-extra-copy-pool', m, lambda: f.declare_class(m, 'mend'))
        m, _ = f.class_make(name); f.capture_class(m, 'mend')
        frame = f.frame(m); frame['actions'] = 2
        reject(name+'/forged-extra-Action', m, lambda: m.declare('bad', 'capture', permission='pending', grant_id=name+'/class-engine', frame=frame, selection=f.selection('mend')))
        m, _ = f.class_make(name); f.capture_class(m, 'mend')
        frame = f.frame(m); frame['unmodifiedPrice'] = False
        reject(name+'/unsupported-price-hook-fails-closed', m, lambda: m.declare('bad', 'capture', permission='pending', grant_id=name+'/class-engine', frame=frame, selection=f.selection('mend')))
        m, _ = f.class_make(name); f.capture_class(m, 'mend')
        m.captures.acquired.pay.suppressed.add('mimicry')
        reject(name+'/suppressed-paid-feat', m, lambda: f.declare_class(m, 'mend'))
        m, _ = f.class_make(name); f.capture_class(m, 'mend')
        m.cadence['dissonance'] = 18
        reject(name+'/actual-feat-Limit-Fractured-block', m, lambda: f.declare_class(m, 'mend'))
        m, _ = f.class_make(name); f.capture_class(m, 'mend'); m.cadence['dissonance'] = 12
        rp = m.pool['rp']; cast = f.declare_class(m, 'mend')
        check(name+'/actual-feat-Limit-surcharge', cast['quote']['surcharge'] == 1 and m.pool['rp'] == rp-3)

    # The actual paid Shaman totem, ordinary vent and copy share one RP/cadence
    # dictionary, one action account and one adopted concentration burden.
    m, s = f.class_make('Shaman', shaman=True)
    check('Shaman/paid-own-active-object', s.totems['totem']['paidRP'] == 2 and s.totems['totem']['hp'] == 24 and s._qualifying_aura('owner') == 'totem')
    check('Shaman/same-resource-cadence-action-identities', m.pool is m.cadence is m.action_account is s.actors['owner'])
    f.capture_class(m, 'mend'); f.declare_class(m, 'mend'); resolve(m, 'mend')
    check('CRS03-B/copy-inside-aura-no-vent-consumption', m.pool['rp'] == 29 and m.cadence['dissonance'] == 1 and not s.vent_uses and s.totems['totem']['state'] == 'active')
    s.conditional_extra_action('owner', {'authorityEvent': 'conditional-independent-legal-extra-Action', 'sourceVersion': 'upstream-grant-premise', 'actualLegalGrant': True})
    s.learn('owner', 'fate-coin', 1, 'conditional-actual-native-Fate-Coin-learning')
    s.world['entities']['counter']['hands'] = deepcopy(s.actors['counter']['body']['hands'])
    cast = s.declare('owner', 'fate-coin', 'ordinary-after-copy', {'target': 'counter', 'hand': 'left'})
    s.resolve_fate_coin('ordinary-after-copy')
    check('CRS03-B/ordinary-positive-vent-still-available', cast['quote']['cost'] == 2 and cast['dissonanceAdded'] == 0 and s.vent_uses['owner']['1']['reduction'] == 1 and m.pool['rp'] == 27 and m.cadence['dissonance'] == 1)
    check('Shaman/shared-chronological-history', m.cadence['previousSpell'] == 'fate-coin' and m.cadence['refrain'] == 0)
    record('Shaman/actual-totem-copy-then-ordinary-vent', m, s.snapshot())
    for profile in ['ward', 'hindrance', 'boon']:
        m, s = f.class_make('Shaman', shaman=True); f.capture_class(m, profile); f.declare_class(m, profile)
        check('Shaman/'+profile+'/ends-actual-totem-before-counter', s.totems['totem']['state'] == 'ended' and s.actors['owner']['concentration'] == 'cast' and not s.vent_uses)
        m.resolve('cast', countered=True)
        check('Shaman/'+profile+'/counter-keeps-spend-no-totem-restore', m.pool['rp'] == 29 and s.totems['totem']['state'] == 'ended' and s.actors['owner']['concentration'] is None)
        record('Shaman/totem-counter/'+profile, m, s.snapshot())
    m, s = f.class_make('Shaman', shaman=True); f.capture_class(m, 'mend')
    s.actors['owner']['concentration'] = 'different-ordinary-source'
    reject('Shaman/unintegrated-concentration-change-fails-closed', m, lambda: f.declare_class(m, 'mend'))
    for field, value in [('conscious', False), ('canAct', False), ('silenced', True), ('canSpeak', False)]:
        m, s = f.class_make('Shaman', shaman=True); f.capture_class(m, 'mend')
        s.actors['owner']['body'][field] = value
        reject('Shaman/linked-class-body/'+field, m, lambda: f.declare_class(m, 'mend'))
    m, s = f.class_make('Shaman', shaman=True); f.capture_class(m, 'mend')
    s.actors['owner']['body']['hands']['left']['holding'] = 'actual-held-item'
    reject('Shaman/linked-class-body/no-free-somatic-hand', m, lambda: f.declare_class(m, 'mend'))
    m, s = f.class_make('Shaman', shaman=True); f.capture_class(m, 'mend'); s.actors['owner']['heroPath'] = 'Bloodcaller'
    reject('Shaman/Bloodcaller-keeps-pool-not-ranked-route', m, lambda: f.declare_class(m, 'mend'))
    check('Shaman/Bloodcaller-pool-and-totem-preserved', m.pool['rp'] == 31 and s.totems['totem']['state'] == 'active')
    m, _ = f.class_make('Shaman'); m.captures.acquired.native_state['heroPath'] = 'Bloodcaller'
    gid = 'eldritch_echo/Shaman:4'
    f.capture_class(m, 'strike', grant=gid); cast = f.declare_class(m, 'strike', grant=gid); resolve(m, 'strike')
    check('Shaman/Bloodcaller-independent-paid-CHA-q0', cast['provider']['ability'] == 'CHA' and cast['provider']['maximumLearnableRank'] == 0 and cast['spellAttack'] == 7 and cast['quote']['cost'] == 0)
    record('Shaman/Bloodcaller-retains-independent-feat-only-route', m)

    # Actual old CreatureWorld summon/command transactions, conditional prior
    # class record. Only their shared allowance/payment boundary is certified;
    # class Mirrorbind and class Echo strain/payload are not implemented here.
    def beast(m):
        h = m.captures.acquired
        assert {'mirrorsage.base.echo-release', 'mirrorsage.base.mirror-beast-summon'} <= set(h.base_kit['choices'])
        world = CreatureWorld(); wallet = SharedClassWallet(m.pool); commands = CommandLedger('owner')
        stats = SourceStats('owner', 'mirrorsage', 12, 4, 4, 3, 8, 16)
        world.summon('mirrorsage.base.mirror-beast-summon', ('beast',), stats, 0, ClockMarker(60), wallet,
            use_key='conditional-actual-summon-opportunity', legal=True, ledger=commands)
        m.pool['actions'] = 1  # Explicit next actual owner turn after summon.
        m.echoes.records.add('conditional-prior-class-record')
        return world, wallet, commands, stats
    for first in ['feat', 'class-boundary']:
        m, _ = f.class_make('Mirrorsage'); b, w, commands, stats = beast(m)
        f.capture_class(m, 'mend')
        def class_echo():
            return b.echo_from_beast('beast', stats, 6, 1, 'conditional-prior-class-record', 2, w, commands, m.echoes, own_turn=True, legal=True)
        if first == 'feat':
            f.declare_class(m, 'mend'); resolve(m, 'mend')
            m.pool['actions'] = 1  # Explicit independent legal extra Action premise.
            before = deepcopy((b.__dict__, commands.__dict__, m.echoes.__dict__, m.pool))
            try: class_echo()
            except ValueError: check('Mirror/feat-blocks-existing-class-beast-path', True)
            else: raise AssertionError('Mirror class path bypassed shared cap')
            check('Mirror/blocked-class-path-preserves-record-and-wallet', before == (b.__dict__, commands.__dict__, m.echoes.__dict__, m.pool))
        else:
            class_echo(); m.pool['actions'] = 1
            reject('Mirror/existing-class-beast-path-blocks-feat', m, lambda: f.declare_class(m, 'mend'))
        check('Mirror/canonical-shared-payment-and-cap/'+first, w.rp == m.pool['rp'] == 25 and m.echoes.released_rounds == {1})
        record('Mirror/mutual-cap/'+first, m, {'creatureWorld': b.__dict__, 'commands': commands.__dict__, 'classRecordPremise': 'One independently legal already captured class record; capture/strain/payload not executed by cap test.'})
    m, _ = f.class_make('Mirrorsage'); f.capture_class(m, 'mend', adapt=True)
    f.declare_class(m, 'mend'); resolve(m, 'mend'); next_round(m)
    cast = f.declare_class(m, 'mend', event='adapted', permission='adapted')
    check('CRS03-C/no-class-first-release-waiver', cast['quote']['refrain'] == 1 and cast['quote']['dissonanceAdded'] == 2 and cast['quote']['classHooksApplied'] == [])
    m.resolve('adapted', countered=True)
    check('Mirror/counter-retains-both-caps', m.release_rounds == m.echoes.released_rounds == {1, 2} and not m.echoes.records)
    record('Mirror/repeated-copy-no-class-waiver-countered-cap', m)
    m, _ = f.class_make('Mirrorsage'); f.capture_class(m, 'strike', grant='eldritch_echo/Mirrorsage:4')
    f.declare_class(m, 'strike', grant='eldritch_echo/Mirrorsage:4')
    check('Mirror/CHA-feat-route-still-spends-owned-class-cap', m.echoes.released_rounds == {1})
    m.captures.end_regular('turn1', actual_regular_end=True); m.captures.start_extra('extra', 1, actual_extra_turn=True)
    m.pool.update(turnId='extra', actions=1)
    f.capture_class(m, 'strike', event='capture2', sid='eldritch_echo', grant='eldritch_echo/Mirrorsage:4')
    reject('Mirror/extra-turn-does-not-reset-round-cap', m, lambda: f.declare_class(m, 'strike', event='second', cap='capture2', grant='eldritch_echo/Mirrorsage:4'))
    m, _ = f.class_make('Mirrorsage'); f.capture_class(m, 'mend'); m.echoes.owner = 'other-owner'
    reject('Mirror/cannot-substitute-another-owner-cap', m, lambda: f.declare_class(m, 'mend'))
    m, _ = f.class_make('Mirrorsage'); f.capture_class(m, 'mend'); m.echoes = None
    reject('Mirror/cannot-omit-class-cap', m, lambda: f.declare_class(m, 'mend'))
    check('source-preservation', bindings == [info(p) for p in paths])
    report = {'recordedAtUtc': datetime.now(timezone.utc).isoformat(), 'status': 'pass', 'checks': len(checks),
        'failures': [], 'sourceBindings': bindings, 'results': checks, 'histories': histories,
        'counts': {'histories': len(histories), 'classes': 2, 'profiles': 7},
        'coverage': {'CRS03-B': 'Paid selected own totem, shared RP/cadence/action/concentration, copy no vent, subsequent actual ordinary Fate Coin gets positive vent.',
                     'CRS03-C': 'Actual native INT provider, paid feats, repeated copy Refrain retained, same EchoLedger shared with existing paid Beast-origin class boundary both directions.'},
        'limits': ['Conditional ability rolls, known-spell subset, attained levels, hero path, observed source components and physical/turn/extra-Action predicates are explicit fixtures, not authenticated campaign events.',
            'Ability/repertoire/Base selections and paid ASIs are modeled; full training, class/arch/hero advancement, class Mirrorbind/capture and the class Echo strain/payload remain separate.',
            'Shaman bridge recognizes the existing totem burden and registered copy casts only. Unintegrated ordinary concentration changes fail closed. General suppression, dispel, body-end/save-load and live-engine scheduling remain open.',
            'Mirror tests execute existing summon/command/payment/shared-cap boundaries with an explicit prior-record premise; they do not certify the entire class Echo casting procedure.',
            'Ready/shared-round timing remains COPY-READY-ALLOWANCE-01 pending actual GPT. Price modifiers, full interceptors, wider copy component sources and other previously reported payload limits remain open.',
            'No new GPT response received: Part4 length limit; Part5 creation authorization remains pending. This package is UNSENT until actual delivery is recorded.',
            'These Python reference tests are not shipped-runtime, human playtest, balance, cosmology, whole-feat, whole-game or release approval.'],
        'newRuleAdoptions': 0, 'sourceInformationDeleted': 0, 'runtimeApproved': False,
        'fullFeatExactApproved': False, 'wholeGameComplete': False}
    if write: output.write_text(json.dumps(clean(report), ensure_ascii=False, indent=2)+'\n', encoding='utf8', newline='\n')
    print(json.dumps({'checks': len(checks), 'histories': len(histories), 'sources': len(bindings), 'report': info(output) if write else None}))


if __name__ == '__main__': main()
