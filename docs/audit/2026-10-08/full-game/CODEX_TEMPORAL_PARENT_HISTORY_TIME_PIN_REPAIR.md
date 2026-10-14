# Parent history: canonical query time and retained-reference repair

Your actual 55-method review is preserved verbatim in GPT_TEMPORAL_PARENT_HISTORY_REPAIR_REVIEW.md. The original four findings are independently confirmed repaired; these are the two remaining implementation corrections. No new source rule is introduced.

The suite now has 59 passing methods. valid_form_deadline() defaults to the actual scheduler time in initiative, rejects a supplied time different from that clock, and always rejects times earlier than the last observed event. Outside initiative an explicit actual-world marker is still required; it is bounded by observed history until the broader calendar adapter exists.

Both reference-pin tables now have retained-reference manifests checked before every validation and before extending pins. Key deletion, entry replacement and lost historical concentration tuples reject. Existing manifest entries cannot be overwritten through _pin_objects(); retained tuple and callback references remain even after ordinary concentration ending. Failed native operations no longer extend pins. This uses the same accidental-corruption/shadow-evidence model as the existing audit copies; it is not a security sandbox against a caller deliberately rewriting every private validator root.

Four new methods cover expired/backdated initiative queries, no-argument current-time queries plus the outside-history lower bound, form-pin deletion with equal-field replacement, and deletion of ended concentration pins. All preceding native-operation, authority, finite-economy and transition checks still pass.

Below is the exact diff from your immutable 55-method submission plus current hashes/report. Please confirm this bounded source-history checkpoint if no reproducible issue remains. Parent restoration, full class casting hooks, replay-safe wrappers, all seven broader integrations, full Time Loop and the final whole-game/GitHub gate remain open.

## tools/temporal_parent_history.py
Current SHA-256 `74dca59616b9d6783ce870d6975983847075b28fc4722cc41074e70b9a999e87`

```diff
--- submitted-55/tools/temporal_parent_history.py
+++ repair-59/tools/temporal_parent_history.py
@@ -124,7 +124,8 @@
         self.last_time=ClockMarker(0);self.chain='parent-history-v1'
         self._events=();self._receipts=();self._failures=();self._chain=self.chain
         self._mode=self.mode;self._last_time=self.last_time;self._scheduler_binding=None
-        self._pins={};self._slot_pins={};self._initial=self._state()
+        self._pins={};self._slot_pins={};self._pin_manifest={};self._slot_manifest={}
+        self._initial=self._state()
         self._expected=leaf(self._initial)
         self._expected_finite=self._finite_state()
         self._bind_world()
@@ -144,21 +145,34 @@
                               for a,d in w.druids.items()}
 
     def _pin_objects(self):
+        self._validate_pin_manifests()
         w=self.world
         for domain,registry in (('body',w.bodies),('cast',w.casts),('link',w.links)):
             for key,obj in registry.items():
                 k=(domain,key)
                 require(k not in self._pins or self._pins[k] is obj,'Canonical parent identity replaced')
                 self._pins[k]=obj
+                self._pin_manifest.setdefault(k,obj)
         for owner,d in w.druids.items():
             for key,obj in d.instances.items():
                 k=('form',owner,key)
                 require(k not in self._pins or self._pins[k] is obj,'Canonical form identity replaced')
                 self._pins[k]=obj
+                self._pin_manifest.setdefault(k,obj)
         for owner,slot in w.concentration.current.items():
             require(type(slot) is tuple and len(slot)==2 and type(slot[0]) is str and callable(slot[1]),
                     'Malformed actual concentration slot')
             self._slot_pins[id(slot)]=slot
+            self._slot_manifest.setdefault(id(slot),(slot,slot[1]))
+
+    def _validate_pin_manifests(self):
+        require(set(self._pins)==set(self._pin_manifest) and
+                all(self._pins[k] is v for k,v in self._pin_manifest.items()),
+                'Canonical parent pin manifest changed')
+        require(set(self._slot_pins)==set(self._slot_manifest) and
+                all(self._slot_pins[k] is slot and slot[1] is callback
+                    for k,(slot,callback) in self._slot_manifest.items()),
+                'Historical concentration pin manifest changed')
 
     def _state(self):
         w=self.world;exact(w,TransformationWorld);exact(w.concentration,ConcentrationLedger)
@@ -251,6 +265,7 @@
                 and self.chain==self._chain,'Parent historical record was replaced or edited')
         require(self.used=={e['eventId'] for e in self.events},'Parent event history mismatch')
         require(not self.failures,'Failed mutating source operation needs host reconciliation')
+        self._validate_pin_manifests()
         current=self._state()
         require(current==self._expected,'Unobserved parent lifecycle mutation; no historical receipt')
         require(self._finite_state()==self._expected_finite,
@@ -384,7 +399,8 @@
         # Detached copies detect accidental mutation of public audit projections.
         self._events=leaf(self.events);self._receipts=leaf(self.receipts)
         self._failures=leaf(self.failures);self._chain=self.chain
-        self._expected=leaf(after);self.last_time=frame['marker'];self._last_time=self.last_time;self._pin_objects()
+        self._expected=leaf(after);self.last_time=frame['marker'];self._last_time=self.last_time
+        if not failed:self._pin_objects()
         self._expected_finite=self._finite_state()
         if integrity_error is not None:raise integrity_error
 
@@ -620,9 +636,20 @@
         return tuple(leaf(r) for r in self.receipts if r['kind']==kind and
                      identity in (r.get('formId'),r.get('castId'),r.get('linkId')))
 
-    def valid_form_deadline(self,owner,form_id,now):
+    def _query_time(self,now):
+        if self.mode=='initiative':
+            marker=self.scheduler.now if now is None else clock_marker(now)
+            require(marker==self.scheduler.now,'Evidence query must use current canonical scheduler time')
+        else:
+            require(now is not None,'Outside evidence query needs the actual world time')
+            marker=clock_marker(now)
+        require(marker>=self.last_time,'Evidence query cannot predate observed history')
+        return marker
+
+    def valid_form_deadline(self,owner,form_id,now=None):
         """Evidence for later planning, not permission to reactivate anatomy."""
-        self.validate();d=self.world.druids[owner];f=d.instances[form_id]
+        self.validate();current_time=self._query_time(now)
+        d=self.world.druids[owner];f=d.instances[form_id]
         created=self.records('form-created',form_id)
         require(len(created)==1 and created[0]['owner']==owner,'Missing unique actual form creation')
         endpoint=created[0]['initial']['expiry']
@@ -631,7 +658,7 @@
             endpoint=row['newExpiry']
         require(endpoint==leaf(f.expiry),'Current form endpoint lacks an actual renewal receipt')
         marker=ClockMarker(**endpoint)
-        require(clock_marker(now)<marker,'Original/renewed form endpoint is no longer valid')
+        require(current_time<marker,'Original/renewed form endpoint is no longer valid')
         return marker
 
     def permanent_link(self,link_id):

```

