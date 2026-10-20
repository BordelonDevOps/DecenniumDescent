"""Isolated targeted reference-module tests, not game runtime or Oracle acquisition.

Use only a separately reconstructed archival source tree. Fixtures retain their
conditional source and world premises. Reports use exclusive creation.
"""
import argparse
import json
import sys
import unittest
from copy import deepcopy
from dataclasses import replace
from pathlib import Path

sys.dont_write_bytecode = True
parser = argparse.ArgumentParser()
parser.add_argument('--source-root', required=True)
parser.add_argument('--report', required=True)
args = parser.parse_args()
root = Path(args.source_root).resolve()
report_path = Path(args.report)
if report_path.exists():
    raise SystemExit('Preserve existing report; use a new report path')
sys.path.insert(0, str(root / 'DescentReviewChanges/ReviewBible/tools'))
from feat335_copy_payload_fixtures import CopyPayloadFixtures
from healing_playtest_rules import HealingReduction, healing_packet
from form_temphp_playtest_rules import BufferGrant
from control_playtest_rules import ClockMarker

F = CopyPayloadFixtures()

class Followup(unittest.TestCase):
    def ready(self, profile='mend', paid=True):
        m = F.make(); F.start(m); F.capture(m, profile)
        if paid:
            F.declare(m, profile)
        return m

    def reduction(self, present=True, suppressed=False, next_healing=True, ident='old', value=1):
        return HealingReduction(ident, 'actual-reducer', 'flat', value,
                                present=present, suppressed=suppressed, next_healing=next_healing)

    def atomic_error(self, m, call, message=None):
        before = m.snapshot()
        with self.assertRaises(ValueError) as ctx:
            call()
        if message:
            self.assertIn(message, str(ctx.exception))
        self.assertEqual(m.snapshot(), before)

    def mend(self, m):
        return m.resolve('cast', rolls={'nativeDice': [4, 4]})

    def buffer(self, m, target='target', ident='actual-prior-overflow', deadline=12,
               amount=5, rider=True, dependencies=()):
        # Already lawfully established conditional fixture: no Oracle source
        # acquisition, invocation, healing conversion, or condition removal.
        grant = BufferGrant(ident,
            'oracle.supplement.life.overflowing-light' if rider else 'actual-prior-plain-buffer',
            'prior-owner', target, amount, expiry=ClockMarker(deadline),
            riders={'overflowing-cleanse'} if rider else set(), dependencies=dependencies)
        m.world.buffers.offer(grant, m.world.now); m.world.projection()
        return grant

    def expected(self, m, deadline=12):
        return deepcopy(m.world.buffers).expire(ClockMarker(deadline))

    def test_active_next_heal_rejected_before_payment_atomically(self):
        m = self.ready(paid=False)
        m.world.actors['target']['healingReductions'] = [self.reduction()]
        frame = F.frame(m); before_frame = deepcopy(frame)
        self.atomic_error(m, lambda: m.declare('cast', 'capture', permission='pending',
            grant_id='Wizard/class-engine', frame=frame, selection=F.selection('mend')), 'source-owned adapter')
        self.assertEqual(frame, before_frame)
        self.assertEqual(m.pool['rp'], 44)

    def test_active_next_heal_rejected_after_paid_commit_atomically(self):
        m = self.ready()
        m.world.actors['target']['healingReductions'] = [self.reduction()]
        self.atomic_error(m, lambda: self.mend(m), 'actual consumption adapter')
        self.assertEqual(m.pool['rp'], 42)
        self.assertEqual(m.world.actors['target']['life'].hp, 30)

    def test_reducer_becoming_operative_after_declaration_is_rechecked(self):
        m = self.ready(paid=False)
        actor = m.world.actors['target']; r = self.reduction(suppressed=True)
        actor['healingReductions'] = [r]; F.declare(m, 'mend')
        actor['healingReductions'] = [replace(r, suppressed=False)]
        self.atomic_error(m, lambda: self.mend(m), 'actual consumption adapter')

    def test_unresolved_paid_attempt_can_resume_when_reducer_is_now_suppressed(self):
        m = self.ready(); actor = m.world.actors['target']; r = self.reduction()
        actor['healingReductions'] = [r]
        self.atomic_error(m, lambda: self.mend(m))
        actor['healingReductions'] = [replace(r, suppressed=True)]
        paid_rp = m.pool['rp']; result = self.mend(m)
        self.assertTrue(result['resolved']); self.assertEqual(actor['life'].hp, 32)
        self.assertEqual(m.pool['rp'], paid_rp)
        self.assertEqual(result['targets']['target']['nextHealingCandidates'], [])

    def test_active_ordinary_flat_reducer_still_applies(self):
        m = self.ready(); actor = m.world.actors['target']
        actor['healingReductions'] = [self.reduction(next_healing=False)]
        self.assertTrue(self.mend(m)['resolved']); self.assertEqual(actor['life'].hp, 31)

    def test_mixed_inactive_next_and_active_ordinary_reduction(self):
        m = self.ready(); actor = m.world.actors['target']
        rs = [self.reduction(suppressed=True), self.reduction(ident='ordinary', next_healing=False)]
        actor['healingReductions'] = rs
        result = self.mend(m); self.assertEqual(actor['life'].hp, 31)
        self.assertEqual(result['targets']['target']['nextHealingCandidates'], [])
        self.assertEqual(actor['healingReductions'], rs)

    def test_active_next_not_waived_when_its_arithmetic_group_loses(self):
        m = self.ready(); actor = m.world.actors['target']
        actor['healingReductions'] = [self.reduction(), self.reduction(ident='stronger', value=9, next_healing=False)]
        self.atomic_error(m, lambda: self.mend(m))

    def test_hp_prohibition_retained_with_inactive_next_record(self):
        m = self.ready(); actor = m.world.actors['target']
        actor['healingReductions'] = [self.reduction(present=False)]
        actor['hpGainProhibited'] = True
        result = self.mend(m)
        self.assertTrue(result['resolved']); self.assertEqual(actor['life'].hp, 30)
        self.assertEqual(result['targets']['target']['actualHpGained'], 0)

    def test_countered_inactive_mend_rolls_nothing_and_keeps_payment(self):
        m = self.ready(); actor = m.world.actors['target']
        actor['healingReductions'] = [self.reduction(present=False)]
        result = m.resolve('cast', countered=True)
        self.assertFalse(result['resolved']); self.assertEqual(actor['life'].hp, 30)
        self.assertEqual(m.pool['rp'], 42)

    def test_inactive_record_does_not_restore_lost_target_eligibility(self):
        m = self.ready(); actor = m.world.actors['target']
        actor['healingReductions'] = [self.reduction(suppressed=True)]
        actor['willing'] = False
        result = m.resolve('cast')
        self.assertFalse(result['resolved']); self.assertEqual(actor['life'].hp, 30)

    def test_successful_inactive_mend_cannot_resolve_twice(self):
        m = self.ready()
        m.world.actors['target']['healingReductions'] = [self.reduction(present=False)]
        self.mend(m); self.atomic_error(m, lambda: self.mend(m))

    def test_canonical_life_and_reducer_objects_are_retained(self):
        m = self.ready(); actor = m.world.actors['target']; life = actor['life']
        r = self.reduction(suppressed=True); actor['healingReductions'] = [r]
        self.mend(m)
        self.assertIs(actor['life'], life); self.assertIs(actor['healingReductions'][0], r)
        self.assertEqual(life.hp, 32); self.assertTrue(r.next_healing)

    def test_advance_without_expiry_returns_empty_instructions(self):
        m = F.make(); F.start(m)
        self.assertEqual(m.world.advance(ClockMarker(7), [m]), [])

    def test_natural_expiry_returns_exact_source_instruction(self):
        m = F.make(); F.start(m); grant = self.buffer(m); expected = self.expected(m)
        result = m.world.advance(ClockMarker(12), [m])
        self.assertEqual(result, expected); self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['sourceId'], grant.source_id)
        self.assertEqual(result[0]['grantId'], grant.grant_id)
        self.assertEqual(result[0]['target'], 'target')
        self.assertEqual(m.world.buffers.grants[grant.grant_id].state, 'natural-expiry')
        self.assertEqual(m.world.actors['target']['life'].temp_hp, 0)

    def test_external_source_expiry_without_copy_engines_is_forwarded(self):
        m = F.make(); F.start(m); self.buffer(m)
        expected = self.expected(m)
        self.assertEqual(m.world.advance(ClockMarker(12), []), expected)

    def test_expired_grant_keeps_original_owner_for_downstream_lookup(self):
        m = F.make(); F.start(m); grant = self.buffer(m)
        result = m.world.advance(ClockMarker(12), [m])
        stored = m.world.buffers.grants[result[0]['grantId']]
        self.assertEqual(stored.owner, 'prior-owner')
        self.assertEqual(stored.source_id, grant.source_id)
        self.assertNotEqual(stored.owner, m.owner)
        self.assertEqual(stored.state, 'natural-expiry')

    def test_before_deadline_keeps_buffer_and_emits_nothing(self):
        m = F.make(); F.start(m); grant = self.buffer(m)
        self.assertEqual(m.world.advance(ClockMarker(11), [m]), [])
        self.assertEqual(m.world.buffers.current('target').grant_id, grant.grant_id)
        self.assertEqual(m.world.actors['target']['life'].temp_hp, 5)
        self.assertEqual(len(m.world.advance(ClockMarker(12), [m])), 1)

    def test_repeat_expiry_does_not_duplicate_instruction(self):
        m = F.make(); F.start(m); self.buffer(m)
        first = m.world.advance(ClockMarker(12), [m])
        self.assertEqual(len(first), 1)
        self.assertEqual(m.world.advance(ClockMarker(12), [m]), [])
        self.assertEqual(m.world.buffers.expire(ClockMarker(12)), [])
        self.assertEqual(m.world.advance(ClockMarker(13), [m]), [])

    def test_instruction_preserves_choice_and_never_cleanses_automatically(self):
        m = F.make(); F.start(m); self.buffer(m)
        conditions = {'Frightened', 'Poisoned', 'Staggered', 'Blinded'}
        m.world.actors['target']['conditions'] = set(conditions)
        result = m.world.advance(ClockMarker(12), [m])
        self.assertEqual(result[0]['chooseUpTo'], 1)
        self.assertEqual(result[0]['eligibleConditions'], ('Frightened', 'Poisoned', 'Staggered'))
        self.assertEqual(m.world.actors['target']['conditions'], conditions)
        self.assertEqual(m.world.actors['target']['life'].hp, 30)

    def test_actual_caller_can_receive_all_instructions_without_reexpiring(self):
        m = F.make(); F.start(m); self.buffer(m)
        expected = self.expected(m); receiver = []
        receiver.extend(m.world.advance(ClockMarker(12), [m]))
        self.assertEqual(receiver, expected)
        self.assertEqual(m.world.buffers.expire(ClockMarker(12)), [])
        # Receiver is a recorder, not a gameplay condition-choice implementation.

    def test_multiple_grants_preserve_exact_order_and_source_identity(self):
        m = F.make(); F.start(m); self.buffer(m)
        self.buffer(m, target='target2', ident='second-actual-overflow')
        expected = self.expected(m); result = m.world.advance(ClockMarker(12), [m])
        self.assertEqual(result, expected); self.assertEqual(len(result), 2)
        self.assertEqual([e['target'] for e in result], ['target', 'target2'])

    def test_plain_buffer_expiry_does_not_invent_cleanse(self):
        m = F.make(); F.start(m); grant = self.buffer(m, rider=False)
        self.assertEqual(m.world.advance(ClockMarker(12), [m]), [])
        self.assertEqual(m.world.buffers.grants[grant.grant_id].state, 'natural-expiry')

    def test_replaced_overflow_emits_no_natural_expiry_rider(self):
        m = F.make(); F.start(m); grant = self.buffer(m)
        self.buffer(m, ident='larger-plain', amount=6, rider=False)
        self.assertEqual(m.world.buffers.grants[grant.grant_id].state, 'replaced')
        self.assertEqual(m.world.advance(ClockMarker(12), [m]), [])

    def test_actual_damage_depletion_emits_no_expiry_rider(self):
        m = F.make(); F.start(m); grant = self.buffer(m); actor = m.world.actors['target']
        life, _ = m.world.buffers.core_damage('target', 'actual-prior-damage', actor['life'], 5,
                                             now=m.world.now, critical=False)
        actor['life'].__dict__.update(life.__dict__); m.world.projection()
        self.assertEqual(m.world.buffers.grants[grant.grant_id].state, 'depleted')
        self.assertEqual(m.world.advance(ClockMarker(12), [m]), [])

    def test_dependency_end_is_not_natural_expiry(self):
        m = F.make(); F.start(m); grant = self.buffer(m, dependencies=('actual-dependency',))
        m.world.buffers.end_dependency('actual-dependency'); m.world.projection()
        self.assertEqual(m.world.buffers.grants[grant.grant_id].state, 'dependency-ended')
        self.assertEqual(m.world.advance(ClockMarker(12), [m]), [])

    def test_equal_rejected_offer_retains_original_overflow_instruction(self):
        m = F.make(); F.start(m); grant = self.buffer(m)
        self.buffer(m, ident='equal-plain', amount=5, rider=False)
        expected = self.expected(m); result = m.world.advance(ClockMarker(12), [m])
        self.assertEqual(result, expected); self.assertEqual(result[0]['grantId'], grant.grant_id)
        self.assertEqual(m.world.buffers.grants['equal-plain'].state, 'rejected')

    def test_copy_ward_and_other_source_expire_without_cross_source_cleanse(self):
        m = self.ready('ward', paid=False)
        F.declare(m, 'ward', selection=F.selection('ward', ['target2']))
        m.resolve('cast', rolls={'nativeDice': [4, 4]})
        self.buffer(m, deadline=18)
        expected = self.expected(m, 18)
        result = m.world.advance(ClockMarker(18), [m])
        self.assertEqual(result, expected); self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['target'], 'target')
        self.assertEqual(m.world.actors['target2']['life'].temp_hp, 0)
        self.assertTrue(all(not e['active'] for e in m.world.effects.values()))

    def test_missing_live_copy_engine_rejects_before_expiry_and_clock_mutation(self):
        m = self.ready('ward'); m.resolve('cast', rolls={'nativeDice': [4, 4]})
        self.buffer(m, target='target2')
        self.atomic_error(m, lambda: m.world.advance(ClockMarker(18), []))
        self.assertEqual(m.world.buffers.current('target2').remaining, 5)

    def test_backward_clock_rejects_before_expiry(self):
        m = F.make(); F.start(m); self.buffer(m)
        self.atomic_error(m, lambda: m.world.advance(ClockMarker(5), [m]))

    def test_returned_instruction_mutation_does_not_revive_or_change_grant(self):
        m = F.make(); F.start(m); grant = self.buffer(m)
        result = m.world.advance(ClockMarker(12), [m]); snapshot = m.world.snapshot()
        result[0]['grantId'] = 'caller-mutated-copy'
        self.assertEqual(m.world.snapshot(), snapshot)
        self.assertEqual(m.world.buffers.grants[grant.grant_id].source_id,
                         'oracle.supplement.life.overflowing-light')

