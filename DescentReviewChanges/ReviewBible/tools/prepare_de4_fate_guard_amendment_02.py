"""Extend the unadopted guard proposal to current Director feat copies, preserving v1."""
from copy import deepcopy
from datetime import datetime,timezone
import json
from apply_di7_ap_as_01 import G,R,A,info,encoded
from prepare_ac5_current_interfaces_01 import at
from prepare_de4_fate_guard_amendment_01 import parent

def read(p):return json.loads(p.read_bytes())

def main():
    previous=A/'DE4_FATE_GUARD_AMENDMENT_DRAFT_01.json';out=A/'DE4_FATE_GUARD_AMENDMENT_DRAFT_02.json';report=A/'DE4_FATE_GUARD_AMENDMENT_CHECK_02.json'
    assert not out.exists() and not report.exists()
    prior=read(previous);doc=deepcopy(prior);before=doc['existingGuardVerbatim'];after=doc['proposedGuardVerbatim'];checks=[]
    def ck(label,ok):checks.append({'name':label,'passed':bool(ok)});assert ok,label
    ck('Original proposal checks pass',read(A/'DE4_FATE_GUARD_AMENDMENT_CHECK_01.json')['failureCount']==0)
    for b in prior['sourceBindings']:ck('Original proposal source unchanged '+b['path'],info(G/b['path'])==b)
    for name,expected in [('magic_extended',1),('general_combat',3)]:
        p=R/f'data/director/feat_candidates/exact_01/cohorts/{name}.json';old=read(p);new=deepcopy(old);ops=[];originals=[]
        def walk(x,path=''):
            if isinstance(x,dict):
                for k,v in x.items():walk(v,path+'/'+k.replace('~','~0').replace('/','~1'))
            elif isinstance(x,list):
                for i,v in enumerate(x):walk(v,path+'/'+str(i))
            elif isinstance(x,str) and before in x:
                if '/completeOriginalCatalogObject/' in path:
                    originals.append({'path':p.relative_to(G).as_posix(),'pointer':path,'retainedOriginal':x});return
                ck('Single current guard '+name+path,x.count(before)==1)
                val=x.replace(before,after,1);parent(new,path)[0][parent(new,path)[1]]=val
                ops.append({'pointer':path,'before':x,'after':val})
                if path.startswith('/currentGoverningExcerpts/'):
                    meta=at(old,path.rsplit('/',1)[0]);current=G/meta['file']
                    ck('Prepared governing excerpt remains literal current text '+name,x in current.read_text(encoding='utf8'))
                    doc.setdefault('governingExcerptRefreshRequirements',[]).append({'cohort':info(p),'pointer':path.rsplit('/',1)[0],'priorMetadata':{k:v for k,v in meta.items() if k!='exactText'},'currentSourceBindingBeforeAmendment':info(current),'requirement':'Retain preparedWholeFileSha256/old sha256 as historical evidence; after actual accepted amendment regenerate the complete current excerpt and bind it to the new complete governing document. Do not label the old prepared whole-file hash current.'})
        walk(old);ck('Expected active locations '+name,len(ops)==expected)
        restored=deepcopy(new)
        for op in reversed(ops):v,k=parent(restored,op['pointer']);ck('Expected proposed value '+name+op['pointer'],v[k]==op['after']);v[k]=op['before']
        ck('Reversible whole cohort '+name,restored==old)
        for row in originals:ck('Original catalog object untouched '+name+row['pointer'],at(new,row['pointer'])==row['retainedOriginal'])
        doc['plannedActiveRepresentationChanges'].append({'source':info(p),'kind':'proposed-json-field-replacements','operations':ops})
        doc['sourceBindings'].append(info(p));doc['immutableHistoricalRecordsRetained'].extend(originals)
    doc.update(id='DE4-FATE-GUARD-AMENDMENT-DRAFT-02',recordedAtUtc=datetime.now(timezone.utc).isoformat(),previousCompleteProposal=info(previous),status='UNSENT and UNADOPTED. Current proposal covers nine active files including Director feat cohorts; originals and all historical prepared bindings remain preserved. No live rule or current file was modified.')
    ck('Nine active files, four immutable original dependency records',len(doc['plannedActiveRepresentationChanges'])==9 and len(doc['immutableHistoricalRecordsRetained'])==4)
    out.write_bytes(encoded(doc));report.write_bytes(encoded({'id':'DE4-FATE-GUARD-AMENDMENT-CHECK-02','draft':info(out),'previousCheck':info(A/'DE4_FATE_GUARD_AMENDMENT_CHECK_01.json'),'checks':checks,'checkCount':len(checks),'failureCount':0,'activeFiles':9,'activeJsonFieldReplacements':sum(len(x.get('operations',[])) for x in doc['plannedActiveRepresentationChanges']),'proseGuardOccurrences':sum(x.get('expectedOccurrences',0) for x in doc['plannedActiveRepresentationChanges']),'immutableHistoricalRecordsPreserved':4,'currentFilesModified':0,'status':'Exact reversible proposal only; no joint review, adoption or runtime execution.'}))
    print(json.dumps({'draft':info(out),'check':info(report),'newChecks':len(checks),'failures':0,'activeFiles':9,'currentFilesModified':0}))

if __name__=='__main__':main()
