"""Adversarial tests for the unpromoted temporal transaction kernel."""
from copy import deepcopy
from dataclasses import replace
from pathlib import Path
from fractions import Fraction
import hashlib
import json
import unittest

from temporal_playtest_rules import (
    TemporalKernel, Scheduler, Wallet, LifeState, MaximumContext, SoulIdentity,
    Inventory, PhysicalRecord, Geometry, Pose, EnvironmentAnchor, Memory,
    BufferGrant, ClockMarker, OneShot, RewardOpportunityKey, SpellRuleError,
    ExternalDependency, ExternalEffect, MaxHpRecord, SoulBind, SoulRecord,
    RoundId, TurnId,
)
from healing_playtest_rules import HealingReduction, healing_packet


def scene(*, capture=True, outsider=False):
    actors = ['a', 'b', 'foe'] + (['outside'] if outsider else [])
    lives = {a: LifeState(30, 25) for a in actors}
    wallets = {a: Wallet(rp=10) for a in actors}
    maxima = {a: MaximumContext(30, progression_signature=('level:20',)) for a in actors}
    souls = SoulIdentity(living=set(actors))
    inventory = Inventory(physical={a: PhysicalRecord(a, 'root', a) for a in actors})
    cells = frozenset((x, y) for x in range(20) for y in range(5))
    geometry = Geometry(cells, cells, {a: Pose((1+3*i, 2)) for i, a in enumerate(actors)})
    memory = Memory(known={a: {'start:'+a} for a in actors},
                    alliances={'a': {'a', 'b'}, 'b': {'b'}})
    scheduler = Scheduler('encounter-1', ('a', 'b', 'foe'), rc={'a': 5, 'b': 3})
    w = TemporalKernel(scheduler, wallets, lives, maxima, souls=souls,
                       inventory=inventory, geometry=geometry, memory=memory)
    if capture:
        w.capture(('a', 'b', 'foe'))
    return w


def event(w, name='attack-1', now=12):
    w.scheduler.now = ClockMarker(now)
    w.scheduler.begin_event(name)
    w.scheduler.finish_event(name)


def history(w):
    return deepcopy({
        'scheduler': vars(w.scheduler), 'wallets': {a:vars(v) for a,v in w.wallets.items()},
        'lives': {a:vars(v) for a,v in w.lives.items()}, 'buffers':vars(w.buffers),
        'healing':vars(w.healing), 'souls':vars(w.souls), 'inventory':vars(w.inventory),
        'geometry':vars(w.geometry), 'memory':vars(w.memory), 'rewards':vars(w.rewards),
        'external':vars(w.external), 'maxima':{a:vars(v) for a,v in w.maxima.items()}, 'history':vars(w.history),
    })


