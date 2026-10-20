#!/usr/bin/env python3
"""Read-only verification of this bounded RD8 proposal. Never applies project files.
Only an explicitly requested NEW report path is written. No archived script is executed.
"""
from __future__ import annotations
import argparse, ast, copy, hashlib, io, json, stat, zipfile
from collections import Counter
from pathlib import Path, PurePosixPath

ROOT=Path(__file__).resolve().parent
checks=[]
def sha(b):return hashlib.sha256(b).hexdigest()
def jb(x):return (json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode('utf8')
def load(p):return json.loads((ROOT/p).read_text(encoding='utf8'))
def check(name,ok,category='structure',detail=None):
    checks.append({'id':name,'category':category,'passed':bool(ok),'detail':detail})
    if not ok:raise AssertionError(name)
def file(p):
    rel=PurePosixPath(p)
    if rel.is_absolute() or '..' in rel.parts or '\\' in p:raise ValueError('unsafe path')
    result=ROOT.joinpath(*rel.parts)
    if not result.resolve().is_relative_to(ROOT):raise ValueError('outside package')
    return result
def bind(name,b,expected,category='source'):
    check(name, len(b)==expected['bytes'] and sha(b)==expected['sha256'],category,
          {'bytes':len(b),'sha256':sha(b)})
def zip_open(name,b):
    z=zipfile.ZipFile(io.BytesIO(b))
    ns=z.namelist()
    check(name+':safe_unique',len(ns)==len(set(ns)) and all(
        not PurePosixPath(n).is_absolute() and '..' not in PurePosixPath(n).parts and '\\' not in n
        and not(stat.S_ISLNK(z.getinfo(n).external_attr>>16)) for n in ns),'archive')
    check(name+':CRC',z.testzip() is None,'archive')
    return z
def parts(p):return [s.replace('~1','/').replace('~0','~') for s in p[1:].split('/')]
def at(x,p):
    if p=='':return x
    for s in parts(p):x=x[int(s)] if isinstance(x,list) else x[s]
    return x
def replay(x,ops,reverse=False,prefix='replay'):
    result=copy.deepcopy(x)
    for i,op in enumerate(reversed(ops) if reverse else ops):
        parent=result;tokens=parts(op['pointer'])
        for t in tokens[:-1]:parent=parent[int(t)] if isinstance(parent,list) else parent[t]
        k=int(tokens[-1]) if isinstance(parent,list) else tokens[-1]
        if reverse:
            check(f'{prefix}:{i}:{op["pointer"]}:after',parent[k]==op['after'],'full_value')
            if op['beforeExists']:parent[k]=copy.deepcopy(op['before'])
            else:del parent[k]
        else:
            check(f'{prefix}:{i}:{op["pointer"]}:before',
                  parent[k]==op['before'] if op['beforeExists'] else k not in parent,'full_value')
            parent[k]=copy.deepcopy(op['after'])
    return result
def walk(x,p=''):
    yield p,x
    if isinstance(x,dict):
        for k,v in x.items():yield from walk(v,p+'/'+str(k).replace('~','~0').replace('/','~1'))
    elif isinstance(x,list):
        for i,v in enumerate(x):yield from walk(v,p+'/'+str(i))
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--report',type=Path);ap.add_argument('--manifest',action='store_true')
    args=ap.parse_args()
    incoming_path='input/DD_Rank8_Damage6_Local_Corrections_01.zip'
    incoming=file(incoming_path).read_bytes()
    bind('incoming archive',incoming,{'bytes':5204994,'sha256':'c8264a558ae3e6f6581f3f1d32dc1b4ac4866908cec7c732d23028590a1003ac'},'archive')
    z=zip_open('incoming',incoming)
    im=json.loads(z.read('MANIFEST.json'))
    for e in im['files']:bind('incoming:'+e['path'],z.read(e['path']),e)
    rb=z.read('input/DD_Rank8_Damage_6_Part5_Conference_Return_01.zip')
    bind('original return archive',rb,{'bytes':4912092,'sha256':'119bfa063012d4c8c870ad6385c680a7c00c153d778c83bad08ae9895ff935d0'},'archive')
    oldz=zip_open('original return',rb);om=json.loads(oldz.read('MANIFEST.json'))
    for e in om['files']:bind('old manifest:'+e['path'],oldz.read(e['path']),e)
    for n in oldz.namelist():
        if not n.endswith('/'):check('history exact:'+n,file('history/return01/'+n).read_bytes()==oldz.read(n),'history')
    # Full original source archive and complete51 sources; no preparation program executed.
    sn=next(n for n in oldz.namelist() if n.startswith('input/') and n.endswith('.zip'))
    source_bytes=oldz.read(sn)
    check('source root copy exact',file(sn).read_bytes()==source_bytes,'history')
    sz=zip_open('source conference',source_bytes);sm=json.loads(sz.read('MANIFEST.json'))
    check('source count51',len(sm['files'])==51,'source')
    for e in sm['files']:bind('source:'+e['path'],sz.read('sources/'+e['path']),e)
    bind('source candidate',sz.read('CANDIDATE.json'),sm['candidate'])
    check('source baseline exact',file('baseline/CANDIDATE.json').read_bytes()==sz.read('CANDIDATE.json'),'history')
    # Five actually bound local class/registry files equal both current local evidence and old frozen sources.
    for e in im['files']:
        if e['path'].startswith('sources/'):
            check('current evidence exact:'+e['path'],file('local_evidence/'+e['path']).read_bytes()==z.read(e['path']),'source')
            if e['path'] in sz.namelist():
                frozen=sz.read(e['path']);anchor='original source packet'
            else:
                # The additional Warrior source was supplied as a complete later context, not one of the51 packet files.
                check('only known extra context source',e['path']=='sources/DescentReviewChanges/ReviewBible/data/public/class_playtests/warrior.json','source')
                frozen=oldz.read('context/warrior.json');anchor='original return context/warrior.json'
            check('current-vs-frozen:'+e['path'],z.read(e['path'])==frozen,'source',{'anchor':anchor})
    for n in ('REQUEST.txt','LOCAL_SEMANTIC_REVIEW.json','LOCAL_DIAGNOSTICS.py','MANIFEST.json'):
        check('local original:'+n,file('local_evidence/'+n).read_bytes()==z.read(n),'history')
    local=load('local_evidence/LOCAL_SEMANTIC_REVIEW.json')
    check('eight actual findings',len(local['findings'])==8,'source')
    check('supplied diagnostics not relabelled',local['diagnosticCheckCount']==96 and local['diagnosticFailures']==4,'source')
    for n in [n for n in oldz.namelist() if n.startswith('context/') and not n.endswith('/')]:
        check('full context exact:'+n,file(n).read_bytes()==oldz.read(n),'source')
    old=json.loads(oldz.read('MODEL.json'));new=load('MODEL.json')
    oldcases=json.loads(oldz.read('CASE_DISPOSITIONS.json'));cases=load('CASE_DISPOSITIONS.json')
    check('original MODEL binding',len(oldz.read('MODEL.json'))==1673824 and sha(oldz.read('MODEL.json'))=='df8dd333da82c14178d21657e0702671506e1c30d3ed87d5204993ef8061bc90','source')
    for planfile in('EXACT_OPERATIONS_FROM_RETURN01.json','EXACT_OPERATIONS_FROM_SOURCE.json'):
        plan=load(planfile);base=file(plan['base']['file']).read_bytes();target=file(plan['successor']['file']).read_bytes()
        bind(planfile+':base',base,plan['base']);bind(planfile+':target',target,plan['successor'])
        check(planfile+':count',len(plan['operations'])==plan['operationCount'],'full_value')
        forward=replay(json.loads(base),plan['operations'],prefix=planfile+':forward')
        reverse=replay(json.loads(target),plan['operations'],True,prefix=planfile+':reverse')
        check(planfile+':full_forward_bytes',jb(forward)==target,'full_value')
        check(planfile+':full_reverse_bytes',jb(reverse)==base,'full_value')
    composed=load('EXACT_OPERATIONS_FROM_SOURCE.json');prior=json.loads(oldz.read('EXACT_OPERATIONS_FROM_SOURCE.json'))
    check('37 old operations verbatim',composed['operations'][:37]==prior['operations'],'history')
    apath=file('ARTIFACT_OPERATIONS_FROM_RETURN01.json')
    if apath.exists():
        art=load('ARTIFACT_OPERATIONS_FROM_RETURN01.json')
        for e in art['files']:
            before=file(e['before']['path']).read_bytes();after=file(e['after']['path']).read_bytes()
            bind('artifact before:'+e['after']['path'],before,e['before'])
            bind('artifact after:'+e['after']['path'],after,e['after'])
            if e['kind']=='json-full-value':
                check('full artifact before:'+e['after']['path'],json.loads(before)==e['operation']['before'],'full_value')
                check('full artifact after:'+e['after']['path'],json.loads(after)==e['operation']['after'],'full_value')
                check('artifact forward bytes:'+e['after']['path'],jb(e['operation']['after'])==after,'full_value')
                check('artifact reverse bytes:'+e['after']['path'],jb(e['operation']['before'])==before,'full_value')
            else:
                check('full text forward:'+e['after']['path'],e['operation']['after'].encode('utf8')==after,'full_value')
                check('full text reverse:'+e['after']['path'],e['operation']['before'].encode('utf8')==before,'full_value')
    check('six identities preserved',len(new['records'])==6,'preservation')
    for i,(a,b) in enumerate(zip(old['records'],new['records'])):
        ac,bc=copy.deepcopy(a),copy.deepcopy(b);ac.pop('procedure');bc.pop('procedure')
        check('native record/history/access exact:'+str(i),ac==bc,'preservation')
        if i!=2:check('unchanged full procedure:'+str(i),a['procedure']==b['procedure'],'preservation')
    check('six shared clauses byte-for-data unchanged',old['selectedSharedRules']==new['selectedSharedRules'],'preservation')
    for k in old:
        if k not in('id','recordedAtUtc','status','records','currentVectors','reviewQuestionDispositions02','proposedScopedRuleSelections02','reviewBoundaries02'):
            check('untouched MODEL field:'+k,old[k]==new[k],'preservation')
    check('model-case complete mirror',new['currentVectors']==cases['allCases'],'mirrors')
    check('case counts12/42',cases['mainCaseCount']==12 and cases['independentBranchCount']==42 and
          len(cases['allCases'])==12 and sum(len(x['independentBranches']) for x in cases['allCases'])==42,'structure')
    check('all prior case/branch IDs retained',set(c['id'] for c in oldcases['allCases'])==set(c['id'] for c in cases['allCases']) and
          {b['id'] for c in oldcases['allCases'] for b in c['independentBranches']}.issubset(
          {b['id'] for c in cases['allCases'] for b in c['independentBranches']}),'preservation')
    for i,c in enumerate(cases['allCases']):
        check('original scenario link exact:'+c['id'],c['originalScenarioHistory']==oldcases['allCases'][i]['originalScenarioHistory'],'preservation')
        if i not in(1,2,5,6,7,9,10,11):check('whole untouched case:'+c['id'],c==oldcases['allCases'][i],'preservation')
        check('no runtime claim:'+c['id'],c['runtimeExecuted'] is False and all(b['runtimeExecuted'] is False for b in c['independentBranches']),'scope')
    questions=load('QUESTION_DISPOSITIONS.json');spells=load('SPELL_DISPOSITIONS.json');authors=load('NEW_SCOPED_AUTHORSHIP.json')
    check('question mirror',questions==new['reviewQuestionDispositions02'],'mirrors')
    check('20 full question originals',len(questions)==20 and all(
          q['completeSubmittedQuestionUnchanged']==old['reviewQuestionDispositions02'][i]['completeSubmittedQuestionUnchanged']
          for i,q in enumerate(questions)),'preservation')
    for i in range(20):
        if i not in(7,8):check('unchanged full answer:'+str(i),questions[i]==old['reviewQuestionDispositions02'][i],'preservation')
    check('authorship full mirrors',authors['completeSpellRules']==spells and authors['decisions']==questions and
          authors['completeSharedRules']==new['selectedSharedRules'],'mirrors')
    check('new authorship strictly scoped',authors['ids']==new['proposedScopedRuleSelections02'] and
          authors['ids'][:-1]==old['proposedScopedRuleSelections02'] and authors['ids'][-1]=='RD8-PYRE-READY-BATCH-03','scope')
    player=file('PLAYER_CHAPTER.md').read_text();director=file('DIRECTOR_REVIEW.md').read_text()
    for i,s in enumerate(spells):
        check('full spell mirror:'+str(i),s['procedure']==new['records'][i]['procedure'],'mirrors')
        check('player complete procedure:'+str(i),s['procedure'] in player,'mirrors')
        check('director complete procedure:'+str(i),s['procedure'] in director,'mirrors')
        for q in s['sourceConflictAnswers']:
            check('complete spell question:'+str(i)+':'+q['id'],q==next(x for x in questions if x['id']==q['id']),'mirrors')
    for q in questions:check('full director question:'+q['id'],json.dumps(q,indent=2,ensure_ascii=False) in director,'mirrors')
    check('full director case block',json.dumps(cases,indent=2,ensure_ascii=False) in director,'mirrors')
    hold=load('HOLD_REGISTER.json')
    check('full director hold block',json.dumps(hold,indent=2,ensure_ascii=False) in director,'mirrors')
    check('model holds match',new['reviewBoundaries02']==hold,'mirrors')
    check('five unrelated holds retained',hold['retainedIndependentWholePositiveCaseHolds']==
          old['reviewBoundaries02']['retainedIndependentWholePositiveCaseHolds'],'preservation')
    check('10 external branches retained',len(hold['conditionalExternalBranches'])==10,'scope')
    f=load('FINDING_DISPOSITIONS.json')
    for i,r in enumerate(f['findings']):
        check('submitted full finding preserved:'+r['id'],r['completeSubmittedFinding']==local['findings'][i],'history')
        for p in r['successorModelPointers']:
            check('finding pointer:'+r['id']+p,at(new,p) is not None,'references')
    ev=load('CORRECTION_SOURCE_EVIDENCE.json')
    for i,e in enumerate(ev['completeExcerpts']):
        ref=e['source'];b=file(ref['path']).read_bytes()
        bind('excerpt source:'+str(i),b,ref)
        check('exact excerpt:'+str(i),at(json.loads(b),ref['pointer'])==e['completeValue'],'references')
    for name in('ORIGINAL_HISTORIES.json','COUNTERPART_DISPOSITIONS.json','INTERFACE_USAGE.json',
                'SOURCE_BINDINGS.json','INPUT_BINDINGS.json','EXTRA_SOURCE_BINDINGS.json','CONTEXT_BINDINGS.json','SOURCE_AUTHORITY.json'):
        check('unchanged root artifact:'+name,file(name).read_bytes()==oldz.read(name),'preservation')
    # Preserve all62 prior test methods exactly in AST, not just their test names.
    old_ast=ast.parse(oldz.read('specification_tests.py'));new_ast=ast.parse(file('specification_tests.py').read_text())
    def tests(tree):return {n.name:ast.dump(n,include_attributes=False) for n in ast.walk(tree)
                           if isinstance(n,ast.FunctionDef) and n.name.startswith('test_')}
    ot,nt=tests(old_ast),tests(new_ast)
    check('96 total parsed tests',len(ot)==62 and len(nt)==96,'specification')
    for name,value in ot.items():check('old test preserved:'+name,nt[name]==value,'specification')
    report=load('SPECIFICATION_REPORT.json')
    check('isolated report result',report['testsRun']==96 and report['failures']==0 and report['errors']==0,'specification')
    check('isolated report case binding',report['casesSha256']==sha(file('CASE_DISPOSITIONS.json').read_bytes()),'specification')
    history=load('AFFECTED_CASE_HISTORY.json')
    for e in history['cases']:
        oldcase=next(c for c in oldcases['allCases'] if c['id']==e['id'])
        newcase=next(c for c in cases['allCases'] if c['id']==e['id'])
        check('full case before/after history:'+e['id'],e['before']==oldcase and e['after']==newcase,'history')
    check('scope applied unchanged',new['boundedCorrectionConference03']['appliedChanges']==0 and
          new['boundedCorrectionConference03']['newIndependentLocalAcceptances']==0 and
          hold['boundedCorrectionScope']['unchangedAppliedCounts']==[525,323,249,173],'scope')
    if args.manifest:
        manifest=load('MANIFEST.json')
        paths=[e['path'] for e in manifest['files']]
        check('manifest set exact',set(paths)=={str(p.relative_to(ROOT)).replace('\\\\','/') for p in ROOT.rglob('*') if p.is_file() and p!=ROOT/'MANIFEST.json'},'manifest')
        check('manifest uniqueness',len(paths)==len(set(paths))==manifest['fileCount'],'manifest')
        for e in manifest['files']:bind('return member:'+e['path'],file(e['path']).read_bytes(),e,'manifest')
    summary={'id':'RD8-CORRECTION-READONLY-VERIFICATION-03','checkCount':len(checks),
             'failures':sum(not c['passed'] for c in checks),'categories':dict(Counter(c['category'] for c in checks)),
             'checks':checks,'scope':'Read-only source/structure/replay/preservation. No archived project/diagnostic script executed; no game runtime.',
             'manifestIncluded':args.manifest,'runtimeTests':0,'projectWrites':0}
    if args.report:
        with args.report.open('x',encoding='utf8') as h:json.dump(summary,h,indent=2,ensure_ascii=False);h.write('\n')
    print(json.dumps({k:v for k,v in summary.items() if k!='checks'},indent=2))
if __name__=='__main__':main()
