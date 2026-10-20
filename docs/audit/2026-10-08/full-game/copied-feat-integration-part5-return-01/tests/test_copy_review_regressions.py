"""Independent isolated tests of delivered/proposed reference modules, not a game engine.
Run: python test_copy_review_regressions.py --source-root ROOT --report REPORT.json
Source-root is a separately extracted sandbox, never a production working tree.
The Windows-only DI7 locator is rebound in memory; source bytes are not changed.
"""
from pathlib import Path
import argparse,sys,json,unittest,traceback
sys.dont_write_bytecode = True
from copy import deepcopy
from fractions import Fraction

parser=argparse.ArgumentParser();parser.add_argument('--source-root',required=True);parser.add_argument('--report',required=True)
args=parser.parse_args(); ROOT=Path(args.source_root).resolve(); TOOLS=ROOT/'DescentReviewChanges/ReviewBible/tools'
sys.path.insert(0,str(TOOLS))
import apply_di7_ap_as_01 as locator
locator.G=ROOT;locator.R=ROOT/'DescentReviewChanges/ReviewBible';locator.A=ROOT/'docs/audit/2026-10-08/full-game';locator.V=locator.A/'di7-joint-review-01-verdict'
from feat335_copy_class_fixtures import ClassCopyFixtures
from feat335_copy_payload_fixtures import CopyPayloadFixtures
from feat335_copy_capture import CopyCaptures
from feat335_copy_payloads import CopyPayloadReleases
from feat335_copy_class_release import ClassCopyPayloadReleases,ShamanConcentrationBridge
from feat335_copy_release import CopyReleases
from transformation_spell_playtest_rules import ConcentrationLedger
F=ClassCopyFixtures(); P=CopyPayloadFixtures()

