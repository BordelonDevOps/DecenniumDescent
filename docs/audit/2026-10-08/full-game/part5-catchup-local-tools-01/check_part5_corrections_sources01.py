from pathlib import Path
import json,hashlib,copy,zipfile
from datetime import datetime,timezone
G=Path(r'C:\Github\DecenniumDescent'); A=G/'docs/audit/2026-10-08/full-game'; P=A/'part5-control-ready-corrections-01'
def raw(p):return Path('\\\\?\\'+str(p)).read_bytes()
def load(p):return json.loads(raw(p))
def sha(b):return hashlib.sha256(b).hexdigest()
def meta(p):
 b=raw(p);return {'path':str(p.relative_to(G)).replace('\\','/'),'bytes':len(b),'sha256':sha(b)}
def serial(v):return (json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
def parent(v,ptr):
 parts=[p.replace('~1','/').replace('~0','~') for p in ptr.split('/')[1:]]
 for p in parts[:-1]:v=v[int(p)] if isinstance(v,list) else v[p]
 return v,int(parts[-1]) if isinstance(v,list) else parts[-1]
ops=load(P/'POINTER_OPERATIONS.json')['operations']; bases=load(P/'ARTIFACT_BINDINGS.json')['files']; results=[]
assert len(ops)==22 and len(bases)==5
for row in bases:
 b=raw(P/row['baselineFile']);c=raw(P/row['correctedFile']);live=raw(G/row['repositoryPath'])
 assert len(b)==row['bytes'] and sha(b)==row['sha256'] and b==live
 assert len(c)==row['correctedBytes'] and sha(c)==row['correctedSha256']
 original=json.loads(b); changed=copy.deepcopy(original); fops=[o for o in ops if o['fileKey']==row['key']]
 for op in fops:
  assert op['repositoryPath']==row['repositoryPath']
  par,k=parent(changed,op['jsonPointer'])
  if op['op']=='replace':assert par[k]==op['before']
  else:assert op['op']=='add' and isinstance(par,dict) and k not in par and op['before'] is None
  par[k]=copy.deepcopy(op['after'])
 assert changed==json.loads(c) and serial(changed)==c
 for op in reversed(fops):
  par,k=parent(changed,op['jsonPointer']);assert par[k]==op['after']
  if op['op']=='add':del par[k]
  else:par[k]=copy.deepcopy(op['before'])
 assert changed==original and serial(changed)==b and raw(G/row['repositoryPath'])==live
 results.append({'fileKey':row['key'],'source':meta(G/row['repositoryPath']),'operationCount':len(fops),'fullForwardAndReverseByteEquality':True,'liveFileUnchanged':True})
cov=load(P/'SOURCE_COVERAGE.json');recovered=[]
for x in cov['unavailableBoundSources']:
 b=raw(G/x['path']);assert len(b)==x['bytes'] and sha(b)==x['sha256']; recovered.append({k:x[k] for k in ('path','bytes','sha256')})
archives=[]
for filename,prefix in [('DD_Control_15_Conference_12.zip','sources/'),('DD_Control_Illusion_Current_Acceptance_Context_01.zip','sources/')]:
 with zipfile.ZipFile(A/filename) as z:
  names=z.namelist();assert len(names)==len(set(names)) and z.testzip() is None
  assert all(not n.startswith(('/', '\\')) and '..' not in n.split('/') and '\\' not in n and ':' not in n for n in names)
  m=json.loads(z.read('MANIFEST.json'));files=m.get('files',m.get('sources'))
  assert files is not None
  for x in files:
   d=z.read(prefix+x['path']);assert len(d)==x['bytes'] and sha(d)==x['sha256']
  if filename=='DD_Control_15_Conference_12.zip':
   for x in cov['allBindings']:
    d=z.read(prefix+x['path']);assert len(d)==x['bytes'] and sha(d)==x['sha256']
   all54=True
  archives.append({'archive':meta(A/filename),'memberCount':len(names),'manifestFilesVerified':len(files),'all54ExactControlBindingsPresent':filename=='DD_Control_15_Conference_12.zip'})
index=meta(G/'DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json');assert index['sha256']=='6f9b86e21f6a69c7ba2469aba89d5907aa08da567226a2c4bd3ced9e09409857'
report={'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'scope':'Independent read-only byte/pointer/source verification, not substantive adoption, executable engine testing or correction application. No downloaded script executed.','correctionArchive':meta(A/'DD_Part5_Control_Ready_Corrections_01.zip'),'files':results,'operationCount':len(ops),'recoveredMissingSourceCount':len(recovered),'recoveredMissingSources':recovered,'conferenceArchives':archives,'historicalIndexBoundary':'Conference12 retains its actual480/368 historical index. Separate current acceptance context binds525/323,45 accepted Damage25/Persistent20 identities and173 interfaces. Preserve both; no silent baseline replacement.','authoredIndex':index,'sourceInformationDeleted':0,'rulesApplied':0,'runtimeTestsExecuted':0}
out=A/'PART5_CORRECTIONS_LOCAL_PREFLIGHT_01.json';assert not out.exists();out.write_bytes(serial(report))
print(json.dumps({'report':meta(out),'liveBaselinesMatched':len(results),'reversibleOperations':len(ops),'missingSourcesRecovered':len(recovered),'archives':archives,'rulesApplied':0},indent=2))
