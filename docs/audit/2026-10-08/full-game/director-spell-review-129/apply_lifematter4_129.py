"""Fresh reversible authored-index selection; requires separately recorded exact four-ID acceptance."""
from pathlib import Path
import json,hashlib,copy,datetime,shutil
G=Path(r'C:\Github\DecenniumDescent');D=Path(__file__).parent;S=D/'lifematter5_return01_received';R=G/'DescentReviewChanges/ReviewBible';E=R/'data/public/spell_candidates/lifematter4_reviewed_129'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def enc(x):return (json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
def sha(x):return hashlib.sha256(x).hexdigest()
def bind(p):return {'path':p.relative_to(G).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())}
def fresh(p,b):
 assert not p.exists(),str(p)
 p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
def ptr(x,p):
 for k in p.strip('/').split('/'):
  k=k.replace('~1','/').replace('~0','~');x=x[int(k)] if isinstance(x,list) else x[k]
 return x
ap=D/'LIFEMATTER4_EXACT_ACCEPTANCE_129.json';a=read(ap);ids=['awaken','bone-cage','contagion','telekinesis']
assert a['approvedForCanonicalApplication'] and a['acceptedIdentities']==ids and a['semanticFindings']==[] and not a['canonicalApplied'] and not a['runtimeExecuted']
for b in a['acceptedFileBindings']:assert bind(G/b['path'])==b
ip=R/'data/public/spell_playtests/authored_review_index.json';raw=ip.read_bytes();old=read(ip);idx=copy.deepcopy(old)
assert bind(ip)==a['canonicalBaseline'] and old['authoredCounts']=={'reviewed':623,'pending':225}
assert all(next(e for e in idx['entries'] if e['id']==sid)['authoredStatus']=='pending-authored-procedure' for sid in ids)
disBefore=copy.deepcopy(next(e for e in old['entries'] if e['id']=='disintegrate'));assert disBefore['authoredStatus']=='pending-authored-procedure'
fresh(D/'authored_review_index.before_lifematter4_129.json',raw)
assert not E.exists();shutil.copytree(S,E)
files=[p for p in S.rglob('*') if p.is_file()]
for p in files:assert p.read_bytes()==(E/p.relative_to(S)).read_bytes()
model=read(E/'MODEL.json');procs=model['completeProcedures'];shared=model['sharedRules'];assert len(shared)==6
chapter=R/'docs/spells/candidates/LIFEMATTER4_REVIEWED_129.md'
text='# LifeMatter4 - applied authored review129\n\nAwaken, Bone Cage, Contagion and Telekinesis are independently accepted by LIFEMATTER4_EXACT_ACCEPTANCE_129.json and selected by LIFEMATTER4_APPLICATION_129.json. The complete original LifeMatter5 Return01 evidence is preserved byte for byte in data/public/spell_candidates/lifematter4_reviewed_129.\n\nOnly these four identities and shared requirements applicable to them are selected. Disintegrate, its cases and its local dust clauses (including those in LM130-LIFE) remain unaccepted candidate evidence pending focused director correction. This application changes no global damage or temporal rule. Historical five-spell/pending labels in the source files do not broaden this receipt.\n\nAll source qualifications, unavailable original positive-case premises, and runtime, human-play, balance, cosmology and release holds remain.\n\n'
for s in procs:
 if s['id'] in ids:text+='## '+s['name']+'\n\n'+s['procedure']+'\n\n'