class TemporalTests(unittest.TestCase):
    def blocked(self, w, match, oracle='a'):
        before = history(w)
        with self.assertRaisesRegex(SpellRuleError, match):
            w.kernel_plan(oracle)
        self.assertEqual(history(w), before, 'Failed preflight mutated canonical state/cost')

    def test_full_time_loop_remains_gated(self):
        w = scene()
        self.assertFalse(w.support_report()['fullTimeLoopOperational'])
        self.assertEqual(len(w.support_report()['missing']), 7)
        with self.assertRaisesRegex(SpellRuleError, 'unavailable'):
            w.playable_plan('a')

    def test_atomic_restore_preserves_resources_and_object_aliases(self):
        w = scene()
        life, wallet, buffer = w.lives['a'], w.wallets['a'], w.buffers
        life.hp = 3
        life.wounds = (1,)
        wallet.rp = 2
        wallet.actions = 0
        wallet.used.add('daily-spent')
        w.scheduler.rc['a'] = 0
        w.scheduler.encounter_uses['a'] = {'encounter-spent'}
        w.geometry.poses['a'] = Pose((2, 3))
        event(w)
        before = history(w)
        plan = w.kernel_plan('a')
        self.assertEqual(history(w), before)
        plan.commit()
        self.assertIs(w.lives['a'], life)
        self.assertIs(w.wallets['a'], wallet)
        self.assertIs(w.buffers, buffer)
        self.assertEqual((life.hp, life.wounds, wallet.rp, wallet.actions), (25, (), 2, 1))
        self.assertEqual(wallet.used, {'daily-spent'})
        self.assertFalse(wallet.reaction)
        self.assertEqual(w.scheduler.rc['a'], 5)
        self.assertEqual(w.scheduler.encounter_uses['a'], set())
        self.assertEqual(w.geometry.poses['a'].anchor, (1, 2))
        self.assertEqual(w.scheduler.now, ClockMarker(12))
        self.assertEqual(w.scheduler.iteration, 1)
        with self.assertRaisesRegex(SpellRuleError, 'already committed'):
            plan.commit()

    def test_all_oracle_debts_survive_later_loop(self):
        w = scene()
        event(w)
        w.kernel_plan('a').commit()
        event(w, 'attack-2', 13)
        w.kernel_plan('b').commit()
        self.assertEqual(w.scheduler.debts, {'a', 'b'})
        self.assertFalse(w.wallets['a'].reaction)
        self.assertFalse(w.wallets['b'].reaction)
        self.assertEqual(w.scheduler.loop_uses, {('a', 0), ('b', 0)})

    def test_actual_regular_refresh_clears_only_owner_debt(self):
        w = scene()
        event(w)
        w.kernel_plan('a').commit()
        w.regular_start('a', 13)
        self.assertTrue(w.wallets['a'].reaction)
        self.assertNotIn('a', w.scheduler.debts)
        event(w, 'attack-2', 13)
        w.kernel_plan('b').commit()
        self.assertTrue(w.wallets['a'].reaction)
        self.assertEqual(w.scheduler.global_regular, 1)
        self.assertEqual(w.scheduler.debts, {'b'})

    def test_same_owner_long_rest_use_does_not_return(self):
        w = scene()
        event(w)
        w.kernel_plan('a').commit()
        w.regular_start('a', 13)
        event(w, 'attack-2', 13)
        self.blocked(w, 'already spent')

    def test_round_and_turn_keys_are_iteration_qualified(self):
        w = scene()
        before = w.scheduler.round_id().token()
        event(w)
        w.kernel_plan('a').commit()
        self.assertNotEqual(before, w.scheduler.round_id().token())
        self.assertNotEqual(TurnId('e', 0, 'a', 1).token(), TurnId('e', 1, 'a', 1).token())
        self.assertNotEqual(TurnId('e', 0, 'a', 1).token(), TurnId('e', 0, 'a', 1, 'extra').token())

    def test_timing_failures_spend_nothing(self):
        for kind in ('no-event', 'mid-event', 'late-round', 'queue'):
            with self.subTest(kind=kind):
                w = scene()
                if kind != 'no-event':
                    event(w)
                if kind == 'mid-event':
                    w.scheduler.begin_event('pending')
                if kind == 'late-round':
                    w.scheduler.round = 4
                if kind == 'queue':
                    w.scheduler.queued['command'] = {'owner': 'a'}
                self.blocked(w, 'resolved|round four|Queued')

    def test_stale_plan_detects_each_conserved_mutation(self):
        changes = (
            lambda w: setattr(w.wallets['a'], 'rp', 1),
            lambda w: w.inventory.quantities.update(potion=0),
            lambda w: w.buffers.rest_epochs.update(a=1),
            lambda w: w.rewards.claims.update(other='claim'),
            lambda w: w.memory.perceived.update(a={'new information'}),
        )
        for change in changes:
            w = scene(); event(w)
            plan = w.kernel_plan('a'); change(w); before = history(w)
            with self.assertRaisesRegex(SpellRuleError, 'Stale'):
                plan.commit()
            self.assertEqual(history(w), before)

    def test_stale_plan_detects_replaced_canonical_binding(self):
        w = scene(); event(w)
        plan = w.kernel_plan('a')
        w.wallets['a'] = deepcopy(w.wallets['a'])
        with self.assertRaisesRegex(SpellRuleError, 'registry changed'):
            plan.commit()
        self.assertFalse(w.scheduler.loop_uses)

    def test_stale_plan_detects_new_unknown_field(self):
        w = scene(); event(w)
        plan = w.kernel_plan('a')
        w.lives['a'].new_effect = 'unclassified'
        with self.assertRaisesRegex(SpellRuleError, 'schema changed'):
            plan.commit()
        self.assertFalse(w.scheduler.loop_uses)

    def test_maximum_hp_clamps_without_healing_critical_ceiling(self):
        w = scene(capture=False)
        w.lives['a'] = LifeState(30, 30, wounds=(1, 2, 3))
        w.capture(('a', 'b', 'foe'))
        w.maxima['a'].base = 20
        w.lives['a'].hp = 2
        event(w)
        w.kernel_plan('a').commit()
        self.assertEqual((w.lives['a'].maximum_hp, w.lives['a'].hp), (20, 20))
        self.assertEqual(w.lives['a'].wounds, (1, 2, 3))
        self.assertFalse(w.healing.committed_event_ids)
        self.assertFalse(w.buffers.damage_events)

    def test_larger_current_maximum_does_not_increase_snapshot_hp(self):
        w = scene(); w.maxima['a'].base = 100; event(w)
        w.kernel_plan('a').commit()
        self.assertEqual((w.lives['a'].maximum_hp, w.lives['a'].hp), (100, 25))

    def test_structural_progression_divergence_fails(self):
        w = scene(); w.maxima['a'].progression_signature += ('new-feat',); event(w)
        self.blocked(w, 'Progression')

    def test_rest_ended_monk_trauma_does_not_return(self):
        w = scene(capture=False)
        trauma = MaxHpRecord('trauma', 'monk.hero.iron-fist-master.ribcrusher-strike',
                             'b', 'a', 5, ends_on_completed_rest=True)
        w.maxima['a'].records = (trauma,)
        w.lives['a'] = LifeState(25, 20)
        w.capture(('a', 'b', 'foe'))
        w.maxima['a'].records = (replace(trauma, present=False, ended_reason='completed-target-short-rest'),)
        event(w); w.kernel_plan('a').commit()
        self.assertEqual(w.lives['a'].maximum_hp, 30)

    def test_stable_resolved_or_expired_event_never_replays(self):
        for resolved, now in ((True, 12), (False, 3600)):
            w = scene(capture=False)
            w.lives['b'] = LifeState(30, 0, stable=True, stable_until_seconds=3600)
            w.souls.stable_event_ids['b'] = 'recovery-1'
            w.capture(('a', 'b', 'foe'))
            if resolved:
                w.souls.resolved_stable.add('recovery-1')
            event(w, now=now)
            self.blocked(w, 'Stable')

    def test_valid_stable_deadline_is_not_rebased(self):
        w = scene(capture=False)
        w.lives['b'] = LifeState(30, 0, stable=True, stable_until_seconds=3600)
        w.souls.stable_event_ids['b'] = 'recovery-1'
        w.capture(('a', 'b', 'foe'))
        event(w); w.kernel_plan('a').commit()
        self.assertEqual(w.lives['b'].stable_until_seconds, 3600)

    def test_same_body_returns_without_revival_event(self):
        w = scene()
        w.lives['b'] = LifeState(30, 0, dead=True)
        w.souls.living.remove('b'); w.souls.deaths['b'] = 'death-1'
        w.souls.remains['b'] = {'corpse': 'body-b'}
        event(w); w.kernel_plan('a').commit()
        self.assertFalse(w.lives['b'].dead)
        self.assertEqual(w.lives['b'].hp, 25)
        self.assertNotIn('b', w.souls.deaths)
        self.assertNotIn('b', w.souls.remains)
        self.assertEqual(w.souls.return_history, set())

    def test_soul_bind_keeps_original_deadline(self):
        for now, present in ((12, True), (60, False)):
            w = scene(capture=False)
            w.lives['b'] = LifeState(30, 0)
            w.souls.binds['bind'] = SoulRecord('bind', 'foe', 'b', SoulBind('b', 'pending', 60))
            w.capture(('a', 'b', 'foe')); event(w, now=now)
            w.kernel_plan('a').commit()
            self.assertEqual('bind' in w.souls.binds, present)
            if present:
                self.assertEqual(w.souls.binds['bind'].bind.expires, 60)

    def test_post_snapshot_death_bind_becomes_inactive(self):
        w = scene()
        w.lives['b'] = LifeState(30, 0, dead=True)
        w.souls.living.remove('b'); w.souls.deaths['b'] = 'death-1'
        w.souls.binds['bind'] = SoulRecord('bind', 'foe', 'b', SoulBind('b', 'bound', 86400), 'death-1')
        event(w); w.kernel_plan('a').commit()
        self.assertFalse(w.souls.binds)

    def test_default_buffer_restores_same_id_remaining_not_new_offer(self):
        w = scene(capture=False)
        w.buffers.offer(BufferGrant('shield', 'feat:chef', 'b', 'a', 8, rest_epoch=0))
        w.lives['a'].temp_hp = 8
        w.capture(('a', 'b', 'foe'))
        w.buffers.grants['shield'].remaining = 2
        w.lives['a'].temp_hp = 2
        w.buffers.damage_events.add(('a', 'damage-old'))
        event(w); w.kernel_plan('a').commit()
        self.assertEqual((w.buffers.amount('a'), w.lives['a'].temp_hp), (8, 8))
        self.assertEqual(set(w.buffers.grants), {'shield'})
        self.assertEqual(w.buffers.damage_events, {('a', 'damage-old')})

    def test_buffer_real_rest_invalidates_snapshot_grant(self):
        w = scene(capture=False)
        w.buffers.offer(BufferGrant('shield', 'feat:chef', 'b', 'a', 8, rest_epoch=0))
        w.lives['a'].temp_hp = 8
        w.capture(('a', 'b', 'foe'))
        w.buffers.completed_long_rest('a', 1)
        w.lives['a'].temp_hp = 0
        event(w); w.kernel_plan('a').commit()
        self.assertEqual((w.buffers.amount('a'), w.lives['a'].temp_hp), (0, 0))

    def test_blood_ally_absolute_buffer_expired_does_not_return(self):
        w = scene(capture=False)
        w.buffers.offer(BufferGrant('blood', 'feat:blood_ritual', 'a', 'b', 8, expiry=ClockMarker(3600)))
        w.lives['b'].temp_hp = 8
        w.capture(('a', 'b', 'foe')); event(w, now=3600)
        w.kernel_plan('a').commit()
        self.assertEqual(w.lives['b'].temp_hp, 0)

    def test_unknown_buffer_source_is_unavailable(self):
        w = scene(capture=False)
        w.buffers.offer(BufferGrant('x', 'future-source', 'a', 'a', 8, rest_epoch=0))
        w.lives['a'].temp_hp = 8
        with self.assertRaisesRegex(SpellRuleError, 'No temporal source policy'):
            w.capture(('a', 'b', 'foe'))
        self.assertIsNone(w._snapshot)

    def test_external_late_buffer_not_silently_erased(self):
        w = scene(outsider=True)
        w.buffers.offer(BufferGrant('shield', 'feat:chef', 'outside', 'a', 8, rest_epoch=0))
        w.lives['a'].temp_hp = 8
        event(w); self.blocked(w, 'external buffer')

    def test_one_shot_same_id_new_consumption_view_preserves_audit(self):
        w = scene(capture=False)
        shot = OneShot('agony-1', 'feat:soul_cage:agony', 'a', 'foe', True, ClockMarker(60))
        w.healing.register(shot)
        w.capture(('a', 'b', 'foe'))
        reduction = HealingReduction('agony-1', 'agony', 'factor', Fraction(1, 2), next_healing=True)
        packet = healing_packet(w.lives['foe'], 8, reductions=(reduction,))
        w.healing.commit('heal-1', packet)
        event(w); w.kernel_plan('a').commit()
        self.assertTrue(w.healing.records['agony-1'].available)
        self.assertEqual(w.healing.commit('heal-2', packet), {'agony-1'})
        self.assertEqual(w.healing.consumed_reducer_ids, {('agony-1', 0), ('agony-1', 1)})
        self.assertEqual(w.healing.committed_event_ids, {'heal-1', 'heal-2'})
        with self.assertRaisesRegex(SpellRuleError, 'already committed'):
            w.healing.commit('heal-1', packet)

    def test_snapshot_consumed_one_shot_stays_consumed(self):
        w = scene(capture=False)
        w.healing.register(OneShot('agony-1', 'feat:soul_cage:agony', 'a', 'foe', False, ClockMarker(60)))
        w.capture(('a', 'b', 'foe')); event(w)
        w.kernel_plan('a').commit()
        self.assertFalse(w.healing.records['agony-1'].available)
        with self.assertRaisesRegex(SpellRuleError, 'already consumed'):
            w.healing.commit('heal-1', {'nextHealingCandidates': ['agony-1']})

    def test_expired_one_shot_stays_unavailable(self):
        w = scene(capture=False)
        w.healing.register(OneShot('agony-1', 'feat:soul_cage:agony', 'a', 'foe', True, ClockMarker(60)))
        w.capture(('a', 'b', 'foe')); event(w, now=60)
        w.kernel_plan('a').commit()
        self.assertFalse(w.healing.records['agony-1'].available)

    def test_reward_opportunity_not_fresh_death_event(self):
        w = scene()
        key = RewardOpportunityKey('encounter-1', 'foe', 'xp', 'defeat')
        w.rewards.opportunities.add(key); w.rewards.claim(key, 'death-1')
        event(w); w.kernel_plan('a').commit()
        with self.assertRaisesRegex(SpellRuleError, 'already claimed'):
            w.rewards.claim(key, 'death-2')
        other = RewardOpportunityKey('encounter-1', 'foe', 'harvest', 'gland')
        w.rewards.opportunities.add(other); w.rewards.claim(other, 'harvest-1')
        self.assertEqual(len(w.rewards.claims), 2)

    def test_immutable_snapshot_cannot_be_recaptured(self):
        w = scene()
        with self.assertRaisesRegex(SpellRuleError, 'already exists'):
            w.capture(('a', 'b', 'foe'))

    def test_snapshot_returned_copy_cannot_change_original(self):
        w = scene(capture=False)
        returned = w.capture(('a', 'b', 'foe'))
        returned.life['a'].hp = 1
        event(w); w.kernel_plan('a').commit()
        self.assertEqual(w.lives['a'].hp, 25)

    def test_physical_derivative_entity_retires_cost_conserved(self):
        w = scene()
        w.inventory.physical['raised'] = PhysicalRecord('raised', 'temporal-entity', 'a', ('foe',), 0,
                                                        source_owner='a')
        w.geometry.poses['raised'] = Pose((17, 2))
        w.inventory.quantities['onyx'] = 0
        w.inventory.expenditure_events.add('raise-cost')
        event(w); w.kernel_plan('a').commit()
        self.assertFalse(w.inventory.physical['raised'].survives)
        self.assertNotIn('raised', w.geometry.poses)
        self.assertEqual(w.inventory.quantities['onyx'], 0)
        self.assertEqual(w.inventory.expenditure_events, {'raise-cost'})

    def test_transitive_surviving_inventory_derivative_blocks(self):
        w = scene()
        w.inventory.physical['harvest'] = PhysicalRecord('harvest', 'inventory', 'a', ('foe',), 0, False)
        w.inventory.physical['sale'] = PhysicalRecord('sale', 'inventory', 'outside', ('harvest',), 0)
        event(w); self.blocked(w, 'transferable derivative')

    def test_mixed_roots_and_external_asset_slot_block(self):
        for mode in ('mixed', 'binding', 'enrollment'):
            w = scene()
            w.inventory.physical['ore'] = PhysicalRecord('ore', 'root', 'outside')
            w.inventory.physical['new'] = PhysicalRecord('new', 'temporal-entity', 'a',
                ('foe', 'ore') if mode == 'mixed' else ('foe',), 0, source_owner='a',
                external_binding='slot' if mode == 'binding' else None,
                persistent_enrollment='asset' if mode == 'enrollment' else None)
            event(w); self.blocked(w, 'Mixed|external source slot')

    def test_consumed_derivative_remains_consumed(self):
        w = scene()
        w.inventory.physical['used'] = PhysicalRecord('used', 'inventory', 'a', ('foe',), 0, False)
        event(w); w.kernel_plan('a').commit()
        self.assertFalse(w.inventory.physical['used'].survives)

    def test_transferred_original_item_ownership_is_conserved(self):
        w = scene(capture=False)
        w.inventory.physical['sword'] = PhysicalRecord('sword', 'inventory', 'a')
        w.capture(('a', 'b', 'foe'))
        w.inventory.physical['sword'] = replace(w.inventory.physical['sword'], owner='outside')
        event(w); w.kernel_plan('a').commit()
        self.assertEqual(w.inventory.physical['sword'].owner, 'outside')

    def test_provenance_cycle_blocks(self):
        w = scene()
        w.inventory.physical['x'] = PhysicalRecord('x', 'inventory', 'a', ('y',))
        w.inventory.physical['y'] = PhysicalRecord('y', 'inventory', 'a', ('x',))
        event(w); self.blocked(w, 'cycle')

    def test_snapshot_pose_overlap_with_outsider_blocks(self):
        w = scene(outsider=True)
        w.geometry.poses['outside'] = Pose((1, 2))
        w.geometry.poses['a'] = Pose((0, 0))
        event(w); self.blocked(w, 'overlap')

    def test_atomic_participant_exchange_is_legal(self):
        w = scene()
        w.geometry.poses['a'], w.geometry.poses['b'] = w.geometry.poses['b'], w.geometry.poses['a']
        event(w); w.kernel_plan('a').commit()
        self.assertEqual(w.geometry.poses['a'].anchor, (1, 2))
        self.assertEqual(w.geometry.poses['b'].anchor, (4, 2))

    def test_environment_cannot_enclose_outsider_without_cell_overlap(self):
        w = scene(capture=False, outsider=True)
        wall = EnvironmentAnchor('wall', blocked=frozenset((12, y) for y in range(5)))
        w.geometry.anchors['wall'] = wall
        w.inventory.physical['wall'] = PhysicalRecord('wall', 'root', None)
        w.capture(('a', 'b', 'foe'), ('wall',))
        w.geometry.anchors['wall'] = replace(wall, blocked=frozenset())
        event(w); self.blocked(w, 'restricts a protected outsider')

    def test_environment_cannot_remove_external_support(self):
        w = scene(capture=False, outsider=True)
        w.geometry.fixed_support -= {(10, 2)}
        w.geometry.poses['outside'] = Pose((11, 2))
        floor = EnvironmentAnchor('floor')
        w.geometry.anchors['floor'] = floor
        w.inventory.physical['floor'] = PhysicalRecord('floor', 'root', None)
        w.capture(('a', 'b', 'foe'), ('floor',))
        w.geometry.anchors['floor'] = replace(floor, support=frozenset({(10, 2)}))
        w.geometry.poses['outside'] = Pose((10, 2))
        event(w); self.blocked(w, 'lost support')

    def test_external_concentration_not_recreated_or_changed(self):
        w = scene(capture=False, outsider=True)
        w.external.concentration['outside'] = 'cast-original'
        w.external.dependencies = (ExternalDependency('effect', 'b', 'outside', 'cast-original'),)
        w.capture(('a', 'b', 'foe'))
        w.lives['outside'].hp = 5
        event(w); w.kernel_plan('a').commit()
        self.assertEqual(w.external.concentration['outside'], 'cast-original')
        self.assertEqual(w.lives['outside'].hp, 5)
        event(w, 'attack-2', 13)
        w.external.concentration['outside'] = 'cast-new'
        self.blocked(w, 'External concentration', oracle='b')

    def test_external_new_maximum_modifier_overlays_snapshot(self):
        w = scene(outsider=True)
        modifier = MaxHpRecord('external-trauma', 'monk.hero.iron-fist-master.ribcrusher-strike',
                               'outside', 'a', 9, ends_on_completed_rest=True)
        w.external.effects['external-trauma'] = ExternalEffect('external-trauma', 'outside', 'a',
                                                              'maximum-hp', modifier)
        event(w); w.kernel_plan('a').commit()
        self.assertEqual(w.lives['a'].maximum_hp, 21)
        self.assertEqual(w.lives['a'].hp, 21)

    def test_external_unknown_anatomy_blocks(self):
        w = scene(outsider=True)
        w.external.effects['new-form'] = ExternalEffect('new-form', 'outside', 'a', 'anatomy')
        event(w); self.blocked(w, 'External anatomy')

    def test_memory_only_snapshot_allies_and_observed_facts(self):
        w = scene()
        w.memory.perceived = {'a': {'saw trap'}, 'b': {'heard warning'}, 'foe': {'saw attack'}}
        w.memory.known['foe'].add('saw attack')
        w.memory.alliances['a'] = {'foe'}
        event(w); w.kernel_plan('a').commit()
        self.assertIn('saw trap', w.memory.known['a'])
        self.assertIn('heard warning', w.memory.known['b'])
        self.assertNotIn('saw attack', w.memory.known['foe'])
        self.assertNotIn('heard warning', w.memory.known['a'])
        self.assertNotIn('secret stats', set.union(*w.memory.known.values()))

    def test_retained_memory_is_cumulative_across_different_oracles(self):
        w = scene()
        w.memory.perceived = {'a': {'first'}, 'b': {'first-b'}}
        event(w); w.kernel_plan('a').commit()
        w.memory.perceived = {'a': {'second-a'}, 'b': {'second-b'}}
        event(w, 'attack-2', 13); w.kernel_plan('b').commit()
        self.assertIn('first', w.memory.known['a'])
        self.assertNotIn('second-a', w.memory.known['a'])
        self.assertTrue({'first-b', 'second-b'} <= w.memory.known['b'])

    def test_unsupported_holder_and_dynamic_state_fail(self):
        w = scene(); w.integrations['DruidState'] = object(); event(w)
        self.blocked(w, 'Unsupported active')
        w = scene(); w.buffers.new_refill = 10; event(w)
        self.blocked(w, 'Unclassified')

    def test_discarded_death_and_grant_records_remain_in_audit(self):
        w = scene()
        w.lives['b'] = LifeState(30, 0, dead=True)
        w.souls.living.remove('b'); w.souls.deaths['b'] = 'death-1'
        event(w); w.kernel_plan('a').commit()
        frame = w.history.frames[0]
        change = next(x for x in frame['changes'] if x['holder'] == 'souls' and x['field'] == 'deaths')
        self.assertEqual(change['before']['b'], 'death-1')
        self.assertNotIn('b', change['after'])
        self.assertNotIn('death-1', w.memory.known['a'])

    def test_destroyed_participant_root_restores_same_physical_identity(self):
        w = scene()
        w.inventory.physical['b'] = replace(w.inventory.physical['b'], survives=False)
        w.lives['b'] = LifeState(30, 0, dead=True)
        w.souls.living.remove('b'); w.souls.deaths['b'] = 'death-1'
        event(w); w.kernel_plan('a').commit()
        self.assertTrue(w.inventory.physical['b'].survives)
        self.assertFalse(w.lives['b'].dead)
        self.assertEqual(set(w.inventory.physical), {'a', 'b', 'foe'})

    def test_deleted_or_reused_physical_history_rejects(self):
        for kind in ('removed', 'reused', 'ownership'):
            w = scene()
            if kind == 'removed':
                del w.inventory.physical['b']
            elif kind == 'reused':
                w.inventory.physical['b'] = replace(w.inventory.physical['b'], roots=('foe',))
            else:
                w.inventory.physical['b'] = replace(w.inventory.physical['b'], owner='outside')
            event(w); self.blocked(w, 'Physical history|provenance changed|ownership')

    def test_one_canonical_rest_epoch_controls_loop_use(self):
        w = scene(); event(w); w.kernel_plan('a').commit()
        w.buffers.completed_long_rest('a', 1)
        w.regular_start('a', 13)
        event(w, 'event-after-real-rest', 13)
        w.kernel_plan('a').commit()
        self.assertEqual(w.scheduler.loop_uses, {('a', 0), ('a', 1)})

    def test_external_current_record_replaces_stale_same_id_projection(self):
        w = scene(outsider=True)
        old = MaxHpRecord('external-trauma', 'monk.hero.iron-fist-master.ribcrusher-strike',
                          'outside', 'a', 3, ends_on_completed_rest=True)
        w.maxima['a'].records = (old,)
        new = replace(old, amount=10)
        w.external.effects['external-trauma'] = ExternalEffect('external-trauma', 'outside', 'a', 'maximum-hp', new)
        event(w); w.kernel_plan('a').commit()
        self.assertEqual(w.lives['a'].maximum_hp, 20)

    def test_world_marker_never_moves_before_snapshot(self):
        w = scene(capture=False)
        w.scheduler.now = ClockMarker(20)
        w.capture(('a', 'b', 'foe'))
        event(w, now=10)
        self.blocked(w, 'moved backward')

    def test_retired_temporal_wall_removes_its_geometry_too(self):
        w = scene()
        w.inventory.physical['temporary-wall'] = PhysicalRecord('temporary-wall', 'temporal-entity',
            'a', ('foe',), 0, source_owner='a')
        w.geometry.anchors['temporary-wall'] = EnvironmentAnchor('temporary-wall', blocked=frozenset({(15, 3)}))
        event(w); w.kernel_plan('a').commit()
        self.assertFalse(w.inventory.physical['temporary-wall'].survives)
        self.assertNotIn('temporary-wall', w.geometry.anchors)

    def test_retiring_temporal_floor_cannot_drop_outsider(self):
        w = scene(capture=False, outsider=True)
        w.geometry.poses['outside'] = Pose((11, 2))
        w.geometry.fixed_support -= {(10, 2)}
        w.capture(('a', 'b', 'foe'))
        w.inventory.physical['temporary-floor'] = PhysicalRecord('temporary-floor', 'temporal-entity',
            'a', ('foe',), 0, source_owner='a')
        w.geometry.anchors['temporary-floor'] = EnvironmentAnchor('temporary-floor', support=frozenset({(10, 2)}))
        w.geometry.poses['outside'] = Pose((10, 2))
        event(w); self.blocked(w, 'lost support')

    def test_out_of_order_regular_start_cannot_clear_debt(self):
        w = scene(); event(w); w.kernel_plan('a').commit()
        event(w, 'second', 13); w.kernel_plan('b').commit()
        before = history(w)
        with self.assertRaisesRegex(SpellRuleError, 'initiative cursor'):
            w.regular_start('b', 13)
        self.assertEqual(history(w), before)
        self.assertEqual(w.scheduler.debts, {'a', 'b'})

    def test_repeated_regular_start_cannot_create_marker_or_refresh(self):
        w = scene()
        first = w.regular_start('a', 0)
        before = history(w)
        with self.assertRaisesRegex(SpellRuleError, 'already active'):
            w.regular_start('a', 0)
        self.assertEqual(history(w), before)
        w.scheduler.regular_end(first, 1)
        self.assertEqual(w.scheduler.cursor, 1)
        second = w.regular_start('b', 1)
        w.scheduler.regular_end(second, 2)
        third = w.regular_start('foe', 2)
        w.scheduler.regular_end(third, 3)
        self.assertEqual((w.scheduler.round, w.scheduler.cursor, w.scheduler.global_regular), (2, 0, 3))

    def test_foreign_or_replayed_regular_end_is_rejected(self):
        w = scene()
        turn = w.regular_start('a', 0)
        with self.assertRaisesRegex(SpellRuleError, 'actual active'):
            w.scheduler.regular_end(replace(turn, actor='b'), 1)
        w.scheduler.regular_end(turn, 1)
        with self.assertRaisesRegex(SpellRuleError, 'actual active'):
            w.scheduler.regular_end(turn, 1)

    def test_destroyed_snapshot_wall_restores_physics_and_geometry(self):
        w = scene(capture=False)
        wall = EnvironmentAnchor('wall', blocked=frozenset({(15, 3)}))
        w.geometry.anchors['wall'] = wall
        w.inventory.physical['wall'] = PhysicalRecord('wall', 'root', None)
        w.capture(('a', 'b', 'foe'), ('wall',))
        w.inventory.physical['wall'] = replace(w.inventory.physical['wall'], survives=False)
        w.geometry.anchors['wall'] = replace(wall, blocked=frozenset())
        event(w); w.kernel_plan('a').commit()
        self.assertTrue(w.inventory.physical['wall'].survives)
        self.assertEqual(w.geometry.anchors['wall'], wall)

    def test_unbound_or_wrong_identity_anchor_cannot_be_captured(self):
        for kind in ('missing', 'identity', 'hazard'):
            w = scene(capture=False)
            w.geometry.anchors['wall'] = EnvironmentAnchor('other' if kind == 'identity' else 'wall')
            if kind != 'missing':
                w.inventory.physical['wall'] = PhysicalRecord('wall', 'inventory' if kind == 'hazard' else 'root', None)
            with self.assertRaisesRegex(SpellRuleError, 'Environment anchor|Nonphysical'):
                w.capture(('a', 'b', 'foe'), ('wall',))
            self.assertIsNone(w._snapshot)

    def test_new_external_dependency_without_overlay_blocks(self):
        w = scene(outsider=True)
        w.external.concentration['outside'] = 'new-cast'
        w.external.dependencies = (ExternalDependency('new-effect', 'b', 'outside', 'new-cast'),)
        event(w); self.blocked(w, 'New external dependency')

    def test_new_supported_external_dependency_is_preserved(self):
        w = scene(outsider=True)
        w.external.concentration['outside'] = 'new-cast'
        w.external.dependencies = (ExternalDependency('trauma', 'b', 'outside', 'new-cast'),)
        record = MaxHpRecord('trauma', 'monk.hero.iron-fist-master.ribcrusher-strike',
                              'outside', 'b', 7, ends_on_completed_rest=True)
        w.external.effects['trauma'] = ExternalEffect('trauma', 'outside', 'b', 'maximum-hp', record)
        event(w); w.kernel_plan('a').commit()
        self.assertEqual(w.lives['b'].maximum_hp, 23)
        self.assertEqual(w.external.concentration['outside'], 'new-cast')
        self.assertEqual(len(w.external.dependencies), 1)

    def test_missing_dependency_cannot_hide_behind_same_concentration_id(self):
        w = scene(capture=False, outsider=True)
        w.external.concentration['outside'] = 'original'
        w.external.dependencies = (ExternalDependency('effect', 'b', 'outside', 'original'),)
        w.capture(('a', 'b', 'foe'))
        w.external.dependencies = ()
        event(w); self.blocked(w, 'dependency disappeared')

    def test_valid_maximum_source_without_temporal_policy_is_blocked(self):
        w = scene()
        # This source IS accepted by the existing MaxHpRecord constructor; its
        # creating-Wizard/creature lifecycle temporal adapter is still absent.
        record = MaxHpRecord('creation-bonus', 'wizard.engine[10]', 'a', 'a', 5)
        w.maxima['a'].records = (record,)
        event(w); self.blocked(w, 'No temporal maximum-HP source policy')

    def test_reviewers_arbitrary_maxhp_examples_already_fail_source_constructor(self):
        for source in ('some.participant.temporary.maxhp', 'monk.passive.permanent-maxhp'):
            with self.assertRaisesRegex(SpellRuleError, 'Unreviewed maximumHP modifier source'):
                MaxHpRecord('unknown', source, 'a', 'a', 5)

    def test_passive_maximum_source_cannot_disguise_temporary_endpoint(self):
        w = scene()
        w.maxima['a'].records = (MaxHpRecord('feat-bonus', 'feat:tenacity', 'a', 'a', 5, expires=ClockMarker(60)),)
        event(w); self.blocked(w, 'unsupported temporary endpoint')

    def test_missing_required_buffer_history_field_blocks(self):
        w = scene(); del w.buffers.damage_events; event(w)
        self.blocked(w, 'missing required BufferLedger')

    def test_buffer_target_state_amount_and_duplicate_identity_invariants(self):
        for kind in ('target', 'state', 'zero', 'duplicate'):
            w = scene(capture=False)
            w.buffers.offer(BufferGrant('shield', 'feat:chef', 'a', 'a', 8, rest_epoch=0))
            w.lives['a'].temp_hp = 8
            if kind == 'target':
                w.buffers.grants['shield'].target = 'b'
            elif kind == 'state':
                w.buffers.grants['shield'].state = 'rejected'
            elif kind == 'zero':
                w.buffers.grants['shield'].remaining = 0; w.lives['a'].temp_hp = 0
            else:
                w.buffers.active['b'] = 'shield'; w.lives['b'].temp_hp = 8
            with self.assertRaisesRegex(SpellRuleError, 'Active grant|Malformed active|multiple targets'):
                w.capture(('a', 'b', 'foe'))
            self.assertIsNone(w._snapshot)

    def test_pending_soul_bind_rejects_positive_hp_stable_dead_and_death_id(self):
        for kind in ('positive', 'stable', 'dead', 'death-id'):
            w = scene(capture=False)
            w.lives['b'] = LifeState(30, 25 if kind == 'positive' else 0,
                                     stable=kind == 'stable', dead=kind == 'dead')
            if kind == 'dead':
                w.souls.living.remove('b'); w.souls.deaths['b'] = 'death'
            w.souls.binds['bind'] = SoulRecord('bind', 'foe', 'b', SoulBind('b', 'pending', 60),
                                              'death' if kind == 'death-id' else None)
            with self.assertRaisesRegex(SpellRuleError, 'living dying'):
                w.capture(('a', 'b', 'foe'))
            self.assertIsNone(w._snapshot)

    def test_bound_soul_record_requires_matching_identity_and_death(self):
        for kind in ('application', 'target', 'death'):
            w = scene(capture=False)
            w.lives['b'] = LifeState(30, 0, dead=True)
            w.souls.living.remove('b'); w.souls.deaths['b'] = 'death-1'
            w.souls.binds['bind'] = SoulRecord('other' if kind == 'application' else 'bind', 'foe', 'b',
                SoulBind('foe' if kind == 'target' else 'b', 'bound', 86400), 'death-2' if kind == 'death' else 'death-1')
            with self.assertRaisesRegex(SpellRuleError, 'identity mismatch|exact current dead'):
                w.capture(('a', 'b', 'foe'))

    def test_valid_snapshot_dead_bound_record_stays_dead_and_bound(self):
        w = scene(capture=False)
        w.lives['b'] = LifeState(30, 0, dead=True)
        w.souls.living.remove('b'); w.souls.deaths['b'] = 'death-1'
        w.souls.binds['bind'] = SoulRecord('bind', 'foe', 'b', SoulBind('b', 'bound', 86400), 'death-1')
        w.capture(('a', 'b', 'foe')); event(w); w.kernel_plan('a').commit()
        self.assertTrue(w.lives['b'].dead)
        self.assertEqual(w.souls.binds['bind'].death_instance, 'death-1')

    def test_public_regular_start_cannot_accept_another_actors_wallet(self):
        w = scene(); event(w); w.kernel_plan('a').commit()
        event(w, 'second', 13); w.kernel_plan('b').commit()
        before = history(w)
        with self.assertRaises(TypeError):
            w.regular_start('a', 13, wallet=w.wallets['b'])
        self.assertEqual(history(w), before)
        self.assertFalse(hasattr(w.scheduler, 'regular_start'), 'Unsafe public entry point must not remain')
        turn = w.regular_start('a', 13)
        self.assertTrue(w.wallets['a'].reaction)
        self.assertFalse(w.wallets['b'].reaction)
        self.assertEqual(w.scheduler.debts, {'b'})
        w.scheduler.regular_end(turn, 14)
        w.regular_start('b', 14)
        self.assertTrue(w.wallets['b'].reaction)

    def test_distinct_actors_cannot_alias_one_wallet(self):
        w = scene(); w.wallets['a'] = w.wallets['b']; before = history(w)
        with self.assertRaisesRegex(SpellRuleError, 'alias the same canonical wallet'):
            w.regular_start('a', 0)
        self.assertEqual(history(w), before)

    def test_live_one_shot_registry_is_validated_without_register(self):
        changes = {
            'source': {'source_id':'future:unreviewed-source'},
            'key': {'effect_id':'different'},
            'expiry': {'expires':None},
            'rest': {'rest_epoch':0},
            'owner': {'owner':'unknown'},
            'target': {'target':'unknown'},
            'availability': {'available':'yes'},
        }
        for stage in ('capture', 'preflight'):
            for name, change in changes.items():
                with self.subTest(stage=stage, malformed=name):
                    w = scene(capture=stage == 'preflight')
                    row = OneShot('x', 'feat:soul_cage:agony', 'a', 'b', True, ClockMarker(60))
                    w.healing.records['x'] = replace(row, **change)
                    if stage == 'preflight':
                        event(w); self.blocked(w, 'one-shot|One-shot|Agony')
                    else:
                        before = history(w)
                        with self.assertRaises(SpellRuleError):
                            w.capture(('a', 'b', 'foe'))
                        self.assertEqual(history(w), before)
                        self.assertIsNone(w._snapshot)

    def test_live_one_shot_availability_cannot_conflict_with_history(self):
        w = scene(capture=False)
        w.healing.register(OneShot('x', 'feat:soul_cage:agony', 'a', 'b', True, ClockMarker(60)))
        w.healing.commit('heal-1', {'nextHealingCandidates':['x']})
        w.healing.records['x'] = replace(w.healing.records['x'], available=True)
        with self.assertRaisesRegex(SpellRuleError, 'both available and consumed'):
            w.capture(('a', 'b', 'foe'))

    def test_consumption_token_requires_matching_historical_event(self):
        w = scene(); w.healing.consumed_reducer_ids.add(('old', 0)); event(w)
        self.blocked(w, 'missing historical evidence')
        w = scene(); w.healing.consumption_history.add(('old', 0, 'absent-event')); event(w)
        self.blocked(w, 'missing its committed event')

    def test_external_effect_key_and_dependency_identity_cannot_differ(self):
        for stage in ('capture', 'preflight'):
            for with_dependency in (False, True):
                w = scene(capture=stage == 'preflight', outsider=True)
                record = MaxHpRecord('effect-B', 'monk.hero.iron-fist-master.ribcrusher-strike',
                                      'outside', 'b', 7, ends_on_completed_rest=True)
                w.external.effects['dep-A'] = ExternalEffect('effect-B', 'outside', 'b', 'maximum-hp', record)
                if with_dependency:
                    w.external.concentration['outside'] = 'cast'
                    w.external.dependencies = (ExternalDependency('dep-A', 'b', 'outside', 'cast'),)
                if stage == 'preflight':
                    event(w); self.blocked(w, 'dictionary/application identity mismatch')
                else:
                    before = history(w)
                    with self.assertRaisesRegex(SpellRuleError, 'dictionary/application identity mismatch'):
                        w.capture(('a', 'b', 'foe'))
                    self.assertEqual(history(w), before)


def main():
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TemporalTests)
    result = unittest.TextTestRunner(verbosity=1).run(suite)
    root = Path(__file__).resolve().parents[1]
    report = {
        'status': 'PASS' if result.wasSuccessful() else 'FAIL',
        'scope': 'Unpromoted foundational temporal kernel only; seven integrations and actual notebook review remain',
        'testMethods': result.testsRun,
        'failures': len(result.failures), 'errors': len(result.errors),
        'fullTimeLoopOperational': False,
        'helperSha256': hashlib.sha256((root/'tools/temporal_playtest_rules.py').read_bytes()).hexdigest(),
    }
    (root/'docs/mechanics/TEMPORAL_KERNEL_VALIDATION.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(report))
    raise SystemExit(0 if result.wasSuccessful() else 1)


if __name__ == '__main__':
    main()
