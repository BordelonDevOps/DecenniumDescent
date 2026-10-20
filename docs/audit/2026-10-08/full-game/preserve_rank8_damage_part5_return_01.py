"""Independent inbound preservation and exact replay; never import returned code."""
from pathlib import Path, PurePosixPath
from datetime import datetime, timezone
import ast, copy, hashlib, io, json, stat, zipfile

G = Path(r'C:\Github\DecenniumDescent')
A = G / 'docs/audit/2026-10-08/full-game'
IN = Path(r'C:\Users\cbord\Downloads\DD_Rank8_Damage_6_Part5_Conference_Return_01.zip')
OUT = A / IN.name
ROOT = A / 'rank8-damage6-part5-conference-return-01'
REPORT = A / 'RANK8_DAMAGE6_PART5_RETURN_01_LOCAL_PREFLIGHT.json'
checks = []
def ck(label, value):
    checks.append({'check':label, 'passed':bool(value)})
    assert value, label
def sha(b): return hashlib.sha256(b).hexdigest()
def enc(x): return (json.dumps(x, ensure_ascii=False, indent=2)+'\n').encode()
def info(p):
    b=p.read_bytes()
    return {'path':p.relative_to(G).as_posix(), 'bytes':len(b), 'sha256':sha(b)}
def binding(raw, b, label):
    ck(label, len(raw)==b['bytes'] and sha(raw)==b['sha256'])
def safe(z, label):
    names=z.namelist()
    ck(label+' exact and case-insensitive unique names',len(names)==len(set(names))==len(set(n.casefold() for n in names)))
    for i in z.infolist():
        p=PurePosixPath(i.filename)
        ck(label+' safe member '+i.filename,not p.is_absolute() and '..' not in p.parts and '\\' not in i.filename and ':' not in i.filename and not stat.S_ISLNK(i.external_attr >> 16) and not i.is_dir())
    ck(label+' bounded expanded size',sum(i.file_size for i in z.infolist())<100_000_000)
    ck(label+' CRC',z.testzip() is None)
def parent(doc, pointer):
    parts=[x.replace('~1','/').replace('~0','~') for x in pointer.split('/')[1:]]
    cur=doc
    for k in parts[:-1]: cur=cur[int(k)] if isinstance(cur,list) else cur[k]
    return cur, parts[-1]

