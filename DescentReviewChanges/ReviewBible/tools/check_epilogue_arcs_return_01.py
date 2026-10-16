"""Preserve and source-check the actual campaign-arcs return; semantics remain separate."""
from pathlib import Path,PurePosixPath
from zipfile import ZipFile
from xml.etree import ElementTree as ET
from datetime import datetime,timezone
import hashlib,json,sys
from apply_di7_ap_as_01 import G,R,A,info,encoded

def read(p):return json.loads(p.read_bytes())
def sha(b):return hashlib.sha256(b).hexdigest()

def main():
    incoming=Path(sys.argv[1]);suffix=sys.argv[2] if len(sys.argv)>2 else '01'
    archive=A/f'DD_Cosmology_Epilogue_Campaign_Arcs_01_Return_{suffix}.zip'
    root=A/f'cosmology-epilogue-campaign-arcs-01-return-{suffix}'
    receipt=A/f'COSMOLOGY_EPILOGUE_CAMPAIGN_ARCS_01_RETURN_SOURCE_CHECK_{suffix}.json'
    assert all(not p.exists() for p in [archive,root,receipt])
    expected_names={'REGISTER.json','CAMPAIGN_ARCS_MODEL.json','PLAYER_CHAPTER.md','DIRECTOR_CHAPTER.md','CASEBOOK.json','SOURCE_HASHES.json','VERDICT.md','EVIDENCE_MANIFEST.json'}
    with ZipFile(incoming) as z:
        names=z.namelist();assert len(names)==len(set(names))==8 and set(names)==expected_names
        assert all(not PurePosixPath(n).is_absolute() and '..' not in PurePosixPath(n).parts for n in names)
        files={n:z.read(n) for n in names}
    archive.write_bytes(incoming.read_bytes());root.mkdir()
    for n,b in files.items():(root/n).write_bytes(b)
    checks=[];cache={};packet=A/'cosmology-epilogue-campaign-arcs-06'
    expected={x['path']:x for x in read(packet/'SOURCE_BINDINGS.json')};assert len(expected)==51
    def ck(kind,where,passed,detail=None):
        row={'kind':kind,'where':where,'passed':bool(passed)}
        if not passed:row['detail']=detail
        checks.append(row)
    manifest=read(root/'EVIDENCE_MANIFEST.json');entries=manifest.get('files',manifest.get('outputs',manifest.get('entries',[])))
    ck('exact-manifest-set','EVIDENCE_MANIFEST.json',len(entries)==7 and {x.get('path',x.get('name')) for x in entries}==expected_names-{'EVIDENCE_MANIFEST.json'})
    for e in entries:
        name=e.get('path',e.get('name'));b=files.get(name,b'');ck('output-bytes',name,len(b)==e.get('bytes') and sha(b)==e.get('sha256'))
    hashes=read(root/'SOURCE_HASHES.json');got=hashes['sources'] if isinstance(hashes,dict) else hashes
    ck('exact-source-set','SOURCE_HASHES.json',len(got)==51 and {x['path'] for x in got}==set(expected))
    for e in got:
        name=e['path']
        if name not in expected:ck('known-source',name,False);continue
        b=(packet/'sources'/name).read_bytes();ck('frozen-source',name,e==expected[name] and len(b)==e['bytes'] and sha(b)==e['sha256'])
    def walk(v,where):
        if isinstance(v,dict):
            if 'path' in v and any(k in v for k in ['paragraphIndexZeroBased','jsonPointer','firstLineOneBased','lineOneBased']):
                try:
                    name=v['path'];assert name in expected,'Not in supplied51-source set';p=packet/'sources'/name;actual=None
                    if 'paragraphIndexZeroBased' in v:
                        key=(name,v.get('part','word/document.xml'))
                        if key not in cache:
                            with ZipFile(p) as z:xml=ET.fromstring(z.read(key[1]))
                            ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
                            cache[key]=[''.join(t.text or '' for t in q.findall('.//w:t',ns)) for q in xml.findall('.//w:p',ns)]
                        actual=cache[key][v['paragraphIndexZeroBased']]
                    elif 'jsonPointer' in v:
                        node=read(p);pointer=v['jsonPointer']
                        if pointer:
                            assert pointer.startswith('/')
                            for k in pointer[1:].split('/'):
                                k=k.replace('~1','/').replace('~0','~');node=node[int(k)] if isinstance(node,list) else node[k]
                        ck('json-value' if 'value' in v else 'json-pointer-resolves',where,'value' not in v or node==v['value'])
                    else:
                        lines=p.read_text(encoding='utf-8-sig').splitlines();lo=v.get('firstLineOneBased',v.get('lineOneBased'));hi=v.get('lastLineOneBased',lo)
                        assert 1<=lo<=hi<=len(lines);actual='\n'.join(lines[lo-1:hi])
                    if actual is not None:
                        if 'excerpt' in v:ck('exact-excerpt',where,actual==v['excerpt'],{'actual':actual,'citation':v})
                        if 'textSha256' in v:ck('exact-location-hash',where,sha(actual.encode())==v['textSha256'],{'actualSha256':sha(actual.encode()),'citation':v})
                        if not any(k in v for k in ['excerpt','textSha256']):ck('location-only',where,True)
                except Exception as e:ck('citation-resolves',where,False,repr(e))
            for k,x in v.items():walk(x,where+'/'+k)
        elif isinstance(v,list):
            for i,x in enumerate(v):walk(x,where+'/'+str(i))
    for n in ['REGISTER.json','CAMPAIGN_ARCS_MODEL.json','CASEBOOK.json']:walk(read(root/n),n)
    oldids=[x['id'] for x in read(packet/'CASEBOOK.json')['cases']];newids=[x['id'] for x in read(root/'CASEBOOK.json')['cases']]
    ck('original67-case-ids-preserved','CASEBOOK.json',set(oldids)<=set(newids),sorted(set(oldids)-set(newids)))
    ck('original-case-relative-order','CASEBOOK.json',[x for x in newids if x in set(oldids)]==oldids)
    ck('six-integration-cases','CASEBOOK.json',{f'ARCX-{i:02}' for i in range(1,7)}<=set(newids))
    ck('unique-at-least73-cases','CASEBOOK.json',len(newids)==len(set(newids)) and len(newids)>=73)
    fails=[x for x in checks if not x['passed']]
    receipt.write_bytes(encoded({'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'archive':info(archive),'submittedPacket':info(A/'DD_Cosmology_Epilogue_Campaign_Arcs_06.zip'),'checks':checks,'checkCount':len(checks),'failureCount':len(fails),'failures':fails,'sourceIntegrityOnly':True,'semanticReview':'PENDING independent full review of source fidelity, executable completeness, meaningful adventure design and cross-module correctness.','newRulesAdopted':False,'runtimeTestsExecuted':0,'humanPlaytested':False,'sourceInformationDeleted':0}))
    print(json.dumps({'receipt':info(receipt),'archive':info(archive),'checks':len(checks),'failures':len(fails),'firstFailures':fails[:6]}))

if __name__=='__main__':main()
