"""Preserve actual GPT final and verify returned files; apply no proposal."""
from datetime import datetime,timezone
from pathlib import Path,PurePosixPath
import hashlib,json,zipfile
from apply_di7_ap_as_01 import G,R,A,info,encoded

def main():
    downloaded=Path(r'C:\Users\cbord\Downloads\DD_Companion_Life_10_Conference_01_Review.zip');archive=A/downloaded.name;root=A/'companion-life10-conference-01-review';receipt=A/'COMPANION_LIFE_10_CONFERENCE_01_RECEIPT.json'
    assert all(not p.exists() for p in [archive,root,receipt])
    raw=downloaded.read_bytes();assert len(raw)==223884 and hashlib.sha256(raw).hexdigest()=='2adf97d06f236ff00f49bc9071bf89695a2d592d10d6c2a2566610f2dba5a70a'
    nativep=A/'COMPANION_LIFE_10_CONFERENCE_01_ACTUAL_GPT_FINAL.json';native=json.loads(nativep.read_bytes());messages=[m for t in native['turns'] for m in t['items'] if m.get('type')=='agentMessage' and m.get('id')=='d3bf83fd-f019-4c50-803c-2026bcbd8a69'];assert len(messages)==1 and hashlib.sha256(raw).hexdigest() in messages[0]['text']
    checks=[]
    with zipfile.ZipFile(downloaded) as z:
        names=z.namelist();assert len(names)==len(set(names))==8 and z.testzip() is None
        for n in names:
            p=PurePosixPath(n);assert not p.is_absolute() and '..' not in p.parts and len(p.parts)==1 and '\\' not in n
        manifest=json.loads(z.read('EVIDENCE_MANIFEST.json'));expected=manifest['inputArchive'];actual=info(A/expected['name']);assert actual['bytes']==expected['bytes'] and actual['sha256']==expected['sha256']
        for f in manifest['outputFiles']:
            b=z.read(f['name']);assert len(b)==f['bytes'] and hashlib.sha256(b).hexdigest()==f['sha256'];checks.append({**f,'verified':True})
        proposal=json.loads(z.read('PROPOSED_CORRECTIONS.json'));review=json.loads(z.read('REVIEW.json'));case=json.loads(z.read('CASE_DEVELOPMENT.json'));assert info(G/proposal['targetCandidate']['path'])==proposal['targetCandidate']
        assert len(review['perSpellDispositions'])==10 and len(review['conferenceDispositions'])==16 and len(review['originalQuestionDispositions'])==10 and len(proposal['operations'])==11 and len(case['cases'])==20
        archive.write_bytes(raw);root.mkdir()
        for n in names:(root/n).write_bytes(z.read(n))
    receipt.write_bytes(encoded({'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'actualChat':'Review Continuation Part 4','actualThreadId':'6ad1acef-455c-83ea-bc33-56e4adaec9c8','actualUserMessageId':'e064c030-16dc-47a0-85d0-e361fdef35b1','actualAssistantMessageId':'d3bf83fd-f019-4c50-803c-2026bcbd8a69','actualNativeFinal':info(nativep),'inputArchive':actual,'inputCandidate':proposal['targetCandidate'],'returnedArchive':info(archive),'returnedFiles':[info(root/n) for n in names],'manifestVerification':checks,'verdict':review['verdict'],'procedureCount':10,'conferenceQuestionCount':16,'originalQuestionCount':10,'preservedScenarioCount':20,'proposedOperations':11,'correctionsApplied':False,'newRuleAdoptions':0,'runtimeTestsExecuted':0,'sourceInformationDeleted':0,'scope':'Actual final/source-conference return verified and preserved. Local full semantic inspection, reversible proposal application, complete current cases and final exact review remain.'}));print(json.dumps({'receipt':info(receipt),'archive':info(archive),'verifiedFiles':len(checks),'proposedOperations':11}))

if __name__=='__main__':main()