def main():
    ck('Fresh output locations',not any(p.exists() for p in (OUT,ROOT,REPORT)))
    cp=json.loads((A/'ACTIVE_AUTHORING_CHECKPOINT_RANK9_MEMORY_DENIAL_57.json').read_bytes())
    protected=[G/cp[k]['path'] for k in ['currentWorkQueue','currentAuthoredIndex','currentAcceptedInterfaceRegistry','decisionLedger']]
    protected += [G/b['path'] for b in cp['canonicalHelperBaselinesUnchanged']]
    protected += [G/'DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json',G/'DescentReviewChanges/ReviewBible/data/director/spell_review/rank8_damage_6_source_conference_01.json']
    before={p:p.read_bytes() for p in protected}
    raw=IN.read_bytes()
    binding(raw,{'bytes':4912092,'sha256':'119bfa063012d4c8c870ad6385c680a7c00c153d778c83bad08ae9895ff935d0'},'Expected downloaded archive')
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        safe(z,'Returned archive')
        payload={n:z.read(n) for n in z.namelist()}
    j=lambda n:json.loads(payload[n])
    man=j('MANIFEST.json')
    ck('40 members and 39 bound files',len(payload)==40 and len(man['files'])==man['fileCount']==39)
    ck('Manifest exact membership',set(payload)=={'MANIFEST.json'}|{b['path'] for b in man['files']})
    for b in man['files']:binding(payload[b['path']],b,'Return manifest '+b['path'])
    ib=j('INPUT_BINDINGS.json'); original=payload[ib['archive']]
    binding(original,ib,'Original input binding')
    ck('Original input exact local archive',original==(A/Path(ib['archive']).name).read_bytes())
    with zipfile.ZipFile(io.BytesIO(original)) as iz:
        safe(iz,'Original source archive')
        ck('Original candidate exact local and baseline',iz.read('CANDIDATE.json')==payload['baseline/CANDIDATE.json']==before[protected[-1]])
        sources=j('SOURCE_BINDINGS.json')['originalFullSources']
        ck('51 complete source bindings retained',sources==ib['sourceBindingsUnchanged'] and len(sources)==51)
        for b in sources:
            src=iz.read('sources/'+b['path'])
            binding(src,b,'Original bound source '+b['path'])
            ck('Original local source unchanged '+b['path'],(G/b['path']).read_bytes()==src)
    archives={}
    context=j('CONTEXT_BINDINGS.json')['files']
    ck('11 complete context files',len(context)==11)
    for b in context:
        content=payload[b['file']];binding(content,b,'Context '+b['file'])
        ck('Context has actual archive anchor '+b['file'],bool(b['exactArchiveAnchors']))
        for a in b['exactArchiveAnchors']:
            if a['archive'] not in archives:
                archives[a['archive']]=(A/a['archive']).read_bytes()
            ar=archives[a['archive']]
            binding(ar,{'bytes':a['archiveBytes'],'sha256':a['archiveSha256']},'Prior archive '+a['archive'])
            with zipfile.ZipFile(io.BytesIO(ar)) as az:member=az.read(a['member'])
            binding(member,a,'Prior context member '+a['member'])
            ck('Exact context anchor '+b['file']+' '+a['member'],member==content)
    ops=j('EXACT_OPERATIONS_FROM_SOURCE.json');base=payload[ops['base']['file']];target=payload[ops['successor']['file']]
    binding(base,ops['base'],'Replay base');binding(target,ops['successor'],'Replay successor')
    ck('37 full-value operations',len(ops['operations'])==ops['operationCount']==37)
    current=json.loads(base)
    for i,o in enumerate(ops['operations']):
        p,k=parent(current,o['pointer'])
        ck('Supported exact operation '+str(i),isinstance(p,dict) and o['op'] in ('replace','add'))
        ck('Before presence '+str(i),(k in p)==o['beforeExists'])
        ck('Before value '+str(i),p.get(k)==o['before'])
        p[k]=copy.deepcopy(o['after'])
    ck('Forward exact bytes',enc(current)==target)
    for i,o in enumerate(reversed(ops['operations'])):
        p,k=parent(current,o['pointer'])
        ck('Reverse after-value '+str(i),k in p and p[k]==o['after'])
        if o['beforeExists']:p[k]=copy.deepcopy(o['before'])
        else:del p[k]
    ck('Reverse exact bytes',enc(current)==base)
    old=json.loads(base);model=json.loads(target)
    for i,(a,b) in enumerate(zip(old['records'],model['records'])):
        ck('Source record preserved '+str(i),all(b[k]==v for k,v in a.items() if k!='status'))
        required={s['id'] for s in model['selectedSharedRules']}
        if b['spellId'] not in {'deep-crust-spike','soul-pyre'}:required.remove('RD8-MIXED-02')
        ck('Procedure present and applicable rule routing '+str(i),len(b['procedure'])>1000 and set(b['selectedSharedRuleIds'])==required)
    for k in old:
        if k not in {'id','recordedAtUtc','status','records','currentVectors'}:ck('Original top-level field preserved '+k,old[k]==model[k])
    cases=j('CASE_DISPOSITIONS.json')
    ck('12 main cases 41 branches',len(cases['allCases'])==cases['mainCaseCount']==12 and sum(len(c['independentBranches']) for c in cases['allCases'])==cases['independentBranchCount']==41)
    ck('Runtime flags remain false',not model['runtimeImplemented'] and not model['runtimeSelectionEnabled'] and not model['runtimeTestsExecuted'] and not model['newAppliedProjectRuleAdoptions'])
    ck('Original risk counts retained',model['riskCounts']==old['riskCounts']=={'B':4,'C':2})
    for n,b in payload.items():
        if n.endswith('.py'):ast.parse(b.decode('utf-8'));ck('Python parsed only, not executed '+n,True)
    ROOT.mkdir()
    OUT.write_bytes(raw)
    for n,b in payload.items():
        dest=ROOT/n;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(b)
        ck('Extracted bytes exact '+n,dest.read_bytes()==b)
    ck('Preserved archive exact',OUT.read_bytes()==raw)
    for p,b in before.items():ck('Protected authority unchanged '+p.relative_to(G).as_posix(),p.read_bytes()==b)
    report={'id':'RANK8-DAMAGE6-PART5-RETURN-01-LOCAL-PREFLIGHT','recordedAtUtc':datetime.now(timezone.utc).isoformat(),'archive':info(OUT),'model':info(ROOT/'MODEL.json'),'nativeFinal':info(A/'GPT_PART5_RANK8_DAMAGE_RETURN_01_NATIVE.json'),'checks':checks,'checkCount':len(checks),'failures':0,'sourceFiles':51,'contextFiles':11,'forwardAndReverseOperations':37,'caseInventory':{'main':12,'branches':41},'scope':'Independent source/hash/manifest/exact forward-reverse replay and preservation only. Semantic review is pending; no new acceptance or implementation. Returned Python AST parsed, never imported/executed. GPT-reported tests are not local engine tests.','acceptedButUnappliedUnchanged':39,'appliedCountsUnchanged':{'reviewed':525,'pending':323,'standalone':249,'interfaces':173},'runtimeTestsExecuted':0,'humanPlaytests':0,'sourceInformationDeleted':0,'implementationApplied':False}
    REPORT.write_bytes(enc(report))
    print(json.dumps({'report':info(REPORT),'checks':len(checks),'failures':0,'archive':info(OUT)}))

if __name__=='__main__':main()
