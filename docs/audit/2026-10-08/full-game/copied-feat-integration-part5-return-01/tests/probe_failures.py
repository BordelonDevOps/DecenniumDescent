"""Reproduce five bounded findings on a separately staged reference tree.
No project runtime or source qualified creature acquisition is inferred.
"""
from pathlib import Path
import argparse,sys,json
sys.dont_write_bytecode = True
from copy import deepcopy
p=argparse.ArgumentParser();p.add_argument('--source-root',required=True);p.add_argument('--report',required=True);a=p.parse_args()
R=Path(a.source_root).resolve();T=R/'DescentReviewChanges/ReviewBible/tools';sys.path.insert(0,str(T))
import apply_di7_ap_as_01 as loc
loc.G=R;loc.R=R/'DescentReviewChanges/ReviewBible';loc.A=R/'docs/audit/2026-10-08/full-game';loc.V=loc.A/'di7-joint-review-01-verdict'
from feat335_copy_class_fixtures import ClassCopyFixtures
from feat335_copy_payload_fixtures import CopyPayloadFixtures
from feat335_copy_payloads import CopyPayloadReleases
from validate_feat335_copy_classes_01 import clean
F=ClassCopyFixtures();P=CopyPayloadFixtures();out=[]
def run(ident,m,attempt,extra=None):
 row={'id':ident,'fullBefore':clean(m.snapshot()),'extraBefore':clean(extra()) if extra else None}
 try:row['outcome']={'returned':clean(attempt()),'rejected':False}
 except ValueError as e:row['outcome']={'rejected':True,'reason':str(e)}
 row.update(fullAfter=clean(m.snapshot()),extraAfter=clean(extra()) if extra else None);out.append(row)
for name,linked in [('Shaman',True),('Mirrorsage',False)]:
 m,s=F.class_make(name,shaman=linked);run('CFI-01/'+name,m,lambda:F.capture_class(m,'mend',sid='eldritch_echo'),lambda:{'nativeReaction':m.action_account.get('reactions',m.action_account.get('reaction')),'captureReaction':m.captures.reactions})
m=P.make();P.capture(m,'mend',adapt=True);P.start(m);P.declare(m,'mend');m.resolve('cast',rolls={'nativeDice':[4,4]})
def duplicate():
 n=CopyPayloadReleases(m.captures,m.owner,m.pool,m.cadence,m.lifecycle.ledger,m.world)
 return n.declare('again','capture',permission='adapted',grant_id='Wizard/class-engine',frame=P.frame(n),selection=P.selection('mend'))
run('CFI-02/duplicate-adapter',m,duplicate)
m,s=F.class_make('Shaman',shaman=True);F.capture_class(m,'mend');F.declare_class(m,'mend');s.actors['owner']['body']['conscious']=False
run('CFI-03/native-unconscious',m,lambda:m.resolve('cast',rolls={'nativeDice':[4,4]}),lambda:{'nativeConscious':s.actors['owner']['body']['conscious'],'targetHP':m.world.actors['target']['life'].hp})
m,s=F.class_make('Shaman',shaman=True);F.capture_class(m,'ward');F.declare_class(m,'ward');s.actors['owner']['concentration']='independently-established-new-source'
run('CFI-03/native-concentration-drift',m,lambda:m.resolve('cast',rolls={'nativeDice':[4,4]}),lambda:{'nativeBurden':s.actors['owner']['concentration'],'bridgeBurden':m.lifecycle.snapshot()['currentBurden']})
m,s=F.class_make('Shaman',shaman=True);F.capture_class(m,'step');selection=F.selection('step');selection.update(destination=[-15,0,0],distanceFeet=15)
def step():
 m.declare('step','capture',permission='pending',grant_id='Shaman/class-engine',frame=F.frame(m),selection=selection)
 return m.resolve('step')
run('CFI-04/native-Step-pose',m,step,lambda:{'nativePositionFeet':s.actors['owner']['positionFeet'],'copyWorldPosition':m.world.actors['owner']['position'],'qualifyingNativeAura':s._qualifying_aura('owner')})
m=P.make();c=m.captures;c.start_extra('same-id',1,actual_extra_turn=True);c.end_extra('same-id',actual_extra_end=True);c.reactions=0
run('CFI-05/reused-turn-id',m,lambda:c.start_regular('same-id',1,1,actual_new_regular_start=True))
Path(a.report).write_text(json.dumps({'scope':'Isolated source-fixture adversarial reference probes, not live game events. Full before/after states retained. Five issues, seven probe scenarios.','sourceRoot':str(R),'probes':out},indent=2,ensure_ascii=False)+'\n')
print(json.dumps([{'id':r['id'],'rejected':r['outcome']['rejected'],'extraAfter':r['extraAfter']} for r in out]))
