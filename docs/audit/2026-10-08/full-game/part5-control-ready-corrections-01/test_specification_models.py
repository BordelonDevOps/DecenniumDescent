"""Model-only regression tests; no game engine is imported or exercised."""
import copy
from fractions import Fraction
import unittest
from reference_models import PrisonRoot, PuppetEnd, GeasPermission, DominateEnd, CopyReadyLedger, time, operative_cr_eligible

class PrisonTests(unittest.TestCase):
    def root(self, flag=False):
        r=PrisonRoot('caster-A','recipient-A','application-A-root',flag);r.entry(28);return r
    def test_exit_preserves_nonnull_snapshot_after_veil_gain(self):
        r=self.root();r.departure('escape',24,current_caster_null=True)
        self.assertEqual([x['nullNonlethal'] for x in r.events],[False,False])
    def test_exit_preserves_null_snapshot_after_veil_loss(self):
        r=self.root(True);r.departure('escape',24,current_caster_null=False)
        self.assertEqual([x['nullNonlethal'] for x in r.events],[True,True])
    def test_entry_exit_are_separate_damage_events(self):
        r=self.root();r.departure('escape',24)
        self.assertEqual(100-sum(x['amount'] for x in r.events),48)
        self.assertFalse(any(x['amount']>=50 for x in r.events))
        self.assertEqual(len({x['root'] for x in r.events}),1)
    def test_duplicate_departure_cannot_repeat_damage(self):
        r=self.root();self.assertTrue(r.departure('escape',24));self.assertFalse(r.departure('concentration',24));self.assertEqual(len(r.events),2)
    def test_suppression_consumes_exit_without_dice_event(self):
        r=self.root();r.source_suppression();self.assertFalse(r.departure('escape',24));self.assertEqual(len(r.events),1)
    def test_true_seeing_uses_live_exit_not_dispel(self):
        r=self.root();self.assertTrue(r.departure('true-seeing-departure',24));self.assertEqual(r.events[-1]['kind'],'exit')
    def test_actual_death_blocks_exit(self):
        r=self.root();self.assertFalse(r.departure('death',24,target_alive=False));self.assertEqual(len(r.events),1)
    def test_zero_hp_is_not_actual_death(self):
        # Life-state resolution is an external input; alive at 0 is not deleted.
        r=self.root();self.assertTrue(r.departure('concentration',24,target_alive=True))
    def test_distinct_new_admission_has_distinct_root(self):
        old=self.root(True);old.departure('replacement',24)
        new=PrisonRoot('caster-B','recipient-A','application-B-root',False);new.entry(28)
        self.assertNotEqual(old.events[-1]['root'],new.events[0]['root'])
        self.assertNotEqual(old.events[-1]['nullNonlethal'],new.events[0]['nullNonlethal'])

