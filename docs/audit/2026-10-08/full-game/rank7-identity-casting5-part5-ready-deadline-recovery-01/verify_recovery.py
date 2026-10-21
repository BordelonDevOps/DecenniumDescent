#!/usr/bin/env python3
"""Read-only data/source/replay verifier for the distinct Rank7 recovery delivery.

No supplied/downloaded scripts or project modules are executed or imported.
Reports are written only to a new path outside the package. Verification is not
semantic acceptance, game-engine execution, scheduler integration or balance.
"""
from __future__ import annotations
import argparse, ast, copy, hashlib, io, json, stat, zipfile
from pathlib import Path, PurePosixPath
from typing import Any

INPUT_NAME='DD_Rank7_Exact_Model_Recovery_77.zip'
INPUT_SIZE=65655383
INPUT_SHA='8fd6800e8654c2efa9fc0505b86c183d3520602d9adc7d6b6e8247fceb87c0eb'
BASE_MEMBER='input/DD_Rank7_Identity_Casting_5_Part5_Correction_Return_02.zip'
BASE_SIZE=64667556
BASE_SHA='d063125b1b570230afa9cef56714efc26d011dd9ca0dd56c064d5473c85b63a1'
MODEL_SHA='949ef5c6a1f05c1b0823d9ec4e10cd3e387a0c8c918680e95fa0047b60e40e3a'
BASE_MODEL_SHA='fbdfd5c299d7a501d53eedad03df82211da312df783b06d68e1dae3de5fd0a36'
BRANCH='/currentVectors/2/independentBranches/0'

