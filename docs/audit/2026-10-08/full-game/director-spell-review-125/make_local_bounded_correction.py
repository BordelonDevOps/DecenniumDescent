import copy,json,pathlib,hashlib,zipfile
D=pathlib.Path(r'C:\Github\DecenniumDescent\docs\audit\2026-10-08\full-game\director-spell-review-125'); src=D/'body8-checkpoint';out=D/'body8-local-correction';out.mkdir(exist_ok=True)
original=json.loads((src/'CASE_CHECKPOINT_08.json').read_text(encoding='utf-8')); cases=copy.deepcopy(original)
templates0=json.loads((src/'ACTOR_TEMPLATES.json').read_text(encoding='utf-8'));templates=copy.deepcopy(templates0)
changes=[]
def allcases(c):
 yield c
 for b in c.get('independentBranches',[]):yield from allcases(b)
def acquired(a):
 if a.get('class')=='Wizard' and a.get('classLevel')==2:
  a['automaticCards']=[x for x in a['automaticCards'] if x.get('completeCard',x).get('minimumClassLevel',0)<=2]
acquired(templates['W2'])
def repair_tree(v):
 if isinstance(v,dict):
  if 'sourcePoint' in v and 'center' in v and v.get('radius')==10:
   point=v.get('declaredSourcePoint')
   if point is None:
    for key in ['declaredLineOfEffect','lineOfEffect','centerPath']:
     path=v.get(key)
     if isinstance(path,list) and len(path)==2 and path[1]==v['center']:point=path[0];break
   if point is not None:v['sourcePoint']=copy.deepcopy(point)
  if v.get('massLb')==300 and v.get('Load')==20:
   v['massLb']=200
  if v.get('pounds')==310 and v.get('Load')==21:v['pounds']=210
  if v.get('grossPounds')==310 and v.get('grossLoad')==21:v['grossPounds']=210
  if v.get('location')=='ground' and v.get('custodian') is None and v.get('heldBy'):
   v['previousHeldByBeforeRelease']=copy.deepcopy(v['heldBy']);v['heldBy']=[]
  if v.get('id')=='crate' and v.get('custodian')=='T' and v.get('support')=='rated real floor':v['support']='Held by T through the declared two-handed grip; not floor-supported.'
  for a in list(v.values()):repair_tree(a)
 elif isinstance(v,list):
  for a in v:repair_tree(a)
observation_repairs=[]
def observations(v,st,path):
 if isinstance(v,dict):
  if isinstance(v.get('id'),str) and v['id'] in st['sources'] and len(set(v)&set(st['sources'][v['id']]))>3:
   actual=st['sources'][v['id']]
   if v!=actual:observation_repairs.append(path);v.clear();v.update(copy.deepcopy(actual))
  else:
   for k,a in v.items():observations(a,st,path+'/'+k)
 elif isinstance(v,list):
  for i,a in enumerate(v):observations(a,st,path+'/'+str(i))
for main in cases['cases']:
 for c in allcases(main):
  for a in c.get('actorDefinitions',{}).values():acquired(a)
  for k in ['initialState','expectedFinalState']:repair_tree(c[k])
  for e in c['timeline']:
   for k in ['before','after','observations']:repair_tree(e[k])
   observations(e['observations'],e['after'],c['id']+'/'+str(e['time'])+'/observations')
c=cases['cases'][8];assert c['id']=='TU6-03-A';last=c['timeline'][-1];assert last['time']==6.1
last['observations'].update({'oldCapacity':22,'restoredCapacity':18,'capacityUnits':'Load','grossLoadBeforeRelease':21,'grossPoundsBeforeRelease':210,'oldPoundCapacity':330,'restoredPoundCapacity':270,'limitingMeasure':'Load21 exceeds restored18; pounds210 remains below270. No overweight claim.'})
# Log exact reversible value changes; untouched historical source material stays in the original archive.
def diff(a,b,path,ops):
 if type(a)!=type(b):ops.append({'path':path,'before':a,'after':b});return
 if isinstance(a,dict):
  if a.keys()!=b.keys():ops.append({'path':path,'before':a,'after':b});return
  for k in a:diff(a[k],b[k],path+'/'+k.replace('~','~0').replace('/','~1'),ops)
 elif isinstance(a,list):
  if len(a)!=len(b):ops.append({'path':path,'before':a,'after':b});return
  for i,(x,y) in enumerate(zip(a,b)):diff(x,y,path+'/'+str(i),ops)
 elif a!=b:ops.append({'path':path,'before':a,'after':b})
def apply(doc,ops,reverse=False):
 r=copy.deepcopy(doc)
 for op in reversed(ops) if reverse else ops:
  parts=op['path'].strip('/').split('/');node=r
  for x in parts[:-1]:x=x.replace('~1','/').replace('~0','~');node=node[int(x)] if isinstance(node,list) else node[x]
  k=parts[-1].replace('~1','/').replace('~0','~');k=int(k) if isinstance(node,list) else k
  before,after=(op['after'],op['before']) if reverse else (op['before'],op['after'])
  assert node[k]==before;node[k]=copy.deepcopy(after)
 return r
receipt={'id':'BODY8-LOCAL-INDEPENDENT-CORRECTION-125','status':'LOCAL_REVIEW_CANDIDATE_PENDING_DIRECTOR_COMPARISON_NOT_ACCEPTED_NOT_APPLIED','scope':'Own fresh bounded data repairs only. No historical/supplied authoring code executed. Original recovered archive unchanged.','observationRepairs':observation_repairs,'files':[],'remaining':'Complete director model and question/hold/conference receipt still required; compare this local copy with director output before acceptance.'}
for name,before,after in [('CASEBOOK.json',original,cases),('ACTOR_TEMPLATES.json',templates0,templates)]:
 ops=[];diff(before,after,'',ops);assert apply(before,ops)==after;assert apply(after,ops,True)==before
 raw=(json.dumps(after,indent=2,ensure_ascii=False)+'\n').encode();(out/name).write_bytes(raw)
 (out/(name+'.operations.json')).write_text(json.dumps({'operations':ops,'forwardAndReverseExact':True},indent=2,ensure_ascii=False),encoding='utf-8')
 receipt['files'].append({'path':name,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'operations':len(ops),'forwardAndReverseExact':True})
(out/'RECEIPT.json').write_text(json.dumps(receipt,indent=2),encoding='utf-8');print(json.dumps(receipt,indent=2))
