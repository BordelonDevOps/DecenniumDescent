# Atomic transport of the exact original parent references

The actual 59-method history closure is recorded. The next necessary parent restoration component is exact-reference staging in the EXISTING Transaction. The prior reviewed transaction accepted only copied data values; concentration contains callbacks and Druid.current must remain the original FormInstance. Copying either would violate the ten source policies.

This is an extension to the existing common transaction, not a separate commit mechanism. It adds only two specific write paths: canonical Druid.current (original registered instance or None), and ConcentrationLedger.current (a shallow map whose slot tuples must be the originals in the supplied retained-slot registry). They share the same write-conflict namespace, all-before-write stale checks, one commit and rollback. No callback, cast, entry or ending helper runs at commit. Prepared concentration maps are detached from the input map; exact slot/callback objects remain shared and pinned. Reference audit rows store object tokens rather than trying to serialize callbacks.

This layer provides identity transport, not source legality. The future parent planner must still prove complete original closures, valid clocks, paid renewal/stabilization history, nonparticipant protection, current suppression, gear/inventory/enrollment/geometry reconciliation and dependent shield/creature state. A transport-only test deliberately demonstrates that clearing Druid.current alone does NOT run ordinary child cleanup: that cleanup must be explicitly staged by the complete planner.

15 new tests pass. They cover exact original form and concentration objects, rejection of equal-looking replacements, stale current/instance/retained registries, edited prepared maps, shared conflict checks, no entry payment, no ending hook at commit, rollback of data and exact original references after an injected later assignment failure, and a subsequent REAL concentration ending reaching the original TransformationWorld link. Existing suites also pass:76 foundation +22 payment/output +50 control/pulse +59 history, 222 total including these15. No active form is yet admitted to the kernel; full Time Loop remains disabled and all seven larger integrations remain open.

The previous exact foundation is preserved separately at temporal_playtest_rules_control_checkpoint.py. Its historical approval is not silently inherited by this extension. Ordinary source helpers and the actual history module are unchanged.

Please inspect this exact transaction diff and regression evidence for atomicity/reference defects. Confirm only reference transport if sound. Parent planning and full game/GitHub flow are still open.

## Exact full-file diff

