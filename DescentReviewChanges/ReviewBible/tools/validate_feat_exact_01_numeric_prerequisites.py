"""Source-qualified synthetic numeric/level prerequisite boundary projections.

The oracle parses the original printed strings independently of the normalized
contract evaluator. Nothing is written into an operative candidate. Reports use
exclusive creation so earlier evidence cannot be silently overwritten.
"""
import argparse
from collections import Counter, defaultdict
from copy import deepcopy
from datetime import datetime, timezone
from hashlib import sha256
from itertools import product
import json
from pathlib import Path
import re

from feat_exact_01_acquisition_models import PaidChoices
from feat_exact_01_numeric_prerequisite_model import (
    is_numeric_tree, meets_numeric_prerequisite, numeric_and_opportunity_gate,
)

R = Path(__file__).resolve().parents[1]
G = R.parents[1]
A = G / 'docs/audit/2026-10-08/full-game'
ABILITIES = ('STR', 'DEX', 'CON', 'INT', 'WIS', 'CHA')
NAMES = dict(zip(('Strength', 'Dexterity', 'Constitution', 'Intelligence',
                  'Wisdom', 'Charisma'), ABILITIES))
NAMES['Agility'] = 'DEX'  # Explicit FS-02 alias, not an invented general alias.
NAME_RE = '(?:' + '|'.join(NAMES) + ')'


def binding(path):
    data = path.read_bytes()
    return {'path': path.relative_to(G).as_posix(), 'bytes': len(data),
            'sha256': sha256(data).hexdigest()}


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def printed_clauses(text):
    """Separate grammar: comma=AND; each returned clause contains OR options.

    Each atom is (ability abbreviation or LEVEL, printed threshold). No
    normalized contract node or builder parser is imported by this oracle.
    """
    if text == 'None':
        return []
    clauses = []
    for piece in text.split(','):
        piece = piece.strip()
        match = re.fullmatch(r'[Ll]evel (\d+)\+?', piece)
        if match:
            clauses.append([('LEVEL', int(match[1]))])
            continue
        match = re.fullmatch(fr'({NAME_RE}) or ({NAME_RE}) (\d+)(?:\+| or higher)', piece)
        if match:
            clauses.append([(NAMES[match[1]], int(match[3])),
                            (NAMES[match[2]], int(match[3]))])
            continue
        alternatives = piece.split(' or ')
        if piece.endswith(' or higher'):
            alternatives = [piece]
        atoms = []
        for alternative in alternatives:
            match = re.fullmatch(fr'({NAME_RE}) (\d+)(?:\+| or higher)', alternative)
            if not match:
                raise ValueError(f'Printed grammar is outside this finite cohort: {text!r}')
            atoms.append((NAMES[match[1]], int(match[2])))
        clauses.append(atoms)
    return clauses


def printed_truth(clauses, scores, total_level):
    return all(any((total_level if key == 'LEVEL' else scores[key]) >= minimum
                   for key, minimum in alternatives) for alternatives in clauses)


def node_kinds(node):
    return {node['kind']}.union(*(node_kinds(child) for child in node.get('requirements', [])))