class ControlTimingTests(unittest.TestCase):
    def puppet(self):return PuppetEnd(time('8.4'),time('14.4'))
    def test_underway_puppet_end_is_not_first_future_end(self):
        p=self.puppet();self.assertEqual(p.checkpoint(time('2.4'),actual_phase=True,save_success=True),'no-save')
    def test_puppet_suppressed_start_still_has_first_end_save(self):
        p=self.puppet();self.assertEqual(p.checkpoint(time('8.4'),actual_phase=True,save_success=False,start_suppressed=True),'save-failure')
    def test_puppet_suppressed_end_and_no_travel_still_save(self):
        p=self.puppet();self.assertEqual(p.checkpoint(time('8.4'),actual_phase=True,save_success=True,end_suppressed=True,distance_travelled=0),'save-success')
    def test_puppet_expiry_precedes_final_save(self):
        self.assertEqual(self.puppet().checkpoint(time('14.4'),actual_phase=True,save_success=True),'expiry-no-save')
    def test_puppet_missing_phase_does_not_create_save(self):
        self.assertEqual(self.puppet().checkpoint(time('8.4'),actual_phase=False,save_success=True),'no-save')
    def test_geas_cannot_promote_soft_task_to_full_action(self):
        g=GeasPermission(False,time(2592000))
        self.assertEqual(g.next_instruction(time(10),requires_full_action=True,safe_soft_alternative=False),'suspend-unexecutable-portion-no-hard-acquisition')
        self.assertFalse(g.acquired_hard);self.assertEqual(g.deadline,2592000)
    def test_geas_soft_alternative_and_voluntary_opening(self):
        g=GeasPermission(False,time(2592000))
        self.assertEqual(g.next_instruction(time(10),requires_full_action=True,safe_soft_alternative=True),'soft-only')
        self.assertEqual(g.next_instruction(time(11),requires_full_action=True,safe_soft_alternative=False,voluntary_action_opened_path=True),'soft-only')
        self.assertFalse(g.acquired_hard)
    def test_geas_keeps_legitimately_acquired_hard_permission(self):
        g=GeasPermission(True,time(2592000));self.assertEqual(g.next_instruction(time(10),requires_full_action=True,safe_soft_alternative=False),'original-hard-permission-subject-to-source-limits')
    def test_geas_original_deadline(self):
        self.assertEqual(GeasPermission(False,time(2592000)).next_instruction(time(2592000),requires_full_action=False,safe_soft_alternative=True),'expired')
    def test_dominate_no_phase_is_end_only(self):
        d=DominateEnd(time(1),time(61));due=d.next_absent_due(time(1));self.assertEqual(due,7)
        self.assertEqual(d.save('v1',due,real_phase_end=False,absent_schedule_due=due),'one-wis-save-no-action')
    def test_dominate_real_phase_maps_next_save_and_cadence(self):
        d=DominateEnd(time(1),time(61));self.assertEqual(d.save('p1',time(4),real_phase_end=True),'one-wis-save-no-action');self.assertEqual(d.next_absent_due(time(5)),10)
    def test_dominate_toggle_does_not_reset_or_catch_up(self):
        d=DominateEnd(time(1),time(61));self.assertEqual(d.next_absent_due(time(3)),7);self.assertEqual(d.next_absent_due(time(6)),7);self.assertEqual(d.next_absent_due(time(20)),25)
    def test_dominate_simultaneous_checkpoints_deduplicated(self):
        d=DominateEnd(time(1),time(61));d.save('p1',time(7),real_phase_end=True)
        self.assertEqual(d.save('v1',time(7),real_phase_end=False,absent_schedule_due=time(7)),'already-consumed')
    def test_dominate_expiry_precedes_save(self):
        self.assertEqual(DominateEnd(time(1),time(61)).save('p',time(61),real_phase_end=True),'expiry-no-save')
    def test_missing_cr_not_level_conversion(self):
        self.assertFalse(operative_cr_eligible(None));self.assertFalse(operative_cr_eligible('10'));self.assertFalse(operative_cr_eligible(True));self.assertFalse(operative_cr_eligible(11));self.assertTrue(operative_cr_eligible(10))

