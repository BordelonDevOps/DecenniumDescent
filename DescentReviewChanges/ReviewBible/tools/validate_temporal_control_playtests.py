"""Integration regressions for the temporal control/pulse bridge in progress."""
from copy import deepcopy
from pathlib import Path
import hashlib
import json
import unittest

from temporal_control_playtest_rules import CanonicalPulseWallet, ConservedPulseOutputs
from temporal_playtest_rules import ClockMarker, Scheduler, Wallet, SpellRuleError
from healing_pulse_playtest_rules import PulseSeries, RecipientLedger, NativeOccurrenceLedger
from validate_temporal_playtests import scene, event


class PulsePaymentTests(unittest.TestCase):
    def test_existing_maintenance_uses_real_rp_and_bonus_action(self):
        w = scene(); wallet = CanonicalPulseWallet(w, 'a')
        series = PulseSeries('briar-1', 'healing-briar', ClockMarker(0),
            tuple(ClockMarker(t) for t in (6,12,18)), RecipientLedger(),
            maintenance_ends=tuple(ClockMarker(t,20) for t in (5,11,17)))
        series.resolve(0,ClockMarker(0),('b',),wallet,round_number=1)
        self.assertEqual((w.wallets['a'].rp,w.wallets['a'].bonus_action),(10,True))
        series.resolve(1,ClockMarker(6),('b',),wallet,round_number=2)
        self.assertEqual((w.wallets['a'].rp,w.wallets['a'].bonus_action),(9,False))

    def test_existing_song_uses_real_rc_without_local_pool(self):
        w = scene(); wallet = CanonicalPulseWallet(w, 'a')
        series = PulseSeries('song-1','song-of-mending',ClockMarker(0),
            (ClockMarker(6),ClockMarker(12)),RecipientLedger(),roster=('b',))
        series.resolve(0,ClockMarker(0),('b',),wallet,round_number=1)
        series.resolve(1,ClockMarker(6),('b',),wallet,round_number=2)
        self.assertEqual((w.scheduler.rc['a'],w.wallets['a'].rp),(4,10))
        self.assertFalse({'rp','rc','bonus_action'} & vars(wallet).keys())

    def test_payment_bridge_observes_real_time_loop_resource_result(self):
        w = scene(); wallet = CanonicalPulseWallet(w, 'a')
        wallet.spend(2,'RC'); wallet.spend(4,'RP',bonus_action=True)
        event(w); w.kernel_plan('a').commit()
        self.assertEqual((wallet.rp,wallet.rc,wallet.bonus_action),(6,5,True))
        wallet.spend(1,'RC'); self.assertEqual(w.scheduler.rc['a'],4)

    def test_insufficient_payment_and_unavailable_action_are_atomic(self):
        for currency,amount,ba in [('RP',11,True),('RC',6,True),('RP',1,True)]:
            with self.subTest(currency=currency,amount=amount):
                w = scene(); wallet = CanonicalPulseWallet(w,'a')
                if amount==1:w.wallets['a'].bonus_action=False
                before=deepcopy((vars(w.wallets['a']),w.scheduler.rc))
                with self.assertRaises(SpellRuleError):wallet.spend(amount,currency,bonus_action=ba)
                self.assertEqual((vars(w.wallets['a']),w.scheduler.rc),before)

    def test_changed_canonical_bindings_reject_without_spending(self):
        for change in ('wallet','registry','scheduler','actor','alias'):
            with self.subTest(change=change):
                w=scene(); wallet=CanonicalPulseWallet(w,'a')
                if change=='wallet':w.wallets['a']=Wallet(rp=99)
                elif change=='registry':w.wallets=dict(w.wallets)
                elif change=='scheduler':w.scheduler=Scheduler('other',('a','b','foe'))
                elif change=='actor':del w.lives['a']
                else:w.wallets['b']=w.wallets['a']
                before=deepcopy(({a:vars(v) for a,v in w.wallets.items()},w.scheduler.rc))
                with self.assertRaises(SpellRuleError):wallet.spend(1)
                self.assertEqual(({a:vars(v) for a,v in w.wallets.items()},w.scheduler.rc),before)

    def test_unknown_actor_and_initial_alias_rejected(self):
        w=scene()
        with self.assertRaises(SpellRuleError):CanonicalPulseWallet(w,'unknown')
        w.wallets['b']=w.wallets['a']
        with self.assertRaises(SpellRuleError):CanonicalPulseWallet(w,'a')

    def test_missing_rc_allows_zero_cost_without_creating_balance(self):
        w=scene(); wallet=CanonicalPulseWallet(w,'foe')
        wallet.spend(0,'RC')
        self.assertNotIn('foe',w.scheduler.rc)
        with self.assertRaises(SpellRuleError):wallet.spend(1,'RC')
        self.assertNotIn('foe',w.scheduler.rc)

    def test_invalid_cost_and_malformed_balances_reject(self):
        cases=[(-1,'RP',False),(True,'RP',False),(1,'Ki',False),(1,'RP',1)]
        for amount,currency,ba in cases:
            with self.subTest(case=(amount,currency,ba)):
                w=scene(); wallet=CanonicalPulseWallet(w,'a')
                with self.assertRaises(SpellRuleError):wallet.spend(amount,currency,bonus_action=ba)
                self.assertEqual((w.wallets['a'].rp,w.scheduler.rc['a']),(10,5))
        w=scene(); wallet=CanonicalPulseWallet(w,'a');w.scheduler.rc['a']=True
        with self.assertRaises(SpellRuleError):wallet.spend(0,'RC')

    def test_existing_native_pulse_spends_canonical_wallet(self):
        w=scene(); wallet=CanonicalPulseWallet(w,'a'); ledger=NativeOccurrenceLedger()
        self.assertTrue(ledger.commit('aura-of-grace','a',ClockMarker(6),wallet))
        self.assertFalse(ledger.commit('aura-of-grace','a',ClockMarker(6),wallet))
        self.assertEqual(w.wallets['a'].rp,9)

    def test_payment_does_not_change_finite_use_history(self):
        w=scene();w.wallets['a'].used.add('long-rest-source')
        CanonicalPulseWallet(w,'a').spend(1,'RP',bonus_action=True)
        self.assertEqual(w.wallets['a'].used,{'long-rest-source'})


