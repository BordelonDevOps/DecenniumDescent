"""Preserve actual GPT response and verify every source binding and quoted citation."""
from datetime import datetime, timezone
import hashlib, json, re, zipfile
from xml.etree import ElementTree as ET
from apply_di7_ap_as_01 import G, R, A, info, encoded


def norm(s): return ' '.join(s.split())


def walk(o):
    if isinstance(o,dict):
        yield o
        for v in o.values():yield from walk(v)
    elif isinstance(o,list):
        for v in o:yield from walk(v)


def strings(o):
    if isinstance(o,str):yield o
    elif isinstance(o,dict):
        for v in o.values():yield from strings(v)
    elif isinstance(o,list):
        for v in o:yield from strings(v)


def main():
    archive=A/'COSMOLOGY_OWNER_RECONCILIATION_01_Addendum_and_Evidence.zip'
    root=A/'cosmology-owner-reconciliation-01-received'
    receipt=A/'COSMOLOGY_OWNER_RECONCILIATION_01_RECEIVED_DECISION.json'
    check=A/'COSMOLOGY_OWNER_RECONCILIATION_01_APPLICATION_CHECK.json'
    assert all(not p.exists() for p in [root,receipt,check])
    assert info(archive)['sha256']=='fb025f88e14ba8c130a5e50ac1bb6097bfe47db4f3b510bc424bf89199336f6b'
    with zipfile.ZipFile(archive) as z:
        names=z.namelist(); assert len(names)==len(set(names))==7
        assert all(PathSafe(n) for n in names)
        manifest=json.loads(z.read('EVIDENCE_MANIFEST.json'))
        for row in manifest['payloads']:
            b=z.read(row['filename']); assert len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256']
        payloads={n:z.read(n) for n in names}
    bindings=json.loads((A/'cosmology-owner-reconciliation-01/CURRENT_SOURCE_BINDINGS.json').read_bytes())
    returned_bindings=json.loads(payloads['SOURCE_HASHES.json'])['entries']
    assert sorted(bindings,key=lambda r:r['path'])==sorted(returned_bindings,key=lambda r:r['path'])
    assert len(bindings)==83 and all(info(G/r['path'])==r for r in bindings)
    register=json.loads(payloads['REGISTER.json'])
    owner=json.loads((A/'COSMOLOGY_OWNER_CORRECTIONS_2026_10_15_MESSAGE_CAPTURE.json').read_bytes())['ownerMessage']
    quotes=owner['paragraphs']+[x['text'] for x in owner['listItems']]
    assert [x['id'] for x in register['items']]==[f'OC-{i:02d}' for i in range(1,12)]
    assert [x['ownerQuote'] for x in register['items']]==quotes
    cache={}; citations=[]; non_doc=[]; failures=[]
    n='{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
    objects=[register,json.loads(payloads['ADOPTION_MATRIX.json'])]
    for obj in objects:
        for row in walk(obj):
            if 'paragraphIndexZeroBased' in row and 'file' in row:
                key=(row['file'],row.get('part','word/document.xml'))
                if key not in cache:
                    with zipfile.ZipFile(G/key[0]) as z:xml=ET.fromstring(z.read(key[1]))
                    cache[key]=[''.join(t.text or '' for t in p.iter(n+'t')) for p in xml.iter(n+'p')]
                i=row['paragraphIndexZeroBased']; actual=cache[key][i]
                result={**row,'actualText':actual,'actualTextSha256':hashlib.sha256(actual.encode()).hexdigest(),'hashMatches':row['textSha256']==hashlib.sha256(actual.encode()).hexdigest(),'excerptMatches':norm(row['excerpt']) in norm(actual)}
                citations.append(result)
                if not result['hashMatches'] or not result['excerptMatches']:failures.append(result)
            elif 'sourcePath' in row and 'excerpt' in row:
                aliases={name:A/'cosmology-owner-reconciliation-01'/name for name in ['LOCAL_SOURCE_PROBE.json','EXTERNAL_HARMONY_REFERENCE.json']}
                aliases['COSMOLOGY_OWNER_RECONCILIATION_01_ENCODING_ADDENDUM.json']=A/'COSMOLOGY_OWNER_RECONCILIATION_01_ENCODING_ADDENDUM.json'
                path=aliases.get(row['sourcePath'],G/row['sourcePath']); raw=path.read_text(encoding='utf-8-sig')
                candidates=[raw]
                if path.suffix=='.json':candidates+=list(strings(json.loads(raw)))
                ok=any(norm(row['excerpt']) in norm(s) for s in candidates)
                result={**row,'resolvedSourcePath':path.relative_to(G).as_posix(),'excerptMatchesDecodedSource':ok}
                non_doc.append(result)
                if not ok:failures.append(result)
    root.mkdir()
    for name,b in payloads.items():(root/name).write_bytes(b)
    now=datetime.now(timezone.utc).isoformat()
    check.write_bytes(encoded({'reviewId':register['reviewId'],'recordedAtUtc':now,'payloadHashesVerified':len(manifest['payloads']),'sourceBindingsVerified':len(bindings),'exactOwnerQuotesVerified':len(quotes),'docxCitationOccurrences':len(citations),'uniqueDocxParagraphs':len({(x['file'],x.get('part'),x['paragraphIndexZeroBased']) for x in citations}),'docxChecks':citations,'nonDocxChecks':non_doc,'failures':failures,'editorialCorrectionRequired':[{'file':'DIRECTOR_COMPANION.md','returnedQuotedText':'The heartcell was a desperate attempt to find something that silence them, the Pact manifested the prison.','exactOwnerText':quotes[7],'issue':'Returned companion silently changes the owner typo desperte to desperate inside quotation marks and omits initial No. Use the exact owner sentence in the derived local companion; preserve returned file unchanged.'}],'sourcePriorityClarification':'Pending; no branch selected','sourceInformationDeleted':0,'fullCosmologyApproved':False,'runtimeApproved':False}))
    receipt.write_bytes(encoded({'reviewId':register['reviewId'],'recordedAtUtc':now,'status':'Terminal returned evidence preserved; application check recorded; source-priority decision remains conditional','archive':info(archive),'receivedFiles':[info(root/name) for name in names],'submission':info(A/'COSMOLOGY_OWNER_RECONCILIATION_01_SUBMISSION.json'),'applicationCheck':info(check),'sourceBindingsVerified':83,'exactOwnerQuotesVerified':11,'citationFailures':len(failures),'dependentAuthorshipAdopted':False,'sourceInformationDeleted':0,'laterLocalArchiveProbeNotReviewedByGpt':info(A/'COSMOLOGY_OWNER_RECONCILIATION_01_ARCHIVE_INDEX_CHECK.json')}))
    print(json.dumps({'receipt':info(receipt),'check':info(check),'docxOccurrences':len(citations),'nonDocxOccurrences':len(non_doc),'failures':failures,'remainingDependencies':register['remainingDependencies']}))


def PathSafe(name): return '/' not in name and '\\' not in name and name not in ['.','..']


if __name__=='__main__':main()
