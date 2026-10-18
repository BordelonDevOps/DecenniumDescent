"""Isolated specification of the EN6-07-B terminal clarification.

Actual phase existence, save outcomes and source eligibility are INPUTS.
No game engine, scene, character builder, companion profile or RNG is imported.
An unspecified intervening save is an obligation, never an automatic failure.
"""
from dataclasses import dataclass, field
from fractions import Fraction
import unittest

@dataclass
class DanceApplication:
    deadline: Fraction = Fraction('61.2')
    active: bool = True
    suppressed: bool = False
    hard_guard_spent: bool = True
    owner_bonus_action_spent: bool = True
    phase_action_spent: bool = True
    resolved_saves: set = field(default_factory=set)

    def end_checkpoint(self, event_id, at, *, actual_regular_phase_end, success):
        if not self.active:
            return 'already-ended'
        if at >= self.deadline:
            self.active = False
            return 'original-expiry-no-save'
        if not actual_regular_phase_end:
            return 'no-invented-save'
        if event_id in self.resolved_saves:
            return 'no-replay'
        if success is None:
            return 'unresolved-save-obligation'
        self.resolved_saves.add(event_id)
        if success:
            self.active = False
            return 'save-ends-source'
        return 'failed-save-source-remains'

    def end_suppression(self):
        self.suppressed = False
        return self.active


class DanceTerminalTests(unittest.TestCase):
    def suppressed(self):
        return DanceApplication(suppressed=True)

    def test_suppressed_success_ends_before_nominal_expiry(self):
        d = self.suppressed()
        self.assertEqual(d.end_checkpoint('end8.4', Fraction('8.4'), actual_regular_phase_end=True, success=True), 'save-ends-source')
        self.assertFalse(d.active)
        self.assertEqual(d.deadline, Fraction('61.2'))

    def test_suppressed_failure_keeps_same_deadline(self):
        d = self.suppressed()
        self.assertEqual(d.end_checkpoint('end8.4', Fraction('8.4'), actual_regular_phase_end=True, success=False), 'failed-save-source-remains')
        self.assertTrue(d.active)
        self.assertEqual(d.deadline, Fraction('61.2'))

    def test_unspecified_save_is_not_assumed_failure(self):
        d = self.suppressed()
        self.assertEqual(d.end_checkpoint('end8.4', Fraction('8.4'), actual_regular_phase_end=True, success=None), 'unresolved-save-obligation')
        self.assertNotIn('end8.4', d.resolved_saves)

    def test_missing_phase_does_not_create_a_save(self):
        d = self.suppressed()
        self.assertEqual(d.end_checkpoint('absent', Fraction('8.4'), actual_regular_phase_end=False, success=True), 'no-invented-save')
        self.assertTrue(d.active)

    def test_expiry_precedes_coincident_save(self):
        d = self.suppressed()
        self.assertEqual(d.end_checkpoint('deadline', Fraction('61.2'), actual_regular_phase_end=True, success=True), 'original-expiry-no-save')
        self.assertNotIn('deadline', d.resolved_saves)

    def test_earlier_success_cannot_be_restored_at_field_end(self):
        d = self.suppressed()
        d.end_checkpoint('end8.4', Fraction('8.4'), actual_regular_phase_end=True, success=True)
        self.assertFalse(d.end_suppression())
        self.assertEqual(d.end_checkpoint('nominal', Fraction('61.2'), actual_regular_phase_end=False, success=None), 'already-ended')

    def test_expired_source_cannot_resume_at63(self):
        d = self.suppressed()
        d.end_checkpoint('deadline', Fraction('61.2'), actual_regular_phase_end=False, success=None)
        self.assertFalse(d.end_suppression())
        self.assertEqual(d.end_checkpoint('field-end', Fraction(63), actual_regular_phase_end=False, success=None), 'already-ended')

    def test_save_replay_does_not_create_new_result(self):
        d = self.suppressed()
        d.end_checkpoint('end8.4', Fraction('8.4'), actual_regular_phase_end=True, success=False)
        self.assertEqual(d.end_checkpoint('end8.4', Fraction('8.4'), actual_regular_phase_end=True, success=True), 'no-replay')
        self.assertTrue(d.active)

    def test_no_ending_refunds_prior_budgets(self):
        for success in (True, False, None):
            d = self.suppressed()
            d.end_checkpoint('end8.4', Fraction('8.4'), actual_regular_phase_end=True, success=success)
            d.end_suppression()
            self.assertTrue(d.hard_guard_spent)
            self.assertTrue(d.owner_bonus_action_spent)
            self.assertTrue(d.phase_action_spent)

if __name__ == '__main__':
    unittest.main(verbosity=2)
