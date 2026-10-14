# Actual incremental pulse payment/output code — 22 tests

Your nine-part policy conference is preserved in GPT_TEMPORAL_CONTROL_PULSE_BOUNDARIES.md. I accept the Sacred Chant Conviction addition, source-qualified rider distinctions, and one-evaluation-only native regular starts. No new original source text is needed. No full integration or full-game closure is claimed.

Here is the first concrete portion: the canonical pulse payment facade and the resolved independent-output guard using actual existing PulseSeries.resolve calls. All22 methods pass. Foundation helper SHA b821829ed352e69ce1ecf3c3d753f0206c8f8d2ec5a5d64bc89d5fd7d8a72151 remains unchanged. This incremental helper does not yet admit active control/pulse state into TemporalKernel. All seven integrations remain counted as missing.

Please review this code for defects inside its stated payment/resolved-output scope. Source-clock restoration, authentic start receipts, missed-output treatment, parent concentration, and final Ki/Conviction resource application are explicitly still missing; do not treat these22 checks as proof of those adapters. The host must apply a returned allowance once within the same atomic event to its actual capped resource holder. This helper contains no Ki/Conviction pool. The next full adapter must join that mutation to its source transaction.

Two source wording clarifications before clock code:

1. Your maintenance paragraph said failed payment has no retry, but the existing reviewed guide explicitly preserves an early failed ordinary maintenance opportunity until that turn's end; only exact-due paid sequences/windows end immediately. Since your conference expressly does not reopen ordinary behavior, I retain that distinction. Please confirm.
2. The actual immutable snapshot is initiative-start, before its first turn/event. A source created after that boundary cannot be restored as snapshot state. Existing pre-initiative pulse series normally have outside-origin preserved virtual markers. Your in-encounter logical-opportunity rule can apply only when the actual source was already present at the immutable boundary; no later source may relabel itself to gain snapshot membership. Please confirm this constraint and identify any authentic at-boundary origin case that needs separate support. I will not fabricate a turn or entry/cast at capture.

One initial test incorrectly expected a prepaid later pulse to fail merely because the first was missed; the existing helper correctly permits the later due opportunity. I corrected the test to exercise an actually early request, without changing ordinary source behavior. The initial result is preserved as TEMPORAL_CONTROL_FIRST_TEST_RESULT.json.

The current guide records both the settled policy and outstanding implementation. Please give a bounded code disposition or concrete counterexample. Full Time Loop, remaining game authorship, final joint flow confirmation and GitHub delivery are still open.


## tools/temporal_control_playtest_rules.py

