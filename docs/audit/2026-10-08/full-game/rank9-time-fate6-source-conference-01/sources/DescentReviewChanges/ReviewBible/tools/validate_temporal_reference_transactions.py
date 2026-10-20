"""Exact-parent reference transport tests; not full parent restoration tests."""
from copy import deepcopy
from pathlib import Path
from types import SimpleNamespace
import hashlib,json,unittest

from temporal_playtest_rules import Transaction,Wallet,SpellRuleError
from transformation_spell_playtest_rules import ConcentrationLedger
from validate_temporal_parent_history import fixture,shift,observed,world,cast


def form_fixture():
    w,ds,d,j=fixture();shift(j,ds);old=d.current
    j.wallets['a'].bonus_action=True;j.revert('revert','a',1,j.wallets['a'],legal=True)
    return w,ds,d,j,old


class ExplodingWrite:
    """Inject a later assignment failure to exercise rollback of earlier writes."""
    def __init__(self):object.__setattr__(self,'value',0)
    def __setattr__(self,name,value):
        if value==1:raise RuntimeError('injected later field assignment failure')
        object.__setattr__(self,name,value)


class ReferenceTransactionTests(unittest.TestCase):
    def test_restore_exact_historical_form_reference_without_entry_payment(self):
        w,ds,d,j,old=form_fixture();resources=(d.shifts,d.reserve,d.surges)
        tx=Transaction();tx.write(old,'state','active');tx.write_form_reference(d,old)
        self.assertIsNone(d.current);tx.commit()
        self.assertIs(d.current,old);self.assertEqual(old.state,'active')
        self.assertEqual((d.shifts,d.reserve,d.surges),resources)

    def test_reject_equal_looking_noncanonical_form_before_staging(self):
        w,ds,d,j,old=form_fixture();tx=Transaction()
        with self.assertRaisesRegex(SpellRuleError,'canonical instance identity'):
            tx.write_form_reference(d,deepcopy(old))
        self.assertFalse(tx.writes);self.assertIsNone(d.current)

    def test_reference_retirement_invokes_no_ordinary_end_hook(self):
        w,ds,d,j=fixture();shift(j,ds);old=d.current;grants=deepcopy(w.buffers.grants)
        tx=Transaction();tx.write_form_reference(d,None);tx.commit()
        self.assertIsNone(d.current);self.assertEqual(old.state,'active')
        self.assertEqual(w.buffers.grants,grants)
        # This demonstrates why the parent planner must stage child cleanup.

    def test_instance_registry_replacement_between_stage_and_commit_rejects(self):
        w,ds,d,j,old=form_fixture();tx=Transaction();tx.write_form_reference(d,old)
        d.instances=dict(d.instances)
        with self.assertRaisesRegex(SpellRuleError,'binding changed'):tx.commit()
        self.assertIsNone(d.current)

    def test_instance_object_replacement_between_stage_and_commit_rejects(self):
        w,ds,d,j,old=form_fixture();tx=Transaction();tx.write_form_reference(d,old)
        d.instances['F']=deepcopy(old)
        with self.assertRaisesRegex(SpellRuleError,'registry changed'):tx.commit()
        self.assertIsNone(d.current)

    def test_form_identity_edit_between_stage_and_commit_rejects(self):
        w,ds,d,j,old=form_fixture();tx=Transaction();tx.write_form_reference(d,old)
        old.instance_id='replacement'
        with self.assertRaisesRegex(SpellRuleError,'Stale temporal plan'):tx.commit()
        self.assertIsNone(d.current)

    def test_reference_and_data_writes_share_conflict_detection(self):
        w,ds,d,j,old=form_fixture();tx=Transaction();tx.write_form_reference(d,old)
        with self.assertRaisesRegex(SpellRuleError,'Conflicting adapters'):tx.write(d,'current',None)
        with self.assertRaisesRegex(SpellRuleError,'Conflicting adapters'):tx.write_form_reference(d,None)

    def test_same_id_new_concentration_tuple_is_not_original(self):
        w=world();j=observed(w);cast(j);slot=w.concentration.current['a']
        fake=tuple([slot[0],slot[1]]);self.assertIsNot(fake,slot)
        tx=Transaction()
        with self.assertRaisesRegex(SpellRuleError,'retained original identity'):
            tx.write_concentration_references(w.concentration,{'a':fake},retained_slots=j._slot_pins)
        self.assertIs(w.concentration.current['a'],slot)

    def test_restore_exact_callback_then_actual_end_reaches_original_link(self):
        w=world();j=observed(w);cast(j);slot=w.concentration.current['a']
        body=w.bodies['b'];saved_body={k:deepcopy(v) for k,v in vars(body).items() if k not in ('life','origin')}
        saved_anatomies=dict(w.buffers.spell_anatomies)
        j.end_concentration('end','a',1,reason='failed-save');events=deepcopy(w.events)
        tx=Transaction()
        for name,value in saved_body.items():tx.write(body,name,value)
        tx.write(w.links['C:b'],'state','shaping');tx.write(w.casts['C'],'state','active')
        tx.write(w.buffers,'spell_anatomies',saved_anatomies)
        tx.write_concentration_references(w.concentration,{'a':slot},retained_slots=j._slot_pins)
        tx.commit();self.assertIs(w.concentration.current['a'],slot)
        self.assertEqual(w.events,events);self.assertEqual(w.links['C:b'].state,'shaping')
        w.concentration.end('a','voluntary-release')
        self.assertEqual(w.links['C:b'].state,'voluntary-release');self.assertIsNone(body.anatomy)
        self.assertEqual(len(w.events),len(events)+1)

    def test_concentration_input_map_is_detached_but_slot_is_not_copied(self):
        w=world();j=observed(w);cast(j);slot=w.concentration.current['a'];after={'a':slot}
        tx=Transaction();tx.write_concentration_references(w.concentration,after,retained_slots=j._slot_pins)
        after.clear();tx.commit();self.assertIs(w.concentration.current['a'],slot)

    def test_live_concentration_change_rejects_all_writes_before_payment(self):
        w=world();j=observed(w);cast(j);slot=w.concentration.current['a'];wallet=j.wallets['a'];rp=wallet.rp
        tx=Transaction();tx.write(wallet,'rp',0)
        tx.write_concentration_references(w.concentration,{},retained_slots=j._slot_pins)
        w.concentration.current['a']=tuple([slot[0],lambda reason:None])
        with self.assertRaisesRegex(SpellRuleError,'registry changed'):tx.commit()
        self.assertEqual(wallet.rp,rp)

    def test_lost_retained_slot_before_commit_rejects(self):
        w=world();j=observed(w);cast(j);slot=w.concentration.current['a']
        j.end_concentration('end','a',1,reason='failed-save')
        tx=Transaction();tx.write_concentration_references(w.concentration,{'a':slot},retained_slots=j._slot_pins)
        j._slot_pins.clear()
        with self.assertRaisesRegex(SpellRuleError,'registry changed'):tx.commit()
        self.assertEqual(w.concentration.current,{})

    def test_prepared_reference_map_edit_rejects_before_any_write(self):
        w=world();j=observed(w);cast(j);slot=w.concentration.current['a'];wallet=j.wallets['a'];rp=wallet.rp
        tx=Transaction();tx.write(wallet,'rp',0)
        tx.write_concentration_references(w.concentration,{'a':slot},retained_slots=j._slot_pins)
        tx.writes[(id(w.concentration),'current')].after.clear()
        with self.assertRaisesRegex(SpellRuleError,'Prepared concentration'):tx.commit()
        self.assertEqual(wallet.rp,rp);self.assertIs(w.concentration.current['a'],slot)

    def test_failure_after_reference_writes_rolls_back_original_references(self):
        w,ds,d,j,old=form_fixture();ledger=w.concentration;original_map=ledger.current
        calls=[];slot=('original',lambda reason:calls.append(reason));pins={id(slot):slot}
        bad=ExplodingWrite();tx=Transaction();tx.write(old,'state','active')
        tx.write_form_reference(d,old);tx.write_concentration_references(ledger,{'a':slot},retained_slots=pins)
        tx.write(bad,'value',1)
        with self.assertRaises(RuntimeError):tx.commit()
        self.assertIsNone(d.current);self.assertEqual(old.state,'voluntary-reversion')
        self.assertIs(ledger.current,original_map);self.assertEqual(calls,[])
        self.assertFalse(tx.used)

    def test_audit_contains_identity_tokens_and_commit_cannot_repeat(self):
        w,ds,d,j,old=form_fixture();tx=Transaction();tx.labels[id(d)]='druid:a';tx.write_form_reference(d,old)
        row=tx.audit_rows()[0]
        self.assertEqual(row['after'],{'formId':'F','objectToken':id(old)})
        self.assertIsNone(row['before']);tx.commit()
        with self.assertRaisesRegex(SpellRuleError,'already committed'):tx.commit()


if __name__=='__main__':
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(ReferenceTransactionTests)
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    root=Path(__file__).resolve().parents[1]
    report={'status':'PASS' if result.wasSuccessful() else 'FAIL','testMethods':suite.countTestCases(),
        'scope':'Atomic original-reference transport only; parent legality/restoration planner still pending',
        'kernelSha256':hashlib.sha256((root/'tools/temporal_playtest_rules.py').read_bytes()).hexdigest(),
        'parentRuntimeIntegrated':False,'fullTimeLoopOperational':False,'remainingMajorIntegrations':7,
        'failures':len(result.failures),'errors':len(result.errors)}
    (root/'docs/mechanics/TEMPORAL_REFERENCE_TRANSACTION_VALIDATION.json').write_text(json.dumps(report,indent=2)+'\n')
    raise SystemExit(0 if result.wasSuccessful() else 1)
