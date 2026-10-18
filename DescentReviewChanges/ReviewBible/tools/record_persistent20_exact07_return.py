"""Preserve actual persistent20 exact07 final and verify all accepted raw bytes."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,zipfile
from apply_di7_ap_as_01 import G,R,A,info,encoded

def main():
 downloaded=Path(r'C:\Users\cbord\Downloads\DD_Persistent_Damage_20_Exact_Rebound_07_Review.zip');archive=A/downloaded.name;root=A/'persistent-damage20-exact07-review';receipt=A/'PERSISTENT_DAMAGE_20_EXACT07_RETURN_RECEIPT.json'
 assert not any(p.exists() for p in [archive,root,receipt]);raw=downloaded.read_bytes();sha=hashlib.sha256(raw).hexdigest();assert len(raw)==47448 and sha=='25b2b40fab9677f69c8231681a2ced54b69fa34560520e72d3821fd99deda63e'
 nativep=A/'PERSISTENT_DAMAGE_20_EXACT_REBOUND_07_ACTUAL_GPT_FINAL.json';native=json.loads(nativep.read_bytes());turn=native['turns'][0];reply=next(i for i in turn['items'] if i['type']=='agentMessage');assert turn['id']=='82f23f2f-dc41-4814-9d0f-ec6c331ee127' and reply['id']=='83efadaa-6cfb-4a89-b9c9-1fc6b354392a' and sha in reply['text']
 checks=[]
 with zipfile.ZipFile(downloaded) as z:
  assert sorted(z.namelist())==['EVIDENCE_MANIFEST.json','REVIEW.json','SOURCE_VERIFICATION.json','VERDICT.md'] and z.testzip() is None
  manifest=json.loads(z.read('EVIDENCE_MANIFEST.json'));review=json.loads(z.read('REVIEW.json'))
  for b in manifest['files']:
   d=z.read(b['name']);assert len(d)==b['bytes'] and hashlib.sha256(d).hexdigest()==b['sha256'];checks.append(dict(b,verified=True))
  assert review['verdict']=='ACCEPT_BYTE_IDENTICAL_FOR_PROVISIONAL_AUTHORED_PERSISTENT_DAMAGE20_VIDEO_GAME_CANDIDATE' and review['verdict'] in reply['text'] and not review['requiredCorrections'] and not review['remainingBlockingFindings'] and review['candidateCanRemainByteIdentical']
  assert review['acceptedArtifactBindings']==manifest['acceptedCandidateFiles'] and len(review['acceptedArtifactBindings'])==8
  submitted=A/review['reviewedInputArchive']['name'];assert all(info(submitted)[k]==review['reviewedInputArchive'][k] for k in ['bytes','sha256'])
  with zipfile.ZipFile(submitted) as inp:
   for b in review['acceptedArtifactBindings']:
    p=A/'persistent-damage20-exact-rebound-07'/b['name'];assert inp.read(b['archivePath'])==p.read_bytes() and all(info(p)[k]==b[k] for k in ['bytes','sha256']);checks.append(dict(b,verified=True))
  archive.write_bytes(raw);root.mkdir()
  for n in z.namelist():(root/n).write_bytes(z.read(n))
 receipt.write_bytes(encoded({'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'actualThreadId':native['thread']['id'],'actualUserMessageId':turn['id'],'actualAssistantMessageId':reply['id'],'actualNativeFinal':info(nativep),'reviewedArchive':info(submitted),'returnedArchive':info(archive),'returnedFiles':[info(p) for p in sorted(root.iterdir())],'acceptedArtifactBindings':review['acceptedArtifactBindings'],'verdict':review['verdict'],'checks':checks,'sourceInformationDeleted':0,'membershipApplied':False,'runtimeTestsExecuted':0,'scope':'Actual exact authored acceptance preserved and verified. Separately checked installation and current-index update remain.'}));print(json.dumps({'receipt':info(receipt),'verifiedBindings':len(checks),'verdict':review['verdict']}))

if __name__=='__main__':main()