class CopyReadyTests(unittest.TestCase):
    def prepared(self, owns=False,profile='Strike'):
        m=CopyReadyLedger(class_engine_actually_owned=owns);self.assertTrue(m.prepare('h','N',time(6),profile=profile));return m
    def test_preparation_spends_before_counter(self):
        m=CopyReadyLedger();self.assertTrue(m.prepare('h','N',time(6),countered=True));self.assertEqual((m.rp,m.permission_uses,m.counter_windows,m.action_spends),(23,2,1,1));self.assertIn('N',m.feat_rounds);self.assertIsNone(m.hold)
    def test_precommit_failure_is_atomic(self):
        m=CopyReadyLedger(class_engine_actually_owned=True);m.class_rounds['N']='other';before=m.snapshot();self.assertFalse(m.prepare('h','N',time(6)));self.assertEqual(before,m.snapshot())
    def test_same_round_release_reuses_own_token(self):
        m=self.prepared(True);self.assertEqual(m.release('N',time(2)),'committed');self.assertEqual((len(m.feat_rounds),len(m.class_rounds)),(1,1))
    def test_crossround_spends_both_rounds_with_one_payment(self):
        m=self.prepared(True);self.assertEqual(m.release('N+1',time(5)),'committed');self.assertEqual(set(m.feat_rounds),{'N','N+1'});self.assertEqual(set(m.class_rounds),{'N','N+1'});self.assertEqual((m.rp,m.permission_uses,m.cast_history_updates,m.counter_windows,m.components_provided),(23,2,1,1,1))
    def test_crossround_class_cap_failure_no_partial_feat_spend(self):
        m=self.prepared(True);m.class_rounds['N+1']='actually-lawful-other-release';before=m.snapshot();self.assertEqual(m.release('N+1',time(5)),'not-committed');self.assertEqual(before,m.snapshot())
    def test_crossround_feat_cap_failure_no_partial_class_spend(self):
        m=self.prepared(True);m.feat_rounds['N+1']='actually-lawful-other-copy';before=m.snapshot();self.assertEqual(m.release('N+1',time(5)),'not-committed');self.assertEqual(before,m.snapshot())
    def test_target_invalid_keeps_hold_without_reaction(self):
        m=self.prepared();before=m.snapshot();self.assertEqual(m.release('N',time(3),legal_target_and_sources=False),'not-committed');self.assertEqual(before,m.snapshot())
    def test_decline_keeps_original_hold_and_deadline(self):
        m=self.prepared();self.assertEqual(m.release('N',time(3),trigger_declined=True),'not-committed');self.assertEqual(m.hold['expiry'],6);self.assertEqual(m.reaction_spends,0)
    def test_expiry_exact_boundary_precedes_release(self):
        m=self.prepared();self.assertEqual(m.release('N+1',time(6)),'expired');self.assertEqual(m.reaction_spends,0);self.assertNotIn('N+1',m.feat_rounds);self.assertEqual(m.rp,23)
    def test_concentration_loss_no_refund(self):
        m=self.prepared();m.lose_hold();self.assertEqual((m.rp,m.permission_uses),(23,2));self.assertIn('N',m.feat_rounds);self.assertEqual(m.release('N',time(4)),'no-hold')
    def test_retry_no_second_payload_or_spend(self):
        m=self.prepared();m.release('N',time(3));before=m.snapshot();self.assertEqual(m.release('N',time(3)),'no-hold');self.assertEqual(m.snapshot(),before)
    def test_preparation_id_cannot_be_reused(self):
        m=self.prepared();m.lose_hold();before=m.snapshot();self.assertFalse(m.prepare('h','N+1',time(10)));self.assertEqual(before,m.snapshot())
    def test_invalid_replacement_does_not_delete_prior_hold(self):
        m=self.prepared();before=m.snapshot();self.assertFalse(m.prepare('other','N+1',time(10),legal_action_and_sources=False));self.assertEqual(before,m.snapshot())
    def test_same_round_cannot_use_someone_elses_token(self):
        m=self.prepared();m.feat_rounds['N']='different-copy';before=m.snapshot();self.assertEqual(m.release('N',time(3)),'not-committed');self.assertEqual(before,m.snapshot())
    def test_unowned_class_engine_not_granted(self):
        m=self.prepared(False);m.release('N+1',time(5));self.assertEqual(m.class_rounds,{})
    def test_sustained_same_concentration_burden(self):
        m=self.prepared(profile='Ward');m.release('N',time(3));self.assertEqual(m.concentration,'sustained');self.assertEqual(m.cast_history_updates,1)
    def test_immediate_concentration_ends_after_resolution(self):
        m=self.prepared(profile='Strike');m.release('N',time(3));self.assertIsNone(m.concentration)
    def test_late_prevention_retains_committed_spends(self):
        m=self.prepared(True);self.assertEqual(m.release('N+1',time(5),later_payload_prevented=True),'committed-prevented');self.assertEqual(m.reaction_spends,1);self.assertIn('N+1',m.class_rounds);self.assertEqual(m.payloads,0)
    def test_snapshot_restoration_preserves_history(self):
        m=self.prepared(True);saved=m.snapshot();restored=CopyReadyLedger();restored.__dict__=copy.deepcopy(saved);restored.release('N+1',time(5));self.assertEqual((restored.rp,restored.counter_windows,restored.cast_history_updates),(23,1,1));self.assertIn('N',restored.feat_rounds)
    def test_no_future_allowance_reserved_at_preparation(self):
        m=self.prepared(True);self.assertNotIn('N+1',m.feat_rounds);self.assertNotIn('N+1',m.class_rounds)

if __name__=='__main__':unittest.main(verbosity=2)
