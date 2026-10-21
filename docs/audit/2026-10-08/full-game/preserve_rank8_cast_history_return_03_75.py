"""Independent data preservation/replay. Downloaded Python is parsed only, never run."""
from pathlib import Path,PurePosixPath
from datetime import datetime,timezone
import ast,copy,hashlib,io,json,re,stat,zipfile
G=Path(r'C:\Github\DecenniumDescent');A=G/'docs/audit/2026-10-08/full-game'
IN=Path(r'C:\Users\cbord\Downloads\DD_Rank8_Damage_6_Part5_Cast_History_Return_03.zip')
OUT=A/IN.name;ROOT=A/'rank8-damage6-part5-cast-history-return-03';OLD=A/'rank8-damage6-part5-correction-return-02'
REPORT=A/'RANK8_DAMAGE6_PART5_CAST_HISTORY_RETURN_03_LOCAL_PREFLIGHT.json'
def sha(b):return hashlib.sha256(b).hexdigest()
def enc(x):return (json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode()
def read(p):return json.loads(p.read_bytes())
def info(p):
 b=p.read_bytes();return {'path':p.relative_to(G).as_posix(),'bytes':len(b),'sha256':sha(b)}
def parent(d,ptr):
 parts=[v.replace('~1','/').replace('~0','~') for v in ptr.split('/')[1:]]
 for k in parts[:-1]:d=d[int(k)] if isinstance(d,list) else d[k]
 return d,int(parts[-1]) if isinstance(d,list) else parts[-1]
assert not any(p.exists() for p in [OUT,ROOT,REPORT,A/Path(__file__).name])
checks=[]
def ck(n,v):checks.append({'check':n,'passed':bool(v)});assert v,n
def binding(b,expected,label):ck(label,len(b)==expected['bytes'] and sha(b)==expected['sha256'])
def unpack(raw,label):
 with zipfile.ZipFile(io.BytesIO(raw)) as z:
  names=z.namelist();ck(label+' unique names',len(names)==len(set(names))==len(set(n.casefold() for n in names)))
  ck(label+' bounded expansion',sum(i.file_size for i in z.infolist())<110_000_000)
  for i in z.infolist():
   p=PurePosixPath(i.filename);ck(label+' safe '+i.filename,not p.is_absolute() and '..' not in p.parts and '\\' not in i.filename and ':' not in i.filename and not i.is_dir() and not stat.S_ISLNK(i.external_attr>>16))
  ck(label+' CRC',z.testzip() is None);return {n:z.read(n) for n in names}
cpfile=A/'ACTIVE_AUTHORING_CHECKPOINT_RANK7_DEADLINE_SEMANTICS_74.json';cp=read(cpfile)
protected=[cpfile,G/'DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json']
protected += [G/cp[k]['path'] for k in ['currentWorkQueue','currentAuthoredIndex','currentAcceptedInterfaceRegistry','decisionLedger']]
protected += [G/b['path'] for b in cp['canonicalHelperBaselinesUnchanged']]
protected += [p for p in OLD.rglob('*') if p.is_file()]
before={p:sha(p.read_bytes()) for p in protected}
raw=IN.read_bytes();binding(raw,{'bytes':38149990,'sha256':'68fa6b727450a883672483800b02a54934525e0bccbbfc6392e3dddb4e6afe9e'},'Exact downloaded Return03')
payload=unpack(raw,'Return03');j=lambda n:json.loads(payload[n]);man=j('MANIFEST.json')
ck('150 members and149 manifest files',len(payload)==150 and len(man['files'])==man['fileCount']==149)
ck('Complete manifest membership',set(payload)=={'MANIFEST.json'}|{b['path'] for b in man['files']})
for b in man['files']:binding(payload[b['path']],b,'Manifest '+b['path'])
ib=j('INPUT_BINDINGS.json');submitted=payload[ib['currentInput']['path']]
binding(submitted,ib['currentInput'],'Submitted packet binding');ck('Exact actual submitted packet',submitted==(A/'DD_Rank8_Damage6_Cast_History_Correction_02.zip').read_bytes())
incoming=unpack(submitted,'Submitted packet');nested=incoming[ib['priorReturn']['nestedMember']]
binding(nested,ib['priorReturn'],'Nested Return02 binding');ck('Exact prior archive retained',nested==(A/'DD_Rank8_Damage_6_Part5_Correction_Return_02.zip').read_bytes())
oldpayload=unpack(nested,'Preserved Return02');ck('All99 prior members retained',len(oldpayload)==99)
for n,b in oldpayload.items():ck('Actual prior full member '+n,b==(OLD/n).read_bytes())
for n,b in payload.items():
 if n.startswith('history/return02/'):ck('Historical Return02 root '+n,b==oldpayload[n[len('history/return02/'):]])
 if n.startswith('history/return01/'):ck('Historical Return01 '+n,b==oldpayload[n])
 if n.startswith('cast_history_source/'):ck('Exact supplied local evidence '+n,b==incoming[n[len('cast_history_source/'):]])
source=payload['input/DD_Rank8_Damage_6_Source_Conference_01.zip']
ck('Actual complete original source packet',source==(A/'DD_Rank8_Damage_6_Source_Conference_01.zip').read_bytes())
sp=unpack(source,'Original source packet');sources=j('SOURCE_BINDINGS.json')['originalFullSources']
ck('51 complete source bindings',len(sources)==51)
ck('Original source candidate exact',sp['CANDIDATE.json']==payload['baseline/CANDIDATE.json'])
for b in sources:
 data=sp['sources/'+b['path']];binding(data,b,'Source binding '+b['path']);ck('Current actual source '+b['path'],data==(G/b['path']).read_bytes())
contexts=j('CONTEXT_BINDINGS.json')['files'];ck('Eleven complete contexts',len(contexts)==11)
for b in contexts:
 data=payload[b['file']];binding(data,b,'Context binding '+b['file']);ck('Full prior context unchanged '+b['file'],data==oldpayload[b['file']])
 for anchor in b['exactArchiveAnchors']:
  ar=(A/anchor['archive']).read_bytes();binding(ar,{'bytes':anchor['archiveBytes'],'sha256':anchor['archiveSha256']},'Context source archive '+anchor['archive'])
  with zipfile.ZipFile(io.BytesIO(ar)) as z:body=z.read(anchor['member'])
  binding(body,anchor,'Context source member '+anchor['member']);ck('Actual context body '+b['file'],body==data)
def replay(name,count):
 plan=j(name);base=payload[plan['base']['file']];target=payload[plan['successor']['file']]
 binding(base,plan['base'],name+' baseline');binding(target,plan['successor'],name+' successor')
 ck(name+' exact count',len(plan['operations'])==plan['operationCount']==count);d=json.loads(base)
 for i,o in enumerate(plan['operations']):
  p,k=parent(d,o['pointer']);exists=(0<=k<len(p)) if isinstance(p,list) else k in p
  ck(name+' supported operation '+str(i),o['op'] in ['replace','add'] and (not isinstance(p,list) or o['op']=='replace'))
  ck(name+' before existence '+str(i),exists==o['beforeExists']);ck(name+' complete before '+str(i),(p[k] if exists else None)==o.get('before'));p[k]=copy.deepcopy(o['after'])
 ck(name+' complete forward bytes',enc(d)==target)
 for i,o in enumerate(reversed(plan['operations'])):
  p,k=parent(d,o['pointer']);ck(name+' reverse after '+str(i),p[k]==o['after'])
  if o['beforeExists']:p[k]=copy.deepcopy(o['before'])
  else:del p[k]
 ck(name+' complete reverse bytes',enc(d)==base)
replay('EXACT_OPERATIONS_FROM_RETURN02.json',4);replay('EXACT_OPERATIONS_FROM_SOURCE.json',58)
ck('Full prior54 operations unchanged',j('EXACT_OPERATIONS_FROM_SOURCE.json')['operations'][:54]==json.loads(oldpayload['EXACT_OPERATIONS_FROM_SOURCE.json'])['operations'])
ck('Exact new4 suffix',j('EXACT_OPERATIONS_FROM_SOURCE.json')['operations'][54:]==j('EXACT_OPERATIONS_FROM_RETURN02.json')['operations'])
plans=j('ARTIFACT_OPERATIONS_FROM_RETURN02.json')['files'];ck('17 full artifact replacements',len(plans)==17)
for row in plans:
 op=row['operation'];b=payload[row['before']['path']];a=payload[row['after']['path']]
 binding(b,row['before'],'Artifact before '+row['before']['path']);binding(a,row['after'],'Artifact after '+row['after']['path'])
 if row['kind']=='json-full-value':ck('Complete JSON before '+row['before']['path'],enc(op['before'])==b);ck('Complete JSON after '+row['after']['path'],enc(op['after'])==a)
 else:
  ck('Supported full text replacement',row['kind'] in ['text-full-file','exact-utf8-full-file']);ck('Complete text before '+row['before']['path'],op['before'].encode()==b);ck('Complete text after '+row['after']['path'],op['after'].encode()==a)
model=j('MODEL.json');old=json.loads(oldpayload['MODEL.json']);cases=j('CASE_DISPOSITIONS.json')['allCases']
binding(payload['MODEL.json'],{'bytes':1762437,'sha256':'07e508c7135a65db2cabc98d6c8aa97b7f5feb4bc108b499f11b697aa904e656'},'Exact successor MODEL')
ck('Full case mirror',cases==model['currentVectors']);ck('12 main42 branches',len(cases)==12 and sum(len(c['independentBranches']) for c in cases)==42)
for key in ['records','selectedSharedRules','questionDispositions','riskCounts']:
 if key in old:ck('Complete prior authority retained '+key,model[key]==old[key])
for n in ['PLAYER_CHAPTER.md','SPELL_DISPOSITIONS.json','QUESTION_DISPOSITIONS.json','HOLD_REGISTER.json','INTERFACE_USAGE.json']:
 ck('Byte-identical authority '+n,payload[n]==oldpayload[n])
ck('Eleven other complete main cases unchanged',all(b==a for i,(b,a) in enumerate(zip(old['currentVectors'],cases)) if i!=9))
bcase=old['currentVectors'][9];acase=cases[9];restored=copy.deepcopy(acase)
for before_case,after_case,restored_case in zip([bcase]+bcase['independentBranches'],[acase]+acase['independentBranches'],[restored]+restored['independentBranches']):
 b=before_case['actorSheets']['anchorCaster'];a=after_case['actorSheets']['anchorCaster'];tag=after_case['id']
 ck(tag+' exact two changed fields',{k for k in b.keys()|a.keys() if b.get(k)!=a.get(k)}=={'matrixFamiliesUsed','initialSetup'})
 ck(tag+' correct used family',a['matrixFamiliesUsed']==['dimensional-anchor']);ck(tag+' full initial setup prefix retained',a['initialSetup'].startswith(b['initialSetup']))
 restored_case['actorSheets']['anchorCaster']=copy.deepcopy(b)
ck('No other RD8-05-B field changes',restored==bcase)
ck('No runtime flags enabled',not model['runtimeImplemented'] and not model['runtimeSelectionEnabled'] and not model['runtimeTestsExecuted'] and not model['newAppliedProjectRuleAdoptions'])
for n,b in payload.items():
 if n.endswith('.py'):ast.parse(b.decode('utf-8'));ck('Parse only no execution '+n,True)
ROOT.mkdir();OUT.write_bytes(raw)
for n,b in payload.items():
 p=ROOT/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b);ck('Complete extracted bytes '+n,p.read_bytes()==b)
