"""Independent fresh serialized-data checks. Never imports supplied code or runs gameplay."""
from pathlib import Path
import json,hashlib,copy,collections,sys
D=Path(__file__).parent;S=D/(sys.argv[1] if len(sys.argv)>1 else 'time5-return01');corrected=S.name=='time5-corrected-127'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def dump(x):return (json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode()
def sha(b):return hashlib.sha256(b).hexdigest()
checks=[];findings=[];counts=collections.Counter()
def check(test,label,detail=None):
 checks.append({'check':label,'pass':bool(test)})
 if not test:findings.append({'check':label,'detail':detail})
def ptr(x,s):
 for k in s.strip('/').split('/'):
  k=k.replace('~1','/').replace('~0','~');x=x[int(k)] if isinstance(x,list) else x[k]
 return x
def parent(x,s):
 p=s.rsplit('/',1);return (ptr(x,p[0]) if p[0] else x),p[1]
for f in read(S/('CURRENT_MANIFEST_127.json' if corrected else 'MANIFEST.json'))['files']:
 b=(S/f['path']).read_bytes();check(len(b)==f['bytes'] and sha(b)==f['sha256'],'manifest/'+f['path'])
 if f['path'].endswith('.json'):read(S/f['path'])
m=read(S/'MODEL.json');b=read(S/'history/ORIGINAL_CANDIDATE.json');orig=copy.deepcopy(b)
ops=read(S/'EXACT_OPERATIONS_FROM_SOURCE.json')['operations']
for op in ops:
 p,k=parent(b,op['pointer']);check(k not in p,'add absent/'+op['pointer']);p[k]=copy.deepcopy(ptr(m,op['afterReference']['pointer']))
check(b==m and dump(b)==(S/'MODEL.json').read_bytes(),'complete forward model bytes')
for op in reversed(ops):p,k=parent(b,op['pointer']);del p[k]
check(b==orig and dump(b)==(S/'history/ORIGINAL_CANDIDATE.json').read_bytes(),'complete inverse original bytes')
for field,file,key in [('selectedCurrentCases124','CASEBOOK.json','cases'),('selectedSharedRules124','SHARED_RULES.json',None),('selectedQuestionDispositions124','QUESTION_DISPOSITIONS.json',None),('selectedHoldRegister124','HOLD_REGISTER.json','holds'),('selectedOriginalScenarioDispositions124','ORIGINAL_SCENARIO_DISPOSITIONS.json',None),('selectedActorTemplates124','ACTOR_TEMPLATES.json',None)]:
 x=read(S/file);x=x[key] if key else x
 if field=='selectedOriginalScenarioDispositions124':x=x['scenarios']
 check(m[field]==x,'mirror/'+field)
procs=read(S/'PROCEDURES.json')['spells']
check([r['selectedOperationalProcedure124'] for r in m['records']]==procs,'all five procedure mirrors')
for i,p in enumerate(procs):
 check(p['completeNativeSourceAndAccess']==m['records'][i]['completeCurrentCatalogSourceAndAccess'],'native source/access/'+p['id'])
 check(bool(p['procedure']) and all(x in {y['id'] for y in m['selectedSharedRules124']} for x in p['sharedRuleIds']),'complete procedure/shared refs/'+p['id'])
ts=read(S/'FINAL_CASE_TIMESTAMP_OPERATIONS.json');x=read(S/ts['baseline']['file']);before=copy.deepcopy(x)
for op in ts['operations']:
 p,k=parent(x,op['pointer']);check(p[k]==op['before'],'timestamp before/'+op['pointer']);p[k]=op['after']
check(dump(x)==((D/'time5-return01' if corrected else S)/'CASEBOOK.json').read_bytes(),'historical timestamp forward complete bytes')
for op in reversed(ts['operations']):p,k=parent(x,op['pointer']);p[k]=op['before']
check(x==before and dump(x)==(S/ts['baseline']['file']).read_bytes(),'timestamp inverse complete bytes')
caseids=set()
def walkobs(x):
 if isinstance(x,dict):
  yield x
  for v in x.values():yield from walkobs(v)
 elif isinstance(x,list):
  for v in x:yield from walkobs(v)
def inspect(c):
 cid=c['id'];counts['cases']+=1;check(cid not in caseids,cid+'/unique case');caseids.add(cid)
 prev=c['initialState'];evts=set()
 for n,e in enumerate(c['timeline']):
  counts['events']+=1;tag=cid+'/'+str(n);be=e['before'];af=e['after'];obs=e['observations']
  check(prev==be,tag+'/full-state continuity');prev=af
  check(e['id'] not in evts,tag+'/unique event');evts.add(e['id'])
  check(be['time']<=e['time']==af['time'],tag+'/clock continuity')
  for sn,st in [('before',be),('after',af)]:
   counts['states']+=1
   for aid,a in st['actors'].items():
    if 'maxHp' not in a:continue
    check(0<=a['hp']<=a['maxHp'] and 0<=a['rp']<=a['maxRp'] and a['tempHp']>=0 and a['dissonance']>=0,tag+'/'+sn+'/'+aid+'/resource caps')
    check(not(a['stable'] and a['dying']) and (a['alive'] or not(a['stable'] or a['dying'])),tag+'/'+sn+'/'+aid+'/life state')
    check(not (a['stable'] or a['dying']) or a['hp']==0,tag+'/'+sn+'/'+aid+'/zero HP life')
    check(len(a['wounds'])<=3,tag+'/'+sn+'/'+aid+'/wound cap')
  new=[v for k,v in af['castLedger'].items() if k not in be['castLedger']]
  for cast in new:
   counts['casts']+=1;a=be['actors'][cast['caster']];z=af['actors'][cast['caster']];rank=cast['rank'];hist=cast['castingHistory'];fam=cast['family']
   native=0 if rank==0 else 1 if rank<=5 else 2
   exemption=a['class']=='Wizard' and fam not in a['preparedFamiliesUsed']
   refrain=min(3,a['refrain']+1) if a['lastSpell']==fam else 0
   check(hist['base']==native,tag+'/native rank Dissonance',[hist,native])
   check(hist['wizardExemption']==exemption,tag+'/actual first distinct exemption',[hist,exemption])
   check(hist['refrain']==refrain and hist['dissonanceAdded']==(0 if exemption else native)+refrain,tag+'/Dissonance arithmetic',[hist,refrain])
   check(z['dissonance']==a['dissonance']+hist['dissonanceAdded'],tag+'/Dissonance state')
   check(z['rp']==a['rp']-cast['actualPaid'] and z['hp']==a['hp']-cast['hpPaid'],tag+'/paid resource state')
   check(cast['actualPaid']==cast['baseRp']+cast['surcharge'],tag+'/paid surcharge arithmetic')
   check(z['lastSpell']==fam and z['refrain']==refrain,tag+'/chronological family state')
   if a['class']=='Wizard':check(fam in z['preparedFamiliesUsed'],tag+'/prepared-family mark')
   if cast['grant']=='ordinary':
    check(cast['baseRp']==[0,2,3,5,7,10,13,17,21,26][rank],tag+'/ordinary rank price')
    check(cast['spellId'] in a['prepared'] or rank==0,tag+'/ordinary preparation')
   ab=a.get('abilities',{});lim=max(4,2+a.get('pb',0)+max(0,(ab.get('INT',10)-10)//2))
   surcharge=0 if rank==0 else 3 if a['dissonance']>=lim+6 else 2 if a['dissonance']>=lim+3 else 1 if a['dissonance']>=lim else 0
   check(cast['surcharge']==surcharge,tag+'/precast surcharge',[a['class'],lim,surcharge])
  for d in walkobs(obs):
   if {'raw','resolved','tempAbsorbed','normalHpLost','overkill','recipient'}<=d.keys():
    counts['damageRecords']+=1
    check(d['resolved']==d['tempAbsorbed']+d['normalHpLost']+d['overkill'],tag+'/damage allocation',d)
    check(min(d['raw'],d['resolved'],d['tempAbsorbed'],d['normalHpLost'],d['overkill'])>=0,tag+'/damage nonnegative')
   if {'die','modifier','total'}<=d.keys():check(d['die']+d['modifier']==d['total'],tag+'/d20 arithmetic',d)
   if {'total','DC','success'}<=d.keys():check(d['success']==(d['total']>=d['DC']),tag+'/save success',d)
 check(prev==c['finalState'],cid+'/complete final state')
 for branch in c['branches']:inspect(branch)
for c in read(S/'CASEBOOK.json')['cases']:inspect(c)
if corrected:
 cb=read(S/'CASEBOOK.json')
 for row in read(S/'CASE_DISPOSITIONS.json')['cases']:
  ca=ptr(cb,row['completeCase']['pointer']);h=sha(json.dumps(ca,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
  check(h==row['completeCase']['canonicalObjectSha256'],'current case hash/'+row['id'])
 ts=cb['cases'][4];draw=next(e for e in ts['timeline'] if e['time']==12.3);sigil=next(e for e in ts['timeline'] if e['time']==24.01)
 check(draw['after']['actors']['C']['gear']['book']['heldBy']=='right','book held before departure')
 check(sigil['before']['time']==24 and sigil['before']['actors']['C']['gear']['book']['location']=='carried-open','immediate BA follows mandatory START with already open book')
 check(not sigil['before']['actors']['C']['ordinaryInteractionUsed'],'no intervening return interaction')
 for case,expected in [(cb['cases'][0]['branches'][1],[20,-3,3]),(cb['cases'][8]['branches'][0],[15,3,3])]:
  e=next(e for e in case['timeline'] if e['observations'].get('spellId')=='antimagic-field-lesser');p=e['observations']['preparation'];point=p['center'];source=p['sourcePoint']
  check(point==expected and sum((x-y)**2 for x,y in zip(point,source))==49,case['id']+'/clear native7ft selection')
  for aid,a in e['before']['actors'].items():
   pos=a['position'];w,d,h=a['body']['extentFeet'];lo=[pos[0]-w/2,pos[1]-d/2,pos[2]];hi=[pos[0]+w/2,pos[1]+d/2,pos[2]+h]
   check(not all(lo[i]<point[i]<hi[i] for i in range(3)),case['id']+'/point outside '+aid+' interior')
 for case in [cb['cases'][8],cb['cases'][8]['branches'][0]]:
  cast=case['finalState']['castLedger']['PAY'];point=cast['preparation']['bodyCenteredArea'];check(point==[12.5,0,3],case['id']+'/visible front-surface load point')
  check(point[0]<20 and point[0]==case['initialState']['actors']['R']['position'][0]-2.5,case['id']+'/native range and boundary')
result={'id':'TIME5-INDEPENDENT-DATA-INSPECTION-127','folder':S.name,'scope':'Fresh static file, reconstruction, state, native-cast and arithmetic checks. Not runtime or a replacement for semantic review.','checks':len(checks),'counts':dict(counts),'findings':findings,'results':checks}
(D/('TIME5_CORRECTED_DATA_CHECKS_127.json' if corrected else 'TIME5_FINAL_DATA_CHECKS_127.json')).write_bytes(dump(result));print(json.dumps({k:v for k,v in result.items() if k!='results'},indent=2))
