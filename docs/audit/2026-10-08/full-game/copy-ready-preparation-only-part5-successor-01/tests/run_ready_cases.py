"""Complete finite specification cases; executes no delivered/project module.
The output path must be new and outside the manifest-bound bundle.
"""
from pathlib import Path
import json, sys, copy, argparse
from ready_policy_reference import ReadyPolicyReference, PROFILES

BASE=dict(event='hold-A',round_id='N',now=0,ready_expiry=6,capture_expiry=20)
def prep(**kw):return dict(method='prepare',arguments={**BASE,**kw})
def rel(**kw):return dict(method='release',arguments={'event':'release-A','round_id':'N+1','now':5,**kw})
def step(method,**kw):return dict(method=method,arguments=kw)
def at(path,value):return {'path':path,'value':value}

# Each case retains its complete initial state, events, selected and historical
# traces. Predicates are stipulated source-qualified inputs, not engine checks.
CASES=[]
def case(i,title,events,checks,*,owned=False,initial=None,qualification=None,historical_difference=None):
 CASES.append(dict(id=i,title=title,ownsMirrorsage=owned,initialOverrides=initial or {},events=events,expected=checks,
   qualification=qualification or 'Isolated accounting fixture. Actual source acquisition, q/quote, action availability, clocks, perception and geometry are supplied premises; no runtime reachability is demonstrated.',
   historicalDifference=historical_difference))

case('RP02-01','Same-round valid release', [prep(),rel(round_id='N',now=2)], [at('lastResult','release-committed'),at('state.feat_rounds',{'N':'hold-A'}),at('state.rp',23),at('state.counts.reactions',1),at('state.counts.payments',1)])
case('RP02-02','Later-round release, otherwise free new-round allowance',[prep(),rel()], [at('lastResult','release-committed'),at('state.feat_rounds',{'N':'hold-A'}),at('state.counts.history',1),at('state.counts.counter_windows',1),at('state.counts.components',1)],historical_difference='Old rule added N+1; selected rule leaves it free.')
case('RP02-03','Owned Mirrorsage same-round release',[prep(),rel(round_id='N',now=2)], [at('state.class_rounds',{'N':'hold-A'}),at('state.feat_rounds',{'N':'hold-A'}),at('state.counts.reactions',1)],owned=True)
case('RP02-04','Owned Mirrorsage later-round release',[prep(),rel()], [at('state.class_rounds',{'N':'hold-A'}),at('state.feat_rounds',{'N':'hold-A'}),at('state.authorizations',2)],owned=True,historical_difference='Old rule added both N+1 allowances; selected rule adds neither.')
case('RP02-05','Another otherwise lawful nonconcentration copy precedes release',[prep(),step('direct',event='other-copy',round_id='N+1',now=4,legal_action=True),rel()], [at('lastResult','release-committed'),at('state.feat_rounds',{'N':'hold-A','N+1':'other-copy'}),at('state.counts.payloads',2),at('state.rp',16),at('state.counts.payments',2),at('state.counts.history',2)],qualification='The earlier direct copy requires its own genuinely legal Action/source opportunity BEFORE this hold expires at the next owner regular START. This fixture grants no such extra Action and is conditional on an actual provider. Its immediate profile does not break held concentration.',historical_difference='Old release blocked by other-copy cap; selected release succeeds without rewriting that spend.')
case('RP02-06','Actually owned class shared allowance already spent',[prep(),step('supplied_class_use',event='class-other',round_id='N+1'),rel()], [at('lastResult','release-committed'),at('state.class_rounds',{'N':'hold-A','N+1':'class-other'}),at('state.feat_rounds',{'N':'hold-A'})],owned=True,qualification='Requires a separately genuine class-use event that leaves the held concentration and Reaction available. Its real class costs/effects are external premises, not a class Echo implementation.',historical_difference='Old class cap blocks release; selected policy does not consult release-round availability.')
case('RP02-07','Both current-round allowances already spent by one lawful copy',[prep(),step('direct',event='other-copy',round_id='N+1',now=4),rel()], [at('lastResult','release-committed'),at('state.feat_rounds',{'N':'hold-A','N+1':'other-copy'}),at('state.class_rounds',{'N':'hold-A','N+1':'other-copy'}),at('state.counts.payloads',2)],owned=True,qualification='Conditional separately lawful pre-expiry Action/source opportunity, nonconcentration copy, real remaining Reaction. No action or source is granted by the cap policy.',historical_difference='Old release fails; selected release uses only Reaction and hold receipt.')
case('RP02-08','Release first, then a genuinely lawful new commitment in that round',[prep(),rel(),step('direct',event='other-copy',round_id='N+1',now=7)], [at('lastResult','direct-committed'),at('state.counts.payloads',2),at('state.feat_rounds',{'N':'hold-A','N+1':'other-copy'}),at('state.rp',16)],qualification='The hold releases at5 before its deadline6. A separate actual regular-turn Action and still-valid source permission are supplied at7 within the same numbered round N+1. No hold crosses expiry and no Action is granted by this policy.',historical_difference='Old release spent N+1 and blocked later direct; selected release leaves that allowance free.')
case('RP02-09','Policy supplies no competing Action',[prep(),step('direct',event='no-action',round_id='N+1',now=4,legal_action=False),rel()], [at('results.1','direct-rejected'),at('lastResult','release-committed'),at('state.rp',23),at('state.counts.payloads',1)])
case('RP02-10','Competing concentration cast really ends the old hold',[prep(),step('direct',event='new-ward',round_id='N+1',now=4,profile='Ward'),rel()], [at('lastResult','no-hold'),at('state.concentration',{'id':'new-ward','state':'sustained'}),at('state.counts.reactions',0)],qualification='The new cast has a separately genuine pre-expiry Action/source opportunity. It really displaces held concentration; ignoring current-round cap does not preserve the old hold.')
for i,key,title in [(11,'trigger_completed','Incomplete trigger'),(12,'trigger_perceived','Unperceived trigger'),(13,'legal_target','Invalid target'),(14,'legal_source','Missing actual source predicate')]:
 case(f'RP02-{i:02}',title,[prep(),rel(**{key:False})],[at('lastResult','release-not-committed'),at('state.counts.reactions',0),at('state.hold.id','hold-A'),at('state.feat_rounds',{'N':'hold-A'})])