class Regressions(unittest.TestCase):
    """Each test preserves source-qualified fixture premises; no invented game provider."""
    def unchanged_error(self,m,fn):
        before=m.snapshot()
        with self.assertRaises(ValueError):fn()
        self.assertEqual(before,m.snapshot())

    def test_same_owner_adapter_cannot_reset_release_cap(self):
        m=P.make();P.capture(m,'mend',adapt=True);P.start(m);P.declare(m,'mend');m.resolve('cast',rolls={'nativeDice':[4,4]})
        self.unchanged_error(m,lambda:CopyPayloadReleases(m.captures,m.owner,m.pool,m.cadence,m.lifecycle.ledger,m.world))

    def test_same_owner_plain_commit_adapter_cannot_bypass_payload_adapter(self):
        m=P.make()
        self.unchanged_error(m,lambda:CopyReleases(m.captures,m.owner,m.pool,m.cadence,m.lifecycle.ledger))

    def test_same_owner_new_capture_wrapper_cannot_reset_release_cap(self):
        m=P.make();c=CopyCaptures(m.captures.acquired,m.captures.witnesses)
        self.unchanged_error(m,lambda:CopyPayloadReleases(c,m.owner,m.pool,m.cadence,m.lifecycle.ledger,m.world))

    def test_bad_pool_constructor_does_not_reserve_owner(self):
        m=P.make();ledger=ConcentrationLedger();pool=deepcopy(m.pool);pool['owner']='not-owner'
        with self.assertRaises(ValueError):CopyPayloadReleases(m.captures,m.owner,pool,m.cadence,ledger,m.world)
        self.assertNotIn(m.owner,getattr(ledger,'_feat_copy_engine_owners',set()))
        n=CopyPayloadReleases(m.captures,m.owner,m.pool,m.cadence,ledger,m.world)
        self.assertEqual(n.owner,m.owner)

    def test_bad_world_constructor_does_not_reserve_owner(self):
        m=P.make();ledger=ConcentrationLedger()
        with self.assertRaises(ValueError):CopyPayloadReleases(m.captures,m.owner,m.pool,m.cadence,ledger,None)
        self.assertNotIn(m.owner,getattr(ledger,'_feat_copy_engine_owners',set()))

    def test_existing_owner_cap_survives_concentration_end(self):
        m=P.make();P.capture(m,'ward');P.start(m);P.declare(m,'ward');m.resolve('cast',rolls={'nativeDice':[4,4]})
        m.lifecycle.ledger.end(m.owner,'actual-qualified-concentration-loss')
        self.unchanged_error(m,lambda:CopyPayloadReleases(m.captures,m.owner,m.pool,m.cadence,m.lifecycle.ledger,m.world))

    def test_different_owners_can_share_actual_concentration_ledger(self):
        m=P.make();c=CopyCaptures(m.captures.acquired,m.captures.witnesses);pool=deepcopy(m.pool);pool['owner']='other'
        n=CopyReleases(c,'other',pool,deepcopy(m.cadence),m.lifecycle.ledger)
        self.assertEqual(n.owner,'other')

    def test_extra_turn_event_cannot_be_replayed_as_regular(self):
        m=P.make();c=m.captures;c.start_extra('extra1',1,actual_extra_turn=True);c.end_extra('extra1',actual_extra_end=True)
        self.unchanged_error(m,lambda:c.start_regular('extra1',1,1,actual_new_regular_start=True))

    def test_regular_turn_event_cannot_be_replayed_as_extra(self):
        m=P.make();c=m.captures;c.start_regular('regular1',1,1,actual_new_regular_start=True);c.end_regular('regular1',actual_regular_end=True)
        self.unchanged_error(m,lambda:c.start_extra('regular1',1,actual_extra_turn=True))

    def test_distinct_extra_then_distinct_regular_remains_legal(self):
        m=P.make();c=m.captures;c.start_extra('extra1',1,actual_extra_turn=True);c.end_extra('extra1',actual_extra_end=True)
        c.start_regular('regular1',1,1,actual_new_regular_start=True)
        self.assertEqual((c.current_turn,c.regular_ordinal),('regular1',1))

    def test_linked_shaman_step_rejected_before_payment(self):
        m,s=F.class_make('Shaman',shaman=True);F.capture_class(m,'step');frame=F.frame(m);original=deepcopy(frame)
        sel=F.selection('step');sel.update(destination=[-15,0,0],distanceFeet=15)
        native=deepcopy(s.actors);world=deepcopy(s.world);totems=deepcopy(s.totems)
        self.unchanged_error(m,lambda:m.declare('cast','capture',permission='pending',grant_id='Shaman/class-engine',frame=frame,selection=sel))
        self.assertEqual(frame,original);self.assertEqual(native,s.actors);self.assertEqual(world,s.world);self.assertEqual(totems,s.totems)
        self.assertEqual(s.actors['owner']['positionFeet'],0)

    def test_unlinked_shaman_step_keeps_disclosed_coordinate_only_slice(self):
        m,s=F.class_make('Shaman');F.capture_class(m,'step');F.declare_class(m,'step');r=m.resolve('cast')
        self.assertTrue(r['resolved']);self.assertEqual(m.world.actors['owner']['position'],[10,0,0]);self.assertIsNone(s)

    def test_mirrorsage_step_keeps_disclosed_coordinate_only_slice(self):
        m,s=F.class_make('Mirrorsage');F.capture_class(m,'step');F.declare_class(m,'step');r=m.resolve('cast')
        self.assertTrue(r['resolved']);self.assertEqual(m.world.actors['owner']['position'],[10,0,0])

    def test_shaman_concentration_drift_blocks_payload_without_overwrite(self):
        m,s=F.class_make('Shaman',shaman=True);F.capture_class(m,'ward');F.declare_class(m,'ward')
        s.actors['owner']['concentration']='new-unintegrated-actual-source'
        self.unchanged_error(m,lambda:m.resolve('cast',rolls={'nativeDice':[4,4]}))
        self.assertEqual(s.actors['owner']['concentration'],'new-unintegrated-actual-source')
        self.assertNotIn(('owner','cast'),m.world.resolutions)

    def test_shaman_concentration_drift_blocks_counter_cleanup(self):
        m,s=F.class_make('Shaman',shaman=True);F.capture_class(m,'ward');F.declare_class(m,'ward')
        s.actors['owner']['concentration']='new-unintegrated-actual-source'
        self.unchanged_error(m,lambda:m.resolve('cast',countered=True))
        self.assertEqual(s.actors['owner']['concentration'],'new-unintegrated-actual-source')

    def test_shaman_concentration_drift_blocks_world_expiry_before_clock_mutation(self):
        m,s=F.class_make('Shaman',shaman=True);F.capture_class(m,'ward');F.declare_class(m,'ward');m.resolve('cast',rolls={'nativeDice':[4,4]})
        s.actors['owner']['concentration']='new-unintegrated-actual-source'
        before=m.world.now
        self.unchanged_error(m,lambda:m.world.advance(Fraction(4000),[m]))
        self.assertEqual(m.world.now,before)

    def test_integrated_concentration_end_remains_final(self):
        m,s=F.class_make('Shaman',shaman=True);F.capture_class(m,'ward');F.declare_class(m,'ward')
        m.lifecycle.ledger.end('owner','actual-integrated-loss');r=m.resolve('cast')
        self.assertFalse(r['resolved']);self.assertIsNone(s.actors['owner']['concentration']);self.assertEqual(m.world.buffers.amount('target'),0)

    def test_actual_somatic_loss_after_commit_not_a_second_component_payment(self):
        m,s=F.class_make('Shaman',shaman=True);F.capture_class(m,'mend');F.declare_class(m,'mend')
        for hand in s.actors['owner']['body']['hands'].values():hand['usable']=False
        r=m.resolve('cast',rolls={'nativeDice':[4,4]});self.assertTrue(r['resolved'])

    def test_reaction_link_has_no_late_ledger_merge(self):
        m=P.make();c=m.captures;c.start_regular('r',1,1,actual_new_regular_start=True)
        before=c.snapshot();account={'reaction':False}
        with self.assertRaises(ValueError):c.bind_reaction_account(account,'reaction',lambda:True)
        self.assertEqual(c.snapshot(),before);self.assertFalse(account['reaction'])

    def test_reaction_link_cannot_be_rebound(self):
        m=P.make();c=m.captures;a={'reaction':False};c.bind_reaction_account(a,'reaction',lambda:True)
        before=c.snapshot();b={'reaction':True}
        with self.assertRaises(ValueError):c.bind_reaction_account(b,'reaction',lambda:True)
        self.assertEqual(c.snapshot(),before);self.assertFalse(a['reaction']);self.assertTrue(b['reaction'])

    def test_invalid_reaction_link_field_does_not_mutate(self):
        m=P.make();c=m.captures;before=c.snapshot()
        with self.assertRaises(ValueError):c.bind_reaction_account({'rp':5},'rp',lambda:True)
        self.assertEqual(c.snapshot(),before)

    def test_singular_reaction_link_does_not_coerce_nonboolean(self):
        m=P.make();c=m.captures;before=c.snapshot()
        with self.assertRaises(ValueError):c.bind_reaction_account({'reaction':1},'reaction',lambda:True)
        self.assertEqual(c.snapshot(),before)

    def test_counted_reaction_link_does_not_coerce_boolean(self):
        m=P.make();c=m.captures;before=c.snapshot()
        with self.assertRaises(ValueError):c.bind_reaction_account({'reactions':True},'reactions',lambda:True)
        self.assertEqual(c.snapshot(),before)

    def test_singular_link_rejects_invented_second_reaction(self):
        m=P.make();c=m.captures;a={'reaction':True};c.bind_reaction_account(a,'reaction',lambda:True)
        with self.assertRaises(ValueError):c.reactions=2
        self.assertTrue(a['reaction']);self.assertEqual(c.reactions,1)

