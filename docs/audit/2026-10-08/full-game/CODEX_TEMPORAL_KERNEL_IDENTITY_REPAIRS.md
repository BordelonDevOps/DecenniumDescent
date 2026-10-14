# Exact fixes for the three identity/admission findings

Thank you for confirming the original six repairs. The remaining three now have targeted fixes and regressions; all76 methods pass. This packet is an exact verified unified diff against the complete70-test helper/tests/guide you just reviewed. The original packet and hashes are preserved. There are no unshown edits to these files.

1. Public regular-start API is now TemporalKernel.regular_start(actor, now). It obtains self.wallets[actor] internally, accepts NO wallet argument, and rejects actors aliasing one Wallet. Scheduler._regular_start is private implementation only; the unsafe public scheduler.regular_start entry point is removed. All existing tests use the public world wrapper. A new regression tries supplying B's actual Wallet for A and confirms rejection without mutation, then confirms a proper A start leaves B's Reaction/debt untouched.
2. Capture and preflight now independently validate EVERY live one-shot record, even if inserted directly without register(): exact key/ID/source, original absolute Agony clock/no rest substitute, canonical scene owner/target and boolean availability. History validates set/token/event shapes, nonfuture iterations, corresponding committed event evidence and no duplicate consumption pair. An available record cannot simultaneously be consumed in the current generation. Sixteen direct-malformation subcases cover capture/preflight plus dedicated conflicting-history cases.
3. Every ExternalEffect dictionary key must equal its identity, and maximum-HP entries must match record application/owner/target. New dependency satisfaction also explicitly requires dep.effect_id == effect.identity. Tests cover both capture and preflight with and without a misleading dependency lookup key.

Please confirm whether the three findings are resolved in this admitted scope, or give any remaining reproducible blocker. This is only a bounded foundational checkpoint: playable_plan remains unavailable, seven source integrations remain absent, and whole-game/GitHub gates remain open.


## tools/temporal_playtest_rules.py

