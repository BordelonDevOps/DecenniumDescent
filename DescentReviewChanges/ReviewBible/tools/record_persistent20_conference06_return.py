"""Preserve and verify the actual GPT final return without applying corrections."""
from datetime import datetime, timezone
from pathlib import PurePosixPath
import hashlib, json, zipfile
from apply_di7_ap_as_01 import G, R, A, info, encoded


def main():
    archive = A / 'DD_Persistent_Damage_20_Conference_06_Review.zip'
    root = A / 'persistent-damage20-conference-06-review'
    receipt = A / 'PERSISTENT_DAMAGE_20_CONFERENCE_06_RECEIPT.json'
    assert not root.exists() and not receipt.exists()
    b = info(archive)
    assert b['bytes'] == 117073 and b['sha256'] == 'c567ba4e158f148a6bebc3dcce85eac5672d8d2c2e8603fa3b4678a4489de778'
    nativepath = A / 'PERSISTENT_DAMAGE_20_CONFERENCE_06_ACTUAL_GPT_FINAL.json'
    native = json.loads(nativepath.read_bytes())
    messages = [m for t in native['turns'] for m in t['items'] if m.get('type') == 'agentMessage' and m.get('id') == '0d6f943a-dd04-4129-9af8-cab561c62fc8']
    assert len(messages) == 1 and b['sha256'] in messages[0]['text']
    checks=[]
    with zipfile.ZipFile(archive) as z:
        names=z.namelist()
        assert len(names)==len(set(names))==6
        for name in names:
            p=PurePosixPath(name)
            assert not p.is_absolute() and '..' not in p.parts and len(p.parts)==1
        manifest=json.loads(z.read('EVIDENCE_MANIFEST.json'))
        for f in manifest['files']:
            raw=z.read(f['path'])
            assert len(raw)==f['bytes'] and hashlib.sha256(raw).hexdigest()==f['sha256']
            checks.append({'path':f['path'],'bytes':len(raw),'sha256':f['sha256'],'verified':True})
        for key, base in [('inputArchive',A),('inputCandidate',G)]:
            expected=manifest[key]
            actual=info(base/expected['path'])
            assert actual['bytes']==expected['bytes'] and actual['sha256']==expected['sha256']
        root.mkdir()
        for name in names:
            (root/name).write_bytes(z.read(name))
    review=json.loads((root/'REVIEW.json').read_bytes())
    proposal=json.loads((root/'PROPOSED_CORRECTIONS.json').read_bytes())
    assert len(review['procedureDispositions'])==20 and len(review['questionDispositions'])==24
    assert len(proposal['operations'])==9 and all(o['appliedToLiveCandidate'] is False for o in proposal['operations'])
    record={'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'actualChat':'Review Continuation Part 4',
            'actualThreadId':'6ad1acef-455c-83ea-bc33-56e4adaec9c8','actualUserMessageId':'28a42338-ffbd-4fb8-9a49-ec96d447762d',
            'actualAssistantMessageId':'0d6f943a-dd04-4129-9af8-cab561c62fc8','actualNativeFinal':info(nativepath),
            'inputArchive':info(A/'DD_Persistent_Damage_20_Conference_06.zip'),'returnedArchive':b,
            'returnedFiles':[info(root/name) for name in names],'manifestVerification':checks,
            'verdict':review['verdict'],'procedureCount':20,'questionCount':24,'proposedOperations':9,
            'correctionsApplied':False,'newRuleAdoptions':0,'runtimeTestsExecuted':0,'sourceInformationDeleted':0,
            'scope':'Actual final GPT conference preserved. Exact input/output/file hashes verified locally. No semantic operation applied by this receipt; geometry finding requires cross-packet example audit.'}
    receipt.write_bytes(encoded(record))
    print(json.dumps({'receipt':info(receipt),'returnedArchive':b,'verifiedFiles':len(checks),'procedures':20,'questions':24,'operations':9}))


if __name__ == '__main__':
    main()
