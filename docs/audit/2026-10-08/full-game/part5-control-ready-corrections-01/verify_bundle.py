#!/usr/bin/env python3
"""Reproduce correction/preservation checks and isolated specification tests.
No network, repository modification, or game-engine execution.
"""
from __future__ import annotations
from collections import Counter
from pathlib import Path
import argparse
import copy
import hashlib
import importlib
import io
import json
import shutil
import tempfile
import unittest
import zipfile
import apply_corrections as patch

ROOT = Path(__file__).resolve().parent

def load(name):return json.loads((ROOT/name).read_text(encoding='utf-8'))
def raw(name):return (ROOT/name).read_bytes()
def digest(b):return hashlib.sha256(b).hexdigest()

def differences(a,b,p=''):
    if type(a) != type(b): return [p]
    if isinstance(a,dict):
        out=[]
        for k in sorted(set(a)|set(b)):
            q=p+'/'+str(k).replace('~','~0').replace('/','~1')
            out += [q] if k not in a or k not in b else differences(a[k],b[k],q)
        return out
    if isinstance(a,list):
        if len(a)!=len(b): return [p]
        return [q for i,(x,y) in enumerate(zip(a,b)) for q in differences(x,y,p+'/'+str(i))]
    return [] if a==b else [p]

class NamedResult(unittest.TextTestResult):
    def __init__(self,*args,**kwargs):super().__init__(*args,**kwargs);self.passed=[]
    def addSuccess(self,test):super().addSuccess(test);self.passed.append(test.id())

