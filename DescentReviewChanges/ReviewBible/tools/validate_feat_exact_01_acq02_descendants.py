"""Independently reconstruct ACQ-02 changes and exercise its finite cases.

No application script is imported. Conditional damage events below are supplied
resolved scenario inputs; they do not authenticate attacks or campaign facts.
"""
import argparse
from collections import Counter
from copy import deepcopy
from datetime import datetime, timezone
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path
import re

from feat_exact_01_warrior_acquisition_model import (
    BasicMutationActivation, loadout_errors, mutation_prerequisites_met,
    mutation_slots, mutation_component_ready,
)

R = Path(__file__).resolve().parents[1]
G = R.parents[1]
A = G/'docs/audit/2026-10-08/full-game'
V = A/'feat327-acq02-source'


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def info(path):
    data = path.read_bytes()
    return {'path': path.relative_to(G).as_posix(), 'bytes': len(data), 'sha256': sha256(data).hexdigest()}


class ConditionalTranscendent(BasicMutationActivation):
    """Normal cap-three route, with actual event records rather than a flag.

    The host scenario supplies correctly resolved, personally caused damage
    against independent meaningful hostiles. Dice, target defense, threat and
    action legality are not authenticated by this arithmetic/event model.
    """
    def __post_init__(self):
        super().__post_init__()
        self.progress = Fraction(0)
        self.bt = 0
        self.event_ids = set()
        self.damage_events = []
        self.pulse_until = None
        self.pulse_used = False
        self.maximum_hp = 80

    @property
    def active(self):
        if self.pulse_until is not None and self.turn < self.pulse_until:
            return list(self.equipped)
        return super().active

    def record_damage_event(self, event):
        if event['id'] in self.event_ids:
            raise ValueError('Same resolved event cannot contribute twice')
        if event['regularRound'] != self.turn:
            raise ValueError('Event must belong to the current recorded round')
        if type(event['actualDamage']) is not int or event['actualDamage'] < 0:
            raise ValueError('Actual resolved damage must be a nonnegative integer')
        self.event_ids.add(event['id'])
        self.damage_events.append(deepcopy(event))
        if not (event['personalDamage'] and event['meaningfulIndependentHostile']) or event['noResourceGeneration']:
            return False
        before = self.progress
        self.progress += min(event['actualDamage'], Fraction(self.maximum_hp, 4))
        crossings = sum(before < Fraction(self.maximum_hp*n, 4) <= self.progress for n in (1, 2, 3))
        # Each event is capped at one quarter; the authored trace uses one
        # contributing event per separate round, below normal generation2.
        self.bt = min(3, self.bt+crossings)
        trigger = self.level >= 12 and before < self.maximum_hp <= self.progress and not self.pulse_used
        if trigger:
            self.pulse_used = True
            self.pulse_until = self.turn+1
        return trigger

    def next_regular_turn(self):
        super().next_regular_turn()
        if self.pulse_until is not None and self.turn >= self.pulse_until:
            self.pulse_until = None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path, default=A/'FEAT327_ACQ_02_INDEPENDENT_FULFILLMENT.json')
    args = parser.parse_args()
    assert not args.report.exists(), 'Use a new report path to preserve prior evidence'
    operations_path = A/'FEAT327_ACQ_02_DERIVED_OPERATIONS.json'
    applied = read(operations_path)
    source_ops = read(V/'OPERATIONS.json')
    o1, o2, o3 = source_ops['operations']
    preservation = read(A/'feat-exact-01-before-acq02/PRESERVATION_MANIFEST.json')
    before = {row['path']: G/row['preservedCopy'] for row in preservation}
    checks = []

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

    check('exact-scope-decision', source_ops['disposition'],
          'REVISE_GLOBAL_GLOBAL_PROPOSAL_TO_PER_TREE_ADVANCED_GLOBAL_APEX', 'source-data')
    for payload in read(V/'FILE_MANIFEST.json')['payloads']:
        measured = info(V/payload['path'])
        check(payload['path']+':package-payload',
              {key: measured[key] for key in ('bytes', 'sha256')},
              {key: payload[key] for key in ('bytes', 'sha256')}, 'source-integrity')
    archive = A/'DD_FEAT327_ACQ_02_Warrior_Tier_Addendum.zip'
    check('actual-GPT-package-bytes', archive.stat().st_size, 20196, 'source-integrity')
    check('actual-GPT-package-hash', info(archive)['sha256'],
          '7e69bc1839aa96f5119d345520b0f1f9791cd6317e9f02aa92a6b30c7303f726', 'source-integrity')
    check('seven-derived-descendants', len(preservation), 7, 'source-data')
    for row in preservation:
        copied = info(G/row['preservedCopy'])
        check(row['path']+':preserved-exact-old-bytes',
              {key: copied[key] for key in ('bytes', 'sha256')},
              {key: row[key] for key in ('bytes', 'sha256')}, 'source-integrity')

    class_paths = [o1['path'], 'DescentReviewChanges/ReviewBible/data/playtest/class_drafts/warrior.json']
    for path in class_paths:
        original = read(before[path])
        check(path+':old-engine-binding', original['engine'][17], o1['old'], 'source-integrity')
        expected = deepcopy(original)
        expected['engine'][17] = o1['replacement']
        check(path+':whole-json-only-one-allowed-field', read(G/path), expected, 'whole-descendant')
    original_guide = before[o2['path']].read_text(encoding='utf-8')
    check('Warrior-manuscript:exact-one-paragraph', (G/o2['path']).read_text(encoding='utf-8'),
          original_guide.replace(o2['old'], o2['replacement']), 'whole-descendant')
    shared_paths = ['DescentReviewChanges/ReviewBible/data/director/feat_candidates/exact_01/shared_rules.json',
                    'DescentReviewChanges/ReviewBible/data/public/feat_candidates/exact_01/shared_rules.json']
    for path in shared_paths:
        original = read(before[path])
        expected = deepcopy(original)
        fs1 = next(row for row in expected['rules'] if row['id'] == 'FS-01')
        fs1['wording'] += '\n\n'+o3['paragraph']
        check(path+':whole-json-only-FS01-append', read(G/path), expected, 'whole-descendant')
    manuscript = 'DescentReviewChanges/ReviewBible/docs/feats/exact-candidate-01/SHARED_RULES.md'
    old_fs1 = next(row['wording'] for row in read(before[shared_paths[0]])['rules'] if row['id'] == 'FS-01')
    check('FS01-manuscript:exact-append', (G/manuscript).read_text(encoding='utf-8'),
          before[manuscript].read_text(encoding='utf-8').replace(old_fs1, old_fs1+'\n\n'+o3['paragraph']),
          'whole-descendant')
    foundation = 'DescentReviewChanges/ReviewBible/data/playtest/character_foundation.json'
    expected = read(before[foundation])
    next(row for row in expected['classes'] if row['class'] == 'Warrior')['classCandidateSha256'] = info(G/o1['path'])['sha256']
    check('foundation:only-current-Warrior-hash-updated', read(G/foundation), expected, 'whole-descendant')
    for binding in applied['measuredCurrentDescendants']:
        check(binding['path']+':current-operation-binding', info(G/binding['path']), binding, 'source-integrity')
    for binding in applied['unchangedProtectedBindings']:
        check(binding['path']+':historical-or-unaffected-file-still-identical', info(G/binding['path']), binding, 'source-integrity')

    fixtures = read(A/'FEAT_EXACT_01_WARRIOR_ACQUISITION_FIXTURES.json')
    current_warrior = read(G/o1['path'])
    cards = {row['id']: row for row in current_warrior['cards']}
    profiles = fixtures['ordinaryMutationProfiles']
    for sid, profile in profiles.items():
        check(sid+':whole-source-profile-still-identical',
              {key: value for key, value in profile.items() if key not in {'tier', 'tree'}}, cards[sid], 'source-integrity')
        match = re.fullmatch(r'Warrior (\d+); (Basic|Advanced|Apex) (Vital|Combat|Aberrant)(?:; maximum one Apex equipped)?',
                             cards[sid]['prerequisite'])
        check(sid+':actual-tree-and-tier', (profile['tier'], profile['tree']), (match[2], match[3]), 'source-data')
    contracts = read(A/'FEAT_EXACT_01_ACQUISITION_CONTRACTS.json')
    records = {row['id']: row for row in contracts['records']}
    for fixture in fixtures['fixtures']:
        sid = fixture['featId']
        check(sid+':current-corrected-engine-positive', mutation_prerequisites_met(
            records[sid]['requirements'], fixture['classLevels'], fixture['equipmentReceipt']['equippedAfter'],
            profiles, 'per-tree'), True)
        check(sid+':procedure-and-requirement-unchanged',
              (records[sid]['completeOperativeProcedure'], records[sid]['requirements']),
              (fixture['completeOperativeProcedure'], fixture['requirements']), 'source-integrity')

    def mut(*suffixes):
        return ['warrior.supplement.'+suffix for suffix in suffixes]

    def owned(level):
        return {sid for row in fixtures['completeClassSelectionHistoryThrough20'][:level]
                for sid in row['selectedCards']+row['automaticCards']}

    mixed3 = mut('ossified-core', 'echo-knuckles', 'warpgrip-talons')
    check('ACQ02-T01:mixed-three-Advanced-legal', loadout_errors(13, mixed3, profiles, 'per-tree'), [])
    state = BasicMutationActivation(13, mixed3, profiles, owned(13), 'per-tree')
    check('ACQ02-T01:ordinary-global-active-limit-with-Efficiency', state.ordinary_limit, 2)
    state_no_eff = BasicMutationActivation(13, mixed3, profiles, owned(13)-{'warrior.arch.mutation-efficiency'}, 'per-tree')
    check('ACQ02-T01:no-automatic-Efficiency-by-level', state_no_eff.ordinary_limit, 1)
    double_apex = mut('mythic-carapace', 'butcherform-chassis')
    check('ACQ02-T02:dormant-two-Apex-rejected-across-trees',
          loadout_errors(16, double_apex, profiles, 'per-tree'), ['more than one Apex equipped'])
    advanced3 = mut('echo-knuckles', 'warpgrip-talons', 'adrenal-backlash-core')
    check('ACQ02-T03:three-same-tree-Advanced-rejected', loadout_errors(20, advanced3, profiles, 'per-tree'),
          ['more than two Advanced equipped in one tree'])
    reject('ACQ02-T03:Apex-Form-cannot-repair-illegal-equipment',
           lambda: BasicMutationActivation(20, advanced3, profiles, owned(20), 'per-tree'))
    check('ACQ02-T03:Warrior20-has-four-slots-once', mutation_slots(20), 4)
    for names in [('echo-knuckles', 'warpgrip-talons', 'ossified-core', 'mythic-carapace'),
                  ('echo-knuckles', 'warpgrip-talons', 'ossified-core', 'redundant-organs')]:
        check('ACQ02-T05:mixed-four-control:'+names[-1], loadout_errors(20, mut(*names), profiles, 'per-tree'), [])
    vitals = mut('bloodthick-node', 'ironhide-graft', 'spinal-buffer')
    check('ACQ02-T06:other-class-levels-cannot-unlock-Warrior13', mutation_prerequisites_met(
        records['livingFortress']['requirements'], {'Warrior': 8, 'Mage': 8}, vitals, profiles, 'per-tree'), False)
    check('ACQ02-T07:duplicate-source-identity-rejected',
          loadout_errors(20, [vitals[0], vitals[0]], profiles, 'per-tree'), ['same mutation equipped twice'])
    forged = deepcopy(profiles[advanced3[2]])
    forged['tree'] = 'Vital'
    check('ACQ02-T07:invented-tree-label-fails-source-binding', forged == profiles[advanced3[2]], False)

    # T04 and T08 share a concrete conditional trace. Two real modeled serum
    # payments precede the fourth supplied resolved damage contribution. The
    # pulse follows threshold crossing; no caller can set a pulse boolean.
    pulse = ConditionalTranscendent(16, vitals, profiles, owned(16), 'per-tree')
    trace = []
    for turn in range(1, 5):
        if turn > 1:
            pulse.next_regular_turn()
        if turn == 2:
            pulse.inject_basic(vitals[0])
        if turn == 3:
            pulse.inject_basic(vitals[1])
            check('ACQ02-T04:two-active-before-real-threshold-event',
                  mutation_component_ready('livingFortress', vitals, pulse.active, profiles), False)
        event = {'id': f'conditional-hostile-damage-{turn}', 'regularRound': turn,
                 'actualDamage': 20, 'personalDamage': True,
                 'meaningfulIndependentHostile': True, 'noResourceGeneration': False}
        triggered = pulse.record_damage_event(event)
        trace.append({'event': event, 'progress': int(pulse.progress), 'storedBt': pulse.bt,
                      'pulseTriggered': triggered, 'active': list(pulse.active)})
    check('ACQ02-T08:actual-progress-event-sequence', [row['progress'] for row in trace], [20, 40, 60, 80])
    check('ACQ02-T08:stored-BT-does-not-become-four', [row['storedBt'] for row in trace], [1, 2, 3, 3])
    check('ACQ02-T08:only-fourth-event-triggers', [row['pulseTriggered'] for row in trace], [False, False, False, True])
    check('ACQ02-T04:recorded-pulse-three-active',
          mutation_component_ready('livingFortress', vitals, pulse.active, profiles), True)
    check('ACQ02-T04:pulse-does-not-consume-another-serum', len(pulse.doses), 1)
    old_durations = dict(pulse.active_until)
    check('ACQ02-T04:original-serum-duration-history', old_durations, {vitals[0]: 5, vitals[1]: 6})
    reject('ACQ02-T08:same-resolved-event-cannot-count-twice', lambda: pulse.record_damage_event(trace[-1]['event']))
    pulse.next_regular_turn()
    check('ACQ02-T04:pulse-ends-next-regular-start', pulse.pulse_until, None)
    check('ACQ02-T04:unexpired-original-duration-only', pulse.active, [vitals[1]])
    check('ACQ02-T04:duration-not-refreshed', pulse.active_until, {vitals[1]: 6})
    check('ACQ02-T04:flanking-mutation-component-stops',
          mutation_component_ready('livingFortress', vitals, pulse.active, profiles), False)
    later = {**trace[-1]['event'], 'id': 'conditional-later-event', 'regularRound': 5}
    check('ACQ02-T08:later-event-cannot-repeat-pulse', pulse.record_damage_event(later), False)
    for key, value in [('personalDamage', False), ('meaningfulIndependentHostile', False), ('noResourceGeneration', True)]:
        control = ConditionalTranscendent(16, vitals, profiles, owned(16), 'per-tree')
        event = {**trace[0]['event'], key: value}
        check('ACQ02-T08:excluded-event:'+key, control.record_damage_event(event), False)
        check('ACQ02-T08:excluded-event-no-progress:'+key, int(control.progress), 0)

    authored_cases = read(V/'ACCEPTANCE_CASES.json')['cases']
    check('all-eight-source-case-identities-represented',
          sorted(row['id'] for row in authored_cases), [f'ACQ02-T{i:02}' for i in range(1, 9)], 'coverage')
    check('current-active-contract-mirrors-identical', read(G/shared_paths[0]), read(G/shared_paths[1]), 'whole-descendant')
    failures = [row for row in checks if not row['passed']]
    result = {
        'recordedAtUtc': datetime.now(timezone.utc).isoformat(),
        'status': 'fulfilled-narrow-ACQ02-only' if not failures else 'failed',
        'addendumId': 'FEAT327-ACQ-02', 'checks': len(checks),
        'checkKinds': dict(Counter(row['kind'] for row in checks)),
        'failureCount': len(failures), 'failures': failures, 'results': checks,
        'operationReceipt': info(operations_path), 'validator': info(Path(__file__)),
        'mutationModel': info(R/'tools/feat_exact_01_warrior_acquisition_model.py'),
        'sourceCases': info(V/'ACCEPTANCE_CASES.json'), 'conditionalTranscendentTrace': trace,
        'sourceCaseExecutionScope': 'Equipment/source/class predicates and conditional progress, serum, '
                                  'active-state, frequency and expiry accounting are executed. Actual attack '
                                  'rolls, resolved-damage derivation, meaningful-hostile facts and campaign '
                                  'rest/advancement records remain supplied premises, not authenticated facts.',
        'measuredCurrentDescendants': applied['measuredCurrentDescendants'],
        'originalSourcePackagesPreserved': True,
        'onlyNamedIssueClosed': not failures,
        'allTwelveFullFeatRuntimeProceduresExecuted': False,
        'candidateReadyForSubmission': False, 'sourceInformationDeleted': False,
        'runtimeImplemented': False, 'humanBalanceApproved': False,
        'wholeGameFlowConfirmed': False, 'pushed': False, 'cosmologyReviewed': False,
    }
    with args.report.open('x', encoding='utf-8', newline='\n') as stream:
        json.dump(result, stream, ensure_ascii=False, indent=2)
        stream.write('\n')
    print(json.dumps({'report': info(args.report), 'checks': len(checks), 'failureCount': len(failures),
                      'checkKinds': result['checkKinds'], 'onlyNamedIssueClosed': not failures}, indent=2))
    if failures:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