```diff
--- reviewed-control-checkpoint/temporal_playtest_rules.py
+++ reference-candidate/temporal_playtest_rules.py
@@ -77,6 +77,21 @@
     after: object
 
 
+@dataclass
+class ReferenceWrite:
+    """Transport exact retained parents; never manufacture or call a callback.
+
+    Source legality belongs to the parent planner. These narrow writes only
+    guarantee exact reference transport inside the shared atomic transaction.
+    """
+    holder: object
+    name: str
+    before: object
+    after: object
+    kind: str
+    expected: object
+
+
 class Transaction:
     """Single-thread reference compare-and-swap; no callbacks during commit.
 
@@ -114,9 +129,74 @@
         before = self.watch(holder, name)
         self.writes[key] = FieldWrite(holder, name, before, data(after))
 
+    def write_form_reference(self, druid, form):
+        """Stage the canonical Druid.current reference, including None.
+
+        Membership proves identity only. The caller must already have planned
+        legal state/expiry, dependent children, costs and geometry for this form.
+        """
+        from form_temphp_playtest_rules import DruidState, FormInstance
+        require(type(druid) is DruidState and type(druid.instances) is dict,
+                'Exact canonical Druid required for reference staging')
+        require(form is None or (type(form) is FormInstance and
+                druid.instances.get(form.instance_id) is form),'Form reference lacks canonical instance identity')
+        require(druid.current is None or (type(druid.current) is FormInstance and
+                druid.instances.get(druid.current.instance_id) is druid.current),
+                'Current form reference lacks canonical identity')
+        key=id(druid),'current'
+        require(key not in self.writes,'Conflicting adapters write the same field')
+        self.watch_shape(druid);self.watch_binding(druid,'current')
+        self.watch_binding(druid,'instances');self.watch_registry(druid.instances)
+        for current in (druid.current,form):
+            if current is not None:
+                self.watch_shape(current);self.watch(current,'instance_id')
+        self.writes[key]=ReferenceWrite(druid,'current',druid.current,form,'form',form)
+
+    def write_concentration_references(self, ledger, after, *, retained_slots):
+        """Stage original slot tuples in the actual shared concentration ledger.
+
+        retained_slots is the parent history's token->original-slot registry.
+        No fresh tuple/callback may stand in for an ended historical source.
+        Legality of the full source closure remains the planner's responsibility.
+        """
+        from transformation_spell_playtest_rules import ConcentrationLedger
+        require(type(ledger) is ConcentrationLedger and set(vars(ledger))=={'current'}
+                and type(ledger.current) is dict and type(after) is dict
+                and type(retained_slots) is dict,'Exact concentration reference registries required')
+        for rows in (ledger.current,after):
+            for owner,slot in rows.items():
+                ident(owner)
+                require(type(slot) is tuple and len(slot)==2 and type(slot[0]) is str
+                        and callable(slot[1]),'Malformed actual concentration slot')
+                require(retained_slots.get(id(slot)) is slot,'Concentration slot lacks retained original identity')
+        key=id(ledger),'current'
+        require(key not in self.writes,'Conflicting adapters write the same field')
+        self.watch_shape(ledger);self.watch_binding(ledger,'current');self.watch_registry(ledger.current)
+        self.watch_registry(retained_slots)
+        proposed=dict(after)
+        self.writes[key]=ReferenceWrite(ledger,'current',ledger.current,proposed,'concentration',dict(proposed))
+
+    @staticmethod
+    def _reference_tokens(value,kind):
+        if kind=='form':return None if value is None else {'formId':value.instance_id,'objectToken':id(value)}
+        return {owner:{'castId':slot[0],'slotToken':id(slot),'callbackToken':id(slot[1])}
+                for owner,slot in value.items()}
+
+    @staticmethod
+    def _check_reference_write(change):
+        if change.kind=='form':
+            require(change.after is change.expected,'Prepared form reference changed')
+        else:
+            require(change.kind=='concentration' and type(change.after) is dict
+                    and set(change.after)==set(change.expected)
+                    and all(change.after[k] is v for k,v in change.expected.items()),
+                    'Prepared concentration references changed')
+
     def audit_rows(self):
         return tuple({'holder': self.labels[id(v.holder)], 'field': v.name,
-                      'before': data(v.before), 'after': data(v.after)} for v in self.writes.values())
+                      'before': self._reference_tokens(v.before,v.kind) if type(v) is ReferenceWrite else data(v.before),
+                      'after': self._reference_tokens(v.after,v.kind) if type(v) is ReferenceWrite else data(v.after)}
+                     for v in self.writes.values())
 
     def commit(self):
         require(not self.used, 'Temporal transaction already committed')
@@ -128,15 +208,18 @@
             require({k: id(v) for k, v in registry.items()} == before, 'Canonical actor registry changed')
         for holder, name, before in self.watches.values():
             require(data(getattr(holder, name)) == before, 'Stale temporal plan; re-run preflight')
+        for change in self.writes.values():
+            if type(change) is ReferenceWrite:self._check_reference_write(change)
         applied = []
         try:
             for change in self.writes.values():
                 # Only exact known, ordinary Python data holders are writable.
-                setattr(change.holder, change.name, data(change.after))
+                value=(dict(change.after) if change.kind=='concentration' else change.after) if type(change) is ReferenceWrite else data(change.after)
+                setattr(change.holder, change.name, value)
                 applied.append(change)
         except Exception:
             for change in reversed(applied):
-                setattr(change.holder, change.name, data(change.before))
+                setattr(change.holder, change.name, change.before if type(change) is ReferenceWrite else data(change.before))
             raise
         self.used = True
 

```

## Complete current value-copy and transaction code

