"""Read-only discovery of current catalog-dependent metadata before a pending patch."""
from datetime import datetime,timezone
import json
from apply_di7_ap_as_01 import G,R,A,info,encoded

def main():
    out=A/'DE4_REBINDING_TARGET_AUDIT_07.json';assert not out.exists()
    cat=R/'data/public/spell_playtests/catalog.json'; cb=info(cat); rel=cb['path'];hits=[]
    files=[R/'data/public/spell_playtests/authored_review_index.json']
    for folder in [R/'data/public/feat_candidates/exact_01',R/'data/director/feat_candidates/exact_01']:
        files+=sorted(folder.rglob('*.json'))
    for p in files:
        doc=json.loads(p.read_bytes()); found=[]
        def walk(x,path=''):
            if isinstance(x,dict):
                if (x.get('file')==rel or x.get('path')==rel) and any(k in x for k in ['sha256','bytes','pointer']):
                    found.append({'pointer':path,'keys':list(x),'binding':{k:x[k] for k in ['file','path','bytes','sha256','pointer'] if k in x},'historicalContainer':any(t in path.lower() for t in ['original','historical','previous','sourcefiles','frozen','evidencemanifest'])})
                for k,y in x.items():walk(y,path+'/'+k.replace('~','~0').replace('/','~1'))
            elif isinstance(x,list):
                for i,y in enumerate(x):walk(y,path+'/'+str(i))
            elif isinstance(x,str) and x==cb['sha256']:
                found.append({'pointer':path,'kind':'currentCatalogWholeHashLiteral','historicalContainer':any(t in path.lower() for t in ['original','historical','previous','sourcefiles','frozen'])})
        walk(doc)
        if found:hits.append({'source':info(p),'matches':found})
    out.write_bytes(encoded({'id':'DE4-REBINDING-TARGET-AUDIT-07','recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'Read-only metadata discovery; no binding is rewritten or deemed active solely by this heuristic','catalog':cb,'searchedFiles':len(files),'filesWithMatches':len(hits),'findings':hits,'mutations':0,'scope':'Current feat candidate directories plus authored index only; sealed historical packages are not rewrite targets.'}))
    print(json.dumps({'audit':info(out),'searchedFiles':len(files),'matchesByFile':[{'file':h['source']['path'],'matches':len(h['matches']),'candidateBindingPointers':[x['pointer'] for x in h['matches'] if 'binding'in x and not x['historicalContainer']][:8]} for h in hits]}))

if __name__=='__main__':main()
