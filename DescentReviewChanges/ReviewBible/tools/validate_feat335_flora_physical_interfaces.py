"""Execute GPT's eighteen Flora follow-through groups with paid source fixtures."""
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
import json
from feat335_flora_source_followthrough_v2 import FloraSourceFollowthrough
from feat335_flora_physical_interfaces import FloraPhysicalInterfaces
from feat_exact_01_flora_acquisition import FloraAcquisition
from feat_exact_01_initiate_acquisition_model import InitiateAcquisitions
from feat_exact_01_casting_credential_model import CastingSources
from validate_feat_exact_01_composite_casting import read, info, serial

R = Path(__file__).resolve().parents[1]; G = R.parents[1]
A = G / 'docs/audit/2026-10-08/full-game'; V = A / 'feat335-flora-source-check-01-verdict'


def main():
    out = A / 'FEAT335_FLORA_PHYSICAL_INTERFACES_CHECK.json'
    assert not out.exists()
    paths = [R / 'data/playtest/character_foundation.json', R / 'data/playtest/ancestry_background_candidate.json',
        R / 'data/playtest/equipment_source_catalog.json', R / 'data/public/feat_candidates/exact_01/supplements.json',
        R / 'data/public/feat_candidates/exact_01/spell_dependencies.json', R / 'data/public/class_playtests/wizard.json',
        A / 'FEAT_EXACT_01_ACQUISITION_CONTRACTS.json', A / 'FEAT_EXACT_01_INITIATE_ACQUISITION_CHECK.json',
        R / 'data/director/magic_core_feat_operating_proposal_internal.json',
        V / 'FINITE_FLORA_EXPECTATIONS.json', V / 'FOUR_QUESTION_REGISTER.json', V / 'EXACT_FLORA_CORRECTIONS.json',
        A / 'FEAT335_FLORA_SOURCE_PROPAGATION_CHECK.json', A / 'FEAT335_FLORA_SOURCE_CHECK_01_REPRODUCED.json',
        R / 'data/public/feat_candidates/exact_01/shared_rules.json', R / 'docs/mechanics/COMBAT_ACTION_PLAYTEST.md', R / 'docs/mechanics/CORE_RESOLUTION_PLAYTEST.md', Path(__file__),
        *[R / 'tools' / n for n in ['feat335_flora_physical_interfaces.py', 'combat_playtest_rules.py', 'feat335_flora_source_followthrough_v2.py', 'feat335_flora_source_followthrough.py', 'feat335_flora_use.py',
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

    def physical(*, plant=False, mode='lash', armed=False, verdant=True):
        f = make()
        if verdant:
            f.acquired.advance(16); f.acquired.earn(16); f.acquired.acquire_named('verdant_bond', 16)
        if plant:
            f.create('create', 'p', mode, 10, 60, armed=armed)
            f.begin_turn('regular-2', 'round-2', 6)
        inspector = make(level=8, trap=False).acquired
        return FloraPhysicalInterfaces(f, {'observer': {'acquired': inspector, 'canAct': True,
            'actions': 1, 'usableHeldThievesTools': ['tools.thieves-tools']}})

    group = 'Verdant-Nature-task'
    for label, wilderness, other, disadvantage, faces, kept in [
            ('wilderness-no-Flora', True, False, False, [2, 18], 18),
            ('nonwilderness-no-advantage', False, False, False, [10], 10),
            ('disadvantage-cancels-Verdant', True, False, True, [10], 10),
            ('multiple-advantage-does-not-stack', True, True, False, [2, 18], 18),
            ('other-advantage-cancels-disadvantage', True, True, True, [10], 10),
            ('no-advantage-disadvantage-lower', False, False, True, [2, 18], 2)]:
        m = physical(); before = deepcopy(m.flora.acquired.training_projection)
        declared = m.declare_nature('nature', actual_wilderness=wilderness, actual_work_and_senses=True,
            dc=20, other_advantage=other, disadvantage=disadvantage)
        check(label + '/actual-Action-paid-before-roll', m.flora.actions == 0 and 'result' not in m.events['nature'])
        check(label + '/no-plant-prerequisite', not m.flora.plants and declared['verdantAdvantage'] == wilderness)
        result = m.resolve('nature', faces)
        check(label + '/actual-Core-kept-die', result['keptNatural'] == kept and result['total'] == kept + declared['modifier'])
        check(label + '/no-training-or-resource-grant', m.flora.acquired.training_projection == before and m.flora.initial['creationUses']['current'] == 1)
        reject(label + '/no-repeat-outcome', m, lambda: m.resolve('nature', faces), 'pending paid task')
        record(label, m)
    m = physical(); m.flora.acquired.pay.suppress('verdant_bond')
    declared = m.declare_nature('suppressed', actual_wilderness=True, actual_work_and_senses=True, dc=20)
    check('suppressed-Verdant-retains-ordinary-Nature-only', not declared['verdantAdvantage'] and declared['rollMode'] == 'normal')
    m.resolve('suppressed', [10]); record('suppressed-feat-normal-task', m)
    m = physical()
    reject('actual-work-and-senses-still-required', m, lambda: m.declare_nature('invalid', actual_wilderness=True, actual_work_and_senses=False, dc=20), 'ordinary work/senses')
    m.declare_nature('paid', actual_wilderness=True, actual_work_and_senses=True, dc=20)
    reject('wrong-number-of-dice-retains-commitment', m, lambda: m.resolve('paid', [20]), 'kept-die')
    m.interrupt('paid', actual_authorized_interruption=True)
    check('interrupted-Nature-no-Action-refund', m.flora.actions == 0 and not m.pending)
    record('work-input-and-interruption-boundaries', m)

    group = 'Verdant-actual-movement'
    rows = [
        ('sole-nonmagical-plants', 'difficult', ['nonmagical-plants'], True, 10),
        ('mixed-stones', 'difficult', ['nonmagical-plants', 'loose-stones'], False, 20),
        ('magical-plants', 'difficult', ['magical-plants'], False, 20),
        ('other-difficult', 'difficult', ['mud'], False, 20),
        ('occupied-nonhostile-space', 'difficult', ['nonmagical-plants', 'nonhostile-occupied-space'], False, 20),
        ('severe-plant-terrain-not-difficult', 'severe', ['nonmagical-plants'], False, 30),
        ('ordinary-terrain', 'normal', ['ordinary-ground'], False, 10)]
    for label, terrain, causes, discounted, expected in rows:
        m = physical(plant=True)
        result = m.move_owner('move', 10, actual_endpoint=10, terrain=terrain, causes=causes,
            current_speed=30, actual_legal_route=True, actual_hazards=['independent-thorns-hazard'])
        check(label + '/exact-current-cost', result['cost'] == expected and result['verdantDiscount'] == discounted)
        check(label + '/real-budget-and-endpoint', m.movement.spent == expected and m.flora.position('owner') == 10 and result['remainingMovement'] == 30 - expected)
        check(label + '/hazard-not-negated', result['hazardsStillRequireOrdinaryResolution'] == ['independent-thorns-hazard'] and not result['hazardsNegated'])
        reject(label + '/no-route-replay', m, lambda: m.move_owner('move', 10, actual_endpoint=20, terrain=terrain, causes=causes, current_speed=30, actual_legal_route=True), 'cannot be replayed')
        record(label, m)
    for label, crawling, squeezing, expected in [('crawl', True, False, 20), ('squeeze', False, True, 20), ('crawl-and-squeeze', True, True, 30)]:
        m = physical(plant=True)
        result = m.move_owner('move', 10, actual_endpoint=10, terrain='difficult', causes=['nonmagical-plants'],
            current_speed=30, actual_legal_route=True, crawling=crawling, squeezing=squeezing)
        check(label + '/retains-post-terrain-costs', result['cost'] == expected and result['verdantDiscount'])
        record(label, m)
    for absent in ['no-plant', 'ended-plant', 'suppressed-plant', 'no-Verdant']:
        m = physical(plant=absent != 'no-plant', verdant=absent != 'no-Verdant')
        if absent == 'ended-plant': m.flora.uproot('p')
        if absent == 'suppressed-plant': m.flora.plants['p']['suppressed'] = True
        result = m.move_owner('move', 10, actual_endpoint=10, terrain='difficult', causes=['nonmagical-plants'], current_speed=30, actual_legal_route=True)
        check(absent + '/ordinary-terrain-cost', result['cost'] == 20 and not result['verdantDiscount'])
        record(absent, m)
    m = physical(plant=True); m.flora.plants['p']['canAct'] = False
    check('incapable-but-active-plant-still-supports-movement', m.move_owner('move', 10, actual_endpoint=10, terrain='difficult', causes=['nonmagical-plants'], current_speed=30, actual_legal_route=True)['cost'] == 10)
    m.flora.uproot('p')
    result = m.move_owner('later-segment', 10, actual_endpoint=20, terrain='difficult', causes=['nonmagical-plants'], current_speed=30, actual_legal_route=True)
    check('mid-route-ending-next-segment-ordinary-no-refund', result['cost'] == 20 and result['spentTotal'] == 30 and result['remainingMovement'] == 0)
    reject('no-movement-refill-on-new-segment', m, lambda: m.move_owner('over-budget', 5, actual_endpoint=25, terrain='normal', causes=['ground'], current_speed=30, actual_legal_route=True), 'Insufficient movement')
    record('live-benefit-and-conserved-movement-budget', m)
    m = physical(plant=True)
    for label, speed, legal, endpoint in [('zero-Speed', 0, True, 10), ('illegal-route', 30, False, 10), ('fabricated-distance', 30, True, 20)]:
        reject(label, m, lambda speed=speed,legal=legal,endpoint=endpoint:m.move_owner('invalid', 10, actual_endpoint=endpoint, terrain='difficult', causes=['nonmagical-plants'], current_speed=speed, actual_legal_route=legal))
    record('movement-ordinary-prerequisites', m)

    group = 'Flora-identify-and-disarm'
    for mode in ['lash', 'spore', 'entangle']:
        for natural, success in [(1, False), (20, True)]:
            m = physical(plant=True, mode=mode, armed=True)
            declared = m.declare_identify('identify', 'observer', 'p', actual_legal_inspection=True)
            check(mode + str(natural) + '/Action-paid-no-free-identification', m.inspectors['observer']['actions'] == 0 and not m.knowledge and 'result' not in m.events['identify'])
            check(mode + str(natural) + '/INT-Investigation-not-provider-or-defaultPB', declared['modifier'] == 3 and declared['dc'] == m.flora.dc())
            result = m.resolve('identify', [natural])
            check(mode + str(natural) + '/mode-only-on-task-success', result['success'] == success and result['identifiedMode'] == (mode if success else None))
            check(mode + str(natural) + '/inspection-no-disarm-or-offense', m.flora.plants['p']['armed'] and m.flora.plants['p']['active'] and not m.flora.offense)
            reject(mode + str(natural) + '/no-second-unpaid-inspection', m, lambda: m.declare_identify('again', 'observer', 'p', actual_legal_inspection=True), 'unspent Action')
            record('identify/' + mode + '/' + str(natural), m)
    for natural, success in [(1, False), (20, True)]:
        m = physical(plant=True, mode='spore', armed=True); body = deepcopy(m.flora.plants['p'])
        declared = m.declare_disarm('disarm', 'observer', 'p', actual_tool='tools.thieves-tools', actual_in_reach=True)
        check('disarm' + str(natural) + '/own-DEX-no-invented-tool-proficiency', declared['modifier'] == 3 and m.inspectors['observer']['actions'] == 0)
        result = m.resolve('disarm', [natural])
        check('disarm' + str(natural) + '/task-result-and-no-explosion', result['disarmed'] == success and not result['automaticExplosion'] and m.flora.plants['p']['armed'] == (not success) and not m.flora.offense)
        check('disarm' + str(natural) + '/body-HP-mode-deadline-unchanged', all(m.flora.plants['p'][k] == body[k] for k in ['active','hp','maximumHP','mode','deadline','position','owner']))
        record('disarm/' + str(natural), m)
    m = physical(plant=True, armed=True)
    reject('inspection-not-perception-scan', m, lambda:m.declare_identify('bad', 'observer', 'p', actual_legal_inspection=False), 'legal inspection')
    reject('disarm-no-phantom-tools', m, lambda:m.declare_disarm('bad', 'observer', 'p', actual_tool='invented-tool', actual_in_reach=True), 'usable held thieves tools')
    reject('disarm-real-reach', m, lambda:m.declare_disarm('bad', 'observer', 'p', actual_tool='tools.thieves-tools', actual_in_reach=False), 'accessible armed plant')
    m.declare_identify('paid', 'observer', 'p', actual_legal_inspection=True); m.flora.uproot('p')
    check('body-ended-during-paid-inspection-no-refund-no-knowledge', m.resolve('paid', [20]) is None and m.inspectors['observer']['actions'] == 0 and not m.knowledge and m.events['paid']['status'] == 'interrupted-no-refund')
    record('actual-inspection-tools-reach-and-ending', m)
    m = physical(plant=True, armed=False)
    reject('unarmed-plant-not-armed-mode-task', m, lambda:m.declare_identify('bad', 'observer', 'p', actual_legal_inspection=True), 'visible armed Flora')
    reject('unarmed-plant-not-disarm-target', m, lambda:m.declare_disarm('bad', 'observer', 'p', actual_tool='tools.thieves-tools', actual_in_reach=True), 'accessible armed plant')
    record('actually-armed-target-required', m)

    group = 'source-and-scope'
    check('all-current-inputs-stable', bindings == [info(p) for p in paths])
    result = {'recordedAtUtc': datetime.now(timezone.utc).isoformat(), 'status': 'pass',
        'checks': len(checks), 'failures': [], 'sourceBindings': bindings, 'results': checks, 'histories': histories,
        'counts': {'conditionalHistories': len(histories), 'FloraModesIdentified': 3},
        'completeContracts': {k: contracts[k] for k in ['verdant_bond', 'trapcasting']},
        'scope': 'Paid Verdant wilderness Nature-check advantage and ordinary cancellation, current active-Flora plant-only difficult-terrain exception with actual movement ledger, and three Flora mode identification/disarm Action tasks through actual inspector ability/training.',
        'limits': ['Terrain causes, wilderness, legal task work/senses/inspection, actual held tools, one-axis route legality, hazards and real actor Action/Speed budgets are explicit conditional world premises, not authenticated campaign or general pathfinding/acoustics/perception systems.',
            'Movement records actual one-axis endpoints and conserved expenditure. Hazards remain pending ordinary resolution; no damage immunity or automatic obstacle/occupied-space passage is supplied.',
            'Inspection cases use a distinct source-materialized Warrior8 inspector with ordinary INT/DEX and no Investigation/thieves-tools proficiency. They do not certify every proficiency source or arbitrary task advantage/condition.',
            'Core kept-die/task outcomes execute, but the fictional knowledge/reaction/effect layers remain bounded. Full ordinary plant attacks/defenses/life-state and genuine scheduler/whole335 execution are separate.',
            'Nature Whisper classification and casting interfaces remain under the separate actual GPT review; this pass changes no source rule or approval.'],
        'newRules': 0, 'fullFeatExactApproved': False, 'runtimeApproved': False, 'humanBalanceApproved': False, 'cosmologyReviewed': False}
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2, default=serial) + '\n', encoding='utf-8', newline='\n')
    print(json.dumps({'checks': len(checks), 'histories': len(histories), 'report': info(out)}))


if __name__ == '__main__': main()