def sha(b: bytes) -> str:return hashlib.sha256(b).hexdigest()
def enc(x: Any) -> bytes:return (json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
def pointer(obj: Any, path: str) -> Any:
    for part in path.lstrip('/').split('/') if path else []:
        part=part.replace('~1','/').replace('~0','~')
        obj=obj[int(part)] if isinstance(obj,list) else obj[part]
    return obj

def replay(obj: Any, operations: list, reverse: bool=False) -> Any:
    result=copy.deepcopy(obj)
    for op in reversed(operations) if reverse else operations:
        path=op['pointer']; parent_path,leaf=path.rsplit('/',1)
        parent=pointer(result,parent_path); leaf=leaf.replace('~1','/').replace('~0','~')
        key=int(leaf) if isinstance(parent,list) else leaf
        exists=(0<=key<len(parent)) if isinstance(parent,list) else key in parent
        want_exists=op.get('afterExists',True) if reverse else op.get('beforeExists',True)
        expected=op['after'] if reverse else op['before']
        if exists!=want_exists:raise AssertionError(f'Existence mismatch {path}')
        if exists and (type(parent[key]) is not type(expected) or parent[key]!=expected):
            raise AssertionError(f'Full-value mismatch {path}')
        destination_exists=op.get('beforeExists',True) if reverse else op.get('afterExists',True)
        if destination_exists:parent[key]=copy.deepcopy(op['before'] if reverse else op['after'])
        else:del parent[key]
    return result

def diff(a:Any,b:Any,path:str='')->list:
    if type(a) is not type(b):return [path]
    if isinstance(a,dict):
        if list(a)!=list(b):return [path+'/<key-or-order-change>']
        return [d for k in a for d in diff(a[k],b[k],path+'/'+k.replace('~','~0').replace('/','~1'))]
    if isinstance(a,list):
        if len(a)!=len(b):return [path+'/<length-change>']
        return [d for j,(x,y) in enumerate(zip(a,b)) for d in diff(x,y,path+'/'+str(j))]
    return [path] if a!=b else []

def verify(root:Path, history:Path, with_manifest:bool=False)->dict:
    checks=[]
    def ck(group,name,condition):
        passed=bool(condition);checks.append({'group':group,'check':name,'passed':passed})
        if not passed:raise AssertionError(group+': '+name)
    def read(name):return json.loads((root/name).read_bytes())
    def bound(raw,rec):return len(raw)==rec['bytes'] and sha(raw)==rec['sha256']
    def zip_valid(z,label):
        names=z.namelist()
        safe=len(names)==len(set(names))
        for info in z.infolist():
            p=PurePosixPath(info.filename)
            safe=safe and not p.is_absolute() and '..' not in p.parts and '\\' not in info.filename and not stat.S_ISLNK(info.external_attr>>16)
        ck('archive',label+' safe unique members',safe)
        ck('archive',label+' complete CRC',z.testzip() is None)
    def manifest_files(z,label):
        entries=json.loads(z.read('MANIFEST.json'))['files']
        ck('archive',label+' manifest covers complete archive except itself',
           {e['path'] for e in entries}==set(z.namelist())-{'MANIFEST.json'})
        for e in entries:ck('source_binding',label+' '+e['path'],bound(z.read(e['path']),e))
    def scan_strings(x):
        if isinstance(x,dict):
            for v in x.values():yield from scan_strings(v)
        elif isinstance(x,list):
            for v in x:yield from scan_strings(v)
        elif isinstance(x,str):yield x
    raw_history=history.read_bytes()
    ck('archive','supplied recovery input exact bytes/hash',len(raw_history)==INPUT_SIZE and sha(raw_history)==INPUT_SHA)
    with zipfile.ZipFile(io.BytesIO(raw_history)) as h:
        zip_valid(h,'recovery input');manifest_files(h,'recovery input')
        ck('archive','25 supplied members',len(h.namelist())==25)
        raw_base=h.read(BASE_MEMBER)
        ck('archive','complete Return02 exact bytes/hash',len(raw_base)==BASE_SIZE and sha(raw_base)==BASE_SHA)
        with zipfile.ZipFile(io.BytesIO(raw_base)) as b:
            zip_valid(b,'Return02');manifest_files(b,'Return02')
            ck('archive','73 Return02 members',len(b.namelist())==73)
            original=b.read('MODEL.json');recovered=h.read('MODEL.json');local=(root/'MODEL.json').read_bytes()
            ck('model','Return02 MODEL binding',len(original)==12000315 and sha(original)==BASE_MODEL_SHA)
            ck('model','supplied reported MODEL binding',len(recovered)==12000315 and sha(recovered)==MODEL_SHA)
            ck('model','MODEL exact copied bytes; not reserialized metadata',local==recovered)
            old=json.loads(original);m=json.loads(local)
            opdoc=read('EXACT_OPERATIONS_FROM_RETURN02.json');ops=opdoc['operations']
            ck('replay','six supplied operations preserved byte-identically',(root/'EXACT_OPERATIONS_FROM_RETURN02.json').read_bytes()==h.read('EXACT_OPERATIONS_FROM_RETURN02.json'))
            ck('replay','six exact scalar differences only',diff(old,m)==[o['pointer'] for o in ops])
            ck('replay','all six full-value62-to61 replacements',len(ops)==6 and all(o['before']==62 and o['after']==61 for o in ops))
            ck('replay','full forward bytes from Return02',enc(replay(old,ops))==local)
            ck('replay','full reverse bytes to Return02',enc(replay(m,ops,True))==original)
            for file,expected_n,oldplan in [('EXACT_OPERATIONS_FROM_SOURCE.json',44,'EXACT_OPERATIONS_FROM_SOURCE.json'),('EXACT_OPERATIONS_FROM_RETURN01.json',17,'EXACT_OPERATIONS_FROM_RETURN01.json')]:
                plan=read(file);baseline=(root/plan['baseline']['path']).read_bytes();prior=json.loads(b.read(oldplan))
                ck('replay',file+' exact bound baseline',bound(baseline,plan['baseline']))
                ck('replay',file+' inherited full operations exact',plan['operations'][:-6]==prior['operations'])
                ck('replay',file+' six appended operations exact',plan['operations'][-6:]==ops)
                ck('replay',file+' total count',plan['operationCount']==len(plan['operations'])==expected_n)
                ck('replay',file+' entire forward bytes',enc(replay(json.loads(baseline),plan['operations']))==local)
                ck('replay',file+' entire reverse bytes',enc(replay(m,plan['operations'],True))==baseline)
            for fn in ['baseline/RETURN02_MODEL.json','baseline/RETURN01_MODEL.json','baseline/CANDIDATE.json']:
                member='MODEL.json' if fn=='baseline/RETURN02_MODEL.json' else fn
                ck('history',fn+' exact complete baseline',(root/fn).read_bytes()==b.read(member))
            # Unchanged complete model fields, including metadata and former39-status context.
            for key in m:
                if key!='currentVectors':ck('model_preservation','entire unchanged field /'+key,m[key]==old[key])
            ck('model','10 main cases,39 branches,11 conditional register',len(m['currentVectors'])==10 and sum(len(c['independentBranches']) for c in m['currentVectors'])==39 and len(m['conditionalBranchRegister'])==11)
            for j,(oc,nc) in enumerate(zip(old['currentVectors'],m['currentVectors'])):
                if j!=2:ck('case_preservation','entire unchanged main '+nc['id'],oc==nc)
                else:
                    for key in nc:
                        if key!='independentBranches':ck('case_preservation','affected parent unchanged field '+key,oc[key]==nc[key])
                    for k,nb in enumerate(nc['independentBranches']):
                        if k:ck('case_preservation','entire unchanged branch '+nb['id'],nb==oc['independentBranches'][k])
            br=pointer(m,BRANCH);ob=pointer(old,BRANCH)
            hist=read('AFFECTED_CASE_HISTORY.json')
            ck('case_preservation','complete supplied branch before/after',hist['branch']==json.loads(h.read('COMPLETE_AFFECTED_BRANCH.json')) and hist['branch']['before']==ob and hist['branch']['after']==br)
            ck('case_preservation','full parent before/after',hist['parentCase']['before']==old['currentVectors'][2] and hist['parentCase']['after']==m['currentVectors'][2])
            for rec in hist['sixCompleteStatePairs']:
                ck('case_preservation','full state before '+rec['modelPointer'],rec['before']==pointer(old,rec['modelPointer']))
                ck('case_preservation','full state after '+rec['modelPointer'],rec['after']==pointer(m,rec['modelPointer']))
            # Full operational mirrors, not identifier-only checks.
            ck('mirrors','all current cases complete',read('CASE_DISPOSITIONS.json')['cases']==m['currentVectors'])
            ck('mirrors','all raw worked cases complete',read('evidence/worked_cases.json')==m['currentVectors'])
            ck('mirrors','all selected question dispositions complete',read('QUESTION_DISPOSITIONS.json')['dispositions']==m['selectedQuestionDispositions'])
            procs=read('evidence/procedures.json');spells=read('SPELL_DISPOSITIONS.json')['dispositions']
            for rec,disp in zip(m['records'],spells):
                sid=rec['spellId'];p=rec['proposedProcedure']
                ck('mirrors',sid+' full source/access/authoring record unchanged',rec==old['records'][m['records'].index(rec)])
                ck('mirrors',sid+' full disposition procedure',disp['spellId']==sid and disp['fullSelectedProcedure']==p)
                ck('mirrors',sid+' raw JSON procedure',procs[sid]==p)
                ck('mirrors',sid+' raw MD procedure',(root/('evidence/procedure_'+sid+'.md')).read_text().strip()==p.strip())
                for chap in ['PLAYER_CHAPTER.md','DIRECTOR_REVIEW.md']:
                    ck('chapters',sid+' complete procedure in '+chap,p in (root/chap).read_text())
            ck('mirrors','all5 shared clauses complete',read('evidence/shared_rules.json')==m['selectedSharedRules'])
            for rule in m['selectedSharedRules']:
                for chap in ['PLAYER_CHAPTER.md','DIRECTOR_REVIEW.md']:
                    ck('chapters',rule['id']+' full wording '+chap,rule['wording'] in (root/chap).read_text())
            sels=read('evidence/decision_selections.json')
            for q in m['selectedQuestionDispositions']:
                ck('mirrors','full selected pair '+q['id'],sels[q['id']]==[q['disposition'],q['selectedAnswer']])
            ck('mirrors','actor accounting profiles complete',read('ACTOR_FEATURE_ACCOUNTING.json')['profiles']==read('evidence/actor_profiles.json'))
            ck('mirrors','clock/body matrix complete',read('CLOCK_AND_BODY_MATRIX.json')=={'clocks':m['clockMatrix'],'simulacrumFields':m['simulacrumFieldDisposition']})
            ck('mirrors','all exact holds retained',read('HOLD_REGISTER.json')=={'holds':m['explicitHolds'],'conditionalBranches':m['conditionalBranchRegister']})
            ck('mirrors','source authority exact frozen model envelope',read('SOURCE_AUTHORITY.json')==m['sourceAuthority'])
            for file in ['ACTOR_FEATURE_ACCOUNTING.json','ACTION_AUDIT.json','HOLD_REGISTER.json','CLOCK_AND_BODY_MATRIX.json','DI7_COMPARISON.json','DECISIONS.md','QUESTION_DISPOSITIONS.json','SPELL_DISPOSITIONS.json','SOURCE_AUTHORITY.json','SOURCE_REFERENCES.json','INPUT_BINDINGS.json','CONTEXT_BINDINGS.json','TARGETED_DIAGNOSTIC_EVIDENCE.json']:
                ck('preservation','complete unchanged '+file,(root/file).read_bytes()==b.read(file))
            # Reconcile only current fields in historical comparative evidence.
            num=read('NUMERICAL_STATE_EVIDENCE.json');oldnum=json.loads(b.read('NUMERICAL_STATE_EVIDENCE.json'))
            ck('mirrors','current numerical timeline exact',num['relatedCadence'][1]['completeCorrectedTimeline']==br['timeline'])
            ck('history','original numerical timeline preserved',num['relatedCadence'][1]['completeOriginalTimeline']==oldnum['relatedCadence'][1]['completeOriginalTimeline'])
            af=read('AFFECTED_CASES.json');oa=json.loads(b.read('AFFECTED_CASES.json'))
            current={c['id']:c for c in m['currentVectors']}
            for a,o in zip(af['cases'],oa['cases']):
                ck('history','original complete case before '+a['caseId'],a['before']==o['before'])
                ck('mirrors','current complete case after '+a['caseId'],a['after']==current[a['caseId']])
            mg=read('MIRROR_OPERATIONS_FROM_RETURN02.json')
            ck('replay','25 exact mirror operations',mg['operationCount']==sum(len(g['operations']) for g in mg['files'])==25)
            for g in mg['files']:
                raw_before=b.read(g['file']);raw_after=(root/g['file']).read_bytes()
                ck('replay',g['file']+' before binding',bound(raw_before,g['before']))
                ck('replay',g['file']+' after binding',bound(raw_after,g['after']))
                ck('replay',g['file']+' full forward',enc(replay(json.loads(raw_before),g['operations']))==raw_after)
                ck('replay',g['file']+' full reverse',enc(replay(json.loads(raw_after),g['operations'],True))==raw_before)
            # Actual original source archive and later context copies; no script execution.
            sf='inputs/DD_Rank7_Identity_Casting_5_Source_Conference_01.zip';sr=(root/sf).read_bytes()
            ck('source_binding','complete original source archive unchanged',sr==b.read(sf) and len(sr)==4534073 and sha(sr)=='fad1e1d4b5146782305d94f62194f8856300dde461a2aec4ef1b5b37e61490ec')
            with zipfile.ZipFile(io.BytesIO(sr)) as s:
                zip_valid(s,'source conference')
                for rec in m['sourceBindings']:
                    ck('source_binding','all68 source '+rec['path'],bound(s.read('sources/'+rec['path']),rec))
                for p in (root/'sources').rglob('*'):
                    if p.is_file():
                        rel=p.relative_to(root).as_posix()
                        ck('source_binding','supplied supplemental/current '+rel,p.read_bytes()==h.read(rel))
            for rec in read('CONTEXT_BINDINGS.json'):
                raw=(root/rec['path']).read_bytes()
                ck('source_binding','full later context '+rec['path'],bound(raw,rec) and raw==b.read(rec['path']))
            # History index covers every input file including oversized original maps.
            hb=read('HISTORY_BINDINGS.json')
            ck('history','all25 supplied original members addressed',{r['path'] for r in hb['suppliedMembers']}==set(h.namelist()))
            for r in hb['suppliedMembers']:ck('history','exact input member '+r['path'],bound(h.read(r['path']),r))
            ck('history','all73 Return02 original members addressed',{r['path'] for r in hb['completeReturn02']['members']}==set(b.namelist()))
            for r in hb['completeReturn02']['members']:ck('history','exact retained Return02 '+r['path'],bound(b.read(r['path']),r))
            for p in (root/'history/return02').rglob('*'):
                if p.is_file():
                    rel=p.relative_to(root/'history/return02').as_posix()
                    ck('history','unchanged embedded original '+rel,p.read_bytes()==b.read(rel))
            for p in (root/'history/recovery_input').rglob('*'):
                if p.is_file():
                    rel=p.relative_to(root/'history/recovery_input').as_posix()
                    ck('history','unchanged recovery evidence '+rel,p.read_bytes()==h.read(rel))
            local_report=json.loads(h.read('evidence/RANK7_IDENTITY_CASTING5_PART5_CORRECTION_RETURN_02_SEMANTIC_RECONCILIATION_74.json'))
            ck('history','historical554 report553 pass1 fail preserved',local_report['diagnosticCheckCount']==554 and local_report['diagnosticFailures']==1 and sum(d['passed'] is False for d in local_report['diagnosticChecks'])==1)
            ck('history','reported unavailable original archive not manufactured',hb['missingOriginalReturn03']['available'] is False and hb['missingOriginalReturn03']['recreated'] is False)
            if (root/'ARTIFACT_BINDINGS.json').exists():
                ab=read('ARTIFACT_BINDINGS.json')
                for rec in ab['currentArtifacts']:
                    ck('delivery_binding','current artifact '+rec['path'],bound((root/rec['path']).read_bytes(),rec))
            if (root/'ARTIFACT_OPERATIONS_FROM_RETURN02.json').exists():
                ao=read('ARTIFACT_OPERATIONS_FROM_RETURN02.json')
                for entry in ao['operations']:
                    before=b.read(entry['before']['member']);after=(root/entry['after']['path']).read_bytes()
                    ck('artifact_replacement','full external before '+entry['before']['member'],bound(before,entry['before']))
                    ck('artifact_replacement','full local after '+entry['after']['path'],bound(after,entry['after']))
                    ck('artifact_replacement','replacement genuinely different '+entry['after']['path'],before!=after)
            # New diagnostic is data-checked independently, without executing its file.
            d=read('READY_DEADLINE_DIAGNOSTIC.json');ck('diagnostic','three independent boundary resets',len(d['independentBoundaryCases'])==3)
            expected_before=br['timeline'][2]['before']
            for n,case in enumerate(d['independentBoundaryCases']):
                ck('diagnostic',case['id']+' full identical paid before',case['completeBefore']==expected_before)
                out=case['completeAfter'];r=case['receiptAfter'];release=n==0
                ck('diagnostic',case['id']+' actual old/new predicate',case['obsoleteTimeLessThan62'] is True and case['correctedTimeLessThan61']==release)
                ck('diagnostic',case['id']+' actual targetHP',out['actors']['target']['hp']==(74 if release else 80))
                ck('diagnostic',case['id']+' actual remaining Action/Reaction',out['actors']['mage']['action'] is False and out['actors']['mage']['reaction']==(not release))
                ck('diagnostic',case['id']+' no second transaction/history/class use',all(out['actors']['mage'][k]==expected_before['actors']['mage'][k] for k in ['rp','dissonance','refrain','lastSpell','preparedFamiliesUsed','metaspellUses']))
                ck('diagnostic',case['id']+' counts once',r=={'payloadApplications':int(release),'reactionDebits':int(release),'holdEnds':1,'concentrationEnds':1})
                if release:ck('diagnostic','full positive after/final matches recovered model',out==br['timeline'][2]['after']==br['expectedFinalState'])
                else:
                    ex=copy.deepcopy(expected_before);ex['sourceLedger']['hold']['state']='expired';ex['actors']['mage']['concentration']=None
                    ck('diagnostic',case['id']+' only expiry cleanup state',out==ex)
                for cb in case['repeatCallbacks']:ck('diagnostic',case['id']+' no replay@'+cb['observedAt'],cb['completeAfter']==out and cb['receiptAfter']==r)
            ck('diagnostic','scheduler scope explicit',all(d['schedulerScope'][k] is False for k in ['regularStartDispatched','worldClockOrOtherActorsAdvanced','actualFullStateAt61Or61_1Asserted','actionOrReactionRefreshGranted']))
            for rec in d['checks']:ck('diagnostic_report','reported boundary assertion '+rec['check'],rec['passed'])
            receipt=read('RECOVERY_RECEIPT.json')
            ck('scope','45 supplied accepted-unapplied only; no new acceptance',receipt['acceptedButUnappliedReportedByOwner']==45 and receipt['newAcceptedIdentities']==0)
            ck('scope','applied525/323/249/173 unchanged',receipt['appliedCounts']=={'reviewed':525,'pending':323,'standalone':249,'interfaces':173})
            ck('scope','no originalZIP recovery/application/runtime',receipt['originalReturn03ZipRecovered'] is False and receipt['implementationApplied'] is False and receipt['runtimeTestsExecuted']==0)
            for p in [root/'ready_deadline_diagnostic.py',root/'verify_recovery.py']:
                ast.parse(p.read_text(),filename=p.name);ck('syntax','new recovery script syntax '+p.name,True)
    if with_manifest:
        mf=read('MANIFEST.json')
        files={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
        ck('manifest','all local files bound except root manifest',{e['path'] for e in mf['files']}==files-{'MANIFEST.json'})
        for e in mf['files']:ck('manifest','complete member '+e['path'],bound((root/e['path']).read_bytes(),e))
    counts={}
    for c in checks:counts[c['group']]=counts.get(c['group'],0)+1
    return {'id':'RIC5-READY-DEADLINE-RECOVERY01-VERIFICATION','scope':'New read-only archive/source/replay/mirror and stored diagnostic checks. Not a rerun of historical scripts, semantic acceptance or game runtime.','historyArchive':{'name':INPUT_NAME,'bytes':INPUT_SIZE,'sha256':INPUT_SHA},'model':{'bytes':12000315,'sha256':MODEL_SHA},'manifestIncluded':with_manifest,'checkCount':len(checks),'groups':counts,'failures':0,'checks':checks,'historicalScriptsExecuted':False,'gameModulesImported':False,'runtimeTestsExecuted':0}

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root',type=Path,default=Path(__file__).resolve().parent)
    ap.add_argument('--history-archive',type=Path)
    ap.add_argument('--manifest',action='store_true')
    ap.add_argument('--report',type=Path)
    args=ap.parse_args();root=args.root.resolve()
    history=args.history_archive or root.parent/INPUT_NAME
    if not history.is_file():raise FileNotFoundError(f'Exact retained history archive required: {history}')
    report=verify(root,history,args.manifest)
    if args.report:
        target=args.report.resolve()
        if target==root or root in target.parents:raise ValueError('Report must be a new path outside the recovery package')
        target.parent.mkdir(parents=True,exist_ok=True)
        with target.open('xb') as f:f.write(enc(report))
    print(json.dumps({'checkCount':report['checkCount'],'failures':0,'groups':report['groups'],'runtimeTests':0}))

if __name__=='__main__':main()
