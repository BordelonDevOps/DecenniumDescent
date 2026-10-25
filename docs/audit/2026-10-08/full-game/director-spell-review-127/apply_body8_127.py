"""Fresh local data integration of exact independently accepted Body8. No game code."""
from pathlib import Path
import json, hashlib, copy, datetime
G=Path(r'C:\Github\DecenniumDescent')
A=G/'docs/audit/2026-10-08/full-game'
R=G/'DescentReviewChanges/ReviewBible'
D=A/'director-spell-review-127'
S=A/'director-spell-review-126/body8-accepted-126'
def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def data(o): return (json.dumps(o,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
def sha(b): return hashlib.sha256(b).hexdigest()
def bind(p):
 b=p.read_bytes(); return {'path':p.relative_to(G).as_posix(),'bytes':len(b),'sha256':sha(b)}
def write(p,b):
 if p.exists():
  assert p.read_bytes()==b,str(p)
  return
 p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
authority=A/'director-spell-review-126/BODY8_EXACT_ACCEPTANCE_126.json'
acc=read(authority);ids=acc['acceptedIdentities']
assert acc['status']=='AUTHORED_REVIEW_ACCEPTED_WITH_RETAINED_CONTENT_AND_IMPLEMENTATION_HOLDS'
assert sha((S/'MODEL.json').read_bytes())==acc['currentModel']['sha256']
for f in read(S/'CURRENT_MANIFEST_126.json')['files']:
 p=S/f['path'];assert p.stat().st_size==f['bytes'] and sha(p.read_bytes())==f['sha256'],f['path']
model=read(S/'MODEL.json');procs=read(S/'PROCEDURES.json')['spells']
assert [x['id'] for x in procs]==ids
assert [x['selectedOperationalProcedure123'] for x in model['records']]==procs
assert model['selectedCurrentCasebook123']==read(S/'CASEBOOK.json')
assert model['selectedHoldRegister123']==read(S/'HOLD_REGISTER.json')
ip=R/'data/public/spell_playtests/authored_review_index.json';before=ip.read_bytes();idx=read(ip);original=copy.deepcopy(idx)
assert idx['authoredCounts']=={'reviewed':597,'pending':251}
assert all(next(x for x in idx['entries'] if x['id']==s)['authoredStatus']=='pending-authored-procedure' for s in ids)
write(D/'authored_review_index.before_body8_127.json',before)
mp=R/'data/public/spell_candidates/body_defense8_reviewed_127.json'
cp=R/'data/playtest/spell_candidates/body_defense8_cases_127.json'
hp=R/'data/director/spell_review/body_defense8_retained_holds_127.json'
tp=R/'docs/spells/candidates/BODY_DEFENSE8_REVIEWED_127.md'
for dst,src in [(mp,'MODEL.json'),(cp,'CASEBOOK.json'),(hp,'HOLD_REGISTER.json')]:write(dst,(S/src).read_bytes())
header='# Body/Defense8 — applied authored review 127\n\nThe exact accepted authored procedures and cases are applied under the owner instruction “Keep working on the spells until they are accepted and then apply.” The independent acceptance is BODY8_EXACT_ACCEPTANCE_126.json; this application is BODY8_APPLICATION_127.json. The historical director pending labels below and inside the exact MODEL are retained evidence, superseded for these eight identities by those receipts. Only the independent exact-review and canonical-application reservations are discharged. All other source-content, conditional positive-case, implementation, human, balance, cosmology and release holds remain. Runtime selection remains disabled.\n\n'
write(tp,header.encode('utf-8')+(S/'OPERATIVE_TEXT.md').read_bytes())
receipt={'id':'BODY8-APPLICATION-127','recordedAtUtc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'APPLIED_AUTHORED_REVIEW_WITH_RETAINED_HOLDS','ownerInstruction':'Keep working on the spells until they are accepted and then apply.','acceptedIds':ids,'acceptedModelSource':bind(S/'MODEL.json'),'canonicalModel':bind(mp),'authority':bind(authority),'exactEvidenceRoot':S.relative_to(G).as_posix(),'evidenceManifest':bind(S/'CURRENT_MANIFEST_126.json'),'chapter':bind(tp),'casebook':bind(cp),'holds':bind(hp),'runtimeSelectionEnabled':False,'runtimeImplemented':False,'historicalPendingLabelsPreserved':True,'scope':'Apply exact independently accepted authored procedures and cases. Preserve all content and implementation holds; no new mechanics or runtime behavior.','supersession':'BD123-INDEPENDENT-REVIEW closed by acceptance126; canonical-integration reservation discharged by explicit current owner instruction. Other holds retained.'}
rp=D/'BODY8_APPLICATION_127.json'
if rp.exists():receipt['recordedAtUtc']=read(rp)['recordedAtUtc']
write(rp,data(receipt))
ops=[]
for n,entry in enumerate(idx['entries']):
 if entry['id'] not in ids:continue
 old=copy.deepcopy(entry);i=ids.index(entry['id']);record=model['records'][i];proc=record['selectedOperationalProcedure123']
 assert record['spellId']==entry['id'] and proc['id']==entry['id']
 assert proc['classAccess']==record['completeCurrentCatalogSourceAndAccess']['classAccess']
 entry.update({'authoredStatus':'reviewed-authored-operational-playtest','procedureFile':'../spell_candidates/'+mp.name,'sourceCatalogWholeCardPointer':old['wholeCardPointer'],'wholeCardPointer':f'/records/{i}/selectedOperationalProcedure123','wholeCardIdField':'id','procedurePointer':f'/records/{i}/selectedOperationalProcedure123','procedureTextPointer':f'/records/{i}/selectedOperationalProcedure123/fullSelectedProcedure','sharedRulesPointer':'/selectedSharedRules123','manuscript':'../../../docs/spells/candidates/'+tp.name,'reviewId':receipt['id'],'runtimeSelectionEnabled':False,'completeEnvelopeBinding':bind(mp),'authoredAcceptanceReceipt':bind(authority),'authoredApplicationReceipt':bind(rp),'historicalCandidateLabelsPreserved':True,'casebookBinding':bind(cp),'retainedHoldsBinding':bind(hp)})
 ops.append({'pointer':f'/entries/{n}','before':old,'after':copy.deepcopy(entry)})
idx['authoredCounts']={'reviewed':605,'pending':243}
idx['representationCounts']['completeReviewedStandaloneProcedures']=329
idx['additionalStandaloneEnvelopes'].append({'file':'../spell_candidates/'+mp.name,'binding':bind(mp),'reviewId':receipt['id'],'acceptedIds':ids,'authority':bind(authority),'receipt':bind(rp)})
for key in ['authoredCounts','representationCounts','additionalStandaloneEnvelopes']:ops.append({'pointer':'/'+key,'before':original[key],'after':idx[key]})
assert len(ops)==11
for old,new in zip(original['entries'],idx['entries']):
 if old['id'] not in ids:assert old==new
assert sum(x['authoredStatus']=='reviewed-authored-operational-playtest' for x in idx['entries'])==605
assert sum(x['authoredStatus']!='reviewed-authored-operational-playtest' for x in idx['entries'])==243
def apply(obj,operations,reverse=False):
 x=copy.deepcopy(obj)
 for op in reversed(operations) if reverse else operations:
  parts=op['pointer'].strip('/').split('/');parent=x
  for k in parts[:-1]:parent=parent[int(k)] if isinstance(parent,list) else parent[k]
  key=int(parts[-1]) if isinstance(parent,list) else parts[-1]
  assert parent[key]==op['after' if reverse else 'before']
  parent[key]=copy.deepcopy(op['before' if reverse else 'after'])
 return x
assert apply(original,ops)==idx and apply(idx,ops,True)==original
after=data(idx)
write(D/'BODY8_INDEX_OPERATIONS_127.json',data({'id':'BODY8-INDEX-APPLICATION-127','before':{'bytes':len(before),'sha256':sha(before),'backup':'authored_review_index.before_body8_127.json'},'after':{'bytes':len(after),'sha256':sha(after)},'operations':ops,'reverseSemanticExact':True,'reverseByteExactBackup':True}))
assert ip.read_bytes()==before
ip.write_bytes(after)
assert read(ip)==idx and mp.read_bytes()==(S/'MODEL.json').read_bytes() and cp.read_bytes()==(S/'CASEBOOK.json').read_bytes()
validation={'id':'BODY8-APPLICATION-VALIDATION-127','passed':True,'acceptedIdentitiesApplied':8,'acceptedManifestBindings':len(read(S/'CURRENT_MANIFEST_126.json')['files']),'unrelatedIndexEntriesUnchanged':840,'selectedProceduresAndAccessExact':8,'casebookAndHoldsExact':True,'forwardReverseOperations':11,'counts':idx['authoredCounts'],'representationCounts':idx['representationCounts'],'index':bind(ip),'applicationReceipt':bind(rp),'runtimeSelectionEnabled':False}
write(D/'BODY8_APPLICATION_VALIDATION_127.json',data(validation));print(json.dumps(validation,indent=2))
