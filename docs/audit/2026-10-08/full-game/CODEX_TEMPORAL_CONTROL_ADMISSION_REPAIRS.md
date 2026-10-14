# Exact follow-up admission repairs — 49 methods pass

Your completed review of the 44-method revision is preserved as GPT_TEMPORAL_CONTROL_WORLD_REPAIR_REVIEW.md. It expressly closes the first five defects and both Oracle concentration omissions, and identifies two remaining admission defects. Both are now repaired. This packet is the exact incremental diff from that full 44-method submission, with new tests and validation; all unchanged code remains as previously supplied.

1. capture_payload now non-mutatively checks every active pulse activation <= snapshot marker, unexpired absolute deadline, and a live clone advanced to the snapshot marker. It rejects future activation, stale missed upkeep and already-expired source state. These do not charge or mutate anything.
2. Pulse component must equal its explicit admitted source profile. Bloom/contact/native require the finite identifiers installments/first-contact/regular-heal. Each family has an unknown-component capture regression.

I also performed four additional concrete malformed-state probes (results attached). Before the new checks, changing a required set/dict to a list could permit partial resource/opportunity mutation followed by AttributeError/IndexError: output guard.consumed, recipient.history, pulse.declarations, or native.consumed. The new world/holder/guard/recipient collection checks reject these before writes; all four have no-mutation regressions. Concentration slot shape/callback, control Boolean fields and pulse mode/declaration/application structure are also checked before use. The original approved helpers remain unchanged; validation belongs to the admitting world adapter.

Finally, tracing the already-agreed original-clock behavior found one missed-installment problem: restore at second7 advances an Eternal Bloom parent past its second opportunity at6, but restoring only its old consumed={0} child view would prevent its still-legal third share at12. The repaired Bloom view consumes every original share whose marker is strictly earlier than now, without healing or recalculating the reserve. consume_bloom uses the same projection before a real current parent receipt. A real restore regression proves consumed={0,1} at7, no HP change, then actual third pulse/share3 at12. Exact due markers are not skipped, so a genuine new iteration at the same still-current marker remains possible. Please check this correction against the existing rule that missed outside-clock installments are lost and later installments remain scheduled.

49 integration methods pass; 76 foundation and 22 payment/output checks remain passing. No foundation/approved-helper changes were made after the prior submission. Please give a bounded code disposition or concrete remaining defect. Full nine-family coverage, actual final HP/Ki/Conviction application, all seven major integrations, whole-game flow and delivery remain open. This is not a publication or balance approval request.


## tools/temporal_control_world.py