# Explicit class variants retain real fixture type and actual Reaction account.
def add_class_tests(cls,linked,field):
    label=cls.lower()
    def make():return F.class_make(cls,shaman=linked)
    def echo_debit(self):
        m,s=make();F.capture_class(m,'mend',sid='eldritch_echo')
        self.assertEqual(m.captures.reactions,0);self.assertEqual(int(m.action_account[field]),0)
    def native_debit(self):
        m,s=make();m.action_account[field]=False if field=='reaction' else 0
        self.unchanged_error(m,lambda:F.capture_class(m,'mend',sid='eldritch_echo'))
    def mimicry_free(self):
        m,s=make();before=m.action_account[field];F.capture_class(m,'mend')
        self.assertEqual(m.action_account[field],before)
    def denied(self):
        m,s=make();m.world.actors['owner']['ordinaryReactionAllowed']=False
        self.unchanged_error(m,lambda:F.capture_class(m,'mend',sid='eldritch_echo'))
    def extra(self):
        m,s=make();F.capture_class(m,'mend',sid='eldritch_echo');c=m.captures;turn=c.current_turn
        c.end_regular(turn,actual_regular_end=True);c.start_extra('extra',1,actual_extra_turn=True)
        self.assertEqual(int(m.action_account[field]),0);self.assertEqual(c.reactions,0)
    def regular(self):
        m,s=make();F.capture_class(m,'mend',sid='eldritch_echo');c=m.captures;turn=c.current_turn
        c.end_regular(turn,actual_regular_end=True);c.start_regular('next-actual-start',2,2,actual_new_regular_start=True)
        self.assertEqual(int(m.action_account[field]),1);self.assertEqual(c.reactions,1)
    def invalid_component(self):
        m,s=make();self.unchanged_error(m,lambda:F.capture_class(m,'nonexistent',sid='eldritch_echo'))
    def multiple(self):
        m,s=make();self.unchanged_error(m,lambda:ClassCopyPayloadReleases(m.captures,m.owner,m.pool,m.cadence,m.lifecycle.ledger,m.world,echoes=m.echoes,action_account=m.action_account))
    for suffix,fn in [('echo_debits_actual_reaction',echo_debit),('actual_reaction_spend_blocks_echo',native_debit),('mimicry_does_not_spend_reaction',mimicry_free),('actual_reaction_denial_blocks_echo',denied),('extra_turn_does_not_refresh',extra),('actual_regular_start_refreshes',regular),('invalid_component_atomic',invalid_component),('duplicate_adapter_rejected',multiple)]:
        setattr(Regressions,'test_'+label+'_'+suffix,fn)
