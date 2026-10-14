"""Execute GPT's eighteen Flora follow-through groups with paid source fixtures."""
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
import json
from feat335_flora_source_followthrough import FloraSourceFollowthrough
from feat_exact_01_flora_acquisition import FloraAcquisition
from feat_exact_01_initiate_acquisition_model import InitiateAcquisitions
from feat_exact_01_casting_credential_model import CastingSources
from validate_feat_exact_01_composite_casting import read, info, serial

R = Path(__file__).resolve().parents[1]; G = R.parents[1]
A = G / 'docs/audit/2026-10-08/full-game'; V = A / 'feat335-flora-source-check-01-verdict'


def main():
    out = A / 'FEAT335_FLORA_SOURCE_FOLLOWTHROUGH_CHECK.json'
    assert not out.exists()
    paths = [R / 'data/playtest/character_foundation.json', R / 'data/playtest/ancestry_background_candidate.json',
        R / 'data/playtest/equipment_source_catalog.json', R / 'data/public/feat_candidates/exact_01/supplements.json',
        R / 'data/public/feat_candidates/exact_01/spell_dependencies.json', R / 'data/public/class_playtests/wizard.json',
        A / 'FEAT_EXACT_01_ACQUISITION_CONTRACTS.json', A / 'FEAT_EXACT_01_INITIATE_ACQUISITION_CHECK.json',
        R / 'data/director/magic_core_feat_operating_proposal_internal.json',
        V / 'FINITE_FLORA_EXPECTATIONS.json', V / 'FOUR_QUESTION_REGISTER.json', V / 'EXACT_FLORA_CORRECTIONS.json',
        A / 'FEAT335_FLORA_SOURCE_PROPAGATION_CHECK.json', A / 'FEAT335_FLORA_SOURCE_CHECK_01_REPRODUCED.json',
        R / 'data/public/feat_candidates/exact_01/shared_rules.json', Path(__file__),
        *[R / 'tools' / n for n in ['feat335_flora_source_followthrough.py', 'feat335_flora_use.py',
            'feat_exact_01_flora_acquisition.py', 'feat_exact_01_remaining_owned_chains.py',
            'feat_exact_01_casting_selections.py', 'feat_exact_01_composite_casting_model.py',
            'feat_exact_01_initiate_acquisition_model.py', 'feat_exact_01_casting_credential_model.py',
            'feat_exact_01_training_prerequisite_model.py', 'feat_exact_01_acquisition_models.py', 'core_playtest_rules.py']]]
    bindings = [info(p) for p in paths]
    foundation, ancestry, equipment, sm, dependencies, wizard, contracts, prior, core = [read(p) for p in paths[:9]]
    classes = {x['class']: x for x in foundation['classes']}
    skills = {s: a for a, ss in foundation['skillAbilities'].items() for s in ss}
    equipment = {x['id']: x for x in equipment['records']}; backgrounds = {x['id']: x for x in ancestry['backgrounds']}
    supplements = {x['id']: x['value'] for x in sm['groups']}; contracts = {x['id']: x for x in contracts['records']}
    sources = CastingSources(G, dependencies['spells'], supplements, wizard)
    checks = []; histories = []; group = None

    def check(label, ok, detail=None):
        checks.append({'group': group, 'id': label, 'passed': bool(ok), 'detail': deepcopy(detail)})
        assert ok, (group, label)

    def reject(label, m, call, expected=None):
        before = m.snapshot()
        try:
            call()
        except (ValueError, TypeError) as e:
            check(label, expected is None or expected in str(e), str(e))
        else:
            check(label, False)
        check(label + '/unchanged', before == m.snapshot())

    def world():
        return {'evidenceMode': 'conditional_fixture', 'actors': {
            'owner': {'position': 0, 'canAct': True, 'dead': False, 'spokenCommand': True,
                'silenced': False, 'visibleCommand': False, 'perceivesPlants': True,
                'saves': {'DEX': 0, 'CON': 0, 'STR': 0}, 'conditionImmunities': []},
            **{name: {'position': pos, 'saves': {'DEX': 0, 'CON': 0, 'STR': 0},
                      'conditionImmunities': []} for name, pos in [('enemy', 15), ('ally', 20), ('distant', 100)]}},
            'supportedVisibleGround': [5, 10, 20, 25, 30, 35, 75], 'walls': [],
            'areas': {'square-A': {'origin': 15, 'supported': True, 'creatures': ['enemy', 'ally']}}}

    def make(curriculum='Wizard', level=12, trap=True, verdant_only=False):
        actor = deepcopy(prior['actorSourceProjection'])
        actor.update(firstClass='Warrior', classLevels={'Warrior': 1}, selectedClassSkills=['Nature', 'Athletics'])
        h = FloraAcquisition(actor, classes, equipment, skills, ancestry, backgrounds, contracts, supplements, sources)
        h.configure_choice_sources(core)
        paid = InitiateAcquisitions(actor, classes, equipment, skills, ancestry, backgrounds, contracts, supplements['SUP-04'], dependencies['spells'])
        paid.advance(4); paid.earn(4)
        ability, cantrips, rank1 = prior['authoredCurriculumChoices'][curriculum]
        paid.acquire('magicInitiate', 4, {'curriculum': curriculum, 'cantrips': cantrips, 'rank1': rank1})
        h.advance(4); h.pay = paid.pay; h.casting.import_initiate(paid, 4)
        h.advance(8); h.earn(8)
        if verdant_only:
            h.acquire_named('verdant_bond', 8)
        else:
            h.acquire_named('conjure_flora', 8, h.actual_casting_routes()[0])
        if level > 8: h.advance(level)
        if trap:
            assert level >= 12
            h.earn(12); h.acquire_named('trapcasting', 12)
        if verdant_only: return h
        m = FloraSourceFollowthrough(h, world()); m.begin_turn('regular-1', 'round-1', 0)
        return m

    def record(label, m, **extra):
        histories.append({'group': group, 'id': label, 'state': m.snapshot(), 'extra': deepcopy(extra),
                          'evidenceMode': 'conditional_source_qualified_not_campaign_fact'})

    def command(m, mode='lash', participants=None):
        return m.declare_command('command', participants or ['p'], mode,
            **({'area': 'square-A'} if mode == 'entangle' else {'target': 'enemy'}))

    def phase(m, mode='lash', targets=None, event='command', roll=1):
        turn = m.pending[event]['regularTurn']
        if turn not in m.ended_regular_turns:
            m.end_regular_turn(turn, actual_end_processing_complete=True)
        targets = targets or (['enemy', 'ally'] if mode == 'entangle' else ['enemy'])
        return m.resolve_attached(event, actual_phase_turn=turn, rolls={t: roll for t in targets},
                                  die=5 if mode == 'lash' else None, deadlines={t: m.now + 40 for t in targets})

    def remove_provider(m):
        gid = m.bound_route['grantId']
        m.acquired.casting.grants[gid]['removedAt'] = m.acquired.casting.moment
        return gid

    group = 'FLA-01'
    m = make(); remove_provider(m)
    check('removed-route-no-new-casting-prerequisite', not m.acquired.actual_casting_routes() and not m.acquired.prerequisite('verdant_bond'))
    m.create('create', 'p', 'lash', 10, 60, armed=True)
    command(m); result = phase(m)
    check('removed-route-new-creation-and-command', result[0]['nativeDamage'] == 5)
    m.begin_turn('regular-2', 'round-2', 6)
    result = m.burst('burst', 'p', ['owner', 'enemy', 'ally'], {'owner': 20, 'enemy': 1, 'ally': 20}, [3, 4])
    check('removed-route-new-burst', [r['nativeDamage'] for r in result] == [3, 7, 3])
    record('lost-original-provider-continuing-independent-Flora', m)

    group = 'FLA-02'
    m = make(); m.acquired.casting.use_state['rp'] = 0
    for charge in m.acquired.casting.use_state['renewableCharges'].values(): charge['current'] = 0
    m.acquired.casting.use_state['temporaryBlocks'] = ['conditional-spell-only-prohibition']
    m.world['actors']['owner']['silenced'] = True
    m.create('create', 'p', 'lash', 10, 60)
    reject('Silence-blocks-audible-not-creation', m, lambda: command(m), 'receive the command')
    m.world['actors']['owner']['visibleCommand'] = True; command(m)
    check('depleted-temporarily-blocked-visible-command', phase(m)[0]['nativeDamage'] == 5)
    m.begin_turn('regular-2', 'round-2', 6); m.operative = False
    reject('actual-Flora-suppression-controls', m, lambda: m.create('second', 'p2', 'lash', 20, 66, additional=True), 'cannot use')
    check('suppression-alone-not-ending-window', m.second is not None and m.plants['p']['active'])
    m.operative = True; m.create('second', 'p2', 'lash', 20, 66, additional=True)
    record('actual-effect-scope-and-resumption', m)

    group = 'FLA-03'
    for bad in ['missing', 'foreign', 'invalid', 'late']:
        m = make()
        if bad == 'missing': m.initial.pop('fixedCastingRoute')
        elif bad == 'foreign': m.initial['fixedCastingRoute']['grantId'] = 'foreign-owner/provider'
        elif bad == 'invalid': m.initial['fixedCastingRoute']['ability'] = 'Spellcraft'
        else:
            next(g for g in m.acquired.pay.grants if g['identity'] == 'conjure_flora')['choice'] = None
        reject(bad + '-provider-unestablished', m, lambda: FloraSourceFollowthrough(m.acquired, m.world), 'provider/ability binding')
        record(bad + '-original-binding', m)
    for curriculum, ability in [('Dragoon', 'STR'), ('Monk', 'DEX'), ('Thief', 'DEX'), ('Wizard', 'INT'), ('Cleric', 'WIS'), ('Bard', 'CHA')]:
        m = make(curriculum); remove_provider(m); m.create('create', 'p', 'lash', 10, 60)
        command(m); results = phase(m)
        check(curriculum + '-retains-actual-ability', m.bound_route['ability'] == ability and results[0]['dc'] == m.dc())
        record('actual-paid-provider/' + curriculum, m)

    group = 'FLA-04'
    m = make(trap=False); m.acquired.pay.scores['INT'] = 16; m.acquired.pay.scores['CHA'] = 20
    m.create('create', 'p', 'lash', 10, 60); command(m); original = phase(m); remove_provider(m)
    actor = deepcopy(prior['actorSourceProjection']); actor.update(firstClass='Warrior', classLevels={'Warrior': 1}, selectedClassSkills=['Nature', 'Athletics'])
    second = InitiateAcquisitions(actor, classes, equipment, skills, ancestry, backgrounds, contracts, supplements['SUP-04'], dependencies['spells'])
    second.pay = m.acquired.pay; second.advance(12); second.earn(12)
    _, cantrips, rank1 = prior['authoredCurriculumChoices']['Bard']
    second.acquire('magic_initiate_bard', 12, {'curriculum': 'Bard', 'cantrips': cantrips, 'rank1': rank1})
    m.acquired.casting.import_initiate(second, 12)
    check('new-actual-CHA-provider-no-reselection', m.acquired.actual_casting_routes()[0]['ability'] == 'CHA' and m.dc() == 15)
    m.acquired.pay.scores['INT'] = 18
    m.begin_turn('regular-2', 'round-2', 6); m.declare_command('later', ['p'], 'lash', target='enemy')
    later = phase(m, event='later')
    check('live-bound-score-later-only', original[0]['dc'] == 15 and later[0]['dc'] == 16 and m.plants['p']['maximumHP'] == 9)
    record('separately-paid-other-provider-and-current-bound-ability', m, original=original, later=later)

    group = 'FLA-05'
    for ending in ['damage', 'uproot', 'burst', 'other-actual-ending']:
        m = make(); m.create('create', 'p', 'spore', 10, 60, armed=True); command(m, 'spore'); phase(m, 'spore')
        check(ending + '/generator-condition-present', len(m.conditions) == 1)
        m.begin_turn('regular-2', 'round-2', 18)
        if ending == 'damage': m.damage('p', 99)
        elif ending == 'uproot': m.uproot('p')
        elif ending == 'burst': m.burst('burst', 'p', ['owner', 'enemy', 'ally'], {t: 1 for t in ['owner', 'enemy', 'ally']}, [3, 4])
        else: m.end('p', 'conditional-actual-ending-effect')
        check(ending + '/immediate-permanent-window-close', m.second is None and m.consumed_second == {'create'} and not m.conditions and m.window_closures[-1]['closedAt'] == 18)
        m.begin_turn('regular-3', 'round-3', 24)
        reject(ending + '/otherwise-valid-Action-no-second', m, lambda: m.create('second', 'p2', 'lash', 20, 84, additional=True), 'entitlement')
        check(ending + '/paid-use-retained', m.initial['creationUses']['current'] == 0)
        record('first-end/' + ending, m)

    group = 'FLA-06'
    m = make(); m.create('first', 'p', 'lash', 10, 60); m.begin_turn('regular-2', 'round-2', 6)
    m.create('second', 'p2', 'lash', 20, 66, additional=True); m.advance(18); m.uproot('p')
    check('second-independent-deadline', m.plants['p2']['active'] and m.plants['p2']['deadline'] == 66 and not m.second)
    m.begin_turn('regular-3', 'round-3', 24); m.damage('p2', 99)
    reject('free-capacity-and-Action-cannot-replace-spent-second', m, lambda: m.create('third', 'p3', 'lash', 25, 84, additional=True), 'entitlement')
    record('independent-second-and-isolated-third-rejection', m)

    group = 'FLA-07'
    m = make(level=8, trap=False); m.create('first', 'p', 'lash', 10, 60)
    check('below10-original-window-recorded', m.second == {'use': 'first', 'first': 'p', 'deadline': 60})
    m.advance(6); m.acquired.advance(10)
    check('growth-capacity-no-charge-no-heal', m.initial['plantCapacity'] == 2 and m.initial['creationUses']['current'] == 0 and m.plants['p']['hp'] == m.plants['p']['maximumHP'] == 8)
    m.begin_turn('regular-2', 'round-2', 12); m.create('second', 'p2', 'lash', 20, 72, additional=True)
    check('live10-second-paid-own-snapshot', m.actions == 0 and m.plants['p2']['maximumHP'] == 9 and m.plants['p2']['deadline'] == 72 and m.plants['p']['maximumHP'] == 8 and m.second is None)
    m.advance(60); check('original-expiry-does-not-end-second', not m.plants['p']['active'] and m.plants['p2']['active'])
    m.advance(72); check('second-expires-own-minute', not m.plants['p2']['active'])
    record('live-level10-completion-not-old-fixed-snapshot', m)

    group = 'FLA-08'
    for closed in ['deadline', 'first-ended']:
        m = make(level=8, trap=False); m.create('first', 'p', 'lash', 10, 60)
        if closed == 'first-ended': m.advance(5); m.uproot('p')
        m.advance(60); m.acquired.advance(10); m.begin_turn('renamed-scene-turn', 'new-round', 61, actions=2)
        reject(closed + '/growth-cannot-reopen', m, lambda: m.create('new-identity', 'new-body', 'lash', 20, 121, additional=True), 'entitlement')
        check(closed + '/original-paid-history', m.initial['creationUses']['current'] == 0 and m.consumed_second == {'first'})
        record('late-growth/' + closed, m)
    m = make(); m.create('first', 'p', 'lash', 10, 60); m.begin_turn('regular-2', 'round-2', 6)
    m.create('second', 'p2', 'lash', 20, 66, additional=True); m.uproot('p2'); m.acquired.advance(16)
    m.begin_turn('extra-Action', 'round-3', 12, actions=2)
    reject('spent-with-free-capacity-growth-no-reopen', m, lambda: m.create('third', 'p3', 'lash', 25, 72, additional=True), 'entitlement')
    record('spent-window-no-growth-replay', m)

    group = 'FLA-09'
    for death in [False, True]:
        m = make(); m.create('create', 'p', 'lash', 10, 60); m.begin_turn('regular-2', 'round-2', 6)
        command(m); check(str(death) + '/commit-leaves-owner-Action', m.actions == 1 and m.bonus_actions == 0 and m.offense == {'round-2'})
        m.world['actors']['owner'].update(canAct=False, dead=death)
        reject(str(death) + '/incapable-new-creation', m, lambda: m.create('second', 'p2', 'lash', 20, 66, additional=True), 'cannot use')
        result = phase(m)
        check(str(death) + '/original-phase-after-incapacity', result[0]['nativeDamage'] == 5 and m.plants['p']['active'] and m.plants['p']['owner'] == 'owner')
        reject(str(death) + '/no-phase-replay', m, lambda: m.resolve_attached('command', actual_phase_turn='regular-2'), 'original pending')
        m.begin_turn('regular-3', 'round-3', 12)
        reject(str(death) + '/incapable-new-command', m, lambda: m.declare_command('new', ['p'], 'lash', target='enemy'), 'cannot use')
        reject(str(death) + '/incapable-new-Burst', m, lambda: m.burst('burst', 'p', ['owner', 'enemy', 'ally'], {t: 1 for t in ['owner', 'enemy', 'ally']}, [3, 4]), 'cannot use')
        record('received-command-then-' + ('death' if death else 'incapacity'), m)

    group = 'FLA-10'
    for loss in ['silence', 'sight-channel', 'separation', 'deafened']:
        m = make(); m.create('create', 'p', 'lash', 10, 60)
        if loss == 'sight-channel': m.world['actors']['owner'].update(spokenCommand=False, visibleCommand=True)
        command(m)
        if loss == 'silence': m.world['actors']['owner']['silenced'] = True
        elif loss == 'sight-channel': m.world['walls'] = [5]
        elif loss == 'separation': m.world['actors']['owner']['position'] = 100
        else: m.plants['p']['deafened'] = True
        check(loss + '/received-command-persists', phase(m)[0]['nativeDamage'] == 5)
        m.begin_turn('regular-2', 'round-2', 6)
        reject(loss + '/new-command-still-needs-channel', m, lambda: m.declare_command('new', ['p'], 'lash', target='enemy'), 'receive the command')
        record('channel-loss-after-receipt/' + loss, m)

    group = 'FLA-11'
    for invalid in ['no-channel', 'owner-incapable']:
        m = make(); m.create('create', 'p', 'lash', 10, 60)
        if invalid == 'no-channel': m.world['actors']['owner']['silenced'] = True
        else: m.world['actors']['owner']['canAct'] = False
        reject(invalid + '/precommit-no-spend', m, lambda: command(m))
        check(invalid + '/no-pending-no-offense', not m.pending and not m.offense and m.bonus_actions == 1)
        record('precommit-rejection/' + invalid, m)
    for invalid in ['destroyed', 'plant-incapable', 'plant-suppressed', 'expired', 'target-range', 'target-LoE', 'plant-perception', 'express-cancel']:
        m = make(); m.create('create', 'p', 'lash', 10, 60); command(m)
        if invalid == 'destroyed': m.damage('p', 99)
        elif invalid == 'plant-incapable': m.plants['p']['canAct'] = False
        elif invalid == 'plant-suppressed': m.plants['p']['suppressed'] = True
        elif invalid == 'expired': m.advance(60)
        elif invalid == 'target-range': m.world['actors']['enemy']['position'] = 100
        elif invalid == 'target-LoE': m.world['walls'] = [12]
        elif invalid == 'plant-perception': m.plants['p']['perceivesTargets'] = False
        else: m.cancel_command('command', actual_cancelling_effect=True)
        if invalid != 'express-cancel': check(invalid + '/fizzles', phase(m) == [])
        check(invalid + '/paid-close-without-refund', not m.pending and m.offense == {'round-1'} and m.bonus_actions == 0 and m.initial['creationUses']['current'] == 0)
        reject(invalid + '/no-retarget-or-later-resolve', m, lambda: m.resolve_attached('command', actual_phase_turn='regular-1'), 'original pending')
        record('postcommit-outcome-lost/' + invalid, m)

    group = 'FLA-12'
    m = make(); m.create('first', 'p', 'spore', 10, 60); m.begin_turn('regular-2', 'round-2', 6)
    m.create('second', 'p2', 'entangle', 20, 66, additional=True); command(m, participants=['p', 'p2']); m.uproot('p')
    check('surviving-originally-nominated-Lash-origin', phase(m)[0]['nativeDamage'] == 5)
    record('nominated-Lash-fallback-same-target', m)
    for mode in ['spore', 'entangle']:
        m = make(); m.create('first', 'p', mode, 10, 60); m.begin_turn('regular-2', 'round-2', 6)
        m.create('second', 'p2', mode, 20, 66, additional=True); command(m, mode); m.uproot('p')
        check(mode + '/no-unnominated-fallback', phase(m, mode) == [] and m.plants['p2']['active'])
        record('fixed-origin-loss/' + mode, m)
    m = make(); m.create('create', 'p', 'entangle', 10, 60); command(m, 'entangle')
    m.world['actors']['distant']['position'] = 15
    m.world['areas']['square-A']['creatures'] = ['ally', 'distant']
    result = phase(m, 'entangle', targets=['ally', 'distant'])
    check('fixed-area-actual-phase-occupants-including-ally', {r['target'] for r in result} == {'ally', 'distant'} and all(r['condition']['kind'] == 'Restrained' for r in result))
    record('area-current-occupants', m)

    group = 'FLA-13'
    m = make(); m.create('create', 'p', 'lash', 10, 60, armed=True); command(m)
    m.world['actors']['enemy']['position'] = 10
    check('pending-command-already-spent-entry-budget', m.enter('entry', 'p', 'enemy', 1, from_outside=True, meaningful_hostile=True, die=6) == [])
    check('phase-no-second-spend-even-save', phase(m, roll=20)[0]['nativeDamage'] == 2 and m.offense == {'round-1'})
    record('command-before-entry', m)
    m = make(); m.create('create', 'p', 'lash', 10, 60, armed=True); m.world['actors']['enemy']['position'] = 10
    check('entry-save-spends-offense', m.enter('entry', 'p', 'enemy', 20, from_outside=True, meaningful_hostile=True, die=6)[0]['nativeDamage'] == 0)
    reject('entry-before-command-blocks', m, lambda: command(m), 'offense unavailable')
    record('entry-before-command', m)

    group = 'FLA-14'
    m = make(); m.create('create', 'p', 'lash', 10, 60, armed=True)
    m.world['actors']['owner'].update(canAct=False, dead=True); m.world['actors']['enemy']['position'] = 10
    first = m.enter('entry', 'p', 'enemy', 1, from_outside=True, meaningful_hostile=True, die=6)
    check('dead-owner-existing-trap', first[0]['nativeDamage'] == 6 and m.plants['p']['owner'] == 'owner')
    m.begin_turn('extra-turn', 'round-1', 1, regular=False)
    check('extra-turn-no-entry-refresh', m.enter('repeat', 'p', 'enemy', 1, from_outside=True, meaningful_hostile=True, die=6) == [])
    m.world['actors']['owner'].update(canAct=True, dead=False)
    check('recovery-no-shared-round-refresh', m.offense == {'round-1'} and m.enter('recovered-entry', 'p', 'enemy', 1, from_outside=True, meaningful_hostile=True, die=6) == [])
    m.world['actors']['owner'].update(canAct=False, dead=True)
    m.begin_turn('external-round-marker', 'round-2', 6, regular=False, actions=0, bonus_actions=0)
    check('later-actual-round-new-entry', m.enter('later-entry', 'p', 'enemy', 1, from_outside=True, meaningful_hostile=True, die=6)[0]['nativeDamage'] == 6)
    m.begin_turn('external-round-marker-3', 'round-3', 12, regular=False, actions=0, bonus_actions=0)
    m.offense.add('round-3')  # Conditional actual prior offense by another companion of this same owner.
    check('other-companion-shares-original-owner-cap', m.enter('other-companion-round', 'p', 'enemy', 1, from_outside=True, meaningful_hostile=True, die=6) == [])
    record('same-owner-death-recovery-and-global-round-history', m)

    group = 'FLA-15'
    m = make(); m.create('create', 'p', 'lash', 10, 60); command(m)
    reject('not-before-owner-end-processing', m, lambda: m.resolve_attached('command', actual_phase_turn='regular-1'), 'original pending')
    m.begin_turn('authorized-extra', 'round-1', 1, regular=False)
    reject('extra-turn-not-original-phase', m, lambda: m.resolve_attached('command', actual_phase_turn='authorized-extra'), 'original pending')
    check('extra-turn-did-not-advance-or-duplicate', 'command' in m.pending and not m.closed_phases)
    m.end_regular_turn('regular-1', actual_end_processing_complete=True)
    m.miss_attached('command', actual_phase_turn='regular-1', actual_missed_phase=True)
    m.begin_turn('recovery-turn', 'round-2', 6)
    reject('missed-phase-no-recovery-backlog', m, lambda: m.resolve_attached('command', actual_phase_turn='regular-1'), 'original pending')
    record('explicit-missed-original-phase', m)
    m = make(); m.create('create', 'p', 'lash', 10, 60)
    m.world['actors']['owner']['canAct'] = False; m.end_regular_turn('regular-1', actual_end_processing_complete=True)
    reject('never-issued-no-autonomous-phase', m, lambda: m.resolve_attached('phantom', actual_phase_turn='regular-1'), 'original pending')
    m.world['actors']['owner']['canAct'] = True
    m.begin_turn('isolated-extra', 'round-2', 6, regular=False)
    check('isolated-extra-other-guards-valid', m.bonus_actions == 1 and 'round-2' not in m.offense and m.channel(m.plants['p']) and m.plants['p']['active'])
    reject('extra-turn-alone-disallows-command', m, lambda: command(m), 'unfinished owner regular turn')
    record('never-issued-and-isolated-extra-turn', m)

    group = 'FLA-16'
    m = make(); m.create('create', 'p', 'spore', 10, 60, armed=True)
    result = m.burst('burst', 'p', ['owner', 'enemy', 'ally'], {'owner': 20, 'enemy': 1, 'ally': 20}, [3, 4])
    check('body-consumption-does-not-cancel-bound-Burst', result[1]['nativeDamage'] == 7 and result[1]['damageType'] == 'poison' and not m.plants['p']['active'] and not m.second and m.history[-1]['plantEndedBeforePayload'])
    m.begin_turn('regular-2', 'round-2', 6)
    check('dead-body-negative-other-guards-valid', m.bonus_actions == 1 and m.world['actors']['owner']['canAct'] and 'round-2' not in m.offense)
    reject('ended-body-no-second-Burst', m, lambda: m.burst('burst-again', 'p', ['owner', 'enemy', 'ally'], {t: 1 for t in ['owner', 'enemy', 'ally']}, [3, 4]), 'active plant')
    reject('ended-body-no-command', m, lambda: command(m), 'active plant')
    record('bound-Burst-and-isolated-ended-body-rejections', m)

    group = 'FLA-17'
    m = make(); m.acquired.pay.scores['INT'] = 18
    m.create('create', 'p', 'lash', 10, 60, armed=True); m.world['actors']['enemy']['position'] = 10
    m.world['actors']['owner'].update(canAct=False, dead=True)
    first = m.enter('entry-before-expiry', 'p', 'enemy', 15, from_outside=True, meaningful_hostile=True, die=6)
    m.begin_turn('actual-round-2-marker', 'round-2', 6, regular=False, actions=0, bonus_actions=0)
    m.acquired.pay.scores['INT'] = 16  # Explicit conditional due expiry of the existing +2 source; not death itself.
    later = m.enter('entry-after-expiry', 'p', 'enemy', 15, from_outside=True, meaningful_hostile=True, die=6)
    check('continuing-dead-owner-stat-expiry', first[0]['dc'] == 16 and first[0]['nativeDamage'] == 6 and later[0]['dc'] == 15 and later[0]['nativeDamage'] == 0)
    check('no-death-body-heal-reset-or-new-owner', m.plants['p']['maximumHP'] == 9 and m.plants['p']['deadline'] == 60 and m.plants['p']['owner'] == 'owner' and m.initial['creationUses']['current'] == 0)
    m.acquired.pay.scores.pop('INT')
    reject('missing-continuing-operand-not-zero-default', m, lambda: m.dc(), 'operand required')
    record('lawful-timed-stat-expiry-after-death', m, beforeExpiry=first, afterExpiry=later, timedModifier={'ability': 'INT', 'before': 18, 'after': 16, 'actualExpiryTime': 6, 'evidenceMode': 'conditional_source_defined_expiry'})

    group = 'FLA-18'
    h = make(verdant_only=True)
    check('paid-Verdant-and-Trapcasting-alone-no-Flora-initialization', h.pay.has('verdant_bond') and h.pay.has('trapcasting') and 'conjure_flora' not in h.initializations)
    try: FloraSourceFollowthrough(h, world())
    except ValueError as e: check('Verdant-only-cannot-invent-body-engine', 'paid Flora acquisition' in str(e))
    else: check('Verdant-only-cannot-invent-body-engine', False)
    histories.append({'group': group, 'id': 'paid-Verdant-only', 'state': h.snapshot()})
    for curriculum in ['Druid', 'Ranger', 'Shaman']:
        m = make(curriculum, trap=False)
        m.acquired.earn(12); m.acquired.acquire_named('verdant_bond', 12)
        route = m.acquired.casting.qualifying()[0]; dc = m.dc()
        check(curriculum + '/no-active-Flora-no-spell-bonus', m.verdant_spell_bonus(route, actual_legal_cast=True) == 0)
        m.create('create', 'p', 'lash', 10, 60)
        check(curriculum + '/actual-owned-nature-route-predicate', m.verdant_spell_bonus(route, actual_legal_cast=True) == 1)
        check(curriculum + '/copied-or-not-actual-cast-ineligible', m.verdant_spell_bonus(route, actual_legal_cast=True, copied=True) == m.verdant_spell_bonus(route, actual_legal_cast=False) == 0)
        command(m); result = phase(m)
        check(curriculum + '/nonspell-Flora-DC-no-Verdant-addition', result[0]['dc'] == dc)
        m.uproot('p')
        check(curriculum + '/ended-body-no-spell-bonus', m.verdant_spell_bonus(route, actual_legal_cast=True) == 0)
        record('Verdant-source-predicate/' + curriculum, m)
    m = make(trap=False); m.acquired.earn(12); m.acquired.acquire_named('verdant_bond', 12); m.create('create', 'p', 'lash', 10, 60)
    check('actual-Wizard-route-not-nature-by-label', m.verdant_spell_bonus(m.acquired.casting.qualifying()[0], actual_legal_cast=True) == 0)
    record('non-nature-actual-provider', m)

    expected = {x['id'] for x in read(V / 'FINITE_FLORA_EXPECTATIONS.json')['groups']}
    group = 'binding-and-scope'
    check('all-eighteen-received-groups-executed', {h['group'] for h in histories} == expected)
    check('all-sources-stable', bindings == [info(p) for p in paths])
    result = {'recordedAtUtc': datetime.now(timezone.utc).isoformat(), 'status': 'pass',
        'checks': len(checks), 'failures': [], 'sourceBindings': bindings, 'results': checks, 'histories': histories,
        'counts': {'receivedAcceptanceGroups': len(expected), 'conditionalHistories': len(histories), 'sourceModes': 3, 'actualProviderAbilities': 5, 'actualProviderCurricula': 6},
        'fullReceivedExpectations': read(V / 'FINITE_FLORA_EXPECTATIONS.json'),
        'scope': 'Finite FLQ01–04 completion: paid provider retention, live second window and ending, separate command commitment/original phase, owner continuity, and directly coupled trap/Burst/Verdant source predicates.',
        'limits': ['Actual clock/phase authority, ground, senses, body/target positions, effect suppression, legal spell cast and due timed modifier expiry are conditional premises; this is not a general campaign scheduler or event authenticator.',
            'Native damage is before ordinary defenses and full HP/Wound integration. Full condition action restrictions, movement, armed-mode identification, Verdant message/speech, full Nature casting/Weave and all335 use gates remain separate.',
            'Verdant tests execute its finite bonus predicate against paid actual route records, not full spell casts. Original114 report is preserved; its obsolete fixed-at-creation level interpretation is superseded, and its compound negatives are not upgraded retroactively.',
            'No whole-game approval, human playtesting, balance approval, automatic runtime implementation, push or cosmology review follows.'],
        'fullFeatExactApproved': False, 'runtimeApproved': False, 'humanBalanceApproved': False, 'cosmologyReviewed': False}
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2, default=serial) + '\n', encoding='utf-8')
    print(json.dumps({'checks': len(checks), 'counts': result['counts'], 'report': info(out)}))


if __name__ == '__main__': main()