```diff
--- 44-method/tools/temporal_control_world.py
+++ 49-method/tools/temporal_control_world.py
@@ -73,6 +73,14 @@
 HOLDER_TYPES = {'speed':SpeedRecord,'guiding':GuidingStarMark,'brand':WrathfulBrand,
     'rider':OneShotRider,'reflection':PerTurnReflection,'pulse':PulseSeries,
     'bloom':BloomReserve,'contact':FirstContactLedger,'native':NativeOccurrenceLedger}
+COMPONENTS={'bloom':'installments','contact':'first-contact','native':'regular-heal'}
+COLLECTION_FIELDS={
+    'guiding':{'_pending':set},'reflection':{'used_turn_ids':set},
+    'pulse':{'states':list,'declarations':dict,'applications':set,'roster':tuple,
+             'future_starts':tuple,'maintenance_ends':tuple,'opens':tuple},
+    'bloom':{'roster_missing':dict,'shares':dict,'consumed':set},
+    'contact':{'profiles':dict,'consumed':set},'native':{'consumed':set},
+}
 IMMUTABLE_FIELDS = {
     'speed':('application_id','owner','target','group','profile','mode','amount','floor','expires','slowed_hook'),
     'guiding':('owner','target','expires','s','_identity'),
@@ -187,6 +195,13 @@
         if record.family=='bloom':expected|={'shares'}
         required|=expected-{f.name for f in fields(type(h))}
         require(required<=set(vars(h))<=expected,'Unclassified control/pulse holder fields')
+        for name,kind in COLLECTION_FIELDS.get(record.family,{}).items():
+            require(type(getattr(h,name)) is kind,'Malformed control holder collection: '+name)
+        for name in ('active','available','suppressed','attack_bonus_available','hit_rider_available',
+                     'owner_rider_available','ally_rider_available','slowed_hook'):
+            if hasattr(h,name):require(type(getattr(h,name)) is bool,'Malformed control Boolean: '+name)
+        if record.family in COMPONENTS:
+            require(record.component==COMPONENTS[record.family],'Exact temporal component policy missing')
         require(not record.dependencies,'Required physical/device/form/source parent adapter missing')
         if record.family in ('speed','guiding','brand','rider','reflection'):
             policy=CONTROL_POLICIES.get((record.source,record.component))
@@ -214,6 +229,7 @@
                 ident(h._identity);integer(h._next_token,'historical attack token',0)
             if record.family=='reflection':require(record.concentration_id is not None,'Divine Judgment concentration required')
         elif record.family=='pulse':
+            require(record.component==h.profile_name,'Exact temporal pulse component policy missing')
             require(h.instance_id==record.identity and PULSE_SOURCES.get(h.profile_name)==record.source,
                     'Pulse source/profile/application mismatch')
             require(h.profile is PROFILES[h.profile_name] and h.ledger is self.recipients,
@@ -222,6 +238,21 @@
             require(h.expires==record.deadline,'Pulse deadline identity mismatch')
             require(len(h.states)==h.profile.count and set(h.states)<=
                     {'pending','funded','committed','lost','closed'},'Malformed pulse opportunity state')
+            require(h.profile.mode=='window' or not {'funded','closed'}&set(h.states),
+                    'Pulse opportunity state belongs to another mode')
+            require(h.ended_at is None or type(h.ended_at) is ClockMarker,'Malformed pulse end marker')
+            require((h.ended_at is None)==(h.ended_reason is None),'Pulse ending fields disagree')
+            if h.ended_reason is not None:ident(h.ended_reason)
+            for index,targets in h.declarations.items():
+                integer(index,'declared pulse index',0,h.profile.count-1)
+                require(type(targets) is tuple and set(targets)<=set(record.targets)
+                        and len(targets)==len(set(targets)) and h.states[index]=='committed',
+                        'Malformed pulse declaration')
+            for application in h.applications:
+                require(type(application) is tuple and len(application)==2 and h.profile.mode=='window',
+                        'Malformed pulse application')
+                integer(application[0],'pulse application index',0,h.profile.count-1)
+                require(application[1] in record.targets,'Unknown pulse application recipient')
             require(set(h.roster)<=set(record.targets),'Pulse fixed roster/target mismatch')
             if h.profile_name=='hemostasis':
                 require(len(record.targets)==1 and h.roster==record.targets,'Hemostasis requires its one actual target')
@@ -264,9 +295,13 @@
         require(set(vars(self))=={'scheduler','concentration','recipients','records','canonical',
                 'active','events','native_evaluations','outputs'},'Unclassified control world state')
         require(self.scheduler is kernel.scheduler,'Control scheduler alias differs')
+        for name,kind in (('records',dict),('canonical',dict),('active',set),('events',dict),('native_evaluations',dict)):
+            require(type(getattr(self,name)) is kind,'Malformed control world collection: '+name)
         require(type(self.outputs) is ConservedPulseOutputs and self.outputs.kernel is kernel
                 and set(vars(self.outputs))=={'kernel','series','consumed','events'},
                 'Canonical independent-output guard/schema required')
+        require(type(self.outputs.series) is dict and type(self.outputs.consumed) is set
+                and type(self.outputs.events) is dict,'Malformed independent-output collections')
         expected_outputs={key for key,r in self.records.items() if r.family=='pulse'
                           and r.holder.profile_name in INDEPENDENT_OUTPUTS}
         require(set(self.outputs.series)==expected_outputs,'Undisclosed independent-output source')
@@ -276,9 +311,19 @@
                     'Independent-output guard and live world must share canonical holders')
         require(type(self.concentration) is ConcentrationLedger and set(vars(self.concentration))=={'current'},
                 'Canonical concentration ledger required')
+        require(type(self.concentration.current) is dict,'Malformed concentration registry')
+        for owner,slot in self.concentration.current.items():
+            ident(owner)
+            require(type(slot) is tuple and len(slot)==2 and callable(slot[1]),'Malformed concentration slot')
+            ident(slot[0])
         require(type(self.recipients) is TemporalRecipientLedger and self.recipients.scheduler is kernel.scheduler,
                 'Canonical temporal recipient ledger required')
         require(set(vars(self.recipients))=={'claimed','scheduler','history'},'Recipient schema changed')
+        require(type(self.recipients.claimed) is set and type(self.recipients.history) is set,
+                'Malformed recipient collections')
+        for claim in self.recipients.claimed:
+            require(type(claim) is tuple and len(claim)==3,'Malformed active recipient claim')
+            ident(claim[0]);ident(claim[1]);integer(claim[2],'recipient round',1)
         require(set(self.records)==set(self.canonical) and self.active<=self.records.keys(),'Control registry incomplete')
         require(len({id(r.holder) for r in self.records.values()})==len(self.records),'Shared control holder needs one canonical record')
         for key,r in self.records.items():
@@ -300,6 +345,11 @@
         for r in self.records.values():
             require(r.family=='native' or r.origin=='outside',
                     'No supplied active control source is created at the immutable initiative boundary')
+            if r.family=='pulse' and r.identity in self.active:
+                require(r.holder.activation<=kernel.scheduler.now,'Pulse did not exist at initiative snapshot')
+                require(r.deadline is None or kernel.scheduler.now<r.deadline,'Pulse expired before snapshot')
+                projected=plain_clone(r.holder,payload(r.holder));projected.advance(kernel.scheduler.now)
+                require(projected.ended_at is None,'Pulse already ended or missed upkeep before snapshot')
         return {'records':{key:{'metadata':{k:data(v) for k,v in vars(r).items() if k!='holder'},
                                'fields':payload(r.holder)} for key,r in self.records.items()},
                 'active':data(self.active),'recipientClaims':data(self.recipients.claimed)}
@@ -374,6 +424,9 @@
                 candidate['_next_token']=max(candidate['_next_token'],r.holder._next_token)
                 candidate['_pending']=set()
             if r.family=='reflection':candidate['used_turn_ids']=data(r.holder.used_turn_ids)
+            if r.family=='bloom':
+                parent=self.records[r.parent_id].holder
+                candidate['consumed']|={i for i,at in enumerate(parent.opens) if at<now}
             if r.family=='pulse':
                 # Outside-origin real clock remains fixed. Purely retire missed
                 # opportunities; advance() performs no healing, payment or pulse.
@@ -477,7 +530,10 @@
                 and receipt.get('at')==kernel.scheduler.now and receipt.get('pulse')==index
                 and set(eligible_targets)<=set(output.get('outputTargets',())),
                 'Bloom installment requires a current unsuppressed parent pulse receipt')
-        result=r.holder.consume(index,eligible_targets=eligible_targets)
+        candidate=plain_clone(r.holder,payload(r.holder))
+        candidate.consumed|={i for i,at in enumerate(parent.opens) if at<kernel.scheduler.now}
+        result=candidate.consume(index,eligible_targets=eligible_targets)
+        r.holder.consumed=candidate.consumed
         self.events[event_id]={'identity':identity,'iteration':kernel.scheduler.iteration,'installment':index,'result':data(result)}
         return result
 
@@ -544,4 +600,3 @@
         result=r.holder.trigger(**source_arguments)
         self.events[event_id]={'identity':identity,'iteration':kernel.scheduler.iteration,'consumed':result}
         return result
-

```