```
"""Temporal control/pulse integration under construction, not full Time Loop.

This first bridge lets the existing pulse helper spend the canonical RP, RC and
Bonus Action. It owns no second resource pool and changes no source timing.
Remaining source policies require their actual notebook conference and review.
"""
from device_lifecycle_playtest_rules import Wallet
from healing_pulse_playtest_rules import PulseSeries, PROFILES
from spell_playtest_rules import integer
from temporal_playtest_rules import Scheduler, TemporalKernel, ident, require, shape


class CanonicalPulseWallet:
    """Duck-typed spend interface used by the reviewed PulseSeries helper.

Bind once to a known host actor. Every spend verifies that its scene, scheduler,
registry and Wallet aliases still designate those same canonical objects. RC
comes from Scheduler.rc, the encounter resource explicitly restored by the
kernel; RP/used-history remain on the real Wallet. There is no local balance.
"""
    def __init__(self, kernel, actor):
        require(isinstance(kernel, TemporalKernel), 'Canonical temporal host required')
        ident(actor)
        require(actor in kernel.wallets and actor in kernel.lives, 'Canonical pulse actor required')
        self.kernel = kernel
        self.actor = actor
        self._scheduler = kernel.scheduler
        self._registry = kernel.wallets
        self._wallet = kernel.wallets[actor]
        self._validate()

    def _validate(self):
        require(self.kernel.scheduler is self._scheduler and self.kernel.wallets is self._registry
                and self._registry.get(self.actor) is self._wallet,
                'Canonical pulse binding changed')
        require(self.actor in self.kernel.lives, 'Canonical pulse actor disappeared')
        require(len({id(w) for w in self._registry.values()}) == len(self._registry),
                'Pulse actors cannot share one Wallet')
        shape(self._scheduler, Scheduler)
        shape(self._wallet, Wallet)
        integer(self._wallet.rp, 'canonical RP', 0)
        require(type(self._wallet.bonus_action) is bool, 'Canonical Bonus Action must be boolean')
        require(type(self._scheduler.rc) is dict, 'Canonical RC registry required')

    @property
    def rp(self):
        self._validate()
        return self._wallet.rp

    @property
    def rc(self):
        self._validate()
        value = self._scheduler.rc.get(self.actor, 0)
        return integer(value, 'canonical RC', 0)

    @property
    def bonus_action(self):
        self._validate()
        return self._wallet.bonus_action

    def spend(self, amount, currency='RP', *, bonus_action=False):
        self._validate()
        integer(amount, 'pulse cost', 0)
        require(currency in ('RP', 'RC'), 'Unknown pulse currency')
        require(type(bonus_action) is bool, 'Explicit Bonus Action cost required')
        balance = self.rp if currency == 'RP' else self.rc
        require(balance >= amount, 'Required pulse resource unavailable')
        require(not bonus_action or self._wallet.bonus_action, 'Required pulse Bonus Action unavailable')
        # All checks precede mutation. Reference host holds its scene/event lock.
        if currency == 'RP':
            self._wallet.rp -= amount
        elif amount:
            self._scheduler.rc[self.actor] = balance - amount
        if bonus_action:
            self._wallet.bonus_action = False


# Zero-based pulse indexes. These keys identify conserved source opportunities,
# not new resource pools. Source acquisition/parent eligibility stay with host.
INDEPENDENT_OUTPUTS = {
    'transcendent-meditation': ('monk.hero.enlightened-master.transcendent-meditation',1,'Ki'),
    'sacred-chant': ('cleric.base.sacred-chant',2,'Conviction'),
}


class ConservedPulseOutputs:
    """Guard actual resolved outputs through the existing PulseSeries method.

This is the resolution boundary only. It does not restore series, validate their
parent concentration, or authorize a due marker. The eventual temporal source
adapter must provide those. It retains one canonical series object per identity
and never grants the same instance/index resource twice, even across iterations.

Returned allowances must be applied once in the host's same atomic event to its
real resource holder with the printed cap. This guard owns no Ki or Conviction.
Missed/expired clock events still require the source-clock adapter; no method
here fabricates an occurrence from an old committed state or a supplied receipt.
"""
    def __init__(self, kernel):
        require(isinstance(kernel, TemporalKernel),'Canonical temporal host required')
        self.kernel = kernel
        self.series = {}
        self.consumed = set()
        self.events = {}

    def register(self, series, owner, source_id):
        require(type(series) is PulseSeries, 'Canonical PulseSeries required')
        require(series.profile_name in INDEPENDENT_OUTPUTS,'Unsupported independent-output source')
        expected = INDEPENDENT_OUTPUTS[series.profile_name][0]
        require(source_id == expected,'Independent-output source/profile mismatch')
        ident(series.instance_id)
        require(series.instance_id not in self.series,'Canonical pulse identity already registered')
        CanonicalPulseWallet(self.kernel,owner)
        self.series[series.instance_id] = (series,owner,source_id,series.profile_name)

    def _binding(self, instance):
        require(instance in self.series,'Unknown independent-output instance')
        series,owner,source_id,profile = self.series[instance]
        require(type(series) is PulseSeries and series.instance_id == instance
                and series.profile_name == profile and series.profile == PROFILES[profile]
                and source_id == INDEPENDENT_OUTPUTS[profile][0],
                'Independent-output canonical binding changed')
        return series,owner,profile

    def resolve(self, instance, index, now, targets, *, event_id, round_number,
                real_encounter, regular=True, upkeep_legal=True,
                whole_effect_suppressed=False):
        ident(event_id)
        require(event_id not in self.events,'Independent-output event replay')
        require(type(real_encounter) is bool and type(whole_effect_suppressed) is bool,
                'Explicit encounter and suppression state required')
        series,owner,profile = self._binding(instance)
        wallet = CanonicalPulseWallet(self.kernel,owner)
        # This call actually resolves a pending opportunity; reading a historical
        # series state or passing a copied result is not sufficient.
        result = series.resolve(index,now,targets,wallet,round_number=round_number,
            regular=regular,upkeep_legal=upkeep_legal,
            whole_effect_suppressed=whole_effect_suppressed)
        _,output_index,resource = INDEPENDENT_OUTPUTS[profile]
        key = (instance,index,resource)
        allowance = 0
        if index == output_index:
            first = key not in self.consumed
            self.consumed.add(key)  # Suppressed/capped occurrences never bank.
            allowance = int(first and not whole_effect_suppressed
                            and (profile != 'sacred-chant' or real_encounter))
        # Replace the old helper's unguarded Ki flag rather than returning two
        # independently usable authorizations for the same resource component.
        result['independentKi'] = allowance if resource == 'Ki' else 0
        result['independentConviction'] = allowance if resource == 'Conviction' else 0
        result['resourceOwner'] = owner
        result['occurrenceId'] = event_id
        result['iteration'] = self.kernel.scheduler.iteration
        self.events[event_id] = {'instance':instance,'index':index,
            'iteration':self.kernel.scheduler.iteration,'resource':resource,
            'allowance':allowance,'wholeSuppressed':whole_effect_suppressed}
        return result

```


