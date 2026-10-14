"""Apply GPT's finite cadence addendum, retaining every previous report/builder."""
from copy import deepcopy
from datetime import datetime, timezone
import importlib.util
import json
from pathlib import Path
import shutil
from validate_feat_exact_01_composite_casting import read, info

G=Path('C:/Github/DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game';V=A/'feat335-cadence-check-01-verdict'
def save(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def replace_bindings(value,mapping):
    if isinstance(value,dict):
        if set(value)=={'path','bytes','sha256'} and value['path'] in mapping:return deepcopy(mapping[value['path']])
        return {k:replace_bindings(v,mapping) for k,v in value.items()}
    if isinstance(value,list):return [replace_bindings(v,mapping) for v in value]
    return value

def main():
    now=datetime.now(timezone.utc).isoformat();changes=[];checks=[]
    def check(label,ok):
        checks.append({'id':label,'pass':bool(ok)})
        if not ok:raise AssertionError(label)
    old_desc=A/'FEAT335_ALLOWANCE_DESCRIPTORS.json';desc=A/'FEAT335_ALLOWANCE_DESCRIPTORS_AFTER_CADENCE.json'
    old_builder=R/'tools/build_feat335_allowance_descriptors.py';builder=R/'tools/build_feat335_allowance_descriptors_after_cadence.py'
    old_assembly=A/'FEAT335_COMPLETE_ACQUISITION_ASSEMBLY.json';assembly=A/'FEAT335_COMPLETE_ACQUISITION_ASSEMBLY_AFTER_CADENCE.json'
    old_register=A/'FEAT335_CURRENT_ACQUISITION_FOLLOWTHROUGH_COMPLETE.json';register=A/'FEAT335_CURRENT_ACQUISITION_FOLLOWTHROUGH_AFTER_CADENCE.json'
    report=A/'FEAT335_CADENCE_FULFILLMENT_CHECK.json';delta=A/'FEAT335_CADENCE_DERIVED_OPERATIONS.json'
    preservation=A/'source-before-feat335-cadence-check-01'
    assert all(not p.exists() for p in [desc,builder,assembly,register,report,delta,preservation])
    for n,b in read(V/'FILE_MANIFEST.json')['payloads'].items():
        actual=info(V/n);check('received:'+n,actual['bytes']==b['bytes'] and actual['sha256']==b['sha256'])
    reproduced=A/'FEAT335_CADENCE_CHECK_01_REPRODUCED.json'
    check('381-local-reproduction',read(reproduced)==read(V/'EXECUTED_CHECKS.json') and read(reproduced)['failed']==0)
    check('only-Windows-newline-byte-difference',reproduced.read_bytes().replace(b'\r\n',b'\n')==(V/'EXECUTED_CHECKS.json').read_bytes())
    ops=read(V/'EXACT_CADENCE_CORRECTIONS.json')['operations'];before_bindings={p:info(p) for p in [old_desc,old_builder,old_assembly,old_register]}
    for op in ops:check('guard:'+op['operationId'],info(G/op['path'])['sha256']==op['expectedSha256'])
    public=R/'data/public/feat_candidates/exact_01/shared_rules.json'
    internal=R/'data/director/feat_candidates/exact_01/shared_rules.json'
    manuscript=R/'docs/feats/exact-candidate-01/SHARED_RULES.md'
    addition=ops[0]['append'];old_wording=ops[0]['old'];amendments={}
    for p in [public,internal]:
        original=read(p);new=deepcopy(original);row=next(x for x in new['rules'] if x['id']=='FS-06')
        check('actual-FS06:'+p.parent.parent.name,row['wording']==old_wording);row['wording']+=addition
        check('all-other-shared-values:'+p.parent.parent.name,[x for x in new['rules'] if x['id']!='FS-06']==[x for x in original['rules'] if x['id']!='FS-06'])
        amendments[p]=json.dumps(new,ensure_ascii=False,indent=2)+'\n'
    old_text=manuscript.read_text(encoding='utf-8');check('exact-manuscript-anchor',old_text.count(old_wording)==1)
    amendments[manuscript]=old_text.replace(old_wording,old_wording+addition,1)
    text=old_builder.read_text(encoding='utf-8');d=read(old_desc);original_d=deepcopy(d)
    for op in ops[1:]:
        if op['kind']=='replace_text':
            check('exact-builder-anchor:'+op['operationId'],text.count(op['old'])==1);text=text.replace(op['old'],op['replacement'],1)
        elif op['kind']=='replace_json_value':
            index=int(op['pointer'].split('/')[2]);row=d['entries'][index]
            check('exact-descriptor-anchor:'+op['recordId'],row['id']==op['recordId'] and row['laterEventCadences']==op['old'])
            row['laterEventCadences']=deepcopy(op['replacement'])
        else:raise AssertionError(op['kind'])
    text=text.replace("out=A/'FEAT335_ALLOWANCE_DESCRIPTORS.json'","out=A/'FEAT335_ALLOWANCE_DESCRIPTORS_AFTER_CADENCE.json'")
    text=text.replace("'entries':entries, 'newRules':0,","'entries':entries, 'newRules':1, 'cadenceAuthority':'FEAT335-CADENCE-CHECK-01',")
    compile(text,str(builder),'exec')
    for p,content in amendments.items():
        copy=preservation/p.relative_to(G);copy.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,copy)
        check('byte-preserved:'+p.relative_to(G).as_posix(),p.read_bytes()==copy.read_bytes())
        before={**info(p),'preservedCopy':copy.relative_to(G).as_posix()};p.write_text(content,encoding='utf-8',newline='\n')
        changes.append({'before':before,'after':info(p)})
    save(preservation/'PRESERVATION_MANIFEST.json',[x['before'] for x in changes])
    save(delta,{'authority':info(V/'EXACT_CADENCE_CORRECTIONS.json'),'recordedAtUtc':now,'changes':changes,
        'historicalBuilderAndReportsUnchanged':True,'newRuleCompletions':1,'sourceInformationDeleted':0,
        'pathAdaptation':'Builder, descriptors, joined assembly and register are new named descendants; their old source-bound versions remain byte-identical. Three actual shared-rule mirrors are amended with preserved before copies.'})
    builder.write_text(text,encoding='utf-8',newline='\n')
    mapping={old_builder.relative_to(G).as_posix():info(builder),public.relative_to(G).as_posix():info(public)}
    d=replace_bindings(d,mapping);d.update(recordedAtUtc=now,previousDescriptor=info(old_desc),cadenceAuthority=info(V/'EXACT_CADENCE_CORRECTIONS.json'),newRules=1)
    save(desc,d)
    # Execute only the declaration extraction already reviewed in GPT's checker.
    spec=importlib.util.spec_from_file_location('cadence_bound_checker',V/'check_cadence_addendum.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    declared=mod.cadence_from_builder(text);selected={x['id']:x['laterEventCadences'] for x in d['entries'] if x['laterEventCadences']}
    check('all38-current-declarations-match',declared==selected and len(selected)==38)
    for old,new in zip(original_d['entries'],d['entries']):
        preserved=deepcopy(new);preserved['laterEventCadences']=old['laterEventCadences']
        check('177-unrelated-entry-values:'+old['id'],preserved==old)
    check('exact12-amended-entries',sum(o!=n for o,n in zip(original_d['entries'],d['entries']))==12)
    for row in read(V/'CADENCE_38_REGISTER.json')['rows']:check('reviewed-disposition:'+row['id'],selected[row['id']]==row['after'])
    mapping[old_desc.relative_to(G).as_posix()]=info(desc)
    a=replace_bindings(read(old_assembly),mapping);a.update(recordedAtUtc=now,previousAssembly=info(old_assembly),cadenceAuthority=info(V/'EXACT_CADENCE_CORRECTIONS.json'))
    a['scope']+=' Current cadence descriptors apply FEAT335-CADENCE-CHECK-01; the original4307-check report remains historical evidence, supplemented by the narrow current fulfillment.'
    save(assembly,a);mapping[old_assembly.relative_to(G).as_posix()]=info(assembly)
    for old,new in zip(read(old_assembly)['entries'],a['entries']):
        for key in ['currentPublic','currentCompleteContract','reviewedAcquisitionDescriptor','mandatorySelectionsAndSnapshots','initialState','conditionalOrDeferred']:
            check('335-source-preserved:'+old['id']+':'+key,old[key]==new[key])
    for p,b in before_bindings.items():check('historical-file-unchanged:'+p.name,info(p)==b)
    check('public-internal-FS06-parity',next(x for x in read(public)['rules'] if x['id']=='FS-06')['wording']==next(x for x in read(internal)['rules'] if x['id']=='FS-06')['wording'])
    check('manuscript-complete-current-FS06',(old_wording+addition) in manuscript.read_text(encoding='utf-8'))
    for b in d['sourceBindings']:check('current-descriptor-binding:'+b['path'],info(G/b['path'])==b)
    save(report,{'recordedAtUtc':now,'status':'pass','checks':len(checks),'failures':[],'results':checks,
        'receivedArchive':info(A/'FEAT335_Cadence_Check_01_Addendum_and_Evidence.zip'),'reproduction':info(reproduced),
        'reproductionChecks':381,'reproductionByteEquality':False,'reproductionSemanticEquality':True,'reproductionDifference':'Only Windows CRLF versus LF',
        'descriptors':info(desc),'builder':info(builder),'assembly':info(assembly),'sourceChanges':info(delta),
        'fulfilled':'15 guarded GPT operations; mirrored FS06 addition; exact38 dispositions including12 corrected keys; all177 unrelated descriptor fields and335 source/acquisition records preserved.',
        'executionLimits':'381 reproduced checks include21 extracted identity-algebra comparisons with conditional supplied turn facts. This application verifies current declarations, exact text/fields and preservation; no scheduler, full feat effects, Ready/cast/rest or temporal restoration engine is certified.',
        'newSharedRuleCompletions':1,'fullFeatExactApproved':False,'humanBalanceApproved':False,'cosmologyReviewed':False})
    current=replace_bindings(read(old_register),mapping)
    current.update(recordedAtUtc=now,previousRegister=info(old_register),cadenceFulfillment=info(report))
    current['allowanceAssemblyEvidence']['cadenceFulfillment']=info(report)
    for row in current['rows']:
        row['completeAcquisitionAssemblyEvidence']['cadenceFulfillment']=info(report)
        if 'ordinaryAllowanceEvidence' in row:row['ordinaryAllowanceEvidence']['cadenceFulfillment']=info(report)
    save(register,current)
    print(json.dumps({'checks':len(checks),'report':info(report),'register':info(register),'sourceChanges':len(changes)}))
if __name__=='__main__':main()
