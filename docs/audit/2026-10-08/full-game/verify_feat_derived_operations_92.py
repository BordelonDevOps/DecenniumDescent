"""Independent reconstruction of the locally authored FT84 mirror operations."""
from pathlib import Path
from copy import deepcopy
from collections import defaultdict
from datetime import datetime, timezone
import json, hashlib, zipfile

G=Path(r'C:\Github\DecenniumDescent');A=G/'docs/audit/2026-10-08/full-game'
ROOT=A/'feat335-ft84-derived-review-92';REPORT=A/'FEAT335_FT84_DERIVED_MIRROR_RECONCILIATION_92.json'
OUT=A/'FEAT335_FT84_DERIVED_OPERATIONS_VERIFICATION_92.json';SAVED=A/Path(__file__).name
for p in [OUT,SAVED]:assert not p.exists(),str(p)
def sha(b):return hashlib.sha256(b).hexdigest()
def enc(v):return (json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode()
def info(p):
 b=p.read_bytes();return {'path':p.relative_to(G).as_posix(),'bytes':len(b),'sha256':sha(b)}
def load(b):return json.loads(b.decode('utf-8-sig'))
checks=[]
def ck(name,ok):
 checks.append({'check':name,'pass':bool(ok)});assert ok,name
report=load(REPORT.read_bytes());groups=defaultdict(list)
for op in report['newDerivedOperations']:groups[op['repositoryPath']].append(op)
ck('Eleven operations on eight derived mirrors',len(report['newDerivedOperations'])==11 and len(groups)==8)
def locate(obj,pointer):
 parts=[p.replace('~1','/').replace('~0','~') for p in pointer.split('/')[1:]]
 for part in parts[:-1]:obj=obj[int(part)] if isinstance(obj,list) else obj[part]
 return obj,int(parts[-1]) if isinstance(obj,list) else parts[-1]
results=[]
for rel,ops in groups.items():
 before=(ROOT/'before'/rel).read_bytes();after=(ROOT/'after'/rel).read_bytes()
 if rel.endswith('.json'):
  original=load(before);state=deepcopy(original)
  for op in ops:
   parent,key=locate(state,op['pointer'])
   if op['kind']=='json-add':ck(rel+' absent add '+op['pointer'],key not in parent)
   else:ck(rel+' exact before '+op['pointer'],parent[key]==op['before'])
   parent[key]=deepcopy(op['after'])
  ck(rel+' complete forward JSON bytes',enc(state)==after)
  for op in reversed(ops):
   parent,key=locate(state,op['pointer']);ck(rel+' exact inverse before '+op['pointer'],parent[key]==op['after'])
   if op['kind']=='json-add':del parent[key]
   else:parent[key]=deepcopy(op['before'])
  ck(rel+' complete inverse JSON values',state==original)
  inverse_exact=enc(state)==before
 else:
  state=before.decode('utf-8')
  for op in ops:
   if op['kind']=='exact-text-replace':
    ck(rel+' unique complete before text',state.count(op['before'])==1);state=state.replace(op['before'],op['after'],1)
   else:state+=op['after']
  ck(rel+' complete forward text bytes',state.encode()==after)
  for op in reversed(ops):
   if op['kind']=='exact-text-replace':
    ck(rel+' unique complete after text',state.count(op['after'])==1);state=state.replace(op['after'],op['before'],1)
   else:
    ck(rel+' exact appended suffix',state.endswith(op['after']));state=state[:-len(op['after'])]
  inverse_exact=state.encode()==before;ck(rel+' complete inverse text bytes',inverse_exact)
 results.append({'repositoryPath':rel,'operationCount':len(ops),'forwardWholeBytesExact':True,'inverseWholeValuesExact':True,'inverseDefaultSerializationBytesExact':inverse_exact,'originalByteRestoration':'Use the preserved complete before artifact for original formatting.'})
ck('New mirrors include no unrelated source mechanics',report['newRuleAdoptions']==0 and not report['canonicalImplementationApplied'])
ck('All three preexisting feat differences explicitly retained',len(report['preexistingPublicInternalProcedureDifferences'])==3)
ck('Preexisting FS08 public difference explicitly retained',report['preexistingPublicSharedDifference']['ruleId']=='FS-08')
archive=A/'DD_Feat335_Derived_Review_Candidate_92.zip'
with zipfile.ZipFile(archive) as z:
 manifest=load(z.read('MANIFEST.json'))
 ck('Archive exact member census',set(z.namelist())=={r['path'] for r in manifest['files']}|{'MANIFEST.json'})
 ck('Archive exact file bindings',all(len(z.read(r['path']))==r['bytes'] and sha(z.read(r['path']))==r['sha256'] for r in manifest['files']))
 ck('Archive report equals saved full report',z.read('RECONCILIATION.json')==REPORT.read_bytes())
for row in report['fullArtifactPlan']:
 ck('Source unchanged '+row['repositoryPath'],(G/row['repositoryPath']).read_bytes()==(ROOT/row['before']['path']).read_bytes())
result={'id':'FEAT335-FT84-DERIVED-OPERATIONS-VERIFICATION-92','recordedAtUtc':datetime.now(timezone.utc).isoformat(),'scope':'Own independent JSON/text operation reconstruction and archive/source fidelity; not gameplay semantic approval or engine execution.','report':info(REPORT),'archive':info(archive),'operations':results,'checks':checks,'passed':len(checks),'failed':0,'runtimeTestsExecuted':0,'canonicalApplied':False,'parent335Accepted':False,'sourceInformationDeleted':0}
payload=enc(result)
with SAVED.open('xb') as f:f.write(Path(__file__).read_bytes())
with OUT.open('xb') as f:f.write(payload)
print(json.dumps({'report':info(OUT),'checks':len(checks),'failed':0,'nonidenticalDefaultInverseSerializations':[r['repositoryPath'] for r in results if not r['inverseDefaultSerializationBytesExact']]},indent=2))