```diff
--- reviewed70/tools/temporal_playtest_rules.py
+++ current76/tools/temporal_playtest_rules.py
@@ -199,7 +199,8 @@
         self.last_completed_event = event_id
         self.completed_events.add(event_id)
 
-    def regular_start(self, actor, wallet, now):
+    def _regular_start(self, actor, wallet, now):
+        """Internal mutation; public callers use TemporalKernel.regular_start."""
         shape(wallet, Wallet)
         require(self.atomic_event is None and self.active_regular is None,
                 'Regular turn already active or atomic event unresolved')
@@ -278,7 +279,10 @@
     def register(self, record):
         shape(record, OneShot)
         require(record.source_id == 'feat:soul_cage:agony', 'One-shot source adapter still required')
-        require(record.expires is not None, 'Agony has an absolute original deadline')
+        require(record.expires is not None and record.rest_epoch is None, 'Agony has only its absolute original deadline')
+        require(type(record.available) is bool, 'One-shot availability must be boolean')
+        for value in (record.effect_id, record.owner, record.target):
+            ident(value)
         require(record.effect_id not in self.records, 'Canonical effect already registered')
         self.records[record.effect_id] = data(record)
 
@@ -519,6 +523,17 @@
     def playable_plan(self, oracle):
         raise SpellRuleError('Full Time Loop unavailable: seven source integrations and independent review remain')
 
+    def regular_start(self, actor, now):
+        """The public boundary obtains the actor's canonical wallet itself.
+
+        No wallet argument is accepted. The underscore scheduler mutator is an
+        internal implementation detail, not another public event-entry API.
+        """
+        require(actor in self.wallets, 'No canonical wallet for the actor')
+        require(len({id(v) for v in self.wallets.values()}) == len(self.wallets),
+                'Distinct actors cannot alias the same canonical wallet')
+        return self.scheduler._regular_start(actor, self.wallets[actor], now)
+
     def _validate_holders(self):
         shape(self.scheduler, Scheduler)
         for holder, cls in ((self.souls, SoulIdentity), (self.inventory, Inventory),
@@ -528,6 +543,9 @@
         require(not self.integrations, 'Unsupported active integrations: ' + ', '.join(self.integrations))
         require(set(self.wallets) == set(self.lives) == set(self.maxima),
                 'Canonical scene registries must name the same actors, including outsiders')
+        for registry in (self.wallets, self.lives, self.maxima):
+            require(len({id(v) for v in registry.values()}) == len(registry),
+                    'Distinct actors cannot alias one canonical holder')
         for actor in self.lives:
             ident(actor)
             shape(self.lives[actor], LifeState)
@@ -545,6 +563,7 @@
         require(set(vars(self.healing)) == {'iteration', 'records', 'consumption_history',
                     'committed_event_ids', 'consumed_reducer_ids'}, 'Unclassified healing ledger state')
         require(self.healing.iteration == self.scheduler.iteration, 'Healing/scheduler iteration mismatch')
+        self._validate_one_shots()
         require(self.geometry.movement_model == 'finite-level-ground', 'Geometry source adapter required')
         for name, minimum in (('iteration', 0), ('round', 1), ('cursor', 0), ('global_regular', 0), ('turn_ordinal', 0)):
             integer(getattr(self.scheduler, name), 'scheduler '+name, minimum)
@@ -593,6 +612,48 @@
         for context in self.maxima.values():
             for record in context.records:
                 self._maximum_policy(record)
+        for key, effect in self.external.effects.items():
+            shape(effect, ExternalEffect)
+            require(key == effect.identity, 'External effect dictionary/application identity mismatch')
+            if effect.kind == 'maximum-hp':
+                shape(effect.record, MaxHpRecord)
+                require((key, effect.owner, effect.target) ==
+                        (effect.record.application_id, effect.record.owner, effect.record.target),
+                        'External maximum record identity mismatch')
+
+    def _validate_one_shots(self):
+        ledger = self.healing
+        require(type(ledger.records) is dict, 'Canonical one-shot registry must be a dictionary')
+        for key, record in ledger.records.items():
+            shape(record, OneShot)
+            require(key == record.effect_id, 'One-shot dictionary/effect identity mismatch')
+            require(record.source_id == 'feat:soul_cage:agony', 'Unsupported live one-shot source')
+            require(type(record.expires) is ClockMarker and record.rest_epoch is None,
+                    'Agony requires only its original absolute deadline')
+            require(record.owner in self.lives and record.target in self.lives,
+                    'One-shot owner and target require canonical scene identities')
+            ident(record.effect_id)
+            require(type(record.available) is bool, 'One-shot availability must be boolean')
+            require(not record.available or (record.effect_id, ledger.iteration) not in ledger.consumed_reducer_ids,
+                    'One-shot is both available and consumed in this iteration')
+        require(all(type(x) is set for x in (ledger.committed_event_ids, ledger.consumed_reducer_ids,
+                                             ledger.consumption_history)), 'Canonical consumption histories must be sets')
+        for event_id in ledger.committed_event_ids:
+            ident(event_id)
+        for token in ledger.consumed_reducer_ids:
+            require(type(token) is tuple and len(token) == 2, 'Malformed temporal consumption token')
+            ident(token[0]); integer(token[1], 'consumption iteration', 0, ledger.iteration)
+        observed = set()
+        for entry in ledger.consumption_history:
+            require(type(entry) is tuple and len(entry) == 3, 'Malformed consumption audit entry')
+            effect_id, generation, event_id = entry
+            ident(effect_id); ident(event_id); integer(generation, 'consumption iteration', 0, ledger.iteration)
+            token = effect_id, generation
+            require(token in ledger.consumed_reducer_ids and event_id in ledger.committed_event_ids,
+                    'Consumption history is missing its committed event/token')
+            require(token not in observed, 'One temporal permission has multiple consumption events')
+            observed.add(token)
+        require(observed == ledger.consumed_reducer_ids, 'Consumption token is missing historical evidence')
 
     @staticmethod
     def _maximum_policy(record):
@@ -828,6 +889,7 @@
             if dep.effect_id not in snapshot_dependencies:
                 effect = self.external.effects.get(dep.effect_id)
                 require(effect is not None and effect.kind == 'maximum-hp'
+                        and effect.identity == dep.effect_id
                         and (effect.owner, effect.target) == (dep.caster, dep.target),
                         'New external dependency lacks a supported overlay')
         for effect in self.external.effects.values():

```


## tools/validate_temporal_playtests.py

