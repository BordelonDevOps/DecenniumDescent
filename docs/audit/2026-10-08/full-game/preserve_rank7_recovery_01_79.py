from pathlib import Path, PurePosixPath
import json, hashlib, zipfile, io, stat
from datetime import datetime, timezone

G=Path(r'C:\Github\DecenniumDescent')
A=G/'docs/audit/2026-10-08/full-game'
src=Path(r'C:\Users\cbord\Downloads\DD_Rank7_Identity_Casting_5_Part5_Ready_Deadline_RECOVERY_01.zip')
dst=A/src.name
root=A/'rank7-identity-casting5-part5-ready-deadline-recovery-01'
report=A/'RANK7_READY_DEADLINE_RECOVERY_01_PRESERVATION_79.json'
assert not dst.exists() and not root.exists() and not report.exists(), 'One-shot outputs already exist'
checks=[]
def ck(label,ok):
 checks.append({'check':label,'passed':bool(ok)})
 if not ok: raise AssertionError(label)
def enc(v):return (json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode()
def sha(b):return hashlib.sha256(b).hexdigest()
def bound(label,b,x):ck(label,len(b)==x['bytes'] and sha(b)==x['sha256'])
cp=json.loads((A/'ACTIVE_AUTHORING_CHECKPOINT_RANK9_MASS_UNDEATH_78.json').read_bytes())
protect=[cp['currentAuthoredIndex'],cp['currentAcceptedInterfaceRegistry'],*cp['canonicalHelperBaselinesUnchanged'],{'path':'DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json','bytes':4945319,'sha256':'f52cf6a4a4673897615a74c7c67dcba798c431362d4357e71ee552cc7c5d31f8'}]
for x in protect:bound('Protected baseline '+x['path'],(G/x['path']).read_bytes(),x)
b=src.read_bytes();bound('Exact GPT archive',b,{'bytes':31701046,'sha256':'789826c98199b32e779149a8bf00a4eaef18aeb664d1a85e4f9cab78b4875a54'})
z=zipfile.ZipFile(io.BytesIO(b));ns=z.namelist()
ck('CRC',z.testzip() is None);ck('104 unique case-insensitive members',len(ns)==104 and len(set(n.casefold() for n in ns))==104)
for i in z.infolist():
 p=PurePosixPath(i.filename)
 ck('Safe regular member '+i.filename,not p.is_absolute() and '..' not in p.parts and '\\' not in i.filename and ':' not in i.filename and not i.is_dir() and not stat.S_ISLNK(i.external_attr>>16))
manifest=json.loads(z.read('MANIFEST.json'))
ck('Complete 103-file manifest',len(manifest['files'])==103 and set(x['path'] for x in manifest['files'])==set(ns)-{'MANIFEST.json'})
for x in manifest['files']:bound('Manifest '+x['path'],z.read(x['path']),x)
h=json.loads(z.read('HISTORY_BINDINGS.json'));oldbytes=(A/h['retainedExternalInput']['path']).read_bytes();bound('Retained input archive',oldbytes,h['retainedExternalInput']);old=zipfile.ZipFile(io.BytesIO(oldbytes))
ck('Complete supplied history inventory',set(old.namelist())==set(x['path'] for x in h['suppliedMembers']) and len(h['suppliedMembers'])==25)
for x in h['suppliedMembers']:bound('Supplied history '+x['path'],old.read(x['path']),x)
r2bytes=old.read(h['completeReturn02']['member']);bound('Complete Return02 container',r2bytes,h['completeReturn02']);r2=zipfile.ZipFile(io.BytesIO(r2bytes))
ck('Complete Return02 member inventory',set(r2.namelist())==set(x['path'] for x in h['completeReturn02']['members']) and len(r2.namelist())==73)
for x in h['completeReturn02']['members']:bound('Return02 history '+x['path'],r2.read(x['path']),x)
ck('Exact preserved Return02 archive',r2bytes==(A/'DD_Rank7_Identity_Casting_5_Part5_Correction_Return_02.zip').read_bytes())
ck('Exact recovered MODEL from supplied input',z.read('MODEL.json')==old.read('MODEL.json'))
bound('Reported exact MODEL',z.read('MODEL.json'),{'bytes':12000315,'sha256':'949ef5c6a1f05c1b0823d9ec4e10cd3e387a0c8c918680e95fa0047b60e40e3a'})
for n in ns:
 if n.startswith('history/recovery_input/'):ck('Input history copy '+n,z.read(n)==old.read(n[len('history/recovery_input/'):]))
 if n.startswith('history/return02/'):ck('Return02 history copy '+n,z.read(n)==r2.read(n[len('history/return02/'):]))
 if n.startswith(('sources/','context/','inputs/')) and n in r2.namelist():ck('Unchanged source/context '+n,z.read(n)==r2.read(n))
for x in json.loads(z.read('ARTIFACT_BINDINGS.json'))['currentArtifacts']:bound('Current artifact binding '+x['path'],z.read(x['path']),x)
for x in json.loads(z.read('ARTIFACT_OPERATIONS_FROM_RETURN02.json'))['operations']:
 bound('Complete before artifact '+x['artifact'],r2.read(x['before']['member']),x['before']);bound('Complete after artifact '+x['artifact'],z.read(x['after']['path']),x['after'])
ck('No file exceeds 100 MB',all(i.file_size<100_000_000 for i in z.infolist()))
dst.write_bytes(b);root.mkdir()
for n in ns:
 p=Path('\\\\?\\'+str((root/n).resolve()));p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(z.read(n))
for x in manifest['files']:bound('Extracted full bytes '+x['path'],Path('\\\\?\\'+str((root/x['path']).resolve())).read_bytes(),x)
for x in protect:bound('Protected authority unchanged '+x['path'],(G/x['path']).read_bytes(),x)
(A/Path(__file__).name).write_bytes(Path(__file__).read_bytes())
report.write_bytes(enc({'id':'RANK7-READY-DEADLINE-RECOVERY01-PRESERVATION-79','recordedAtUtc':datetime.now(timezone.utc).isoformat(),'archive':{'path':str(dst.relative_to(G)).replace('\\','/'),'bytes':len(b),'sha256':sha(b)},'extraction':str(root.relative_to(G)).replace('\\','/'),'checkCount':len(checks),'failures':0,'checks':checks,'gptReportedChecksNotRerun':{'recoveryAndManifest':932,'isolatedDiagnostic':124},'downloadedCodeExecuted':False,'semanticAcceptance':False,'canonicalChanges':False,'sourceInformationDeleted':0,'scope':'Archive integrity, complete history/source preservation, exact model, full-file bindings and safe extraction. Semantic reconciliation remains separate.'}))
print(json.dumps({'report':str(report),'checkCount':len(checks),'failures':0,'archiveBytes':len(b),'members':len(ns)}))
