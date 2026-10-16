"""Verify frozen files and exact locations; this does not certify route playability."""
from datetime import datetime,timezone
from zipfile import ZipFile
from xml.etree import ElementTree as E
import hashlib,json,sys
from apply_di7_ap_as_01 import G,R,A,info,encoded

def read(p):return json.loads(p.read_bytes())
def sha(b):return hashlib.sha256(b).hexdigest()

def main():
    suffix=sys.argv[1] if len(sys.argv)>1 else '01'
    source_suffix=sys.argv[2] if len(sys.argv)>2 else suffix
    root=A/('cosmology-chronology-research-route-01-return'+('' if source_suffix=='01' else '-'+source_suffix))
    packet=A/'cosmology-chronology-research-route-01';frozen=packet/'sources';checks=[];cache={}
    target=A/f'COSMOLOGY_CHRONOLOGY_RESEARCH_ROUTE_01_RETURN_SOURCE_CHECK_{suffix}.json';assert not target.exists()
    def check(kind,where,ok,detail=None):
        row={'kind':kind,'where':where,'passed':bool(ok)}
        if not ok:row['detail']=detail
        checks.append(row)
    manifest=read(root/'EVIDENCE_MANIFEST.json');entries=manifest.get('files',manifest.get('outputs',manifest.get('entries',[])))
    check('manifest-count','EVIDENCE_MANIFEST.json',len(entries)==7)
    for row in entries:
        name=row.get('path',row.get('name'));raw=(root/name).read_bytes()
        check('output-file',name,len(raw)==row['bytes'] and sha(raw)==row['sha256'])
    expected={row['path']:row for row in read(packet/'SOURCE_BINDINGS.json')};got=read(root/'SOURCE_HASHES.json')['sources']
    check('exact-source-set','SOURCE_HASHES.json',len(got)==83 and {v['path'] for v in got}==set(expected))
    for row in got:
        raw=(frozen/row['path']).read_bytes();check('frozen-source',row['path'],row==expected[row['path']] and len(raw)==row['bytes'] and sha(raw)==row['sha256'])
    def walk(v,where):
        if isinstance(v,dict):
            if 'path' in v and any(k in v for k in ['paragraphIndexZeroBased','jsonPointer','firstLineOneBased','lineOneBased']):
                try:
                    p=frozen/v['path']
                    if 'paragraphIndexZeroBased' in v:
                        key=(v['path'],v.get('part','word/document.xml'))
                        if key not in cache:
                            with ZipFile(p) as z:doc=E.fromstring(z.read(key[1]))
                            ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
                            cache[key]=[''.join(t.text or '' for t in q.findall('.//w:t',ns)) for q in doc.findall('.//w:p',ns)]
                        actual=cache[key][v['paragraphIndexZeroBased']]
                    elif 'jsonPointer' in v:
                        actual=read(p)
                        for part in v['jsonPointer'].strip('/').split('/'):
                            part=part.replace('~1','/').replace('~0','~');actual=actual[int(part)] if isinstance(actual,list) else actual[part]
                        check('json-value' if 'value' in v else 'json-pointer-resolves',where,'value' not in v or actual==v['value'])
                        actual=None
                    else:
                        lo=v.get('firstLineOneBased',v.get('lineOneBased'));hi=v.get('lastLineOneBased',lo)
                        actual='\n'.join(p.read_text(encoding='utf-8-sig').splitlines()[lo-1:hi])
                    if actual is not None:
                        if 'excerpt' in v:check('exact-excerpt',where,actual==v['excerpt'],{'actual':actual,'citation':v})
                        if 'textSha256' in v:check('exact-location-text-hash',where,sha(actual.encode('utf-8'))==v['textSha256'],{'actualHash':sha(actual.encode('utf-8')),'citation':v})
                        if 'excerpt' not in v and 'textSha256' not in v:check('location-only',where,True)
                except Exception as ex:check('citation-resolves',where,False,repr(ex))
            for k,w in v.items():walk(w,where+'/'+k)
        elif isinstance(v,list):
            for i,w in enumerate(v):walk(w,where+'/'+str(i))
    for name in ['REGISTER.json','TIMELINE_AND_RESEARCH_ROUTE.json','CASEBOOK.json','SEMANTIC_COVERAGE.json']:walk(read(root/name),name)
    reg=read(root/'REGISTER.json');model=read(root/'TIMELINE_AND_RESEARCH_ROUTE.json');cases=read(root/'CASEBOOK.json')
    check('issue-identities','REGISTER.json',{v['id'] for v in reg['issues']}=={f'CE{i:02d}' for i in range(1,9)} and len(reg['issues'])==8)
    draft=read(frozen/'DescentReviewChanges/ReviewBible/data/director/cosmology/chronology_research_sites_draft_01.json')
    check('original-case-identities','CASEBOOK.json',[v['id'] for v in cases['suppliedSituations']]==[v['id'] for v in draft['reviewSituations']])
    check('route-case-count','CASEBOOK.json',len(cases['newRouteExamples'])>=10)
    check('epilogue-identities','TIMELINE_AND_RESEARCH_ROUTE.json',[v['id'] for v in model['epilogueNextWork']]==[v['id'] for v in draft['existingEpilogueInventory']['groups']])
    failures=[v for v in checks if not v['passed']]
    target.write_bytes(encoded({'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'checks':checks,'checkCount':len(checks),'failureCount':len(failures),'failures':failures,'sourceIntegrityOnly':True,'newRulesAdopted':False,'runtimeTestsExecuted':0,'humanPlaytested':False,'sourceInformationDeleted':0}))
    print(json.dumps({'receipt':info(target),'checkCount':len(checks),'failureCount':len(failures),'failures':failures[:10]},ensure_ascii=False))

if __name__=='__main__':main()
