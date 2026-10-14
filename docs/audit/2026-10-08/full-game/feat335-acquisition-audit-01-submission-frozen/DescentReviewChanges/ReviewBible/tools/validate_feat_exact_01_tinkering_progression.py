"""Validate real source trade thresholds and a paid Tinker Adept acquisition."""
from copy import deepcopy
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
from feat_exact_01_acquisition_models import PaidChoices
from feat_exact_01_training_prerequisite_model import materialize_training
from feat_exact_01_tinkering_progression import TinkeringProgression

R = Path(__file__).resolve().parents[1]; G = R.parents[1]; A = G / 'docs/audit/2026-10-08/full-game'


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def info(path):
    data = path.read_bytes()
    return {'path': path.relative_to(G).as_posix(), 'bytes': len(data), 'sha256': sha256(data).hexdigest()}


def serial(value):
    if isinstance(value, set):
        return sorted(value)
    raise TypeError(type(value).__name__)


def main():
    output = A / 'FEAT_EXACT_01_TINKERING_PROGRESSION_CHECK.json'
    notes = A / 'FEAT_EXACT_01_TINKERING_PROGRESSION_NOTES.md'
    assert not output.exists() and not notes.exists(), 'Refuse to overwrite source evidence'
    paths = [Path(__file__), R / 'tools/feat_exact_01_tinkering_progression.py',
        R / 'tools/feat_exact_01_training_prerequisite_model.py', R / 'tools/feat_exact_01_acquisition_models.py',
        R / 'tools/validate_advanced_craft_worked_cases.py', R / 'tools/core_playtest_rules.py',
        R / 'tools/spell_playtest_rules.py', R / 'tools/fishing_reference.py',
        R / 'data/playtest/character_foundation.json', R / 'data/playtest/ancestry_background_candidate.json',
        R / 'data/playtest/equipment_source_catalog.json', R / 'data/crafting/advanced_craft_recipe_candidate_public.json',
        R / 'data/playtest/crafting_engine_candidate.json', R / 'docs/mechanics/CRAFTING_HARVEST_PLAYTEST.md',
        R / 'docs/mechanics/CRAFTING_TRADE_REFERENCE.md', A / 'FEAT_EXACT_01_INITIATE_ACQUISITION_CHECK.json',
        A / 'FEAT_EXACT_01_ACQUISITION_CONTRACTS.json', A / 'FEAT_EXACT_01_COMPOSITE_CASTING_PREREQUISITE_CHECK.json']
    bindings = [info(path) for path in paths]
    foundation = read(paths[8]); classes = {c['class']: c for c in foundation['classes']}
    skills = {s: ability for ability, group in foundation['skillAbilities'].items() for s in group}
    ancestry = read(paths[9]); backgrounds = {b['id']: b for b in ancestry['backgrounds']}
    equipment = {x['id']: x for x in read(paths[10])['records']}
    advanced = read(paths[11]); card = next(c for c in advanced['cards'] if c['recipeId'] == 'recipe-591')
    craft = read(paths[12]); guide = paths[13].read_text(encoding='utf-8')
    actor = deepcopy(read(paths[15])['actorSourceProjection'])
    actor.update({'firstClass': 'Monk', 'classLevels': {'Monk': 1}, 'selectedClassSkills': ['Athletics', 'Insight'], 'classToolChoices': ['tools.tinker-s-tools']})
    contracts = {c['id']: c for c in read(paths[16])['records']}; contract = contracts['tinker_adept']
    prior = read(paths[17]); results = []

    def check(label, truth):
        results.append({'id': label, 'passed': bool(truth)})
        if not truth:
            raise AssertionError(label)

    def reject(label, operation, snapshot=None):
        before = snapshot() if snapshot else None
        try:
            operation()
        except (ValueError, KeyError) as exc:
            results.append({'id': label, 'passed': True, 'reason': str(exc)})
        else:
            check(label, False)
        if snapshot:
            check(label + '/no-mutation', snapshot() == before)

    check('reviewed-recipe-whole-source', advanced['exactRecipeApproval'] is True and card['status'] == 'reviewed-authored-operational-playtest')
    check('actual-primary-tool-binding', next(t for t in craft['trades'] if t['name'] == 'Tinkering')['primaryTool'] == "Tinker's tools")
    check('actual-XP-source', 'Advancing from level L to L+1 costs 10+L trade XP' in guide and 'Spend XP immediately when a threshold is reached' in guide)
    check('tool-initialization-source', 'may initialize that trade at level 1, with zero trade XP' in guide)
    check('no-check-modifier-trade-level-alias', 'do not add the numerical trade level to the check' in guide)
    training = materialize_training(actor, classes, equipment, skills, ancestry, backgrounds)
    progress = TinkeringProgression('conditional-monk-tinker', training, 1, card, 33)
    initial = progress.snapshot()
    check('actual-tool-initializes-only-level1-zeroXP', progress.level == 1 and progress.xp == 0 and not progress.prerequisite(contract))
    actor['temporaryBonuses'] = {'Tinkering': 99, 'INT': 99}
    check('temporary-bonuses-not-trade-progression', not progress.prerequisite(contract))
    untrained = deepcopy(training); untrained['tools'].remove('tools.tinker-s-tools')
    untrained['ownedKit'] = 'tools.tinker-s-tools'; untrained['claimedTinkeringModifier'] = 99
    reject('physical-kit-and-high-check-bonus-not-training', lambda: TinkeringProgression('untrained', untrained, 1, card, 1))

    def order(index):
        start = ((index - 1) // 4) * 1440 + ((index - 1) % 4) * 120
        return {'id': 'conditional-order-' + str(index), 'actorId': progress.actor_id, 'recipeId': card['recipeId'],
                'role': 'lead', 'startMinute': start, 'endMinute': start + 120,
                'station': "Tinker's Workshop", 'physicalTools': deepcopy(card['sourceRecipe']['workRequirements']['requiredTools']),
                'componentOccurrences': deepcopy(card['sourceRecipe']['components']), 'chosenAbility': 'INT',
                'naturalD20': 5, 'toolBonus': 0, 'facilityBonus': 0, 'assistantBonus': 0,
                'conditionalPremises': 'Independent fabrication, ordinary body/material eligibility, world access and completed Standard work are supplied source-qualified premises; this pass replays XP, not the complete product engine.'}

    bad = order(1); bad['endMinute'] = 119
    reject('incomplete-work-no-award', lambda: progress.complete(bad), progress.snapshot)
    bad = order(1); bad['physicalTools'] = ["Tinker's tools"]
    reject('proficiency-does-not-supply-workshop-tools', lambda: progress.complete(bad), progress.snapshot)
    bad = order(1); bad['role'] = 'assistant'
    reject('assistant-does-not-receive-lead-XP', lambda: progress.complete(bad), progress.snapshot)
    bad = order(1); bad['actorId'] = 'another-actor'
    reject('another-actor-receipt-no-award', lambda: progress.complete(bad), progress.snapshot)
    bad = order(1); bad['componentOccurrences'][0]['quantity'] -= 1
    reject('incomplete-input-receipt-no-award', lambda: progress.complete(bad), progress.snapshot)
    trace4 = None; trace5 = None
    for index in range(1, 25):
        trace = progress.complete(order(index))
        # Independent closed-form thresholds derived from the printed 10+L costs.
        total = 4 + (index - 1) * 2
        expected_level = 1
        while expected_level < 20 and total >= sum(10 + level for level in range(1, expected_level + 1)):
            expected_level += 1
        spent = sum(10 + level for level in range(1, expected_level))
        check('order' + str(index) + '/XP-award', trace['xpAward'] == (4 if index == 1 else 2))
        check('order' + str(index) + '/level-and-carry', (progress.level, progress.xp, progress.total_earned) == (expected_level, total - spent, total))
        check('order' + str(index) + '/actual-trade-gate', progress.prerequisite(contract) == (expected_level >= 5))
        check('order' + str(index) + '/trade-not-added-to-check', trace['modifier'] == 5 and trace['sourceBand'] == 'Standard')
        if index == 23:
            trace4 = progress.snapshot()
        if index == 24:
            trace5 = progress.snapshot()
    check('level4-boundary', (trace4['level'], trace4['xp'], trace4['total_earned']) == (4, 12, 48))
    check('level5-boundary', (trace5['level'], trace5['xp'], trace5['total_earned']) == (5, 0, 50))
    reject('duplicate-completion-no-second-XP', lambda: progress.complete(order(24)), progress.snapshot)
    overlap = order(25); overlap['startMinute'] = progress.last_end - 120; overlap['endMinute'] = progress.last_end
    reject('overlapping-work-no-award', lambda: progress.complete(overlap), progress.snapshot)
    # Ordinary progression remains independent from the earned class feat payment.
    pay = PaidChoices({n: c['asiClassLevels'] for n, c in classes.items()}, {}, {'Monk': 1}, deepcopy(training['scores']), set(contracts))
    reject('trade5-does-not-create-class-opportunity', lambda: pay.earn_class_opportunity('Monk:1', 'Monk', 1), lambda: deepcopy(pay.__dict__))
    pay.current_classes = {'Monk': 4}; pay.earn_class_opportunity('Monk:4', 'Monk', 4)
    acquired = pay.commit('tinker_adept', 'Monk:4', prerequisites_met=progress.prerequisite(contract))
    check('Tinker-Adept-paid-own-class-selection', acquired['identity'] == 'tinker_adept' and pay.opportunities['Monk:4']['spent'])
    check('feat-does-not-change-trade-record', progress.snapshot() == trace5)
    pay.current_classes = {'Monk': 8}; pay.earn_class_opportunity('Monk:8', 'Monk', 8)
    reject('Tinker-Adept-not-repeatable', lambda: pay.commit('tinker_adept', 'Monk:8', prerequisites_met=progress.prerequisite(contract)), lambda: deepcopy(pay.__dict__))
    # Reach the recipe's true trivial threshold through real repeats, then award zero.
    for index in range(25, 33):
        progress.complete(order(index))
    check('real-progression-reaches-trivial-level6', (progress.level, progress.xp, progress.total_earned) == (6, 1, 66))
    trivial = progress.complete(order(33))
    check('trivial-success-zeroXP-still-consumes-work-inputs', trivial['xpAward'] == 0 and progress.total_earned == 66 and all(q == 0 for q in progress.stock.values()))
    reject('exhausted-source-stock', lambda: progress.complete(order(34)), progress.snapshot)
    remaining = [x for x in prior['remaining'] if x['id'] != 'tinker_adept']
    check('one-disjoint-partial-identity', len(remaining) == 8 and len(prior['remaining']) == 9)
    for bound in bindings:
        check('unchanged/' + bound['path'], info(G / bound['path']) == bound)
    report = {'createdAtUtc': datetime.now(timezone.utc).isoformat(), 'status': 'passed-source-trade-progression-and-paid-Tinker-Adept-history',
        'sourceBindings': bindings, 'actorSourceProjection': actor, 'initialTradeState': initial,
        'level4Boundary': trace4, 'level5Boundary': trace5, 'completeProgression': progress.snapshot(),
        'paidAcquisitionHistory': deepcopy(pay.__dict__), 'completeFeatContract': contract, 'completeRecipeCard': card,
        'counts': {'workOrderReceipts': 33, 'successfulNontrivialOrders': 32, 'trivialSuccessOrders': 1,
            'earnedTradeXP': 66, 'activeWorkMinutes': 3960, 'newPartialPrerequisiteIdentities': 1,
            'cumulativePartialPrerequisiteIdentities': 327, 'remainingCredentialDependentIdentities': 8},
        'checks': len(results), 'failures': [], 'results': results, 'remaining': remaining,
        'scope': 'Exact actual Tinkering primary-tool initialization and XP costs/first-success/repeat/trivial accounting, with source-qualified conditional order receipts and a separately earned paid Tinker Adept selection.',
        'limits': ['These are synthetic character/work-order histories. Source files are authenticated; actual campaign rolls, work, inventory procurement and legal fabrication premises are not authenticated.',
            'Only the supplied Standard Field Stone Tool work/roll/material slice is replayed. This is not a new review or full execution of all crafting, body fabrication, quality bands, failure research, formula acquisition, product effects or market behavior.',
            'The feat acquisition has no permanent menu or intrinsic finite pool; its complex-mechanism repair use and Short Rest repair bonus remain outside this pass.',
            'Only Tinker Adept is removed from the disjoint partial-prerequisite remainder. No complete327-feat acquisition/use or whole-game approval is claimed.'],
        'newRulesAdopted': False, 'candidateReadyForSubmission': False, 'sourceInformationDeleted': False, 'cosmologyReviewed': False}
    with output.open('x', encoding='utf-8', newline='\n') as stream:
        json.dump(report, stream, ensure_ascii=False, indent=2, default=serial); stream.write('\n')
    with notes.open('x', encoding='utf-8', newline='\n') as stream:
        stream.write(f'''# Tinker Adept acquisition and trade progression

{len(results)} checks pass. An actual Monk artisan-tool choice supplies Tinker's-tools proficiency and initializes Tinkering at level1/zeroXP. The history replays conditional source-bound Standard Field Stone Tool completions:4XP for its first nontrivial success,2XP for repeats, and immediate advancement costing10+current level.

After23 orders, the crafter has48 total earned XP and is level4 with12XP remaining; Tinker Adept fails. After24 orders,50 earned XP reaches level5 with zero remaining; it qualifies. This does not supply a class feat opportunity: the history separately reaches Monk4, earns its actual ASI/feat selection and spends it once. A high skill modifier, temporary bonus or owned kit cannot substitute for trade progression.

The longer33-order replay reaches level6, then correctly awards zero for a trivial success while still consuming the stated work and inputs. Duplicate, overlapping, incomplete, foreign-actor and assistant receipts do not award XP.

These are conditional source-qualified work-order and character slices, not full fabrication, actual campaign authentication, repair execution or runtime. The partial predicate ledger now has327 covered identities and8 remaining.
''')
    print(json.dumps({'report': info(output), 'notes': info(notes), 'checks': len(results), 'failures': 0, 'remaining': len(remaining)}, indent=2))


if __name__ == '__main__':
    main()