case('RP02-15','Declined trigger preserves live hold',[prep(),rel(declined=True)],[at('lastResult','release-not-committed'),at('state.hold.ready_expiry',6),at('state.counts.reactions',0)])
case('RP02-16','Already spent real Reaction blocks release',[prep(),rel()],[at('lastResult','release-not-committed'),at('state.hold.id','hold-A'),at('state.counts.reactions',0)],initial={'reaction_available':False})
case('RP02-17','Invalid target then a later genuinely legal occurrence',[prep(),rel(now=3,legal_target=False),rel(event='release-B',now=5,target='new-current-target')],[at('lastResult','release-committed'),at('state.counts.reactions',1),at('state.last_target','new-current-target'),at('state.counts.payments',1)])
case('RP02-18','Exact Ready/next-owner-START expiry wins',[prep(),rel(now=6)],[at('lastResult','expired'),at('state.hold',None),at('state.counts.reactions',0),at('state.rp',23),at('state.feat_rounds',{'N':'hold-A'})])
case('RP02-19','Earlier capture/use expiry is not extended',[prep(capture_expiry=4),rel(now=4)],[at('lastResult','expired'),at('state.counts.payloads',0),at('state.counts.reactions',0)],qualification='A separately actual earlier capture deadline4 governs even though Ready would end6. No claim that all captured profiles can survive into another numbered round.')
case('RP02-20','Counter at paid preparation retains spend',[prep(countered=True),rel()],[at('results.0','preparation-countered'),at('lastResult','no-hold'),at('state.rp',23),at('state.feat_rounds',{'N':'hold-A'}),at('state.counts.counter_windows',1)])
case('RP02-21','Abandonment retains preparation and does not free same round',[prep(),step('end',reason='abandoned'),step('direct',event='retry-copy',round_id='N',now=2)],[at('lastResult','direct-rejected'),at('state.rp',23),at('state.feat_rounds',{'N':'hold-A'}),at('state.counts.reactions',0)])
case('RP02-22','Concentration loss does not refund or revive',[prep(),step('end',reason='concentration-lost'),rel()],[at('lastResult','no-hold'),at('state.hold',None),at('state.counts.reactions',0),at('state.rp',23)])
case('RP02-23','Failed preparation class allowance is atomic',[prep()],[at('lastResult','preparation-rejected'),at('state.rp',30),at('state.feat_rounds',{}),at('state.class_rounds',{'N':'prior'}),at('state.counts.actions',0)],owned=True,initial={'class_rounds':{'N':'prior'}})
case('RP02-24','Failed preparation source validation is atomic',[prep(legal_sources=False)],[at('lastResult','preparation-rejected'),at('state.rp',30),at('state.counts.payments',0),at('state.authorizations',3)])
case('RP02-25','Release-time target not setup ghost target',[prep(),rel(target='actually-perceived-current-recipient')],[at('state.last_target','actually-perceived-current-recipient'),at('state.counts.components',1),at('state.counts.history',1)],qualification='Actual target eligibility/geometry is a supplied current-state predicate; no world perception or geometry is implemented. The hold contains no preselected target.')
case('RP02-26','Fixed preparation profile cannot be rewritten',[prep(),rel(expected_profile='Mend')],[at('lastResult','release-not-committed'),at('state.hold.profile','Strike'),at('state.counts.reactions',0)])
case('RP02-27','Fixed preparation mode cannot be rewritten',[prep(),rel(expected_mode='another-component')],[at('lastResult','release-not-committed'),at('state.counts.reactions',0)])
case('RP02-28','Later payload prevention retains only real committed spends',[prep(),rel(late_prevented=True)],[at('lastResult','release-committed-prevented'),at('state.counts.payloads',0),at('state.counts.reactions',1),at('state.feat_rounds',{'N':'hold-A'}),at('state.class_rounds',{'N':'hold-A'}),at('state.rp',23)],owned=True,historical_difference='Old rule also spent N+1. New rule does not create such spends; no refund of Reaction or preparation.')
case('RP02-29','Duplicate callback cannot replay',[prep(),rel(),rel()],[at('lastResult','duplicate-release'),at('state.counts.payloads',1),at('state.counts.reactions',1),at('state.counts.permissions',1)])
case('RP02-30','Unowned Mirrorsage account is never created',[prep(),rel()],[at('state.class_rounds',{}),at('state.counts.reactions',1)])
case('RP02-31','Same-round new direct attempt still respects its cap',[prep(),step('direct',event='second-copy',round_id='N',now=2),rel(round_id='N',now=3)],[at('results.1','direct-rejected'),at('lastResult','release-committed'),at('state.rp',23)])
case('RP02-32','Failed replacement preserves prior hold',[prep(),prep(event='bad-new',round_id='N+1',now=3,ready_expiry=10,legal_action=False),rel()],[at('results.1','preparation-rejected'),at('lastResult','release-committed'),at('state.counts.payments',1)])
case('RP02-33','Preparation identity cannot be reused',[prep(),step('end',reason='abandoned'),prep(round_id='N+1',now=3,ready_expiry=10)],[at('lastResult','preparation-rejected'),at('state.rp',23),at('state.counts.payments',1)])
case('RP02-34','JSON fixture restoration preserves paid authorization and expiry',[prep(),step('fixture_json_roundtrip'),rel(),step('fixture_json_roundtrip'),rel()],[at('lastResult','duplicate-release'),at('state.counts.reactions',1),at('state.rp',23),at('state.feat_rounds',{'N':'hold-A'})],qualification='Serialization continuity of this isolated data model only; no production save/load, server authority or crash recovery is implemented.')
case('RP02-35','Actual preparation receipt still required',[prep(),step('fixture_corrupt_preparation_receipt'),rel()],[at('lastResult','invalid-preparation-receipt'),at('state.counts.reactions',0),at('state.rp',23)],qualification='Harness corruption of the historical receipt is rejected. This is an internal consistency result, not a public failure diagnostic or a current-round cap check.')
for j,profile in enumerate(PROFILES,36):
 sustained=profile in ('Ward','Hindrance','Boon')
 case(f'RP02-{j:02}',f'{profile} preserves its exact concentration tag',[prep(profile=profile),rel()],[at('lastResult','release-committed'),at('state.concentration',{'id':'hold-A','state':'sustained'} if sustained else None),at('state.counts.history',1),at('state.counts.permissions',1)],qualification='Tests continuation of one burden, not this profile\'s actual payload/duration/world integration. Original profile text and source-specific earlier deadlines remain controlling.')

