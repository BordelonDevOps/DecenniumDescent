"""Preserve actual final and exact artifact acceptance without applying membership."""
from datetime import datetime,timezone
from pathlib import Path
import hashlib,json,zipfile
from apply_di7_ap_as_01 import G,R,A,info,encoded

def main():
 downloaded=Path(r'C:\Users\cbord\Downloads\DD_Damage_Control_25_Exact_Rebound_10_Review.zip'); archive=A/downloaded.name; root=A/'damage-control25-exact10-review'; receipt=A/'DAMAGE_CONTROL_25_EXACT10_RETURN_RECEIPT.json'
 assert not any(p.exists() for p in [archive,root,receipt])
 raw=downloaded.read_bytes(); assert len(raw)==42399 and hashlib.sha256(raw).hexdigest()=='17833f27e7b5b2f189045266a460236dc5bdf90466b615eeab5678990e5ccc8e'
 nativep=A/'DAMAGE_CONTROL_25_EXACT_REBOUND_10_ACTUAL_GPT_FINAL.json'; native=json.loads(nativep.read_bytes()); turn=native['turns'][0]; reply=next(m for m in turn['items'] if m.get('type')=='agentMessage'); assert turn['id']=='3e0faf42-f4a2-431f-9456-24c212a66cab' and reply['id']=='81bee90e-0066-41fc-a719-4d47ec46af01' and hashlib.sha256(raw).hexdigest() in reply['text']
 checks=[]
 with zipfile.ZipFile(downloaded) as z:
  assert sorted(z.namelist())==['EVIDENCE_MANIFEST.json','REVIEW.json','SOURCE_VERIFICATION.json','VERDICT.md'] and z.testzip() is None
  manifest=json.loads(z.read('EVIDENCE_MANIFEST.json')); review=json.loads(z.read('REVIEW.json'))
  for b in manifest['files']:
   d=z.read(b['name']); assert len(d)==b['bytes'] and hashlib.sha256(d).hexdigest()==b['sha256']; checks.append(dict(b,verified=True))
  assert review['verdict']=='ACCEPT_BYTE_IDENTICAL_FOR_PROVISIONAL_AUTHORED_DAMAGE_CONTROL25_VIDEO_GAME_CANDIDATE' and review['verdict'] in reply['text'] and review['remainingBlockingFindingCount']==0 and review['candidateCanRemainByteIdentical'] and not review['candidateReserializedOrModified']
  assert review['acceptedArtifactBindings']==manifest['acceptedCandidateFiles'] and len(review['acceptedArtifactBindings'])==8
  submitted=A/review['reviewedArchive']['name']; assert all(info(submitted)[k]==review['reviewedArchive'][k] for k in ['bytes','sha256'])
  with zipfile.ZipFile(submitted) as inp:
   for b in review['acceptedArtifactBindings']:
    p=A/'damage-control25-exact-rebound-10'/b['name']; assert inp.read(b['archivePath'])==p.read_bytes() and all(info(p)[k]==b[k] for k in ['bytes','sha256']); checks.append(dict(b,verified=True))
  archive.write_bytes(raw);root.mkdir()
  for n in z.namelist():(root/n).write_bytes(z.read(n))
 receipt.write_bytes(encoded({'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'actualThreadId':native['thread']['id'],'actualUserMessageId':turn['id'],'actualAssistantMessageId':reply['id'],'actualNativeFinal':info(nativep),'reviewedArchive':info(submitted),'returnedArchive':info(archive),'returnedFiles':[info(p) for p in sorted(root.iterdir())],'acceptedArtifactBindings':review['acceptedArtifactBindings'],'verdict':review['verdict'],'checks':checks,'sourceInformationDeleted':0,'membershipApplied':False,'runtimeTestsExecuted':0,'scope':'Actual bounded authored acceptance verified and preserved; separately verified byte copies and membership application remain.'})); print(json.dumps({'receipt':info(receipt),'verifiedBindings':len(checks),'verdict':review['verdict']}))

if __name__=='__main__':main()
