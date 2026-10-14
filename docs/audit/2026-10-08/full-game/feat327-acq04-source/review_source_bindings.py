"""Read-only ACQ-04 source/binding audit. No feat runtime or campaign authentication.
Usage: python review_source_bindings.py ARCHIVE.zip OUTPUT_DIRECTORY
Only OUTPUT_DIRECTORY is written. The archive and its payloads are not modified.
"""
import hashlib,json,re,sys,zipfile
from pathlib import Path, PurePosixPath

def sha(b): return hashlib.sha256(b).hexdigest()
def ptr(obj,p):
    for part in p.lstrip('/').split('/') if p else []:
        part=part.replace('~1','/').replace('~0','~')
        obj=obj[int(part)] if isinstance(obj,list) else obj[part]
    return obj

def leaves(obj,p=''):
    if isinstance(obj,dict):
        for k,v in obj.items(): yield from leaves(v,p+'/'+k.replace('~','~0').replace('/','~1'))
    elif isinstance(obj,list):
        for i,v in enumerate(obj): yield from leaves(v,p+'/'+str(i))
    elif isinstance(obj,str): yield p,obj

def main(archive,output):
    archive=Path(archive); output=Path(output); output.mkdir(parents=True,exist_ok=True)
    checks=[]
    def ck(name,result,**evidence):
        checks.append({'name':name,'passed':bool(result),**evidence})
        if not result: raise ValueError('Failed source check: '+name)
    with zipfile.ZipFile(archive) as z:
        names=[i.filename for i in z.infolist() if not i.is_dir()]
        manifest_bytes=z.read('PACKAGE_MANIFEST.json'); manifest=json.loads(manifest_bytes)
        ck('unique archive member paths',len(names)==len(set(names)))
        ck('safe relative paths',all(not PurePosixPath(n).is_absolute() and '..' not in PurePosixPath(n).parts for n in names))
        ck('exact manifest membership',set(names)==set(manifest)|{'PACKAGE_MANIFEST.json'})
        payload={n:z.read(n) for n in manifest}
        for n,b in payload.items():
            ck('size:'+n,len(b)==manifest[n]['bytes'])
            ck('sha256:'+n,sha(b)==manifest[n]['sha256'])
        def read(n): return json.loads(payload[n])
        audit='docs/audit/2026-10-08/full-game/'
        public='DescentReviewChanges/ReviewBible/data/public/'
        ep=audit+'FEAT327_ACQ_04_SOURCE_EVIDENCE.json'; e=read(ep)
        for b in e['sourceBindings']:
            p=b['path']; ck('evidence binding:'+p,p in manifest and b['bytes']==manifest[p]['bytes'] and b['sha256']==manifest[p]['sha256'])
        cp=audit+'FEAT_EXACT_01_ACQUISITION_CONTRACTS.json'; c=read(cp)
        ck('335 unique contract IDs',len(c['records'])==335 and len({x['id'] for x in c['records']})==335)
        excerpts=[]
        def excerpt(p,pointer):
            ex={'path':p,'sha256':manifest[p]['sha256'],'pointer':pointer,'value':ptr(read(p),pointer)}
            excerpts.append(ex);return ex
        for x in e['completeCredentialContracts']+[e['completeBerserkerParent']]:
            pairs=[(i,y) for i,y in enumerate(c['records']) if y['id']==x['id']]
            ck('complete contract equality:'+x['id'],len(pairs)==1 and pairs[0][1]==x)
            excerpt(cp,'/records/'+str(pairs[0][0]))
        excerpt(cp,'/records/33')
        for x in e['completeRelevantClassCards']:
            p=x['file']['path'];ck('complete class evidence:'+x['completeCard']['id'],ptr(read(p),x['pointer'])==x['completeCard'])
        class_paths=sorted(n for n in manifest if '/class_playtests/' in n and n.endswith('.json'))+[public+'Decennium_Descent_Bard_Playtest_v0_1.json']
        ck('17 full class payloads',len(class_paths)==17)
        pat=re.compile(r'\b(?:rage|raging|rages|berserk\w*|frenz\w*)\b',re.I)
        hits=[];card_counts={};matched_cards=set()
        for p in class_paths:
            j=read(p);card_counts[p]=len(j['cards'])
            for q,s in leaves(j):
                if pat.search(s):
                    hits.append({'path':p,'pointer':q,'text':s})
                    m=re.match(r'(/cards/\d+)(?:/|$)',q)
                    if m:matched_cards.add((p,m.group(1)))
        ck('1223 complete class cards parsed',sum(card_counts.values())==1223)
        for p,q in sorted(matched_cards):excerpt(p,q)
        fp='DescentReviewChanges/ReviewBible/data/playtest/character_foundation.json'
        ap='DescentReviewChanges/ReviewBible/data/playtest/ancestry_background_candidate.json'
        foundation=read(fp);ancestry=read(ap)
        class_names=[x['class'] for x in foundation['classes']]
        actual_lineages=[{'id':x['id'],'name':x['name'],'variants':[{'id':v['id'],'name':v['name']} for v in x['variants']]} for x in ancestry['ancestries']]
        ck('evidence class names equal full foundation',class_names==e['actualClassNames'])
        ck('evidence lineage names/variants equal full catalog',actual_lineages==e['actualLineages'])
        ck('14 base lineages and45 variants',len(actual_lineages)==14 and sum(len(x['variants']) for x in actual_lineages)==45)
        ck('no current Sorcerer class option','Sorcerer' not in class_names)
        ck('no current Dragonborn base/variant option',not any(y['name'].casefold()=='dragonborn' for x in actual_lineages for y in [x]+x['variants']))
        excerpt(fp,'/classes/15');excerpt(ap,'/ancestries/2')
        sp=public+'feat_candidates/exact_01/shared_rules.json'
        for i in [0,1,8,15]:excerpt(sp,'/rules/'+str(i))
        sup=public+'feat_candidates/exact_01/supplements.json';excerpt(sup,'/groups/3/value/Sorcerer')
        ck('four operative procedures and raw prerequisite nodes are present',all(x.get('completeOperativeProcedure') and 'requirements' in x and 'originalObject' in x for x in e['completeCredentialContracts']))
        ck('all four candidate selection flags remain false',all(x['candidateSelectionEnabled'] is False for x in e['completeCredentialContracts']))
        ck('whole contract selection/full-validation/readiness remain false',c['selectionEnabled'] is False and c['allAcquisitionBoundariesValidated'] is False and c['candidateReadyForSubmission'] is False)
        report={'reviewId':'FEAT327-ACQ-04','archive':archive.name,'archiveBytes':archive.stat().st_size,'archiveSha256':sha(archive.read_bytes()),'rootManifest':'PACKAGE_MANIFEST.json','rootManifestSha256':sha(manifest_bytes),'payloadCount':len(manifest),'checksExecuted':len(checks),'failedChecks':[x for x in checks if not x['passed']],'checks':checks,'classCardCounts':card_counts,'classRelevantSearchExpression':pat.pattern,'classRelevantHits':hits,'inspectionScope':'Complete source bytes and JSON trees parsed; four exact contracts, parent Berserker/CF-03, all seven full rage/frenzy/Berserker-matching cards, relevant class engines, shared rules, current option identities and quoted supplement inspected. No general semantic re-review of1223 class procedures.','semanticFinding':'No examined operative class grant expressly establishes the class-rage credential; search hits are preserved history, names, conduct or distinct buffs. This is a reviewer disposition, not an automated semantic proof.','behavioralTestsExecuted':0,'campaignRecordsAuthenticated':0,'priorAcq03SuitesRerun':False,'exactFeatApprovals':0,'sourceBytesModified':0}
        (output/'SOURCE_BINDING_AUDIT.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
        (output/'BOUND_SOURCE_EXCERPTS.json').write_text(json.dumps({'archiveSha256':report['archiveSha256'],'references':excerpts},indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
        (output/'SUBMITTED_PACKAGE_MANIFEST.json').write_bytes(manifest_bytes)
        print(json.dumps({k:report[k] for k in ['payloadCount','checksExecuted','failedChecks','archiveSha256','rootManifestSha256']},indent=2))
if __name__=='__main__':
    if len(sys.argv)!=3:raise SystemExit(__doc__)
    main(sys.argv[1],sys.argv[2])
