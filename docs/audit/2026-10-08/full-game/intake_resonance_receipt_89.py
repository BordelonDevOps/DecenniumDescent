"""One-shot data-only intake and exact incremental reconstruction; no returned code executes."""
from pathlib import Path,PurePosixPath
from copy import deepcopy
from datetime import datetime,timezone
from io import BytesIO
import json,hashlib,zipfile
G=Path(r'C:\Github\DecenniumDescent');A=G/'docs/audit/2026-10-08/full-game'
NAME='DD_Rank9_Resonance_Fields_3_Part5_Feedback_Receipt_Return_02.zip'
SRC=Path(r'C:\Users\cbord\Downloads')/NAME;DEST=A/NAME;ROOT=A/'rank9-resonance-fields3-feedback-receipt-return-02'
OUT=A/'RANK9_RESONANCE_FIELDS3_RECEIPT_RETURN02_INTAKE_89.json';SAVED=A/Path(__file__).name
for p in [DEST,ROOT,OUT,SAVED]:assert not p.exists(),str(p)
def sha(b):return hashlib.sha256(b).hexdigest()
def enc(x):return (json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode()
def info(p):
 b=p.read_bytes();return {'path':p.relative_to(G).as_posix(),'bytes':len(b),'sha256':sha(b)}
checks=[]
def ck(label,ok):
 checks.append({'check':label,'pass':bool(ok)});assert ok,label
b=SRC.read_bytes();ck('Actual downloaded archive binding',len(b)==56617127 and sha(b)=='608c2943bcd976c67a5e80848dd23f635cd813f21f6169342ef29f910c8ca9ab')
z=zipfile.ZipFile(BytesIO(b));names=z.namelist();ck('CRC integrity',z.testzip() is None)
ck('50 unique delivered files',len(names)==50 and len(names)==len(set(names)))
for name in names:
 pp=PurePosixPath(name);ck('Safe member '+name,not pp.is_absolute() and '..' not in pp.parts and '\\' not in name and ':' not in name and not name.endswith('/'))
files={name:z.read(name) for name in names};manifest=json.loads(files['MANIFEST.json'])
ck('49 manifest-bound files',manifest['fileCount']==49 and {r['path'] for r in manifest['files']}==set(names)-{'MANIFEST.json'})
for row in manifest['files']:
 data=files[row['path']];ck('Manifest '+row['path'],len(data)==row['bytes'] and sha(data)==row['sha256'])
for row in json.loads(files['INPUT_BINDINGS.json'])['inputs']:
 data=files[row['file']];local=(A/Path(row['file']).name).read_bytes()
 ck('Complete original input preserved '+row['file'],data==local and len(data)==row['bytes'] and sha(data)==row['sha256'])
archives={name:zipfile.ZipFile(BytesIO(data)) for name,data in files.items() if name.startswith('input/') and name.endswith('.zip')}
def raw(ref):return files[ref['file']] if 'file' in ref else archives[ref['archive']].read(ref['member'])
def ptr(obj,path):
 for key in path.split('/')[1:]:
  key=key.replace('~1','/').replace('~0','~');obj=obj[int(key)] if isinstance(obj,list) else obj[key]
 return obj
def value(ref):return ptr(json.loads(raw(ref)),ref.get('pointer',''))
def parent(obj,path):
 parts=path.split('/');return ptr(obj,'/'.join(parts[:-1])),parts[-1].replace('~1','/').replace('~0','~')
def vhash(x):return sha(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
opset=json.loads(files['EXACT_OPERATIONS_FROM_RETURN01.json']);oldbytes=raw(opset['baseline']);newbytes=raw(opset['successor'])
for name,ref in [('baseline',opset['baseline']),('successor',opset['successor'])]:
 data=raw(ref);ck('Exact MODEL '+name,len(data)==ref['bytes'] and sha(data)==ref['sha256'])
ck('Six incremental operations',opset['operationCount']==6 and len(opset['operations'])==6)
model=json.loads(oldbytes)
for idx,op in enumerate(opset['operations']):
 par,key=parent(model,op['path']);key=int(key) if isinstance(par,list) else key
 before=op['before'];after=op['after'];exists=0<=key<len(par) if isinstance(par,list) else key in par
 ck(f'Operation{idx} present-before matches',exists==before['present'])
 if exists:
  val=value(before['valueRef']);ck(f'Operation{idx} exact whole before',par[key]==val and vhash(val)==before['valueSha256'])
 assert op['op'] in ['replace','add'] and after['present']
 val=value(after['valueRef']);ck(f'Operation{idx} full after hash',vhash(val)==after['valueSha256']);par[key]=deepcopy(val)
ck('Forward six operations reproduce complete MODEL bytes',enc(model)==newbytes)
for idx,op in reversed(list(enumerate(opset['operations']))):
 par,key=parent(model,op['path']);key=int(key) if isinstance(par,list) else key
 ck(f'Reverse{idx} expected full successor',par[key]==value(op['after']['valueRef']))
 if op['before']['present']:par[key]=deepcopy(value(op['before']['valueRef']))
 else:del par[key]
ck('Inverse restores complete Return01 MODEL bytes',enc(model)==oldbytes)
replacements=json.loads(files['ARTIFACT_REPLACEMENTS_FROM_RETURN01.json'])
ck('12 complete artifact replacements',replacements['replacementCount']==12 and len(replacements['replacements'])==12)
for row in replacements['replacements']:
 for side in ['before','after']:
  ref=row[side];data=raw(ref);ck('Complete artifact '+side+' '+row['path'],len(data)==ref['bytes'] and sha(data)==ref['sha256'])
old=archives['input/DD_Rank9_Resonance_Fields_3_Part5_Conference_Return_01.zip']
unchanged=['PROCEDURES.json','SHARED_RULES.json','QUESTION_DISPOSITIONS.json','ACTOR_TEMPLATES.json','ACTOR_FEATURE_ACCOUNTING.json','ALL_MAGIC_CATEGORY_MAP.json','PLAYER_CHAPTER.md','SPELL_DISPOSITIONS.json','DECISIONS.md','SOURCE_AUTHORITY.json','SOURCE_EXCERPTS.json','SOURCE_REFERENCES.json','HOLD_REGISTER.json','ORIGINAL_HISTORY.json','PENDING_COMPARISON_NOT_ADOPTED.json']
for name in unchanged:ck('Entire earlier artifact unchanged '+name,files[name]==old.read(name))
newmodel=json.loads(newbytes);casebook=json.loads(files['CASE_DISPOSITIONS.json'])
ck('Full current MODEL and casebook agreement',newmodel['currentVectors']==casebook['cases'])
ck('Full Director casebook contains exact current case JSON',json.dumps(casebook,ensure_ascii=False,indent=2) in files['DIRECTOR_REVIEW.md'].decode())
ck('Seven main cases and28 branches',len(casebook['cases'])==7 and sum(len(c.get('independentBranches',[])) for c in casebook['cases'])==28)
canonical=json.loads((A/'ACTIVE_AUTHORING_CHECKPOINT_FEAT_WORK_SEMANTIC_REVIEW_88.json').read_text(encoding='utf-8'))
for row in [canonical['currentAuthoredIndex'],canonical['currentAcceptedInterfaceRegistry'],canonical['currentWorkQueue'],*canonical['canonicalHelperBaselinesUnchanged']]:ck('Canonical untouched '+row['path'],info(G/row['path'])==row)
# Only after every data-only check succeeds preserve/extract into a fresh isolated directory.
with DEST.open('xb') as f:f.write(b)
ROOT.mkdir()
for name,data in files.items():
 dst=Path('\\\\?\\'+str((ROOT/name).resolve()));dst.parent.mkdir(parents=True,exist_ok=True)
 with dst.open('xb') as f:f.write(data)
 ck('Extracted bytes '+name,dst.read_bytes()==data)
with SAVED.open('xb') as f:f.write(Path(__file__).read_bytes())
report={'id':'RF9-FEEDBACK-RETURN02-INTAKE-89','recordedAtUtc':datetime.now(timezone.utc).isoformat(),'archive':info(DEST),'model':info(ROOT/'MODEL.json'),'fileCount':50,'incrementalOperations':6,'completeArtifactReplacements':12,'checks':checks,'passed':len(checks),'failed':0,'semanticReviewComplete':False,'exactAuthorshipAccepted':False,'canonicalApplied':False,'downloadedCodeExecuted':False,'script':info(SAVED),'reportedGptDiagnostics':{'sourceReconstructionChecks':918,'freshArchiveChecks':968,'diagnosticCases':31,'diagnosticAssertions':64,'locallyExecuted':False},'scope':'Data integrity, exact source preservation and independent forward/inverse six-operation reconstruction. Full31 diagnostic and receipt semantic review remains next; no claim of runtime or parent335 acceptance.'}
with OUT.open('xb') as f:f.write(enc(report))
print(json.dumps({'report':info(OUT),'archive':info(DEST),'model':info(ROOT/'MODEL.json'),'passed':len(checks),'failed':0},indent=2))
