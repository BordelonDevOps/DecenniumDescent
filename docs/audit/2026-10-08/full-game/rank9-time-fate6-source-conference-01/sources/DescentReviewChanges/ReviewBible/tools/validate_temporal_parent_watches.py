"""Actual later events must stale a prepared complete parent graph watch."""
from copy import deepcopy
from pathlib import Path
import hashlib,json,unittest
from temporal_playtest_rules import Transaction,SpellRuleError
from temporal_parent_watches import watch_parent_graph
from validate_temporal_parent_history import fixture,shift,observed,world,cast


class ParentWatchTests(unittest.TestCase):
    def prepared(self,j):
        tx=Transaction();watch_parent_graph(tx,j)
        wallet=j.wallets['a'];before=wallet.rp;tx.write(wallet,'rp',0)
        return tx,wallet,before

    def rejects(self,tx,wallet,before):
        with self.assertRaises(SpellRuleError):tx.commit()
        self.assertEqual(wallet.rp,before)

    def test_unchanged_graph_watches_are_pure_and_allow_shared_transaction(self):
        w,ds,d,j=fixture();shift(j,ds);old=d.current
        tx,wallet,before=self.prepared(j)
        self.assertEqual(wallet.rp,before);self.assertIs(d.current,old)
        tx.commit();self.assertEqual(wallet.rp,0);self.assertIs(d.current,old)

    def test_real_paid_renewal_after_preflight_invalidates_entire_plan(self):
        w,ds,d,j=fixture();shift(j,ds);tx,wallet,before=self.prepared(j)
        j.renew('renew',ds,600);self.rejects(tx,wallet,before)
        self.assertEqual(d.current.expiry.seconds,1200)

    def test_real_concentration_ending_after_preflight_invalidates_plan(self):
        w=world();j=observed(w);cast(j);tx,wallet,before=self.prepared(j)
        j.end_concentration('end','a',1,reason='failed-save');self.rejects(tx,wallet,before)
        self.assertEqual(w.links['C:b'].state,'failed-save')

    def test_actual_equipment_loss_after_preflight_invalidates_plan(self):
        w=world();j=observed(w);cast(j);tx,wallet,before=self.prepared(j)
        j.lose_gear('lost','b','b:coat',1,actual_loss=True);self.rejects(tx,wallet,before)
        self.assertIn('b:coat',w.bodies['b'].lost_items)

    def test_shared_cadence_change_is_conserved_but_stales_old_quote_plan(self):
        w,ds,d,j=fixture();shift(j,ds);tx,wallet,before=self.prepared(j)
        d.cadence['dissonance']+=1;j.validate();self.rejects(tx,wallet,before)

    def test_actual_final_hp_change_after_preflight_is_watched(self):
        w=world();j=observed(w);cast(j);tx,wallet,before=self.prepared(j)
        w.bodies['b'].life.hp=1;self.rejects(tx,wallet,before)

    def test_historical_form_mutable_local_permission_is_watched(self):
        w,ds,d,j=fixture();shift(j,ds);old=d.current
        j.wallets['a'].bonus_action=True;j.revert('revert','a',1,j.wallets['a'],legal=True)
        tx,wallet,before=self.prepared(j);old.spent.add('unobserved')
        self.rejects(tx,wallet,before)

    def test_completed_rest_after_preflight_conserves_refill_and_stales_plan(self):
        w,ds,d,j=fixture();shift(j,ds);j.druid_clock_transition('leave','a',1,transition='leave')
        tx,wallet,before=self.prepared(j)
        j.druid_rest('rest',ds,1,601,kind='long',actual_completed=True)
        self.rejects(tx,wallet,before);self.assertEqual(d.long_epoch,1)

    def test_ended_callback_pin_removal_after_preflight_stales_plan(self):
        w=world();j=observed(w);cast(j);j.end_concentration('end','a',1,reason='failed-save')
        tx,wallet,before=self.prepared(j);j._slot_pins.clear();self.rejects(tx,wallet,before)

    def test_new_dynamic_body_field_is_not_silently_unwatched(self):
        w=world();j=observed(w);tx,wallet,before=self.prepared(j)
        w.bodies['a'].unknown=1;self.rejects(tx,wallet,before)

    def test_shared_life_binding_replacement_after_preflight_rejects(self):
        w=world();j=observed(w);tx,wallet,before=self.prepared(j)
        w.bodies['b'].life=deepcopy(w.bodies['b'].life);self.rejects(tx,wallet,before)


if __name__=='__main__':
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(ParentWatchTests);count=suite.countTestCases()
    result=unittest.TextTestRunner(verbosity=2).run(suite);root=Path(__file__).resolve().parents[1]
    report={'status':'PASS' if result.wasSuccessful() else 'FAIL','testMethods':count,
      'scope':'Candidate full current parent graph staleness watches; no parent restore planning/admission',
      'helperSha256':hashlib.sha256((root/'tools/temporal_parent_watches.py').read_bytes()).hexdigest(),
      'independentReview':'Pending integration with the complete parent planner',
      'parentRuntimeIntegrated':False,'fullTimeLoopOperational':False,'remainingMajorIntegrations':7,
      'failures':len(result.failures),'errors':len(result.errors)}
    (root/'docs/mechanics/TEMPORAL_PARENT_WATCH_VALIDATION.json').write_text(json.dumps(report,indent=2)+'\n')
    raise SystemExit(0 if result.wasSuccessful() else 1)
