"""Live-object integration regressions, not whole-game/Time Loop approval."""
from dataclasses import replace
from copy import deepcopy
from pathlib import Path
import hashlib
import json
import unittest

from validate_temporal_playtests import scene,event,history
from temporal_playtest_rules import ClockMarker,SpellRuleError
from temporal_control_world import (TemporalControlWorld,BoundEffect,TemporalRecipientLedger,
    GuidingStarMark,WrathfulBrand,OneShotRider,SpeedRecord,PerTurnReflection,
    PulseSeries,BloomReserve,FirstContactLedger,NativeOccurrenceLedger,payload,PULSE_SOURCES,CONCENTRATION_PROFILES)
from temporal_control_playtest_rules import CanonicalPulseWallet,ConservedPulseOutputs


def world():
    w=scene(capture=False);c=TemporalControlWorld(w.scheduler,outputs=ConservedPulseOutputs(w))
    w.integrations['control-pulses']=c
    return w,c


def attach(c,family,holder,source,component,*,identity='effect',owner='a',targets=('b',),
           deadline=ClockMarker(30),parent=None,concentration=None,origin='outside'):
    record=BoundEffect(identity,family,source,component,owner,targets,holder,origin,deadline,
                       concentration_id=concentration,parent_id=parent)
    c.register(record);return record


def star(c,**kw):
    return attach(c,'guiding',GuidingStarMark('a','b',ClockMarker(30),3),
        'oracle.supplement.stars.guiding-bolt','oracle.guiding-bolt.star-mark',**kw)


def capture(w):w.capture(('a','b','foe'))


def whole_state(w,c):
    # Assertion-only copy; production never deepcopies the live scene.
    return deepcopy((history(w),c.active,c.events,c.native_evaluations,c.outputs.consumed,c.outputs.events,
        {k:payload(r.holder) for k,r in c.records.items()},c.recipients.claimed,c.recipients.history))


