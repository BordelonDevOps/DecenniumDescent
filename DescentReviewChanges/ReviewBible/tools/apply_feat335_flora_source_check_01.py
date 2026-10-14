"""Guarded current-source propagation of the four actual-GPT Flora decisions."""
from copy import deepcopy
from datetime import datetime,timezone
from pathlib import Path
import json,shutil
from hashlib import sha256
from validate_feat_exact_01_composite_casting import read,info
from apply_feat335_cadence_check_01 import replace_bindings
G=Path('C:/Github/DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game';V=A/'feat335-flora-source-check-01-verdict'
def save(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def at(v,p):
    for k in p.strip('/').split('/'):v=v[int(k)] if isinstance(v,list) else v[k]
    return v
def main():
    now=datetime.now(timezone.utc).isoformat();preserve=A/'source-before-feat335-flora-source-check-01'
    delta=A/'FEAT335_FLORA_DERIVED_OPERATIONS.json';check_path=A/'FEAT335_FLORA_SOURCE_PROPAGATION_CHECK.json'
    old_desc=A/'FEAT335_ALLOWANCE_DESCRIPTORS_AFTER_CADENCE.json';desc=A/'FEAT335_ALLOWANCE_DESCRIPTORS_AFTER_FLORA.json'
    old_assembly=A/'FEAT335_COMPLETE_ACQUISITION_ASSEMBLY_AFTER_CADENCE.json';assembly=A/'FEAT335_COMPLETE_ACQUISITION_ASSEMBLY_AFTER_FLORA.json'
    old_register=A/'FEAT335_CURRENT_ACQUISITION_FOLLOWTHROUGH_AFTER_CADENCE.json';register=A/'FEAT335_CURRENT_ACQUISITION_FOLLOWTHROUGH_AFTER_FLORA.json'
    assert all(not p.exists() for p in [preserve,delta,check_path,desc,assembly,register])
    checks=[]
    def check(label,ok):
        checks.append({'id':label,'pass':bool(ok)})
        if not ok:raise AssertionError(label)
    reproduced=A/'FEAT335_FLORA_SOURCE_CHECK_01_REPRODUCED.json'
    check('101-source-checks-reproduced',read(reproduced)==read(V/'EXECUTED_SOURCE_CHECKS.json') and read(reproduced)['checks']==101 and not read(reproduced)['failed'])
    ops=read(V/'EXACT_FLORA_CORRECTIONS.json')['operations'];originals={};changed={};field_changes={}
    def change(p,pointer,old,new,label):
        originals.setdefault(p,p.read_bytes());data=changed.setdefault(p,read(p));parent,key=pointer.rsplit('/',1);node=at(data,parent)
        check('exact-anchor:'+label,node[key]==old);node[key]=new;field_changes.setdefault(p,[]).append({'pointer':pointer,'old':old,'replacement':new,'authority':label})
    for op in ops:
        p=G/op['path'];check('submitted-hash:'+op['id'],info(p)['sha256']==op['expectedSourceSha256'])
        parts=op['pointer'].split('/');check('identity:'+op['id'],read(p)[parts[1]][int(parts[2])]['id']==op['identityGuard']['id'])
        change(p,op['pointer'],op['old'],op['replacement'],op['id'])
    internal=R/'data/director/feat_candidates/exact_01/candidate.json'
    for sid,op in [('conjure_flora',ops[0]),('trapcasting',ops[1])]:
        index=next(i for i,x in enumerate(read(internal)['records']) if x['id']==sid)
        for field in ['operationalRules','payloadOperational']:change(internal,f'/records/{index}/{field}',op['old'],op['replacement'],op['id']+'/internal/'+field)
    supplement=R/'data/director/feat_candidates/exact_01/supplements.json'
    for op in ops[6:]:
        field=op['pointer'].rsplit('/',1)[-1]
        change(supplement,'/groups/6/completeAuthoringValue/floraBody/'+field,op['old'],op['replacement'],op['id']+'/current-internal-value')
    texts={}
    for filename,subset in [('MAGIC_EXTENDED.md',ops[:2]),('SUPPLEMENTS.md',ops[6:])]:
        p=R/'docs/feats/exact-candidate-01'/filename;originals[p]=p.read_bytes();text=p.read_text(encoding='utf-8')
        for op in subset:
            check('manuscript-anchor:'+filename+'/'+op['id'],text.count(op['old'])==1);text=text.replace(op['old'],op['replacement'],1)
        texts[p]=text
    for p,new in changed.items():
        restored=deepcopy(new)
        for entry in reversed(field_changes[p]):parent,key=entry['pointer'].rsplit('/',1);at(restored,parent)[key]=entry['old']
        check('all-other-values-preserved:'+p.relative_to(G).as_posix(),restored==json.loads(originals[p]))
    saved=[]
    for p,blob in originals.items():
        copy=preserve/p.relative_to(G);copy.parent.mkdir(parents=True,exist_ok=True);copy.write_bytes(blob);check('saved-before:'+p.name,p.read_bytes()==copy.read_bytes())
        saved.append({**info(p),'preservedCopy':copy.relative_to(G).as_posix()})
    save(preserve/'PRESERVATION_MANIFEST.json',saved)
    for p,data in changed.items():save(p,data)
    for p,text in texts.items():p.write_text(text,encoding='utf-8',newline='\n')
    changes=[{'before':x,'after':info(G/x['path'])} for x in saved]
    save(delta,{'recordedAtUtc':now,'authority':info(V/'EXACT_FLORA_CORRECTIONS.json'),'changes':changes,
        'directGuardedOperations':10,'mirrorPropagation':'Only current internal operative fields and completeAuthoringValue plus the two current reading chapters; original/sourceDirection/cohort/applied-operation historical text remains preserved.',
        'allOtherValuesPreserved':True,'sourceInformationDeleted':0,'finiteModelFollowThroughComplete':False,'fullFeatExactApproved':False})
    public_path=R/'data/public/feat_candidates/exact_01/candidate.json';contract_path=A/'FEAT_EXACT_01_ACQUISITION_CONTRACTS.json'
    public={r['id']:r for r in read(public_path)['feats']};contracts={r['id']:r for r in read(contract_path)['records']};inside={r['id']:r for r in read(internal)['records']}
    old_public={r['id']:r for r in json.loads(originals[public_path])['feats']}
    for sid,row in public.items():
        check('335-original-wrapper:'+sid,row.get('sourceObject',row.get('unchangedReviewedRecord'))==old_public[sid].get('sourceObject',old_public[sid].get('unchangedReviewedRecord')))
        if sid not in {'conjure_flora','trapcasting'}:check('333-full-wrapper-unchanged:'+sid,row==old_public[sid])
    for sid in ['conjure_flora','trapcasting']:
        check('current-complete-text-parity:'+sid,public[sid]['operationalRules']==public[sid]['payloadOperational']==inside[sid]['operationalRules']==inside[sid]['payloadOperational']==contracts[sid]['completeOperativeProcedure'])
        check('disabled-flags-retained:'+sid,all(public[sid][k] is False for k in ['selectionEnabled','exactApproved','runtimeApproved']))
    mapping={x['after']['path']:x['after'] for x in changes}
    d=replace_bindings(read(old_desc),mapping)
    for row in d['entries']:row['currentCompleteContract']=deepcopy(contracts[row['id']])
    d.update(recordedAtUtc=now,previousDescriptor=info(old_desc),floraUseAuthority=info(V/'EXACT_FLORA_CORRECTIONS.json'))
    save(desc,d);mapping[old_desc.relative_to(G).as_posix()]=info(desc)
    a=replace_bindings(read(old_assembly),mapping)
    for row in a['entries']:
        row['currentPublic']=deepcopy(public[row['id']]);row['currentCompleteContract']=deepcopy(contracts[row['id']])
    a.update(recordedAtUtc=now,previousAssembly=info(old_assembly),floraUseAuthority=info(V/'EXACT_FLORA_CORRECTIONS.json'))
    save(assembly,a);mapping[old_assembly.relative_to(G).as_posix()]=info(assembly)
    current=replace_bindings(read(old_register),mapping)
    for row in current['rows']:row['currentPublicRecordSha256']=sha256(json.dumps(public[row['id']],sort_keys=True,ensure_ascii=False).encode()).hexdigest()
    current.update(recordedAtUtc=now,previousRegister=info(old_register),floraSourcePropagation=info(delta),floraFiniteModelFollowThroughComplete=False)
    save(register,current)
    for b in d['sourceBindings']:check('new-current-descriptor-binding:'+b['path'],info(G/b['path'])==b)
    save(check_path,{'recordedAtUtc':now,'status':'pass','checks':len(checks),'failures':[],'results':checks,
        'receivedArchive':info(A/'FEAT335_Flora_Source_Check_01_Addendum_and_Evidence.zip'),'reproduction':info(reproduced),'reproducedChecks':101,
        'changes':info(delta),'descriptors':info(desc),'assembly':info(assembly),'register':info(register),
        'scope':'Exact10 guarded source changes, current mirrors/readers, original fields/333 unaffected wrappers/disabled flags preserved and current acquisition assembly descendants rebound. Eighteen authored Flora behavior expectations are NOT executed by this source propagation check.',
        'finiteModelFollowThroughComplete':False,'fullFeatExactApproved':False,'cosmologyReviewed':False})
    print(json.dumps({'checks':len(checks),'sourceFilesChanged':len(changes),'report':info(check_path),'register':info(register)}))
if __name__=='__main__':main()