```python
def data(value):
    """Copy only explicit data leaves; forbid cross-world aliases/callbacks."""
    if value is None or type(value) in (str, int, bool, Fraction):
        return value
    if type(value) in (tuple, list, set, frozenset):
        return type(value)(data(x) for x in value)
    if type(value) is dict:
        return {data(k): data(v) for k, v in value.items()}
    if type(value) in DATA_TYPES:
        shape(value, type(value))
        # Reconstruct typed data, never copy a world/controller/callback.
        return type(value)(**{f.name: data(getattr(value, f.name)) for f in fields(value)})
    raise SpellRuleError('Unclassified temporal payload: ' + type(value).__name__)


@dataclass
class FieldWrite:
    holder: object
    name: str
    before: object
    after: object


@dataclass
class ReferenceWrite:
    """Transport exact retained parents; never manufacture or call a callback.

    Source legality belongs to the parent planner. These narrow writes only
    guarantee exact reference transport inside the shared atomic transaction.
    """
    holder: object
    name: str
    before: object
    after: object
    kind: str
    expected: object


class Transaction:
    """Single-thread reference compare-and-swap; no callbacks during commit.

    Host must hold its scene lock from preflight through commit. Every watched
    attribute is rechecked so a rest, inventory change or combat event makes a
    prepared plan stale. Container contents are replaced, holder identities stay.
    """
    def __init__(self):
        self.watches = {}
        self.writes = {}
        self.shapes = []
        self.bindings = []
        self.registries = []
        self.labels = {}
        self.used = False

    def watch_shape(self, holder):
        self.shapes.append((holder, type(holder), frozenset(vars(holder))))

    def watch_binding(self, holder, name):
        self.bindings.append((holder, name, getattr(holder, name)))

    def watch_registry(self, registry):
        self.registries.append((registry, {k: id(v) for k, v in registry.items()}))

    def watch(self, holder, name):
        key = id(holder), name
        if key not in self.watches:
            self.watches[key] = holder, name, data(getattr(holder, name))
        return data(self.watches[key][2])

    def write(self, holder, name, after):
        key = id(holder), name
        require(key not in self.writes, 'Conflicting adapters write the same field')
        before = self.watch(holder, name)
        self.writes[key] = FieldWrite(holder, name, before, data(after))

    def write_form_reference(self, druid, form):
        """Stage the canonical Druid.current reference, including None.

        Membership proves identity only. The caller must already have planned
        legal state/expiry, dependent children, costs and geometry for this form.
        """
        from form_temphp_playtest_rules import DruidState, FormInstance
        require(type(druid) is DruidState and type(druid.instances) is dict,
                'Exact canonical Druid required for reference staging')
        require(form is None or (type(form) is FormInstance and
                druid.instances.get(form.instance_id) is form),'Form reference lacks canonical instance identity')
        require(druid.current is None or (type(druid.current) is FormInstance and
                druid.instances.get(druid.current.instance_id) is druid.current),
                'Current form reference lacks canonical identity')
        key=id(druid),'current'
        require(key not in self.writes,'Conflicting adapters write the same field')
        self.watch_shape(druid);self.watch_binding(druid,'current')
        self.watch_binding(druid,'instances');self.watch_registry(druid.instances)
        for current in (druid.current,form):
            if current is not None:
                self.watch_shape(current);self.watch(current,'instance_id')
        self.writes[key]=ReferenceWrite(druid,'current',druid.current,form,'form',form)

    def write_concentration_references(self, ledger, after, *, retained_slots):
        """Stage original slot tuples in the actual shared concentration ledger.

        retained_slots is the parent history's token->original-slot registry.
        No fresh tuple/callback may stand in for an ended historical source.
        Legality of the full source closure remains the planner's responsibility.
        """
        from transformation_spell_playtest_rules import ConcentrationLedger
        require(type(ledger) is ConcentrationLedger and set(vars(ledger))=={'current'}
                and type(ledger.current) is dict and type(after) is dict
                and type(retained_slots) is dict,'Exact concentration reference registries required')
        for rows in (ledger.current,after):
            for owner,slot in rows.items():
                ident(owner)
                require(type(slot) is tuple and len(slot)==2 and type(slot[0]) is str
                        and callable(slot[1]),'Malformed actual concentration slot')
                require(retained_slots.get(id(slot)) is slot,'Concentration slot lacks retained original identity')
        key=id(ledger),'current'
        require(key not in self.writes,'Conflicting adapters write the same field')
        self.watch_shape(ledger);self.watch_binding(ledger,'current');self.watch_registry(ledger.current)
        self.watch_registry(retained_slots)
        proposed=dict(after)
        self.writes[key]=ReferenceWrite(ledger,'current',ledger.current,proposed,'concentration',dict(proposed))

    @staticmethod
    def _reference_tokens(value,kind):
        if kind=='form':return None if value is None else {'formId':value.instance_id,'objectToken':id(value)}
        return {owner:{'castId':slot[0],'slotToken':id(slot),'callbackToken':id(slot[1])}
                for owner,slot in value.items()}

    @staticmethod
    def _check_reference_write(change):
        if change.kind=='form':
            require(change.after is change.expected,'Prepared form reference changed')
        else:
            require(change.kind=='concentration' and type(change.after) is dict
                    and set(change.after)==set(change.expected)
                    and all(change.after[k] is v for k,v in change.expected.items()),
                    'Prepared concentration references changed')

    def audit_rows(self):
        return tuple({'holder': self.labels[id(v.holder)], 'field': v.name,
                      'before': self._reference_tokens(v.before,v.kind) if type(v) is ReferenceWrite else data(v.before),
                      'after': self._reference_tokens(v.after,v.kind) if type(v) is ReferenceWrite else data(v.after)}
                     for v in self.writes.values())

    def commit(self):
        require(not self.used, 'Temporal transaction already committed')
        for holder, kind, keys in self.shapes:
            require(type(holder) is kind and frozenset(vars(holder)) == keys, 'Temporal holder schema changed')
        for holder, name, bound in self.bindings:
            require(getattr(holder, name) is bound, 'Canonical temporal binding changed')
        for registry, before in self.registries:
            require({k: id(v) for k, v in registry.items()} == before, 'Canonical actor registry changed')
        for holder, name, before in self.watches.values():
            require(data(getattr(holder, name)) == before, 'Stale temporal plan; re-run preflight')
        for change in self.writes.values():
            if type(change) is ReferenceWrite:self._check_reference_write(change)
        applied = []
        try:
            for change in self.writes.values():
                # Only exact known, ordinary Python data holders are writable.
                value=(dict(change.after) if change.kind=='concentration' else change.after) if type(change) is ReferenceWrite else data(change.after)
                setattr(change.holder, change.name, value)
                applied.append(change)
        except Exception:
            for change in reversed(applied):
                setattr(change.holder, change.name, change.before if type(change) is ReferenceWrite else data(change.before))
            raise
        self.used = True



```

