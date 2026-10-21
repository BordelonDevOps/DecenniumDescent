"""Read-only FT84 source/reconstruction/mirror verifier; imports no project modules.
Use: python verify_bundle.py [--report /a/new/file.json]
All reconstruction occurs in memory. This tool has no apply mode.
"""
from pathlib import Path, PurePosixPath
from copy import deepcopy
import argparse, ast, hashlib, json, zipfile, stat
ROOT=Path(__file__).resolve().parent

def encode(x):return (json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode()
def sha(b):return hashlib.sha256(b).hexdigest()
def parse(b):return json.loads(b)
def read(n):return parse((ROOT/n).read_bytes())
def pointer(obj,p):
    for k in p.split('/')[1:]:
        k=k.replace('~1','/').replace('~0','~');obj=obj[int(k)] if isinstance(obj,list) else obj[k]
    return obj

def replace(obj,p,v):
    parts=p.split('/')[1:];parent=obj
    for k in parts[:-1]:
        k=k.replace('~1','/').replace('~0','~');parent=parent[int(k)] if isinstance(parent,list) else parent[k]
    k=parts[-1].replace('~1','/').replace('~0','~')
    if isinstance(parent,list):parent[int(k)]=deepcopy(v)
    else:parent[k]=deepcopy(v)

def run():
    checks=[]
    def brief(x):
        if isinstance(x,set):return sorted(x)
        if isinstance(x,bytes):return {'bytes':len(x),'sha256':sha(x)}
        if isinstance(x,(dict,list)) or isinstance(x,str) and len(x)>160:
            b=encode(x);return {'jsonBytes':len(b),'sha256':sha(b)}
        return x
    def eq(label,a,b=True):
        ok=a==b;checks.append({'check':label,'pass':ok,'actual':brief(a),'expected':brief(b)})
        if not ok:raise AssertionError(checks[-1])
    inputs=read('INPUT_BINDINGS.json');all_archives={};sources={};reports={};member_count=0;source_count=0
    for key,bind in inputs.items():
        path=ROOT/bind['file'];raw=path.read_bytes();eq(key+' input length',len(raw),bind['bytes']);eq(key+' input SHA256',sha(raw),bind['sha256'])
        with zipfile.ZipFile(path) as z:
            eq(key+' CRC',z.testzip(),None);names=z.namelist();eq(key+' unique members',len(names),len(set(names)));eq(key+' member count',len(names),bind['memberCount'])
            rawmembers={}
            for info in z.infolist():
                p=PurePosixPath(info.filename);safe=not p.is_absolute() and '..' not in p.parts and '\\' not in info.filename and ':' not in info.filename and not stat.S_ISLNK(info.external_attr>>16)
                eq(key+' safe '+info.filename,safe);rawmembers[info.filename]=z.read(info.filename)
            man=parse(rawmembers['MANIFEST.json']);eq(key+' manifest count',len(man),bind['manifestBoundCount'])
            for name,meta in man.items():
                b=rawmembers[name];eq(key+' length '+name,len(b),meta['bytes']);eq(key+' SHA256 '+name,sha(b),meta['sha256']);member_count+=1
                if name.startswith('sources/'):
                    source_count+=1;path=name[8:]
                    if path in sources:eq('overlapping full source '+path,b,sources[path])
                    else:sources[path]=b
                if name.endswith('.py'):ast.parse(b.decode('utf-8'));eq('supplied syntax parse only '+name,True)
            all_archives[bind['file']]=rawmembers;reports[key]=parse(rawmembers['REPORT.json'])
    sb=read('SOURCE_BINDINGS.json');eq('full source-member count',source_count,28);eq('distinct full source count',len(sources),21)
    for path,bind in sb['sources'].items():
        raw=all_archives[bind['archive']][bind['member']];eq('source address '+path,raw,sources[path]);eq('source stored hash '+path,sha(raw),bind['sha256'])
    bindings=read('ARTIFACT_BINDINGS.json')['files'];ops=read('JSON_POINTER_OPERATIONS.json')['operations'];eq('exact operation count',len(ops),51);eq('complete file bindings',len(bindings),7)
    before={};after={}
    for f in bindings:
        key=f['fileKey'];bb=all_archives[f['before']['archive']][f['before']['member']];aa=(ROOT/f['after']['file']).read_bytes()
        eq(key+' baseline length',len(bb),f['before']['bytes']);eq(key+' baseline hash',sha(bb),f['before']['sha256']);eq(key+' successor length',len(aa),f['after']['bytes']);eq(key+' successor hash',sha(aa),f['after']['sha256'])
        before[key]=bb;after[key]=aa;local=[o for o in ops if o['fileKey']==key]
        if f['repositoryPath'].endswith('.json'):
            a=parse(bb)
            for i,o in enumerate(local):
                eq(key+' full before '+o['pointer'],pointer(a,o['pointer']),o['before']);replace(a,o['pointer'],o['after'])
            eq(key+' full forward bytes',encode(a),aa)
            for o in reversed(local):
                eq(key+' full reverse precondition '+o['pointer'],pointer(a,o['pointer']),o['after']);replace(a,o['pointer'],o['before'])
            eq(key+' full reverse bytes',encode(a),bb)
            if local:eq(key+' repeat forward rejected',pointer(parse(aa),local[0]['pointer'])!=local[0]['before'])
    eq('full artifact alternatives',read('FULL_ARTIFACT_REPLACEMENTS.json')['replacements'],bindings)
    B={k:parse(v) for k,v in before.items() if k in ['director','public','assembly','shared']};A={k:parse(v) for k,v in after.items() if k in B}
    proc=read('SELECTED_PROCEDURES.json')['procedures'];changed={p['id'] for p in proc}
    eq('selected six IDs',changed,{'spell_scribe','ritual_caster','diligent_researcher','craftsman','contraption_crafter','trapsetter'})
    # Source data and historical authorship remain independent of selected operative fields.
    for key,items in [('director','records'),('public','feats'),('assembly','entries')]:
        bb=B[key];aa=A[key];eq(key+' order IDs',[x['id'] for x in bb[items]],[x['id'] for x in aa[items]])
        for name in bb:
            if name!=items:eq(key+' root preserved '+name,aa[name],bb[name])
        for old,new in zip(bb[items],aa[items]):
            fid=old['id']
            if fid not in changed:eq(key+' unchanged record '+fid,new,old)
            elif key in ['director','public']:
                for name in old:
                    if name not in ['operationalRules','payloadOperational']:eq(key+' original/historical field '+fid+'/'+name,new[name],old[name])
            else:
                stripped=deepcopy(new)
                local=[o for o in ops if o['fileKey']=='assembly' and o['pointer'].startswith('/entries/'+str(bb[items].index(old))+'/')]
                for o in local:
                    rel='/'+o['pointer'].split('/',3)[3];replace(stripped,rel,o['before'])
                eq('assembly full original excluding selected mirror ops '+fid,stripped,old)
    for i,(old,new) in enumerate(zip(B['shared']['rules'],A['shared']['rules'])):
        if i!=13:eq('unchanged shared rule '+str(i),new,old)
        else:
            eq('FS14 original complete text retained',new['wording'].startswith(old['wording']));other=deepcopy(new);other['wording']=old['wording'];eq('FS14 other fields retained',other,old)
    pd={p['id']:p for p in proc}
    for p in proc:
        fid=p['id'];old=next(x for x in B['director']['records'] if x['id']==fid);eq('full original selected record '+fid,p['completeOriginalRecord'],old);eq('original operative string '+fid,p['before'],old['operationalRules']);eq('old wording prefix retained '+fid,p['after'].startswith(p['before']))
        for key,col in [('director','records'),('public','feats')]:
            row=next(x for x in A[key][col] if x['id']==fid)
            for field in ['operationalRules','payloadOperational']:eq(key+' current mirror '+fid+'/'+field,row[field],p['after'])
        a=next(x for x in A['assembly']['entries'] if x['id']==fid)
        for ptr in ['/currentPublic/operationalRules','/currentPublic/payloadOperational','/currentCompleteContract/completeOperativeProcedure','/reviewedAcquisitionDescriptor/completeControllingOperativeProcedure']:eq('assembly current mirror '+fid+ptr,pointer(a,ptr),p['after'])
        eq('no false exact approval claimed '+fid,p['exactApproved'],False);eq('no runtime claimed '+fid,p['runtimeApproved'],False)
    # Complete chapter replacement and appending preserve all other bytes.
    s=before['craftChapter'].decode()
    for fid in ['craftsman','diligent_researcher','trapsetter']:
        eq('chapter exact single original '+fid,s.count(pd[fid]['before']),1);s=s.replace(pd[fid]['before'],pd[fid]['after'],1)
    eq('complete CRAFTING chapter rendition',s.encode(),after['craftChapter'])
    for key in ['languageGuide','craftGuide']:
        eq(key+' full previous bytes retained',after[key].startswith(before[key]));eq(key+' exact proposed Q02 present',read('QUESTION_DISPOSITIONS.json')['questions'][1]['selectedWording'] in after[key].decode().replace('\r\n','\n'))
    qs=read('QUESTION_DISPOSITIONS.json')['questions'];eq('exact three question IDs',[x['id'] for x in qs],['FT84-Q01','FT84-Q02','FT84-Q03'])
    for original,q in zip(reports['84']['openDispositions'],qs):
        eq('complete original question '+q['id'],q['completeOriginalQuestion'],original)
        for ref in q['sources']:
            eq('question source hash '+q['id']+' '+ref['path'],sha(sources[ref['path']]),ref['binding']['sha256'])
            if 'pointer' in ref:pointer(parse(sources[ref['path']]),ref['pointer']);eq('question source pointer '+q['id']+ref['pointer'],True)
    model=read('MODEL.json');eq('MODEL complete selected questions',model['questions'],qs);eq('MODEL bindings',model['fileBindings'],bindings)
    for p,q in zip(proc,model['fullSelectedProcedures']):eq('MODEL procedure '+p['id'],q['procedure'],p['after'])
    eq('no canonical application',model['canonicalApplied'],False);eq('no335 acceptance',model['parent335Accepted'],False)
    orig=read('ORIGINAL_CASE_DISPOSITIONS.json')['cases'];eq('historical case total',len(orig),106)
    for i,c in enumerate(orig):
        k='84' if c['archive'].endswith('_84.zip') else '83';n=int(c['pointer'].split('/')[-1]);eq('complete historical case '+c['id'],c['completeOriginalCase'],reports[k]['cases'][n]);eq('historical script not executed '+c['id'],c['historicalScriptExecutedHere'],False)
    casebook=read('CASEBOOK.json');spec=read('SPECIFICATION_REPORT.json');eq('new case count',casebook['caseCount'],57);eq('new unique IDs',len(set(c['id'] for c in spec['cases'])),57);eq('new assertions counted',len(spec['assertions']),spec['assertionCount']);eq('reported specification failures',spec['failures'],0)
    for c in spec['assertions']:eq('stored actual/expected '+c['assertion'],c['actual'],c['expected']);eq('stored pass flag '+c['assertion'],c['pass'],True)
    for c,s in zip(casebook['cases'],spec['cases']):eq('complete current case mirror '+c['id'],c['completeSpecificationCase'],s);eq('no runtime case claim '+c['id'],c['realRuntimeExecuted'],False)
    eq('new casebook assertion total',casebook['assertionCount'],spec['assertionCount'])
    for name in ['spec_work.py','verify_bundle.py']:ast.parse((ROOT/name).read_text());eq('returned syntax '+name,True)
    manifest=ROOT/'MANIFEST.json'
    if manifest.exists():
        man=read('MANIFEST.json');expected={f['path'] for f in man['files']};actual={str(p.relative_to(ROOT)).replace('\\','/') for p in ROOT.rglob('*') if p.is_file() and p.name!='MANIFEST.json' and '__pycache__' not in p.parts}
        eq('manifest complete file set',sorted(actual),sorted(expected))
        for f in man['files']:
            b=(ROOT/f['path']).read_bytes();eq('return file length '+f['path'],len(b),f['bytes']);eq('return file hash '+f['path'],sha(b),f['sha256'])
    return {'id':'FT84-READ-ONLY-VERIFICATION-01','checkCount':len(checks),'failures':sum(not c['pass'] for c in checks),'inputManifestMembers':member_count,'sourceMemberCount':source_count,'distinctSourcePaths':len(sources),'jsonOperationCount':len(ops),'successorFileCount':len(bindings),'historicalCasesPreserved':len(orig),'checks':checks,'scope':'Read-only byte/value/pointer/mirror and stored-report checks. No project or downloaded input script executed/imported, no reference specification rerun by this verifier, no runtime/gameplay/balance proof.'}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--report',type=Path);a=p.parse_args();r=run()
    if a.report:
        payload=encode(r)
        with a.report.open('xb') as f:f.write(payload)
    print(json.dumps({k:v for k,v in r.items() if k!='checks'},ensure_ascii=False))
