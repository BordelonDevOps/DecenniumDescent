#!/usr/bin/env python3
"""Read-only DI7 source/reference verification; no gameplay or source mutation.
Run: python di7_reference_checks.py --archive DD_DI7_Joint_Review_01.zip --output results.json
Place beside the supplied register and exact corrections. Python standard library only.
"""
from __future__ import annotations
import argparse, copy, hashlib, io, json, math, zipfile
from pathlib import Path
from fractions import Fraction as F

EXPECTED_SHA='9ca5cd879b951dc3d23c2cf2815814db6dea1e064ad1779cd34d2383b03eb576'
BASE='DescentReviewChanges/ReviewBible/'
RANK_PRICE=[0,2,3,5,7,10,13,17,21,26]
def sha(b:bytes)->str:return hashlib.sha256(b).hexdigest()
def canonical(x:object)->str:return sha(json.dumps(x,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode())
def ptr(x:object,p:str):
 for token in p.strip('/').split('/'):
  token=token.replace('~1','/').replace('~0','~')
  if token:x=x[int(token)] if isinstance(x,list) else x[token]
 return x
def setptr(x,p,value):
 toks=p.strip('/').split('/'); a=x
 for tok in toks[:-1]:a=a[int(tok)] if isinstance(a,list) else a[tok]
 key=int(toks[-1]) if isinstance(a,list) else toks[-1];a[key]=copy.deepcopy(value)
def strict_int(x,minimum=0):
 if type(x) is not int or x<minimum:raise ValueError('Requires finite integral source value, not bool/coercion')
 return x
def quote(rank:int,dissonance:int,limit:int,armor:int=0)->int:
 strict_int(rank);strict_int(dissonance);strict_int(limit,1);strict_int(armor)
 if rank>9:raise ValueError('Rank outside ordinary table')
 if rank and dissonance>=limit+6:raise ValueError('Ranked cast blocked')
 surcharge=0 if rank==0 or dissonance<limit else (1 if dissonance<limit+3 else 2)
 return RANK_PRICE[rank]+surcharge+armor

def history(d:int,last:str|None,repeat:int,name:str,rank:int,waive_base:bool=False):
 n=min(3,repeat+1) if last==name else 0
 base=0 if waive_base or rank==0 else 1 if rank<=5 else 2
 return d+base+n,name,n

def plan_fate(rp=48,d=0,limit=11,child_rank=1,last=None,repeat=0,outer_first=True):
 # Pure preflight reference; no supplied world/ability/counter premises authenticated.
 outer=quote(7,d,limit);d1,n1,r1=history(d,last,repeat,'fate-echo',7,outer_first)
 child=quote(child_rank,d1,limit);d2,n2,r2=history(d1,n1,r1,'copied-payload',child_rank)
 if rp<outer+child:raise ValueError('Composite unaffordable')
 return {'outer':outer,'child':child,'remaining':rp-outer-child,'dAfterOuter':d1,'dAfterChild':d2,'last':n2,'repeat':r2}

def task_counter(natural:int,mod:int,rank:int):
 strict_int(natural,1)
 if natural>20:raise ValueError('d20 required')
 dc=10+2*rank;total=natural+mod
 degree=3 if total>=dc+10 else 2 if total>=dc else 0 if total<=dc-10 else 1
 if natural==20:degree=min(3,degree+1)
 if natural==1:degree=max(0,degree-1)
 return degree>=2

def echo_age(original:F,commit:F,already_resolved=True,copy_descendant=False,rank=1,activation='Action'):
 return (F(0)<=commit-original<=F(18) and already_resolved and not copy_descendant and type(rank)is int and 0<=rank<=7 and activation in ('Action','Bonus Action'))

def suggest(base:tuple[int|None,int|None],caster:tuple[int|None,int|None]):
 out={}
 for i,(a,b) in enumerate(zip(base,caster)):
  if a is not None and b is not None and a!=b:out[str(i)]=a+(1 if b>a else -1)
 return out

def effective(base,suggestion:dict,purge:bool):
 if purge and all(x is not None for x in base):return (0,0)
 return tuple(suggestion.get(str(i),x) for i,x in enumerate(base))

class Ward:
 """Conditional event-key reference, not event discovery or a damage engine."""
 def __init__(self,start=F(0)):
  self.deadline=F(start)+60;self.remaining=2;self.covered=set();self.alive=True
 def event(self,key,now,*,suppressed=False,qualifies=True,post_defense_transfer=False):
  if not self.alive or F(now)>=self.deadline or suppressed or not qualifies or post_defense_transfer:return False
  if key in self.covered:return True
  if self.remaining<=0:return False
  self.remaining-=1;self.covered.add(key);return True
 def finish(self,key):
  self.covered.discard(key)
  if self.remaining==0 and not self.covered:self.alive=False

def finite_prevention(amount,covered,post_defense_transfer=False):
 strict_int(amount)
 return amount if post_defense_transfer or not covered else 0

def redact(records):
 # Authoritative input premises assumed; hidden existence must not leak IDs/counts.
 out=[]
 for row in records:
  if row['existenceProtected']:continue
  fields={k:('Indeterminate' if k in row['protectedFields'] or v is None else v) for k,v in row['fields'].items()}
  out.append(fields)
 return out

def cone_point(d,y,z=0):
 d,y,z=F(d),F(y),F(z)
 return 0<d<=60 and y*y+z*z<=d*d/4

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--archive',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
 out=[]
 def ck(name,ok,category='source/static'):
  out.append({'id':len(out)+1,'category':category,'name':name,'pass':bool(ok)})
 def ref(name,actual,expected):ck(name,actual==expected,'executed bounded reference arithmetic/state projection')
 def reject(name,fun):
  try:fun()
  except (ValueError,TypeError,KeyError):ck(name,True,'executed bounded rejection')
  else:ck(name,False,'executed bounded rejection')
 raw=args.archive.read_bytes();ck('Exact archive bytes',len(raw)==5899968);ck('Exact archive SHA256',sha(raw)==EXPECTED_SHA)
 if sha(raw)!=EXPECTED_SHA:raise SystemExit('Wrong archive; refused verification of another submission')
 with zipfile.ZipFile(args.archive) as z:
  names=z.namelist(); ck('No duplicate ZIP entries',len(names)==len(set(names)))
  m=json.loads(z.read('PACKAGE_MANIFEST.json'));ck('Exactly58 declared payloads',len(m)==58)
  ck('ZIP has exactly payloads+manifest',set(names)==set(m)|{'PACKAGE_MANIFEST.json'})
  for path,v in m.items():
   b=z.read(path);ck(path+' bytes',len(b)==v['bytes']);ck(path+' SHA256',sha(b)==v['sha256'])
  I=json.loads(z.read('CURRENT_DIVINATION_RANK7_REVIEW_INPUT.json'))
  old=json.loads(z.read(BASE+'data/director/spell_proposals/divination_rank7.json'))
  cat=json.loads(z.read(BASE+'data/public/spell_playtests/catalog.json'));cs={c['id']:c for c in cat['spells']}
  core=json.loads(z.read(BASE+'data/public/Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json'))
  index=json.loads(z.read(BASE+'data/public/spell_playtests/authored_review_index.json'))
  ck('Current authored counts412/436 preserved',index['authoredCounts']=={'reviewed':412,'pending':436})
  ck('Seven unchanged complete proposed records',I['records']==old['records'] and len(I['records'])==7)
  ck('Fourteen unchanged joint issues',I['explicitJointIssues']==old['explicitJointIssues'] and len(I['explicitJointIssues'])==14)
  ck('Eight book bindings preserved',I['originalBookBindings']==old['originalBookBindings'] and len(I['originalBookBindings'])==8)
  ck('Fourteen original authored examples',sum(len(x['workedCases']) for x in I['records'])==14)
  ck('Exactly46 current source bindings',len(I['sourceFiles'])==46)
  for p,v in I['sourceFiles'].items():ck('Current source '+p,sha(z.read(p))==v['sha256'] and len(z.read(p))==v['bytes'])
  expected={c:{'rank':7,'minimumClassLevel':n,'school':'Divination','baseRpCost':17} for c,n in [('Cleric',13),('Wizard',13),('Mirrorsage',19),('Shaman',19)]}
  for x in I['records']:
   sid=x['spellId'];src=x['fullSourceAndCurrentAccessRecord']
   ck(sid+' full source equals actual catalog',src==cs[sid]);ck(sid+' canonical source hash',canonical(src)==x['sourceRecordSha256'])
   ck(sid+' four exact access rows',src['classAccess']==expected)
   ck(sid+' still null/pending',src['operational'] is None and src['status']=='blocked-pending-operational-review')
   for e in src['source']['coreEntries']:ck(sid+' actual Core entry',core['spells'][e['index']]==e['original'])
  for x in I['completeClassComparisons']:
   ck(x['path']+' full current class parity',json.loads(z.read(x['path']))==x['completeCurrentEnvelope'])
  for p,v in I['currentGoverningDocuments'].items():ck(p+' complete current guide parity',io.StringIO(z.read(p).decode('utf-8'),newline=None).read()==v['fullCurrentText'])
  current_changed={p for p in I['sourceFiles'] if I['sourceFiles'][p]!=I['historicalSourceFiles'][p]}
  ck('Only two declared rebased source bindings',current_changed=={BASE+'data/director/higher_spell_operating_proposal_index.json',BASE+'data/public/class_playtests/ranger.json'})
  ck('Receipt-only data unchanged',I['completeUntouchedDeferredReceipts']==old['completeUntouchedDeferredReceipts'])
  ck('Receipt spell not operative',cs['planar-summons-greater']['operational'] is None)
  for c in I['completeCurrentCounterparts']:
   ck(c['id']+' current source catalog equality',cs[c['id']]==c['currentSourceCatalogRecord'])
   a=c['completeCurrentAuthoredRecord']; status=c['currentAuthoredIndexEntry']['authoredStatus']
   ck(c['id']+' source-qualified review status',(status=='reviewed-authored-operational-playtest' and isinstance(a['operational'],dict)) or (status=='pending-authored-procedure' and a['operational'] is None))
  ck('Wizard13 actual RP maximum48',core['caster_pools']['Wizard'][12]==48)
  ck('Cleric13 actual RP maximum36',core['caster_pools']['Cleric'][12]==36)
  # Check proposed descendant substitutions and inverse, not approval metadata.
  home=Path(__file__).resolve().parent
  operations=json.loads((home/'EXACT_DI7_CORRECTIONS.json').read_text());register=json.loads((home/'DI7_SOURCE_DECISION_REGISTER.json').read_text())
  d=copy.deepcopy(I)
  for op in operations['changes']:
   if 'recordGuard'in op:ck(op['pointer']+' identity guard',ptr(d,op['recordGuard']['pointer'])==op['recordGuard']['equals'])
   ck(op['pointer']+' old value guard',ptr(d,op['pointer'])==op['old'])
   setptr(d,op['pointer'],op['replacement'])
  for n,row in enumerate(register['records']):
   ck(row['spellId']+' full replacement/procedure equality',d['records'][n]['procedure']==row['procedure'])
   ck(row['spellId']+' full replacement/example equality',d['records'][n]['workedCases']==row['workedCases'])
   for k in I['records'][n]:
    if k not in ['procedure','workedCases']:ck(row['spellId']+' preserved '+k,d['records'][n][k]==I['records'][n][k])
  for k in I:
   if k not in ['sharedProposal','records']:ck('Preserved whole input '+k,d[k]==I[k])
  ck('Shared original status and deferred boundary unchanged',d['sharedProposal']['status']==I['sharedProposal']['status'] and d['sharedProposal']['deferredBoundary']==I['sharedProposal']['deferredBoundary'])
  for op in reversed(operations['changes']):setptr(d,op['pointer'],op['old'])
  ck('Exact object inverse to submission',d==I)
  ae=json.loads((home/'ALIGNMENT_SUGGESTION_AP_AS_01.json').read_text())
  for op in ae['operationsOnNewDerivedCopies']:
   ck('AP-AS source file hash '+op['path'],sha(z.read(op['path']))==op['sourceFileSha256'])
   if 'pointer'in op:ck('AP-AS exact original lower-card field',ptr(json.loads(z.read(op['path'])),op['pointer'])==op['old'])
   else:ck('AP-AS exact original guide paragraph',z.read(op['path']).decode().splitlines().count(op['old'])==1)
  ck('All14 issue IDs exact', {r['id'] for r in register['jointIssues']}=={r['id'] for r in I['explicitJointIssues']})
  ck('No eighth operative row',len(register['records'])==7 and all(r['spellId']!='planar-summons-greater' for r in register['records']))
 # Bounded calculations/state projections. Inputs explicitly conditional, not validated actors/events.
 ref('Common ordinary Limit Wizard13 INT4 PB5',max(4,2+5+4),11)
 ref('Ordinary rank7 no surcharge',quote(7,0,11),17)
 ref('Rank7 at Limit',quote(7,11,11),18)
 ref('Rank7 at Limit+3',quote(7,14,11),19)
 reject('Ranked blocked at Limit+6',lambda:quote(7,17,11))
 ref('Cantrip still no strain surcharge at high D',quote(0,30,11),0)
 ref('Actual nonproficient armor independently charges cantrip',quote(0,30,11,1),1)
 reject('Boolean rank rejected',lambda:quote(True,0,11));reject('Negative D rejected',lambda:quote(1,-1,11))
 ref('Fate first prepared matrix + copiedrank1',plan_fate(),{'outer':17,'child':2,'remaining':29,'dAfterOuter':0,'dAfterChild':1,'last':'copied-payload','repeat':0})
 ref('Previously spent matrix exemption does not become child exemption',plan_fate(outer_first=False)['dAfterChild'],3)
 high=plan_fate(d=9,outer_first=False);ref('Chronological child surcharge',high['child'],3);ref('Chronological total RP48→28',high['remaining'],28);ref('Chronological strain9→12',high['dAfterChild'],12)
 reject('Predictably blocked child rejects full forecast',lambda:plan_fate(d=15,outer_first=False))
 reject('RP18 cannot fund ordinary17+2 child',lambda:plan_fate(rp=18))
 ref('Countered outer commits17 only',48-17,31)
 ref('Countered child retains17+2',48-17-2,29)
 # A real later Reaction cast must not be overwritten on parent resume.
 d,last,rep=history(0,None,0,'fate-echo',7,True)
 d,last,rep=history(d,last,rep,'counterspell',3,True)
 d,last,rep=history(d,last,rep,'copied-payload',1)
 ref('Intervening own counter: latest history belongs to actual child', (d,last,rep),(1,'copied-payload',0))
 ref('Counter taskDC rank7',10+2*7,24);ref('Natural20 can counter DC24 withmod0',task_counter(20,0,7),True)
 ref('Natural1+23 vsDC24 is task failure after shift',task_counter(1,23,7),False)
 ref('Purge ordinary save total17 succeeds',17>=17,True)
 ref('Purge total16 fails',16>=17,False)
 for age,expected in [(F(0),True),(F(18),True),(F(18001,1000),False),(F(-1),False)]:ref('Echo age '+str(age),echo_age(F(0),age),expected)
 ref('Copy descendant is not original',echo_age(F(0),F(1),copy_descendant=True),False)
 ref('Unresolved original ineligible',echo_age(F(0),F(1),already_resolved=False),False)
 ref('Reaction mode excluded',echo_age(F(0),F(1),activation='Reaction'),False)
 ref('Rank null excluded',echo_age(F(0),F(1),rank=None),False)
 ref('Rank8 excluded',echo_age(F(0),F(1),rank=8),False)
 ref('Readiedoriginal uses prep0 not release5 freshness',echo_age(F(0),F(19)),False)
 ref('Legal original18 at own Fate preparation remains admitted snapshot',echo_age(F(0),F(18)),True)
 w=Ward();ref('Miss consumes first occurrence',w.event('attack1',5),True);ref('Remaining after miss',w.remaining,1)
 ref('Second occurrence admitted',w.event('attack2',6),True);ref('Remaining0 while occurrence live',w.remaining,0)
 ref('Same second occurrence still covered',w.event('attack2',6),True);ref('Third distinct interleaved occurrence not covered',w.event('attack3',6),False)
 w.finish('attack1');w.finish('attack2');ref('Depleted ward terminal',w.alive,False)
 w=Ward();ref('Beam1 immediate group',w.event('castA:immediate:B',5),True);ref('Beam2 same group',w.event('castA:immediate:B',5),True);ref('Beam3 same group',w.event('castA:immediate:B',5),True);ref('Three beams only one use',w.remaining,1)
 w.finish('castA:immediate:B');ref('Later tick distinct group',w.event('castA:tick1:B',11),True)
 w=Ward();ref('Nondamaging beneficial resolution qualifies',w.event('bless:immediate:B',1),True)
 ref('Suppressed event not covered',w.event('attack2',2,suppressed=True),False);ref('Suppression does not spend unuseduse',w.remaining,1)
 ref('Exact deadline excludes new event',w.event('attack3',60),False)
 ref('Canceled/notactual recipient excluded',w.event('none',3,qualifies=False),False)
 ref('Postdefense transfer skip excludes event',w.event('share',4,post_defense_transfer=True),False)
 ref('Postdefense exclusion retains ward use',w.remaining,1)
 w=Ward();ref('Positive premitigation share may qualify',w.event('root:pre:recipient',1),True)
 ref('Same occurrence share/direct cannot doublecharge',w.event('root:pre:recipient',1),True);ref('Share once',w.remaining,1)
 ref('Bloodbond20 splits5/15', (20//4,20-20//4),(5,15))
 ref('Ward on original share blocks15 not other5',(finite_prevention(20-20//4,True),finite_prevention(20//4,False)),(0,5));ref('Postdefense6 skip remains6',finite_prevention(6,True,True),6)
 ref('Forbidden maximumHP assignment not damage-prevented',max(0,26-15),11)
 ref('Cone forward boundary',cone_point(60,30),True);ref('Cone outside lateral',cone_point(60,F(301,10)),False);ref('Cone beyond axial',cone_point(F(601,10),0),False);ref('Cone origin excluded',cone_point(0,0),False)
 ref('6s lie window inclusive94 at100',F(100)-F(94)<=6,True);ref('93.999 outside window',F(100)-F(93999,1000)<=6,False)
 ref('Vision completion timestamp',F(1)+60,F(61));ref('Vision horizon30days from61',61+30*86400,2592061)
 ref('Vision interruption40 precedes61',40<61,True)
 base=(-1,-1);old_s=suggest(base,(1,1));ref('Suggestion LG towardCE',(old_s),{'0':0,'1':0})
 ref('Purge covers Suggestion',effective(base,old_s,True),(0,0))
 ref('Target baseline excludes temporaryNeutral',suggest(base,(-1,-1)),{})
 ref('Purged caster effectiveNeutral snapshot',suggest((1,1),(0,0)),{'0':0,'1':0})
 newbase=(0,1);ref('EndPurge reveals stilllive oldSuggestion',effective(newbase,old_s,False),(0,0))
 ref('EndSuggestion exposes true newerbase',effective(newbase,{},False),(0,1))
 ref('Undefined axis not fabricated asNeutral',effective((None,1),{},True),(None,1))
 red=redact([{'existenceProtected':True,'protectedFields':[],'fields':{'id':'SECRET','location':'sealed'}},{'existenceProtected':False,'protectedFields':['person'],'fields':{'activity':'convoy','person':'agent','time':None}}])
 ref('Protected existence omitted and fields independently unreadable',red,[{'activity':'convoy','person':'Indeterminate','time':'Indeterminate'}])
 ref('Projection contains no secret ID', 'SECRET' in json.dumps(red),False)
 ref('Century interval represented once',len([{'start':0,'end':100*365*86400,'id':'one-continuing-source'}]),1)
 summary={'archiveSha256':EXPECTED_SHA,'checks':len(out),'passed':sum(x['pass'] for x in out),'failed':sum(not x['pass'] for x in out),'categories':{c:sum(x['category']==c for x in out) for c in sorted({x['category'] for x in out})},'scope':'Executed read-only source/static checks and small conditional arithmetic/state projections only. Not full spell/counter/companion runtime or authentication of world facts. Does not rerun submitted historical142-check builder.','checksDetail':out}
 args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({k:v for k,v in summary.items() if k!='checksDetail'},indent=2))
 if summary['failed']:
  for x in out:
   if not x['pass']:print('FAIL',x['name'])
  raise SystemExit(1)
if __name__=='__main__':main()