```diff
--- reviewed70/tools/validate_temporal_playtests.py
+++ current76/tools/validate_temporal_playtests.py
@@ -111,7 +111,7 @@
         w = scene()
         event(w)
         w.kernel_plan('a').commit()
-        w.scheduler.regular_start('a', w.wallets['a'], 13)
+        w.regular_start('a', 13)
         self.assertTrue(w.wallets['a'].reaction)
         self.assertNotIn('a', w.scheduler.debts)
         event(w, 'attack-2', 13)
@@ -124,7 +124,7 @@
         w = scene()
         event(w)
         w.kernel_plan('a').commit()
-        w.scheduler.regular_start('a', w.wallets['a'], 13)
+        w.regular_start('a', 13)
         event(w, 'attack-2', 13)
         self.blocked(w, 'already spent')
 
@@ -539,7 +539,7 @@
     def test_one_canonical_rest_epoch_controls_loop_use(self):
         w = scene(); event(w); w.kernel_plan('a').commit()
         w.buffers.completed_long_rest('a', 1)
-        w.scheduler.regular_start('a', w.wallets['a'], 13)
+        w.regular_start('a', 13)
         event(w, 'event-after-real-rest', 13)
         w.kernel_plan('a').commit()
         self.assertEqual(w.scheduler.loop_uses, {('a', 0), ('a', 1)})
@@ -586,28 +586,28 @@
         event(w, 'second', 13); w.kernel_plan('b').commit()
         before = history(w)
         with self.assertRaisesRegex(SpellRuleError, 'initiative cursor'):
-            w.scheduler.regular_start('b', w.wallets['b'], 13)
+            w.regular_start('b', 13)
         self.assertEqual(history(w), before)
         self.assertEqual(w.scheduler.debts, {'a', 'b'})
 
     def test_repeated_regular_start_cannot_create_marker_or_refresh(self):
         w = scene()
-        first = w.scheduler.regular_start('a', w.wallets['a'], 0)
+        first = w.regular_start('a', 0)
         before = history(w)
         with self.assertRaisesRegex(SpellRuleError, 'already active'):
-            w.scheduler.regular_start('a', w.wallets['a'], 0)
+            w.regular_start('a', 0)
         self.assertEqual(history(w), before)
         w.scheduler.regular_end(first, 1)
         self.assertEqual(w.scheduler.cursor, 1)
-        second = w.scheduler.regular_start('b', w.wallets['b'], 1)
+        second = w.regular_start('b', 1)
         w.scheduler.regular_end(second, 2)
-        third = w.scheduler.regular_start('foe', w.wallets['foe'], 2)
+        third = w.regular_start('foe', 2)
         w.scheduler.regular_end(third, 3)
         self.assertEqual((w.scheduler.round, w.scheduler.cursor, w.scheduler.global_regular), (2, 0, 3))
 
     def test_foreign_or_replayed_regular_end_is_rejected(self):
         w = scene()
-        turn = w.scheduler.regular_start('a', w.wallets['a'], 0)
+        turn = w.regular_start('a', 0)
         with self.assertRaisesRegex(SpellRuleError, 'actual active'):
             w.scheduler.regular_end(replace(turn, actor='b'), 1)
         w.scheduler.regular_end(turn, 1)
@@ -733,6 +733,85 @@
         self.assertTrue(w.lives['b'].dead)
         self.assertEqual(w.souls.binds['bind'].death_instance, 'death-1')
 
+    def test_public_regular_start_cannot_accept_another_actors_wallet(self):
+        w = scene(); event(w); w.kernel_plan('a').commit()
+        event(w, 'second', 13); w.kernel_plan('b').commit()
+        before = history(w)
+        with self.assertRaises(TypeError):
+            w.regular_start('a', 13, wallet=w.wallets['b'])
+        self.assertEqual(history(w), before)
+        self.assertFalse(hasattr(w.scheduler, 'regular_start'), 'Unsafe public entry point must not remain')
+        turn = w.regular_start('a', 13)
+        self.assertTrue(w.wallets['a'].reaction)
+        self.assertFalse(w.wallets['b'].reaction)
+        self.assertEqual(w.scheduler.debts, {'b'})
+        w.scheduler.regular_end(turn, 14)
+        w.regular_start('b', 14)
+        self.assertTrue(w.wallets['b'].reaction)
+
+    def test_distinct_actors_cannot_alias_one_wallet(self):
+        w = scene(); w.wallets['a'] = w.wallets['b']; before = history(w)
+        with self.assertRaisesRegex(SpellRuleError, 'alias the same canonical wallet'):
+            w.regular_start('a', 0)
+        self.assertEqual(history(w), before)
+
+    def test_live_one_shot_registry_is_validated_without_register(self):
+        changes = {
+            'source': {'source_id':'future:unreviewed-source'},
+            'key': {'effect_id':'different'},
+            'expiry': {'expires':None},
+            'rest': {'rest_epoch':0},
+            'owner': {'owner':'unknown'},
+            'target': {'target':'unknown'},
+            'availability': {'available':'yes'},
+        }
+        for stage in ('capture', 'preflight'):
+            for name, change in changes.items():
+                with self.subTest(stage=stage, malformed=name):
+                    w = scene(capture=stage == 'preflight')
+                    row = OneShot('x', 'feat:soul_cage:agony', 'a', 'b', True, ClockMarker(60))
+                    w.healing.records['x'] = replace(row, **change)
+                    if stage == 'preflight':
+                        event(w); self.blocked(w, 'one-shot|One-shot|Agony')
+                    else:
+                        before = history(w)
+                        with self.assertRaises(SpellRuleError):
+                            w.capture(('a', 'b', 'foe'))
+                        self.assertEqual(history(w), before)
+                        self.assertIsNone(w._snapshot)
+
+    def test_live_one_shot_availability_cannot_conflict_with_history(self):
+        w = scene(capture=False)
+        w.healing.register(OneShot('x', 'feat:soul_cage:agony', 'a', 'b', True, ClockMarker(60)))
+        w.healing.commit('heal-1', {'nextHealingCandidates':['x']})
+        w.healing.records['x'] = replace(w.healing.records['x'], available=True)
+        with self.assertRaisesRegex(SpellRuleError, 'both available and consumed'):
+            w.capture(('a', 'b', 'foe'))
+
+    def test_consumption_token_requires_matching_historical_event(self):
+        w = scene(); w.healing.consumed_reducer_ids.add(('old', 0)); event(w)
+        self.blocked(w, 'missing historical evidence')
+        w = scene(); w.healing.consumption_history.add(('old', 0, 'absent-event')); event(w)
+        self.blocked(w, 'missing its committed event')
+
+    def test_external_effect_key_and_dependency_identity_cannot_differ(self):
+        for stage in ('capture', 'preflight'):
+            for with_dependency in (False, True):
+                w = scene(capture=stage == 'preflight', outsider=True)
+                record = MaxHpRecord('effect-B', 'monk.hero.iron-fist-master.ribcrusher-strike',
+                                      'outside', 'b', 7, ends_on_completed_rest=True)
+                w.external.effects['dep-A'] = ExternalEffect('effect-B', 'outside', 'b', 'maximum-hp', record)
+                if with_dependency:
+                    w.external.concentration['outside'] = 'cast'
+                    w.external.dependencies = (ExternalDependency('dep-A', 'b', 'outside', 'cast'),)
+                if stage == 'preflight':
+                    event(w); self.blocked(w, 'dictionary/application identity mismatch')
+                else:
+                    before = history(w)
+                    with self.assertRaisesRegex(SpellRuleError, 'dictionary/application identity mismatch'):
+                        w.capture(('a', 'b', 'foe'))
+                    self.assertEqual(history(w), before)
+
 
 def main():
     suite = unittest.defaultTestLoader.loadTestsFromTestCase(TemporalTests)

```


