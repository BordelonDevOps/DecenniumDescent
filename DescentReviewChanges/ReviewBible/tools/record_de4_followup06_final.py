"""Preserve the downloaded final Director report and verify its exact identities."""
from datetime import datetime, timezone
import json, hashlib, zipfile
from pathlib import Path
from apply_di7_ap_as_01 import G,R,A,info,encoded

def main():
 src=Path('C:/Users/cbord/Downloads/DD_DE4_Review_Followup_06_Review.zip');dest=A/src.name;out=A/'de4-review-followup-06-review-final';receipt=A/'DE4_REVIEW_FOLLOWUP_06_FINAL_RECEIPT.json'
 assert not dest.exists() and not out.exists() and not receipt.exists()
 raw=src.read_bytes();assert len(raw)==34683 and hashlib.sha256(raw).hexdigest()=='40dee719099012a8491a96c123f487bd55ce193a31a3c76807c1eb0236cdb4a9'
 native=A/'DE4_REVIEW_FOLLOWUP_06_FINAL_NATIVE.json';nt=native.read_text(encoding='utf-8');assert '72260b80-d940-4e87-b0a9-a4c88ffd2501' in nt and hashlib.sha256(raw).hexdigest() in nt
 with zipfile.ZipFile(src) as z:
  names=z.namelist();assert sorted(names)==sorted(['REVIEW.json','VERDICT.md','PROPOSED_CORRECTIONS.json','SOURCE_VERIFICATION.json','EVIDENCE_MANIFEST.json']);assert z.testzip() is None
  manifest=json.loads(z.read('EVIDENCE_MANIFEST.json'))
  for b in manifest['files']:
   data=z.read(b['name']);assert len(data)==b['bytes'] and hashlib.sha256(data).hexdigest()==b['sha256']
  out.mkdir()
  for name in names:(out/name).write_bytes(z.read(name))
 dest.write_bytes(raw)
 receipt.write_bytes(encoded({'id':'DE4-REVIEW-FOLLOWUP-06-FINAL-RECEIPT','recordedAtUtc':datetime.now(timezone.utc).isoformat(),'threadId':'6ad1acef-455c-83ea-bc33-56e4adaec9c8','assistantMessageId':'72260b80-d940-4e87-b0a9-a4c88ffd2501','archive':info(dest),'nativeEvidence':info(native),'verifiedPayloads':[info(out/n) for n in names],'verdict':'Four substantive deltas agreed; one exact N04 wording correction remains. Final rebound files not accepted.','activeFilesModified':0,'counts':{'reviewed':465,'pending':383}}))
 print(json.dumps({'receipt':info(receipt),'corrections':json.loads((out/'PROPOSED_CORRECTIONS.json').read_bytes()),'reviewKeys':list(json.loads((out/'REVIEW.json').read_bytes()))},ensure_ascii=False))

if __name__=='__main__':main()