for p,h in before.items():ck('Protected unchanged '+p.relative_to(G).as_posix(),sha(p.read_bytes())==h)
(A/Path(__file__).name).write_bytes(Path(__file__).read_bytes())
result={'id':'RANK8-DAMAGE6-CAST-HISTORY-RETURN03-LOCAL-PREFLIGHT','recordedAtUtc':datetime.now(timezone.utc).isoformat(),'archive':info(OUT),'model':info(ROOT/'MODEL.json'),
 'nativeFinal':info(A/'GPT_PART5_RANK8_CAST_HISTORY_RETURN_03_NATIVE.json'),'assistantTurn':'d87b38d5-7614-46bb-825e-2da9141c7cdb','ownerClarificationTurn':'8d896794-6126-4220-8882-38425ff3e6c7',
 'checks':checks,'checkCount':len(checks),'failures':0,'sourceFiles':51,'contextFiles':11,'oldReturnMembersPreserved':99,'manifestFiles':149,'incrementalOperationsForwardAndReverse':4,'alternativeComposedOperationsForwardAndReverse':58,'fullArtifactReplacements':17,
 'caseInventory':{'main':12,'branches':42},'supportingActorCopiesChanged':9,'scope':'Full preservation/source/reversible data reconstruction and narrow two-field delta validation. Separate later-cast semantic review remains pending. No downloaded code executed or new acceptance claimed.',
 'acceptedButUnappliedUnchanged':39,'appliedCountsUnchanged':{'reviewed':525,'pending':323,'standalone':249,'interfaces':173},'runtimeTestsExecuted':0,'implementationApplied':False,'sourceInformationDeleted':0}
REPORT.write_bytes(enc(result));print(json.dumps({'report':info(REPORT),'checks':len(checks),'failures':0,'archive':info(OUT)}))
