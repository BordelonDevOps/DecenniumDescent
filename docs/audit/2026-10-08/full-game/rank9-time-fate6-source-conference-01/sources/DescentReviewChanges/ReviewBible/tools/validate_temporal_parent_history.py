"""Actual-operation journal checks; not Time Loop parent restoration tests."""
from copy import deepcopy
from pathlib import Path
import hashlib
import json
import unittest

from temporal_parent_history import TemporalParentHistory, CasterAuthority, leaf
from validate_transformation_spell_playtests import world,stats,price,select
from form_temphp_playtest_rules import DruidState,DruidStats
from transformation_spell_playtest_rules import Body,PhysicalOrigin,CastPrice,CastStats
from temporal_playtest_rules import Scheduler,Wallet,ClockMarker,SpellRuleError


def observed(w, *, scheduler=None, druid_stats=None, caster_level=20, known=None):
    druid_stats={} if druid_stats is None else druid_stats
    authorities={}
    for owner in w.bodies:
        cadence=w.druids[owner].cadence if owner in w.druids else {'refrain':0,'rememberedSpell':None,'dissonance':0}
        actual_stats=CastStats(owner,'Druid',10,18,6,4) if owner in druid_stats else stats(owner)
        level=druid_stats[owner].level if owner in druid_stats else caster_level
        authorities[owner]=CasterAuthority(actual_stats,level,100,4,
            frozenset(('polymorph','shapechange','true-polymorph','mass-polymorph') if known is None else known),cadence)
    return TemporalParentHistory(w,wallets={a:Wallet(rp=100) for a in w.bodies},
        druid_stats=druid_stats,casters=authorities,scheduler=scheduler)


def fixture(level=14):
    w=world();ds=DruidStats('a',level,6,4,4,4)
    d=DruidState(ds,'Moon',w.buffers,{'refrain':2,'rememberedSpell':'x','dissonance':8})
    w.druids['a']=d
    return w,ds,d,observed(w,druid_stats={'a':ds})


def shift(j,ds,*,fid='F',source='druid.base.bear-form-tank',now=0,event='shift'):
    wallet=j.wallets[ds.owner];wallet.bonus_action=True
    return j.shift(event,ds,source,fid,now,wallet,legal=True)


def cast(j,*,spell='polymorph',cid='C',event='cast',now=0,target='b',owner='a',save=False,countered=False):
    return j.cast(event,cid,spell,j.casters[owner].stats,j.quote_price(owner,spell),j.wallets[owner],[select(target)],now,0,
                  legal=True,resolve_save=lambda t,dc:save,countered=countered)


