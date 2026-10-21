"""New data-only acquisition appendix; does not rerun any historical validator."""
from pathlib import Path
from copy import deepcopy
import json, hashlib, datetime, zipfile
G=Path(r'C:\Github\DecenniumDescent')
A=G/'docs/audit/2026-10-08/full-game'
P=A/'feat335-assembly-106'
O=A/'feat335-acquisition-106'
assert not O.exists()
sources={};checks=[];ops=[]
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):
    p=p.resolve();b=p.read_bytes();sources[str(p)]=b
    return json.loads(b.decode('utf-8-sig'))
def info(p):
    b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':sha(b)}
def check(name,result):
    checks.append({'name':name,'passed':bool(result)});assert result,name
def pointer(o,p):
    for k in p.strip('/').split('/') if p else []:o=o[int(k)] if isinstance(o,list) else o[k.replace('~1','/').replace('~0','~')]
    return o
def replace(o,p,v,artifact):
    parts=p.strip('/').split('/');q=pointer(o,'/'+('/'.join(parts[:-1]))) if len(parts)>1 else o
    k=int(parts[-1]) if isinstance(q,list) else parts[-1];exists=(k<len(q)) if isinstance(q,list) else k in q
    if exists and q[k]==v:return
    ops.append({'artifact':artifact,'pointer':p,'beforeExists':exists,'before':deepcopy(q[k]) if exists else None,'after':deepcopy(v),'afterExists':True})
    q[k]=deepcopy(v)
def operate(o,subset,reverse=False):
    o=deepcopy(o)
    for r in reversed(subset) if reverse else subset:
        parts=r['pointer'].strip('/').split('/');p=pointer(o,'/'+('/'.join(parts[:-1]))) if len(parts)>1 else o;k=int(parts[-1]) if isinstance(p,list) else parts[-1]
        old,new=('after','before') if reverse else ('before','after')
        exists=k<len(p) if isinstance(p,list) else k in p
        assert exists==r[old+'Exists']
        if exists:assert p[k]==r[old]
        if r[new+'Exists']:p[k]=deepcopy(r[new])
        else:del p[k]
    return o

acq_before=load(P/'after/acquisition_assembly.json');acq=deepcopy(acq_before)
allow_before=load(A/'FEAT335_ALLOWANCE_DESCRIPTORS_AFTER_FLORA.json');allow=deepcopy(allow_before)
current=load(P/'after/data/public/feat_candidates/exact_01/candidate.json')
contracts=load(P/'after/acquisition_contracts.json')
supplements=load(P/'after/data/public/feat_candidates/exact_01/supplements.json')
policy=supplements['groups'][6]['value']['copyProfileContract']['readyAllowanceDecision']
check('Current authority is preparation-only Ready',policy['id']=='COPY-READY-ALLOWANCE-02' and policy['newCastAtRelease'] is False)
by_public={x['id']:x for x in current['feats']};by_contract={x['id']:x for x in contracts['records']}
refs={}
def find_refs(v):
    if isinstance(v,dict):
        if all(k in v for k in ['path','bytes','sha256']):refs[(v['path'],v['sha256'])]=deepcopy(v)
        for x in v.values():find_refs(x)
    elif isinstance(v,list):
        for x in v:find_refs(x)
for key in ['finiteGroupEvidence','cadenceAuthority','floraUseAuthority']:find_refs(acq[key])
for entry in acq['entries']:
    for key in ['finiteGroupEvidence','specializedCurrentEvidence','commonPaymentAndInitializationEvidence']:find_refs(entry[key])
evidence=[]
for ref in refs.values():
    path=(G/ref['path']).resolve();check('Evidence inside source tree '+path.name,path.is_relative_to(G))
    obj=load(path);raw=sources[str(path)]
    check('Exact historical evidence bytes '+path.name,len(raw)==ref['bytes'] and sha(raw)==ref['sha256'])
    evidence.append({'binding':ref,'reportedScope':obj.get('scope',obj.get('status')),
        'reportedStatus':obj.get('status'),'reportedCounts':{k:obj[k] for k in ['counts','checks','failed','failures','failureCount','historyCount','acceptanceGroups','finiteWorkGroup','fulfilledGroups'] if k in obj and not isinstance(obj[k],list)},
        'classification':'Preserved historical evidence; program not rerun; no new runtime or broad acceptance inferred.'})

