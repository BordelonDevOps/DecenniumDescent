from pathlib import Path
import sys,json
from copy import deepcopy
from dataclasses import asdict,is_dataclass
from fractions import Fraction
sys.dont_write_bytecode=True
root=Path(sys.argv[1]).resolve();sys.path.insert(0,str(root/'DescentReviewChanges/ReviewBible/tools'))
from feat335_copy_payload_fixtures import CopyPayloadFixtures
from healing_playtest_rules import HealingReduction,healing_packet
from form_temphp_playtest_rules import BufferGrant
from control_playtest_rules import ClockMarker
f=CopyPayloadFixtures();cases=[]
def clean(v):
 if is_dataclass(v):return clean(asdict(v))
 if isinstance(v,Fraction):return str(v)
 if isinstance(v,dict):return {str(k):clean(x) for k,x in v.items()}
 if isinstance(v,(list,tuple)):return [clean(x) for x in v]
 if isinstance(v,set):return sorted(clean(x) for x in v)
 return v
for timing in ['before-declaration','after-paid-declaration']:
 for present,suppressed in [(False,False),(True,True)]:
  m=f.make();f.start(m);f.capture(m,'mend')
  if timing=='after-paid-declaration':f.declare(m,'mend')
  actor=m.world.actors['target'];r=HealingReduction('old','actual-reducer','flat',1,present=present,suppressed=suppressed,next_healing=True);actor['healingReductions']=[r]
  expected=healing_packet(actor['life'],2,dice_count=2,reductions=[r])
  before=m.snapshot();error=None;result=None
  try:
   if timing=='before-declaration':f.declare(m,'mend')
   result=m.resolve('cast',rolls={'nativeDice':[4,4]})
  except ValueError as e:error=str(e)
  cases.append({'id':'LOCAL-COPY-INACTIVE-MEND-'+('ABSENT' if not present else 'SUPPRESSED')+'::'+timing,'reducer':clean(r),'expectedByHelper':{'hp':expected['state'].hp,'nextHealingCandidates':expected['nextHealingCandidates']},'before':clean(before),'after':clean(m.snapshot()),'error':error,'failureAtomic':m.snapshot()==before if error else None,'hp':actor['life'].hp,'result':clean(result)})
m=f.make();f.start(m);g=BufferGrant('actual-prior-overflow','oracle.supplement.life.overflowing-light','prior-owner','target',5,expiry=ClockMarker(12),riders={'overflowing-cleanse'})
m.world.buffers.offer(g,m.world.now);m.world.projection();before=m.snapshot();expected=deepcopy(m.world.buffers).expire(ClockMarker(12));returned=m.world.advance(ClockMarker(12),[m]);second=m.world.buffers.expire(ClockMarker(12))
cases.append({'id':'LOCAL-COPY-SHARED-BUFFER-EXPIRY-01','premise':'Conditionally already lawfully established source-specific buffer. No Oracle acquisition or condition application is implemented.','before':clean(before),'expected':clean(expected),'returned':clean(returned),'secondExpiry':clean(second),'finalGrantState':m.world.buffers.grants[g.grant_id].state,'after':clean(m.snapshot())})
print(json.dumps({'variant':root.name,'cases':cases},indent=2))