class ControlTransactionTests(unittest.TestCase):
    def test_star_same_object_entitlements_restore_tokens_do_not_rewind(self):
        w,c=world();r=star(c);capture(w);h=r.holder
        token=h.begin_ally_attack(actor='foe',ally_of_owner=True,now=1)['attackToken']
        h.resolve_ally_attack(token,hit=True,now=1)
        event(w,now=2);before=whole_state(w,c);plan=w.kernel_plan('a')
        self.assertEqual(whole_state(w,c),before);plan.commit()
        self.assertIs(r.holder,h);self.assertTrue(h.active and h.attack_bonus_available and h.hit_rider_available)
        self.assertEqual(h._next_token,1)
        next_token=h.begin_ally_attack(actor='foe',ally_of_owner=True,now=3)['attackToken']
        self.assertNotEqual(next_token,token)
        with self.assertRaises(SpellRuleError):h.resolve_ally_attack(token,hit=True,now=3)

    def test_pending_attack_blocks_atomic_restore_without_cost(self):
        w,c=world();r=star(c);capture(w)
        r.holder.begin_ally_attack(actor='foe',ally_of_owner=True,now=1);event(w,now=2)
        before=whole_state(w,c)
        with self.assertRaisesRegex(SpellRuleError,'Mid-roll'):w.kernel_plan('a')
        self.assertEqual(whole_state(w,c),before)

    def test_brand_independent_entitlements_restore_in_place(self):
        w,c=world();h=WrathfulBrand('a','b',ClockMarker(30),ally_rider_available=False)
        attach(c,'brand',h,'oracle.supplement.flame.wrathful-brand','oracle.wrathful-brand')
        capture(w);h.trigger(actor='a',ally_of_owner=True,now=1,resolved_damage=4,direct_attack_hit=True,base_dice_total=8)
        event(w,now=2);w.kernel_plan('a').commit()
        self.assertTrue(h.owner_rider_available);self.assertFalse(h.ally_rider_available)

    def test_rider_actual_consumption_rewinds_history_remains(self):
        w,c=world();h=OneShotRider('hit')
        attach(c,'rider',h,'thief.hero.blackguard.crippling-lash','thief.crippling-lash.weapon-hit-damage-penalty')
        capture(w)
        self.assertTrue(c.trigger_rider(w,'effect','hit-one',qualifying=True,hit=True))
        event(w,now=2);w.kernel_plan('a').commit()
        self.assertTrue(h.available);self.assertIn('hit-one',c.events)
        with self.assertRaisesRegex(SpellRuleError,'replay'):c.trigger_rider(w,'effect','hit-one',qualifying=True,hit=True)

    def test_frozen_speed_value_updates_canonical_binding_atomically(self):
        w,c=world();h=SpeedRecord('effect','a','b','ray','ordinary','flat',10,expires=ClockMarker(30))
        r=attach(c,'speed',h,'ray-of-frost','ordinary.ray-of-frost.slow');capture(w)
        r.holder=replace(h,active=False)
        event(w,now=2);w.kernel_plan('a').commit()
        self.assertTrue(r.holder.active);self.assertIs(c.canonical['effect'],r)
        self.assertEqual(r.holder.application_id,'effect');c.validate(w)

    def test_world_expired_control_does_not_return(self):
        w,c=world();r=star(c);capture(w);event(w,now=31);w.kernel_plan('a').commit()
        self.assertNotIn('effect',c.active);self.assertFalse(r.holder.active)

    def test_unknown_speed_suppression_blocks_capture_and_restore(self):
        for initially_suppressed in (False,True):
            with self.subTest(initially_suppressed=initially_suppressed):
                w,c=world();h=SpeedRecord('effect','a','b','ray','ordinary','flat',10,
                                        expires=ClockMarker(30),suppressed=initially_suppressed)
                r=attach(c,'speed',h,'ray-of-frost','ordinary.ray-of-frost.slow')
                if initially_suppressed:
                    with self.assertRaisesRegex(SpellRuleError,'suppression provenance'):capture(w)
                else:
                    capture(w);r.holder=replace(h,suppressed=True);event(w,now=2)
                    before=whole_state(w,c)
                    with self.assertRaisesRegex(SpellRuleError,'suppression provenance'):w.kernel_plan('a')
                    self.assertEqual(whole_state(w,c),before)

    def test_added_concentration_schema_makes_prepared_plan_stale(self):
        w,c=world();star(c);capture(w);event(w,now=2);plan=w.kernel_plan('a')
        c.concentration.new_temporal_state={'unknown':True};before=whole_state(w,c)
        with self.assertRaises(SpellRuleError):plan.commit()
        self.assertEqual(whole_state(w,c),before)

    def test_post_snapshot_rider_retires_and_payment_stays_spent(self):
        w,c=world();capture(w);w.wallets['a'].rp-=2
        h=OneShotRider('hit');attach(c,'rider',h,'dragoon.hero.drake-rider.drake-mark','dragoon.drake-mark',origin='encounter')
        event(w,now=2);w.kernel_plan('a').commit()
        self.assertNotIn('effect',c.active);self.assertFalse(h.available);self.assertEqual(w.wallets['a'].rp,8)

    def test_unknown_or_mismatched_sources_block_admission(self):
        for change in ('source','component','holder','origin','extra'):
            with self.subTest(change=change):
                w,c=world();r=star(c)
                if change=='source':r.source='future'
                elif change=='component':r.component='future'
                elif change=='holder':r.holder=GuidingStarMark('a','b',ClockMarker(30),3)
                elif change=='origin':r.origin='encounter'
                else:r.holder.unclassified=True
                with self.assertRaises(SpellRuleError):capture(w)
                self.assertIsNone(w._snapshot)

    def test_stale_control_plan_rejects_before_any_core_write(self):
        for change in ('entitlement','record','registry','ledger'):
            with self.subTest(change=change):
                w,c=world();r=star(c);capture(w);event(w,now=2);plan=w.kernel_plan('a')
                if change=='entitlement':r.holder.active=False
                elif change=='record':r.deadline=ClockMarker(40)
                elif change=='registry':c.active.clear()
                else:c.recipients.claimed.add(('x','a',1))
                before=whole_state(w,c)
                with self.assertRaises(SpellRuleError):plan.commit()
                self.assertEqual(whole_state(w,c),before)

    def test_adapter_added_after_snapshot_blocks(self):
        w=scene();c=TemporalControlWorld(w.scheduler,outputs=ConservedPulseOutputs(w));w.integrations['control-pulses']=c
        event(w)
        with self.assertRaisesRegex(SpellRuleError,'adapter set changed'):w.kernel_plan('a')

    def test_external_target_is_not_silently_rewound(self):
        w=scene(capture=False,outsider=True);c=TemporalControlWorld(w.scheduler,outputs=ConservedPulseOutputs(w));w.integrations['control-pulses']=c
        h=GuidingStarMark('a','outside',ClockMarker(30),3)
        attach(c,'guiding',h,'oracle.supplement.stars.guiding-bolt','oracle.guiding-bolt.star-mark',targets=('outside',))
        capture(w);event(w,now=2)
        with self.assertRaisesRegex(SpellRuleError,'External control'):w.kernel_plan('a')