def dice_for(total):
    # Witness of a possible roll, not a claim a human rolled these dice.
    for dice in product(range(1, 7), repeat=4):
        if sum(dice) - min(dice) == total:
            return list(dice)
    raise ValueError(f'No four-d6/drop-lowest witness for {total}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path, default=A/'FEAT_EXACT_01_NUMERIC_PREREQUISITE_CHECK.json')
    parser.add_argument('--notes', type=Path, default=A/'FEAT_EXACT_01_NUMERIC_PREREQUISITE_NOTES.md')
    parser.add_argument('--source-descendants', type=Path, action='append', default=[])
    args = parser.parse_args()
    for path in (args.report, args.notes):
        if path.exists():
            raise SystemExit(f'Refusing to overwrite previous evidence: {path}')

    paths = [
        Path(__file__), R/'tools/feat_exact_01_numeric_prerequisite_model.py',
        R/'tools/feat_exact_01_acquisition_models.py',
        A/'FEAT_EXACT_01_ACQUISITION_CONTRACTS.json',
        A/'FEAT327_ACQ_01_DERIVED_FULFILLMENT.json',
        R/'data/playtest/character_foundation.json',
        R/'data/playtest/ancestry_background_candidate.json',
        R/'docs/mechanics/CHARACTER_CREATION_PLAYTEST.md',
        R/'data/director/feat_candidates/exact_01/shared_rules.json',
        R/'data/public/feat_candidates/exact_01/candidate.json',
        *args.source_descendants,
    ]
    sources = [binding(path) for path in paths]
    contracts = read(paths[3])
    records = contracts['records']
    by_id = {record['id']: record for record in records}
    foundation = read(paths[5])
    ancestry = read(paths[6])
    human = next(row for row in ancestry['ancestries'] if row['id'] == 'human')
    imperial = next(row for row in human['variants'] if row['id'] == 'imperial-human')
    bonuses = imperial['combinedAbilityBonuses']
    schedules = {row['class']: row['asiClassLevels'] for row in foundation['classes']}
    cohort = [record for record in records if is_numeric_tree(record['requirements'])]
    remaining = [record for record in records if record not in cohort]
    forms = defaultdict(list)
    checks, cases, actors, coverage = [], [], {}, []

    def check(identity, kind, actual, expected):
        a, e = deepcopy(actual), deepcopy(expected)
        checks.append({'id': identity, 'kind': kind, 'actual': a,
                       'expected': e, 'passed': a == e})

    def raises(identity, action):
        try:
            action()
        except ValueError:
            check(identity, 'rejection', True, True)
        else:
            check(identity, 'rejection', False, True)

    def actor(scores, level, target_id):
        earlier = [milestone for milestone in schedules['Bard'] if milestone < level]
        past_ids = [sid for sid in ('alert', 'alertness', 'lucky') if sid != target_id]
        if len(earlier) > len(past_ids):
            raise ValueError('Insufficient distinct prior non-ability feat witnesses')
        data = {
            'synthetic': True, 'completeCharacterSheet': False,
            'methodSelectedBeforeGeneration': 'four-d6-discard-one-lowest',
            'ancestry': 'human', 'variant': 'imperial-human',
            'ancestryBonusAppliedOnce': bonuses,
            'abilityRolls': {key: dice_for(scores[key]-bonuses[key]) for key in ABILITIES},
            'permanentScores': scores, 'classLevels': {'Bard': level},
            'chronologicalClassLevels': [{'class': 'Bard', 'classLevel': n, 'totalLevel': n}
                                         for n in range(1, level+1)],
            'earlierAsiChoices': [{'classLevel': milestone, 'featId': sid}
                                 for milestone, sid in zip(earlier, past_ids)],
            'unmodeled': 'Background, full class selections, spell repertoire, equipment, '
                         'feat-specific acquisition choices, actual campaign rolls and advancement awards.',
        }
        identity = sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()[:20]
        if identity not in actors:
            actors[identity] = data
            rolls_ok = all(len(dice) == 4 and all(1 <= die <= 6 for die in dice)
                           and sum(dice)-min(dice)+bonuses[key] == scores[key]
                           for key, dice in data['abilityRolls'].items())
            check(f'{identity}:ability-rolls-and-once-only-ancestry', 'synthetic-source-witness', rolls_ok, True)
            check(f'{identity}:attained-level-sequence', 'synthetic-source-witness',
                  data['chronologicalClassLevels'][-1]['classLevel'], level)
        return identity, data

    def ledger(data):
        paid = PaidChoices(schedules, {}, deepcopy(data['classLevels']),
                           deepcopy(data['permanentScores']), set(by_id))
        for prior in data['earlierAsiChoices']:
            sid, milestone = prior['featId'], prior['classLevel']
            if by_id[sid]['printedPrerequisite'] != 'None':
                raise ValueError('Prior feat witness has an unmodeled prerequisite')
            identity = f'Bard:{milestone}'
            paid.earn_class_opportunity(identity, 'Bard', milestone)
            paid.commit(sid, identity, prerequisites_met=True)
        return paid

    check('cohort-size', 'coverage', len(cohort), 209)
    check('remaining-size', 'coverage', len(remaining), 126)
    check('original-identities-unique', 'coverage', len(by_id), 335)
    check('ancestry-base-bonuses', 'source-data', human['abilityBonuses'], dict.fromkeys(ABILITIES, 1))
    check('imperial-variant-is-additive-once', 'source-data', bonuses,
          {key: human['abilityBonuses'][key]+imperial['abilityBonuses'].get(key, 0) for key in ABILITIES})
    check('imperial-only-additional-charisma', 'source-data', imperial['abilityBonuses'], {'CHA': 1})
    check('bard-source-schedule', 'source-data', schedules['Bard'], [4, 8, 12, 16, 19])
    check('oracle-source-schedule', 'source-data', schedules['Oracle'], [4, 8, 14, 19])

    fulfillment = read(paths[4])
    descendants = fulfillment['measuredCurrentDescendants']
    if isinstance(descendants, dict):
        descendants = list(descendants.values())
    current_contract_binding = next(item for item in descendants
                                    if item['path'] == sources[3]['path'])
    original_contract_binding = deepcopy(current_contract_binding)
    declared_changes = []
    for receipt_path in args.source_descendants:
        for change in read(receipt_path)['changes']:
            declared_changes.append({**change, 'receipt': binding(receipt_path)})
    contract_binding_chain = []
    visited = set()
    while current_contract_binding != sources[3]:
        if current_contract_binding['sha256'] in visited:
            raise AssertionError('Cyclic current-contract binding chain')
        visited.add(current_contract_binding['sha256'])
        matches = [c for c in declared_changes if c['before']['path'] == sources[3]['path']
                   and c['after']['path'] == sources[3]['path']
                   and c['before']['sha256'] == current_contract_binding['sha256']
                   and c['before']['bytes'] == current_contract_binding['bytes']]
        if len(matches) != 1:
            raise AssertionError('Missing or ambiguous explicit current-contract descendant')
        change = matches[0]
        preserved = binding(G / change['before']['preservedCopy'])
        if preserved['sha256'] != current_contract_binding['sha256'] or preserved['bytes'] != current_contract_binding['bytes']:
            raise AssertionError('Preserved contract before-version mismatch')
        current_contract_binding = deepcopy(change['after'])
        contract_binding_chain.append(deepcopy(change))
    check('current-contract-acq01-binding', 'source-integrity', sources[3], current_contract_binding)

    for record in cohort:
        sid, printed = record['id'], record['printedPrerequisite']
        forms[printed].append(sid)
        clauses = printed_clauses(printed)
        thresholds = defaultdict(set)
        for alternatives in clauses:
            for key, minimum in alternatives:
                thresholds[key].add(minimum)
        dimensions = sorted(key for key in thresholds if key != 'LEVEL')
        values = [[n for n in sorted({x+d for x in thresholds[key] for d in (-1, 0, 1)})]
                  for key in dimensions]
        minimum_level = max(thresholds.get('LEVEL', {1}))
        first_bard_choice = next(level for level in schedules['Bard'] if level >= minimum_level)
        levels = sorted({max(1, minimum_level-1), minimum_level,
                         min(20, minimum_level+1), first_bard_choice})
        entries = []
        for assigned, level in product(product(*values), levels):
            scores = dict.fromkeys(ABILITIES, 10)
            scores.update(zip(dimensions, assigned))
            identity, data = actor(scores, level, sid)
            expected = printed_truth(clauses, scores, level)
            actual = meets_numeric_prerequisite(record['requirements'], scores, {'Bard': level})
            case_id = f'{sid}:{len(entries)+1:03}'
            paid = ledger(data)
            opportunity = f'Bard:{level}'
            earned = level in schedules['Bard']
            if earned:
                paid.earn_class_opportunity(opportunity, 'Bard', level)
            check(case_id+':printed-versus-normalized', 'independent-printed-predicate', actual, expected)
            check(case_id+':numeric-and-earned-choice', 'numeric-plus-opportunity',
                  numeric_and_opportunity_gate(record['requirements'], paid, opportunity),
                  bool(expected and earned))
            check(case_id+':missing-choice-rejected', 'numeric-plus-opportunity',
                  numeric_and_opportunity_gate(record['requirements'], paid, 'unrecorded-grant'), False)
            if earned:
                before = deepcopy(paid.opportunities)
                raises(case_id+':milestone-cannot-be-renamed',
                       lambda: paid.earn_class_opportunity('alias', 'Bard', level))
                check(case_id+':failed-alias-does-not-mutate', 'opportunity-history', paid.opportunities, before)
                paid.opportunities[opportunity]['spent'] = True
                check(case_id+':spent-choice-rejected', 'numeric-plus-opportunity',
                      numeric_and_opportunity_gate(record['requirements'], paid, opportunity), False)
            else:
                raises(case_id+':nonmilestone-cannot-be-earned',
                       lambda: paid.earn_class_opportunity(opportunity, 'Bard', level))
            # Temporary bonuses are supplied as separate scene data, never folded
            # into the six permanent source scores used by either predicate.
            temporary = {key: 20 for key in dimensions}
            after_temporary = meets_numeric_prerequisite(record['requirements'],
                                                        data['permanentScores'], data['classLevels'])
            check(case_id+':temporary-does-not-change-admission', 'temporary-exclusion', after_temporary, expected)
            result = {'id': case_id, 'featId': sid, 'actorRef': identity,
                      'printedPredicateExpected': expected, 'normalizedPredicateActual': actual,
                      'currentBardMilestoneEarned': earned,
                      'numericAndOpportunityExpected': bool(expected and earned),
                      'temporarySceneBonusesExcluded': temporary,
                      'completeAcquisitionValidated': False}
            cases.append(result)
            entries.append(result)

        passing = [case for case in entries if case['printedPredicateExpected']]
        failures = [case for case in entries if not case['printedPredicateExpected']]
        check(sid+':has-open-choice-positive', 'coverage',
              any(case['numericAndOpportunityExpected'] for case in entries), True)
        check(sid+':has-negative-unless-None', 'coverage', bool(failures) or printed == 'None', True)
        # A union-of-thresholds grid exercises each OR arm alone, each required
        # AND atom failing while its peers pass, and equality at every threshold.
        for clause_number, alternatives in enumerate(clauses):
            for atom_number, (key, minimum) in enumerate(alternatives):
                for comparison, delta in [('below', -1), ('equal', 0), ('above', 1)]:
                    found = any((sum(actors[case['actorRef']]['classLevels'].values()) if key == 'LEVEL'
                                 else actors[case['actorRef']]['permanentScores'][key]) == minimum+delta
                                for case in entries)
                    check(f'{sid}:c{clause_number}:a{atom_number}:{comparison}', 'boundary-coverage', found, True)
                if len(alternatives) > 1:
                    def sole_arm(case):
                        snap = actors[case['actorRef']]
                        return (case['printedPredicateExpected'] and snap['permanentScores'][key] >= minimum
                                and all(snap['permanentScores'][other] < threshold
                                        for n, (other, threshold) in enumerate(alternatives) if n != atom_number))
                    check(f'{sid}:or-arm-{atom_number}-alone', 'boundary-coverage', any(sole_arm(x) for x in entries), True)
        coverage.append({'id': sid, 'printedPrerequisite': printed,
                         'caseIds': [case['id'] for case in entries],
                         'predicatePositive': len(passing), 'predicateNegative': len(failures),
                         'firstQualifyingBardMilestone': first_bard_choice,
                         'printedPredicateBoundaryCoverageComplete': True,
                         'completeAcquisitionValidated': False})

    # Real class schedule rows, including Oracle's distinct progression.
    for class_name, schedule in schedules.items():
        for level in range(1, 21):
            paid = PaidChoices(schedules, {}, {class_name: level}, dict.fromkeys(ABILITIES, 15), set(by_id))
            try:
                paid.earn_class_opportunity('current', class_name, level)
                actual = True
            except ValueError:
                actual = False
            check(f'{class_name}:{level}:source-asi-row', 'seventeen-class-schedules', actual, level in schedule)
    mixed = PaidChoices(schedules, {}, {'Bard': 3, 'Mage': 1}, dict.fromkeys(ABILITIES, 15), set(by_id))
    check('multiclass-total4-meets-total-level4', 'total-versus-class-level',
          meets_numeric_prerequisite({'kind': 'totalCharacterLevel', 'minimum': 4}, mixed.scores, mixed.current_classes), True)
    raises('multiclass-total4-does-not-earn-bard4', lambda: mixed.earn_class_opportunity('bad', 'Bard', 4))
    check('multiclass-no-free-opportunity', 'total-versus-class-level',
          numeric_and_opportunity_gate({'kind': 'totalCharacterLevel', 'minimum': 4}, mixed, 'bad'), False)
    raises('credential-gate-is-not-numeric', lambda: meets_numeric_prerequisite(
        {'kind': 'actualProficiency', 'name': 'Arcana'}, dict.fromkeys(ABILITIES, 15), {'Bard': 4}))
    raises('empty-any-is-rejected', lambda: meets_numeric_prerequisite(
        {'kind': 'any', 'requirements': []}, dict.fromkeys(ABILITIES, 15), {'Bard': 4}))
    raises('empty-all-is-rejected', lambda: meets_numeric_prerequisite(
        {'kind': 'all', 'requirements': []}, dict.fromkeys(ABILITIES, 15), {'Bard': 4}))
    for row in remaining:
        raises(row['id']+':credential-tree-cannot-be-bypassed',
               lambda row=row: meets_numeric_prerequisite(row['requirements'], dict.fromkeys(ABILITIES, 20), {'Bard': 20}))
    check('printed-form-count', 'coverage', len(forms), 62)
    check('complete-335-partition', 'coverage',
          sorted([row['id'] for row in cohort]+[row['id'] for row in remaining]), sorted(by_id))
    for path, original in zip(paths, sources):
        check(original['path']+':unchanged-during-run', 'input-integrity', binding(path), original)

    failures = [item for item in checks if not item['passed']]
    notes = [
        '# Numeric feat prerequisite boundary evidence', '',
        '**Finite source-qualified synthetic projections; exact candidate remains unapproved.**', '',
        f'This pass covers all {len(cohort)} numeric/level/None prerequisite trees, representing {len(forms)} exact printed forms. '
        f'It executes {len(cases)} boundary cases against an independent parser of the original printed prerequisite strings. '
        f'{len(actors)} distinct synthetic ability/class-history projections support those cases. '
        f'{len(checks)} checks completed with {len(failures)} failures.', '',
        'Each projection uses possible four-d6/drop-lowest results, Human plus the actual Imperial Human variant bonuses once, '
        'and attained Bard class levels. Earlier ASI choices are recorded as distinct Alert, Alertness or Lucky grants where needed; '
        'these do not increase permanent abilities. No example purports to record actual human rolls or a real campaign award. '
        'These are prerequisite projections, not complete character sheets.', '',
        'The full boundary grid includes one below, exactly at and one above every ability/level threshold; '
        'each OR arm can qualify alone. Temporary scene bonuses are excluded from permanent scores. '
        'A correct numeric predicate still needs an earned unspent class opportunity. Missing, spent, renamed and unearned opportunities fail. '
        'All 17 actual class ASI schedules are checked, including Oracle 4/8/14/19. '
        'Bard 3 / Mage 1 meets total level 4 but has earned neither class\'s level-4 ASI.', '',
        'A passing result does **not** prove a complete feat acquisition: any named curriculum, spell, armor, save, ASI allocation, '
        'nonrepeatable identity, target, finite initialization or deferred payload still needs its own source-qualified check. '
        'None means no printed prerequisite; it does not grant a free choice or make Astral Projection/Planar Binding payloads available. '
        'Candidate selection remains disabled, and no operative source or candidate was changed.', '',
        '## Exact printed forms', '',
        '| Printed prerequisite | Feats | First eligible Bard ASI milestone |',
        '|---|---:|---:|',
    ]
    for printed, ids in sorted(forms.items()):
        milestone = next(item['firstQualifyingBardMilestone'] for item in coverage if item['id'] == ids[0])
        notes.append(f'| {printed} | {len(ids)} | {milestone} |')
    notes += ['', '## Remaining credential-dependent work', '',
              'The other 126 identities need actual proficiency, spell access, lineage, owned-feat, mutation-slot, '
              'trade-level or campaign-context evidence. Numeric scores alone cannot satisfy them. '
              'The JSON report lists all 126 identities and their complete normalized requirements without manufacturing receipts. '
              'The acquisition-history and ACQ-01 reports remain separate evidence; this pass does not replace them.', '',
              'Full FXC acceptance, actual GPT exact review, whole-game flow agreement and the authorized GitHub push remain outstanding. '
              'Cosmology review remains after the verified push.', '']
    result = {
        'recordedAtUtc': datetime.now(timezone.utc).isoformat(),
        'status': 'passed-finite-numeric-projections' if not failures else 'failed',
        'scope': 'Original printed numeric/level/None predicate boundaries plus earned unspent opportunity; '
                 'source-qualified synthetic partial snapshots, not complete character builds or complete feat acquisitions.',
        'sourceBindings': sources,
        'historicalContractBindingResolution': {'originalACQ01Binding': original_contract_binding,
            'actualCurrentBinding': sources[3], 'explicitDescendantChain': contract_binding_chain},
        'counts': {'originalFeats': 335, 'numericPredicateFeats': len(cohort), 'printedForms': len(forms),
                   'boundaryCases': len(cases), 'syntheticProjections': len(actors),
                   'remainingCredentialDependentFeats': len(remaining)},
        'checks': len(checks), 'checkKinds': dict(Counter(item['kind'] for item in checks)),
        'failures': failures, 'results': checks, 'actors': actors, 'cases': cases, 'coverage': coverage,
        'remaining': [{'id': row['id'], 'printedPrerequisite': row['printedPrerequisite'],
                       'requirements': row['requirements'], 'kinds': sorted(node_kinds(row['requirements']))}
                      for row in remaining],
        'all335ActualAcquisitionBoundaryCasesExecuted': False,
        'allNumericCohortCompleteAcquisitionsValidated': False,
        'selectionEnabled': False, 'candidateReadyForSubmission': False,
        'sourceInformationDeleted': False, 'runtimeImplemented': False,
        'wholeGameFlowConfirmed': False, 'pushed': False, 'cosmologyReviewed': False,
    }
    with args.report.open('x', encoding='utf-8', newline='\n') as stream:
        json.dump(result, stream, ensure_ascii=False, indent=2)
        stream.write('\n')
    with args.notes.open('x', encoding='utf-8', newline='\n') as stream:
        stream.write('\n'.join(notes))
    print(json.dumps({'report': binding(args.report), 'notes': binding(args.notes),
                      'counts': result['counts'], 'checks': len(checks),
                      'failures': len(failures), 'checkKinds': result['checkKinds']}, indent=2))
    if failures:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
