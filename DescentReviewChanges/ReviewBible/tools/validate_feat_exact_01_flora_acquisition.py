"""Verify the exact SUP07 choice omitted by the earlier partial Flora model."""
from copy import deepcopy
from datetime import datetime, timezone
import json
from pathlib import Path
from feat_exact_01_flora_acquisition import FloraAcquisition
from feat_exact_01_casting_credential_model import CastingSources
from validate_feat_exact_01_composite_casting import read, info, serial

R = Path(__file__).resolve().parents[1]; G = R.parents[1]
A = G / 'docs/audit/2026-10-08/full-game'


def main():
    output = A / 'FEAT_EXACT_01_FLORA_ACQUISITION_CHECK.json'; notes = A / 'FEAT_EXACT_01_FLORA_ACQUISITION_NOTES.md'
    assert not output.exists() and not notes.exists()
    paths = [Path(__file__), R / 'tools/feat_exact_01_flora_acquisition.py',
        R / 'tools/feat_exact_01_casting_selections.py', R / 'tools/feat_exact_01_remaining_owned_chains.py',
        R / 'tools/feat_exact_01_composite_casting_model.py', R / 'tools/feat_exact_01_casting_credential_model.py',
        R / 'tools/feat_exact_01_training_prerequisite_model.py', R / 'tools/feat_exact_01_initiate_acquisition_model.py',
        R / 'tools/feat_exact_01_acquisition_models.py', R / 'data/playtest/character_foundation.json',
        R / 'data/playtest/ancestry_background_candidate.json', R / 'data/playtest/equipment_source_catalog.json',
        R / 'data/public/class_playtests/wizard.json', R / 'data/public/feat_candidates/exact_01/spell_dependencies.json',
        R / 'data/public/feat_candidates/exact_01/supplements.json', R / 'data/public/feat_candidates/exact_01/shared_rules.json',
        A / 'FEAT_EXACT_01_ACQUISITION_CONTRACTS.json', A / 'FEAT_EXACT_01_INITIATE_ACQUISITION_CHECK.json',
        A / 'FEAT_EXACT_01_REMAINING_OWNED_CHAINS_CHECK.json']
    bindings = [info(p) for p in paths]
    foundation = read(paths[9]); classes = {x['class']: x for x in foundation['classes']}
    skills = {s: a for a, names in foundation['skillAbilities'].items() for s in names}
    ancestry = read(paths[10]); backgrounds = {x['id']: x for x in ancestry['backgrounds']}
    equipment = {x['id']: x for x in read(paths[11])['records']}
    supplements = {x['id']: x['value'] for x in read(paths[14])['groups']}
    sources = CastingSources(G, read(paths[13])['spells'], supplements, read(paths[12]))
    contracts = {x['id']: x for x in read(paths[16])['records']}
    base_actor = read(paths[17])['actorSourceProjection']
    checks = []; histories = []

    def check(label, condition):
        checks.append({'id': label, 'passed': bool(condition)})
        if not condition: raise AssertionError(label)

    def reject(label, history, operation):
        before = history.snapshot()
        try: operation()
        except ValueError as exc: checks.append({'id': label, 'passed': True, 'reason': str(exc)})
        else: check(label, False)
        check(label+'/atomic', history.snapshot() == before)

    def make(nature=True):
        actor = deepcopy(base_actor)
        actor.update(firstClass='Warrior', classLevels={'Warrior': 1},
                     selectedClassSkills=['Nature' if nature else 'Survival', 'Athletics'])
        return FloraAcquisition(actor, classes, equipment, skills, ancestry, backgrounds, contracts, supplements, sources)

    def with_route(ability='INT', nature=True):
        h = make(nature); h.advance(4); h.earn(4)
        h.acquire_casting_selection('telekinetic', 4, {'ability': ability})
        return h

    def record(label, before, h, **extra):
        histories.append({'id': label, 'before': before, 'after': h.snapshot(), **extra})

    dc_clause = supplements['SUP-07']['floraBody']['dc']
    check('existing-source-mandatory-route', dc_clause == 'At acquisition select one actual possessed spellcasting route; use DC 8+current PB+that route’s current ability modifier. No phantom Wisdom/Spellcraft statistic. Actual source-specific component/target defenses still apply.')
    check('capacity-is-total-level', 'Capacity is 1, or 2 at total level 10.' in contracts['conjure_flora']['completeOperativeProcedure'])
    check('level10-is-not-another-Warrior-opportunity', 10 not in classes['Warrior']['asiClassLevels'])
    for ability in ['INT', 'WIS', 'CHA']:
        for attained in [8, 9, 10, 12, 20]:
            h = with_route(ability); h.advance(attained); h.earn(8); route = h.actual_casting_routes()[0]
            before = h.snapshot(); previous_routes = deepcopy(h.casting.snapshot()); scores = deepcopy(h.pay.scores)
            h.acquire_named('conjure_flora', 8, route)
            state = h.initializations['conjure_flora']; projected = h.flora_dc_projection()
            label = ability+'/'+str(attained)
            check(label+'/permanent-exact-route', state['fixedCastingRoute'] == route and h.pay.grants[-1]['choice'] == route)
            check(label+'/capacity-uses-current-level-not-opportunity', state['plantCapacity'] == (2 if attained >= 10 else 1))
            check(label+'/initial-allowance-no-bodies-entitlement-or-stat-grant', state['creationUses'] == {'maximum': 1, 'current': 1} and
                  state['activePlants'] == [] and not state['additionalCreationPending'] and h.pay.scores == scores and h.casting.snapshot() == previous_routes)
            expected_pb = 2+(attained-1)//4
            check(label+'/current-stat-DC', projected['dc'] == 8+expected_pb+(scores[ability]-10)//2 and projected['currentPB'] == expected_pb)
            record('paid-Flora/'+label, before, h, dc=projected)

        h = with_route(ability); h.advance(8); h.earn(8); route = h.actual_casting_routes()[0]
        invalid = [None, {'ability': ability}, {**route, 'grantId': 'not-acquired'},
                   {**route, 'sourceClass': 'Druid'}, {**route, 'ability': 'STR'},
                   {**route, 'ability': next(x for x in ['INT', 'WIS', 'CHA'] if x != ability)},
                   {**route, 'freePlant': True}]
        for i, choice in enumerate(invalid):
            reject(ability+'/invalid-choice/'+str(i), h, lambda c=choice: h.acquire_named('conjure_flora', 8, c))
        before = h.snapshot(); h.casting.use_state.update(rp=0, temporaryBlocks=['conditional-Incapacitated'])
        h.acquire_named('conjure_flora', 8, route)
        check(ability+'/temporary-casting-block-does-not-erase-acquisition-route', h.initializations['conjure_flora']['fixedCastingRoute'] == route)
        before_growth = deepcopy(h.initializations['conjure_flora']); h.advance(10)
        check(ability+'/capacity-growth-no-free-creation', h.initializations['conjure_flora'] == {**before_growth, 'plantCapacity': 2})
        h.advance(12); h.earn(12)
        reject(ability+'/nonrepeatable-no-reinitialization', h, lambda: h.acquire_named('conjure_flora', 12, route))
        record(ability+'/choice-rejections-and-capacity-growth', before, h)

    for first in ['INT', 'WIS', 'CHA']:
        for second in ['INT', 'WIS', 'CHA']:
            if first == second: continue
            for pick in [0, 1]:
                h = with_route(first); h.advance(8); h.earn(8)
                h.acquire_casting_selection('telepathic', 8, {'ability': second})
                routes = h.actual_casting_routes(); check('two-paid-actual-providers/'+first+second+str(pick), len(routes) == 2)
                h.advance(12); h.earn(12); before = h.snapshot(); chosen = routes[pick]
                h.acquire_named('conjure_flora', 12, chosen)
                check('choice-not-best-stat-or-class-alias/'+first+second+str(pick), h.initializations['conjure_flora']['fixedCastingRoute'] == chosen)
                h.advance(16); h.earn(16); h.pay.commit('abilityScoreImprovement', 'Warrior:16',
                    {chosen['ability']: 2}, prerequisites_met=True)
                check('real-ASI-changes-current-DC-not-fixed-route/'+first+second+str(pick), h.flora_dc_projection()['dc'] ==
                      8+5+(before['payment']['scores'][chosen['ability']]+2-10)//2 and h.initializations['conjure_flora']['fixedCastingRoute'] == chosen)
                record('two-provider-selection/'+first+second+str(pick), before, h, actualSelectedProvider=chosen)

    h = make(); h.advance(4); h.earn(4)
    reject('Nature-without-casting-no-Flora', h, lambda: h.acquire_named('conjure_flora', 4, {'ability': 'WIS'}))
    h = with_route(nature=False); h.advance(8); h.earn(8); route = h.actual_casting_routes()[0]
    reject('casting-without-Nature-no-Flora', h, lambda: h.acquire_named('conjure_flora', 8, route))
    h = with_route(); h.advance(8); route = h.actual_casting_routes()[0]
    reject('qualified-but-no-opportunity', h, lambda: h.acquire_named('conjure_flora', 8, route))
    h.earn(8); h.pay.commit('alert', 'Warrior:8', prerequisites_met=True)
    reject('qualified-but-spent-opportunity', h, lambda: h.acquire_named('conjure_flora', 8, route))
    h = with_route(); h.advance(8); h.earn(8); route = h.actual_casting_routes()[0]; h.remove_personal_routes()
    reject('removed-route-before-acquisition', h, lambda: h.acquire_named('conjure_flora', 8, route))
    h = make(); h.advance(4); h.earn(4); h.acquire_casting_selection('forbidden_pact', 4, {'sigil': 'hex'})
    h.advance(8); h.earn(8); route = h.actual_casting_routes()[0]; before = h.snapshot()
    h.acquire_named('conjure_flora', 8, route)
    check('Pact-route-no-phantom-school-or-source-class', route == {'grantId': 'forbidden_pact/Warrior:4', 'ability': 'CHA', 'sourceClass': None} and
          'school' not in h.casting.routes[0] and h.initializations['conjure_flora']['fixedCastingRoute'] == route)
    record('paid-Pact-provider-with-absent-school', before, h)
    check('all-bound-source-bytes-preserved', bindings == [info(p) for p in paths])
    gap = {'kind': 'local-reference-model-omission-not-source-rule-change',
        'sourceClause': dc_clause, 'sourcePointer': '/groups/6/value/floraBody/dc',
        'priorModel': info(paths[3]), 'priorEvidence': info(paths[18]),
        'supersededClaimScope': 'Earlier RemainingOwnedChains Flora initial state omitted the mandatory fixed casting route; it is not complete acquisition evidence. Its parent ownership, prerequisite and empty-body checks remain only their originally demonstrated scopes.',
        'secondCorrection': 'Use current attained total level for capacity, including an earlier unspent opportunity acquired later; opportunity level is payment provenance, not capacity level.',
        'sourceInformationDeleted': False, 'priorReportOverwritten': False}
    report = {'createdAtUtc': datetime.now(timezone.utc).isoformat(), 'status': 'Flora-mandatory-provider-and-current-capacity-reference-pass',
        'checks': len(checks), 'failures': [], 'results': checks, 'sourceBindings': bindings,
        'cohort': ['conjure_flora'], 'localGapCorrection': gap, 'histories': histories,
        'completeOperativeContract': contracts['conjure_flora'], 'completeFloraSupplement': supplements['SUP-07']['floraBody'],
        'counts': {'castingAbilities': 3, 'attainedLevelCasesPerAbility': 5, 'twoProviderChoiceHistories': 12,
                   'recordedHistories': len(histories), 'newPartialPrerequisiteIdentities': 0},
        'limits': ['Source-qualified synthetic Human/Imperial Warrior progression and paid feat-granted personal spell routes, not a full character builder or authenticated campaign.',
            'Uses existing exact Telekinetic, Telepathic and Forbidden Pact acquisition sources. It does not enumerate every possible class/feat casting provider.',
            'DC values are current-stat projections from a fixed acquired provider, not proof of an actual creation, target save, lost-provider use permission or full spellcasting runtime.',
            'Creates no plant. Plant Actions, original minute markers, additional-creation entitlement, rest recovery, commands, Trapcasting, destruction/healing and Verdant Bond use remain open.',
            'The earlier report is preserved and its initial-state incompleteness is explicit. No source rule, exact candidate approval, human balance, runtime, publication or cosmology status changes.'],
        'sourceInformationDeleted': False, 'newRulesAdopted': False, 'fullCandidateApproved': False}
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2, default=serial)+'\n', encoding='utf-8', newline='\n')
    notes.write_text('# Conjure Flora acquisition correction\n\n'
        f'{len(checks)} checks pass across {len(histories)} recorded histories. SUP07 already requires an actual casting-route selection at acquisition. '
        'The earlier partial model omitted that field; a new override now records the exact paid provider and ability without changing or overwriting the earlier model/evidence.\n\n'
        'Plant capacity uses current total level, including a saved level-8 opportunity spent at level 10 or later. All three mental abilities, '
        'two-provider choices, genuine paid ASI changes, unavailable/spent opportunities and missing Nature/casting are exercised. '
        'The feat starts with one creation use and no body or already-pending second creation. No caster resource or spell is added by Flora.\n\n'
        'These are acquisition/current-stat checks. Actual seedlings, rest, command phases, Trapcasting, body conservation and lost-provider use behavior remain separate. '
        'The omission and correction must be carried into the actual GPT audit follow-up.\n', encoding='utf-8', newline='\n')
    print(json.dumps({'checks': len(checks), 'failures': 0, 'counts': report['counts'], 'report': info(output), 'notes': info(notes)}, indent=2))


if __name__ == '__main__': main()