changed_ids=[]
for n,entry in enumerate(allow['entries']):
    ident=entry['id'];row=by_public[ident];old=deepcopy(entry)
    if 'operationalRules' in row:
        replace(allow,f'/entries/{n}/exactAcquisitionDescriptor/completeControllingOperativeProcedure',row['operationalRules'],'allowance_descriptors.json')
        replace(allow,f'/entries/{n}/currentCompleteContract',by_contract[ident],'allowance_descriptors.json')
    if ident in ['arcane_adaptation','eldritch_echo','mimicry']:
        cadences=deepcopy(entry['laterEventCadences'])
        check('One existing copy cadence '+ident,len(cadences)==1 and cadences[0]['family']=='copyRelease')
        cadence=cadences[0]
        cadence['detail']='COPY-READY-ALLOWANCE-02: '+policy['preparationRoundAllowance']+'. Later completion: '+policy['laterRoundRelease']+'. Rest recovery does not reset an independent numbered-round commitment history.'
        cadence['countedEvent']='new paid feat-copy commitment: direct cast or Ready preparation'
        cadence['paidReadyCompletionConsumesNewAllowance']=False
        cadence['controllingRulePointer']='/currentCopyReadyContract'
        cadence['legacyFamilyNameDoesNotDefineSpendTiming']=True
        replace(allow,f'/entries/{n}/laterEventCadences',cadences,'allowance_descriptors.json')
    if entry!=old:changed_ids.append(ident)
replace(allow,'/currentCopyReadyContract',policy,'allowance_descriptors.json')
replace(allow,'/status','Derived current acquisition/allowance descriptor mirror 106; historical evidence retained; no runtime or parent approval.','allowance_descriptors.json')
replace(allow,'/currentProcedureAuthority',info(P/'after/data/public/feat_candidates/exact_01/candidate.json'),'allowance_descriptors.json')
replace(allow,'/previousDescriptor',info(A/'FEAT335_ALLOWANCE_DESCRIPTORS_AFTER_FLORA.json'),'allowance_descriptors.json')