# Exercise the full inactive Boolean state space at BOTH adapter guards.
for timing in ['before_declaration', 'after_paid_declaration']:
    for present, suppressed in [(False, False), (True, True), (False, True)]:
        def case(self, timing=timing, present=present, suppressed=suppressed):
            m = self.ready(paid=timing == 'after_paid_declaration')
            actor = m.world.actors['target']; r = self.reduction(present=present, suppressed=suppressed)
            actor['healingReductions'] = [r]
            expected = healing_packet(actor['life'], 2, dice_count=2, reductions=[r])
            self.assertEqual(expected['state'].hp, 32)
            self.assertEqual(expected['nextHealingCandidates'], [])
            if timing == 'before_declaration':
                F.declare(m, 'mend')
            paid_rp = m.pool['rp']; result = self.mend(m)
            self.assertTrue(result['resolved']); self.assertEqual(actor['life'].hp, 32)
            self.assertEqual(result['targets']['target']['nextHealingCandidates'], [])
            self.assertEqual(actor['healingReductions'], [r])
            self.assertEqual(m.pool['rp'], paid_rp); self.assertEqual(paid_rp, 42)
        setattr(Followup, 'test_inactive_%s_present%s_suppressed%s' % (timing, present, suppressed), case)

class Recorded(unittest.TextTestResult):
    def __init__(self, *a, **k):
        super().__init__(*a, **k); self.records = []
    def addSuccess(self, test):
        super().addSuccess(test); self.records.append({'id': test.id(), 'status': 'PASS'})
    def addFailure(self, test, error):
        super().addFailure(test, error)
        self.records.append({'id': test.id(), 'status': 'FAIL', 'traceback': self._exc_info_to_string(error, test)})
    def addError(self, test, error):
        super().addError(test, error)
        self.records.append({'id': test.id(), 'status': 'ERROR', 'traceback': self._exc_info_to_string(error, test)})

result = unittest.TextTestRunner(verbosity=2, resultclass=Recorded).run(
    unittest.defaultTestLoader.loadTestsFromTestCase(Followup))
report = {'scope': 'Targeted isolated reference-module tests with source-qualified conditional fixtures; not game runtime, Oracle acquisition or downstream cleansing.',
          'testsRun': result.testsRun, 'failures': len(result.failures), 'errors': len(result.errors),
          'results': result.records}
with report_path.open('x', encoding='utf8') as out:
    json.dump(report, out, indent=2); out.write('\n')
raise SystemExit(0 if result.wasSuccessful() else 1)
