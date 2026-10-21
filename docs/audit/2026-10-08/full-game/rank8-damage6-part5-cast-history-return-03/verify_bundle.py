#!/usr/bin/env python3
"""Read-only verification of conference13; no supplied project scripts executed.

All model/whole-file reconstruction is in memory. --report writes one new file
with exclusive creation, never modifies an input, and refuses package-local output.
"""
from __future__ import annotations
import argparse, ast, copy, hashlib, io, json, stat, zipfile
from collections import Counter
from pathlib import Path, PurePosixPath

ROOT=Path(__file__).resolve().parent
checks=[]

def check(label,condition,category='structure'):
    checks.append({'check':label,'category':category,'passed':bool(condition)})
    if not condition:raise AssertionError(label)

def sha(b):return hashlib.sha256(b).hexdigest()
def jb(x):return (json.dumps(x,indent=2,ensure_ascii=False)+'\n').encode('utf8')
def load(n):return json.loads((ROOT/n).read_bytes())
def bind(label,b,e,category='hash'):
    check(label+':bytes',len(b)==e['bytes'],category)
    check(label+':sha256',sha(b)==e['sha256'],category)

def safe_zip(b,label):
    z=zipfile.ZipFile(io.BytesIO(b));names=z.namelist()
    check(label+':unique',len(names)==len(set(names)),'archive')
    check(label+':safe',all(not PurePosixPath(i.filename).is_absolute() and
          '..' not in PurePosixPath(i.filename).parts and '\\' not in i.filename and
          ':' not in i.filename.split('/')[0] and not stat.S_ISLNK(i.external_attr>>16)
          for i in z.infolist()),'archive')
    check(label+':crc',z.testzip() is None,'archive')
    return z

def parts(p):return [t.replace('~1','/').replace('~0','~') for t in p.split('/')[1:]]
def at(d,p):
    for k in parts(p):d=d[int(k)] if isinstance(d,list) else d[k]
    return d

def replay(data,ops,reverse=False,record=True,label='plan'):
    d=copy.deepcopy(data)
    for idx,o in enumerate(reversed(ops) if reverse else ops):
        p=parts(o['pointer']);parent=d
        for k in p[:-1]:parent=parent[int(k)] if isinstance(parent,list) else parent[k]
        key=int(p[-1]) if isinstance(parent,list) else p[-1]
        exists=(0<=key<len(parent)) if isinstance(parent,list) else key in parent
        if reverse:
            if not exists or parent[key]!=o['after']:raise ValueError('Wrong reverse full value: '+o['pointer'])
            if o['beforeExists']:parent[key]=copy.deepcopy(o['before'])
            else:del parent[key]
        else:
            if exists!=o['beforeExists']:raise ValueError('Wrong existence: '+o['pointer'])
            if exists and parent[key]!=o['before']:raise ValueError('Wrong forward full value: '+o['pointer'])
            parent[key]=copy.deepcopy(o['after'])
        if record:check(f'{label}:{"reverse" if reverse else "forward"}:{idx}:{o["pointer"]}',True,'full-value')
    return d