def pulse(c,profile,*,owner='a',identity='pulse',roster=('b',),concentration=None):
    mode_kwargs={}
    from healing_pulse_playtest_rules import PROFILES
    p=PROFILES[profile]
    if concentration is None:concentration=profile in CONCENTRATION_PROFILES
    starts=tuple(ClockMarker(6*(i+1)) for i in range(p.count))
    if p.mode=='maintenance':mode_kwargs['maintenance_ends']=tuple(ClockMarker(5+6*i,20) for i in range(p.count))
    h=PulseSeries(identity,profile,ClockMarker(0),starts,c.recipients,
                  roster=roster if p.fixed else (),**mode_kwargs)
    if concentration:c.concentration.start_committed(owner,identity,lambda reason: c.active.discard(identity))
    r=attach(c,'pulse',h,PULSE_SOURCES[profile],profile,identity=identity,owner=owner,targets=roster,
             deadline=h.expires,concentration=identity if concentration else None)
    return r


class PulseTransactionTests(unittest.TestCase):
    def test_future_pulse_cannot_acquire_snapshot_membership(self):
        w,c=world();h=PulseSeries('future','transcendent-meditation',ClockMarker(6),
            (ClockMarker(12),ClockMarker(18),ClockMarker(24)),c.recipients,roster=('b',))
        c.concentration.start_committed('a','future',lambda reason:c.active.discard('future'))
        attach(c,'pulse',h,PULSE_SOURCES['transcendent-meditation'],'transcendent-meditation',identity='future',
               concentration='future',deadline=h.expires)
        before=whole_state(w,c)
        with self.assertRaisesRegex(SpellRuleError,'did not exist'):capture(w)
        self.assertIsNone(w._snapshot);self.assertEqual(whole_state(w,c),before)

    def test_stale_or_expired_pulse_cannot_be_captured_active(self):
        for now in (7,19):
            with self.subTest(now=now):
                w,c=world();pulse(c,'garden');w.scheduler.now=ClockMarker(now);before=whole_state(w,c)
                with self.assertRaisesRegex(SpellRuleError,'before snapshot'):capture(w)
                self.assertIsNone(w._snapshot);self.assertEqual(whole_state(w,c),before)

    def test_all_remaining_families_require_exact_component(self):
        for family in ('pulse','bloom','contact','native'):
            with self.subTest(family=family):
                w,c=world()
                if family=='pulse':r=pulse(c,'song-of-mending')
                elif family=='bloom':
                    pulse(c,'eternal-bloom')
                    r=attach(c,'bloom',BloomReserve({'b':10}),PULSE_SOURCES['eternal-bloom'],'installments',
                        identity='reserve',deadline=ClockMarker(18),parent='pulse')
                elif family=='contact':
                    pulse(c,'garden')
                    r=attach(c,'contact',FirstContactLedger({'pulse':'garden'}),PULSE_SOURCES['garden'],
                        'first-contact',identity='contact',deadline=ClockMarker(18),parent='pulse')
                else:
                    r=attach(c,'native',NativeOccurrenceLedger(),'cleric.hero.saint.aura-of-grace',
                        'regular-heal',identity='native',targets=('a',),deadline=None)
                r.component='future.unreviewed.component';before=whole_state(w,c)
                with self.assertRaisesRegex(SpellRuleError,'component policy'):capture(w)
                self.assertEqual(whole_state(w,c),before)

    def test_malformed_collections_fail_before_resource_or_opportunity_mutation(self):
        for malformed in ('guard-consumed','recipient-history','pulse-declarations','native-consumed'):
            with self.subTest(malformed=malformed):
                w,c=world()
                if malformed=='native-consumed':
                    r=attach(c,'native',NativeOccurrenceLedger(),'cleric.hero.saint.aura-of-grace',
                        'regular-heal',identity='native',targets=('a',),deadline=None)
                    capture(w);w.regular_start('a',6);r.holder.consumed=[]
                    action=lambda:c.native_occurrence(w,'native','event',eligible=True,opted_in=True)
                else:
                    r=pulse(c,'transcendent-meditation' if malformed=='guard-consumed' else 'song-of-mending')
                    r.holder.resolve(0,ClockMarker(0),(),CanonicalPulseWallet(w,'a'),round_number=1)
                    capture(w);w.regular_start('a',6)
                    if malformed=='guard-consumed':c.outputs.consumed=[]
                    elif malformed=='recipient-history':c.recipients.history=[]
                    else:r.holder.declarations=[]
                    action=lambda:c.resolve_pulse(w,'pulse','event',1,('b',))
                before=whole_state(w,c)
                with self.assertRaisesRegex(SpellRuleError,'collection'):action()
                self.assertEqual(whole_state(w,c),before)

    def test_bloom_missed_original_installment_does_not_block_later_due_share(self):
        w,c=world();p=pulse(c,'eternal-bloom');h=BloomReserve({'b':10})
        p.holder.resolve(0,ClockMarker(0),(),CanonicalPulseWallet(w,'a'),round_number=1)
        h.consume(0,eligible_targets=())
        attach(c,'bloom',h,PULSE_SOURCES['eternal-bloom'],'installments',identity='reserve',deadline=ClockMarker(18),parent='pulse')
        capture(w);event(w,now=7);w.kernel_plan('b').commit()
        self.assertEqual(h.consumed,{0,1});self.assertEqual(w.lives['b'].hp,25)
        w.regular_start('a',12);c.resolve_pulse(w,'pulse','third-pulse',2,('b',))
        self.assertEqual(c.consume_bloom(w,'reserve','third-share',2,eligible_targets=('b',),pulse_event='third-pulse'),{'b':3})

    def test_preinitiative_recipient_claim_requires_import_adapter(self):
        w,c=world();c.recipients.commit('named:Circle of Harmony',('b',),1)
        before=whole_state(w,c)
        with self.assertRaisesRegex(SpellRuleError,'round import adapter'):capture(w)
        self.assertIsNone(w._snapshot);self.assertEqual(whole_state(w,c),before)

    def test_independent_output_is_shared_across_old_and_new_paths(self):
        for original_path in ('guard','world'):
            with self.subTest(original_path=original_path):
                w,c=world();r=pulse(c,'transcendent-meditation');guard=c.outputs
                guard.resolve('pulse',0,ClockMarker(0),('b',),event_id='initial',round_number=1,real_encounter=True)
                capture(w);w.regular_start('a',6)
                if original_path=='guard':
                    first=guard.resolve('pulse',1,ClockMarker(6),('b',),event_id='old-pulse',round_number=1,real_encounter=True)
                else:first=c.resolve_pulse(w,'pulse','old-pulse',1,('b',))
                self.assertEqual(first['independentKi'],1)
                event(w,now=6);w.kernel_plan('b').commit();w.regular_start('a',6)
                if original_path=='guard':second=c.resolve_pulse(w,'pulse','new-pulse',1,('b',))
                else:
                    second=guard.resolve('pulse',1,ClockMarker(6),('b',),event_id='new-pulse',round_number=1,real_encounter=True)
                self.assertEqual(second['independentKi'],0)
                self.assertEqual(guard.consumed,{('pulse',1,'Ki')})
                self.assertIs(c.outputs,guard)

    def test_guard_events_and_state_make_preflight_stale(self):
        for field in ('consumed','events','schema','binding'):
            with self.subTest(field=field):
                w,c=world();pulse(c,'transcendent-meditation');capture(w);event(w,now=2);plan=w.kernel_plan('a')
                if field=='consumed':c.outputs.consumed.add(('pulse',1,'Ki'))
                elif field=='events':c.outputs.events['outside-path']={'used':True}
                elif field=='schema':c.outputs.unknown=True
                else:c.outputs.series['pulse']=tuple(list(c.outputs.series['pulse']))
                before=whole_state(w,c)
                with self.assertRaises(SpellRuleError):plan.commit()
                self.assertEqual(whole_state(w,c),before)

    def test_existing_guard_registration_is_used_without_new_ledger(self):
        w,c=world();guard=c.outputs
        h=PulseSeries('pulse','transcendent-meditation',ClockMarker(0),
                      tuple(ClockMarker(t) for t in (6,12,18)),c.recipients,roster=('b',))
        guard.register(h,'a',PULSE_SOURCES['transcendent-meditation'])
        c.concentration.start_committed('a','pulse',lambda reason:c.active.discard('pulse'))
        attach(c,'pulse',h,PULSE_SOURCES['transcendent-meditation'],'transcendent-meditation',identity='pulse',
               concentration='pulse',deadline=h.expires)
        capture(w);self.assertIs(c.outputs,guard);self.assertIs(guard.series['pulse'][0],h)

    def test_oracle_finals_still_require_concentration(self):
        for profile in ('eternal-bloom','crown-restored'):
            with self.subTest(profile=profile):
                w,c=world();pulse(c,profile,concentration=False)
                with self.assertRaisesRegex(SpellRuleError,'Source concentration required'):capture(w)

    def test_live_resolution_uses_real_wallet_and_authenticated_start(self):
        w,c=world();r=pulse(c,'song-of-mending',concentration=True)
        r.holder.resolve(0,ClockMarker(0),(),CanonicalPulseWallet(w,'a'),round_number=1)
        capture(w)
        for actor,now in (('a',1),('b',2),('foe',3)):
            turn=w.regular_start(actor,now);w.scheduler.regular_end(turn,now)
        w.regular_start('a',6)
        result=c.resolve_pulse(w,'pulse','actual-song',1,('b',))
        self.assertEqual(result['outputTargets'],('b',));self.assertEqual(w.scheduler.rc['a'],4)
        self.assertIn('actual-song',c.events)

    def test_hemostasis_uses_target_start_not_owner_start(self):
        w,c=world();pulse(c,'hemostasis');capture(w)
        with self.assertRaises(SpellRuleError):c.resolve_pulse(w,'pulse','fake',0,('b',))
        ta=w.regular_start('a',6)
        with self.assertRaises(SpellRuleError):c.resolve_pulse(w,'pulse','wrong-owner',0,('b',))
        w.scheduler.regular_end(ta,6);w.regular_start('b',6)
        result=c.resolve_pulse(w,'pulse','target-start',0,('b',))
        self.assertEqual(result['outputTargets'],('b',))
        self.assertEqual(w.wallets['a'].rp,10)

    def test_hemostasis_duplicate_target_is_not_admitted(self):
        w,c=world();pulse(c,'hemostasis');pulse(c,'hemostasis',identity='duplicate')
        with self.assertRaisesRegex(SpellRuleError,'one active Hemostasis'):capture(w)

    def test_bloom_requires_fresh_current_iteration_parent_receipt(self):
        w,c=world();p=pulse(c,'eternal-bloom');h=BloomReserve({'b':10})
        attach(c,'bloom',h,PULSE_SOURCES['eternal-bloom'],'installments',identity='reserve',deadline=ClockMarker(18),parent='pulse')
        p.holder.resolve(0,ClockMarker(0),(),CanonicalPulseWallet(w,'a'),round_number=1)
        h.consume(0,eligible_targets=());capture(w)
        for actor,now in (('a',1),('b',2),('foe',3)):
            turn=w.regular_start(actor,now);w.scheduler.regular_end(turn,now)
        w.regular_start('a',6);c.resolve_pulse(w,'pulse','bloom-pulse',1,('b',))
        with self.assertRaisesRegex(SpellRuleError,'receipt'):
            c.consume_bloom(w,'reserve','forged',1,eligible_targets=('b',),pulse_event='absent')
        self.assertEqual(c.consume_bloom(w,'reserve','share',1,eligible_targets=('b',),pulse_event='bloom-pulse'),{'b':3})
        event(w,now=6);w.kernel_plan('b').commit();w.regular_start('a',6)
        with self.assertRaisesRegex(SpellRuleError,'actual parent pulse|receipt'):
            c.consume_bloom(w,'reserve','old-iteration',1,eligible_targets=('b',),pulse_event='bloom-pulse')

    def test_ended_parent_cannot_leave_contact_live(self):
        w,c=world();p=pulse(c,'garden',concentration=True);h=FirstContactLedger({'pulse':'garden'})
        attach(c,'contact',h,PULSE_SOURCES['garden'],'first-contact',identity='cure',deadline=ClockMarker(18),parent='pulse')
        capture(w);p.holder.end(ClockMarker(1),'test-ended');ta=w.regular_start('a',1)
        w.scheduler.regular_end(ta,1);w.regular_start('b',2)
        with self.assertRaisesRegex(SpellRuleError,'parent ended'):c.contact(w,'cure','bad-contact','b',event='start')
        self.assertEqual(h.consumed,set())

    def test_unobserved_missed_parent_upkeep_cannot_authorize_contact(self):
        w,c=world();p=pulse(c,'garden');h=FirstContactLedger({'pulse':'garden'})
        attach(c,'contact',h,PULSE_SOURCES['garden'],'first-contact',identity='cure',deadline=ClockMarker(18),parent='pulse')
        capture(w);ta=w.regular_start('a',7);w.scheduler.regular_end(ta,7);w.regular_start('b',7)
        self.assertIsNone(p.holder.ended_at)
        before=whole_state(w,c)
        with self.assertRaisesRegex(SpellRuleError,'missed upkeep'):
            c.contact(w,'cure','stale-parent','b',event='start')
        self.assertEqual(whole_state(w,c),before)

    def test_contact_pulse_needs_fresh_unsuppressed_parent_receipt(self):
        w,c=world();pulse(c,'resonant-seed',concentration=True);h=FirstContactLedger({'pulse':'resonant-seed'})
        attach(c,'contact',h,PULSE_SOURCES['resonant-seed'],'first-contact',identity='cure',deadline=ClockMarker(18),parent='pulse')
        capture(w);ta=w.regular_start('a',1);w.scheduler.regular_end(ta,1);w.regular_start('b',2)
        with self.assertRaises(SpellRuleError):c.contact(w,'cure','no-pulse','b',event='pulse')
        c.target_start(w,'pulse','seed-start','b',whole_effect_suppressed=True)
        with self.assertRaises(SpellRuleError):c.contact(w,'cure','suppressed','b',event='pulse',pulse_event='seed-start')
        self.assertEqual(h.consumed,set())

    def test_unrelated_outsider_recipient_budget_is_conserved(self):
        w=scene(capture=False,outsider=True);c=TemporalControlWorld(w.scheduler,outputs=ConservedPulseOutputs(w));w.integrations['control-pulses']=c
        capture(w);c.recipients.commit('named:Circle of Harmony',('outside',),1)
        event(w,now=2);w.kernel_plan('a').commit()
        self.assertIn(('named:Circle of Harmony','outside',1),c.recipients.claimed)

    def test_bloom_cannot_change_both_capture_and_recomputed_shares(self):
        w,c=world();pulse(c,'eternal-bloom');h=BloomReserve({'b':10})
        attach(c,'bloom',h,PULSE_SOURCES['eternal-bloom'],'installments',identity='reserve',deadline=ClockMarker(18),parent='pulse')
        capture(w);h.roster_missing={'b':99};h.shares={'b':(33,33,33)};event(w,now=2)
        with self.assertRaisesRegex(SpellRuleError,'parameters changed'):w.kernel_plan('a')

    def test_real_pulse_series_restores_in_place_without_cast_or_heal(self):
        w,c=world();r=pulse(c,'transcendent-meditation',concentration=True);h=r.holder
        h.resolve(0,ClockMarker(0),('b',),CanonicalPulseWallet(w,'a'),round_number=1)
        capture(w);h.end(ClockMarker(1),'temporary-test-state');event(w,now=2)
        old_life=w.lives['b'].hp;w.kernel_plan('a').commit()
        self.assertIs(r.holder,h);self.assertIs(h.ledger,c.recipients)
        self.assertEqual(h.states,['committed','pending','pending']);self.assertIsNone(h.ended_at)
        self.assertEqual(w.lives['b'].hp,old_life);self.assertEqual(h.future_starts,(ClockMarker(6),ClockMarker(12),ClockMarker(18)))

    def test_missed_original_due_pulse_is_lost_not_rebased(self):
        w,c=world();r=pulse(c,'hemostasis');capture(w);event(w,now=7)
        w.kernel_plan('a').commit()
        self.assertEqual(r.holder.states,['lost','pending','pending'])
        self.assertEqual(r.holder.opens[0],ClockMarker(6))

    def test_all_expired_outside_pulses_retire(self):
        w,c=world();r=pulse(c,'hemostasis');capture(w);event(w,now=20);w.kernel_plan('a').commit()
        self.assertNotIn('pulse',c.active);self.assertEqual(r.holder.states,['lost']*3)

    def test_missing_actual_concentration_blocks_without_mutation(self):
        w,c=world();r=pulse(c,'transcendent-meditation',concentration=True);capture(w)
        c.concentration.end('a','lost');event(w,now=2);before=whole_state(w,c)
        with self.assertRaisesRegex(SpellRuleError,'concentration'):w.kernel_plan('a')
        self.assertEqual(whole_state(w,c),before)

    def test_replaced_concentration_after_preflight_makes_plan_stale(self):
        w,c=world();pulse(c,'transcendent-meditation',concentration=True);capture(w);event(w,now=2)
        plan=w.kernel_plan('a');c.concentration.current['a']=('pulse',lambda reason:None)
        before=whole_state(w,c)
        with self.assertRaises(SpellRuleError):plan.commit()
        self.assertEqual(whole_state(w,c),before)

    def test_same_id_concentration_rebound_before_preflight_rejects(self):
        for replacement in ('different-callback','same-callback-new-slot','new-registered-component'):
            with self.subTest(replacement=replacement):
                w,c=world();pulse(c,'transcendent-meditation');capture(w)
                original=c.concentration.current['a']
                callback=original[1] if replacement=='same-callback-new-slot' else lambda reason:None
                c.concentration.current['a']=tuple(['pulse',callback])
                if replacement=='new-registered-component':
                    attach(c,'rider',OneShotRider('hit'),'dragoon.hero.drake-rider.drake-mark','dragoon.drake-mark',
                           identity='other',origin='encounter',concentration='pulse')
                event(w,now=2);before=whole_state(w,c)
                with self.assertRaisesRegex(SpellRuleError,'binding identity'):w.kernel_plan('a')
                self.assertEqual(whole_state(w,c),before)
                self.assertIs(c.concentration_pins[id(original)],original)

    def test_snapshot_fixed_roster_cannot_change(self):
        w,c=world();r=pulse(c,'eternal-bloom');capture(w);r.holder.roster=('a',);event(w,now=2)
        with self.assertRaisesRegex(SpellRuleError,'roster'):w.kernel_plan('a')

    def test_shared_recipient_current_view_rewinds_history_does_not(self):
        w,c=world();capture(w);c.recipients.commit('named:Circle of Harmony',('b',),1)
        old=set(c.recipients.history);event(w,now=2);w.kernel_plan('a').commit()
        self.assertEqual(c.recipients.claimed,set());self.assertEqual(c.recipients.history,old)
        c.recipients.commit('named:Circle of Harmony',('b',),1)
        self.assertEqual(len(c.recipients.history),2)
        with self.assertRaises(SpellRuleError):c.recipients.commit('named:Circle of Harmony',('b',),1)

    def test_bloom_original_shares_and_snapshot_consumption_restore(self):
        w,c=world();p=pulse(c,'eternal-bloom');h=BloomReserve({'b':10});h.consume(0,eligible_targets=('b',))
        attach(c,'bloom',h,PULSE_SOURCES['eternal-bloom'],'installments',identity='reserve',
               deadline=ClockMarker(18),parent='pulse')
        capture(w);h.consume(1,eligible_targets=('b',));event(w,now=2);w.kernel_plan('a').commit()
        self.assertEqual(h.consumed,{0});self.assertEqual(h.shares,{'b':(4,3,3)})

    def test_bloom_changed_original_missing_hp_rejected(self):
        w,c=world();pulse(c,'eternal-bloom');h=BloomReserve({'b':10})
        attach(c,'bloom',h,PULSE_SOURCES['eternal-bloom'],'installments',identity='reserve',deadline=ClockMarker(18),parent='pulse')
        capture(w);h.roster_missing['b']=100;event(w,now=2)
        with self.assertRaisesRegex(SpellRuleError,'shares'):w.kernel_plan('a')

    def test_contact_consumption_restores_without_contact_event(self):
        w,c=world();pulse(c,'garden',concentration=True);h=FirstContactLedger({'pulse':'garden'})
        attach(c,'contact',h,PULSE_SOURCES['garden'],'first-contact',identity='cure',deadline=ClockMarker(18),parent='pulse')
        capture(w);h.claim('pulse','b',event='start');event(w,now=2);w.kernel_plan('a').commit()
        self.assertEqual(h.consumed,set());self.assertEqual(c.events,{})

    def test_parent_device_without_actual_adapter_rejected(self):
        w,c=world();pulse(c,'nano-aegis')
        with self.assertRaisesRegex(SpellRuleError,'parent adapter'):capture(w)

    def test_ended_concentration_callback_still_targets_same_restored_source(self):
        w,c=world();pulse(c,'transcendent-meditation',concentration=True);capture(w)
        event(w,now=2);w.kernel_plan('a').commit();c.concentration.end('a','later end')
        self.assertNotIn('pulse',c.active)


