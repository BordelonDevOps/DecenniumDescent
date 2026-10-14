"""Finite source-qualified acquisition histories for three trade-training feats."""
from copy import deepcopy
from datetime import datetime, timezone
import json
from pathlib import Path
from feat_exact_01_trade_selections import TradeSelections
from validate_feat_exact_01_composite_casting import read, info, serial

R = Path(__file__).resolve().parents[1]; G = R.parents[1]
A = G/'docs/audit/2026-10-08/full-game'


def main():
    output = A/'FEAT_EXACT_01_TRADE_SELECTIONS_CHECK.json'
    notes = A/'FEAT_EXACT_01_TRADE_SELECTIONS_NOTES.md'
    assert not output.exists() and not notes.exists()
    paths = [Path(__file__), R/'tools/feat_exact_01_trade_selections.py', R/'tools/feat_exact_01_prodigy_choices.py',
             R/'tools/feat_exact_01_acquisition_models.py', R/'tools/feat_exact_01_training_prerequisite_model.py',
             R/'data/playtest/character_foundation.json', R/'data/playtest/ancestry_background_candidate.json',
             R/'data/playtest/equipment_source_catalog.json', R/'docs/mechanics/CRAFTING_TRADE_REFERENCE.md',
             R/'docs/mechanics/CHARACTER_CREATION_PLAYTEST.md', A/'FEAT_EXACT_01_ACQUISITION_CONTRACTS.json',
             A/'FEAT_EXACT_01_INITIATE_ACQUISITION_CHECK.json', R/'data/public/feat_candidates/exact_01/candidate.json']
    bindings = [info(p) for p in paths]
    foundation = read(paths[5]); classes = {r['class']: r for r in foundation['classes']}
    skills = {skill: ability for ability, group in foundation['skillAbilities'].items() for skill in group}
    ancestry = read(paths[6]); backgrounds = {r['id']: r for r in ancestry['backgrounds']}
    equipment = {r['id']: r for r in read(paths[7])['records']}; trade_reference = paths[8].read_text(encoding='utf-8')
    contracts = {r['id']: r for r in read(paths[10])['records']}
    actor = deepcopy(read(paths[11])['actorSourceProjection'])
    actor.update(firstClass='Warrior', classLevels={'Warrior': 1}, selectedClassSkills=['Animal Handling', 'Athletics'])
    results = []; histories = []

    def check(label, truth):
        results.append({'id': label, 'passed': bool(truth)})
        if not truth:
            raise AssertionError(label)

    def history(custom=None):
        h = TradeSelections(custom or actor, classes, equipment, skills, ancestry, backgrounds, contracts, trade_reference)
        h.advance(4); h.earn(4); return h

    def record(label, before, h, premise='Actual source-derived Human/Imperial first-class training, ability rolls and paid ASI slice; no complete class build or real campaign asserted'):
        histories.append({'id': label, 'premise': premise, 'before': before, 'after': h.snapshot()})

    def reject(label, h, sid, selected, level=4):
        before = h.snapshot()
        try:
            h.acquire(sid, level, selected)
        except ValueError as error:
            results.append({'id': label, 'passed': True, 'reason': str(error)})
        else:
            check(label, False)
        check(label + '/unspent-and-unchanged', h.snapshot() == before)
        histories.append({'id': label, 'premise': 'Rejected command', 'feat': sid, 'selection': selected, 'before': before, 'after': h.snapshot()})

    baseline = history()
    check('19-actual-artisan-tool-options', len(baseline.artisan) == 19)
    check('16-distinct-primary-trades', len(baseline.by_trade) == 16)
    # Select every legal table row under an actual class-scheduled opportunity.
    for sid in ['artisan', 'craftsman', 'versatile_artisan']:
        options = sorted(baseline.by_trade if sid == 'versatile_artisan' else baseline.artisan)
        for selected in options:
            h = history(); before = h.snapshot(); event = h.acquire(sid, 4, selected)
            tool = baseline.by_trade[selected] if sid == 'versatile_artisan' else selected
            check(sid + '/' + selected + '/one-real-proficiency', h.tools - set(before['tools']) == {tool})
            expected = {h.primary[tool]: {'level': 1, 'xp': 0}} if tool in h.primary else {}
            check(sid + '/' + selected + '/only-actual-trade', h.trades == expected)
            check(sid + '/' + selected + '/one-real-paid-choice', h.pay.opportunities['Warrior:4']['spent'] and len(h.pay.grants) == 1)
            check(sid + '/' + selected + '/no-other-created-assets', h.actor['physicalInventory'] == [] and event['physicalEquipmentGranted'] == [] and event['recipeOrFormulaGranted'] == [] and event['expertiseGranted'] == [] and h.pay.scores == before['payment']['scores'])
            record(sid + '/' + selected, before, h)
            h.advance(8); h.earn(8)
            next_choice = next(x for x in options if x != selected)
            reject(sid + '/' + selected + '/nonrepeatable', h, sid, next_choice, 8)
    # Non-artisan primaries remain illegal for an artisan-tool grant.
    excluded = set(baseline.primary) - baseline.artisan
    check('non-artisan-primary-identities', {baseline.primary[t] for t in excluded} == {'Fishing', 'Herbalism', 'Mining', 'Poisoncrafting', 'Salvaging', 'Skinning'})
    for sid in ['artisan', 'craftsman']:
        for tool in sorted(excluded | {'tools.flute', 'tools.dragonchess-set', 'tools.thieves-tools'}):
            reject(sid + '/wrong-category/' + tool, history(), sid, tool)
        reject(sid + '/missing-selection', history(), sid, None)
        reject(sid + '/unknown-selection', history(), sid, 'invented-mastercraft-kit')
        low_actor = deepcopy(actor); low_actor['abilityRolls']['INT'] = [1, 1, 5, 5]; low_actor['permanentScores']['INT'] = 12
        low = history(low_actor); low.actor['temporaryBonuses'] = {'INT': 10}
        reject(sid + '/temporary-bonus-does-not-meet-INT13', low, sid, 'tools.tinker-s-tools')
        boundary_actor = deepcopy(actor); boundary_actor['abilityRolls']['INT'] = [1, 2, 5, 5]; boundary_actor['permanentScores']['INT'] = 13
        h = history(boundary_actor); old = h.snapshot(); h.acquire(sid, 4, 'tools.tinker-s-tools')
        check(sid + '/permanent-INT13-boundary', h.pay.scores['INT'] == 13 and h.pay.has(sid))
        record(sid + '/INT13', old, h)
    # Dice-set training is enough for the prerequisite; it does not create a
    # prior discipline, kit, level or source of crafting XP.
    h = history(); check('unrelated-real-tool-qualifies-no-prior-trade', h.tools == {'tools.dice-set'} and h.trades == {})
    h.acquire('versatile_artisan', 4, 'Fishing')
    check('Fishing-is-explicit-cross-discipline-option', h.trades == {'Fishing': {'level': 1, 'xp': 0}} and 'adventuring-gear.fishing-tackle' in h.tools)
    reject('discipline-choice-is-not-arbitrary-tool', history(), 'versatile_artisan', 'tools.flute')
    reject('discipline-choice-is-not-invented-trade', history(), 'versatile_artisan', 'Carpentry')
    no_tool_actor = deepcopy(actor); no_tool_actor.update(background='arcane-academy-dropout', backgroundToolChoice=None)
    no_tool = history(no_tool_actor); no_tool.actor['physicalInventory'] = ['tools.tinker-s-tools']
    reject('physical-kit-does-not-establish-prerequisite', no_tool, 'versatile_artisan', 'Tinkering')
    unpaid = history(); unpaid.pay.opportunities.clear(); reject('eligibility-does-not-award-opportunity', unpaid, 'artisan', 'tools.tinker-s-tools')
    h = history(); h.acquire('artisan', 4, 'tools.tinker-s-tools')
    reject('one-opportunity-cannot-buy-two-training-feats', h, 'craftsman', 'tools.smith-s-tools')
    h.advance(8); h.earn(8); reject('already-trained-artisan-choice-must-change', h, 'craftsman', 'tools.tinker-s-tools', 8)
    old = h.snapshot(); h.acquire('craftsman', 8, 'tools.smith-s-tools'); h.advance(12); h.earn(12)
    reject('already-trained-discipline-must-change', h, 'versatile_artisan', 'Tinkering', 12)
    h.acquire('versatile_artisan', 12, 'Mining')
    check('three-distinct-source-feats-three-real-payments', [g['opportunity'] for g in h.pay.grants] == ['Warrior:4', 'Warrior:8', 'Warrior:12'])
    check('three-discipline-initializations-no-inherited-level', h.trades == {t: {'level': 1, 'xp': 0} for t in ['Tinkering', 'Blacksmithing', 'Mining']})
    record('paid-Artisan4-Craftsman8-Versatile12', old, h)

    for sid in ['artisan', 'craftsman', 'versatile_artisan']:
        h = history()
        h.tools.update(h.primary if sid == 'versatile_artisan' else h.artisan)
        h.trades = {h.primary[t]: {'level': 6, 'xp': 7} for t in h.tools if t in h.primary}
        old = h.snapshot(); event = h.acquire(sid, 4, None)
        check(sid + '/exhausted-no-refund-substitution-XP', event['state'] == 'exhausted' and not event['futureChoiceCredit'] and h.trades == old['trades'] and h.tools == set(old['tools']) and h.pay.opportunities['Warrior:4']['spent'])
        record(sid + '/conditional-saturated-menu', old, h, 'Conditional complete preexisting proficiency/history premise; not asserted to be constructible from this partial Warrior history')
    # A remaining non-trade artisan tool is still a legitimate ordinary choice.
    h = history(); h.tools.update(h.artisan - {'tools.carpenter-s-tools'}); h.trades = {h.primary[t]: {'level': 9, 'xp': 12} for t in h.tools if t in h.primary}
    old = h.snapshot(); h.acquire('artisan', 4, 'tools.carpenter-s-tools')
    check('last-artisan-option-does-not-add-seventeenth-trade', h.trades == old['trades'] and 'Carpentry' not in h.trades)
    record('conditional-last-nontrade-artisan', old, h, 'Conditional saturation boundary; actual tool classification and sixteen-trade menu preserved')
    # Prior lawful progression is a named conditional premise here; retaining
    # it is distinct from importing it into the newly learned discipline.
    h = history(); h.tools.add('tools.tinker-s-tools'); h.trades['Tinkering'] = {'level': 7, 'xp': 3}
    old = h.snapshot(); h.acquire('versatile_artisan', 4, 'Skinning')
    check('prior-level-retained-new-discipline-starts-at-one', h.trades == {'Tinkering': {'level': 7, 'xp': 3}, 'Skinning': {'level': 1, 'xp': 0}})
    record('conditional-prior-trade-new-discipline', old, h, 'Conditional genuine prior Tinkering7/3XP state; previous crafting work not replayed in this test')
    public = {r['id']: r for r in read(paths[12])['feats']}
    for sid in ['artisan', 'craftsman', 'versatile_artisan']:
        check(sid + '/complete-source-procedure-equality', public[sid]['operationalRules'] == contracts[sid]['completeOperativeProcedure'])
    check('all-bound-inputs-preserved', bindings == [info(p) for p in paths])
    report = {'createdAtUtc': datetime.now(timezone.utc).isoformat(), 'status': 'three-tool-training-feat-choice-pass',
              'checks': len(results), 'failures': [], 'results': results, 'sourceBindings': bindings,
              'cohort': ['artisan', 'craftsman', 'versatile_artisan'], 'actorSourceProjection': actor,
              'artisanToolOptions': sorted(baseline.artisan), 'disciplinePrimaryTools': baseline.by_trade,
              'fullSourceProcedures': {sid: contracts[sid]['completeOperativeProcedure'] for sid in ['artisan', 'craftsman', 'versatile_artisan']},
              'histories': histories, 'counts': {'artisans': 19, 'disciplines': 16, 'allMenuPositiveCases': 54, 'recordedHistories': len(histories), 'newPrerequisiteIdentities': 0},
              'limits': ['Acquisition/training initialization only; not a complete build or authenticated campaign.',
                         'Conditional saturation/prior-XP states are not claimed as complete earned histories.',
                         'Masterwork eligibility and actual recipe execution, Craftsman time-discount composition and every full feat use remain separate work.',
                         'No recipe review reopened, new trade authored, physical kit granted, source changed, whole candidate approval or software implementation claimed.'],
              'sourceInformationDeleted': False, 'newRulesAdopted': False, 'fullCandidateApproved': False}
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2, default=serial)+'\n', encoding='utf-8', newline='\n')
    notes.write_text('# Three trade-training feat selections\n\n'
        f'{len(results)} checks passed across {len(histories)} recorded histories. All 19 actual artisan-tool options are selected separately for Artisan and Craftsman, '
        'and all 16 crafting disciplines are selected for Versatile Artisan (54 positive menu cases). '
        'Each uses a real source class ASI and preserves the correct primary-tool/trade distinction.\n\n'
        'Negative cases cover non-artisan/category errors, an inventory kit without proficiency, permanent INT boundaries, duplicate or repeated acquisition, '
        'and shared payment. Conditional saturation and prior-XP states exercise exhausted menus and no level import/reset; they are not complete campaign histories.\n\n'
        'No recipes, time-discount work, quality outcomes, game runtime or whole feat-candidate approval are claimed by this acquisition-only pass. All source rules remain unchanged.\n', encoding='utf-8', newline='\n')
    print(json.dumps({'checks': len(results), 'failures': 0, 'counts': report['counts'], 'report': info(output), 'notes': info(notes)}, indent=2))


if __name__ == '__main__':
    main()