def lookup(j,path):
 for k in path.split('.'):
  j=j[int(k)] if isinstance(j,list) else j[k]
 return j

def run_case(c,policy):
 m=ReadyPolicyReference(policy=policy,owns_mirrorsage=c['ownsMirrorsage'])
 for k,v in c['initialOverrides'].items():setattr(m,k,copy.deepcopy(v))
 initial=m.snapshot();trace=[];results=[]
 for e in c['events']:
  before=m.snapshot();meth=e['method'];args=e.get('arguments',{})
  if meth=='fixture_json_roundtrip':m=ReadyPolicyReference.restore_fixture(json.loads(json.dumps(m.snapshot())));res='fixture-restored'
  elif meth=='fixture_corrupt_preparation_receipt':m.feat_rounds['N']='corrupt';res='fixture-corrupted'
  else:res=getattr(m,meth)(**args)
  results.append(res);trace.append(dict(event=copy.deepcopy(e),before=before,result=res,after=m.snapshot()))
 return dict(initial=initial,trace=trace,results=results,lastResult=results[-1],state=m.snapshot())

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();out=Path(a.output).resolve();root=Path(__file__).resolve().parents[1]
 if out==root or root in out.parents:raise SystemExit('Use a new report path outside the bundle')
 if out.exists():raise SystemExit('Report already exists; preserve evidence')
 result=[];failure=[];checks=0
 for c in CASES:
  new=run_case(c,'preparation-only');old=run_case(c,'historical-both-rounds');assertions=[]
  for x in c['expected']:
   actual=lookup(new,x['path']);ok=actual==x['value'];checks+=1
   assertions.append(dict(**x,actual=actual,passed=ok))
   if not ok:failure.append(dict(case=c['id'],**assertions[-1]))
  result.append(dict(**c,selected=new,historicalCounterfactual=old,assertions=assertions,
     classification='ISOLATED_SUPPLIED_PREDICATE_SPECIFICATION_NOT_GAME_RUNTIME',engineExecuted=False))
 report=dict(policy='COPY-READY-ALLOWANCE-02',caseCount=len(CASES),assertionCount=checks,failures=failure,
   semantics='Historical counterfactual is an explicitly implemented comparison branch in this isolated reference; it is not a replay of project code. Full original historical examples/tests are preserved separately.',
   gameEngineImports=0,gameRuntimeTests=0,actualPayloadImplementations=0,cases=result)
 with out.open('x',encoding='utf-8') as f:json.dump(report,f,ensure_ascii=False,indent=2);f.write('\n')
 print(json.dumps(dict(cases=len(CASES),assertions=checks,failures=len(failure))))
 if failure:raise SystemExit(1)
if __name__=='__main__':main()