allow_bytes=(json.dumps(allow,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
allow_binding={'file':'allowance_descriptors.json','bytes':len(allow_bytes),'sha256':sha(allow_bytes)}
replace(acq,'/currentAllowanceDescriptorAuthority106',allow_binding,'acquisition_assembly.json')
replace(acq,'/historicalEvidenceQualification106','Original finite-group bindings remain exact historical evidence. The current descriptor file and complete current procedures supersede old embedded use wording only; source histories and original reported checks have not been rerun or promoted.','acquisition_assembly.json')
allow_by={x['id']:i for i,x in enumerate(allow['entries'])}
for n,entry in enumerate(acq['entries']):
    if entry['id'] in allow_by:
        p='/entries/'+str(allow_by[entry['id']])
        check('Existing allowance index preserved '+entry['id'],entry['ordinaryAllowanceDescriptorPointer']==p)
        replace(acq,f'/entries/{n}/currentAllowanceDescriptor106',{'source':allow_binding,'pointer':p},'acquisition_assembly.json')
    if 'operationalRules' in by_public[entry['id']]:
        check('Current acquired procedure '+entry['id'],entry['currentCompleteContract']['completeOperativeProcedure']==by_public[entry['id']]['operationalRules'])
for n,entry in enumerate(allow['entries']):
    original=allow_before['entries'][n]
    for key in ['finiteAllowances','exactMandatorySelectionAndSnapshotDescriptor','exactInitialStateDescriptor','exactConditionalOrDeferredDescriptor','sharedOrSeparateIdentity','initializationScope','fullUseRuntimeExecuted']:
        check('Unchanged acquisition identity/initialization '+entry['id']+' '+key,entry[key]==original[key])
    if entry['id'] not in ['arcane_adaptation','eldritch_echo','mimicry']:
        check('Unrelated cadence unchanged '+entry['id'],entry['laterEventCadences']==original['laterEventCadences'])
for name,before,after in [('allowance_descriptors.json',allow_before,allow),('acquisition_assembly.json',acq_before,acq)]:
    relevant=[x for x in ops if x['artifact']==name]
    check('Full forward reconstruction '+name,operate(before,relevant)==after)
    check('Full inverse reconstruction '+name,operate(after,relevant,True)==before)
check('All335 original complete acquisitions remain preserved',len(acq['entries'])==335)
check('All177 descriptor identities preserved',[x['id'] for x in allow['entries']]==[x['id'] for x in allow_before['entries']])
for path,raw in sources.items():check('Source remains byte-identical '+path,Path(path).read_bytes()==raw)

O.mkdir()
def write(name,b):
    p=O/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b if isinstance(b,bytes) else b.encode())
def save(name,v):write(name,json.dumps(v,ensure_ascii=False,indent=2)+'\n')
write('allowance_descriptors.json',allow_bytes);save('acquisition_assembly.json',acq)
save('EXACT_OPERATIONS.json',{'operations':ops,'canonicalApplied':False})
source_map=[]
for n,(path,raw) in enumerate(sorted(sources.items()),1):
    name='sources/'+f'{n:03d}'+Path(path).suffix;write(name,raw)
    source_map.append({'file':name,'originalPath':path,'bytes':len(raw),'sha256':sha(raw)})
save('SOURCE_MAP.json',source_map)
write('REPRODUCTION_SCRIPT.py',Path(__file__).read_bytes())
report={'id':'FEAT335-ACQUISITION-EVIDENCE-106','recordedAtUtc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'sourceAssembly':info(A/'FEAT335_ASSEMBLY_RECEIPT_106.json'),'historicalEvidenceFiles':evidence,
    'fullAcquisitionEntries':335,'allowanceDescriptorEntries':177,'changedDescriptorIdentities':changed_ids,
    'discovery':'Three legacy copyRelease cadence descriptors still used release wording. The derived successor now explicitly counts direct casts/Ready preparation only, under already-selected COPY-READY-ALLOWANCE-02. Family identity and finite initial entitlements are preserved.',
    'reportedNumericCoverage':{'numericPredicateFeats':209,'printedForms':62,'boundaryCases':1678,'syntheticProjections':416,'otherCredentialDependentFeats':126,'qualification':'Historical bounded numeric report; other finite groups separately cover credentials and histories. These figures are not new executions or complete335-character tests.'},
    'exactFieldOperations':len(ops),'passed':len(checks),'failed':0,'checks':checks,
    'newMechanicsAuthored':False,'historicalValidatorsRerun':False,'downloadedScriptsExecuted':False,
    'runtimeExecuted':False,'all335FullAcquisitionsExecuted':False,'canonicalApplied':False,'parent335Accepted':False,
    'candidateReadyForExactSubmission':False,'remaining':'Finish FXC gate-to-evidence mapping and dependency/mirror review before exact parent submission. Current authored-case coverage is660+28; it does not close every acceptance gate.'}
save('EVIDENCE_REPORT.json',report)
manifest=[]
for p in sorted(O.rglob('*')):
    if p.is_file():manifest.append({'file':p.relative_to(O).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())})
save('MANIFEST.json',{'files':manifest,'count':len(manifest)})
zp=A/'DD_Feat335_Acquisition_Evidence_106.zip';assert not zp.exists()
with zipfile.ZipFile(zp,'x',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for p in sorted(O.rglob('*')):
        if p.is_file():z.write(p,p.relative_to(O).as_posix())
with zipfile.ZipFile(zp) as z:
    assert z.testzip() is None
    for r in manifest:
        b=z.read(r['file']);assert len(b)==r['bytes'] and sha(b)==r['sha256']
receipt={'id':report['id'],'zip':info(zp),'report':info(O/'EVIDENCE_REPORT.json'),'currentAcquisition':info(O/'acquisition_assembly.json'),'currentAllowances':info(O/'allowance_descriptors.json'),'passed':len(checks),'failed':0,'sourceFiles':len(sources),'evidenceFiles':len(evidence),'changedDescriptorIdentities':changed_ids,'parentAccepted':False,'canonicalApplied':False}
(A/'FEAT335_ACQUISITION_EVIDENCE_RECEIPT_106.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(receipt,ensure_ascii=False))
