# Final concentration identity repair — 50 integration methods pass

Your completed 49-method review is preserved as GPT_TEMPORAL_CONTROL_ADMISSION_REVIEW.md. It confirms the two admission repairs, four malformed-collection cases and Bloom lost-installment reconciliation. I repaired its one remaining same-ID/different-callback blocker. Here is the exact diff from that 49-method revision, reconstructed from the prior submitted full code plus patch and verified against its exact hashes.

Each active concentration-dependent snapshot record now carries owner, concentration ID, actual slot-identity token and callback-identity token. Preflight requires the same actual slot and callback. Source registration retains strong references to actual concentration slots, so those object-identity tokens cannot be recycled after detachment. Pins are classified, validated and watched; their callbacks are never copied into a second world or invoked at restore. Register the actual concentration parent before registering its dependent component.

The added regression tests three variants before preflight: same textual ID with a different callback; same callback repackaged as a new slot; and a replacement callback subsequently pinned by another newly registered component. All reject without state/resource mutation. The last case proves a newly recognized slot cannot substitute for the immutable snapshot's binding. The existing post-preflight replacement test and later real concentration-end callback test still pass.

50 integration methods pass. Foundation remains hash45ad6ab7d2b26baf7bc56a8377d82398781175d5a81c7562b3dedeb40f28d577 and approved output bridge remains hash835a108a80e5ad8c5d030dbf7d927e0491bc944eb2697d71f2504fd2e0b1df12; their 76+22 checks remain unchanged/passing. Please confirm the admitted transaction checkpoint or give a concrete remaining defect. All broader parent/source integrations, complete nine-family coverage, actual final HP/Ki/Conviction mutation, full Time Loop and the final whole-game flow/GitHub delivery remain unfinished. No original source or catalog count changed.


## tools/temporal_control_world.py

```diff
--- 49-method/tools/temporal_control_world.py
+++ 50-method/tools/temporal_control_world.py
@@ -152,6 +152,9 @@
         self.scheduler=scheduler
         self.outputs=outputs
         self.concentration=concentration if concentration is not None else ConcentrationLedger()
+        # Retain actual slot/callback references so snapshot identity tokens
+        # cannot be recycled after a slot is detached or replaced.
+        self.concentration_pins={}
         self.recipients=TemporalRecipientLedger(scheduler)
         self.records={}
         self.canonical={}
@@ -165,6 +168,11 @@
         require(record.identity not in self.records,'Canonical control identity already registered')
         require(record.family in HOLDER_TYPES,'Unsupported temporal control family')
         require(type(record.holder) is HOLDER_TYPES[record.family],'Control holder type mismatch')
+        if record.concentration_id is not None:
+            slot=self.concentration.current.get(record.owner)
+            require(type(slot) is tuple and len(slot)==2 and slot[0]==record.concentration_id
+                    and callable(slot[1]),'Register actual concentration before its component')
+            self.concentration_pins[id(slot)]=slot
         if record.family=='pulse' and record.holder.profile_name in INDEPENDENT_OUTPUTS:
             if record.identity in self.outputs.series:
                 h,owner,_=self.outputs._binding(record.identity)
@@ -288,12 +296,14 @@
             current=self.concentration.current.get(record.owner)
             require(current is not None and current[0]==record.concentration_id,
                     'Exact current concentration parent missing; restoration adapter required')
+            require(self.concentration_pins.get(id(current)) is current,
+                    'Current concentration binding identity was replaced')
         if record.parent_id is not None:
             require(record.parent_id!=record.identity and record.parent_id in self.records,'Missing/cyclic parent')
 
     def validate(self,kernel):
         require(set(vars(self))=={'scheduler','concentration','recipients','records','canonical',
-                'active','events','native_evaluations','outputs'},'Unclassified control world state')
+                'active','events','native_evaluations','outputs','concentration_pins'},'Unclassified control world state')
         require(self.scheduler is kernel.scheduler,'Control scheduler alias differs')
         for name,kind in (('records',dict),('canonical',dict),('active',set),('events',dict),('native_evaluations',dict)):
             require(type(getattr(self,name)) is kind,'Malformed control world collection: '+name)
@@ -312,6 +322,10 @@
         require(type(self.concentration) is ConcentrationLedger and set(vars(self.concentration))=={'current'},
                 'Canonical concentration ledger required')
         require(type(self.concentration.current) is dict,'Malformed concentration registry')
+        require(type(self.concentration_pins) is dict,'Malformed concentration identity pins')
+        for token,slot in self.concentration_pins.items():
+            require(token==id(slot) and type(slot) is tuple and len(slot)==2 and callable(slot[1]),
+                    'Malformed retained concentration identity')
         for owner,slot in self.concentration.current.items():
             ident(owner)
             require(type(slot) is tuple and len(slot)==2 and callable(slot[1]),'Malformed concentration slot')
@@ -352,7 +366,10 @@
                 require(projected.ended_at is None,'Pulse already ended or missed upkeep before snapshot')
         return {'records':{key:{'metadata':{k:data(v) for k,v in vars(r).items() if k!='holder'},
                                'fields':payload(r.holder)} for key,r in self.records.items()},
-                'active':data(self.active),'recipientClaims':data(self.recipients.claimed)}
+                'active':data(self.active),'recipientClaims':data(self.recipients.claimed),
+                'concentrationBindings':{key:(r.owner,r.concentration_id,
+                    id(self.concentration.current[r.owner]),id(self.concentration.current[r.owner][1]))
+                    for key,r in self.records.items() if key in self.active and r.concentration_id is not None}}
 
     def watch(self,tx):
         tx.labels[id(self)]='control-world'
@@ -363,6 +380,7 @@
         for name in ('active','events','native_evaluations'):tx.watch(self,name)
         tx.watch_shape(self.concentration)
         tx.watch_binding(self.concentration,'current');tx.watch_registry(self.concentration.current)
+        tx.watch_binding(self,'concentration_pins');tx.watch_registry(self.concentration_pins)
         tx.labels[id(self.outputs)]='control-independent-outputs'
         tx.watch_shape(self.outputs);tx.watch_binding(self.outputs,'kernel')
         tx.watch_binding(self.outputs,'series');tx.watch_registry(self.outputs.series)
@@ -384,6 +402,11 @@
         self.validate(kernel)
         now=kernel.scheduler.now
         require(set(saved['records'])<=self.records.keys(),'Snapshot effect object disappeared')
+        for key,(owner,concentration_id,slot_token,callback_token) in saved['concentrationBindings'].items():
+            current=self.concentration.current.get(owner)
+            require(current is not None and current[0]==concentration_id and id(current)==slot_token
+                    and id(current[1])==callback_token and self.concentration_pins.get(slot_token) is current,
+                    'Snapshot concentration binding identity changed; parent adapter required')
         desired=set(self.active)
         missed_outputs=set()
         def restored_active(key):

```