class NativeAndReflectionTests(unittest.TestCase):
    def native(self,c):
        return attach(c,'native',NativeOccurrenceLedger(),'cleric.hero.saint.aura-of-grace','regular-heal',
                      identity='native',targets=('a',),deadline=None)

    def test_native_declined_ineligible_or_unaffordable_cannot_retry_start(self):
        for eligible,opted,rp in ((True,False,10),(False,True,10),(True,True,0)):
            with self.subTest(case=(eligible,opted,rp)):
                w,c=world();self.native(c);capture(w);w.wallets['a'].rp=rp;w.regular_start('a',1)
                self.assertFalse(c.native_occurrence(w,'native','first',eligible=eligible,opted_in=opted))
                w.wallets['a'].rp=10
                with self.assertRaisesRegex(SpellRuleError,'already evaluated'):
                    c.native_occurrence(w,'native','retry',eligible=True,opted_in=True)

    def test_native_new_iteration_can_pay_again_but_old_rp_stays_spent(self):
        w,c=world();r=self.native(c);capture(w);w.regular_start('a',1)
        self.assertTrue(c.native_occurrence(w,'native','heal-1',eligible=True,opted_in=True))
        event(w,now=2);w.kernel_plan('b').commit()
        self.assertEqual(w.wallets['a'].rp,9);self.assertEqual(len(r.holder.consumed),1)
        w.regular_start('a',3);self.assertTrue(c.native_occurrence(w,'native','heal-2',eligible=True,opted_in=True))
        self.assertEqual(w.wallets['a'].rp,8);self.assertEqual(len(r.holder.consumed),2)

    def test_native_has_no_restore_tick_and_no_late_turn_retry(self):
        w,c=world();self.native(c);capture(w);event(w,now=2);w.kernel_plan('a').commit()
        self.assertEqual(c.native_evaluations,{})
        with self.assertRaisesRegex(SpellRuleError,'regular turn'):c.native_occurrence(w,'native','fake',eligible=True,opted_in=True)
        w.regular_start('a',3);w.scheduler.begin_event('action');w.scheduler.finish_event('action')
        with self.assertRaisesRegex(SpellRuleError,'window is closed'):c.native_occurrence(w,'native','late',eligible=True,opted_in=True)

    def test_rapid_coagulation_requires_real_movement_adapter(self):
        w,c=world();r=self.native(c);r.source='warrior.supplement.rapid-coagulation'
        with self.assertRaisesRegex(SpellRuleError,'movement adapter'):capture(w)

    def test_reflection_uses_real_target_turn_and_preserves_history(self):
        w,c=world();h=PerTurnReflection(10)
        c.concentration.start_committed('a','judgment',lambda reason:None)
        attach(c,'reflection',h,'cleric.hero.priest.divine-judgment','cleric.divine-judgment.mark',concentration='judgment')
        capture(w);ta=w.regular_start('a',1)
        with self.assertRaises(SpellRuleError):c.reflect(w,'effect','off-turn',positive_damage_event=True,actual_damage_dealt=8)
        w.scheduler.regular_end(ta,1);w.regular_start('b',2)
        self.assertEqual(c.reflect(w,'effect','damage-1',positive_damage_event=True,actual_damage_dealt=8),4)
        self.assertEqual(c.reflect(w,'effect','damage-2',positive_damage_event=True,actual_damage_dealt=8),0)
        event(w,now=3);w.kernel_plan('a').commit();self.assertEqual(len(h.used_turn_ids),1)
        ta=w.regular_start('a',4);w.scheduler.regular_end(ta,4);w.regular_start('b',5)
        self.assertEqual(c.reflect(w,'effect','damage-3',positive_damage_event=True,actual_damage_dealt=8),4)
        self.assertEqual(len(h.used_turn_ids),2)


if __name__=='__main__':
    suite=unittest.TestSuite(unittest.defaultTestLoader.loadTestsFromTestCase(c) for c in
                            (ControlTransactionTests,PulseTransactionTests,NativeAndReflectionTests))
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    root=Path(__file__).resolve().parents[1]
    report={'status':'PASS' if result.wasSuccessful() else 'FAIL','methods':result.testsRun,
        'failures':len(result.failures),'errors':len(result.errors),'fullTimeLoopOperational':False,
        'scope':'Live control/pulse transaction candidate; exact admitted source policies; parent/entry/mutation adapters remain',
        'hashes':{p:hashlib.sha256((root/p).read_bytes()).hexdigest() for p in
                  ('tools/temporal_playtest_rules.py','tools/temporal_control_world.py')}}
    (root/'docs/mechanics/TEMPORAL_CONTROL_WORLD_VALIDATION.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    raise SystemExit(0 if result.wasSuccessful() else 1)