## tools/validate_temporal_parent_history.py
Current SHA-256 `baad6092a94ce4bc7a482b16d450b4fa7645003d5dbe4cdf731feb5466874c8c`

```diff
--- submitted-55/tools/validate_temporal_parent_history.py
+++ repair-59/tools/validate_temporal_parent_history.py
@@ -421,6 +421,34 @@
         self.assertEqual(w.links['C:b'].state,'replaced');self.assertEqual(w.links['D:b'].state,'shaping')
         self.assertNotIn('a',w.concentration.current);j.validate()
 
+    def test_expired_form_query_cannot_backdate_canonical_initiative(self):
+        w,ds,d,j=fixture();shift(j,ds)
+        j.scheduler=Scheduler('enc',('a','b','c'),now=ClockMarker(601));j.enter_initiative()
+        with self.assertRaisesRegex(SpellRuleError,'canonical scheduler time'):j.valid_form_deadline('a','F',599)
+        with self.assertRaisesRegex(SpellRuleError,'no longer valid'):j.valid_form_deadline('a','F')
+        with self.assertRaisesRegex(SpellRuleError,'no longer valid'):j.valid_form_deadline('a','F',601)
+
+    def test_query_uses_current_scheduler_and_outside_history_lower_bound(self):
+        w,ds,d,j=fixture();shift(j,ds,now=10)
+        with self.assertRaisesRegex(SpellRuleError,'predate observed history'):j.valid_form_deadline('a','F',9)
+        with self.assertRaisesRegex(SpellRuleError,'actual world time'):j.valid_form_deadline('a','F')
+        j.scheduler=Scheduler('enc',('a','b','c'),now=ClockMarker(11));j.enter_initiative()
+        self.assertEqual(j.valid_form_deadline('a','F'),ClockMarker(610))
+
+    def test_removed_form_pin_cannot_hide_equal_object_replacement(self):
+        w,ds,d,j=fixture();shift(j,ds);original=d.current
+        del j._pins[('form','a','F')]
+        d.current=deepcopy(original);d.instances['F']=d.current
+        with self.assertRaisesRegex(SpellRuleError,'pin manifest changed'):j.validate()
+        self.assertIs(j._pin_manifest[('form','a','F')],original)
+
+    def test_ended_concentration_pins_must_remain_retained(self):
+        w=world();j=observed(w);cast(j);slot=w.concentration.current['a']
+        j.end_concentration('end','a',1,reason='voluntary-release');j._slot_pins.clear()
+        with self.assertRaisesRegex(SpellRuleError,'pin manifest changed'):j.validate()
+        self.assertIs(j._slot_manifest[id(slot)][0],slot)
+        self.assertIs(j._slot_manifest[id(slot)][1],slot[1])
+
 
 if __name__=='__main__':
     suite=unittest.defaultTestLoader.loadTestsFromTestCase(ParentHistoryTests)

```

## Exact validation report

```json
{
  "status": "PASS",
  "testMethods": 59,
  "scope": "Actual native-operation source history only; no parent restoration/geometry/commit implementation",
  "helperSha256": "74dca59616b9d6783ce870d6975983847075b28fc4722cc41074e70b9a999e87",
  "parentRuntimeIntegrated": false,
  "fullTimeLoopOperational": false,
  "remainingMajorIntegrations": 7,
  "failures": 0,
  "errors": 0
}

```
