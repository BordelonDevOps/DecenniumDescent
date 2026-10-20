"""Read-only bundle verifier. No project or specification module is imported.

This checks source preservation, exact JSON/text reconstruction, invariants and
recorded evidence. Optional reports require a new path outside the bundle.
--content-only is for package construction before the root manifest is bound.
"""
from __future__ import annotations
from pathlib import Path, PurePosixPath
from copy import deepcopy
from hashlib import sha256
from collections import Counter
import argparse, io, json, stat, zipfile

ROOT=Path(__file__).resolve().parent
checks=[];archive_records=[];seen_archives=set()
def check(name,condition,category='structural'):
    checks.append(dict(name=name,passed=bool(condition),category=category))
    if not condition:raise AssertionError(name)
def load(rel):return json.loads((ROOT/rel).read_text(encoding='utf-8'))
def digest(b):return sha256(b).hexdigest()
def encode(j):return (json.dumps(j,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
def bound(name,b,binding,category='binding'):
    check(name+' complete bytes/hash',len(b)==binding['bytes'] and digest(b)==binding['sha256'],category)
def parent(j,p):
    ts=[x.replace('~1','/').replace('~0','~') for x in p.split('/')[1:]];o=j
    if not ts:raise ValueError('Root replacement not used by this plan')
    for t in ts[:-1]:o=o[int(t)] if isinstance(o,list) else o[t]
    return o,int(ts[-1]) if isinstance(o,list) else ts[-1]
def apply(j,op,reverse=False):
    o,k=parent(j,op['jsonPointer'])
    exists=op['afterExists'] if reverse else op['beforeExists']
    exp=op['after'] if reverse else op['before']
    actual_exists=(k in o if isinstance(o,dict) else 0<=k<len(o))
    if actual_exists!=exists or (exists and o[k]!=exp):raise ValueError('Full before-value/existence mismatch: '+op['jsonPointer'])
    target=op['before'] if reverse else op['after'];target_exists=op['beforeExists'] if reverse else op['afterExists']
    if target_exists:o[k]=deepcopy(target)
    else:del o[k]
    order=op.get('parentKeyOrderBefore' if reverse else 'parentKeyOrderAfter')
    if order is not None:
        if not isinstance(o,dict) or set(o)!=set(order):raise ValueError('Parent key-order mismatch')
        pairs=[(x,o[x]) for x in order];o.clear();o.update(pairs)

def verify_archive(data,label):
    d=digest(data)
    if d in seen_archives:
        archive_records.append(dict(label=label,bytes=len(data),sha256=d,duplicateOfVerifiedArchive=True));return
    seen_archives.add(d)
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        names=z.namelist()
        check(label+' unique names',len(names)==len(set(names)),'archive')
        safe=all(not PurePosixPath(n).is_absolute() and '..' not in PurePosixPath(n).parts and '\\' not in n and ':' not in n and not stat.S_ISLNK(z.getinfo(n).external_attr>>16) for n in names)
        check(label+' safe members',safe,'archive')
        check(label+' CRC',z.testzip() is None,'archive')
        verified=0
        if 'MANIFEST.json' in names:
            m=json.loads(z.read('MANIFEST.json'));entries=m.get('files',m.get('sources',[]))
            if isinstance(entries,list):
                for e in entries:
                    if not isinstance(e,dict) or not {'path','bytes','sha256'}.issubset(e):continue
                    options=[e.get('frozenCopy',''),e['path'],'files/'+e['path'],'sources/'+e['path']]
                    p=next((p for p in options if p in names),None)
                    check(label+' member present '+e['path'],p is not None,'archive')
                    bound(label+'!'+p,z.read(p),e,'archive');verified+=1
        archive_records.append(dict(label=label,bytes=len(data),sha256=d,members=len(names),manifestBindingsVerified=verified,duplicateOfVerifiedArchive=False))
        for n in names:
            if n.endswith('.zip'):verify_archive(z.read(n),label+'!'+n)

def source_member(chain):
    data=(ROOT/chain[0]).read_bytes()
    for member in chain[1:]:
        with zipfile.ZipFile(io.BytesIO(data)) as z:data=z.read(member)
    return data

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--report');ap.add_argument('--content-only',action='store_true');a=ap.parse_args()
    history='history/DD_Part5_Copied_Feat_Integration_Supplement_02.zip'
    hb=(ROOT/history).read_bytes()
    bound('Full unchanged Supplement02',hb,{'bytes':37269540,'sha256':'8ca9f7d6cca9f3353888cd1afb806d705e05e50357c809604cc2f95c54fb83d8'})
    verify_archive(hb,history)
    chainbase=[history,'history/DD_Part5_Copied_Feat_Integration_Review_01.zip']
    return01=source_member(chainbase)
    bound('Full unchanged Return01',return01,{'bytes':36867306,'sha256':'006c3705fa56717b4aa6b4a7fcf08e658e91a1568bbbf2b3cb8a471df42dd064'})
    mapping={'corr':chainbase+['inputs/DD_Part5_Control_Ready_Corrections_01.zip'],
             'control':chainbase+['inputs/DD_Control_15_Full_Conference_Part5_Return_02.zip'],
             'copy':chainbase,'sup':[history]}
    bound('Complete corrections01 preserved',source_member(mapping['corr']),{'bytes':6704401,'sha256':'449e40d625447b206422d1e1df776952c30e7a34b72157d1e4cded0dc04793b0'})
    bound('Complete Control02 preserved',source_member(mapping['control']),{'bytes':20056073,'sha256':'2182baaad08e355da4eef8b0e476eb7b9148804710e72baa92ff3d82194c3123'})
    bs=load('ARTIFACT_BINDINGS.json')['files'];bykey={b['key']:b for b in bs}
    for b in bs:
        original=(ROOT/b['baselineFile']).read_bytes();successor=(ROOT/b['successorFile']).read_bytes()
        bound(b['key']+' baseline',original,b['baseline']);bound(b['key']+' successor',successor,b['successor'])
        prefix,member=b['sourceArchiveMember'].split('/',1)
        check(b['key']+' actual archived baseline equality',source_member(mapping[prefix]+[member])==original,'source')
        if b['kind']=='json':check(b['key']+' lossless canonical serialization',encode(json.loads(original))==original and encode(json.loads(successor))==successor,'serialization')
    plan=load('POINTER_OPERATIONS_FROM_PROPOSALS.json');ops=plan['operations']
    check('30 exact current-proposal JSON operations',len(ops)==plan['operationCount']==30,'replay')
    work={b['key']:load(b['baselineFile']) for b in bs if b['kind']=='json'}
    for i,op in enumerate(ops):
        apply(work[op['artifactKey']],op);check('forward full before-value '+str(i),True,'replay')
    for key,j in work.items():check(key+' complete forward bytes',encode(j)==(ROOT/bykey[key]['successorFile']).read_bytes(),'replay')
    # Applying an already-applied plan must not silently work again.
    try:
        for op in ops:apply(deepcopy(work[op['artifactKey']]),op)
    except (ValueError,KeyError):repeated_rejected=True
    else:repeated_rejected=False
    check('Repeated forward application rejected',repeated_rejected,'mutation-guard')
    for i,op in enumerate(reversed(ops)):
        apply(work[op['artifactKey']],op,True);check('reverse full after-value '+str(i),True,'replay')
    for key,j in work.items():check(key+' complete reverse bytes',encode(j)==(ROOT/bykey[key]['baselineFile']).read_bytes(),'replay')
    bad=deepcopy(ops[0]);bad['before']='not the full bound original value'
    try:apply(deepcopy(work[bad['artifactKey']]),bad)
    except ValueError:wrong_before_rejected=True
    else:wrong_before_rejected=False
    check('Wrong full before-value rejected',wrong_before_rejected,'mutation-guard')
    raw=(ROOT/bs[0]['baselineFile']).read_bytes();check('Drift changes baseline digest',digest(raw+b' ')!=bs[0]['baseline']['sha256'],'mutation-guard')
    alt=load('ALTERNATIVE_RULE_OPERATIONS_FROM_ORIGINAL.json')
    check('Alternative26 operations for four feat files only',len(alt['operations'])==26 and len(alt['files'])==4,'replay')
    x={b['key']:load(b['baselineFile']) for b in alt['files']}
    for b in alt['files']:
        bound(b['key']+' original baseline',(ROOT/b['baselineFile']).read_bytes(),b['baseline'])
        rel=bykey[b['key']]['proposedRepositoryPath'];check(b['key']+' original from original corrections archive',source_member(mapping['corr']+['baseline/'+rel])==(ROOT/b['baselineFile']).read_bytes(),'source')
    oldops=json.loads(source_member(mapping['corr']+['POINTER_OPERATIONS.json']))['operations'];oldops=[o for o in oldops if o['fileKey']!='control15']
    for i,(old,new) in enumerate(zip(oldops,alt['operations'][:13])):
        check('Inherited full feat operation values '+str(i),old['fileKey']==new['artifactKey'] and old['jsonPointer']==new['jsonPointer'] and old['op']==new['op'] and old.get('before')==new.get('before') and old['after']==new['after'],'preservation')
    for op in alt['operations']:apply(x[op['artifactKey']],op)
    for b in alt['files']:check(b['key']+' alternative complete forward bytes',encode(x[b['key']])==(ROOT/b['successorFile']).read_bytes(),'replay')
    for op in reversed(alt['operations']):apply(x[op['artifactKey']],op,True)
    for b in alt['files']:check(b['key']+' alternative complete reverse bytes',encode(x[b['key']])==(ROOT/b['baselineFile']).read_bytes(),'replay')
    txt=load('TEXT_OPERATIONS_FROM_PRIOR_HANDOFF.json')['operations'][0];tb=bykey['handoff']
    check('Handoff exact full before',txt['before'].encode()==(ROOT/tb['baselineFile']).read_bytes(),'replay')
    check('Handoff exact full after',txt['after'].encode()==(ROOT/tb['successorFile']).read_bytes()==(ROOT/'CODEX_HANDOFF.md').read_bytes(),'replay')
    check('Handoff reversible complete bytes',txt['before'].encode()==source_member(chainbase+['CODEX_HANDOFF.md']),'replay')
    policy=load('POLICY_SELECTION.json');newrule=policy['completeOperativeWording']
    oldrule=json.loads(source_member(mapping['corr']+['SCOPED_DECISIONS.json']))['decisions'][5]['completeOperativeWording']
    b0=load(bykey['feat_candidate']['baselineFile']);b1=load(bykey['feat_candidate']['successorFile'])
    s0=load(bykey['feat_shared']['baselineFile']);s1=load(bykey['feat_shared']['successorFile'])
    u0=load(bykey['feat_supplements']['baselineFile']);u1=load(bykey['feat_supplements']['successorFile'])
    a0=load(bykey['feat_acquisition']['baselineFile']);a1=load(bykey['feat_acquisition']['successorFile'])
    mirrors=[s1['rules'][7]['wording'],u1['groups'][6]['value']['copyProfileContract']['lifecycle'],u1['groups'][6]['value']['copyProfileContract']['readyAllowanceDecision']['operativeWording']]
    for i in [291,307,318]:
        f=b1['feats'][i];ac=a1['records'][i]
        check('Feat/acquisition full operative mirrors '+str(i),f['operationalRules']==f['payloadOperational']==ac['completeOperativeProcedure'],'policy')
        mirrors += [f['operationalRules'],f['payloadOperational'],ac['completeOperativeProcedure']]
    for i,s in enumerate(mirrors):check('Complete selected policy mirror '+str(i),s.count(newrule)==1 and oldrule not in s,'policy')
    check('Twelve full policy mirrors',len(mirrors)==12,'policy')
    for i,(f,g) in enumerate(zip(b0['feats'],b1['feats'])):
        changed={k for k in set(f)|set(g) if f.get(k)!=g.get(k)}
        check('Native feat and flags preserved '+str(i),changed==({'operationalRules','payloadOperational'} if i in (291,307,318) else set()),'preservation')
        check('Acquisition record scope '+str(i),{k for k in set(a0['records'][i])|set(a1['records'][i]) if a0['records'][i].get(k)!=a1['records'][i].get(k)}==({'completeOperativeProcedure'} if i in (291,307,318) else set()),'preservation')
    for k in b0:
        if k!='feats':check('Candidate top field unchanged '+k,b0[k]==b1[k],'preservation')
    for k in a0:
        if k!='records':check('Acquisition top field unchanged '+k,a0[k]==a1[k],'preservation')
    for i,r in enumerate(s0['rules']):
        check('Shared rule scope '+str(i), (r==s1['rules'][i]) if i!=7 else {k for k in r if r[k]!=s1['rules'][i][k]}=={'wording'},'preservation')
    for i,g in enumerate(u0['groups']):
        if i!=6:check('Other supplement group unchanged '+str(i),g==u1['groups'][i],'preservation')
    cp0=u0['groups'][6]['value']['copyProfileContract'];cp1=u1['groups'][6]['value']['copyProfileContract']
    check('Seven profiles unchanged',cp0['profiles']==cp1['profiles'] and len(cp1['profiles'])==7,'preservation')
    check('Only three copy-contract fields change',{k for k in cp0 if cp0[k]!=cp1[k]}=={'rankAndPayment','lifecycle','readyAllowanceDecision'},'preservation')
    ctl0=load(bykey['control_context']['baselineFile']);ctl1=load(bykey['control_context']['successorFile'])
    check('Control top-level changed scope',{k for k in set(ctl0)|set(ctl1) if ctl0.get(k)!=ctl1.get(k)}=={'id','status','fullConferenceReviewPart5_02','copyReadyOwnerSupersession20'},'preservation')
    check('Only one full-conference metadata reference changes',{k for k in ctl0['fullConferenceReviewPart5_02'] if ctl0['fullConferenceReviewPart5_02'][k]!=ctl1['fullConferenceReviewPart5_02'][k]}=={'copiedFeatReadyBoundary'},'preservation')
    for i,(s,t) in enumerate(zip(ctl0['spells'],ctl1['spells'])):check('Complete Control spell unchanged '+str(i),s==t,'preservation')
    for name in ('originalExamplesUnchanged','currentExamples'):
        check(name+' count30',len(ctl0[name])==len(ctl1[name])==30,'preservation')
        for i,(s,t) in enumerate(zip(ctl0[name],ctl1[name])):check(name+' complete '+str(i),s==t,'preservation')
    check('Control actual routing unchanged',ctl0['sharedContractRouting11']==ctl1['sharedContractRouting11'],'preservation')
    ic0=load(bykey['implementation_cases']['baselineFile']);ic1=load(bykey['implementation_cases']['successorFile'])
    for i in range(8):check('Other complete integration case unchanged '+str(i),ic0['cases'][i]==ic1['cases'][i],'preservation')
    ex=load('ORIGINAL_AND_REVISED_EXAMPLES.json')
    check('Complete original integration cases retained',ex['completePriorImplementationCases']==ic0,'preservation')
    check('Complete current integration cases match',ex['completeSelectedImplementationCases']==ic1,'preservation')
    check('Twenty historical Ready methods preserved',len(ex['originalReadySpecificationTests'])==20,'preservation')
    check('Four historical expectations superseded',sum(t['currentDisposition']=='SUPERSEDED_EXPECTATION' for t in ex['originalReadySpecificationTests'])==4,'policy')
    cd=json.loads(source_member(chainbase+['CASE_DISPOSITIONS.json']))
    check('Seven full Ready lifecycle histories preserved',ex['completeOriginalReadyLifecycleHistories']==cd['readyLifecycleHistories'] and len(cd['readyLifecycleHistories'])==7,'preservation')
    check('Thirteen full source examples preserved',ex['completeOriginalSourceAcceptanceExamples']==cd['sourceAcceptanceExamples'] and len(cd['sourceAcceptanceExamples'])==13,'preservation')
    check('Sixty-eight full ordinary histories remain in unchanged archive',len(cd['histories'])==68,'preservation')
    for e in ex['cardWorkedCases']:check('Complete card worked cases '+e['id'],e['completeWorkedCases']==b1['feats'][e['index']]['workedCases'],'preservation')
    con0=load(bykey['continuity']['baselineFile']);con1=load(bykey['continuity']['successorFile'])
    check('Five Control decisions unchanged',con0['decisions'][:5]==con1['decisions'][:5],'preservation')
    check('Full old copy decision preserved as historical',con0['decisions'][5]['completePriorDecision']==con1['decisions'][5]['completePriorDecision'],'preservation')
    check('Current continuity marks supersession',con1['decisions'][5]['currentDisposition']=='SUPERSEDED_BY_OWNER_DIRECTED_COPY_READY_ALLOWANCE_02','policy')
    gap=load(bykey['ready_gap']['successorFile'])
    check('Current gap selects exact new policy',gap['selectedOwnerDirectedRule']==policy,'policy')
    check('Old gap active policy selector not retained as current','completeProposedRuleUnchanged' not in gap,'policy')
    for s in load('SOURCE_REFERENCES.json')['sourceCopies']:
        bound('Full source '+s['file'],(ROOT/s['file']).read_bytes(),s,'source')
        origin=s['origin'];prefix,member=origin.split('!',1)
        archive={'corrections01':mapping['corr'],'supplement02':[history]}[prefix]
        check('Exact original source '+s['file'],source_member(archive+[member])==(ROOT/s['file']).read_bytes(),'source')
    spec=load('verification/READY_POLICY_SPECIFICATION.json');cases=load('CASE_DISPOSITIONS.json')
    check('42 complete isolated cases,160 recorded assertions',spec['caseCount']==42 and spec['assertionCount']==160 and not spec['failures'],'recorded-specification')
    check('Complete case disposition/evidence equality',cases['completeCases']==spec['cases'],'recorded-specification')
    check('No project runtime claimed',spec['gameEngineImports']==spec['gameRuntimeTests']==0,'scope')
    for c in spec['cases']:
        check('Case retained complete states '+c['id'],bool(c['selected']['initial']) and bool(c['selected']['trace']) and bool(c['historicalCounterfactual']['trace']),'recorded-specification')
        check('Recorded assertions pass '+c['id'],all(x['passed'] and x['actual']==x['value'] for x in c['assertions']),'recorded-specification')
    limits=load('RETAINED_LIMITATIONS.json')
    check('Five whole positive-case holds preserved',limits['wholePositiveCaseHolds']==['IN6-09-A','IN6-09-B','EN5-01-A','EN5-01-B','EN6-03-B'],'scope')
    check('Applied counts and39 unapplied unchanged',limits['appliedBaseline']==dict(reviewed=525,pending=323,standalone=249,interfaces=173) and limits['acceptedButUnappliedIdentities']==39,'scope')
    check('Latest four proposed code files remain identical',all(source_member([history,'successor/DescentReviewChanges/ReviewBible/tools/'+n])==(ROOT/'sources/latest_proposed_code_unchanged'/n).read_bytes() for n in ('feat335_copy_capture.py','feat335_copy_release.py','feat335_copy_class_release.py','feat335_copy_payloads.py')),'preservation')
    # This verifies already-bound accepted artifact bytes, not new semantic review.
    for archive_name in ('DD_Companion_Life_10_Exact_05_Part5_Return_01.zip','DD_Illusion_Perception_14_Exact_13_Part5_Return_01.zip'):
        data=source_member(chainbase+['inputs/'+archive_name])
        with zipfile.ZipFile(io.BytesIO(data)) as z:
            ns=[n for n in z.namelist() if n.startswith('accepted/current/') and not n.endswith('/')]
            check(archive_name+' eight accepted files preserved within exact archive',len(ns)==8,'preservation')
    content_count=len(checks)
    manifest_checks=0
    if not a.content_only:
        m=load('MANIFEST.json');check('Root manifest fileCount',m['fileCount']==len(m['files']),'return-manifest')
        actual={p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file() and p.name!='MANIFEST.json'}
        check('No unbound return members',actual=={e['path'] for e in m['files']},'return-manifest')
        for e in m['files']:bound('Return member '+e['path'],(ROOT/e['path']).read_bytes(),e,'return-manifest')
        manifest_checks=len(checks)-content_count
    report=dict(id='DD-COPY-READY-PREP-ONLY-INDEPENDENT-VERIFICATION-01',contentChecks=content_count,returnManifestChecks=manifest_checks,failures=0,categories=dict(Counter(x['category'] for x in checks)),uniqueHistoricalArchives=len(seen_archives),archiveRecords=archive_records,checks=checks,
                classification='Read-only structural/source/full-value/preservation verification; recorded isolated tests checked, not reexecuted. No project/specification modules imported.',projectApplied=False,gameRuntimeTestsExecuted=0)
    if a.report:
        p=Path(a.report).resolve()
        if p==ROOT or ROOT in p.parents:raise ValueError('Report must be outside the bound bundle')
        with p.open('x',encoding='utf-8') as f:json.dump(report,f,ensure_ascii=False,indent=2);f.write('\n')
    print(json.dumps(dict(contentChecks=content_count,manifestChecks=manifest_checks,failures=0,uniqueHistoricalArchives=len(seen_archives))))
if __name__=='__main__':main()
