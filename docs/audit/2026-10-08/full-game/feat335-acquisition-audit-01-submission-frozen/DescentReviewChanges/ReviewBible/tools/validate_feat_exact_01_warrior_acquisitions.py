"""Validate twelve sourced mutation-feat acquisitions and bounded activation.

Both possible Advanced cap readings are used only for these shared witnesses;
the mixed-tree ambiguity remains an independent actual-GPT review issue.
"""
import argparse
from collections import Counter
from copy import deepcopy
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path

from feat_exact_01_acquisition_models import PaidChoices, FiniteFeatUse
from feat_exact_01_warrior_acquisition_model import (
    mutation_slots, loadout_errors, mutation_prerequisites_met,
    mutation_component_ready, BasicMutationActivation,
)

R = Path(__file__).resolve().parents[1]
G = R.parents[1]
A = G/'docs/audit/2026-10-08/full-game'


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def info(path):
    data = path.read_bytes()
    return {'path': path.relative_to(G).as_posix(), 'bytes': len(data), 'sha256': sha256(data).hexdigest()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path, default=A/'FEAT_EXACT_01_WARRIOR_ACQUISITION_CHECK.json')
    parser.add_argument('--notes', type=Path, default=A/'FEAT_EXACT_01_WARRIOR_ACQUISITION_NOTES.md')
    args = parser.parse_args()
    assert not args.report.exists() and not args.notes.exists(), 'Preserve prior evidence; use new output paths'
    fixture_path = A/'FEAT_EXACT_01_WARRIOR_ACQUISITION_FIXTURES.json'
    authored = read(fixture_path)
    warrior_path = R/'data/public/class_playtests/warrior.json'
    warrior = read(warrior_path)
    source_cards = {card['id']: card for card in warrior['cards']}
    contracts = read(A/'FEAT_EXACT_01_ACQUISITION_CONTRACTS.json')
    by_id = {record['id']: record for record in contracts['records']}
    foundation = read(R/'data/playtest/character_foundation.json')
    schedules = {row['class']: row['asiClassLevels'] for row in foundation['classes']}
    aliases = {record['sharedPaidIdentity']['classCardId']: record['id']
               for record in contracts['records'] if 'sharedPaidIdentity' in record}
    profiles = authored['ordinaryMutationProfiles']
    history = authored['completeClassSelectionHistoryThrough20']
    paths = [Path(__file__), R/'tools/feat_exact_01_warrior_acquisition_model.py',
             R/'tools/feat_exact_01_acquisition_models.py', fixture_path,
             warrior_path, A/'FEAT_EXACT_01_ACQUISITION_CONTRACTS.json',
             R/'data/playtest/character_foundation.json']
    source_bindings = [info(path) for path in paths]
    checks, executed = [], []

    def check(identity, actual, expected, kind='bounded-reference'):
        checks.append({'id': identity, 'kind': kind, 'actual': actual,
                       'expected': expected, 'passed': actual == expected})

    def reject(identity, callback):
        try:
            callback()
        except ValueError:
            check(identity, True, True, 'rejection')
        else:
            check(identity, False, True, 'rejection')

    def owned_through(level):
        return {identity for row in history[:level]
                for identity in row['selectedCards']+row['automaticCards']}

    for binding in authored['sourceBindings']:
        check(binding['path']+':fixture-source-binding', info(G/binding['path']), binding, 'source-integrity')
    check('twelve-explicit-aliases-only', len(aliases), 12, 'source-data')
    check('thirty-three-normal-source-mutations', len(profiles), 33, 'source-data')
    check('warrior-schedule-source-agreement', schedules['Warrior'], warrior['asiClassLevels'], 'source-data')
    slot_ids = ['warrior.supplement.mutation-slot-i', 'warrior.supplement.mutation-slot-ii',
                'warrior.supplement.mutation-slot-iii', 'warrior.supplement.apex-form']
    check('actual-slot-levels', [source_cards[sid]['minimumClassLevel'] for sid in slot_ids],
          [1, 5, 13, 20], 'source-data')
    for sid, profile in profiles.items():
        check(sid+':complete-source-card', {key: value for key, value in profile.items()
              if key not in {'tier', 'tree'}}, source_cards[sid], 'source-integrity')

    seen = set()
    for row, schedule in zip(history, warrior['schedule']):
        level = row['classLevel']
        selected = [source_cards[sid] for sid in row['selectedCards']]
        check(f'class-level-{level}:exact-choice-count', len(selected), schedule['choose'], 'class-history')
        check(f'class-level-{level}:minimum-actives',
              sum(card['sourceKind'] == 'active' for card in selected) >= schedule['minimumActives'],
              True, 'class-history')
        check(f'class-level-{level}:ordinary-feat-schedule', row['ordinaryFeatOpportunity'],
              schedule['asiOrFeat'], 'class-history')
        for card in selected:
            check(f'class-level-{level}:{card["id"]}:legal-first-selection',
                  card['minimumClassLevel'] <= level and card['band'] in schedule['bands']
                  and card['acquisition'] == 'selection' and card['id'] not in seen
                  and card['path'] in (None, row['heroPath']), True, 'class-history')
            seen.add(card['id'])
        check(f'class-level-{level}:exact-automatic-grants', sorted(row['automaticCards']),
              sorted(card['id'] for card in source_cards.values() if card['acquisition'] == 'automatic'
                     and card['minimumClassLevel'] == level and card['path'] in (None, 'Wardborn')),
              'class-history')
    check('efficiency-actually-selected-at-three',
          'warrior.arch.mutation-efficiency' in history[2]['selectedCards'], True, 'class-history')
    check('strain-modifier-not-owned-in-activation-witness',
          'warrior.base.mutation-adaptation' in owned_through(20), False, 'class-history')
    check('actual-apex-form-automatic-at20',
          'warrior.supplement.apex-form' in history[19]['automaticCards'], True, 'class-history')

    def ledger(fixture):
        paid = PaidChoices(schedules, aliases, deepcopy(fixture['classLevels']),
                           deepcopy(fixture['permanentScores']), set(by_id))
        for previous in fixture['earlierFeatChoices']:
            sid, level = previous['featId'], previous['classLevel']
            assert by_id[sid]['printedPrerequisite'] == 'None'
            token = f'Warrior:{level}'
            paid.earn_class_opportunity(token, 'Warrior', level)
            paid.commit(sid, token, prerequisites_met=True)
        opportunity = fixture['acquisitionOpportunity']
        paid.earn_class_opportunity(opportunity['identity'], 'Warrior', opportunity['classLevel'])
        return paid

    for fixture in authored['fixtures']:
        sid = fixture['featId']
        record = by_id[sid]
        level = fixture['classLevels']['Warrior']
        equipped = fixture['equipmentReceipt']['equippedAfter']
        rest_level = fixture['equipmentReceipt']['atWarriorClassLevel']
        token = fixture['acquisitionOpportunity']['identity']
        check(sid+':unchanged-normalized-requirements', fixture['requirements'], record['requirements'], 'source-integrity')
        check(sid+':unchanged-whole-original', fixture['completeOriginalObject'], record['originalObject'], 'source-integrity')
        check(sid+':unchanged-whole-procedure', fixture['completeOperativeProcedure'], record['completeOperativeProcedure'], 'source-integrity')
        check(sid+':actual-whole-class-counterpart', fixture['completeClassCounterpart'],
              source_cards[fixture['classCardAlias']], 'source-integrity')
        check(sid+':source-standard-array', sorted(fixture['baseScores'].values()), [8, 10, 12, 13, 14, 15], 'actor-source')
        check(sid+':permanent-scores-after-once-only-ancestry', fixture['permanentScores'],
              {key: value+fixture['appliedAbilityBonuses'][key] for key, value in fixture['baseScores'].items()}, 'actor-source')
        check(sid+':complete-attained-class-choices', fixture['classProgression'], history[:level], 'actor-source')
        check(sid+':equipped-before-acquisition', rest_level < level, True, 'actor-source')
        for cap_scope in ['global', 'per-tree']:
            prefix = sid+':'+cap_scope
            check(prefix+':actual-rest-loadout-legal', loadout_errors(rest_level, equipped, profiles, cap_scope), [], 'mutation-equipment')
            qualifies = mutation_prerequisites_met(record['requirements'], fixture['classLevels'], equipped, profiles, cap_scope)
            check(prefix+':qualified-dormant-acquisition', qualifies, fixture['expectedPrerequisitesMet'])
            paid = ledger(fixture)
            before_slots = mutation_slots(level)
            grant = paid.commit(sid, token, prerequisites_met=qualifies)
            check(prefix+':paid-canonical-identity', grant['identity'], sid)
            check(prefix+':actual-opportunity-spent-once', paid.opportunities[token]['spent'], True)
            check(prefix+':acquisition-added-no-slots', mutation_slots(paid.current_classes['Warrior'])-before_slots, 0)
            # The same full predicate, rather than an untested supplied True,
            # also controls a first purchase through the explicit class alias.
            alias_paid = ledger(fixture)
            alias_grant = alias_paid.commit(fixture['classCardAlias'], token, prerequisites_met=qualifies)
            check(prefix+':class-alias-is-same-paid-grant', alias_grant, grant)
            reject(prefix+':spent-opportunity-cannot-replay', lambda: paid.commit(sid, token, prerequisites_met=qualifies))
            next_level = next(n for n in schedules['Warrior'] if n > level)
            paid.current_classes['Warrior'] = next_level
            next_token = f'Warrior:{next_level}'
            paid.earn_class_opportunity(next_token, 'Warrior', next_level)
            before = deepcopy((paid.opportunities, paid.grants))
            reject(prefix+':alias-cannot-purchase-second-copy',
                   lambda: paid.commit(fixture['classCardAlias'], next_token, prerequisites_met=qualifies))
            check(prefix+':rejected-copy-preserves-opportunity-and-grant', (paid.opportunities, paid.grants), before)
            check(prefix+':unequipping-does-not-erase-paid-identity', paid.has(sid), True)
            check(prefix+':unequipped-use-component-off', mutation_component_ready(sid, [], [], profiles), False)
            check(prefix+':no-mutation-means-prerequisite-fails',
                  mutation_prerequisites_met(record['requirements'], fixture['classLevels'], [], profiles, cap_scope), False)
            for n, missing in enumerate(equipped):
                rest = equipped[:n]+equipped[n+1:]
                check(prefix+':required-equipped-member-missing:'+missing,
                      mutation_prerequisites_met(record['requirements'], fixture['classLevels'], rest, profiles, cap_scope), False)
            minimum = record['requirements']['requirements'][0]['minimum']
            check(prefix+':class-below-minimum-despite-total-level',
                  mutation_prerequisites_met(record['requirements'], {'Warrior': minimum-1, 'Mage': 1},
                                             equipped, profiles, cap_scope), False)
            # Invalid purchases must leave an actual earned choice untouched.
            unpaid = ledger(fixture)
            snapshot = deepcopy((unpaid.opportunities, unpaid.grants))
            reject(prefix+':missing-mutation-cannot-buy-through-alias',
                   lambda: unpaid.commit(fixture['classCardAlias'], token, prerequisites_met=False))
            check(prefix+':rejection-is-atomic', (unpaid.opportunities, unpaid.grants), snapshot)
        executed.append({'featId': sid, 'fixtureId': fixture['id'], 'classLevel': level,
                         'equippedAtLevel': rest_level, 'equipped': equipped,
                         'paidIdentityConfirmedThroughBothRepresentations': True,
                         'completeUseTimeProcedureExecuted': False})

    def mut(suffix):
        return 'warrior.supplement.'+suffix

    def qualify(sid, level, names, scope='global'):
        return mutation_prerequisites_met(by_id[sid]['requirements'], {'Warrior': level},
                                          [mut(name) for name in names], profiles, scope)

    for name in ['mythic-carapace', 'butcherform-chassis', 'voidbirth-shell']:
        for sid in ['bornToHorrify', 'evolutionUnderFire']:
            check(sid+':actual-Apex-alternative:'+name, qualify(sid, 16, [name]), True)
    for name in ['wailing-eye-cluster', 'viral-core-sacs']:
        check('synapticRot:either-exact-card-alone:'+name, qualify('synapticRot', 8, [name]), True)
    check('synapticRot:both-exact-cards', qualify('synapticRot', 8, ['wailing-eye-cluster', 'viral-core-sacs']), True)
    check('synapticRot:other-Aberrant-is-not-an-alias', qualify('synapticRot', 8, ['carrion-signal-gland']), False)
    check('evisceratorProtocol:generic-talons-name-not-a-source-card',
          loadout_errors(8, [mut('echo-knuckles'), 'Talons'], profiles, 'global')[-1],
          'unrecognized normal mutation profile')
    check('killChainAdaptation:printed4-does-not-add-second-slot',
          qualify('killChainAdaptation', 4, ['brute-knuckles', 'splinter-bone-fangs']), False)
    check('livingFortress:printed8-does-not-add-third-slot',
          qualify('livingFortress', 8, ['ironhide-graft', 'bloodthick-node', 'spinal-buffer']), False)
    check('livingFortress:actual13-can-meet-equipment-predicate',
          qualify('livingFortress', 13, ['ironhide-graft', 'bloodthick-node', 'spinal-buffer']), True)
    check('duplicate-mutation-does-not-fill-two-distinct-requirements',
          qualify('killChainAdaptation', 8, ['brute-knuckles', 'brute-knuckles']), False)
    check('Advanced-not-unlocked-at-Warrior5',
          bool(loadout_errors(5, [mut('echo-knuckles')], profiles, 'global')), True)
    check('Apex-not-unlocked-at-Warrior14',
          bool(loadout_errors(14, [mut('butcherform-chassis')], profiles, 'global')), True)

    # Mutation readiness is only one use-time component; the actual feat's
    # target/trigger/damage/survival requirements are intentionally not asserted.
    blood, iron, spine = map(mut, ['bloodthick-node', 'ironhide-graft', 'spinal-buffer'])
    bio = BasicMutationActivation(5, [blood, iron], profiles, owned_through(5), 'global')
    bio.inject_basic(blood)
    check('bio:one-actual-injection-does-not-satisfy-two-active',
          mutation_component_ready('bioStabilizer', bio.equipped, bio.active, profiles), False)
    reject('bio:second-injection-cannot-reuse-Bonus-Action', lambda: bio.inject_basic(iron))
    bio.next_regular_turn()
    bio.inject_basic(iron)
    check('bio:second-paid-injection-mutation-component-ready',
          mutation_component_ready('bioStabilizer', bio.equipped, bio.active, profiles), True)
    check('bio:two-doses-spent', len(bio.doses), 0)
    check('bio:ordinary-two-injections-gain-two-Strain', bio.strain, 2)
    bio.next_regular_turn()
    bio.next_regular_turn()
    check('bio:first-duration-expiry-disables-component',
          mutation_component_ready('bioStabilizer', bio.equipped, bio.active, profiles), False)
    no_efficiency = BasicMutationActivation(5, [blood, iron], profiles,
                                           owned_through(5)-{'warrior.arch.mutation-efficiency'}, 'global')
    no_efficiency.inject_basic(blood)
    no_efficiency.next_regular_turn()
    reject('level3-does-not-automatically-grant-Efficiency', lambda: no_efficiency.inject_basic(iron))
    no_efficiency.inject_basic(iron, end_active=blood)
    check('ordinary-replacement-leaves-one-active', no_efficiency.active, [iron])

    fortress = BasicMutationActivation(16, [blood, iron, spine], profiles, owned_through(16), 'global')
    fortress.inject_basic(blood)
    fortress.next_regular_turn()
    fortress.inject_basic(iron)
    fortress.next_regular_turn()
    before = deepcopy((fortress.active_until, fortress.doses, fortress.strain))
    reject('fortress:three-slots-do-not-allow-third-ordinary-active', lambda: fortress.inject_basic(spine))
    check('fortress:invalid-third-activation-does-not-spend',
          (fortress.active_until, fortress.doses, fortress.strain), before)
    check('fortress:two-active-not-ready', mutation_component_ready('livingFortress', fortress.equipped, fortress.active, profiles), False)
    reject('fortress:Warrior16-does-not-own-Apex-Form', fortress.activate_apex_form)
    apex = BasicMutationActivation(20, [blood, iron, spine], profiles, owned_through(20), 'global')
    before_resources = (len(apex.doses), apex.strain)
    apex.activate_apex_form()
    check('fortress:actual-owned20-Apex-Form-activates-three',
          mutation_component_ready('livingFortress', apex.equipped, apex.active, profiles), True)
    check('Apex-Form-does-not-consume-serum-or-add-Strain', (len(apex.doses), apex.strain), before_resources)
    apex.next_regular_turn()
    reject('Apex-Form-once-per-encounter-persists-next-turn', apex.activate_apex_form)
    apex.next_regular_turn()
    check('Apex-Form-third-round-still-active', len(apex.active), 3)
    apex.next_regular_turn()
    check('Apex-Form-expiry-ends-no-previous-duration-mutations', apex.active, [])
    check('fortress:Apex-expiry-disables-component',
          mutation_component_ready('livingFortress', apex.equipped, apex.active, profiles), False)
    hyper_use = FiniteFeatUse(1, 1)
    hyper_use.spend()
    reject('hypermutationSpike:paid-acquisition-does-not-reinitialize-spent-use', hyper_use.reacquire)

    for path, binding in zip(paths, source_bindings):
        check(binding['path']+':unchanged-during-run', info(path), binding, 'input-integrity')
    failures = [item for item in checks if not item['passed']]
    result = {
        'recordedAtUtc': datetime.now(timezone.utc).isoformat(),
        'status': 'passed-bounded-shared-Warrior-acquisitions' if not failures else 'failed',
        'scope': 'Twelve named mutation/class acquisition predicates, sourced full class-choice history and '
                 'one paid identity through either explicit representation; bounded Basic-serum/Apex Form '
                 'sequences establish only the mutation component of Bio-Stabilizer/Living Fortress use.',
        'sourceBindings': source_bindings, 'fixtures': info(fixture_path),
        'checks': len(checks), 'checkKinds': dict(Counter(item['kind'] for item in checks)),
        'failures': failures, 'results': checks, 'acquisitions': executed,
        'mutationFeatCount': 12, 'sourceMutationProfiles': 33, 'completeClassHistoryLevels': 20,
        'pendingIndependentIssue': 'FEAT327-ACQ-02. These twelve witnesses are valid under both proposed '
                                   'Advanced tier-cap readings. This report does not adopt either reading '
                                   'or claim mixed-tree cap cases resolved.',
        'allTwelveCompleteUseTimeProceduresExecuted': False,
        'actualCampaignRestAdvancementOrRollReceiptsAuthenticated': False,
        'all335ActualAcquisitionBoundaryCasesExecuted': False,
        'candidateReadyForSubmission': False, 'selectionEnabled': False,
        'sourceInformationDeleted': False, 'runtimeImplemented': False,
        'wholeGameFlowConfirmed': False, 'pushed': False, 'cosmologyReviewed': False,
    }
    notes = [
        '# Twelve shared Warrior feat acquisition witnesses', '',
        '**Synthetic source-qualified acquisitions; complete feat exact review remains outstanding.**', '',
        f'{len(checks)} checks completed with {len(failures)} failures. Each of the twelve original feat identities '
        'retains its entire original object, current operating procedure and actual class counterpart. '
        'The explicit level-by-level Warrior/Wardborn history is checked against all twenty current schedule rows, '
        'including required active selections, automatic grants and feat opportunities.', '',
        'The examples use the standard array and Human/Imperial bonuses once. Named mutations are equipped '
        'during a supplied qualifying long rest at an earlier attained Warrior level. Earlier feat choices are '
        'spent on distinct Alert, Alertness and Lucky grants as needed. Both the feat ID and its explicit class '
        'alias purchase the same single identity. Replaying payment or buying the alias again fails without '
        'spending the later opportunity. Actual campaign advancement/rest records remain scenario premises.', '',
        '| Feat | Warrior milestone used | Mutations equipped by level | Equipped source profiles |',
        '|---|---:|---:|---|',
    ]
    for row in executed:
        notes.append(f'| {by_id[row["featId"]]["name"]} | {row["classLevel"]} | {row["equippedAtLevel"]} | '
                     + ', '.join(profiles[sid]['name'] for sid in row['equipped'])+' |')
    notes += ['',
        'These milestones describe the supplied history, where earlier choices were already spent. They are '
        'not a new rule about retaining opportunities or a claim that no separately authorized feat grant '
        'could permit an earlier acquisition.', '',
        'Bio-Stabilizer can be acquired with Bloodthick equipped at Warrior 4, but its two-active mutation '
        'component is unavailable with only one slot. The level-5 example uses the actual selected Mutation '
        'Efficiency and two serum injections on different regular turns, spends both doses and gains ordinary '
        'Strain; the first mutation’s expiry disables that component. A missing Efficiency selection cannot '
        'be supplied by merely reaching level 3.', '',
        'Living Fortress requires three equipped Vital mutations. Warrior 8 cannot supply a third slot; '
        'Warrior 13 can meet the equipment predicate. The example spends the ordinary level-16 feat choice. '
        'Three equipped mutations remain distinct from three active mutations. The bounded level-20 sequence '
        'uses actually acquired Apex Form, spends its Bonus Action/once-per-encounter entitlement and loses '
        'the three-active component when that activation expires. It does not use a bare exception boolean.', '',
        'These activation checks do not execute the feats’ full combat triggers, target eligibility, damage, '
        'healing, death or hostile-threat procedures. They assume the actor can act and the supplied rest was '
        'qualifying. The activation projection deliberately excludes modified Strain, concurrent serum/Apex '
        'duration arbitration and other activation routes.', '',
        '**Separate pending source issue:** FEAT327-ACQ-02 asks actual GPT to resolve global versus per-tree '
        'Advanced tier limits and the precise concurrency distinction. Every positive acquisition here fits '
        'both readings; neither is adopted by this report. The original source/class files remain unchanged.', '',
        'The 209 numeric-only predicate cohort is separate. There are 114 other credential-dependent '
        'identities beyond these twelve; complete acquisitions and use-time cases across the full catalog '
        'remain open. No candidate promotion, source deletion, GitHub push or cosmology review occurred.', '']
    with args.report.open('x', encoding='utf-8', newline='\n') as stream:
        json.dump(result, stream, ensure_ascii=False, indent=2)
        stream.write('\n')
    with args.notes.open('x', encoding='utf-8', newline='\n') as stream:
        stream.write('\n'.join(notes))
    print(json.dumps({'report': info(args.report), 'notes': info(args.notes),
                      'checks': len(checks), 'failures': len(failures),
                      'checkKinds': result['checkKinds'], 'mutationFeatCount': 12}, indent=2))
    if failures:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