def delta_paths(a,b,p=''):
    if type(a)!=type(b):return [p]
    if isinstance(a,dict):
        out=[]
        for k in set(a)|set(b):
            path=p+'/'+k.replace('~','~0').replace('/','~1')
            out+=([path] if k not in a or k not in b else delta_paths(a[k],b[k],path))
        return out
    if isinstance(a,list):
        if len(a)!=len(b):return [p]
        return [x for i,(u,v) in enumerate(zip(a,b)) for x in delta_paths(u,v,p+'/'+str(i))]
    return [] if a==b else [p]

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--manifest',action='store_true');ap.add_argument('--report',type=Path);args=ap.parse_args()
    if args.report and (args.report.resolve()==ROOT or ROOT in args.report.resolve().parents):
        raise ValueError('Write reports outside the immutable return directory')
    outerbytes=(ROOT/'input/DD_Rank8_Damage6_Cast_History_Correction_02.zip').read_bytes()
    bind('actual submission',outerbytes,{'bytes':17596751,'sha256':'bf32ada9d9e21b491a45c53b44a8bc1974f35213b2636ebad77ad53583fbe0e4'})
    outer=safe_zip(outerbytes,'submission');om=json.loads(outer.read('MANIFEST.json'))
    check('submission10members',len(outer.namelist())==10,'archive')
    check('submission9bindings',len(om['files'])==9,'archive')
    for e in om['files']:
        bind('submission member:'+e['path'],outer.read(e['path']),e)
        if not e['path'].startswith('input/'):
            check('full submitted evidence preserved:'+e['path'],(ROOT/'cast_history_source'/e['path']).read_bytes()==outer.read(e['path']),'history')
    check('full submitted manifest preserved',(ROOT/'cast_history_source/MANIFEST.json').read_bytes()==outer.read('MANIFEST.json'),'history')
    oldbytes=outer.read('input/DD_Rank8_Damage_6_Part5_Correction_Return_02.zip')
    bind('exact Return02',oldbytes,{'bytes':17408791,'sha256':'6678b1cbe5d02104b38b2cdb4eee4b1eec434dc7a05e60889ed7153ef2f730cb'})
    old=safe_zip(oldbytes,'Return02');oldmanifest=json.loads(old.read('MANIFEST.json'))
    check('98 prior bindings',len(oldmanifest['files'])==98,'history')
    for e in oldmanifest['files']:bind('prior return member:'+e['path'],old.read(e['path']),e,'history')
    # Every extracted historical file is still the exact previous byte sequence.
    for name in old.namelist():
        if '/' not in name:
            check('extracted full old root:'+name,(ROOT/'history/return02'/name).read_bytes()==old.read(name),'history')
        elif name.startswith('history/return01/'):
            check('unchanged prior history:'+name,(ROOT/name).read_bytes()==old.read(name),'history')
    for name in old.namelist():
        if name.startswith(('context/','local_evidence/','baseline/','input/')):
            check('unchanged context/source archive:'+name,(ROOT/name).read_bytes()==old.read(name),'history')
    srcbytes=(ROOT/'input/DD_Rank8_Damage_6_Source_Conference_01.zip').read_bytes()
    bind('original source ZIP',srcbytes,{'bytes':2989121,'sha256':'b6448c425863a3230ba72088ea298b3b53e5f3f9b738806b1ca2152a31d88d87'})
    src=safe_zip(srcbytes,'source51');sm=json.loads(src.read('MANIFEST.json'))
    check('51 original source bindings',len(sm['files'])==51,'source')
    for e in sm['files']:bind('original full source:'+e['path'],src.read('sources/'+e['path']),e,'source')
    for e in om['files']:
        if e['path'].startswith('sources/'):
            check('supplied class/registry matches actual original source:'+e['path'],
                  outer.read(e['path'])==src.read('sources/'+e['source']['path']),'source')
    check('unchanged original candidate',(ROOT/'baseline/CANDIDATE.json').read_bytes()==src.read('CANDIDATE.json'),'history')
    for e in load('CONTEXT_BINDINGS.json')['files']:bind('full current context:'+e['file'],(ROOT/e['file']).read_bytes(),e,'source')
    m=json.loads(old.read('MODEL.json'));n=load('MODEL.json');cases=load('CASE_DISPOSITIONS.json')
    bind('bound Return02 MODEL',old.read('MODEL.json'),{'bytes':1753895,'sha256':'d58674925ea0711de915b713099c0cec55d687f7ceab86e41047563e4c0e9514'})
    plans=['EXACT_OPERATIONS_FROM_RETURN02.json','EXACT_OPERATIONS_FROM_SOURCE.json']
    for name in plans:
        p=load(name);base=(ROOT/p['base']['file']).read_bytes();target=(ROOT/p['successor']['file']).read_bytes()
        bind(name+':base',base,p['base']);bind(name+':successor',target,p['successor'])
        check(name+':count',len(p['operations'])==p['operationCount'],'full-value')
        f=replay(json.loads(base),p['operations'],label=name)
        b=replay(json.loads(target),p['operations'],True,label=name)
        check(name+':complete forward bytes',jb(f)==target,'full-value')
        check(name+':complete reverse bytes',jb(b)==base,'full-value')
        try:replay(f,p['operations'],record=False)
        except (ValueError,KeyError,IndexError):rejected=True
        else:rejected=False
        check(name+':repeat-forward rejected',rejected,'guard')
        tampered=json.loads(base);tampered['id']='unapproved-baseline'
        try:replay(tampered,p['operations'],record=False)
        except (ValueError,KeyError,IndexError):rejected=True
        else:rejected=False
        check(name+':full-before drift rejected',rejected,'guard')
    check('all54 earlier operations preserved verbatim',load(plans[1])['operations'][:54]==json.loads(old.read('EXACT_OPERATIONS_FROM_SOURCE.json'))['operations'],'history')
    paths=['/currentVectors/9/actorSheets/anchorCaster']+[f'/currentVectors/9/independentBranches/{i}/actorSheets/anchorCaster' for i in range(8)]
    expect={'/id','/status','/castHistoryQualificationConference13'}|{p+'/'+f for p in paths for f in ['initialSetup','matrixFamiliesUsed']}
    check('only exact18 actor leaves and3 metadata values changed',set(delta_paths(m,n))==expect,'preservation')
    for p in paths:
        a=at(m,p);b=at(n,p)
        check('original empty history:'+p,a['matrixFamiliesUsed']==[],'history')
        check('correct spent history:'+p,b['matrixFamiliesUsed']==['dimensional-anchor'],'state')
        check('same encounter expressly bound:'+p,'SAME-ENCOUNTER QUALIFICATION RD8-LOCAL70-01' in b['initialSetup'],'state')
        ac=copy.deepcopy(a);bc=copy.deepcopy(b)
        for x in [ac,bc]:x.pop('initialSetup');x.pop('matrixFamiliesUsed')
        check('all remaining full actor data preserved:'+p,ac==bc,'preservation')
    for key in m:
        if key not in ['id','status','currentVectors']:
            check('complete MODEL field unchanged:'+key,m[key]==n[key],'preservation')
    check('full case array mirror',n['currentVectors']==cases['allCases'],'mirror')
    check('12main42branches',len(cases['allCases'])==12 and sum(len(c['independentBranches']) for c in cases['allCases'])==42,'preservation')
    for i,(a,b) in enumerate(zip(m['currentVectors'],n['currentVectors'])):
        if i!=9:check('unchanged complete main:'+a['id'],a==b,'preservation')
        else:
            for oldc,newc in zip([a]+a['independentBranches'],[b]+b['independentBranches']):
                for key in oldc:
                    if key not in ['actorSheets','independentBranches']:
                        check('unchanged case outcome/event:'+oldc['id']+':'+key,oldc[key]==newc[key],'preservation')
    for name in ['PLAYER_CHAPTER.md','SPELL_DISPOSITIONS.json','NEW_SCOPED_AUTHORSHIP.json','QUESTION_DISPOSITIONS.json','HOLD_REGISTER.json','ORIGINAL_HISTORIES.json','SOURCE_BINDINGS.json','SOURCE_AUTHORITY.json','COUNTERPART_DISPOSITIONS.json','INTERFACE_USAGE.json','specification_tests.py']:
        check('unchanged complete operative artifact:'+name,(ROOT/name).read_bytes()==old.read(name),'preservation')
    director=(ROOT/'DIRECTOR_REVIEW.md').read_text()
    check('complete Director case block matches',json.dumps(cases,indent=2,ensure_ascii=False) in director,'mirror')
    for i,r in enumerate(n['records']):
        check('complete Director procedure exact:'+str(i),r['procedure'] in director,'mirror')
    for q in n['reviewQuestionDispositions02']:
        check('complete Director answer exact:'+q['id'],json.dumps(q,indent=2,ensure_ascii=False) in director,'mirror')
    check('actual reported334/333/1 retained',load('cast_history_source/LOCAL_SEMANTIC_RECONCILIATION.json')['diagnosticCheckCount']==334 and load('cast_history_source/LOCAL_SEMANTIC_RECONCILIATION.json')['diagnosticFailures']==1,'history')
    report=load('cast_history_source/LOCAL_SEMANTIC_RECONCILIATION.json')
    check('actual333 reported passes',sum(x['passed'] for x in report['diagnosticChecks'])==333,'history')
    check('withdrawn literal test remains withdrawn',load('FINDING_DISPOSITIONS.json')['withdrawnAssertion']==report['diagnosticScopeCorrection'],'history')
    # Exact complete source excerpts, not recalled source wording.
    for i,e in enumerate(load('CAST_HISTORY_SOURCE_EVIDENCE.json')['completeExcerpts']):
        s=e['source'];b=(ROOT/s['path']).read_bytes();bind('excerpt source:'+str(i),b,s,'reference')
        if 'pointer' in s:check('exact complete source value:'+str(i),at(json.loads(b),s['pointer'])==e['completeValue'],'reference')
        else:check('exact full source section:'+str(i),e['completeValue'] in b.decode('utf8'),'reference')
    h=load('AFFECTED_CASE_HISTORY.json')
    check('full affected case before',h['cases'][0]['before']==m['currentVectors'][9],'history')
    check('full affected case after',h['cases'][0]['after']==n['currentVectors'][9],'history')
    for e in h['allNineFullActorObjects']:
        check('full actor comparison:'+e['modelPointer'],e['before']==at(m,e['modelPointer']) and e['after']==at(n,e['modelPointer']),'history')
    a=load('ARTIFACT_OPERATIONS_FROM_RETURN02.json')
    for e in a['files']:
        before=(ROOT/e['before']['path']).read_bytes();after=(ROOT/e['after']['path']).read_bytes()
        bind('whole-artifact baseline:'+e['after']['path'],before,e['before'],'full-value')
        bind('whole-artifact successor:'+e['after']['path'],after,e['after'],'full-value')
        check('whole-file forward bytes:'+e['after']['path'],e['operation']['after'].encode('utf8')==after,'full-value')
        check('whole-file reverse bytes:'+e['after']['path'],e['operation']['before'].encode('utf8')==before,'full-value')
    for e in load('ARTIFACT_BINDINGS.json')['newArtifacts']:
        bind('new artifact:'+e['path'],(ROOT/e['path']).read_bytes(),e,'hash')
    for nfile in ['specification_tests.py','cast_history_specification_tests.py','verify_bundle.py']:
        tree=ast.parse((ROOT/nfile).read_bytes())
        check('syntax:'+nfile,True,'specification')
        imports=[x.module or '' for x in ast.walk(tree) if isinstance(x,ast.ImportFrom)]
        check('no project from-import:'+nfile,all(not t.startswith(('feat335','druid','wizard','game','Unity')) for t in imports),'specification')
    retained=load('SPECIFICATION_REPORT.json');new=load('CAST_HISTORY_SPECIFICATION_REPORT.json')
    check('96 retained tests report pass',(retained['testsRun'],retained['failures'],retained['errors'])==(96,0,0),'specification')
    check('retained report exact current case binding',retained['casesSha256']==sha((ROOT/'CASE_DISPOSITIONS.json').read_bytes()),'specification')
    check('28 targeted tests report pass',(new['testsRun'],new['failures'],new['errors'])==(28,0,0),'specification')
    check('targeted report exact current MODEL binding',new['modelSha256']==sha((ROOT/'MODEL.json').read_bytes()),'specification')
    num=load('NUMERICAL_STATE_EVIDENCE.json');diag=load('CAST_HISTORY_DIAGNOSTIC.json')
    check('whole computed final equals authored independent final',num['independentlyComputedFinal']==diag['expectedFinalState'],'state')
    check('new history correct old omission detected',not num['oldNineSheetPredicate'] and num['newNineSheetPredicate'],'state')
    check('repeated spell has correct two separate strain components',num['requiredRepeatedBase']==1 and num['actualRepeatedRefrain']==1 and num['correctDissonanceAfter']==2 and num['oldOmissionCounterfactual']['DissonanceAfter']==1,'state')
    check('new diagnostic is independent not appended',diag['classification'].startswith('SEPARATE_') and not diag['originalMainAndBranchOutcomesEdited'],'scope')
    receipt=load('REVIEW_RECEIPT.json')
    check('unchanged applied and unapplied baseline',receipt['unchangedAppliedCounts']==[525,323,249,173] and receipt['acceptedButUnappliedUnchanged']==39,'scope')
    check('no local acceptance or runtime claim',not receipt['independentRank8Acceptance'] and not receipt['independentRank7Acceptance'] and receipt['projectWrites']==0 and receipt['runtimeTests']==0,'scope')
    if args.manifest:
        man=load('MANIFEST.json');paths=[e['path'] for e in man['files']]
        actual={p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file() and p!=ROOT/'MANIFEST.json'}
        check('manifest exact file membership',set(paths)==actual,'manifest')
        check('manifest unique/count',len(paths)==len(set(paths))==man['fileCount'],'manifest')
        for e in man['files']:bind('return-file:'+e['path'],(ROOT/e['path']).read_bytes(),e,'manifest')
    report={'id':'RD8-CAST-HISTORY-READONLY-VERIFICATION-13','checkCount':len(checks),'failures':sum(not x['passed'] for x in checks),'categories':dict(Counter(x['category'] for x in checks)),'checks':checks,'manifestIncluded':args.manifest,'scope':'Read-only full source/hash/replay/preservation checks; isolated test reports separately identified; no local diagnostic or project engine script executed here.','runtimeTests':0,'projectWrites':0}
    if args.report:
        with args.report.open('x',encoding='utf8') as f:f.write(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='checks'},indent=2))

if __name__=='__main__':main()
