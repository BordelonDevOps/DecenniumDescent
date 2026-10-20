"""Preserve full correction return and independently replay exact data operations.

No returned Python is executed or imported. No canonical rule is applied.
"""
from pathlib import Path,PurePosixPath
from datetime import datetime,timezone
import ast,copy,hashlib,io,json,stat,zipfile
G=Path(r'C:\Github\DecenniumDescent');A=G/'docs/audit/2026-10-08/full-game'
IN=Path(r'C:\Users\cbord\Downloads\DD_Rank8_Damage_6_Part5_Correction_Return_02.zip')
OUT=A/IN.name;ROOT=A/'rank8-damage6-part5-correction-return-02'
REPORT=A/'RANK8_DAMAGE6_PART5_CORRECTION_RETURN_02_LOCAL_PREFLIGHT.json'
def sha(b):return hashlib.sha256(b).hexdigest()
def enc(x):return (json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
def info(p):
 b=p.read_bytes();return {'path':p.relative_to(G).as_posix(),'bytes':len(b),'sha256':sha(b)}
def read(p):return json.loads(p.read_bytes())
def parent(d,ptr):
 parts=[v.replace('~1','/').replace('~0','~') for v in ptr.split('/')[1:]]
 for k in parts[:-1]:d=d[int(k)] if isinstance(d,list) else d[k]
 return d,int(parts[-1]) if isinstance(d,list) else parts[-1]
def main():
 assert not any(p.exists() for p in [OUT,ROOT,REPORT,A/Path(__file__).name])
 checks=[]
 def ck(n,v):checks.append({'check':n,'passed':bool(v)});assert v,n
 def binding(raw,b,label):ck(label,len(raw)==b['bytes'] and sha(raw)==b['sha256'])
 def safe(z,label):
  names=z.namelist();ck(label+' unique safe names',len(names)==len(set(names))==len(set(n.casefold() for n in names)))
  for i in z.infolist():
   p=PurePosixPath(i.filename)
   ck(label+' safe member '+i.filename,not p.is_absolute() and '..' not in p.parts and '\\' not in i.filename and ':' not in i.filename and not stat.S_ISLNK(i.external_attr>>16) and not i.is_dir())
  ck(label+' bounded expansion',sum(i.file_size for i in z.infolist())<100_000_000)
  ck(label+' CRC',z.testzip() is None)
 cpfile=A/'ACTIVE_AUTHORING_CHECKPOINT_RANK9_ELEMENTAL_PETS_69.json';cp=read(cpfile)
 protected=[cpfile,G/'DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json']
 protected += [G/cp[k]['path'] for k in ['currentWorkQueue','currentAuthoredIndex','currentAcceptedInterfaceRegistry','decisionLedger']]
 protected += [G/b['path'] for b in cp['canonicalHelperBaselinesUnchanged']]
 protected += [p for p in (A/'rank8-damage6-part5-conference-return-01').rglob('*') if p.is_file()]
 before={p:sha(p.read_bytes()) for p in protected}
 raw=IN.read_bytes();binding(raw,{'bytes':17408791,'sha256':'6678b1cbe5d02104b38b2cdb4eee4b1eec434dc7a05e60889ed7153ef2f730cb'},'Exact downloaded archive')
 with zipfile.ZipFile(io.BytesIO(raw)) as z:
  safe(z,'Correction return');payload={n:z.read(n) for n in z.namelist()}
 j=lambda n:json.loads(payload[n])
 man=j('MANIFEST.json');ck('99 members and98 manifest files',len(payload)==99 and len(man['files'])==man['fileCount']==98)
 ck('Exact manifest membership',set(payload)=={'MANIFEST.json'}|{b['path'] for b in man['files']})
 for b in man['files']:binding(payload[b['path']],b,'Manifest '+b['path'])
 oldroot=A/'rank8-damage6-part5-conference-return-01'
 oldfiles=[p for p in oldroot.rglob('*') if p.is_file()]
 ck('All40 previous return members preserved',len(oldfiles)==40)
 for p in oldfiles:
  n=p.relative_to(oldroot).as_posix();ck('Full original return member '+n,payload['history/return01/'+n]==p.read_bytes())
 ib=j('INPUT_BINDINGS.json');original=payload[ib['archive']]
 binding(original,ib,'Original source archive binding');ck('Original source archive equals actual local',original==(A/Path(ib['archive']).name).read_bytes())
 with zipfile.ZipFile(io.BytesIO(original)) as z:
  safe(z,'Original source archive')
  ck('Original candidate exact',z.read('CANDIDATE.json')==payload['baseline/CANDIDATE.json'])
  sources=j('SOURCE_BINDINGS.json')['originalFullSources'];ck('51 original source bindings',len(sources)==51 and sources==ib['sourceBindingsUnchanged'])
  for b in sources:
   data=z.read('sources/'+b['path']);binding(data,b,'Original source '+b['path']);ck('Current actual source '+b['path'],data==(G/b['path']).read_bytes())
 incoming=payload['input/DD_Rank8_Damage6_Local_Corrections_01.zip']
 ck('Exact full actually submitted correction archive',incoming==(A/'DD_Rank8_Damage6_Local_Corrections_01.zip').read_bytes())
 with zipfile.ZipFile(io.BytesIO(incoming)) as z:
  safe(z,'Submitted local correction packet')
  incoming_members={n:z.read(n) for n in z.namelist()}
 for n,data in payload.items():
  if n.startswith('local_evidence/'):
   relative=n[len('local_evidence/'):]
   if relative in incoming_members:ck('Exact local correction evidence '+relative,data==incoming_members[relative])
   else:raise AssertionError('Unmapped correction evidence '+n)
 context=j('CONTEXT_BINDINGS.json')['files'];ck('Eleven complete prior contexts',len(context)==11)
 for b in context:
  data=payload[b['file']];binding(data,b,'Context '+b['file'])
  ck('Context is exact prior local body '+b['file'],data==(oldroot/b['file']).read_bytes())
  ck('Actual source archive anchors present '+b['file'],bool(b['exactArchiveAnchors']))
  for anchor in b['exactArchiveAnchors']:
   ar=(A/anchor['archive']).read_bytes();binding(ar,{'bytes':anchor['archiveBytes'],'sha256':anchor['archiveSha256']},'Prior archive '+anchor['archive'])
   with zipfile.ZipFile(io.BytesIO(ar)) as z:body=z.read(anchor['member'])
   binding(body,anchor,'Prior context member '+anchor['member']);ck('Prior member matches context '+b['file'],body==data)
 def replay(name,expectedcount):
  ops=j(name);base=payload[ops['base']['file']];target=payload[ops['successor']['file']]
  binding(base,ops['base'],name+' base');binding(target,ops['successor'],name+' target')
  ck(name+' exact count',len(ops['operations'])==ops['operationCount']==expectedcount)
  d=json.loads(base)
  for i,o in enumerate(ops['operations']):
   p,k=parent(d,o['pointer']);exists=(0<=k<len(p)) if isinstance(p,list) else k in p
   ck(name+' supported operation '+str(i),o['op'] in ['replace','add'] and (not isinstance(p,list) or o['op']=='replace'))
   ck(name+' before existence '+str(i),exists==o['beforeExists']);ck(name+' before value '+str(i),(p[k] if exists else None)==o['before'])
   p[k]=copy.deepcopy(o['after'])
  ck(name+' forward exact bytes',enc(d)==target)
  for i,o in enumerate(reversed(ops['operations'])):
   p,k=parent(d,o['pointer']);ck(name+' reverse after value '+str(i),p[k]==o['after'])
   if o['beforeExists']:p[k]=copy.deepcopy(o['before'])
   else:del p[k]
  ck(name+' reverse exact bytes',enc(d)==base)
 replay('EXACT_OPERATIONS_FROM_RETURN01.json',17)
 replay('EXACT_OPERATIONS_FROM_SOURCE.json',54)
 ck('Composed37-operation historical prefix exact',j('EXACT_OPERATIONS_FROM_SOURCE.json')['operations'][:37]==j('history/return01/EXACT_OPERATIONS_FROM_SOURCE.json')['operations'])
 ck('Composed17-operation correction suffix exact',j('EXACT_OPERATIONS_FROM_SOURCE.json')['operations'][37:]==j('EXACT_OPERATIONS_FROM_RETURN01.json')['operations'])
 plans=j('ARTIFACT_OPERATIONS_FROM_RETURN01.json')['files'];ck('17 complete artifact replacements',len(plans)==17)
 for row in plans:
  op=row['operation'];b=payload[row['before']['path']];a=payload[row['after']['path']]
  binding(b,row['before'],'Artifact before '+row['before']['path']);binding(a,row['after'],'Artifact after '+row['after']['path'])
  if row['kind']=='json-full-value':
   ck('Full JSON before exact '+row['before']['path'],enc(op['before'])==b);ck('Full JSON after exact '+row['after']['path'],enc(op['after'])==a)
  else:
   ck('Supported text replacement '+row['after']['path'],row['kind']=='text-full-file')
   ck('Full text before exact '+row['before']['path'],op['before'].encode('utf-8')==b);ck('Full text after exact '+row['after']['path'],op['after'].encode('utf-8')==a)
 old=j('history/return01/MODEL.json');model=j('MODEL.json');cases=j('CASE_DISPOSITIONS.json')['allCases']
 ck('Full case mirror',cases==model['currentVectors'])
 ck('12 main and42 branch cases',len(cases)==12 and sum(len(c['independentBranches']) for c in cases)==42)
 ck('All original main IDs retained',[c['id'] for c in old['currentVectors']]==[c['id'] for c in cases])
 originalbranches={b['id'] for c in old['currentVectors'] for b in c['independentBranches']};branches={b['id'] for c in cases for b in c['independentBranches']}
 ck('Only one additional independent branch',branches-originalbranches=={'RD8-03-B-CONCENTRATION-FAIL'} and originalbranches<=branches)
 ck('Exactly four unchanged whole main objects',sum(a==b for a,b in zip(old['currentVectors'],cases))==4)
 ck('All six shared clauses unchanged',len(model['selectedSharedRules'])==6 and model['selectedSharedRules']==old['selectedSharedRules'])
 for i,(b,a) in enumerate(zip(old['records'],model['records'])):
  ck('All native record fields unchanged '+str(i),all(v==a[k] for k,v in b.items() if k!='procedure'))
  ck('Only Soul Pyre procedure changes '+str(i),(a['procedure']!=b['procedure'])==(a['spellId']=='soul-pyre'))
 ck('Original risks retained',model['riskCounts']==old['riskCounts']=={'B':4,'C':2})
 ck('No implementation or acceptance flags enabled',not model['runtimeImplemented'] and not model['runtimeSelectionEnabled'] and not model['runtimeTestsExecuted'] and not model['newAppliedProjectRuleAdoptions'])
 for n,b in payload.items():
  if n.endswith('.py'):ast.parse(b.decode('utf-8'));ck('Syntax parse only; no execution '+n,True)
 ROOT.mkdir();OUT.write_bytes(raw)
 for n,b in payload.items():
  p=ROOT/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b);ck('Extracted complete bytes '+n,p.read_bytes()==b)
 for p,h in before.items():ck('Protected authority unchanged '+p.relative_to(G).as_posix(),sha(p.read_bytes())==h)
 (A/Path(__file__).name).write_bytes(Path(__file__).read_bytes())
 result={'id':'RANK8-DAMAGE6-CORRECTION-RETURN02-LOCAL-PREFLIGHT','recordedAtUtc':datetime.now(timezone.utc).isoformat(),
  'archive':info(OUT),'model':info(ROOT/'MODEL.json'),'nativeFinal':info(A/'GPT_PART5_RANK8_CORRECTION_RETURN_02_NATIVE.json'),
  'assistantTurn':'0d2643ff-e739-40e7-bbeb-7df819ee4a3c','checks':checks,'checkCount':len(checks),'failures':0,
  'sourceFiles':51,'contextFiles':11,'oldReturnMembersPreserved':40,'manifestFiles':98,
  'incrementalOperationsForwardAndReverse':17,'alternativeComposedOperationsForwardAndReverse':54,'fullArtifactReplacements':17,
  'caseInventory':{'main':12,'branches':42,'originalBranchesRetained':41},'reportedFindingDispositions':8,
  'scope':'Independent full-source,hash,manifest,history,exact reversible data-operation replay and preservation only. All eight semantic corrections and the new Pyre rule still need independent local review. No downloaded code executed,project engine or runtime invoked,acceptance increment or canonical application.',
  'acceptedButUnappliedUnchanged':39,'appliedCountsUnchanged':{'reviewed':525,'pending':323,'standalone':249,'interfaces':173},
  'runtimeTestsExecuted':0,'humanPlaytests':0,'sourceInformationDeleted':0,'implementationApplied':False}
 REPORT.write_bytes(enc(result));print(json.dumps({'report':info(REPORT),'checks':len(checks),'failures':0,'archive':info(OUT)}))
if __name__=='__main__':main()