## tools/validate_temporal_control_world.py

```diff
--- 44-method/tools/validate_temporal_control_world.py
+++ 49-method/tools/validate_temporal_control_world.py
@@ -168,6 +168,74 @@
 
 
 class PulseTransactionTests(unittest.TestCase):
+    def test_future_pulse_cannot_acquire_snapshot_membership(self):
+        w,c=world();h=PulseSeries('future','transcendent-meditation',ClockMarker(6),
+            (ClockMarker(12),ClockMarker(18),ClockMarker(24)),c.recipients,roster=('b',))
+        c.concentration.start_committed('a','future',lambda reason:c.active.discard('future'))
+        attach(c,'pulse',h,PULSE_SOURCES['transcendent-meditation'],'transcendent-meditation',identity='future',
+               concentration='future',deadline=h.expires)
+        before=whole_state(w,c)
+        with self.assertRaisesRegex(SpellRuleError,'did not exist'):capture(w)
+        self.assertIsNone(w._snapshot);self.assertEqual(whole_state(w,c),before)
+
+    def test_stale_or_expired_pulse_cannot_be_captured_active(self):
+        for now in (7,19):
+            with self.subTest(now=now):
+                w,c=world();pulse(c,'garden');w.scheduler.now=ClockMarker(now);before=whole_state(w,c)
+                with self.assertRaisesRegex(SpellRuleError,'before snapshot'):capture(w)
+                self.assertIsNone(w._snapshot);self.assertEqual(whole_state(w,c),before)
+
+    def test_all_remaining_families_require_exact_component(self):
+        for family in ('pulse','bloom','contact','native'):
+            with self.subTest(family=family):
+                w,c=world()
+                if family=='pulse':r=pulse(c,'song-of-mending')
+                elif family=='bloom':
+                    pulse(c,'eternal-bloom')
+                    r=attach(c,'bloom',BloomReserve({'b':10}),PULSE_SOURCES['eternal-bloom'],'installments',
+                        identity='reserve',deadline=ClockMarker(18),parent='pulse')
+                elif family=='contact':
+                    pulse(c,'garden')
+                    r=attach(c,'contact',FirstContactLedger({'pulse':'garden'}),PULSE_SOURCES['garden'],
+                        'first-contact',identity='contact',deadline=ClockMarker(18),parent='pulse')
+                else:
+                    r=attach(c,'native',NativeOccurrenceLedger(),'cleric.hero.saint.aura-of-grace',
+                        'regular-heal',identity='native',targets=('a',),deadline=None)
+                r.component='future.unreviewed.component';before=whole_state(w,c)
+                with self.assertRaisesRegex(SpellRuleError,'component policy'):capture(w)
+                self.assertEqual(whole_state(w,c),before)
+
+    def test_malformed_collections_fail_before_resource_or_opportunity_mutation(self):
+        for malformed in ('guard-consumed','recipient-history','pulse-declarations','native-consumed'):
+            with self.subTest(malformed=malformed):
+                w,c=world()
+                if malformed=='native-consumed':
+                    r=attach(c,'native',NativeOccurrenceLedger(),'cleric.hero.saint.aura-of-grace',
+                        'regular-heal',identity='native',targets=('a',),deadline=None)
+                    capture(w);w.regular_start('a',6);r.holder.consumed=[]
+                    action=lambda:c.native_occurrence(w,'native','event',eligible=True,opted_in=True)
+                else:
+                    r=pulse(c,'transcendent-meditation' if malformed=='guard-consumed' else 'song-of-mending')
+                    r.holder.resolve(0,ClockMarker(0),(),CanonicalPulseWallet(w,'a'),round_number=1)
+                    capture(w);w.regular_start('a',6)
+                    if malformed=='guard-consumed':c.outputs.consumed=[]
+                    elif malformed=='recipient-history':c.recipients.history=[]
+                    else:r.holder.declarations=[]
+                    action=lambda:c.resolve_pulse(w,'pulse','event',1,('b',))
+                before=whole_state(w,c)
+                with self.assertRaisesRegex(SpellRuleError,'collection'):action()
+                self.assertEqual(whole_state(w,c),before)
+
+    def test_bloom_missed_original_installment_does_not_block_later_due_share(self):
+        w,c=world();p=pulse(c,'eternal-bloom');h=BloomReserve({'b':10})
+        p.holder.resolve(0,ClockMarker(0),(),CanonicalPulseWallet(w,'a'),round_number=1)
+        h.consume(0,eligible_targets=())
+        attach(c,'bloom',h,PULSE_SOURCES['eternal-bloom'],'installments',identity='reserve',deadline=ClockMarker(18),parent='pulse')
+        capture(w);event(w,now=7);w.kernel_plan('b').commit()
+        self.assertEqual(h.consumed,{0,1});self.assertEqual(w.lives['b'].hp,25)
+        w.regular_start('a',12);c.resolve_pulse(w,'pulse','third-pulse',2,('b',))
+        self.assertEqual(c.consume_bloom(w,'reserve','third-share',2,eligible_targets=('b',),pulse_event='third-pulse'),{'b':3})
+
     def test_preinitiative_recipient_claim_requires_import_adapter(self):
         w,c=world();c.recipients.commit('named:Circle of Harmony',('b',),1)
         before=whole_state(w,c)
@@ -432,4 +500,3 @@
                   ('tools/temporal_playtest_rules.py','tools/temporal_control_world.py')}}
     (root/'docs/mechanics/TEMPORAL_CONTROL_WORLD_VALIDATION.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
     raise SystemExit(0 if result.wasSuccessful() else 1)
-

```

