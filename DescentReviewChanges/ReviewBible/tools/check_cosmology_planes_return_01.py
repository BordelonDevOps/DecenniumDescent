"""Verify the frozen planes return, preserving any failures for correction."""
from datetime import datetime,timezone
from zipfile import ZipFile
from xml.etree import ElementTree as E
import hashlib,json,sys
from apply_di7_ap_as_01 import G,R,A,info,encoded

def read(p):return json.loads(p.read_bytes())

def main():
    corrected='--corrected' in sys.argv
    root=A/('cosmology-planes-01-corrected-return' if corrected else 'cosmology-planes-01-return');frozen=A/'cosmology-planes-01'/'sources'
    manifest=read(root/'EVIDENCE_MANIFEST.json');checks=[];failures=[];paragraphs={}
    def check(kind,location,ok,detail=None):
        row={'kind':kind,'location':location,'passed':bool(ok)}
        if detail is not None:row['detail']=detail
        checks.append(row)
        if not ok:failures.append(row)
    for row in manifest['files']:
        p=root/row['path'];check('return-file',row['path'],p.stat().st_size==row['bytes'] and hashlib.sha256(p.read_bytes()).hexdigest()==row['sha256'])
    expected={x['path']:x for x in read(A/'cosmology-planes-01'/'SOURCE_BINDINGS.json')}
    for row in read(root/'SOURCE_HASHES.json')['sources']:
        e=expected[row['path']];p=frozen/row['path']
        check('frozen-source',row['path'],p.stat().st_size==e['bytes']==row['actualBytes']==row['expectedBytes'] and hashlib.sha256(p.read_bytes()).hexdigest()==e['sha256']==row['expectedSha256']==row['actualSha256'])
    def walk(v,where):
        if isinstance(v,dict):
            if 'path' in v and any(k in v for k in ['paragraphIndexZeroBased','lineOneBased','jsonPointer']):
                p=frozen/v['path'];actual=None
                try:
                    if 'paragraphIndexZeroBased' in v:
                        key=(v['path'],v.get('part','word/document.xml'))
                        if key not in paragraphs:
                            with ZipFile(p) as z:doc=E.fromstring(z.read(key[1]))
                            ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
                            paragraphs[key]=[''.join(t.text or '' for t in q.findall('.//w:t',ns)) for q in doc.findall('.//w:p',ns)]
                        actual=paragraphs[key][v['paragraphIndexZeroBased']]
                        check('paragraph-excerpt',where,actual==v['excerpt'],None if actual==v['excerpt'] else {'citation':v,'actual':actual})
                    elif 'lineOneBased' in v:
                        actual=p.read_text(encoding='utf-8-sig').splitlines()[v['lineOneBased']-1]
                        check('line-excerpt',where,actual==v['excerpt'],None if actual==v['excerpt'] else {'citation':v,'actual':actual})
                    else:
                        actual=read(p)
                        for t in v['jsonPointer'].strip('/').split('/'):
                            t=t.replace('~1','/').replace('~0','~');actual=actual[int(t)] if isinstance(actual,list) else actual[t]
                        if 'value' in v:check('json-value',where,actual==v['value'])
                        elif v.get('evidenceKind','').startswith(('verbatim','exact')):check('json-excerpt',where,actual==v['excerpt'])
                        elif 'identifiedId' in v:check('identified-card',where,actual.get('id')==v['identifiedId'] and actual.get('name')==v['identifiedName'])
                        elif 'identifiedValues' in v:
                            for key,value in v['identifiedValues'].items():
                                selected=actual
                                for component in key.split('.'):selected=selected[component]
                                check('identified-proposal-field',where+'/'+key,selected==value)
                        else:check('summary-pointer-resolves',where,True,{'citation':v,'resolvedValue':actual,'semanticSummaryNeedsHumanModelReview':True})
                    if 'excerptSha256' in v:check('excerpt-hash',where,hashlib.sha256(v['excerpt'].encode()).hexdigest()==v['excerptSha256'])
                except Exception as ex:check('citation-resolves',where,False,{'citation':v,'error':repr(ex)})
            for k,w in v.items():walk(w,where+'/'+k)
        elif isinstance(v,list):
            for i,w in enumerate(v):walk(w,where+'/'+str(i))
    for filename in ['REGISTER.json','PLANE_AND_COURT_INDEX.json','TRAVEL_INTERFACE_MATRIX.json']:walk(read(root/filename),filename)
    register=read(root/'REGISTER.json');index=read(root/'PLANE_AND_COURT_INDEX.json');travel=read(root/'TRAVEL_INTERFACE_MATRIX.json')
    check('issue-ids','REGISTER.json',[x['id'] for x in register['issues']]==[f'PL-{i:02d}' for i in range(1,12)])
    check('claim-count','PLANE_AND_COURT_INDEX.json',index['claimRecordCount']==len(index['records'])==sum(index['counts'].values())==76)
    check('travel-counts','TRAVEL_INTERFACE_MATRIX.json',len(travel['reviewedEffects'])==6 and len(travel['pendingEffects'])==12)
    check('proposal-identities','TRAVEL_INTERFACE_MATRIX.json/unadoptedCompleteTransportProposals',all(x.get('name') and x.get('id') for x in travel['unadoptedCompleteTransportProposals']),travel['unadoptedCompleteTransportProposals'])
    check('travel-source-links','TRAVEL_INTERFACE_MATRIX.json',all(any(k in x for k in ['evidence','sourceCitations','citations','source','sourceCardCitation']) for x in travel['reviewedEffects']+travel['pendingEffects']), 'Travel summaries should bind actual whole cards rather than rely on a separate general source list.')
    direct=[]
    if corrected:
        base='DescentReviewChanges/ReviewBible/data/public/spell_playtests/'
        cards={name:read(frozen/(base+name))['spells'] for name in ['catalog.json','candidate_low_rank_136.json']}
        for group in ['reviewedEffects','pendingEffects']:
            for row in travel[group]:
                cite=row['sourceCardCitation'];record=read(frozen/cite['path'])
                for t in cite['jsonPointer'].strip('/').split('/'):record=record[int(t)] if isinstance(record,list) else record[t]
                filename='candidate_low_rank_136.json' if row['name'] in ['Arcane Portal','Blink Step'] else 'catalog.json'
                matches=[(i,x) for i,x in enumerate(cards[filename]) if x['id']==record['id']]
                check('card-copy-equals-actual-source',row['name'],len(matches)==1 and matches[0][1]==record)
                i,card=matches[0];direct.append({'name':row['name'],'id':card['id'],'path':base+filename,'jsonPointer':f'/spells/{i}','wholeCardMatchesReadingRecord':card==record})
                if group=='reviewedEffects':
                    op=card.get('operational') or card['operationalCandidate']
                    check('travel-effect-and-limits',row['name'],row['scope']==op['effect'] and row['limitations']==op['limitations'])
                    supplied=row['wholeTargetEndpointRequirements']
                    for key,sourcekey in [('rangeFeet','rangeFeet'),('range','range'),('targets','targets'),('duration','duration')]:check('target-endpoint-field',row['name']+'/'+key,supplied.get(key)==op.get(sourcekey))
                else:
                    supplied=row['wholeTargetEndpointRequirements'];src=card['source']['original']
                    check('pending-source-evidence',row['name'],supplied['operationalStatus']==card['status'] and supplied['operationalCard']==card['operational'] and supplied['sourceDescription']==src['description'] and supplied['sourcePlacements']==src['placements'])
    archive=A/('COSMOLOGY_PLANES_01_Corrected_Addendum_and_Evidence.zip' if corrected else 'COSMOLOGY_PLANES_01_Addendum_and_Evidence.zip')
    result={'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'archive':info(archive),'checks':checks,'failed':failures,'checkCount':len(checks),'failureCount':len(failures),'applicationAllowed':not failures,'directActualCardBindings':direct,'sourceInformationDeleted':0}
    dest=A/('COSMOLOGY_PLANES_01_LOCAL_CORRECTED_RETURN_CHECK_V2.json' if corrected else 'COSMOLOGY_PLANES_01_LOCAL_RETURN_CHECK.json');assert not dest.exists();dest.write_bytes(encoded(result))
    print(json.dumps({'checkCount':len(checks),'failureCount':len(failures),'failures':failures,'directActualCardBindings':len(direct)},ensure_ascii=False))

if __name__=='__main__':main()
