"""Independent data-only reconstruction of the delivered scoped operations."""
from pathlib import Path
from collections import defaultdict
import copy, hashlib, json, zipfile

A=Path(r'C:\Github\DecenniumDescent\docs\audit\2026-10-08\full-game')
P=A/'bestiary-reconciliation-108'/'delivery'
OUT=A/'bestiary-reconciliation-108'/'derived'
OUT.mkdir(exist_ok=False)
checks=[]; bindings={}; operations=[]
def h(b):return hashlib.sha256(b).hexdigest()
def serial(x):return (json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode()
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def load(n):return json.loads((P/n).read_bytes())
def check(n,v):
    checks.append({'name':n,'passed':bool(v)})
    if not v:raise AssertionError(n)
def write(p,b):
    with p.open('xb') as f:f.write(b)
def parent(x,p):
    parts=[s.replace('~1','/').replace('~0','~') for s in p.split('/')[1:]]
    for s in parts[:-1]:x=x[int(s)] if isinstance(x,list) else x[s]
    return x,int(parts[-1]) if isinstance(x,list) else parts[-1]
def value(x,p):
    x,k=parent(x,p);return x[k]
def binding(b):return {'bytes':len(b),'sha256':h(b)}

plan=load('JSON_REFERENCE_OPERATIONS.json'); textplan=load('TEXT_REFERENCE_OPERATIONS.json')
grouped=defaultdict(list)
for o in plan['operations']:grouped[o['member']].append(o)
docs={}
with zipfile.ZipFile(A/'bestiary-deliveries-104'/'DD_Bestiary_Return02.zip') as z:
    for name,ops in grouped.items():
        raw=z.read(name); original=json.loads(raw); current=copy.deepcopy(original); inverse=[]
        check(name+' original serialization',serial(original)==raw)
        for i,o in enumerate(ops):
            pp,key=parent(current,o['path']); before=o['before']
            if o['op']=='replace':
                check(name+o['path']+' exact before',binding(raw)=={'bytes':before['bytes'],'sha256':before['sha256']} and h(canon(value(original,before['pointer'])))==before['canonicalValueSha256'] and pp[key]==value(original,before['pointer']))
                inverse.append((o['path'],copy.deepcopy(pp[key]),False))
            else:
                check(name+o['path']+' absent before add',o['op']=='add' and before=={'present':False} and key not in pp)
                inverse.append((o['path'],None,True))
            after=value(load(o['after']['file']),o['after']['pointer'])
            check(name+o['path']+' bound after',h(canon(after))==o['after']['canonicalValueSha256'])
            pp[key]=copy.deepcopy(after)
            operations.append({'member':name,'path':o['path'],'op':o['op'],'afterHash':h(canon(after))})
        out=serial(current)
        check(name+' full successor matches',binding(out)==plan['virtualSuccessorBindings'][name])
        reverse=copy.deepcopy(current)
        for path,before,added in reversed(inverse):
            pp,key=parent(reverse,path)
            if added:del pp[key]
            else:pp[key]=before
        check(name+' reverse exact original bytes',serial(reverse)==raw)
        write(OUT/name,out);bindings[name]={'before':binding(raw),'derivedAfter':binding(out)};docs[name]=current
    grouped=defaultdict(list)
    for o in textplan['operations']:grouped[o['member']].append(o)
    for name,ops in grouped.items():
        raw=z.read(name);ordered=sorted(ops,key=lambda o:o['before']['offset'])
        check(name+' exact base',binding(raw)==textplan['fullByteBindings'][name]['before'])
        chunks=[];inverse=[];end=0;newpos=0
        for o in ordered:
            b=o['before'];start=b['offset'];stop=start+b['length'];after=(P/o['after']['file']).read_bytes()
            check(name+o['tag']+' exact original span',start>=end and h(raw[start:stop])==b['sha256'] and binding(raw)==b['memberBinding'])
            check(name+o['tag']+' exact after span',binding(after)=={'bytes':o['after']['bytes'],'sha256':o['after']['sha256']})
            chunks.append(raw[end:start]);newpos+=start-end
            inverse.append((newpos,len(after),raw[start:stop]));chunks.append(after);newpos+=len(after);end=stop
        chunks.append(raw[end:]);out=b''.join(chunks)
        check(name+' full successor matches',binding(out)==textplan['fullByteBindings'][name]['virtualAfter'])
        reverse=out
        for start,length,b in reversed(inverse):reverse=reverse[:start]+b+reverse[start+length:]
        check(name+' reverse exact original bytes',reverse==raw)
        write(OUT/name,out);bindings[name]={'before':binding(raw),'derivedAfter':binding(out)}

selected=load('SELECTED_PROCEDURES.json')
for key,idx,section,actionidx in [('pressure',36,'actions',2),('tail',15,'tacticCompletions',0),('constrict',22,'tacticCompletions',0)]:
    obj=selected['completeSelectedReturn02Objects'][key]
    check(key+' complete mirrors agree',docs['MODEL.json']['records'][idx]['proposedOperation02'][section][actionidx]==obj==docs['PROCEDURES.json']['profiles'][idx][section][actionidx])
source=load('BOUND_SOURCES.json');refs={r['id']:r for r in selected['sourceRefs']}
sourcezip=A/source['inputBindings']['sourceArchive']['file']
check('Source archive binding',binding(sourcezip.read_bytes())=={k:source['inputBindings']['sourceArchive'][k] for k in ['bytes','sha256']})
with zipfile.ZipFile(sourcezip) as z:
    sourcebytes={}
    for rid,r in refs.items():
        b=z.read(r['member']);sourcebytes[rid]=b
        check('Full source bound '+rid,binding(b)=={k:r[k] for k in ['bytes','sha256']})
    for rid,r in source['fullOriginalDossiers'].items():check('Full dossier text exact '+rid,r['originalUtf8Text'].encode()==sourcebytes[rid])
    for i,s in enumerate(source['governingFullSections']):
        if 'exactText' in s:
            check('Full governing section '+str(i),h(s['exactText'].encode())==s['sectionUtf8Sha256'] and s['exactText'].replace('\r\n','\n') in sourcebytes[s['sourceId']].decode().replace('\r\n','\n'))
        else:check('Full registry entry '+str(i),value(json.loads(sourcebytes[s['sourceId']]),s['pointer'])==s['completeEntry'])
    originalmodel=json.loads(sourcebytes['SRC-MODEL'])
    for rid,r in source['nativeActors'].items():check('Complete native actor '+rid,value(originalmodel,r['recordPointer'])==r['record'])

report={'id':'BESTIARY-FINAL-RECONCILIATION-RECONSTRUCTION-108','status':'EXACT_DERIVED_RECONSTRUCTION_NOT_CANONICAL_INTEGRATION','passed':len(checks),'failed':0,'checks':checks,'jsonOperationCount':len(operations),'textOperationCount':len(textplan['operations']),'fileBindings':bindings,'operations':operations,'sourceFilesOpened':list(refs),'semanticReviewPending':True,'canonicalApplied':False,'limits':['Independent parsing/reconstruction, complete-source binding and inverse preservation only.','New derived evidence files are not a whole-catalog accepted candidate.','Historical originals, manifests, reports and existing successful programs unchanged.','No supplied script run/imported. No sealed dossier opened. No runtime/gameplay/balance/cosmology approval.']}
write(A/'BESTIARY_FINAL_RECONCILIATION_RECONSTRUCTION_108.json',serial(report))
write(A/Path(__file__).name,Path(__file__).read_bytes())
print(json.dumps({'passed':len(checks),'failed':0,'jsonOperations':len(operations),'textOperations':len(textplan['operations']),'derivedFiles':len(bindings)}))
