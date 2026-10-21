"""Preserve and independently reconstruct FT84 Return01. Never imports returned code."""
from pathlib import Path, PurePosixPath
from copy import deepcopy
from datetime import datetime, timezone
import hashlib, io, json, zipfile

G=Path(r'C:\Github\DecenniumDescent')
A=G/'docs/audit/2026-10-08/full-game'
NAME='DD_Feat335_Work_Compositions_84_Part5_Return_01.zip'
SRC=Path(r'C:\Users\cbord\Downloads')/NAME
DEST=A/NAME
ROOT=A/'feat335-work-compositions84-part5-return-01'
OUT=A/'FEAT335_WORK_COMPOSITIONS_PART5_RETURN01_INTAKE_87.json'
SAVED=A/Path(__file__).name
for p in [DEST,ROOT,OUT,SAVED]:
    assert not p.exists(), f'Exclusive output exists: {p}'
checks=[]
def ck(label,condition):
    checks.append({'check':label,'pass':bool(condition)})
    assert condition,label
def sha(b): return hashlib.sha256(b).hexdigest()
def encode(d): return (json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode()
def binding(p):
    b=p.read_bytes();return {'path':p.relative_to(G).as_posix(),'bytes':len(b),'sha256':sha(b)}
raw=SRC.read_bytes()
ck('Archive exact advertised length',len(raw)==4606749)
ck('Archive exact advertised SHA256',sha(raw)=='c9be0bb12a36131f2b9781730cde1ceff728443717020d372a4a3508e53d020a')
with zipfile.ZipFile(io.BytesIO(raw)) as z:
    names=z.namelist()
    ck('34 unique files',len(names)==len(set(names))==34)
    ck('No case-insensitive collisions',len(set(n.casefold() for n in names))==len(names))
    ck('CRC valid',z.testzip() is None)
    for n in names:
        p=PurePosixPath(n)
        ck('Safe member '+n,not p.is_absolute() and '..' not in p.parts and '\\' not in n and ':' not in n and not n.endswith('/'))
    files={n:z.read(n) for n in names}
manifest=json.loads(files['MANIFEST.json'])
ck('Manifest exactly enumerates remaining files',set(x['path'] for x in manifest['files'])==set(names)-{'MANIFEST.json'} and manifest['fileCount']==33)
for row in manifest['files']:
    b=files[row['path']]
    ck('Manifest bytes/hash '+row['path'],len(b)==row['bytes'] and sha(b)==row['sha256'])
inputs={}
for name in ['DD_Feat335_Work_Compositions_84.zip','DD_Feat335_Time_Provisions_Cases_83.zip']:
    b=files['input/'+name]
    ck('Original input byte preservation '+name,b==(A/name).read_bytes())
    inputs[name]=zipfile.ZipFile(io.BytesIO(b))
    ck('Input CRC '+name,inputs[name].testzip() is None)
sources=json.loads(files['SOURCE_BINDINGS.json'])
for row in sources['inputMembers']:
    b=inputs[row['archive']].read(row['member'])
    ck('Full source binding '+row['archive']+' :: '+row['member'],len(b)==row['bytes'] and sha(b)==row['sha256'])
ops=json.loads(files['JSON_POINTER_OPERATIONS.json'])['operations']
reps=json.loads(files['FULL_ARTIFACT_REPLACEMENTS.json'])['replacements']
ck('51 exact replacements',len(ops)==51 and all(x['op']=='replace' for x in ops))
ck('Seven complete successor files',len(reps)==7)
def slot(doc,pointer):
    parts=[s.replace('~1','/').replace('~0','~') for s in pointer[1:].split('/')]
    obj=doc
    for key in parts[:-1]: obj=obj[int(key)] if isinstance(obj,list) else obj[key]
    key=int(parts[-1]) if isinstance(obj,list) else parts[-1]
    return obj,key
reconstruction=[]
for row in reps:
    br,ar=row['before'],row['after']
    before=inputs[PurePosixPath(br['archive']).name].read(br['member'])
    after=files[ar['file']]
    ck('Full before binding '+row['fileKey'],len(before)==br['bytes'] and sha(before)==br['sha256'])
    ck('Full after binding '+row['fileKey'],len(after)==ar['bytes'] and sha(after)==ar['sha256'])
    ck('Local baseline remains same '+row['fileKey'],(G/row['repositoryPath']).read_bytes()==before)
    selected=[x for x in ops if x['fileKey']==row['fileKey']]
    record={'fileKey':row['fileKey'],'before':br,'after':ar,'operations':len(selected)}
    if selected:
        doc=json.loads(before)
        for op in selected:
            obj,key=slot(doc,op['pointer'])
            ck('Exact before '+op['fileKey']+op['pointer'],obj[key]==op['before'])
            obj[key]=deepcopy(op['after'])
        ck('Complete forward value '+row['fileKey'],doc==json.loads(after))
        ck('Complete forward bytes '+row['fileKey'],encode(doc)==after)
        for op in reversed(selected):
            obj,key=slot(doc,op['pointer'])
            ck('Exact reverse before '+op['fileKey']+op['pointer'],obj[key]==op['after'])
            obj[key]=deepcopy(op['before'])
        ck('Complete inverse bytes '+row['fileKey'],encode(doc)==before)
        record['completeForwardAndInverseBytesVerified']=True
    reconstruction.append(record)
model=json.loads(files['MODEL.json']);casebook=json.loads(files['CASEBOOK.json'])
ck('Model explicitly unapplied and unapproved',not model['canonicalApplied'] and not model['parent335Accepted'] and not model['runtimeImplemented'] and model['sourceInformationDeleted']==0)
ck('57 declared cases retained',len(casebook['cases'])==casebook['caseCount']==57)
ck('Three question dispositions',len(model['questions'])==3)
ck('Six complete proposed procedures',len(model['fullSelectedProcedures'])==6)
# All validations above precede any extraction. Output is isolated from live source files.
with DEST.open('xb') as f:f.write(raw)
ROOT.mkdir()
for name,b in files.items():
    p=Path('\\\\?\\'+str((ROOT/Path(name)).resolve()))
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('xb') as f:f.write(b)
    ck('Extracted byte identity '+name,p.read_bytes()==b)
with SAVED.open('xb') as f:f.write(Path(__file__).read_bytes())
report={'id':'FEAT335-WORK-COMPOSITIONS-PART5-RETURN01-INTAKE-87','recordedAtUtc':datetime.now(timezone.utc).isoformat(),'scope':'Independent complete archive preservation, source binding, full forward/inverse reconstruction and exact current-baseline checks. No returned Python or project code executed. Complete authored semantic case review remains pending.','actualAssistant':'8b206110-876a-4334-bf18-b9810f18952f','actualUserTurn':'e4fba178-593e-4596-915e-b408935b1b8e','archive':binding(DEST),'extractRoot':str(ROOT),'model':binding(ROOT/'MODEL.json'),'checks':checks,'passed':len(checks),'failed':0,'completeReconstruction':reconstruction,'reportedGptDiagnostics':{'cases':57,'assertions':167,'verificationChecks':2337,'freshExtractionChecks':2404,'locallyExecuted':False},'semanticsAccepted':False,'parent335Accepted':False,'canonicalImplementationApplied':False,'runtimeExecuted':False,'sourceInformationDeleted':0,'script':binding(SAVED)}
with OUT.open('xb') as f:f.write(encode(report))
print(json.dumps({'report':binding(OUT),'checks':len(checks),'failures':0,'files':len(files),'operations':len(ops),'scope':report['scope']},indent=2))
