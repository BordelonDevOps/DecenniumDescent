"""Fresh local application. Requires a separately recorded exact semantic acceptance first."""
from pathlib import Path
import json,copy,hashlib,datetime,shutil
G=Path(r'C:\Github\DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game';D=A/'director-spell-review-129';S=D/'magic7_return03_received'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def enc(v):return (json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
def sha(b):return hashlib.sha256(b).hexdigest()
def bind(p):return {'path':p.relative_to(G).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())}
def fresh(p,b):
 assert not p.exists(),str(p)
 p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
def ptr(v,p):
 for k in p.strip('/').split('/'):
  k=k.replace('~1','/').replace('~0','~');v=v[int(k)] if isinstance(v,list) else v[k]
 return v
ap=D/'MAGIC7_EXACT_ACCEPTANCE_129.json';accept=read(ap)
assert accept['approvedForCanonicalApplication'] is True and accept['semanticFindings']==[]
assert accept['canonicalApplied'] is False and accept['runtimeExecuted'] is False
for b in accept['acceptedFileBindings']:
 p=G/b['path'];assert bind(p)==b
checks=read(D/'MAGIC7_RETURN03_INDEPENDENT_DATA_AUDIT_129.json');assert not checks['errors']
ids=['arcane-clone','arcane-reversal','elemental-rebind','spell-sculptor','spell-seal','spell-theft','resonance-communion']
m=read(S/'MODEL.json');assert [v['id'] for v in m['spells']]==ids==accept['acceptedIdentities']
assert len(m['sharedRules'])==6 and len(m['questionDispositions'])==23
for b in read(S/'MANIFEST.json')['files']:
 p=(S/b['path']).resolve();assert p.is_relative_to(S.resolve());raw=p.read_bytes();assert len(raw)==b['bytes'] and sha(raw)==b['sha256']
ip=R/'data/public/spell_playtests/authored_review_index.json';raw=ip.read_bytes();old=read(ip);idx=copy.deepcopy(old)
assert sha(raw)=='a03b61fe6b2bbebc9b019e5576287603c6b9a84708beb361e9b9c5e5e35cc535' and old['authoredCounts']=={'reviewed':616,'pending':232}
assert all(next(e for e in idx['entries'] if e['id']==sid)['authoredStatus']=='pending-authored-procedure' for sid in ids)
fresh(D/'authored_review_index.before_magic7_129.json',raw)
E=R/'data/public/spell_candidates/magic7_reviewed_129';assert not E.exists();shutil.copytree(S,E)
files=[p for p in S.rglob('*') if p.is_file()]
for p in files:assert p.read_bytes()==(E/p.relative_to(S)).read_bytes()
chapter=R/'docs/spells/candidates/MAGIC7_REVIEWED_129.md'
header='# Magic7 - applied authored review129\n\nThe seven exact procedures are accepted by MAGIC7_EXACT_ACCEPTANCE_129.json and applied by MAGIC7_APPLICATION_129.json under the owner instruction to apply each accepted batch. The complete exact Return03 evidence tree is preserved in data/public/spell_candidates/magic7_reviewed_129; historical draft/pending labels remain historical evidence. The acceptance receipt closes only exact authored review and the application receipt selects those procedures. Retained source-content, runtime, human-play, balance, cosmology and release holds remain open. No rule or case is changed locally.\n\n'
fresh(chapter,header.encode()+(S/'OPERATIVE_TEXT.md').read_bytes())
receipt={'id':'MAGIC7-APPLICATION-129','recordedAtUtc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'APPLIED_AUTHORED_REVIEW_WITH_RETAINED_HOLDS','ownerInstruction':'Keep working on the spells until they are accepted and then apply. Do not stop until all232pending are applied. Use Calibration Review part6.','acceptedIds':ids,'authority':bind(ap),'acceptedModelSource':bind(S/'MODEL.json'),'canonicalModel':bind(E/'MODEL.json'),'exactEvidenceRoot':E.relative_to(G).as_posix(),'evidenceManifest':bind(E/'MANIFEST.json'),'casebook':bind(E/'CASEBOOK.json'),'holds':bind(E/'HOLD_REGISTER.json'),'chapter':bind(chapter),'runtimeSelectionEnabled':False,'runtimeImplemented':False,'historicalPendingLabelsPreserved':True,'localRuleOrCaseChanges':0,'scope':'Exact accepted authored procedure selection and complete evidence preservation; no retained external gate closed.'}
rp=D/'MAGIC7_APPLICATION_129.json';fresh(rp,enc(receipt));ops=[]
for n,e in enumerate(idx['entries']):
 if e['id'] not in ids:continue
 before=copy.deepcopy(e);i=ids.index(e['id']);pointer=f'/spells/{i}';assert ptr(m,pointer)['id']==e['id']
 e.update({'authoredStatus':'reviewed-authored-operational-playtest','procedureFile':'../spell_candidates/magic7_reviewed_129/MODEL.json','sourceCatalogWholeCardPointer':before['wholeCardPointer'],'wholeCardPointer':pointer,'wholeCardIdField':'id','procedurePointer':pointer,'procedureTextPointer':pointer+'/procedure','sharedRulesPointer':'/sharedRules','manuscript':'../../../docs/spells/candidates/'+chapter.name,'reviewId':receipt['id'],'runtimeSelectionEnabled':False,'completeEnvelopeBinding':bind(E/'MODEL.json'),'authoredAcceptanceReceipt':bind(ap),'authoredApplicationReceipt':bind(rp),'historicalCandidateLabelsPreserved':True,'casebookBinding':bind(E/'CASEBOOK.json'),'retainedHoldsBinding':bind(E/'HOLD_REGISTER.json'),'completeEvidenceRoot':E.relative_to(G).as_posix()})
 ops.append({'pointer':f'/entries/{n}','before':before,'after':copy.deepcopy(e)})
idx['authoredCounts']={'reviewed':623,'pending':225};idx['representationCounts']['completeReviewedStandaloneProcedures']=347
idx['additionalStandaloneEnvelopes'].append({'file':'../spell_candidates/magic7_reviewed_129/MODEL.json','binding':bind(E/'MODEL.json'),'reviewId':receipt['id'],'acceptedIds':ids,'authority':bind(ap),'receipt':bind(rp)})
for key in ['authoredCounts','representationCounts','additionalStandaloneEnvelopes']:ops.append({'pointer':'/'+key,'before':old[key],'after':idx[key]})
assert sum(e['authoredStatus']=='reviewed-authored-operational-playtest' for e in idx['entries'])==623
unchanged=0
for before,after in zip(old['entries'],idx['entries']):
 if before['id'] not in ids:assert before==after;unchanged+=1
assert unchanged==841
reverse=copy.deepcopy(idx)
for op in reversed(ops):
 parts=op['pointer'].strip('/').split('/');v=reverse
 for k in parts[:-1]:v=v[int(k)] if isinstance(v,list) else v[k]
 k=int(parts[-1]) if isinstance(v,list) else parts[-1];assert v[k]==op['after'];v[k]=copy.deepcopy(op['before'])
assert reverse==old
for e in idx['entries']:
 if e['id'] in ids:
  v=read((ip.parent/e['procedureFile']).resolve());assert ptr(v,e['wholeCardPointer'])['id']==e['id'];assert isinstance(ptr(v,e['procedureTextPointer']),str);assert len(ptr(v,e['sharedRulesPointer']))==6
out=enc(idx);fresh(D/'MAGIC7_INDEX_OPERATIONS_129.json',enc({'id':'MAGIC7-INDEX-APPLICATION-129','before':{'bytes':len(raw),'sha256':sha(raw),'backup':'authored_review_index.before_magic7_129.json'},'after':{'bytes':len(out),'sha256':sha(out)},'operations':ops,'reverseSemanticExact':True,'reverseByteExactBackup':True}))
assert ip.read_bytes()==raw;ip.write_bytes(out);assert read(ip)==idx
result={'id':'MAGIC7-APPLICATION-VALIDATION-129','passed':True,'acceptedIdentitiesApplied':7,'unrelatedIndexEntriesUnchanged':unchanged,'completeEvidenceFilesPreserved':len(files),'exactEvidencePreserved':True,'forwardReverseIndexOperations':len(ops),'counts':idx['authoredCounts'],'representationCounts':idx['representationCounts'],'index':bind(ip),'applicationReceipt':bind(rp),'acceptanceReceipt':bind(ap),'runtimeSelectionEnabled':False}
fresh(D/'MAGIC7_APPLICATION_VALIDATION_129.json',enc(result));print(json.dumps(result,indent=2))
