"""Preserve GPT's decision and build an isolated reference-only successor."""
from pathlib import Path
from collections import defaultdict
import copy,hashlib,json,stat,zipfile,re

G=Path(r'C:\Github\DecenniumDescent');A=G/'docs/audit/2026-10-08/full-game'
B=A/'feat335-assembly-106/after';ACQ=A/'feat335-acquisition-106/acquisition_assembly.json'
OUT=A/'feat335-planar-reference-108';OUT.mkdir(exist_ok=False)
Z=Path(r'C:\Users\cbord\Downloads\DD_Feat335_Planar_Dependency_107_Reference_Return_01.zip')
checks=[];inputs={};outputs={};operations=[]
def h(b):return hashlib.sha256(b).hexdigest()
def ser(x):return (json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode()
def ck(n,v):
    checks.append({'name':n,'passed':bool(v)});assert v,n
def write(rel,b):
    p=OUT/rel;p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('xb') as f:f.write(b)
def info(p):
    b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':h(b)}
def parent(x,p):
    parts=[v.replace('~1','/').replace('~0','~') for v in p.split('/')[1:]]
    for k in parts[:-1]:x=x[int(k)] if isinstance(x,list) else x[k]
    return x,int(parts[-1]) if isinstance(x,list) else parts[-1]
def get(x,p):
    a,k=parent(x,p);return a[k]
def replace(doc,path,after,rel,reason):
    a,k=parent(doc,path);before=copy.deepcopy(a[k]);a[k]=copy.deepcopy(after)
    operations.append({'kind':'json-replace','file':rel,'path':path,'before':before,'after':after,'reason':reason})
def read(rel,source=None):
    p=source or B/rel;raw=p.read_bytes();inputs[rel]=(p,raw);return json.loads(raw)
def text_replace(rel,before,after):
    p=B/rel;raw=p.read_bytes();inputs[rel]=(p,raw);text=raw.decode('utf8')
    ck(rel+' unique complete span',text.count(before)==1)
    result=text.replace(before,after,1).encode();outputs[rel]=result
    operations.append({'kind':'text-replace','file':rel,'before':before,'after':after,'reason':'Carry agreed current reference through complete derived manuscript.'})

raw=Z.read_bytes();ck('Actual final return exact hash',len(raw)==28008 and h(raw)=='decc37802748a5ab24e2830ccbd19bcb69df9cdc9cb4edf7530351ed522fa20e')
write(Z.name,raw)
with zipfile.ZipFile(Z) as z:
    ck('Only three expected nonexecutable members',set(z.namelist())=={'DECISION.json','MANIFEST.json','REVIEW.md'} and len(z.namelist())==3 and all(not stat.S_ISLNK(x.external_attr>>16) for x in z.infolist()))
    ck('Return CRC',z.testzip() is None);manifest=json.loads(z.read('MANIFEST.json'))
    for r in manifest['files']:ck('Return member '+r['file'],len(z.read(r['file']))==r['bytes'] and h(z.read(r['file']))==r['sha256'])
    for n in z.namelist():write('decision/'+n,z.read(n))
    decision=json.loads(z.read('DECISION.json'))
ck('Confirmed exact narrow proposal',decision['verdict']=='CONFIRM_REFERENCE_ONLY_PROPOSAL_WITH_ONE_CONTAINER_HEADER_CLARIFICATION__FEAT_WRAPPERS_REMAIN_NULL')
with zipfile.ZipFile(A/'DD_Feat335_Spell_Dependencies_107.zip') as z:
    proposal=json.loads(z.read('PLANAR_DEPENDENCY_PROPOSAL.json'))
    ck('Current reading unaltered by reviewer',decision['completeSelectedReadingProcedure']==proposal['proposed']['completeReadingProcedure'])
    ck('Complete dependency unaltered by reviewer',decision['operations'][2]['after']==proposal['proposed']['completeDependency'])
    groups=defaultdict(list)
    for op in decision['operations']:groups[op['target']['member']].append(op)
    for member,ops in groups.items():
        src=Path(ops[0]['target']['originalPath']);rel=src.relative_to(B).as_posix();doc=read(rel)
        ck(member+' actual local derived snapshot exact',inputs[rel][1]==z.read(member))
        for op in ops:
            ck(op['id']+' exact bound before',get(doc,op['target']['pointer'])==op['before'] and h(inputs[rel][1])==op['target']['sha256'])
            replace(doc,op['target']['pointer'],op['after'],rel,op['id']+' agreed reference/editorial replacement')
        out=ser(doc);binding=next(x for x in decision['affectedFileBindings'] if x['source']['member']==member)
        ck(member+' expected complete successor hash',len(out)==binding['virtualAfterBytes'] and h(out)==binding['virtualAfterSha256'])
        outputs[rel]=out

private='data/director/feat_candidates/exact_01/candidate.json';public='data/public/feat_candidates/exact_01/candidate.json';deps='data/public/feat_candidates/exact_01/spell_dependencies.json'
oldproc=decision['operations'][0]['before'];newproc=decision['completeSelectedReadingProcedure']
private_new=json.loads(outputs[private]);public_new=json.loads(outputs[public]);dep_new=json.loads(outputs[deps])
contract=read('acquisition_contracts.json');ck('Existing Planar contract matches former procedure',contract['records'][205]['id']=='planar_binding' and contract['records'][205]['completeOperativeProcedure']==oldproc)
replace(contract,'/records/205/completeOperativeProcedure',newproc,'acquisition_contracts.json','Mirror current reading; no acquisition authorization or initialization change.')
outputs['acquisition_contracts.json']=ser(contract)
acq=read('acquisition_assembly.json',ACQ)
for path in ['/entries/205/currentPublic/operationalRules','/entries/205/currentCompleteContract/completeOperativeProcedure','/entries/205/reviewedAcquisitionDescriptor/completeControllingOperativeProcedure']:
    ck('Exact current acquisition mirror '+path,get(acq,path)==oldproc)
    replace(acq,path,newproc,'acquisition_assembly.json','Current reading only; all historical, conditional, null and payment boundaries retained.')
outputs['acquisition_assembly.json']=ser(acq)

docbase='docs/feats/exact-candidate-01/'
rel=docbase+'MAGIC_CORE.md';text=(B/rel).read_text(encoding='utf8')
start=text.index('## Planar Binding (`planar_binding`)');end=text.find('\n## ',start+4);end=len(text) if end<0 else end
oldsection=text[start:end];ck('Complete Planar chapter procedure unique',oldsection.count(oldproc)==1)
newsection=oldsection.replace(oldproc,newproc,1).replace('### Authored examples','### Preserved historical examples\n\nThese unchanged examples record the original deferred source state. The ordinary AC5 procedure is now accepted authored evidence; this separate feat still grants no activation. Their former undefined-payload language does not override the current ordinary-spell reference.',1)
text_replace(rel,oldsection,newsection)
rel=docbase+'source-audit/MAGIC_CORE.md';text_replace(rel,'### Complete current candidate procedure\n\n'+oldproc,'### Complete current candidate procedure\n\n'+newproc)
rel=docbase+'SPELL_PAYLOADS.md';text=(B/rel).read_text(encoding='utf8');start=text.index('## Planar Binding (`planar-binding`)');end=text.find('\n## ',start+4);end=len(text) if end<0 else end;oldsection=text[start:end]
newsection='## Planar Binding (`planar-binding`)\n\n'+decision['completeSelectedDependencyHeader']+'\n\nThis complete reference contains the current accepted ordinary card and the former deferred dependency as history. The separate feat remains unavailable.\n\n```json\n'+json.dumps(dep_new['spells']['planar-binding'],ensure_ascii=False,indent=2)+'\n```\n'
text_replace(rel,oldsection,newsection)

ck('Private/public current Planar reading agrees',private_new['records'][238]['operationalRules']==public_new['feats'][205]['operationalRules']==newproc)
for name,obj,oldobj in [('private',private_new['records'][238],json.loads(inputs[private][1])['records'][238]),('public',public_new['feats'][205],json.loads(inputs[public][1])['feats'][205])]:
    ck(name+' all fields except reading unchanged',{k:v for k,v in obj.items() if k!='operationalRules'}=={k:v for k,v in oldobj.items() if k!='operationalRules'})
    ck(name+' null and disabled retained',obj['payloadOperational'] is None and all(obj[k] is False for k in ['selectionEnabled','exactApproved','runtimeApproved']))
ck('Acquisition full current object and contract mirror',acq['entries'][205]['currentPublic']==public_new['feats'][205] and acq['entries'][205]['currentCompleteContract']==contract['records'][205])
olddeps=json.loads(inputs[deps][1]);ck('Other283 dependency objects unchanged',len(dep_new['spells'])==284 and all(v==olddeps['spells'][k] for k,v in dep_new['spells'].items() if k!='planar-binding'))
ck('Complete historical dependency retained',dep_new['spells']['planar-binding']['historicalDeferredDependencyRecord']==olddeps['spells']['planar-binding'])
ck('Complete284 current source cards now match at the audited reference boundary',dep_new['spells']['planar-binding']['completeCurrentProcedureCard']==proposal['currentOrdinarySource']['completeCard'])
ck('All335 acquisitions preserved',len(acq['entries'])==335 and all(e==json.loads(inputs['acquisition_assembly.json'][1])['entries'][i] for i,e in enumerate(acq['entries']) if i!=205))
for rel,out in outputs.items():
    ops=[x for x in operations if x['file']==rel]
    if rel.endswith('.json'):
        rev=json.loads(out)
        for op in reversed(ops):
            a,k=parent(rev,op['path']);ck(rel+op['path']+' reverse matches after',a[k]==op['after']);a[k]=op['before']
        reverse=ser(rev)
    else:
        reverse=out.decode('utf8')
        for op in reversed(ops):ck(rel+' reversible exact text',reverse.count(op['after'])==1);reverse=reverse.replace(op['after'],op['before'],1)
        reverse=reverse.encode()
    ck(rel+' reverse exact original bytes',reverse==inputs[rel][1])
    ck(rel+' original still unchanged',inputs[rel][0].read_bytes()==inputs[rel][1])
    write('after/'+rel,out)

source_map=[]
for i,(rel,(src,raw)) in enumerate(inputs.items(),1):
    member=f'before/{i:02d}'+src.suffix;write(member,raw);source_map.append({'replacementPath':rel,'originalPath':str(src),'preservedBefore':member,'beforeBytes':len(raw),'beforeSha256':h(raw),'after':{'path':'after/'+rel,'bytes':len(outputs[rel]),'sha256':h(outputs[rel])}})
write('SOURCE_MAP.json',ser(source_map));write('EXACT_OPERATIONS.json',ser({'id':'PLANAR-REFERENCE-MIRRORS-108','operations':operations,'application':'Derived evidence only. Full replacements OR operations, not both. Require the exact stated106/ACQ106 bases; never apply to unseen later work.'}))
report={'id':'FEAT335-PLANAR-REFERENCE-SUCCESSOR-108','status':'AGREED_REFERENCE_ONLY_DERIVED_SUCCESSOR_COMPLETE_NOT_CANONICAL','decisionArchive':info(OUT/Z.name),'decision':info(OUT/'decision/DECISION.json'),'sourceMap':source_map,'fourAgreedOperations':4,'totalExactMirrorOperations':len(operations),'changedFullFiles':len(outputs),'passed':len(checks),'failed':0,'checks':checks,'currentDependencyCards':284,'unchangedOtherDependencyCards':283,'twoNullWrappersRetained':True,'177AllowanceDescriptorsChanged':False,'canonicalApplied':False,'parent335Accepted':False,'runtimeExecuted':False,'historicalProgramsRerun':False,'ordinarySpellCountsChanged':False,'originalCasebookRewritten':False,'sourceHistoryDeleted':False,'remaining':'Use these eight complete successor files over106 assembly and ACQ106 acquisition when building the final exact parent package. Retain106/107 historical source maps and manifests as history; regenerate final package bindings, not old receipts. FXC04/05/07/08/09 exact mappings and final whole-parent request remain.','scope':'Current references, full private/public/manuscript/acquisition mirrors and exact preservation only. No new spell, feat grant, charge, target, lore/cosmology, runtime or balance permission.'}
write('REPORT.json',ser(report))
manifest=[{'file':p.relative_to(OUT).as_posix(),'bytes':p.stat().st_size,'sha256':h(p.read_bytes())} for p in sorted(OUT.rglob('*')) if p.is_file()]
write('MANIFEST.json',ser({'id':'PLANAR-REFERENCE-108-MANIFEST','files':manifest}))
zp=A/'DD_Feat335_Planar_Reference_Successor_108.zip'
with zipfile.ZipFile(zp,'x',zipfile.ZIP_DEFLATED) as z:
    for p in sorted(OUT.rglob('*')):
        if p.is_file():z.write(p,p.relative_to(OUT).as_posix())
with zipfile.ZipFile(zp) as z:
    assert z.testzip() is None
    for r in manifest:assert h(z.read(r['file']))==r['sha256']
receipt={'id':report['id'],'report':info(OUT/'REPORT.json'),'package':info(zp),'passed':len(checks),'failed':0,'changedFiles':len(outputs),'canonicalApplied':False,'actuallySentToGpt':False}
with (A/'FEAT335_PLANAR_REFERENCE_RECEIPT_108.json').open('xb') as f:f.write(ser(receipt))
with (A/Path(__file__).name).open('xb') as f:f.write(Path(__file__).read_bytes())
print(json.dumps(receipt))