class ParentHistoryTests(unittest.TestCase):
    def test_paid_renewal_keeps_same_form_and_actual_payment(self):
        w,ds,d,j=fixture();shift(j,ds);f=d.current;before=d.shifts
        j.renew('renew',ds,600)
        self.assertIs(d.current,f);self.assertEqual(d.shifts,before-1)
        r=j.records('form-renewed','F')[0]
        self.assertEqual((r['oldExpiry']['seconds'],r['newExpiry']['seconds']),(600,1200))
        self.assertEqual((r['shiftBefore'],r['shiftAfter']),(before,before-1))
        self.assertEqual(j.valid_form_deadline('a','F',601),ClockMarker(1200))

    def test_level20_zero_shift_renewal_still_requires_real_endpoint_event(self):
        w,ds,d,j=fixture(20);shift(j,ds);before=d.shifts
        with self.assertRaises(SpellRuleError):j.renew('early',ds,599)
        self.assertFalse(j.records('form-renewed','F'))
        j.renew('on-time',ds,600)
        self.assertEqual(d.shifts,before);self.assertEqual(len(j.records('form-renewed','F')),1)

    def test_renewal_chain_survives_later_real_reversion_without_reactivation(self):
        w,ds,d,j=fixture();shift(j,ds);j.renew('r1',ds,600);j.renew('r2',ds,1200)
        j.wallets['a'].bonus_action=True;j.revert('revert','a',1201,j.wallets['a'],legal=True)
        before=deepcopy((d.reserve,d.surges,d.shifts,d.instances['F'].state))
        self.assertEqual(j.valid_form_deadline('a','F',1202),ClockMarker(1800))
        self.assertIsNone(d.current);self.assertEqual((d.reserve,d.surges,d.shifts,d.instances['F'].state),before)
        with self.assertRaises(SpellRuleError):j.valid_form_deadline('a','F',1800)

    def test_new_instance_does_not_borrow_old_renewal(self):
        w,ds,d,j=fixture();shift(j,ds);j.renew('renew',ds,600)
        shift(j,ds,fid='G',source='druid.base.wolf-form-striker',now=601,event='wolf')
        self.assertFalse(j.records('form-renewed','G'))
        self.assertEqual(j.valid_form_deadline('a','G',602),ClockMarker(1201))
        self.assertEqual(d.instances['F'].state,'changed')

    def test_unobserved_native_renewal_is_not_accepted_as_evidence(self):
        w,ds,d,j=fixture();shift(j,ds);d.natural_endpoint(ds,600,renew=True)
        with self.assertRaisesRegex(SpellRuleError,'Unobserved'):j.valid_form_deadline('a','F',601)

    def test_direct_expiry_edit_cannot_fabricate_paid_extension(self):
        w,ds,d,j=fixture();shift(j,ds);d.current.expiry=ClockMarker(900)
        with self.assertRaisesRegex(SpellRuleError,'Unobserved'):j.validate()

    def test_public_receipt_edit_is_detected(self):
        w,ds,d,j=fixture();shift(j,ds);j.renew('renew',ds,600)
        j.receipts[-1]['newExpiry']['seconds']=1800
        with self.assertRaisesRegex(SpellRuleError,'historical'):j.validate()

    def test_returned_receipt_copy_cannot_mutate_journal(self):
        w,ds,d,j=fixture();shift(j,ds);r=j.records('form-created','F')[0]
        r['initial']['expiry']['seconds']=9999
        self.assertEqual(j.valid_form_deadline('a','F',1),ClockMarker(600))

    def test_event_deletion_and_duplicate_id_reject(self):
        w,ds,d,j=fixture();shift(j,ds)
        with self.assertRaisesRegex(SpellRuleError,'Repeated'):j.renew('shift',ds,600)
        j.events=()
        with self.assertRaisesRegex(SpellRuleError,'historical'):j.validate()

    def test_form_identity_replacement_rejects_even_equal_fields(self):
        w,ds,d,j=fixture();shift(j,ds);f=deepcopy(d.current)
        d.instances['F']=f;d.current=f
        with self.assertRaisesRegex(SpellRuleError,'object was replaced'):j.validate()

    def test_shared_world_and_cadence_aliases_must_remain_canonical(self):
        w,ds,d,j=fixture();d.cadence=dict(d.cadence)
        with self.assertRaisesRegex(SpellRuleError,'same cadence|alias'):j.validate()

    def test_actual_casting_cadence_changes_remain_current(self):
        w,ds,d,j=fixture();shift(j,ds)
        d.cadence.update(refrain=3,rememberedSpell='later-spell',dissonance=19)
        j.validate();j.valid_form_deadline('a','F',1)
        self.assertEqual(d.cadence,{'refrain':3,'rememberedSpell':'later-spell','dissonance':19})

    def test_observation_cannot_start_from_existing_cast_or_form(self):
        w,ds,d,j=fixture();shift(j,ds)
        with self.assertRaisesRegex(SpellRuleError,'before first form'):observed(w)
        w=world();j=observed(w);cast(j)
        with self.assertRaisesRegex(SpellRuleError,'before source creation'):observed(w)

    def test_original_concentration_callback_retained_after_real_end(self):
        w=world();j=observed(w);cast(j);slot=w.concentration.current['a']
        j.end_concentration('failure','a',1,reason='failed-save')
        self.assertEqual(w.links['C:b'].state,'failed-save')
        self.assertIs(j._slot_pins[id(slot)],slot)
        self.assertEqual(j.records('cast-created','C')[0]['concentrationBinding'][1:],(id(slot),id(slot[1])))
        self.assertNotIn('a',w.concentration.current)

    def test_same_id_replaced_callback_detected(self):
        w=world();j=observed(w);cast(j)
        w.concentration.current['a']=('C',lambda reason:None)
        with self.assertRaisesRegex(SpellRuleError,'Unobserved'):j.validate()

    def test_true_stabilization_proof_survives_dispel(self):
        w=world();j=observed(w);cast(j,spell='true-polymorph')
        self.assertFalse(j.permanent_link('C:b'))
        j.checkpoint('checkpoint',60,started_packets_and_due_saves_finished=True)
        self.assertTrue(j.permanent_link('C:b'));self.assertNotIn('a',w.concentration.current)
        j.dispel('dispel','c','b',61,legal=True)
        before=deepcopy((w.links['C:b'].state,w.bodies['b'].anatomy,w.bodies['b'].equipment))
        self.assertTrue(j.permanent_link('C:b'))
        self.assertEqual((w.links['C:b'].state,w.bodies['b'].anatomy,w.bodies['b'].equipment),before)

    def test_fabricated_permanent_flag_is_not_stabilization(self):
        w=world();j=observed(w);cast(j,spell='true-polymorph')
        w.links['C:b'].state='permanent'
        with self.assertRaisesRegex(SpellRuleError,'Unobserved'):j.permanent_link('C:b')

    def test_checkpoint_cannot_resolve_same_link_twice(self):
        w=world();j=observed(w);cast(j,spell='true-polymorph')
        j.checkpoint('checkpoint',60,started_packets_and_due_saves_finished=True)
        j.checkpoint('later',61,started_packets_and_due_saves_finished=True)
        self.assertEqual(len(j.records('link-stabilized','C:b')),1)

    def test_expiring_polymorph_is_not_permanent(self):
        w=world();j=observed(w);cast(j)
        j.checkpoint('checkpoint',60,started_packets_and_due_saves_finished=True)
        self.assertEqual(w.links['C:b'].state,'expired')
        self.assertEqual(j.records('link-ended','C:b')[0]['newState'],'expired')
        with self.assertRaises(SpellRuleError):j.permanent_link('C:b')

    def test_countered_cast_records_real_cost_but_no_link(self):
        w=world();j=observed(w);result=cast(j,countered=True)
        self.assertTrue(result['countered']);self.assertEqual(w.links,{})
        self.assertIsNone(j.records('cast-created','C')[0]['concentrationBinding'])
        e=j.events[0]
        self.assertLess(e['economyAfter']['wallets'][0]['rp'],e['economyBefore']['wallets'][0]['rp'])

    def test_failing_save_callback_taints_partial_committed_cast(self):
        w=world();j=observed(w);wallet=j.wallets['a']
        def broken(target,dc):raise RuntimeError('authoritative resolver failed')
        with self.assertRaises(RuntimeError):j.cast('broken','C','polymorph',j.casters['a'].stats,j.quote_price('a','polymorph'),
            wallet,[select(willing=False)],0,0,legal=True,resolve_save=broken)
        self.assertLess(wallet.rp,100);self.assertTrue(j.events[0]['failed']);self.assertEqual(j.receipts,())
        with self.assertRaisesRegex(SpellRuleError,'host reconciliation'):j.validate()

    def test_failed_unpaid_operation_produces_no_success_receipt(self):
        w,ds,d,j=fixture();before=d.shifts
        with self.assertRaises(SpellRuleError):j.shift('illegal',ds,'druid.base.bear-form-tank','F',0,j.wallets['a'],legal=False)
        self.assertEqual(d.shifts,before);self.assertEqual(j.receipts,());j.validate()

    def test_failure_after_clock_only_mutation_also_taints(self):
        w,ds,d,j=fixture(20)
        source=next(k for k in __import__('form_temphp_playtest_rules').PROFILES if k.endswith('mooncursed'))
        shift(j,ds,source=source)
        j.wallets['a'].actions=0
        with self.assertRaises(SpellRuleError):j.special('bad-payment',ds,1,j.wallets['a'],'howl',legal=True)
        self.assertEqual(d.recharge_clock.now,ClockMarker(1))
        with self.assertRaisesRegex(SpellRuleError,'host reconciliation'):j.validate()

    def test_unknown_holder_fields_reject_before_source_cost(self):
        w,ds,d,j=fixture();d.unknown_state=True;wallet=Wallet();before=deepcopy(vars(wallet))
        with self.assertRaisesRegex(SpellRuleError,'schema'):shift(j,ds)
        self.assertEqual(vars(wallet),before);self.assertFalse(d.instances)

    def test_same_hp_holder_required_but_actual_damage_may_change_hp(self):
        w=world();j=observed(w);cast(j);life=w.bodies['b'].life
        life.hp=0;j.finalize_damage('damage','b',1,incapacitated=False,dead=False)
        self.assertEqual(w.links['C:b'].state,'forced-reversion');self.assertIs(w.bodies['b'].life,life)
        w.bodies['b'].life=deepcopy(life)
        with self.assertRaisesRegex(SpellRuleError,'Unobserved'):j.validate()

    def test_cast_ends_actual_druid_and_records_both_sources(self):
        w,ds,d,j=fixture();shift(j,ds)
        cast(j,target='a',owner='b',now=1)
        self.assertIsNone(d.current)
        self.assertEqual(j.records('form-ended','F')[0]['newState'],'spell-transformation')
        self.assertEqual(w.bodies['a'].anatomy,'C:a')

    def test_outside_origin_and_authenticated_initiative_are_distinct(self):
        w=world();s=Scheduler('enc',('a','b','c'),now=ClockMarker(10));j=observed(w,scheduler=s)
        cast(j,now=9);self.assertEqual(j.records('cast-created','C')[0]['origin']['kind'],'OUTSIDE_CAST')
        j.enter_initiative()
        with self.assertRaisesRegex(SpellRuleError,'atomic'):j.end_concentration('fake','a',10,reason='failed-save')
        s.begin_event('real');j.end_concentration('real','a',10,reason='failed-save');s.finish_event('real')
        self.assertEqual(j.events[-1]['origin']['encounter'],'enc')

    def test_recharge_query_never_ticks_but_authentic_due_start_does(self):
        w,ds,d,j=fixture(20);shift(j,ds,source='druid.hero.moon.mooncursed')
        j.special('clock-use',ds,0,j.wallets['a'],'howl',legal=True)
        s=Scheduler('enc',('a','b','c'),now=ClockMarker(6));j.scheduler=s;j.enter_initiative()
        self.assertEqual(d.recharge_clock.ticks,0);j.valid_form_deadline('a','F',6)
        self.assertEqual(d.recharge_clock.ticks,0)
        s._regular_start('a',Wallet(),6);s.begin_event('start',phase='start')
        j.druid_regular_start('start','a');self.assertEqual(d.recharge_clock.ticks,1)
        self.assertEqual(d.regular_index,s.global_regular)

    def test_fake_recharge_marker_or_body_phase_rejects(self):
        w,ds,d,j=fixture();s=Scheduler('enc',('a','b','c'));j.scheduler=s;j.enter_initiative()
        with self.assertRaisesRegex(SpellRuleError,'Authenticated'):j.druid_regular_start('fake','a')
        s._regular_start('a',Wallet(),0);s.begin_event('body')
        with self.assertRaisesRegex(SpellRuleError,'Authenticated'):j.druid_regular_start('body','a')
        self.assertEqual(d.regular_index,0)

    def test_actual_gear_loss_is_preserved_and_not_restored_by_history_queries(self):
        w=world();j=observed(w);cast(j)
        j.lose_gear('lost','b','b:coat',1,actual_loss=True)
        j.end_concentration('end','a',2,reason='voluntary-release')
        self.assertNotIn('b:coat',w.bodies['b'].equipment)
        self.assertIn('b:coat',w.bodies['b'].lost_items);j.validate()

    def test_duplicate_wallet_cannot_manufacture_cast_payment_history(self):
        w=world();j=observed(w)
        fake=Wallet(rp=100);before=deepcopy(vars(fake))
        with self.assertRaisesRegex(SpellRuleError,'canonical owner wallet'):
            j.cast('fake','C','polymorph',j.casters['a'].stats,j.quote_price('a','polymorph'),fake,[select()],0,0,
                   legal=True,resolve_save=lambda t,dc:False)
        self.assertEqual(vars(fake),before);self.assertEqual(j.events,());self.assertEqual(w.casts,{})

    def test_wallet_registry_replacement_detected_before_payment(self):
        w,ds,d,j=fixture();j.wallets['a']=Wallet(rp=100)
        with self.assertRaisesRegex(SpellRuleError,'wallet registry'):shift(j,ds)
        self.assertFalse(d.instances)

    def test_shared_wallet_between_two_owners_rejects_at_binding(self):
        w=world();wallet=Wallet()
        with self.assertRaisesRegex(SpellRuleError,'alias wallets'):TemporalParentHistory(w,wallets={'a':wallet,'b':wallet},druid_stats={},casters={})

    def test_scheduler_replacement_and_history_mode_edits_reject(self):
        w,ds,d,j=fixture();s=Scheduler('enc',('a','b','c'));j.scheduler=s;j.enter_initiative()
        j.scheduler=deepcopy(s)
        with self.assertRaisesRegex(SpellRuleError,'scheduler changed'):j.validate()
        j.scheduler=s;j.mode='outside'
        with self.assertRaisesRegex(SpellRuleError,'clock/mode'):j.validate()

    def test_clock_tampering_cannot_backdate_a_receipt(self):
        w,ds,d,j=fixture();shift(j,ds,now=10);j.last_time=ClockMarker(0)
        with self.assertRaisesRegex(SpellRuleError,'clock/mode'):j.validate()

    def test_native_successful_repeat_save_records_actual_ending(self):
        w=world();j=observed(w)
        j.cast('cast','C','polymorph',j.casters['a'].stats,j.quote_price('a','polymorph'),j.wallets['a'],[select(willing=False)],0,0,
               legal=True,resolve_save=lambda t,dc:False)
        j.repeat_save('repeat','b',j.casters['a'].stats,1,trigger='damage',event_or_turn='hit',round_number=1,normal_hp_damage=2,success=True)
        self.assertEqual(j.records('link-ended','C:b')[0]['newState'],'repeat-save')
        self.assertIn(('b','hit'),w.damage_events);j.validate()

    def test_unobserved_repeat_history_edit_rejects(self):
        w=world();j=observed(w);cast(j)
        w.damage_rounds.add(('b',99))
        with self.assertRaisesRegex(SpellRuleError,'Unobserved'):j.validate()

    def test_mooncursed_grant_keeps_actual_recipient_rest_lifetime(self):
        w,ds,d,j=fixture(20);shift(j,ds,source='druid.hero.moon.mooncursed')
        before=d.surges
        j.mooncursed_howl('howl',ds,1,j.wallets['a'],['b'],8,['howl:b'],legal=True)
        grant=w.buffers.current('b');self.assertEqual(grant.dependencies,())
        self.assertEqual(grant.rest_epoch,0);self.assertEqual(d.surges,before-1)
        j.wallets['a'].bonus_action=True;j.revert('revert','a',2,j.wallets['a'],legal=True)
        self.assertIs(w.buffers.current('b'),grant);j.validate()

    def test_forged_level20_cannot_avoid_paid_renewal(self):
        w,ds,d,j=fixture(14);shift(j,ds);before=d.shifts;old=d.current.expiry
        with self.assertRaisesRegex(SpellRuleError,'bound current Druid'):
            j.renew('forged',DruidStats('a',20,6,4,4,4),600)
        self.assertEqual((d.shifts,d.current.expiry),(before,old))
        self.assertFalse(j.records('form-renewed','F'))

    def test_equal_looking_unbound_stats_cannot_supply_source_authority(self):
        w=world();j=observed(w)
        with self.assertRaisesRegex(SpellRuleError,'bound current casting'):
            j.cast('fake','C','polymorph',stats(),j.quote_price('a','polymorph'),j.wallets['a'],[select()],0,0,
                   legal=True,resolve_save=lambda t,dc:False)
        self.assertEqual(w.casts,{})

    def test_fabricated_zero_price_rejects_before_cast(self):
        w=world();j=observed(w);fake=CastPrice('polymorph',4,0,0,{})
        with self.assertRaisesRegex(SpellRuleError,'canonical ordinary quote'):
            j.cast('fake','C','polymorph',j.casters['a'].stats,fake,j.wallets['a'],[select()],0,0,
                   legal=True,resolve_save=lambda t,dc:False)
        self.assertEqual(j.wallets['a'].rp,100);self.assertFalse(w.casts);self.assertFalse(j.events)

    def test_stale_quote_cannot_omit_current_dissonance_surcharge(self):
        w=world();j=observed(w);old=j.quote_price('a','polymorph')
        j.casters['a'].cadence['dissonance']=12
        self.assertEqual(j.quote_price('a','polymorph').total,old.total+1)
        with self.assertRaisesRegex(SpellRuleError,'stale quote'):
            j.cast('stale','C','polymorph',j.casters['a'].stats,old,j.wallets['a'],[select()],0,0,
                   legal=True,resolve_save=lambda t,dc:False)
        self.assertEqual(j.wallets['a'].rp,100);self.assertFalse(w.casts)

    def test_actual_repertoire_and_class_level_gate_are_enforced(self):
        for level,known in ((1,('polymorph',)),(20,())):
            with self.subTest(level=level,known=known):
                w=world();j=observed(w,caster_level=level,known=known)
                with self.assertRaises(SpellRuleError):j.quote_price('a','polymorph')
                self.assertEqual(j.wallets['a'].rp,100);self.assertFalse(j.events)

    def test_authority_replacement_is_structural_divergence(self):
        w,ds,d,j=fixture();j.druid_stats['a']=DruidStats('a',20,6,4,4,4)
        with self.assertRaisesRegex(SpellRuleError,'Druid stats changed'):j.validate()

    def test_successful_receipt_contains_actual_stats_and_cadence_evidence(self):
        w,ds,d,j=fixture();shift(j,ds);j.renew('renew',ds,600)
        e=j.events[-1]['economyBefore']['sourceAuthorities']
        self.assertEqual(e['druidStats']['a']['level'],14)
        self.assertEqual(e['casters']['a']['cadence']['dissonance'],8)

    def test_unobserved_druid_finite_fields_each_reject(self):
        edits={'long_epoch':1,'short_epoch':1,'regular_index':1,'recharges':{'fake':2},
               'rest_uses':{'fake':1},'attuned':('fake',),'shifts':99,'buffer_capacity':99,
               'reserve':99,'surges':99,'surge_capacity':99}
        for name,value in edits.items():
            with self.subTest(field=name):
                w,ds,d,j=fixture();shift(j,ds);setattr(d,name,value)
                with self.assertRaisesRegex(SpellRuleError,'Unobserved Druid finite'):
                    j.valid_form_deadline('a','F',1)

    def test_unobserved_recharge_ticks_cannot_be_admitted(self):
        w,ds,d,j=fixture();shift(j,ds);d.recharge_clock.ticks+=10
        with self.assertRaisesRegex(SpellRuleError,'Unobserved Druid finite'):j.validate()

    def test_observed_rest_and_clock_changes_update_finite_expectation(self):
        w,ds,d,j=fixture();shift(j,ds);before=d.shifts
        j.druid_clock_transition('leave','a',1,transition='leave')
        j.druid_rest('rest',ds,1,601,kind='long',actual_completed=True)
        j.validate();self.assertGreater(d.shifts,before);self.assertEqual(d.long_epoch,1)
        self.assertEqual(d.current.instance_id,'F')
        self.assertFalse(j.records('form-renewed','F'))

    def test_save_callback_cannot_launder_native_druid_entry(self):
        w,ds,d,j=fixture()
        def nested(target,dc):
            d.shift(ds,'druid.base.bear-form-tank','unobserved',0,j.wallets['a'],legal=True)
            return False
        with self.assertRaisesRegex(SpellRuleError,'Save resolver changed'):
            j.cast('cast','C','polymorph',j.casters['b'].stats,j.quote_price('b','polymorph'),
                j.wallets['b'],[select('c',willing=False)],0,0,legal=True,resolve_save=nested)
        self.assertIn('unobserved',d.instances);self.assertEqual(j.receipts,())
        self.assertTrue(j.events[-1]['failed'])
        with self.assertRaisesRegex(SpellRuleError,'host reconciliation'):j.validate()

    def test_save_callback_cannot_spend_or_refill_unrelated_druid_economy(self):
        w,ds,d,j=fixture()
        def nested(target,dc):d.shifts+=3;return False
        with self.assertRaisesRegex(SpellRuleError,'Save resolver changed'):
            j.cast('cast','C','polymorph',j.casters['b'].stats,j.quote_price('b','polymorph'),
                j.wallets['b'],[select('c',willing=False)],0,0,legal=True,resolve_save=nested)
        self.assertEqual(j.receipts,())
        with self.assertRaisesRegex(SpellRuleError,'host reconciliation'):j.validate()

    def test_transition_matrix_independently_rejects_unrelated_native_form_creation(self):
        # Inject a faulty helper body to exercise the matrix independently of
        # the public cast's stricter save-callback guard.
        w,ds,d,j=fixture()
        with self.assertRaisesRegex(SpellRuleError,'Unexpected parent transition'):
            j._run('bad-helper',0,'spell-checkpoint','world',
                lambda:d.shift(ds,'druid.base.bear-form-tank','F',0,j.wallets['a'],legal=True))
        self.assertEqual(j.receipts,());self.assertTrue(j.events[-1]['failed'])
        with self.assertRaisesRegex(SpellRuleError,'host reconciliation'):j.validate()

    def test_transition_matrix_rejects_wrong_selected_target_ending(self):
        w=world();j=observed(w);cast(j)
        with self.assertRaisesRegex(SpellRuleError,'Unexpected parent transition'):
            j._run('bad-dispel',1,'spell-dispel','c',lambda:w.dispel('b',legal=True),request={'target':'a'})
        self.assertEqual(len(j.receipts),3)
        self.assertTrue(j.events[-1]['failed'])
        with self.assertRaisesRegex(SpellRuleError,'host reconciliation'):j.validate()

    def test_outside_form_renewal_and_rest_never_receive_cast_origin(self):
        w,ds,d,j=fixture();shift(j,ds);j.renew('renew',ds,600)
        self.assertEqual(j.records('form-created','F')[0]['origin']['kind'],'OUTSIDE_EVENT')
        self.assertTrue(all(e['origin']['kind']=='OUTSIDE_EVENT' for e in j.events))
        self.assertEqual(j.records('form-renewed','F')[0]['operation'],'druid-renew')
        w=world();j=observed(w);cast(j)
        self.assertEqual(j.events[0]['origin']['kind'],'OUTSIDE_EVENT')
        self.assertEqual(j.records('cast-created','C')[0]['origin']['kind'],'OUTSIDE_CAST')
        self.assertEqual(j.records('cast-created','C')[0]['operation'],'spell-cast')

    def test_legitimate_concentration_replacement_keeps_both_closures(self):
        w=world();j=observed(w);cast(j);j.wallets['a'].actions=1
        cast(j,cid='D',event='second',now=1,target='c')
        self.assertEqual(w.links['C:b'].state,'new-concentration')
        self.assertEqual(w.links['D:c'].state,'shaping');j.validate()
        self.assertEqual(j.records('link-ended','C:b')[0]['operation'],'spell-cast')

    def test_legitimate_same_target_replacement_can_end_different_caster_link(self):
        w=world();j=observed(w);cast(j)
        cast(j,cid='D',event='second',now=1,target='b',owner='c')
        self.assertEqual(w.links['C:b'].state,'replaced');self.assertEqual(w.links['D:b'].state,'shaping')
        self.assertNotIn('a',w.concentration.current);j.validate()

    def test_expired_form_query_cannot_backdate_canonical_initiative(self):
        w,ds,d,j=fixture();shift(j,ds)
        j.scheduler=Scheduler('enc',('a','b','c'),now=ClockMarker(601));j.enter_initiative()
        with self.assertRaisesRegex(SpellRuleError,'canonical scheduler time'):j.valid_form_deadline('a','F',599)
        with self.assertRaisesRegex(SpellRuleError,'no longer valid'):j.valid_form_deadline('a','F')
        with self.assertRaisesRegex(SpellRuleError,'no longer valid'):j.valid_form_deadline('a','F',601)

    def test_query_uses_current_scheduler_and_outside_history_lower_bound(self):
        w,ds,d,j=fixture();shift(j,ds,now=10)
        with self.assertRaisesRegex(SpellRuleError,'predate observed history'):j.valid_form_deadline('a','F',9)
        with self.assertRaisesRegex(SpellRuleError,'actual world time'):j.valid_form_deadline('a','F')
        j.scheduler=Scheduler('enc',('a','b','c'),now=ClockMarker(11));j.enter_initiative()
        self.assertEqual(j.valid_form_deadline('a','F'),ClockMarker(610))

    def test_removed_form_pin_cannot_hide_equal_object_replacement(self):
        w,ds,d,j=fixture();shift(j,ds);original=d.current
        del j._pins[('form','a','F')]
        d.current=deepcopy(original);d.instances['F']=d.current
        with self.assertRaisesRegex(SpellRuleError,'pin manifest changed'):j.validate()
        self.assertIs(j._pin_manifest[('form','a','F')],original)

    def test_ended_concentration_pins_must_remain_retained(self):
        w=world();j=observed(w);cast(j);slot=w.concentration.current['a']
        j.end_concentration('end','a',1,reason='voluntary-release');j._slot_pins.clear()
        with self.assertRaisesRegex(SpellRuleError,'pin manifest changed'):j.validate()
        self.assertIs(j._slot_manifest[id(slot)][0],slot)
        self.assertIs(j._slot_manifest[id(slot)][1],slot[1])


if __name__=='__main__':
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(ParentHistoryTests)
    count=suite.countTestCases();result=unittest.TextTestRunner(verbosity=2).run(suite)
    root=Path(__file__).resolve().parents[1]
    report={'status':'PASS' if result.wasSuccessful() else 'FAIL','testMethods':count,
        'scope':'Actual native-operation source history only; no parent restoration/geometry/commit implementation',
        'helperSha256':hashlib.sha256((root/'tools/temporal_parent_history.py').read_bytes()).hexdigest(),
        'parentRuntimeIntegrated':False,'fullTimeLoopOperational':False,'remainingMajorIntegrations':7,
        'failures':len(result.failures),'errors':len(result.errors)}
    (root/'docs/mechanics/TEMPORAL_PARENT_HISTORY_VALIDATION.json').write_text(json.dumps(report,indent=2)+'\n')
    raise SystemExit(0 if result.wasSuccessful() else 1)
