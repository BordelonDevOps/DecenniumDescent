"""Verify actual current04 return bytes and preserve them; adopt no rules."""
from datetime import datetime,timezone
from pathlib import Path,PurePosixPath
import hashlib,json,zipfile
from apply_di7_ap_as_01 import G,R,A,info,encoded

def main():
 downloaded=Path(r'C:\Users\cbord\Downloads\DD_Companion_Life_10_Current_04_Review.zip');archive=A/downloaded.name;root=A/'companion-life10-current04-review';receipt=A/'COMPANION_LIFE_10_CURRENT_04_RETURN_RECEIPT.json'
 assert not any(p.exists() for p in [archive,root,receipt])
 raw=downloaded.read_bytes();assert len(raw)==235978 and hashlib.sha256(raw).hexdigest()=='9890d5b6f4c8d3a0699304a175dcb10510f939bf5b85d09cf520c9e7109733d6'
 nativep=A/'COMPANION_LIFE_10_CURRENT_04_ACTUAL_GPT_FINAL.json';native=json.loads(nativep.read_bytes());messages=[m for t in native['turns'] for m in t['items'] if m.get('type')=='agentMessage' and m.get('id')=='a3ef8d40-93f2-475d-b8af-9eed34023d60'];assert len(messages)==1 and hashlib.sha256(raw).hexdigest() in messages[0]['text']
 checks=[]
 with zipfile.ZipFile(downloaded) as z:
  names=z.namelist();assert len(names)==len(set(names))==8 and z.testzip() is None
  for n in names:
   p=PurePosixPath(n);assert not p.is_absolute() and '..' not in p.parts and len(p.parts)==1 and '\\' not in n
  manifest=json.loads(z.read('EVIDENCE_MANIFEST.json'));expected=manifest['reviewedArchive'];actual=info(A/expected['name']);assert all(actual[k]==expected[k] for k in ['bytes','sha256'])
  assert info(G/manifest['reviewedCandidate']['path'])==manifest['reviewedCandidate']
  for f in manifest['files']:
   b=z.read(f['name']);assert len(b)==f['bytes'] and hashlib.sha256(b).hexdigest()==f['sha256'];checks.append({**f,'verified':True})
  assert len(checks)==7
  proposal=json.loads(z.read('PROPOSED_CORRECTIONS.json'));review=json.loads(z.read('REVIEW.json'));sv=json.loads(z.read('SOURCE_VERIFICATION.json'))
  assert info(G/proposal['targetCandidate']['path'])==proposal['targetCandidate']
  assert len(proposal['operations'])==9 and len(review['perSpellDispositions'])==10 and len(review['clarificationDispositions'])==5 and len(review['perCaseDispositions'])==27
  archive.write_bytes(raw);root.mkdir()
  for n in names:(root/n).write_bytes(z.read(n))
 receipt.write_bytes(encoded({'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'actualChat':'Review Continuation Part 4','actualThreadId':'6ad1acef-455c-83ea-bc33-56e4adaec9c8','actualUserMessageId':'3215cb75-04cf-48fb-8d6b-9dbc93d04850','actualAssistantMessageId':'a3ef8d40-93f2-475d-b8af-9eed34023d60','actualNativeFinal':info(nativep),'inputArchive':actual,'inputCandidate':proposal['targetCandidate'],'returnedArchive':info(archive),'returnedFiles':[info(root/n) for n in names],'manifestVerification':checks,'verdict':review['verdict'],'procedureCount':10,'clarificationQuestionCount':5,'currentMainCases':27,'historicalScenarios':20,'proposedOperations':9,'historicalSourceLimitation':sv.get('historicalReferenceSummary'),'correctionsApplied':False,'newRuleAdoptions':0,'runtimeTestsExecuted':0,'sourceInformationDeleted':0,'liveMembershipQualification':'Actual GPT final correctly did not infer application of Persistent20 from earlier intent. Live verified525/323/249 supersedes the quoted505/343/229 progress snapshot only; the returned review bytes are preserved unchanged.','scope':'Verified actual final/source-conference return preserved. Full local semantic inspection, reversible successor application and final exact integration review remain; Command Undeath exactCR2 whole-case holds remain.'}))
 print(json.dumps({'receipt':info(receipt),'archive':info(archive),'verifiedFiles':7,'proposedOperations':9}))

if __name__=='__main__':main()
