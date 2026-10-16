"""Check the returned archive and frozen citations, separately from semantic review."""
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from zipfile import ZipFile
from xml.etree import ElementTree as ET
import hashlib,json,sys
from apply_di7_ap_as_01 import G,R,A,info,encoded

EXPECTED={'REGISTER.json','EPILOGUE_CHARACTER_MODEL.json','PLAYER_CHAPTER.md','DIRECTOR_CHAPTER.md','CASEBOOK.json','SOURCE_HASHES.json','VERDICT.md','EVIDENCE_MANIFEST.json'}

def read(p):return json.loads(p.read_bytes())
def sha(b):return hashlib.sha256(b).hexdigest()

def main():
    incoming=Path(sys.argv[1]);suffix=sys.argv[2] if len(sys.argv)>2 else '01'
    archive=A/f'DD_Cosmology_Epilogue_Character_01_Return_{suffix}.zip'
    root=A/('cosmology-epilogue-character-01-return'+('' if suffix=='01' else '-'+suffix))
    receipt=A/f'COSMOLOGY_EPILOGUE_CHARACTER_01_RETURN_SOURCE_CHECK_{suffix}.json'
    assert incoming.is_file() and all(not p.exists() for p in [archive,root,receipt])
    raw=incoming.read_bytes()
    with ZipFile(incoming) as z:
        names=z.namelist();assert len(names)==len(set(names))==8 and set(names)==EXPECTED,names
        assert all(not PurePosixPath(n).is_absolute() and '..' not in PurePosixPath(n).parts for n in names)
        payloads={n:z.read(n) for n in names}
    archive.write_bytes(raw);root.mkdir()
    for name,b in payloads.items():(root/name).write_bytes(b)
    checks=[];cache={};packet=A/'cosmology-epilogue-character-01';frozen=packet/'sources'
    def check(kind,where,passed,detail=None):
        row={'kind':kind,'where':where,'passed':bool(passed)}
        if not passed:row['detail']=detail
        checks.append(row)
    manifest=read(root/'EVIDENCE_MANIFEST.json');entries=manifest.get('files',manifest.get('outputs',manifest.get('entries',[])))
    check('manifest-exact-output-set','EVIDENCE_MANIFEST.json',len(entries)==7 and {v.get('path',v.get('name')) for v in entries}==EXPECTED-{'EVIDENCE_MANIFEST.json'})
    for e in entries:
        name=e.get('path',e.get('name'));actual=payloads.get(name,b'')
        check('output-file',str(name),len(actual)==e.get('bytes') and sha(actual)==e.get('sha256'))
    expected={v['path']:v for v in read(packet/'SOURCE_BINDINGS.json')};got=read(root/'SOURCE_HASHES.json')['sources']
    check('exact-source-set','SOURCE_HASHES.json',len(got)==len(expected)==60 and {v['path'] for v in got}==set(expected))
    for e in got:
        name=e['path']
        if name not in expected:check('unknown-source',name,False);continue
        actual=(frozen/name).read_bytes();check('frozen-source',name,e==expected[name] and len(actual)==e['bytes'] and sha(actual)==e['sha256'])
    def walk(value,where):
        if isinstance(value,dict):
            if 'path' in value and any(k in value for k in ['paragraphIndexZeroBased','jsonPointer','firstLineOneBased','lineOneBased']):
                try:
                    name=value['path'];assert name in expected, 'Not a supplied frozen source'
                    p=frozen/name;actual=None
                    if 'paragraphIndexZeroBased' in value:
                        key=(name,value.get('part','word/document.xml'))
                        if key not in cache:
                            ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
                            with ZipFile(p) as z:doc=ET.fromstring(z.read(key[1]))
                            cache[key]=[''.join(t.text or '' for t in q.findall('.//w:t',ns)) for q in doc.findall('.//w:p',ns)]
                        actual=cache[key][value['paragraphIndexZeroBased']]
                    elif 'jsonPointer' in value:
                        node=read(p);pointer=value['jsonPointer']
                        if pointer:
                            assert pointer.startswith('/')
                            for part in pointer[1:].split('/'):
                                part=part.replace('~1','/').replace('~0','~');node=node[int(part)] if isinstance(node,list) else node[part]
                        check('json-value' if 'value' in value else 'json-pointer-resolves',where,'value' not in value or node==value['value'])
                    else:
                        lines=p.read_text(encoding='utf-8-sig').splitlines();lo=value.get('firstLineOneBased',value.get('lineOneBased'));hi=value.get('lastLineOneBased',lo)
                        assert 1<=lo<=hi<=len(lines)
                        actual='\n'.join(lines[lo-1:hi])
                    if actual is not None:
                        if 'excerpt' in value:check('exact-excerpt',where,actual==value['excerpt'],{'actual':actual,'citation':value})
                        if 'textSha256' in value:check('exact-location-hash',where,sha(actual.encode())==value['textSha256'],{'actualSha256':sha(actual.encode()),'citation':value})
                        if not any(k in value for k in ['excerpt','textSha256']):check('location-only',where,True)
                except Exception as ex:check('citation-resolves',where,False,repr(ex))
            for k,v in value.items():walk(v,where+'/'+k)
        elif isinstance(value,list):
            for i,v in enumerate(value):walk(v,where+'/'+str(i))
    for name in ['REGISTER.json','EPILOGUE_CHARACTER_MODEL.json','CASEBOOK.json']:walk(read(root/name),name)
    failures=[v for v in checks if not v['passed']]
    receipt.write_bytes(encoded({'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'archive':info(archive),'sourceArchive':info(A/'DD_Cosmology_Epilogue_Character_01.zip'),'checks':checks,'checkCount':len(checks),'failureCount':len(failures),'failures':failures,'sourceIntegrityOnly':True,'semanticReview':'PENDING separate review of executable completeness and cross-system correctness','newRulesAdopted':False,'runtimeTestsExecuted':0,'humanPlaytested':False,'sourceInformationDeleted':0}))
    print(json.dumps({'receipt':info(receipt),'returnArchive':info(archive),'checks':len(checks),'failures':len(failures),'firstFailures':failures[:8]},ensure_ascii=False))

if __name__=='__main__':main()
