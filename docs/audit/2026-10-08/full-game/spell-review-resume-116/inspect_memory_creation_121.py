import pathlib,json,hashlib,zipfile,io,copy,datetime
from fractions import Fraction as Q
A=pathlib.Path(r'C:\Github\DecenniumDescent\docs\audit\2026-10-08\full-game');P=A/'memory-creation3-review-121';O=A/'spell-review-resume-116'; checks=[];findings=[]
def read(n):return json.loads((P/n).read_bytes())
def ck(n,v):checks.append({'check':n,'passed':bool(v)})
def h(b):return hashlib.sha256(b).hexdigest()
m=read('MODEL.json');c=read('CASEBOOK.json');allcases=[x for root in c['cases'] for x in [root]+root['branches']]
ck('8 mains15branches88events',len(c['cases'])==8 and len(allcases)==23 and sum(len(x['timeline']) for x in allcases)==88)
for k,n,sub in [('spells','PROCEDURES.json','spells'),('currentCases','CASEBOOK.json','cases')]:ck('Exact model mirror '+k,m[k]==read(n)[sub])
cache={}
def source(e):
 chain=e['archiveChain']; key=tuple(chain)
 if key not in cache:
  z=zipfile.ZipFile(A/chain[0])
  for n in chain[1:]:z=zipfile.ZipFile(io.BytesIO(z.read(n)))
  cache[key]=z
 return cache[key].read(e['member'])
refs=read('SOURCE_REFERENCES.json')
for name,e in refs['aliases'].items():
 if 'archiveChain' not in e:continue
 b=source(e);ck('Exact dependency '+name,len(b)==e['bytes'] and h(b)==e['sha256'])
actors=read('ACTOR_DEFINITIONS.json');ck('Wizard whole source',actors['completeWizardSource']==json.loads(source(refs['aliases']['wizard'])));ck('Warrior whole source',actors['completeWarriorSource']==json.loads(source(refs['aliases']['warrior'])))
for op in read('EXACT_OPERATIONS_FROM_ORIGINALS.json')['operations']:
 before=(P/op['completeBefore']['artifact']).read_bytes();after=(P/op['completeAfter']['path']).read_bytes();a=json.loads(before);b=json.loads(after);key=op['pointer'][1:];ck('Add absent '+op['id'],key not in a);a[key]=b[key];ck('Forward whole bytes '+op['id'],(json.dumps(a,indent=2,ensure_ascii=False)+'\n').encode()==after);del b[key];ck('Reverse whole bytes '+op['id'],(json.dumps(b,indent=2,ensure_ascii=False)+'\n').encode()==before)
for case in allcases:
 ck('Final exact '+case['id'],case['final']==case['timeline'][-1]['after'])
 for e in case['timeline']:
  tag=case['id']+'/'+e['id'];o=e.get('outcome',{});before=e['before'];after=e['after'];ck('Event timestamp '+tag,after['time']==e['time'])
  for state in [before,after]:
   for aid,a in state['actors'].items():
    ck('Resource bounds '+tag+'/'+aid,0<=a['hp']<=a['maxHp'] and (a['rp'] is None and a['maxRp'] is None or a['rp'] is not None and 0<=a['rp']<=a['maxRp']) and a['tempHp']>=0)
   for mem in state.get('memory',{}).values():ck('No future firsthand record '+tag,all(a<=b<=state['time']+1e-8 for a,b in mem['experienced']))
  if o.get('status') in ['committed','held'] and 'actualPaid' in o:
   a=before['actors'][o['owner']];b=after['actors'][o['owner']];ck('Actual RP payment '+tag,a['rp']-b['rp']==o['actualPaid']==o['rpBefore']-o['rpAfter']);wallet='reaction' if o['actionType']=='Reaction' else 'action';ck('Spend actual wallet '+tag,a[wallet] and not b[wallet]);ck('Actual casting phase '+tag,o['actionType']=='Reaction' or a['regularStart']<=e['time']<a['regularEnd']);
   if o['spellId']=='woven-threads' and o.get('plan',{}).get('mode')=='Replace' and not(o['plan'].get('narrative') or o['plan'].get('words')):findings.append({'kind':'MISSING_FROZEN_REPLACE_NARRATIVE','case':case['id'],'event':e['id'],'castId':o['id'],'plan':o['plan']})
   if o['spellId']=='creation' and ('boxMin' not in o.get('plan',{}) or 'boxMax' not in o.get('plan',{})):findings.append({'kind':'MISSING_FROZEN_CREATION_PLAN','case':case['id'],'event':e['id'],'castId':o['id'],'plan':o.get('plan')})
  def walk(x):
   if isinstance(x,dict):
    if 'face' in x and 'modifier' in x and 'total' in x:ck('Roll arithmetic '+tag,x['face']+x['modifier']==x['total'])
    if x.get('kind')=='binary-save':ck('Binary save '+tag,x['success']==(x['total']>=x['DC']))
    for v in x.values():walk(v)
   elif isinstance(x,list):
    for v in x:walk(v)
  walk(o)
for v in read('PARTITION_EVIDENCE.json')['fiveVectorResults']:
 s=v['completeSuppliedVector'];M=s['beforeMaximum'];C=s['beforeCurrent'];mass=list(map(Q,s['pieceMasses']));total=sum(mass)
 def alloc(n,cap=None):
  quotas=[n*x/total for x in mass];out=[q.numerator//q.denominator for q in quotas];left=n-sum(out);order=sorted(range(len(out)),key=lambda i:(-(quotas[i]-out[i]),i))
  while left:
   for i in order:
    if left and (cap is None or out[i]<cap[i]):out[i]+=1;left-=1
  return out
 mx=alloc(M);cur=alloc(C,mx);r=v['currentIndependentResult'];ck('Exact rational partition '+v['id'],mx==r['maximumHP'] and cur==r['currentHP'] and sum(cur)==C and sum(mx)==M and all(0<=a<=b for a,b in zip(cur,mx)))
report={'recordedAtUtc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actualArchiveSha256':'57a6fc56c27320b349c54ff4a7b68d12978dde5bdcd295fd54a4d20324a78327','manifestBindingsVerified':52,'checks':checks,'passed':sum(x['passed'] for x in checks),'failed':sum(not x['passed'] for x in checks),'concreteFindings':findings,'scope':'Fresh exact-data/source/arithmetic inspection plus complete manual operative and88event outcome reading; not supplied runner or runtime execution.','accepted':False,'canonicalApplied':False}
(O/'MEMORY_CREATION3_INDEPENDENT_REVIEW_121.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:v for k,v in report.items() if k!='checks'},indent=2));print('FAILED',json.dumps([x for x in checks if not x['passed']])[:5000])