## docs/mechanics/TEMPORAL_CONTROL_WORLD_VALIDATION.json

```json
{
  "status": "PASS",
  "methods": 49,
  "failures": 0,
  "errors": 0,
  "fullTimeLoopOperational": false,
  "scope": "Live control/pulse transaction candidate; exact admitted source policies; parent/entry/mutation adapters remain",
  "hashes": {
    "tools/temporal_playtest_rules.py": "45ad6ab7d2b26baf7bc56a8377d82398781175d5a81c7562b3dedeb40f28d577",
    "tools/temporal_control_world.py": "6ca597d5efbb9945d1222f52602291bc54386e82b2c5ae4b73e949d5bff988fe"
  }
}

```

## Preserved pre-repair malformed-state probes

```json
[
  {
    "case": "guard-consumed",
    "outcome": "AttributeError: 'list' object has no attribute 'add'",
    "stateChanged": true
  },
  {
    "case": "recipient-history",
    "outcome": "AttributeError: 'list' object has no attribute 'update'",
    "stateChanged": true
  },
  {
    "case": "pulse-declarations",
    "outcome": "IndexError: list assignment index out of range",
    "stateChanged": true
  },
  {
    "case": "native-consumed",
    "outcome": "AttributeError: 'list' object has no attribute 'add'",
    "stateChanged": true
  }
]
```

## Exact current hashes

```json
{
  "status": "49-method repair candidate pending independent confirmation",
  "methods": 49,
  "fullTimeLoopOperational": false,
  "remainingMajorIntegrations": 7,
  "hashes": {
    "tools/temporal_control_world.py": "6ca597d5efbb9945d1222f52602291bc54386e82b2c5ae4b73e949d5bff988fe",
    "tools/validate_temporal_control_world.py": "6e18e042e8a92c380360288a6a9d5f2f876f4115344311cbdb5a6232a6bd6143",
    "tools/temporal_playtest_rules.py": "45ad6ab7d2b26baf7bc56a8377d82398781175d5a81c7562b3dedeb40f28d577",
    "tools/temporal_control_playtest_rules.py": "835a108a80e5ad8c5d030dbf7d927e0491bc944eb2697d71f2504fd2e0b1df12"
  }
}
```
