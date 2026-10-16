"""Check exact files/citations; gameplay critique remains a separate model review."""
from datetime import datetime,timezone
from zipfile import ZipFile
from xml.etree import ElementTree as E
import hashlib,json,sys
from apply_di7_ap_as_01 import G,R,A,info,encoded

def read(p):return json.loads(p.read_bytes())

def main():
    suffix=sys.argv[1] if len(sys.argv)>1 else '01'
    source_suffix=sys.argv[2] if len(sys.argv)>2 else suffix
    root=A/('cosmology-souls-research-01-return' if source_suffix=='01' else 'cosmology-souls-research-01-return-'+source_suffix)
    frozen=A/'cosmology-souls-research-01/sources';checks=[];cache={}
    def check(kind,where,ok,detail=None):
        x={'kind':kind,'location':where,'passed':bool(ok)}
        if not ok:x['detail']=detail
        checks.append(x)
    manifest=read(root/'EVIDENCE_MANIFEST.json')
    manifest_rows=manifest.get('files',manifest.get('outputs',manifest.get('entries',[])))
    for row in manifest_rows:
        name=row.get('path',row.get('name'))
        p=root/name;check('output-file',name,p.stat().st_size==row['bytes'] and hashlib.sha256(p.read_bytes()).hexdigest()==row['sha256'])
    check('manifest-count','EVIDENCE_MANIFEST.json',len(manifest_rows)==7)
    expected={x['path']:x for x in read(A/'cosmology-souls-research-01/SOURCE_BINDINGS.json')}
    for row in read(root/'SOURCE_HASHES.json')['sources']:
        p=frozen/row['path'];check('frozen-source',row['path'],row==expected[row['path']] and p.stat().st_size==row['bytes'] and hashlib.sha256(p.read_bytes()).hexdigest()==row['sha256'])
    def walk(v,where):
        if isinstance(v,dict):
            if 'path' in v and any(k in v for k in ['paragraphIndexZeroBased','jsonPointer','firstLineOneBased','lineOneBased']):
                p=frozen/v['path']
                try:
                    if 'paragraphIndexZeroBased' in v:
                        key=(v['path'],v.get('part','word/document.xml'))
                        if key not in cache:
                            with ZipFile(p) as z:doc=E.fromstring(z.read(key[1]))
                            ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
                            cache[key]=[''.join(t.text or '' for t in q.findall('.//w:t',ns)) for q in doc.findall('.//w:p',ns)]
                        actual=cache[key][v['paragraphIndexZeroBased']];check('paragraph',where,actual==v['excerpt'],{'citation':v,'actual':actual})
                    elif 'jsonPointer' in v:
                        actual=read(p)
                        for t in v['jsonPointer'].strip('/').split('/'):
                            t=t.replace('~1','/').replace('~0','~');actual=actual[int(t)] if isinstance(actual,list) else actual[t]
                        check('json-value' if 'value' in v else 'pointer-resolves',where,'value' not in v or actual==v['value'],{'citation':v})
                    else:
                        lo=v.get('firstLineOneBased',v.get('lineOneBased'));hi=v.get('lastLineOneBased',lo)
                        actual='\n'.join(p.read_text(encoding='utf-8-sig').splitlines()[lo-1:hi])
                        check('text-excerpt',where,actual==v['excerpt'],{'citation':v,'actual':actual})
                except Exception as ex:check('citation-resolves',where,False,{'citation':v,'error':repr(ex)})
            for k,w in v.items():walk(w,where+'/'+k)
        elif isinstance(v,list):
            for i,w in enumerate(v):walk(w,where+'/'+str(i))
    for n in ['REGISTER.json','RESEARCH_ROUTE_AND_STATE_MODEL.json','CASEBOOK.json','SEMANTIC_COVERAGE.json']:walk(read(root/n),n)
    reg=read(root/'REGISTER.json');cases=read(root/'CASEBOOK.json')
    check('issue-count','REGISTER.json',len(reg['issues'])==21)
    check('case-count','CASEBOOK.json',len(cases['suppliedCases'])==34 and len(cases['additionalProposedEdgeCases'])>=8)
    check('no-test-certification','CASEBOOK.json',not cases['executedAsSoftwareTests'] and not cases['humanPlaytested'])
    failures=[x for x in checks if not x['passed']]
    receipt=A/f'COSMOLOGY_SOULS_RESEARCH_01_RETURN_SOURCE_CHECK_{suffix}.json';assert not receipt.exists()
    receipt.write_bytes(encoded({'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'checks':checks,'checkCount':len(checks),'failureCount':len(failures),'failures':failures,'sourceVerificationOnly':True,'gameplayDesignAdopted':False,'sourceInformationDeleted':0}))
    print(json.dumps({'checkCount':len(checks),'failureCount':len(failures),'failures':failures,'receipt':info(receipt)},ensure_ascii=False))

if __name__=='__main__':main()