## docs/mechanics/TEMPORAL_KERNEL_PLAYTEST.md

```diff
--- reviewed70/docs/mechanics/TEMPORAL_KERNEL_PLAYTEST.md
+++ current76/docs/mechanics/TEMPORAL_KERNEL_PLAYTEST.md
@@ -10,7 +10,7 @@
 
 The restore is permitted only after a complete atomic combat event, before round four, with an available Reaction and an unspent actual long-rest use. It never interrupts a damage, healing or command transaction. Preflight checks all registered state, source policies, physical dependencies and placements before charging anything. A prepared plan becomes stale if the registered world changes before commit. The single-thread reference requires the host scene lock through preflight and commit. Each committed restore also retains an engine/Director audit frame with the previous and resulting field values; that audit is never a source of character memory. The existing canonical BufferLedger completed-rest epoch also governs Time Loop's own long-rest use; there is no independent rest counter to diverge.
 
-At commit, encounter initiative and the snapshot's Action/Bonus Action/Reaction allowances, RC and declared per-encounter uses return. Every outstanding Oracle Time Loop Reaction debt overlays the restored budgets. Only the owner's actual normal regular-start refresh clears that owner's debt. The bounded scheduler enforces the next actor at the initiative cursor, allows one active regular turn, and advances the cursor/round only when that exact turn ends. An out-of-order or repeated start cannot refresh a Reaction or advance the actual regular marker. Genuine extra turns require the later source adapter and cannot be represented as regular starts. The new iteration has fresh round/turn identities; the rewind itself creates no turn start, pulse or recharge tick. Elapsed world time, real regular-marker count, RP and finite-use history remain unchanged.
+At commit, encounter initiative and the snapshot's Action/Bonus Action/Reaction allowances, RC and declared per-encounter uses return. Every outstanding Oracle Time Loop Reaction debt overlays the restored budgets. Only the owner's actual normal regular-start refresh clears that owner's debt. The public `TemporalKernel.regular_start(actor, now)` obtains the actor's canonical Wallet internally; it accepts no Wallet argument and rejects actor aliases sharing one Wallet. The bounded scheduler enforces the next actor at the initiative cursor, allows one active regular turn, and advances the cursor/round only when that exact turn ends. An out-of-order or repeated start cannot refresh a Reaction or advance the actual regular marker. Genuine extra turns require the later source adapter and cannot be represented as regular starts. The new iteration has fresh round/turn identities; the rewind itself creates no turn start, pulse or recharge tick. Elapsed world time, real regular-marker count, RP and finite-use history remain unchanged.
 
 ## Conservation checks
 
@@ -34,10 +34,10 @@
 
 `TemporalKernel.support_report()` reports that limit. `playable_plan()` always rejects until the full implementation and independent review exist. `kernel_plan()` is a development fixture interface, not a replacement for the complete Oracle feature. The host must disclose every active integration. A supplied unsupported holder rejects preflight; an empty registration is not a certificate that a real game scene is complete.
 
-`TemporalHealingCommitLedger` can be passed as the one canonical healing ledger to existing helpers. Its canonical return IDs preserve `FeatWorld.commit_healing` removal semantics, while its historical consumption tokens are iteration-qualified. Agony creation/refresh/removal still needs the full feat adapter to synchronize active records; this kernel does not claim that synchronization exists.
+`TemporalHealingCommitLedger` can be passed as the one canonical healing ledger to existing helpers. Its canonical return IDs preserve `FeatWorld.commit_healing` removal semantics, while its historical consumption tokens are iteration-qualified. Capture/preflight validate the live registry independently of `register()`: exact source/identity/absolute clock, canonical owner/target, boolean availability, and matching consumption-token/event history. External effect dictionary keys, effect identities, dependency identities and max-HP record identities must also agree. Agony creation/refresh/removal still needs the full feat adapter to synchronize active records; this kernel does not claim that synchronization exists.
 
 ## Validation and next review
 
-Run `tools/validate_temporal_playtests.py`. The current suite contains 70 adversarial test methods. [Validation report](TEMPORAL_KERNEL_VALIDATION.json) records the tested helper hash. The initial 46-test packet, later 52-test packet, and [six independent findings](../../../../docs/audit/2026-10-08/full-game/GPT_TEMPORAL_KERNEL_FINDINGS.md) are preserved separately. Targeted repairs now cover each finding, with the completed independent repair disposition still pending. Two invented maximum-HP source examples in the review already fail the existing source constructor; the repair additionally rejects actual valid sources lacking a temporal policy and replaces prefix inference with exact IDs.
+Run `tools/validate_temporal_playtests.py`. The current suite contains 76 adversarial test methods. [Validation report](TEMPORAL_KERNEL_VALIDATION.json) records the tested helper hash. The initial 46-test packet, later 52-test packet, and [six independent findings](../../../../docs/audit/2026-10-08/full-game/GPT_TEMPORAL_KERNEL_FINDINGS.md) are preserved separately. The notebook [confirmed the original six repairs](../../../../docs/audit/2026-10-08/full-game/GPT_TEMPORAL_KERNEL_REPAIR_REVIEW.md), then identified three narrow identity/admission gaps. Those now have targeted repairs and six additional test methods; their independent confirmation is still pending. Two invented maximum-HP source examples in the first review already fail the existing source constructor; the exact temporal table additionally rejects actual valid sources lacking a temporal policy.
 
 Next, independently review this actual code and its narrow claims, repair defects, then add the seven missing integrations and exact source policies. Do not remove the Time Loop deferred status based on these tests. The final joint whole-game flow review and authorized GitHub push remain later gates.

```


## docs/mechanics/TEMPORAL_KERNEL_VALIDATION.json

```diff
--- reviewed70/docs/mechanics/TEMPORAL_KERNEL_VALIDATION.json
+++ current76/docs/mechanics/TEMPORAL_KERNEL_VALIDATION.json
@@ -1,9 +1,9 @@
 {
   "status": "PASS",
   "scope": "Unpromoted foundational temporal kernel only; seven integrations and actual notebook review remain",
-  "testMethods": 70,
+  "testMethods": 76,
   "failures": 0,
   "errors": 0,
   "fullTimeLoopOperational": false,
-  "helperSha256": "c6ff9b64d51e867cef358729fa1f2df8fb34698e913c234bde43e5afe1db5386"
+  "helperSha256": "b821829ed352e69ce1ecf3c3d753f0206c8f8d2ec5a5d64bc89d5fd7d8a72151"
 }

```
