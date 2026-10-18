from pathlib import Path, PurePosixPath
import hashlib,json,zipfile,stat
from datetime import datetime,timezone
G=Path(r'C:\Github\DecenniumDescent'); A=G/'docs/audit/2026-10-08/full-game'; D=Path(r'C:\Users\cbord\Downloads')
def raw(p): return Path('\\\\?\\'+str(p)).read_bytes()
def write(p,b):
 p=Path('\\\\?\\'+str(p)); p.parent.mkdir(parents=True,exist_ok=True); assert not p.exists(),str(p);p.write_bytes(b)
def binding(p):
 b=raw(p);return {'path':str(p.relative_to(G)).replace('\\','/'),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
specs=[
 ('DD_Companion_Life_10_Exact_05_Part5_Return_01.zip',692808,'161f6920c754e7a0c2d9ea4326be73ba22866912b9b7c81c8421f9d104d52522','companion-life10-exact05-part5-return-01','companion-life10-exact-05','DD_Companion_Life_10_Exact_05.zip','bcc687cc-3169-46a9-a080-a287cbcb6c97'),
 ('DD_Illusion_Perception_14_Exact_13_Part5_Return_01.zip',687725,'c75df814489fe42924ec03fe425565c2474e0080c62764f5188f49472be6eb19','illusion-perception14-exact13-part5-return-01','illusion-perception14-exact-13','DD_Illusion_Perception_14_Exact_13.zip','5f15c8ef-4194-43d9-98e1-ae2e945b21b6'),
 ('DD_Part5_Control_Ready_Corrections_01.zip',6704401,'449e40d625447b206422d1e1df776952c30e7a34b72157d1e4cded0dc04793b0','part5-control-ready-corrections-01',None,None,'b7840891-58fd-4d62-ac01-cb1ed9b8710e')]
receipt=A/'GPT_PART5_PERTINENT_RETURNS_01_RECEIPT.json';assert not receipt.exists()
results=[];prepared=[]
native=json.loads(raw(A/'GPT_PART5_EXACT_ACCEPTANCES_01_NATIVE.json'))
correction_native=json.loads(raw(A/'GPT_PART5_CORRECTIONS_AND_BACKLOG_01_NATIVE.json'))
messages={i['id']:i['text'] for p in [native,correction_native] for t in p['turns'] for i in t['items'] if i['type']=='agentMessage'}
for name,size,sha,folder,current,input_zip,message_id in specs:
 b=raw(D/name);assert len(b)==size and hashlib.sha256(b).hexdigest()==sha
 assert sha in messages[message_id]
 assert not (A/name).exists() and not (A/folder).exists()
 with zipfile.ZipFile(D/name) as z:
  names=z.namelist();assert len(names)==len(set(n.casefold() for n in names));assert z.testzip() is None
  for zi in z.infolist():
   p=PurePosixPath(zi.filename);assert not p.is_absolute() and '..' not in p.parts and '\\' not in zi.filename and ':' not in zi.filename
   assert not stat.S_ISLNK(zi.external_attr>>16)
  m=json.loads(z.read('MANIFEST.json')); entries=m['files'];assert set(names)=={'MANIFEST.json'}|{x['path'] for x in entries}
  for x in entries:
   d=z.read(x['path']);assert len(d)==x['bytes'] and hashlib.sha256(d).hexdigest()==x['sha256']
  matches=[]
  if current:
   with zipfile.ZipFile(A/input_zip) as src:
    for n in names:
     if n.startswith('accepted/current/'):
      fn=n.removeprefix('accepted/current/');d=z.read(n)
      assert d==raw(A/current/fn)==src.read('current/'+fn)
      matches.append({'filename':fn,'bytes':len(d),'sha256':hashlib.sha256(d).hexdigest(),'matchesLocalAndSubmittedArchive':True})
   assert len(matches)==8
  prepared.append((name,folder,b,{n:z.read(n) for n in names}))
  results.append({'archive':{'path':str((A/name).relative_to(G)).replace('\\','/'),'bytes':size,'sha256':sha},'actualAssistantResponse':message_id,'archiveMembers':len(names),'manifestBoundFilesVerified':len(entries),'safeNamesAndCrc':True,'acceptedArtifactComparisons':matches,'extractedDirectory':str((A/folder).relative_to(G)).replace('\\','/')})
for name,folder,b,files in prepared:
 write(A/name,b)
 for n,d in files.items():write(A/folder/n,d)
record={'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'threadId':'6ad4a867-f330-83e9-829e-bf2bb41a6c09','title':'Calibration Review Part 5','status':'ACTUAL_RETURNS_PRESERVED_AND_INTEGRITY_VERIFIED; NOT_APPLIED','returns':results,'sourceIndex':binding(G/'DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json'),'appliedMembershipUnchanged':{'reviewed':525,'pending':323,'standalone':249},'sourceInformationDeleted':0,'correctionsExecuted':False,'runtimeTestsRun':0,'note':'New actual exact Illusion submission/acceptance supersedes the old UNSENT staging observation. The owner subsequently continued review in this original Part5 chat. Routing-only receipts do not override this actual history. Correction package is preserved as proposed scoped authorship pending local substantive reconciliation and implementation instruction.'}
write(receipt,(json.dumps(record,ensure_ascii=False,indent=2)+'\n').encode())
print(json.dumps({'receipt':binding(receipt),'returns':[{k:v for k,v in x.items() if k!='acceptedArtifactComparisons'} for x in results],'exactArtifactsMatched':16},indent=2))