def verify():
    checks=[]
    def check(category,label,condition):
        checks.append({'category':category,'check':label,'passed':bool(condition)})
    binds=load('ARTIFACT_BINDINGS.json')['files'];plan=load('POINTER_OPERATIONS.json');dec=load('SCOPED_DECISIONS.json')
    old={x['key']:load(x['baselineFile']) for x in binds};new={x['key']:load(x['correctedFile']) for x in binds}
    check('inventory','five exact files',len(binds)==5)
    check('inventory','22 operations',len(plan['operations'])==plan['operationCount']==22)
    check('inventory','six scoped decisions only',len(dec['decisions'])==6 and not dec['fullControl15Accepted'] and not dec['fullFeat335Accepted'] and not dec['runtimeImplemented'])
    for row in binds:
        k=row['key'];base=raw(row['baselineFile']);after=raw(row['correctedFile'])
        check('bindings',k+' baseline bytes/hash',len(base)==row['bytes'] and digest(base)==row['sha256'])
        check('bindings',k+' corrected bytes/hash',len(after)==row['correctedBytes'] and digest(after)==row['correctedSha256'])
        expected={x['jsonPointer'] for x in plan['operations'] if x['fileKey']==k}
        check('exact_diff',k+' no undeclared JSON difference',set(differences(old[k],new[k]))==expected)
    forward=patch.prepare();reverse=patch.prepare(reverse=True)
    for row in binds:
        check('replay',row['key']+' full exact forward/reverse bytes',forward[row['repositoryPath']]==raw(row['correctedFile']) and reverse[row['repositoryPath']]==raw(row['baselineFile']))
    c0,c1=old['control15'],new['control15']
    check('preservation','30 complete original scenarios unchanged',len(c0['originalExamplesUnchanged'])==30 and c0['originalExamplesUnchanged']==c1['originalExamplesUnchanged'])
    check('preservation','all complete original shared proposals unchanged',c0['completeOriginalSharedProposals']==c1['completeOriginalSharedProposals'])
    check('preservation','all15 complete source/access and earlier spell records unchanged',all(a['completeSourceAndAccess']==b['completeSourceAndAccess'] and a['completeEarlierRecordUnchanged']==b['completeEarlierRecordUnchanged'] for a,b in zip(c0['spells'],c1['spells'])))
    changed_spell_indexes={1,5,8,10}
    check('preservation','eleven unselected procedures unchanged',all(a['procedure']==b['procedure'] for i,(a,b) in enumerate(zip(c0['spells'],c1['spells'])) if i not in changed_spell_indexes))
    check('preservation','30case IDs and all27 untouched case objects',len(c0['currentExamples'])==30 and [x['id'] for x in c0['currentExamples']]==[x['id'] for x in c1['currentExamples']] and all(a==b for i,(a,b) in enumerate(zip(c0['currentExamples'],c1['currentExamples'])) if i not in {16,17,19}))
    affected=load('AFFECTED_CASES.json')['cases']
    for a in affected:
        check('preservation',a['id']+' complete before/after case records',a['before']==patch.at(c0,a['pointer']) and a['after']==patch.at(c1,a['pointer']))
    for field in [k for k in c0 if k.startswith('previous')]+['pendingTrueSeeingCounterpart','conferenceQuestions10','countsUnchanged','sourceBindings','newRuleAdoptions','runtimeTestsExecuted','memorySourcesSeparated']:
        check('preservation','historical/metadata field unchanged: '+field,c0[field]==c1[field])
    for i in (291,307,318):
        f0,f1=old['feat_candidate']['feats'][i],new['feat_candidate']['feats'][i]
        check('mirrors',f1['id']+' two operative fields remain identical',f1['operationalRules']==f1['payloadOperational'])
        check('preservation',f1['id']+' native object and runtime/acquisition flags unchanged',all(f0[k]==f1[k] for k in f0 if k not in {'operationalRules','payloadOperational'}))
        a0,a1=old['feat_acquisition']['records'][i],new['feat_acquisition']['records'][i]
        check('mirrors',f1['id']+' acquisition operative mirror agrees',a1['completeOperativeProcedure']==f1['operationalRules'])
        check('preservation',f1['id']+' complete acquisition envelope unchanged',all(a0[k]==a1[k] for k in a0 if k!='completeOperativeProcedure'))
    check('preservation','FS09 exact strain rule unchanged',old['feat_shared']['rules'][8]==new['feat_shared']['rules'][8])
    check('preservation','all original feats preserved',old['feat_candidate']['originalFeats']==new['feat_candidate']['originalFeats'])
    for key in ('feat_candidate','feat_acquisition'):
        fields=[k for k in old[key] if k not in ('feats','records')]
        check('preservation',key+' root status/enable/scope metadata unchanged',all(old[key][k]==new[key][k] for k in fields))
    sources=load('SOURCE_REFERENCES.json');records={x['file']:x for x in sources['sources'] if 'file' in x}
    records.update({x['file']:x for x in load('AVAILABLE_CONTROL_SOURCES.json')['files']})
    for name,s in records.items():check('source_bytes',name,len(raw(name))==s['bytes'] and digest(raw(name))==s['sha256'])
    index={x['key']:x['baselineFile'] for x in binds};index.update({x['id']:x['file'] for x in sources['sources'] if 'file' in x})
    for d,links in sources['links'].items():
        for link in links:
            if '#' in link:
                k,p=link.split('#',1);patch.at(load(index[k]),p)
                check('source_pointers',d+' '+link,True)
            else:check('source_pointers',d+' '+link,(ROOT/link).is_file())
    # Negative tests use temporary copies only. No actual repository is opened.
    with tempfile.TemporaryDirectory(prefix='dd-corrections-test-') as tmp:
        t=Path(tmp);repo=t/'source';repo.mkdir()
        for row in binds:
            p=repo/row['repositoryPath'];p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw(row['baselineFile']))
        check('stager','external full snapshot matches',patch.prepare(repo)==forward)
        p=repo/binds[0]['repositoryPath'];p.write_bytes(p.read_bytes()+b' ')
        try:patch.prepare(repo);drift=False
        except patch.CorrectionError:drift=True
        check('stager','baseline drift rejects entire plan',drift)
        staged=t/'staged';patch.stage(forward,staged,None)
        check('stager','staging five full exact outputs',all((staged/row['repositoryPath']).read_bytes()==raw(row['correctedFile']) for row in binds))
        try:patch.stage(forward,staged,None);rejected=False
        except patch.CorrectionError:rejected=True
        check('stager','refuse existing output directory',rejected)
        try:patch.prepare(staged);rejected=False
        except patch.CorrectionError:rejected=True
        check('stager','reject applying forward twice',rejected)
        try:patch.stage(forward,ROOT/'forbidden-output',None);rejected=False
        except patch.CorrectionError:rejected=True
        check('stager','refuse writing within bound bundle',rejected)
    first=copy.deepcopy(plan['operations'][0]);first['before']='WRONG FULL VALUE'
    try:patch.edit(copy.deepcopy(c0),first);rejected=False
    except patch.CorrectionError:rejected=True
    check('stager','full pointer precondition rejects drift',rejected)
    check('membership','no index/registry operations',all('authored_review_index' not in op['repositoryPath'] and 'accepted_interface_registry' not in op['repositoryPath'] for op in plan['operations']))
    stream=io.StringIO();suite=unittest.defaultTestLoader.loadTestsFromName('test_specification_models')
    result=unittest.TextTestRunner(stream=stream,resultclass=NamedResult,verbosity=2).run(suite)
    counts=Counter(x['category'] for x in checks)
    return {'id':'DD-PART5-CONTROL-READY-LOCAL-VERIFICATION-01',
            'structural':{'checks':len(checks),'failures':sum(not x['passed'] for x in checks),'categories':dict(sorted(counts.items())),'results':checks},
            'modelOnly':{'tests':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),'skipped':len(result.skipped),'passedTests':sorted(result.passed),
                         'failureDetails':[{'test':x.id(),'traceback':y} for x,y in result.failures+result.errors],
                         'meaning':'Isolated reference-model tests of authored choices; no existing game runtime or live scheduler executed.'},
            'engineRuntimeTests':0,'fullCohortSemanticsCertified':False,'humanGameplayTests':0,'balanceApproval':False,
            'sourceCoverage':{'exactControl15SourcesAvailable':35,'boundControl15Sources':54,'fullCohortSourceConferenceComplete':False},
            'pass':all(x['passed'] for x in checks) and result.wasSuccessful()}

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--report',type=Path);args=parser.parse_args()
    report=verify()
    if args.report:args.report.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k not in ('structural','modelOnly')},indent=2))
    print(f"Structural: {report['structural']['checks']} checks, {report['structural']['failures']} failures; isolated specification models: {report['modelOnly']['tests']} tests, {report['modelOnly']['failures']} failures, {report['modelOnly']['errors']} errors")
    return 0 if report['pass'] else 1
if __name__=='__main__':raise SystemExit(main())
