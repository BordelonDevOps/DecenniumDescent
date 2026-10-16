"""Preserve the actual AC4 return and verify identities/sources; semantic review is separate."""
from datetime import datetime,timezone
from pathlib import Path
from zipfile import ZipFile
import hashlib,json
from apply_di7_ap_as_01 import G,R,A,info,encoded
def read(p):return json.loads(p.read_bytes())
def sha(raw):return hashlib.sha256(raw).hexdigest()

def main():
    incoming=Path(r'C:\Users\cbord\Downloads\DD_AC4_Current_Review_01_Return.zip')
    archive=A/'DD_AC4_Current_Review_01_Return_01.zip';root=A/'ac4-current-review-01-return-01';receipt=A/'AC4_CURRENT_REVIEW_01_RETURN_SOURCE_CHECK_01.json'
    assert not any(p.exists() for p in [archive,root,receipt])
    raw=incoming.read_bytes();assert len(raw)==60991 and sha(raw)=='0f12daaf4b39e3d830cdf6b7dd3d20d9f50b4cdd0523ffdb4fdce104be9bf6fa'
    expected_names={'REGISTER.json','SPELLS_MODEL.json','PLAYER_CHAPTER.md','DIRECTOR_REVIEW.md','CASEBOOK.json','SOURCE_HASHES.json','VERDICT.md','EVIDENCE_MANIFEST.json'}
    with ZipFile(incoming) as z:
        assert len(z.namelist())==8 and set(z.namelist())==expected_names
        files={name:z.read(name) for name in z.namelist()}
    archive.write_bytes(raw);root.mkdir()
    for name,raw in files.items():(root/name).write_bytes(raw)
    model=read(root/'SPELLS_MODEL.json');cases=read(root/'CASEBOOK.json');manifest=read(root/'EVIDENCE_MANIFEST.json');sources=read(root/'SOURCE_HASHES.json')
    supplied=read(A/'ac4-current-review-01-input/CURRENT_REVIEW_INPUT.json');expected={x['path']:x for x in supplied['sourceBindings']};checks=[]
    def ck(name,ok,details=None):
        item={'name':name,'passed':bool(ok)}
        if not ok:item['detail']=details
        checks.append(item)
    ck('Exact seven-output manifest',len(manifest['outputFiles'])==7 and {x['path'] for x in manifest['outputFiles']}==expected_names-{'EVIDENCE_MANIFEST.json'})
    for binding in manifest['outputFiles']:
        content=files[binding['path']];ck('Output bytes '+binding['path'],len(content)==binding['bytes'] and sha(content)==binding['sha256'])
    ck('Exact70 source bindings',len(sources['bindings'])==70 and {x['path']:x for x in sources['bindings']}==expected)
    with ZipFile(A/'DD_AC4_Current_Review_01.zip') as z:
        for binding in sources['bindings']:
            content=z.read('sources/'+binding['path']);ck('Frozen source '+binding['path'],len(content)==binding['bytes'] and sha(content)==binding['sha256'])
    current_drift=[{'submitted':b,'current':info(G/b['path'])} for b in expected.values() if info(G/b['path'])!=b]
    ck('All70 current sources unchanged',not current_drift,current_drift)
    originals={x['spellId']:x for x in supplied['records']}
    ck('All15 spell IDs/order',[x['spellId'] for x in model['spells']]==[x['spellId'] for x in supplied['records']])
    for row in model['spells']:
        before=originals[row['spellId']]
        ck(row['spellId']+' exact full source/access record',row['sourceAndAccess']==before['fullSourceAndCurrentAccessRecord'])
        ck(row['spellId']+' original source hash',row['sourceRecordSha256']==before['sourceRecordSha256'])
        ck(row['spellId']+' original question identity',row['questionId']==before['questionId'])
        ck(row['spellId']+' complete procedure nonempty',isinstance(row['procedure'],str) and len(row['procedure'])>300)
    wanted=supplied['originalExamples'];ids=[x['id'] for x in cases['cases']]
    ck('All45 unique case IDs',len(ids)==len(set(ids))==45)
    ck('All30 original IDs/order',ids[:30]==[x['id'] for x in wanted])
    for old,new in zip(wanted,cases['cases'][:30]):ck(old['id']+' original example text',new['originalText']==old['originalText'])
    ck('All15 integration example IDs',ids[30:]==[x['id'] for x in supplied['requestedIntegrationExamples']])
    ck('Banishment receipt preserved',model['banishmentSourceOnlyReceipt']==supplied['banishmentSourceOnlyReceipt'])
    failures=[x for x in checks if not x['passed']]
    rec={'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'archive':info(archive),'submittedArchive':info(A/'DD_AC4_Current_Review_01.zip'),'checks':checks,'checkCount':len(checks),'failureCount':len(failures),'failures':failures,'sourceIntegrityOnly':True,'semanticReview':'Pending independent reading of all15 complete procedures, current shared interfaces, all45 examples, both chapters and all dispositions.','newRulesAdopted':False,'sourceInformationDeleted':0,'runtimeTestsExecuted':0,'humanPlaytested':False}
    receipt.write_bytes(encoded(rec));print(json.dumps({'receipt':info(receipt),'checks':len(checks),'failures':len(failures),'firstFailures':failures[:5]}))

if __name__=='__main__':main()