## Exact tools/validate_temporal_reference_transactions.py
SHA-256 `f8ee3e8edbe587e6de22fe07b9a9f233eb07f120097b042d0c12983acce4c63f`

```
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

```

## Exact docs/mechanics/TEMPORAL_REFERENCE_TRANSACTION_VALIDATION.json
SHA-256 `3dc5e5967495f0626fac280f6d499e7f8d8a0ef5da4eb2d10cf768b9586b2a1f`

```
{
  "status": "PASS",
  "testMethods": 15,
  "scope": "Atomic original-reference transport only; parent legality/restoration planner still pending",
  "kernelSha256": "e54059bd9f9dfc187ff5d6695365bed9ab8fe96583ade3dbd3d4af1cfcba1661",
  "parentRuntimeIntegrated": false,
  "fullTimeLoopOperational": false,
  "remainingMajorIntegrations": 7,
  "failures": 0,
  "errors": 0
}

```

## Exact docs/mechanics/TEMPORAL_KERNEL_VALIDATION.json
SHA-256 `287923c0845a2405e7638a4e1fffe70e53aa54ad4af2adefc0656a29d4c91123`

```
{
  "status": "PASS",
  "scope": "Unpromoted foundational temporal kernel only; seven integrations and actual notebook review remain",
  "testMethods": 76,
  "failures": 0,
  "errors": 0,
  "fullTimeLoopOperational": false,
  "helperSha256": "e54059bd9f9dfc187ff5d6695365bed9ab8fe96583ade3dbd3d4af1cfcba1661"
}

```

## Exact docs/mechanics/TEMPORAL_PARENT_HISTORY_VALIDATION.json
SHA-256 `4dd04b3c5ce315205e6a765a674aad15e0db503f204c209fc8d74c0da6281151`

```
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
