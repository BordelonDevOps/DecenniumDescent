"""Independently preserve/replay returned data; never execute downloaded Python."""
from pathlib import Path,PurePosixPath
from datetime import datetime,timezone
from copy import deepcopy
import ast,hashlib,io,json,stat,zipfile
G=Path(r'C:\Github\DecenniumDescent');A=G/'docs/audit/2026-10-08/full-game'
W=Path(r'C:\Users\cbord\Documents\ChatGPT\Decennium Descent\audit_work')
IN=W/'DD_Rank7_Identity_Casting_5_Part5_Correction_Return_02.zip';OUT=A/IN.name
ROOT=A/'rank7-identity-casting5-part5-correction-return-02';REPORT=A/'RANK7_IDENTITY_CASTING5_PART5_CORRECTION_RETURN_02_LOCAL_PREFLIGHT.json'
def sha(b):return hashlib.sha256(b).hexdigest()
def enc(x):return (json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
def read(p):return json.loads(p.read_bytes())
def info(p):
 b=p.read_bytes();return {'path':p.relative_to(G).as_posix(),'bytes':len(b),'sha256':sha(b)}
def parent(d,ptr):
 parts=[x.replace('~1','/').replace('~0','~') for x in ptr.split('/')[1:]]
 for k in parts[:-1]:d=d[int(k)] if isinstance(d,list) else d[k]
 return d,int(parts[-1]) if isinstance(d,list) else parts[-1]
def main():
 native='GPT_PART5_RANK7_CORRECTION_RETURN_02_NATIVE.json'
 assert not any(p.exists() for p in [OUT,ROOT,REPORT,A/Path(__file__).name,A/native])
 checks=[]
 def ck(n,v):checks.append({'check':n,'passed':bool(v)});assert v,n
 def binding(raw,b,n):ck(n,len(raw)==b['bytes'] and sha(raw)==b['sha256'])
 def safe(z,label,limit=400_000_000):
  names=z.namelist();ck(label+' unique names',len(names)==len(set(names))==len(set(n.casefold() for n in names)))
  for i in z.infolist():
   p=PurePosixPath(i.filename);ck(label+' safe '+i.filename,not p.is_absolute() and '..' not in p.parts and '\\' not in i.filename and ':' not in i.filename and not stat.S_ISLNK(i.external_attr>>16) and not i.is_dir() and not i.flag_bits&1)
  ck(label+' bounded expansion',sum(i.file_size for i in z.infolist())<limit);ck(label+' CRC',z.testzip() is None)
 cpfile=A/'ACTIVE_AUTHORING_CHECKPOINT_RANK9_MATERIAL_FORGING_72.json';cp=read(cpfile)
 oldroot=A/'rank7-identity-casting5-part5-conference-return-01'
 protected=[cpfile,G/'DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json']
 protected += [G/cp[k]['path'] for k in ['currentWorkQueue','currentAuthoredIndex','currentAcceptedInterfaceRegistry','decisionLedger']]
 protected += [G/b['path'] for b in cp['canonicalHelperBaselinesUnchanged']]
 protected += [p for p in oldroot.rglob('*') if p.is_file()]
 before={p:sha(p.read_bytes()) for p in protected}
 raw=IN.read_bytes();binding(raw,{'bytes':64667556,'sha256':'d063125b1b570230afa9cef56714efc26d011dd9ca0dd56c064d5473c85b63a1'},'Exact downloaded archive')
 with zipfile.ZipFile(io.BytesIO(raw)) as z:
  safe(z,'Correction Return02');payload={n:z.read(n) for n in z.namelist()}
 j=lambda n:json.loads(payload[n])
 man=j('MANIFEST.json');ck('73 members72 manifest files',len(payload)==73 and len(man['files'])==man['fileCount']==72)
 ck('Exact manifest membership',set(payload)=={'MANIFEST.json'}|{b['path'] for b in man['files']})
 for b in man['files']:binding(payload[b['path']],b,'Manifest '+b['path'])
 incoming_name='inputs/DD_Rank7_Identity_Casting5_Local_Corrections_01.zip';incoming=payload[incoming_name]
 ck('Full actual dispatched packet preserved',incoming==(A/Path(incoming_name).name).read_bytes())
 with zipfile.ZipFile(io.BytesIO(incoming)) as z:
  safe(z,'Local correction12 input');incoming_data={n:z.read(n) for n in z.namelist()}
 oldarchive=incoming_data['input/DD_Rank7_Identity_Casting_5_Part5_Conference_Return_01.zip']
 ck('Complete actual original Return01',oldarchive==(A/'DD_Rank7_Identity_Casting_5_Part5_Conference_Return_01.zip').read_bytes())
 with zipfile.ZipFile(io.BytesIO(oldarchive)) as z:
  safe(z,'Original Return01');olddata={n:z.read(n) for n in z.namelist()}
 history=j('HISTORY_INDEX.json');ck('All50 original manifest-bound files indexed',len(olddata)==51 and len(history['originalFiles'])==50)
 ck('Exact original history membership',set(olddata)=={'MANIFEST.json'}|{b['path'] for b in history['originalFiles']})
 ck('Original root manifest exact',olddata['MANIFEST.json']==(oldroot/'MANIFEST.json').read_bytes())
 for b in history['originalFiles']:
  binding(olddata[b['path']],b,'Original history '+b['path']);ck('Original body matches prior local '+b['path'],olddata[b['path']]==(oldroot/b['path']).read_bytes())
 ib=j('INPUT_BINDINGS.json');binding(payload[ib['archive']['path']],ib['archive'],'Original source archive bound')
 ck('Original source archive actual bytes',payload[ib['archive']['path']]==(A/Path(ib['archive']['path']).name).read_bytes())
 with zipfile.ZipFile(io.BytesIO(payload[ib['archive']['path']])) as z:
  safe(z,'Original complete source conference');ck('Original source candidate exact',z.read('CANDIDATE.json')==payload['baseline/CANDIDATE.json'])
  ck('68 complete original sources',len(ib['sourceChecks'])==ib['expectedSources']==68)
  for b in ib['sourceChecks']:
   data=z.read('sources/'+b['path']);binding(data,b,'Original source '+b['path']);ck('Actual unchanged source '+b['path'],data==(G/b['path']).read_bytes())
 cb=j('CORRECTION_INPUT_BINDINGS.json')
 for b in cb['localManifestSourceAndHistoryRecords']:binding(incoming_data[b['path']],b,'Complete input evidence '+b['path'])
 for n,data in payload.items():
  if n.startswith('sources/'):
   ck('Actual full supplemental source '+n,data==(G/n[len('sources/'):]).read_bytes());ck('Unchanged supplied supplemental source '+n,data==incoming_data[n])
 contexts=j('CONTEXT_BINDINGS.json');ck('Ten unchanged complete contexts',len(contexts)==10 and payload['CONTEXT_BINDINGS.json']==olddata['CONTEXT_BINDINGS.json'])
 for b in contexts:
  data=payload[b['path']];binding(data,b,'Context '+b['path']);ck('Context previous local exact '+b['path'],data==olddata[b['path']])
  anchor=b['originArchive'];ar=(A/anchor['name']).read_bytes();binding(ar,anchor,'Actual context archive '+anchor['name'])
  with zipfile.ZipFile(io.BytesIO(ar)) as z:ck('Actual context archive member '+b['member'],z.read(b['member'])==data)
 ck('Exact original model baseline',payload['baseline/RETURN01_MODEL.json']==olddata['MODEL.json'])
 def replay(name,count):
  plan=j(name);base=payload[plan['baseline']['path']];target=payload[plan['successor']['path']]
  binding(base,plan['baseline'],name+' baseline');binding(target,plan['successor'],name+' successor')
  ck(name+' count',len(plan['operations'])==plan['operationCount']==count);d=json.loads(base)
  for i,o in enumerate(plan['operations']):
   p,k=parent(d,o['pointer']);exists=0<=k<len(p) if isinstance(p,list) else k in p
   ck(name+' supported '+str(i),o['op'] in ['replace','add'] and (not isinstance(p,list) or o['op']=='replace'))
   ck(name+' before existence '+str(i),exists==o['beforeExists']);ck(name+' full before '+str(i),(p[k] if exists else None)==o['before']);p[k]=deepcopy(o['after'])
  ck(name+' forward exact bytes',enc(d)==target)
  for i,o in enumerate(reversed(plan['operations'])):
   p,k=parent(d,o['pointer']);ck(name+' reverse full after '+str(i),p[k]==o['after'])
   if o['beforeExists']:p[k]=deepcopy(o['before'])
   else:del p[k]
  ck(name+' reverse exact bytes',enc(d)==base)
 replay('EXACT_OPERATIONS_FROM_RETURN01.json',11);replay('EXACT_OPERATIONS_FROM_SOURCE.json',38)
 composed=j('EXACT_OPERATIONS_FROM_SOURCE.json')['operations'];incremental=j('EXACT_OPERATIONS_FROM_RETURN01.json')['operations']
 ck('Exact original27 prefix',composed[:27]==json.loads(olddata['EXACT_OPERATIONS_FROM_SOURCE.json'])['operations']);ck('Exact11 correction suffix',composed[27:]==incremental)
 art=j('ARTIFACT_OPERATIONS_FROM_RETURN01.json');ck('15 complete file replacements',len(art['operations'])==art['operationCount']==15)
 for o in art['operations']:
  ck('Supported complete replacement '+o['path'],o['op']=='replace_full_file' and o['encoding']=='utf-8')
  b=olddata[o['path']];a=payload[o['path']];binding(b,o['beforeBinding'],'Full artifact baseline '+o['path']);binding(a,o['afterBinding'],'Full artifact successor '+o['path'])
  ck('Complete original text retained '+o['path'],o['beforeText'].encode('utf-8')==b);ck('Complete successor text exact '+o['path'],o['afterText'].encode('utf-8')==a)
 old=json.loads(olddata['MODEL.json']);model=j('MODEL.json');cases=model['currentVectors']
 ck('Ten complete current case mirrors',len(cases)==10 and j('CASE_DISPOSITIONS.json')['cases']==j('evidence/worked_cases.json')==cases)
 ck('All39 independent branch IDs retained',sum(len(c['independentBranches']) for c in cases)==39 and [b['id'] for c in cases for b in c['independentBranches']]==[b['id'] for c in old['currentVectors'] for b in c['independentBranches']])
 ck('All original main IDs retained',[c['id'] for c in cases]==[c['id'] for c in old['currentVectors']])
 ck('Eight complete parent-case changes',sum(a!=b for a,b in zip(old['currentVectors'],cases))==8)
 for k in ['records','selectedSharedRules','selectedQuestionDispositions','questions','sourceBindings','riskCounts','conditionalBranchRegister','explicitHolds']:
  ck('Complete unchanged authority field '+k,model[k]==old[k])
 ck('Five spells24 questions11 original qualifications',len(model['records'])==5 and len(model['selectedQuestionDispositions'])==24 and len(model['conditionalBranchRegister'])==11)
 for f in ['SPELL_DISPOSITIONS.json','QUESTION_DISPOSITIONS.json','CLOCK_AND_BODY_MATRIX.json','DI7_COMPARISON.json','HOLD_REGISTER.json']:ck('Complete unchanged artifact '+f,payload[f]==olddata[f])
 ck('Exact full actor-accounting mirrors',j('ACTOR_FEATURE_ACCOUNTING.json')['profiles']==j('evidence/actor_profiles.json'))
 ck('No new rule/runtime/cosmology/deletion claims',model['newRuleAdoptions']==model['runtimeTestsExecuted']==model['cosmologyDecisions']==model['sourceInformationDeleted']==0 and not model['wholeGameComplete'])
 parsed=[]
 for n,b in payload.items():
  if n.endswith('.py'):ast.parse(b.decode('utf-8'));parsed.append(n);ck('Syntax only, never execute '+n,True)
 ROOT.mkdir();OUT.write_bytes(raw)
 for n,b in payload.items():
  p=ROOT/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b);ck('Complete extracted bytes '+n,p.read_bytes()==b)
 for p,h in before.items():ck('Protected original unchanged '+p.relative_to(G).as_posix(),sha(p.read_bytes())==h)
 (A/native).write_bytes((W/native).read_bytes());(A/Path(__file__).name).write_bytes(Path(__file__).read_bytes())
 result={'id':'RANK7-IDENTITY-CASTING5-CORRECTION-RETURN02-LOCAL-PREFLIGHT','recordedAtUtc':datetime.now(timezone.utc).isoformat(),
  'archive':info(OUT),'model':info(ROOT/'MODEL.json'),'nativeFinal':info(A/native),'assistantTurn':'da6b802d-c239-4e09-baef-694fa6346bd9',
  'checks':checks,'checkCount':len(checks),'failures':0,'sourceFiles':68,'contextFiles':10,'oldReturnMembersPreserved':51,'manifestFiles':72,
  'incrementalOperationsForwardAndReverse':11,'alternativeComposedOperationsForwardAndReverse':38,'fullArtifactReplacements':15,
  'caseInventory':{'main':10,'branches':39,'conditionalQualifications':11},'syntaxParsedOnly':parsed,
  'scope':'Full source/hash/manifest/history/mirror and exact reversible operation replay only. Three supplied corrections and three additional cadence repairs still require independent semantic review. No downloaded code executed,game engine invoked,acceptance increment or canonical application.',
  'acceptedButUnappliedUnchanged':39,'appliedCountsUnchanged':{'reviewed':525,'pending':323,'standalone':249,'interfaces':173},
  'runtimeTestsExecuted':0,'humanPlaytests':0,'sourceInformationDeleted':0,'implementationApplied':False}
 REPORT.write_bytes(enc(result));print(json.dumps({'report':info(REPORT),'archive':info(OUT),'model':info(ROOT/'MODEL.json'),'checks':len(checks),'failures':0}))
if __name__=='__main__':main()