## tools/validate_temporal_control_world.py

```diff
--- 49-method/tools/validate_temporal_control_world.py
+++ 50-method/tools/validate_temporal_control_world.py
@@ -399,6 +399,21 @@
         with self.assertRaises(SpellRuleError):plan.commit()
         self.assertEqual(whole_state(w,c),before)
 
+    def test_same_id_concentration_rebound_before_preflight_rejects(self):
+        for replacement in ('different-callback','same-callback-new-slot','new-registered-component'):
+            with self.subTest(replacement=replacement):
+                w,c=world();pulse(c,'transcendent-meditation');capture(w)
+                original=c.concentration.current['a']
+                callback=original[1] if replacement=='same-callback-new-slot' else lambda reason:None
+                c.concentration.current['a']=tuple(['pulse',callback])
+                if replacement=='new-registered-component':
+                    attach(c,'rider',OneShotRider('hit'),'dragoon.hero.drake-rider.drake-mark','dragoon.drake-mark',
+                           identity='other',origin='encounter',concentration='pulse')
+                event(w,now=2);before=whole_state(w,c)
+                with self.assertRaisesRegex(SpellRuleError,'binding identity'):w.kernel_plan('a')
+                self.assertEqual(whole_state(w,c),before)
+                self.assertIs(c.concentration_pins[id(original)],original)
+
     def test_snapshot_fixed_roster_cannot_change(self):
         w,c=world();r=pulse(c,'eternal-bloom');capture(w);r.holder.roster=('a',);event(w,now=2)
         with self.assertRaisesRegex(SpellRuleError,'roster'):w.kernel_plan('a')

```

## Current validation

```json
{
  "status": "PASS",
  "methods": 50,
  "failures": 0,
  "errors": 0,
  "fullTimeLoopOperational": false,
  "scope": "Live control/pulse transaction candidate; exact admitted source policies; parent/entry/mutation adapters remain",
  "hashes": {
    "tools/temporal_playtest_rules.py": "45ad6ab7d2b26baf7bc56a8377d82398781175d5a81c7562b3dedeb40f28d577",
    "tools/temporal_control_world.py": "aeec3e2124190ba2307c5c887cb383b724eef332d339842625772998a377d090"
  }
}

```

## Exact current hashes

```json
{
  "status": "50-method callback-binding repair pending independent confirmation",
  "methods": 50,
  "fullTimeLoopOperational": false,
  "remainingMajorIntegrations": 7,
  "hashes": {
    "tools/temporal_control_world.py": "aeec3e2124190ba2307c5c887cb383b724eef332d339842625772998a377d090",
    "tools/validate_temporal_control_world.py": "c7f6458bdea7dac7861fefb283a09c476353055661a496760fc3df6777db3991",
    "tools/temporal_playtest_rules.py": "45ad6ab7d2b26baf7bc56a8377d82398781175d5a81c7562b3dedeb40f28d577",
    "tools/temporal_control_playtest_rules.py": "835a108a80e5ad8c5d030dbf7d927e0491bc944eb2697d71f2504fd2e0b1df12"
  }
}
```
