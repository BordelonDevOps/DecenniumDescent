"""Validate all current ancestry variants against thirteen literal feat gates.

Complete source objects/procedures and missing legacy-branch limitations are
retained. This does not claim full acquisitions or execute racial feat effects.
"""
import argparse
from collections import Counter
from copy import deepcopy
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import re

from feat_exact_01_lineage_prerequisite_model import LineagePrerequisites, TARGETS

R = Path(__file__).resolve().parents[1]
G = R.parents[1]
A = G / 'docs/audit/2026-10-08/full-game'


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def binding(path):
    data = path.read_bytes()
    return {'path': path.relative_to(G).as_posix(), 'bytes': len(data), 'sha256': sha256(data).hexdigest()}


def serial(value):
    if isinstance(value, set):
        return sorted(value)
    raise TypeError(type(value).__name__)


def printed_lineages(text):
    """Read original printed literal alternatives independently of normalized nodes."""
    text = text.casefold()
    if text.endswith(' heritage'):
        return {text[:-9]}
    if text not in {'elf or half-elf', 'half-orc or orc', 'half-elf, half-orc, or human'}:
        raise ValueError('Printed prerequisite outside this finite lineage grammar')
    return {part.strip() for part in re.split(r',\s*(?:or\s+)?|\s+or\s+', text)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path, default=A / 'FEAT_EXACT_01_LINEAGE_PREREQUISITE_CHECK.json')
    parser.add_argument('--notes', type=Path, default=A / 'FEAT_EXACT_01_LINEAGE_PREREQUISITE_NOTES.md')
    args = parser.parse_args()
    assert not args.report.exists() and not args.notes.exists(), 'Refusing to overwrite previous evidence'
    paths = [Path(__file__), R / 'tools/feat_exact_01_lineage_prerequisite_model.py',
        R / 'tools/feat_exact_01_acquisition_models.py', A / 'FEAT_EXACT_01_ACQUISITION_CONTRACTS.json',
        R / 'data/playtest/ancestry_background_candidate.json', R / 'data/playtest/character_foundation.json',
        R / 'docs/mechanics/CHARACTER_CREATION_PLAYTEST.md',
        R / 'data/public/feat_candidates/exact_01/candidate.json',
        R / 'data/public/feat_candidates/exact_01/shared_rules.json',
        A / 'FEAT_EXACT_01_OWNED_FEAT_CHAIN_CHECK.json',
        A / 'FEAT327_FXC05_TRAINING_OWNERSHIP_REVIEW_RECEIPT.json',
        A / 'FEAT_EXACT_01_REMAINING_CREDENTIAL_SOURCE_PLAN.json']
    sources = [binding(path) for path in paths]
    contracts = {row['id']: row for row in read(paths[3])['records']}
    ancestry = read(paths[4]); foundation = read(paths[5])
    classes = {row['class']: row for row in foundation['classes']}
    previous = read(paths[9]); candidate = read(paths[7])
    result = []; histories = []

    def check(name, passed, kind='bounded-behavior', **detail):
        result.append({'id': name, 'kind': kind, 'passed': bool(passed), **detail})
        if not passed:
            raise AssertionError(name)

    def reject(name, operation):
        try:
            operation()
        except ValueError as exc:
            check(name, True, 'rejection', reason=str(exc))
        else:
            check(name, False, 'rejection')

    remaining_before = {row['id'] for row in previous['remaining']}
    check('disjoint-new-thirteen', len(TARGETS) == 13 and TARGETS <= remaining_before, 'coverage')
    check('source-roster', len(ancestry['ancestries']) == 14 and sum(len(x['variants']) for x in ancestry['ancestries']) == 45, 'source-data')
    check('no-source-legacy-alias', not {'Dragonborn', 'Half-elf', 'Half-orc'} & {x['name'] for x in ancestry['ancestries']}, 'source-data')
    check('no-current-sorcerer-class', 'Sorcerer' not in classes and 'Mage' in classes and len(classes) == 17, 'source-data')
    check('warrior-actual-opportunities', classes['Warrior']['asiClassLevels'] == [4, 8, 12, 16, 19], 'source-data')
    check('alert-spend-control-has-no-prerequisite', contracts['alert']['printedPrerequisite'] == 'None', 'source-data')
    candidate_records = candidate['feats']
    candidate_by_id = {row['id']: row for row in candidate_records}
    for sid in sorted(TARGETS | {'dragon_blood'}):
        row = contracts[sid]
        check(sid + '/printed-original', row['printedPrerequisite'] == row['originalObject']['prerequisite'], 'source-integrity')
        check(sid + '/full-original', row['originalObject'] == candidate_by_id[sid]['sourceObject'], 'source-integrity')
        check(sid + '/full-procedure', row['completeOperativeProcedure'] == candidate_by_id[sid]['operationalRules'], 'source-integrity')
    qualification_matrix = []
    for base in ancestry['ancestries']:
        for variant in base['variants']:
            expected_bonuses = dict(base['abilityBonuses'])
            for key, value in variant['abilityBonuses'].items():
                expected_bonuses[key] = expected_bonuses.get(key, 0) + value
            check(variant['id'] + '/combined-bonuses-source', expected_bonuses == variant['combinedAbilityBonuses'], 'source-data')
            actor = {'ancestryId': base['id'], 'variantId': variant['id'], 'classLevels': {'Warrior': 4},
                     'abilityRolls': {key: [1, 4, 4, 4] for key in ['STR', 'DEX', 'CON', 'INT', 'WIS', 'CHA']},
                     'permanentScores': {key: 12 + variant['combinedAbilityBonuses'].get(key, 0) for key in ['STR', 'DEX', 'CON', 'INT', 'WIS', 'CHA']},
                     'syntheticWitness': True}
            projection = LineagePrerequisites(actor, ancestry, classes, contracts)
            history = {'id': variant['id'], 'beforeOpportunity': projection.snapshot()}
            expected = {sid: base['name'].casefold() in printed_lineages(contracts[sid]['printedPrerequisite']) for sid in sorted(TARGETS)}
            for sid, truth in expected.items():
                check(variant['id'] + '/' + sid + '/literal-predicate', projection.prerequisite(sid) == truth,
                      expected=truth, sourceLineage=base['name'])
                check(variant['id'] + '/' + sid + '/unearned', not projection.earned_gate(sid, 'Warrior:4'), 'paid-opportunity')
            projection.earn(4)
            for sid, truth in expected.items():
                check(variant['id'] + '/' + sid + '/earned', projection.earned_gate(sid, 'Warrior:4') == truth, 'paid-opportunity')
            history['earnedOpportunity'] = projection.snapshot()
            # A legal earlier Alert spends the opportunity. Target feats, especially
            # Prodigy with further selections, are never committed from lineage alone.
            projection.pay.commit('alert', 'Warrior:4', prerequisites_met=True)
            for sid in sorted(TARGETS):
                check(variant['id'] + '/' + sid + '/spent', not projection.earned_gate(sid, 'Warrior:4'), 'paid-opportunity')
            history['afterActualAlertPurchase'] = projection.snapshot()
            projection.advance(8); projection.earn(8)
            for sid, truth in expected.items():
                check(variant['id'] + '/' + sid + '/later-earned', projection.earned_gate(sid, 'Warrior:8') == truth, 'paid-opportunity')
            history['laterOpportunity'] = projection.snapshot()
            histories.append(history)
            qualification_matrix.append({'ancestryId': base['id'], 'variantId': variant['id'], 'qualifiedFeatIds': [s for s, value in expected.items() if value]})
            check(variant['id'] + '/no-target-granted', not any(projection.pay.has(sid) for sid in TARGETS), 'bounded-behavior')
            check(variant['id'] + '/no-legacy-credential', not any(projection.has_lineage(name) for name in ['Dragonborn', 'Half-elf', 'Half-orc']), 'bounded-behavior')
    template = deepcopy(histories[0]['beforeOpportunity']['actor'])
    for name in ['dragonborn', 'half-elf', 'half-orc']:
        bad = deepcopy(template); bad['ancestryId'] = name
        reject('unsupported-current-ancestry/' + name, lambda b=bad: LineagePrerequisites(b, ancestry, classes, contracts))
    bad = deepcopy(template); bad['variantId'] = 'high-elf'
    reject('variant-from-another-ancestry', lambda: LineagePrerequisites(bad, ancestry, classes, contracts))
    bad_score = deepcopy(template); bad_score['permanentScores']['CON'] += 2
    reject('ancestry-bonus-not-applied-twice', lambda: LineagePrerequisites(bad_score, ancestry, classes, contracts))
    spoof = deepcopy(template)
    spoof.update({'displayName': 'Half-elf Dragonborn Orc', 'lineageAliases': ['Elf', 'Orc', 'Human'],
                  'temporaryForm': 'Elf', 'classFeatures': ['Fey Ancestry'], 'claimedLegacyReceipt': True})
    projection = LineagePrerequisites(spoof, ancestry, classes, contracts)
    check('unearned-labels-do-not-alias', not any(projection.prerequisite(sid) for sid in ['elvenAccuracy', 'orcish_fury', 'prodigy']), 'rejection')
    reject('dragon-blood-not-claimed-as-covered', lambda: projection.prerequisite('dragon_blood'))
    reject('unattained-opportunity', lambda: projection.earn(8))
    reject('non-asi-opportunity', lambda: projection.earn(3))
    remaining = [row for row in previous['remaining'] if row['id'] not in TARGETS]
    check('remaining-forty-three', len(remaining) == 43 and any(x['id'] == 'dragon_blood' for x in remaining), 'coverage')
    for old, path in zip(sources, paths):
        check('unchanged/' + old['path'], binding(path) == old, 'source-integrity')
    report = {
        'createdAtUtc': datetime.now(timezone.utc).isoformat(), 'status': 'passed-current-lineage-prerequisite-projections',
        'scope': 'All45 current ancestry variants against13 literal lineage predicate identities and genuine earned/unspent class opportunities. No target feat is acquired from this necessary gate alone; full selections, effects, class builds and campaign lineage authentication remain outside this pass.',
        'sourceBindings': sources, 'cohort': sorted(TARGETS),
        'completeSourceContracts': [contracts[sid] for sid in sorted(TARGETS)],
        'excludedDragonBloodContract': contracts['dragon_blood'], 'completeAncestrySources': ancestry['ancestries'],
        'fullWarriorFoundationSource': classes['Warrior'], 'spentOpportunityControl': contracts['alert'],
        'counts': {'lineagePredicateIdentities': 13, 'currentAncestries': 14, 'currentVariants': 45,
                   'predicatePairs': 45 * 13, 'sourceQualifiedHistories': len(histories),
                   'priorNumericIdentities': 209, 'priorWarriorIdentities': 12, 'priorTrainingIdentities': 48,
                   'priorOwnedFeatIdentities': 10, 'remainingCredentialDependentIdentities': len(remaining)},
        'qualificationMatrix': qualification_matrix, 'histories': histories,
        'checks': len(result), 'checkKinds': dict(Counter(x['kind'] for x in result)), 'failures': [], 'results': result,
        'remaining': remaining,
        'limits': [
            'Each record is a source-qualified synthetic ancestry/ability/class projection; no real campaign ancestry, roll or advancement is authenticated.',
            'All source variants are checked using their actual ancestry identity. Variant names, physical resemblance, borrowed traits, temporary forms and cosmetic labels do not establish a different lineage.',
            'Half-elf, Half-orc and Dragonborn are absent from these current sources. No positive legacy receipt is supplied or invented; a genuinely authorized legacy character may have a lawful alternate branch outside this projection.',
            'Dragon Blood stays among43 remaining identities: Drakari is not silently Dragonborn; neither Mage nor Magic Initiate(Sorcerer) supplies a Sorcerer class or draconic-bloodline receipt. Its recorded damage-type requirement remains mandatory.',
            'Prodigy still needs its ordered new skill, new tool, eligible language and skill Expertise choices with actual duplicate/exhaustion, trade initialization and language gates. A lineage match does not waive them.',
            'Other named feat uses need their complete source actions, clocks, costs, attacks, conditions, physical objects, variant-specific tasks and actual donor/encounter facts. None is executed here.',
            'Only the ordinary Alert control is purchased to prove spent opportunity rejection. No target feat or its benefits are granted by the lineage-and-opportunity gate.',
            'This extends partial predicate coverage from279 to292 identities, not292 completed acquisitions or approved feats. Source rules and live selection remain unchanged.',
        ],
        'allCohortCompleteAcquisitionsValidated': False, 'candidateReadyForSubmission': False,
        'newRulesAdopted': False, 'sourceInformationDeleted': False, 'cosmologyReviewed': False,
    }
    with args.report.open('x', encoding='utf-8', newline='\n') as stream:
        json.dump(report, stream, ensure_ascii=False, indent=2, default=serial); stream.write('\n')
    notes = (
        '# Current lineage prerequisite projections\n\n'
        f'{len(result)} checks pass across45 current variants,14 ancestries and585 variant/feat pairs for13 lineage prerequisite identities. '
        'The independent expected result reads the original printed lineage strings; the evaluated result reads the normalized prerequisite trees. '
        'All45 synthetic histories verify unearned, earned, spent and later earned Warrior opportunities using the actual class schedule.\n\n'
        'Combined ancestry/variant ability bonuses apply once to six explicit four-d6/drop-lowest witnesses. The full ancestry objects and feat procedures are retained in the report. '
        'A valid source ancestry/variant pair establishes only its own literal lineage; labels and temporary forms do not substitute.\n\n'
        'These are necessary prerequisite/payment gates. No target feat is granted, and no complete character or feat-use sequence is claimed. '
        'Prodigy especially still requires its ordered skill/tool/language/Expertise choices and their separate source gates.\n\n'
        'Half-elf, Half-orc and Dragonborn positive legacy receipts are unavailable in this current-source slice. Those names are preserved as genuine potential alternatives, not erased or aliased. '
        'Dragon Blood remains unresolved here: Drakari is not Dragonborn, and a feat curriculum is not an actual Sorcerer/draconic-bloodline grant.\n\n'
        'The disjoint predicate bookkeeping is209 numeric +12 Warrior +48 training +10 owned-feat +13 current-lineage =292;43 other credential identities remain. '
        'This is not292 complete acquisitions or approved feats. Actual whole-candidate review and all outstanding selection/resource/use work remain.\n'
    )
    with args.notes.open('x', encoding='utf-8', newline='\n') as stream:
        stream.write(notes)
    print(json.dumps({'report': binding(args.report), 'notes': binding(args.notes), 'counts': report['counts'],
                      'checks': report['checks'], 'failures': []}, indent=2))


if __name__ == '__main__':
    main()