text+='## Shared source requirements\n\nThese exact source rules apply within the four-identity scope above; Disintegrate-specific choices remain excluded.\n\n'
for rule in shared:text+='### '+rule['id']+'\n\n'+rule['rule']+'\n\n'
fresh(chapter,text.encode('utf-8'))
receipt={'id':'LIFEMATTER4-APPLICATION-129','recordedAtUtc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'APPLIED_FOUR_AUTHORED_IDENTITIES_WITH_RETAINED_HOLDS','ownerInstruction':'Keep working on the spells until accepted and apply each accepted batch; do not stop until all232pending are applied; use Calibration review part6.','acceptedIds':ids,'excludedPendingId':'disintegrate','authority':bind(ap),'acceptedModelSource':bind(S/'MODEL.json'),'canonicalModel':bind(E/'MODEL.json'),'exactEvidenceRoot':E.relative_to(G).as_posix(),'evidenceManifest':bind(E/'MANIFEST.json'),'casebook':bind(E/'CASEBOOK.json'),'holds':bind(E/'HOLD_REGISTER.json'),'chapter':bind(chapter),'runtimeSelectionEnabled':False,'runtimeImplemented':False,'historicalPendingLabelsPreserved':True,'localRuleOrCaseChanges':0,'scope':a['scope']}
rp=D/'LIFEMATTER4_APPLICATION_129.json';fresh(rp,enc(receipt));ops=[]
for n,e in enumerate(idx['entries']):
 if e['id'] not in ids:continue
 before=copy.deepcopy(e);i=next(i for i,s in enumerate(procs) if s['id']==e['id']);p='/completeProcedures/'+str(i)
 e.update({'authoredStatus':'reviewed-authored-operational-playtest','procedureFile':'../spell_candidates/lifematter4_reviewed_129/MODEL.json','sourceCatalogWholeCardPointer':before['wholeCardPointer'],'wholeCardPointer':p,'wholeCardIdField':'id','procedurePointer':p,'procedureTextPointer':p+'/procedure','sharedRulesPointer':'/sharedRules','manuscript':'../../../docs/spells/candidates/'+chapter.name,'reviewId':receipt['id'],'runtimeSelectionEnabled':False,'completeEnvelopeBinding':bind(E/'MODEL.json'),'authoredAcceptanceReceipt':bind(ap),'authoredApplicationReceipt':bind(rp),'historicalCandidateLabelsPreserved':True,'casebookBinding':bind(E/'CASEBOOK.json'),'retainedHoldsBinding':bind(E/'HOLD_REGISTER.json'),'completeEvidenceRoot':E.relative_to(G).as_posix(),'acceptedSharedRuleScope':'Requirements applicable to this selected identity only. Disintegrate-specific dust clauses remain unaccepted, including LM130-LIFE local rider; see exact acceptance/application scope.'})
 ops.append({'pointer':'/entries/'+str(n),'before':before,'after':copy.deepcopy(e)})
idx['authoredCounts']={'reviewed':627,'pending':221};idx['representationCounts']['completeReviewedStandaloneProcedures']=351
idx['additionalStandaloneEnvelopes'].append({'file':'../spell_candidates/lifematter4_reviewed_129/MODEL.json','binding':bind(E/'MODEL.json'),'reviewId':receipt['id'],'acceptedIds':ids,'excludedPendingId':'disintegrate','authority':bind(ap),'receipt':bind(rp)})
for k in ['authoredCounts','representationCounts','additionalStandaloneEnvelopes']:ops.append({'pointer':'/'+k,'before':old[k],'after':copy.deepcopy(idx[k])})
assert sum(e['authoredStatus']=='reviewed-authored-operational-playtest' for e in idx['entries'])==627
unchanged=sum(before['id'] not in ids and before==after for before,after in zip(old['entries'],idx['entries']));assert unchanged==844
assert next(e for e in idx['entries'] if e['id']=='disintegrate')==disBefore
reverse=copy.deepcopy(idx)
for o in reversed(ops):
 ks=o['pointer'].strip('/').split('/');v=reverse
 for k in ks[:-1]:v=v[int(k)] if isinstance(v,list) else v[k]
 k=int(ks[-1]) if isinstance(v,list) else ks[-1];assert v[k]==o['after'];v[k]=copy.deepcopy(o['before'])
assert reverse==old
for e in idx['entries']:
 if e['id'] in ids:
  v=read((ip.parent/e['procedureFile']).resolve());assert ptr(v,e['wholeCardPointer'])['id']==e['id'];assert ptr(v,e['procedureTextPointer'])==next(s for s in procs if s['id']==e['id'])['procedure'];assert len(ptr(v,e['sharedRulesPointer']))==6
out=enc(idx);fresh(D/'LIFEMATTER4_INDEX_OPERATIONS_129.json',enc({'id':'LIFEMATTER4-INDEX-OPERATIONS-129','before':{'bytes':len(raw),'sha256':sha(raw),'backup':'authored_review_index.before_lifematter4_129.json'},'after':{'bytes':len(out),'sha256':sha(out)},'operations':ops,'reverseSemanticExact':True,'reverseByteExactBackup':True}))
assert ip.read_bytes()==raw;ip.write_bytes(out);assert read(ip)==idx
result={'id':'LIFEMATTER4-APPLICATION-VALIDATION-129','passed':True,'acceptedIdentitiesApplied':4,'unrelatedIndexEntriesUnchanged':unchanged,'disintegrateUnchangedAndPending':True,'completeEvidenceFilesPreserved':len(files),'exactEvidencePreserved':True,'forwardReverseIndexOperations':len(ops),'counts':idx['authoredCounts'],'representationCounts':idx['representationCounts'],'index':bind(ip),'applicationReceipt':bind(rp),'acceptanceReceipt':bind(ap),'runtimeSelectionEnabled':False}
fresh(D/'LIFEMATTER4_APPLICATION_VALIDATION_129.json',enc(result));print(json.dumps(result,indent=2))