## tools/validate_temporal_control_playtests.py

```
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

```


## docs/mechanics/TEMPORAL_CONTROL_PLAYTEST.md

```
# Time Loop: control and healing-pulse integration

**Source policies discussed; implementation in progress. Full Time Loop remains unavailable.**

The [actual nine-part conference](../../../../docs/audit/2026-10-08/full-game/GPT_TEMPORAL_CONTROL_PULSE_BOUNDARIES.md) supplements the [twelve world-conservation decisions](../../../../docs/audit/2026-10-08/full-game/GPT_TEMPORAL_WORLD_BOUNDARIES.md). The existing [control](CONTROL_STATES_PLAYTEST.md) and [pulse](HEALING_PULSE_PLAYTEST.md) guides continue to own ordinary source behavior. No original card was changed.

## Agreed temporal behavior

| State | Temporal rule |
| --- | --- |
| Explicit source/target regular endpoints | Restore remaining logical progress with authentic new-iteration regular markers. World elapsed time does not move backward, and restoration creates no marker event. |
| Current actual-turn endings | Remain attached to the actual application turn. The initiative-start snapshot has no active turn; a pending in-turn attachment there is invalid. Outside-turn +6-second endpoints retain their absolute deadline. |
| Outside-origin pulse schedules | Keep their original virtual markers and absolute deadlines. Entering initiative or using Time Loop does not restart them. Origin must be recorded explicitly. |
| Speed records | Same application, exact source/component/profile and valid endpoint. Do not reapply or refresh. Current external suppression remains authoritative. Aura, net, form, serum and creature children require their actual parent adapters. Hypermutation's floor is systemic parent state, not a hostile slow. |
| Guiding Bolt's Star mark | Restore its two separate entitlements. Keep the same mark identity and monotonic attack-token history; pending attacks block capture and preflight. |
| Wrathful Brand | Restore the separate owner/ally riders and snapshot timed parent. No new damage, healing or save event occurs at restore. |
| One-shot riders | Use exact parent/application/source/component identities and a finite trigger table. Vein Cutter consumes on its qualifying attack hit; Crippling Lash specifically requires a weapon hit. Omen Reader's once/encounter attack adjustment is distinct from the resulting timed star-ash. |
| Divine Judgment reflection | Retain historical actual-turn consumption. A genuinely new iteration turn can qualify, including a separately authenticated extra turn. Ordinary repeat saves and expiry still use regular markers. |
| PulseSeries | Restore snapshot pending/funded/consumed state under the same valid parent and fixed roster. No cast pulse or consumed-at-snapshot opportunity replays. A later pending paid pulse pays its current printed cost when actually due. |
| Recipient budgets | Retain history with domain, target and iteration-round identity. Circle of Harmony remains shared across owners in the same iteration-round. |
| Eternal Bloom | Preserve the original missing-HP capture and shares. Restore only snapshot installment availability; retain old consumption history. Do not grow the reserve from later damage. Its survival floor is separate. |
| First-contact cures | Restore snapshot instance/recipient entitlements. Garden uses entry/start; Enhanced Garden and Seed use their reviewed pulse event. Restore itself is none of these events. Real-rest recipient histories remain conserved. |
| Native healing | One evaluated opportunity at a genuine regular start during a real encounter. Decline, ineligibility or unavailable payment loses that start opportunity. Extra turns and downtime create no tick. A new iteration can supply a new genuine start, with current RP/reserves. |

**Resource-output conservation:** Transcendent Meditation's second pulse can supply1Ki only once for the same effect instance. Sacred Chant's third pulse can supply1Conviction only once for that instance. Reaching the occurrence while capped or while the whole effect is suppressed still consumes that resource opportunity. Healing may later replay under an authorized restored source without generating the same resource again. A never-reached opportunity remains eligible. Restoration itself grants neither resource.

For example, a Monk receives the second pulse's1Ki, then spends it. Rewinding to a snapshot where that pulse was pending can permit its healing again when legally due, but it cannot return that same1Ki. Sacred Chant uses the same conservation rule for Conviction.

The immutable snapshot is at initiative start. A source first created afterward is not silently added to that snapshot. An origin label cannot manufacture preexisting pulse state. Any logical-clock restoration must demonstrate that the actual source instance was already present in the captured state.

The conference's maintenance wording is read with its express instruction not to reopen ordinary mechanics: an early failed ordinary turn-window payment remains pending until the source's real turn-end deadline. Exact-due paid sequences/windows end immediately on failed upkeep. This wording clarification is being returned to the notebook before implementation of the scheduler.

## Current code and checks

`tools/temporal_control_playtest_rules.py` currently implements two limited bridges:

- `CanonicalPulseWallet` lets existing pulse helpers spend the real actor Wallet's RP/Bonus Action and the canonical Scheduler's RC. It owns no duplicate balances and rejects changed aliases before spending.
- `ConservedPulseOutputs` wraps actual `PulseSeries.resolve()` calls for the two resource-producing profiles. It retains unique occurrence IDs and conserved instance/index/component opportunities; it replaces the helper's raw Ki flag with the guarded allowance. Suppressed or capped resolved occurrences cannot be banked. Sacred Chant cannot generate Conviction outside a real encounter.

The returned resource allowance must be applied once by the host in the same atomic event, subject to the actual resource cap. These helpers do not themselves own, increment or restore Ki/Conviction. Source acquisition, legal recipients, actual parent concentration and authenticated due-event scheduling remain host/source-adapter responsibilities. The output guard cannot certify them.

[Validation](TEMPORAL_CONTROL_VALIDATION.json):22 focused methods pass. They exercise the actual existing maintenance, Song, Meditation, Chant and native payment interfaces, plus duplicate output, cap, suppression, early/duplicate occurrence and canonical-alias cases. A replay test deliberately resets only an isolated series view; it demonstrates the output guard, not a complete Time Loop source restoration. Independent code review is pending.

## Still required

All nine-family restoration remains in progress. No supported-adapter count or ordinary catalog status has been promoted. Required work includes source clock descriptors, same-object serialization and restoration, complete shared recipient history, parent/concentration callbacks, missed-output reconciliation, native-start receipts, installment/contact history, and their joint transaction tests.

Rapid Coagulation additionally needs the canonical previous-turn movement baseline from the initiative snapshot. It remains unsupported until that state exists. Net Bolt, Totem/Echo, Nano-Aegis, auras and other dependent sources remain unavailable to Time Loop without their physical/device/parent adapters. The seven major integrations and final whole-game/GitHub gate remain open.

```


## docs/mechanics/TEMPORAL_CONTROL_VALIDATION.json

```
{
  "status": "PASS",
  "testMethods": 22,
  "failures": 0,
  "errors": 0,
  "helperSha256": "835a108a80e5ad8c5d030dbf7d927e0491bc944eb2697d71f2504fd2e0b1df12",
  "scope": "Canonical payment and resolved Ki/Conviction output guards; timing/source restoration unimplemented; independent review pending",
  "fullTimeLoopOperational": false
}

```