def output_fixture(profile='transcendent-meditation'):
    w=scene(); guard=ConservedPulseOutputs(w)
    kw={'roster':('a','b')} if profile=='transcendent-meditation' else {
        'maintenance_ends':tuple(ClockMarker(t,20) for t in (5,11,17))}
    series=PulseSeries('effect-1',profile,ClockMarker(0),
        tuple(ClockMarker(t) for t in (6,12,18)),RecipientLedger(),**kw)
    source=('monk.hero.enlightened-master.transcendent-meditation' if profile=='transcendent-meditation'
            else 'cleric.base.sacred-chant')
    guard.register(series,'a',source)
    return w,guard,series


class IndependentOutputTests(unittest.TestCase):
    def pulse(self,guard,index,*,suppressed=False,real=True,event_id=None):
        _,_,profile=guard._binding('effect-1')
        targets=('a','b') if profile=='transcendent-meditation' else ()
        return guard.resolve('effect-1',index,ClockMarker(index*6),targets,
            event_id=event_id or 'pulse-'+str(index),round_number=index+1,
            real_encounter=real,whole_effect_suppressed=suppressed)

    def test_meditation_real_second_pulse_allows_ki_once(self):
        w,g,s=output_fixture()
        self.assertEqual(self.pulse(g,0)['independentKi'],0)
        self.assertEqual(self.pulse(g,1)['independentKi'],1)
        self.assertEqual(self.pulse(g,2)['independentKi'],0)
        self.assertEqual(g.consumed,{('effect-1',1,'Ki')})

    def test_sacred_chant_real_third_pulse_allows_conviction_once(self):
        w,g,s=output_fixture('sacred-chant')
        self.assertEqual(self.pulse(g,0)['independentConviction'],0)
        self.assertEqual(self.pulse(g,1)['independentConviction'],0)
        w.wallets['a'].bonus_action=True  # Host's actual next-turn refresh.
        self.assertEqual(self.pulse(g,2)['independentConviction'],1)
        self.assertEqual(g.consumed,{('effect-1',2,'Conviction')})

    def test_replayed_snapshot_pending_pulse_cannot_duplicate_ki(self):
        w,g,s=output_fixture();self.pulse(g,0)
        saved=deepcopy((s.states,s.declarations))
        self.assertEqual(self.pulse(g,1)['independentKi'],1)
        # Isolated output-conservation regression: restore only a series view.
        # This is not a complete temporal source adapter/admission claim.
        s.states,s.declarations=deepcopy(saved);w.scheduler.iteration=1
        result=self.pulse(g,1,event_id='new-iteration-pulse')
        self.assertTrue(result['occurred'])
        self.assertEqual(result['outputTargets'],('a','b'))
        self.assertEqual(result['independentKi'],0)
        self.assertEqual(len(g.events),3)

    def test_suppressed_occurrence_consumes_resource_entitlement(self):
        w,g,s=output_fixture();self.pulse(g,0);saved=deepcopy((s.states,s.declarations))
        self.assertEqual(self.pulse(g,1,suppressed=True)['independentKi'],0)
        s.states,s.declarations=deepcopy(saved);w.scheduler.iteration=1
        self.assertEqual(self.pulse(g,1,event_id='after-suppression')['independentKi'],0)

    def test_at_resource_cap_still_consumes_opportunity(self):
        w,g,s=output_fixture();self.pulse(g,0);saved=deepcopy((s.states,s.declarations))
        real_ki=5
        real_ki=min(5,real_ki+self.pulse(g,1)['independentKi'])
        self.assertEqual(real_ki,5)
        s.states,s.declarations=deepcopy(saved);w.scheduler.iteration=1;real_ki=3
        real_ki=min(5,real_ki+self.pulse(g,1,event_id='after-spend')['independentKi'])
        self.assertEqual(real_ki,3)

    def test_unreached_resource_occurrence_remains_available(self):
        w,g,s=output_fixture();self.pulse(g,0);w.scheduler.iteration=1
        self.assertEqual(self.pulse(g,1,event_id='first-real-second')['independentKi'],1)

    def test_outside_encounter_chant_does_not_generate_conviction(self):
        w,g,s=output_fixture('sacred-chant');self.pulse(g,0,real=False)
        self.pulse(g,1,real=False);w.wallets['a'].bonus_action=True
        self.assertEqual(self.pulse(g,2,real=False)['independentConviction'],0)
        self.assertEqual(g.consumed,{('effect-1',2,'Conviction')})

    def test_duplicate_event_rejects_before_source_or_payment_changes(self):
        w,g,s=output_fixture('sacred-chant');self.pulse(g,0)
        before=deepcopy((s.states,vars(w.wallets['a']),g.events,g.consumed))
        with self.assertRaisesRegex(SpellRuleError,'event replay'):
            self.pulse(g,1,event_id='pulse-0')
        self.assertEqual((s.states,vars(w.wallets['a']),g.events,g.consumed),before)

    def test_no_output_for_future_or_already_committed_pulse(self):
        w,g,s=output_fixture()
        with self.assertRaises(SpellRuleError):
            g.resolve('effect-1',1,ClockMarker(3),('a','b'),event_id='early',
                round_number=1,real_encounter=True)
        self.assertFalse(g.events);self.assertFalse(g.consumed)
        # A missed prepaid first pulse does not invalidate a later actual due
        # pulse. Test an early request, not that legitimate source behavior.
        w,g,s=output_fixture();self.pulse(g,0)
        with self.assertRaises(SpellRuleError):self.pulse(g,0,event_id='copy-old')
        self.assertNotIn('copy-old',g.events)

    def test_canonical_identity_and_source_mutations_reject(self):
        for mutation in ('instance','profile','source','duplicate'):
            with self.subTest(mutation=mutation):
                w,g,s=output_fixture()
                if mutation=='instance':s.instance_id='reused'
                elif mutation=='profile':s.profile_name='sacred-chant'
                elif mutation=='source':
                    with self.assertRaises(SpellRuleError):g.register(s,'a','cleric.base.sacred-chant')
                    continue
                else:
                    with self.assertRaises(SpellRuleError):g.register(s,'a','monk.hero.enlightened-master.transcendent-meditation')
                    continue
                with self.assertRaises(SpellRuleError):self.pulse(g,0)
                self.assertFalse(g.events)

    def test_failed_bonus_action_does_not_consume_future_resource_output(self):
        w,g,s=output_fixture('sacred-chant');self.pulse(g,0);self.pulse(g,1)
        with self.assertRaises(SpellRuleError):self.pulse(g,2)
        self.assertFalse(g.consumed)
        self.assertEqual(s.states[2],'pending')

    def test_real_healing_targets_do_not_control_independent_ki(self):
        w,g,s=output_fixture();self.pulse(g,0)
        result=g.resolve('effect-1',1,ClockMarker(6),(),event_id='no-eligible-heal',
            round_number=2,real_encounter=True)
        self.assertEqual(result['outputTargets'],())
        self.assertEqual(result['independentKi'],1)


if __name__=='__main__':
    suite=unittest.TestSuite(unittest.defaultTestLoader.loadTestsFromTestCase(cls)
                             for cls in (PulsePaymentTests,IndependentOutputTests))
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    root=Path(__file__).resolve().parents[1]
    report={'status':'PASS' if result.wasSuccessful() else 'FAIL','testMethods':result.testsRun,
            'failures':len(result.failures),'errors':len(result.errors),
            'helperSha256':hashlib.sha256((root/'tools/temporal_control_playtest_rules.py').read_bytes()).hexdigest(),
            'scope':'Canonical payment and resolved Ki/Conviction output guards; timing/source restoration unimplemented; independent review pending',
            'fullTimeLoopOperational':False}
    (root/'docs/mechanics/TEMPORAL_CONTROL_VALIDATION.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    raise SystemExit(0 if result.wasSuccessful() else 1)
