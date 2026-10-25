"""Fresh exact authored acceptance/application; data only, with reversible index update."""
from pathlib import Path
import json,copy,hashlib,datetime,zipfile,io
G=Path(r'C:\Github\DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game';D=A/'director-spell-review-127';S=D/'time5-corrected-127'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def data(x):return (json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode()
def sha(b):return hashlib.sha256(b).hexdigest()
def bind(p):return {'path':p.relative_to(G).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())}
def write(p,b):assert not p.exists(),str(p);p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
checks=read(D/'TIME5_CORRECTED_DATA_CHECKS_127.json');assert checks['findings']==[] and checks['checks']==16561
assert all(x['exactCurrentCard'] for x in read(D/'TIME5_NATIVE_CARD_COMPARISON_127.json'))
src=read(D/'time5-return01/SOURCE_CHECKS.json');outer=zipfile.ZipFile(A/'DD_Time_Cast5_Director_Conference_124.zip');original=zipfile.ZipFile(io.BytesIO(outer.read('original/DD_Time_Cast_5_Conference_01.zip')))
for b in src['wrapper']:
 v=outer.read(b['path']);assert len(v)==b['bytes'] and sha(v)==b['sha256']
for b in src['original']:
 v=original.read('sources/'+b['path']);assert len(v)==b['bytes'] and sha(v)==b['sha256']
assert original.read('CANDIDATE.json')==(S/'history/ORIGINAL_CANDIDATE.json').read_bytes()
for f in read(S/'CURRENT_MANIFEST_127.json')['files']:
 p=S/f['path'];assert p.stat().st_size==f['bytes'] and sha(p.read_bytes())==f['sha256']
ids=['absolute-zero','chrono-lock','time-skip','quicken-cast','contingency'];m=read(S/'MODEL.json');assert [x['spellId'] for x in m['records']]==ids
assert len(m['selectedQuestionDispositions124'])==22 and len(m['selectedSharedRules124'])==6
arc=D/'DD_Time_Cast5_Accepted_127.zip'
assert not arc.exists()
with zipfile.ZipFile(arc,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p in sorted(S.rglob('*')):
  if p.is_file():z.write(p,p.relative_to(S).as_posix())
with zipfile.ZipFile(arc) as z:assert z.testzip() is None and len(z.namelist())==len(set(z.namelist()))
acceptance={'id':'TIME-CAST5-EXACT-LOCAL-ACCEPTANCE-127','recordedAtUtc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'AUTHORED_REVIEW_ACCEPTED_WITH_RETAINED_CONTENT_AND_IMPLEMENTATION_HOLDS','acceptedIdentities':ids,'directorReturnMessage':'9e84c9a5-81eb-4d67-a277-bc62d9234f16','directorArchive':bind(D/'DD_Time_Cast5_Director124_Return01.zip'),'archive':bind(arc),'currentModel':bind(S/'MODEL.json'),'originalSourceBindingChecks':{'wrapper':len(src['wrapper']),'original':len(src['original']),'completeOriginalCandidateExact':True},'originalDirectorManifestBindings':74,'currentManifest':bind(S/'CURRENT_MANIFEST_127.json'),'independentDataChecks':checks['checks'],'caseCounts':checks['counts'],'exactCurrentNativeCards':16,'localCaseCorrections':bind(S/'LOCAL_CASE_CORRECTIONS_127.json'),'semanticReview':{'absoluteZero':'Native complete CON negation; cold damage/life first; actual control admission and concentrating next original START endpoint. Suppressed Decay opportunities are not banked; corrected real Antimagic point supports same-pose resumption.','chronoLock':'Both native schools/access retained; local no-save union/nonconcentration acknowledged NEW. Original guard not refunded; repeated native rank6 cast correctly pays13RP and2base+1Refrain. Stable recovery waits for first legal START9; actual acquired Corpse Golem owner-attached command/offense phase preserved.','timeSkip':'Self-only source conflict expressly selected; same body/gear with finite registered departure/return and real attached Decay/life events. Corrected book handling occurs on original turn12.3, so first voluntary return event can be immediate acquired Sigil Rewrite. Blocked return remains whole-branch conditional; original poison/qualified-absent-removal obligations retained.','quickenCast':'Two actual acquired Action-time children and independent payment/interruption. Fresh Wizard32-10-5-5=12/D2; nested own counter ends9/D1. Real Haste full Action restriction propagates; no extra third Action or history reset. Actual Fireball clear point17/native20ft and real Evocation Ward/exclusion retained.','contingency':'Bounded separately paid legal LOAD, same predeclared body-relative visible surface for area; immutable finite prearmed set and consume-before-attempt cap. Release is no second cast and native root is created at release with original dealer. Actual0HP Grave Gift LOAD, donor31->16, real paid Cleric0->4/new drop and direct recovery44, broad HP blocker/stabilization deadline3608.21, actual fatal-Wound death branch and inherited False Life prerequisite preserved.'},'holdDisposition':'All19 original hold entries are retained as historical/source/implementation qualifications. Independent exact-review reservation is discharged for these exact current bytes. Canonical-integration reservation is authorized by current owner instruction. Body8 historical pending label is superseded by its independent126 acceptance and127 application; Material8 remains unaccepted. No runtime, human/balance/cosmology or release approval.','canonicalApplied':False,'runtimeExecuted':False,'noSelectedProcedureOrQuestionChanges':True}
ap=D/'TIME5_EXACT_ACCEPTANCE_127.json';write(ap,data(acceptance))
ip=R/'data/public/spell_playtests/authored_review_index.json';raw=ip.read_bytes();idx=read(ip);old=copy.deepcopy(idx);assert idx['authoredCounts']=={'reviewed':605,'pending':243}
write(D/'authored_review_index.before_time5_127.json',raw)
mp=R/'data/public/spell_candidates/time_cast5_reviewed_127.json';cp=R/'data/playtest/spell_candidates/time_cast5_cases_127.json';hp=R/'data/director/spell_review/time_cast5_retained_holds_127.json';tp=R/'docs/spells/candidates/TIME_CAST5_REVIEWED_127.md'
for dst,name in [(mp,'MODEL.json'),(cp,'CASEBOOK.json'),(hp,'HOLD_REGISTER.json')]:write(dst,(S/name).read_bytes())
header='# Time/Cast5 — applied authored review127\n\nThe five exact authored procedures are accepted by TIME5_EXACT_ACCEPTANCE_127.json and applied by TIME5_APPLICATION_127.json under the owner instruction to keep working until accepted, then apply. Historical pending labels are retained evidence. Current cases include the reversible local book-timing and visible-area-point corrections, with no selected spell-rule change. All source-content, conditional positive-case, runtime, human, balance, cosmology and release holds remain. See the application and exact acceptance receipts for authoritative current file bindings.\n\n'
write(tp,header.encode()+(S/'OPERATIVE_TEXT.md').read_bytes()+b'\n\n'+(S/'CURRENT_LOCAL_REVIEW_127.md').read_bytes())
receipt={'id':'TIME5-APPLICATION-127','recordedAtUtc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'APPLIED_AUTHORED_REVIEW_WITH_RETAINED_HOLDS','ownerInstruction':'Keep working on the spells until they are accepted and then apply.','acceptedIds':ids,'acceptedModelSource':bind(S/'MODEL.json'),'canonicalModel':bind(mp),'authority':bind(ap),'exactEvidenceRoot':S.relative_to(G).as_posix(),'evidenceManifest':bind(S/'CURRENT_MANIFEST_127.json'),'chapter':bind(tp),'casebook':bind(cp),'holds':bind(hp),'runtimeSelectionEnabled':False,'runtimeImplemented':False,'historicalPendingLabelsPreserved':True,'scope':'Select exact accepted authored procedures/cases and preserve source access, original evidence and all retained content/runtime holds.','supersession':'Independent exact-review gate closed by acceptance127. Owner canonical-integration reservation discharged by explicit current instruction; all other gates remain.'}
rp=D/'TIME5_APPLICATION_127.json';write(rp,data(receipt));ops=[]
for n,e in enumerate(idx['entries']):
 if e['id'] not in ids:continue
 assert e['authoredStatus']=='pending-authored-procedure';prev=copy.deepcopy(e);i=ids.index(e['id']);record=m['records'][i];proc=record['selectedOperationalProcedure124'];assert proc['id']==e['id']
 e.update({'authoredStatus':'reviewed-authored-operational-playtest','procedureFile':'../spell_candidates/'+mp.name,'sourceCatalogWholeCardPointer':prev['wholeCardPointer'],'wholeCardPointer':f'/records/{i}/selectedOperationalProcedure124','wholeCardIdField':'id','procedurePointer':f'/records/{i}/selectedOperationalProcedure124','procedureTextPointer':f'/records/{i}/selectedOperationalProcedure124/procedure','sharedRulesPointer':'/selectedSharedRules124','manuscript':'../../../docs/spells/candidates/'+tp.name,'reviewId':receipt['id'],'runtimeSelectionEnabled':False,'completeEnvelopeBinding':bind(mp),'authoredAcceptanceReceipt':bind(ap),'authoredApplicationReceipt':bind(rp),'historicalCandidateLabelsPreserved':True,'casebookBinding':bind(cp),'retainedHoldsBinding':bind(hp)})
 ops.append({'pointer':f'/entries/{n}','before':prev,'after':copy.deepcopy(e)})
idx['authoredCounts']={'reviewed':610,'pending':238};idx['representationCounts']['completeReviewedStandaloneProcedures']=334
idx['additionalStandaloneEnvelopes'].append({'file':'../spell_candidates/'+mp.name,'binding':bind(mp),'reviewId':receipt['id'],'acceptedIds':ids,'authority':bind(ap),'receipt':bind(rp)})
for k in ['authoredCounts','representationCounts','additionalStandaloneEnvelopes']:ops.append({'pointer':'/'+k,'before':old[k],'after':idx[k]})
for before,after in zip(old['entries'],idx['entries']):
 if before['id'] not in ids:assert before==after
reverse=copy.deepcopy(idx)
for op in reversed(ops):
 parts=op['pointer'].strip('/').split('/');p=reverse
 for k in parts[:-1]:p=p[int(k)] if isinstance(p,list) else p[k]
 k=int(parts[-1]) if isinstance(p,list) else parts[-1];assert p[k]==op['after'];p[k]=copy.deepcopy(op['before'])
assert reverse==old
assert sum(x['authoredStatus']=='reviewed-authored-operational-playtest' for x in idx['entries'])==610
after=data(idx);write(D/'TIME5_INDEX_OPERATIONS_127.json',data({'id':'TIME5-INDEX-APPLICATION-127','before':{'bytes':len(raw),'sha256':sha(raw),'backup':'authored_review_index.before_time5_127.json'},'after':{'bytes':len(after),'sha256':sha(after)},'operations':ops,'reverseSemanticExact':True,'reverseByteExactBackup':True}))
assert ip.read_bytes()==raw;ip.write_bytes(after);assert read(ip)==idx
validation={'id':'TIME5-APPLICATION-VALIDATION-127','passed':True,'acceptedIdentitiesApplied':5,'unrelatedIndexEntriesUnchanged':843,'exactModelCasebookAndHolds':True,'forwardReverseIndexOperations':8,'counts':idx['authoredCounts'],'representationCounts':idx['representationCounts'],'index':bind(ip),'applicationReceipt':bind(rp),'acceptanceReceipt':bind(ap),'archive':bind(arc),'runtimeSelectionEnabled':False}
write(D/'TIME5_APPLICATION_VALIDATION_127.json',data(validation));print(json.dumps(validation,indent=2))