add_class_tests('Shaman',True,'reactions');add_class_tests('Mirrorsage',False,'reaction')

for field in ['conscious','canAct']:
    def fn(self,field=field):
        m,s=F.class_make('Shaman',shaman=True);F.capture_class(m,'mend');F.declare_class(m,'mend');paid=m.pool['rp'];hp=m.world.actors['target']['life'].hp
        s.actors['owner']['body'][field]=False;r=m.resolve('cast')
        self.assertFalse(r['resolved']);self.assertEqual(r['refund'],0);self.assertEqual(m.pool['rp'],paid);self.assertEqual(m.world.actors['target']['life'].hp,hp)
        self.unchanged_error(m,lambda:m.resolve('cast'))
    setattr(Regressions,'test_linked_body_'+field+'_false_blocks_payload_once',fn)
    def fn2(self,field=field):
        m,s=F.class_make('Shaman',shaman=True);s.actors['owner']['body'][field]=False
        self.unchanged_error(m,lambda:F.capture_class(m,'mend',sid='eldritch_echo'))
    setattr(Regressions,'test_linked_body_'+field+'_false_blocks_echo_capture',fn2)

def capture_body_reaction(self):
    m,s=F.class_make('Shaman',shaman=True);s.actors['owner']['body']['reactionLegal']=False
    self.unchanged_error(m,lambda:F.capture_class(m,'mend',sid='eldritch_echo'))
Regressions.test_linked_native_reaction_prohibition=capture_body_reaction

for field,value in [('reaction',False),('reactions',0)]:
    def fn(self,field=field,value=value):
        m=P.make();c=m.captures;a={field:value};c.bind_reaction_account(a,field,lambda:True)
        self.assertEqual(c.reactions,0);self.assertEqual(a[field],value)
        snap=c.snapshot();self.assertEqual(snap['reactionBinding'],{'linked':True,'field':field})
        self.assertNotIn('_reaction_legality',snap);self.assertNotIn('_reaction_account',snap)
    setattr(Regressions,'test_binding_'+field+'_adopts_spent_without_refill',fn)

class RecordingResult(unittest.TextTestResult):
    def __init__(self,*a,**kw):super().__init__(*a,**kw);self.records=[]
    def addSuccess(self,t):super().addSuccess(t);self.records.append({'id':t.id(),'status':'PASS'})
    def addFailure(self,t,e):super().addFailure(t,e);self.records.append({'id':t.id(),'status':'FAIL','traceback':self._exc_info_to_string(e,t)})
    def addError(self,t,e):super().addError(t,e);self.records.append({'id':t.id(),'status':'ERROR','traceback':self._exc_info_to_string(e,t)})
runner=unittest.TextTestRunner(verbosity=2,resultclass=RecordingResult)
r=runner.run(unittest.defaultTestLoader.loadTestsFromTestCase(Regressions))
report={'scope':'Isolated delivered/proposed reference-module regression tests; no game engine/runtime/human/balance execution. In-memory archive path relocation only.',
        'sourceRoot':str(ROOT),'testsRun':r.testsRun,'failures':len(r.failures),'errors':len(r.errors),'results':r.records}
Path(args.report).write_text(json.dumps(report,indent=2)+'\n')
raise SystemExit(0 if r.wasSuccessful() else 1)
