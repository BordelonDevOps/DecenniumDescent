from pathlib import Path, PurePosixPath
from datetime import datetime, timezone
import hashlib,json,zipfile,stat
G=Path(r'C:\Github\DecenniumDescent');A=G/'docs/audit/2026-10-08/full-game'
SRC=Path(r'C:\Users\cbord\Downloads\DD_Rank9_Resonance_Fields_3_Part5_Conference_Return_01.zip')
ZIP=A/SRC.name;ROOT=A/'rank9-resonance-fields3-part5-return-01';OUT=A/'RANK9_RESONANCE_FIELDS3_PART5_RETURN01_INTAKE_85.json';SAVED=A/Path(__file__).name
for p in [ZIP,ROOT,OUT,SAVED]:assert not p.exists(),str(p)
def enc(x):return (json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
def digest(b):return hashlib.sha256(b).hexdigest()
def info(p):
 b=p.read_bytes();return {'path':p.relative_to(G).as_posix(),'bytes':len(b),'sha256':digest(b)}
checks=[]
def ck(label,value):
 checks.append({'check':label,'pass':bool(value)})
 if not value:raise AssertionError(label)
raw=SRC.read_bytes();ck('Exact actually downloaded archive',len(raw)==54459580 and digest(raw)=='09e6ea3b629723294d0da5f5551a460c9146e9f428471c8fe359bc394955f30d')
with zipfile.ZipFile(SRC) as z:
 members=z.infolist();names=[i.filename for i in members]
 ck('36 unique actual members',len(names)==36 and len(set(names))==36 and len({n.casefold() for n in names})==36)
 for i in members:
  p=PurePosixPath(i.filename)
  ck('Safe regular archive member '+i.filename,not p.is_absolute() and '..' not in p.parts and '\\' not in i.filename and ':' not in i.filename and not i.is_dir() and not stat.S_ISLNK(i.external_attr>>16))
 ck('Archive CRC',z.testzip() is None)
 payload={n:z.read(n) for n in names};mf=json.loads(payload['MANIFEST.json'])
 ck('Manifest accounts for all35 nonmanifest files',mf['fileCount']==35 and len(mf['files'])==35 and {r['path'] for r in mf['files']}==set(names)-{'MANIFEST.json'})
 for r in mf['files']:
  b=payload[r['path']];ck('Exact manifest binding '+r['path'],len(b)==r['bytes'] and digest(b)==r['sha256'])
 ck('Exact complete MODEL',len(payload['MODEL.json'])==5106581 and digest(payload['MODEL.json'])=='79d8411b7d0880ac8cb6682de895bbfc7ff75219575d68608de43f778e6525d9')
 for name,sha,size in [('DD_Rank9_Resonance_Fields_3_Source_Conference_01.zip','9d92814a69f5ddbf8ec47a8d5dc6fd9d1f972e9e923bb7efff2e5d1468147e41',48727634),('DD_Rank9_Resonance_Fields3_Current_Context_80.zip','7acaa6e544b29e9bbace3f16dc7ecbbd057ce1776877ad842e2daa890573f601',4857325)]:
  b=payload['input/'+name];ck('Full original input retained '+name,len(b)==size and digest(b)==sha and b==(A/name).read_bytes())
receipt=json.loads(payload['REVIEW_RECEIPT.json']);model=json.loads(payload['MODEL.json'])
native=A/'GPT_PART5_RESONANCE_FIELDS3_COMPLETE_NATIVE_85.json';n=json.loads(native.read_text(encoding='utf-8'))
turn=n['turns'][0]
ck('Actual targeted GPT turn completed',turn['id']=='fcee2fb1-a2d9-4ee5-b2dc-9c9fb75f9194' and turn['status']=='completed')
cp=json.loads((A/'ACTIVE_AUTHORING_CHECKPOINT_FEAT_WORK_COMPOSITIONS_84.json').read_text(encoding='utf-8'))
protected=[cp['currentAuthoredIndex'],cp['currentAcceptedInterfaceRegistry'],cp['currentWorkQueue'],*cp['canonicalHelperBaselinesUnchanged']]
for r in protected:ck('Protected current authority '+r['path'],info(G/r['path'])==r)
ZIP.write_bytes(raw);ROOT.mkdir()
for name,b in payload.items():
 p=Path('\\\\?\\'+str((ROOT/name).resolve()));p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
 ck('Exact preserved member '+name,p.read_bytes()==b)
ck('Source download itself unchanged',SRC.read_bytes()==raw)
for r in protected:ck('Protected authority unchanged after intake '+r['path'],info(G/r['path'])==r)
SAVED.write_bytes(Path(__file__).read_bytes())
report={'id':'RANK9-RESONANCE-FIELDS3-PART5-RETURN01-INTAKE85','recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'ACTUAL_RETURN_PRESERVED_AND_MANIFEST_VERIFIED_SEMANTIC_REVIEW_PENDING','archive':info(ZIP),'root':ROOT.relative_to(G).as_posix(),'model':info(ROOT/'MODEL.json'),'manifest':info(ROOT/'MANIFEST.json'),'nativeResponse':info(native),'browserResponse':info(A/'GPT_PART5_RESONANCE_FIELDS3_COMPLETE_85.txt'),'actualRequestId':turn['id'],'actualTurnStatus':turn['status'],'actualAssistantItems':[{'id':i.get('id'),'type':i.get('type'),'role':i.get('role')} for i in turn['items']],'reportedGptReceiptUnchanged':receipt,'checks':checks,'checkCount':len(checks),'failures':0,'downloadedCodeExecuted':False,'runtimeTestsExecuted':0,'canonicalImplementationApplied':False,'independentExactAcceptance':False,'acceptedButUnappliedUnchanged':50,'nextAction':'Independently inspect complete procedures, all24 dispositions, seven positive encounters and28 branches, source-qualified costs/actors, full reversible operations and all-magic scope. Supplied reports are evidence of GPT checks, not local semantic approval. Preserve owner reservation.','sourceInformationDeleted':0}
OUT.write_bytes(enc(report));print(json.dumps({'receipt':info(OUT),'archive':info(ZIP),'root':str(ROOT),'checks':len(checks),'failures':0,'modelTopKeys':list(model)}))
