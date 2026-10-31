from __future__ import annotations
import json, pathlib, hashlib, zlib, shutil, copy
from datetime import datetime, timezone
BASE=pathlib.Path(r'docs/audit/2026-10-08/full-game/director-spell-review-129')
REC=BASE/'rank9_mass_undeath2_return214_received'
EX=REC/'extracted'
CAND=pathlib.Path(r'DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9_massundeath2_reviewed_214')
INDEX=pathlib.Path(r'DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json')
CAT=pathlib.Path(r'DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json')
OLD_QUEUE=BASE/'CURRENT_SPELL_QUEUE_213.json'
ACCEPTED=['field-of-endless-dead','plague-of-undeath']
REVIEW='MU214'
def dump(p,obj):
 p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(raw): return hashlib.sha256(raw).hexdigest()
def binding(path):
 p=pathlib.Path(path); b=p.read_bytes(); return {'path':p.as_posix(),'bytes':len(b),'sha256':sha(b),'crc32':f'{zlib.crc32(b)&0xffffffff:08x}'}
def bind_repo(rel):
 p=pathlib.Path(rel); b=p.read_bytes(); return {'path':p.as_posix(),'bytes':len(b),'sha256':sha(b)}
def check(ok,msg):
 if not ok: raise RuntimeError(msg)
# Gate on independently reproduced source, history, and semantic review.
audit=json.loads((REC/'RETURN214_SEMANTIC_INDEPENDENT_AUDIT.json').read_text(encoding='utf-8'))
dec=json.loads((EX/'DIRECTOR_DECISION_214.json').read_text(encoding='utf-8'))
check(audit['status']=='PASS' and all(x['passed'] for x in audit['checks']),'Return214 independent audit did not pass')
check(dec['acceptedIds']==ACCEPTED and dec['applied'] is False and dec['appliedIds']==[] and dec['heldTargetIds']==[],'Director acceptance is not exact and unapplied')
check(all(not p['blockingHoldIds'] for p in json.loads((EX/'PROCEDURES_214.json').read_text(encoding='utf-8'))),'A procedure has whole-spell blockers')
check(dec.get('canonicalChanges') is False and dec.get('githubChanges') is False,'Return214 claims canonical or GitHub changes')
# Bind before state and verify exact current target entries.
raw_before=INDEX.read_bytes(); idx_before=json.loads(raw_before.decode('utf-8')); before_binding=binding(INDEX)
cat_raw=CAT.read_bytes(); cat_before=json.loads(cat_raw.decode('utf-8')); catalog_binding=binding(CAT)
entries_before=copy.deepcopy(idx_before['entries']); byid={e['id']:e for e in idx_before['entries']}
procedures=json.loads((EX/'PROCEDURES_214.json').read_text(encoding='utf-8'))
check(set(p['id'] for p in procedures)==set(ACCEPTED),'Procedure identity set differs')
for sid in ACCEPTED:
 check(byid[sid]['authoredStatus']=='pending-authored-procedure' and byid[sid]['procedurePointer'] is None,'Target is not pending exactly')
 check(byid[sid]['sourceStatus']=='blocked-pending-operational-review','Native source status unexpectedly changed')
# Create a review-only candidate envelope from the exact director procedures.
CAND.mkdir(parents=True,exist_ok=True)
shutil.copyfile(EX/'PROCEDURES_214.json',CAND/'PROCEDURES_214.json')
for fn in ['DIRECTOR_DECISION_214.json','QUESTION_DISPOSITIONS_214.json','BLOCKER_REASSESSMENT_214.json','FUTURE_REQUIREMENT_DISPOSITIONS_214.json','RULE_SOURCE_MAP.json','PROFILES.json']:
 shutil.copyfile(EX/fn,CAND/fn)
hold_register={
 'id':'RANK9-MASSUNDEATH2-HOLD-REGISTER-214',
 'acceptedProcedureScope':'Static authored procedures for the two exact identities only; no runtime selection, canonical promotion, or release.',
 'targetConditionalBoundaries':[
  {'id':'MU214-C01-CONSUMED-REMAINS-RESURRECTION','spellIds':ACCEPTED,'blocking':False,'scope':'Only eligibility of already-consumed animation allocation for independent Resurrection/reconstruction; remains conditional until an exact source resolves eligibility.'},
  {'id':'MU214-C02-CONSTRUCTED-CORPSE','spellIds':ACCEPTED,'blocking':False,'scope':'Only a source-recognized nonliving constructed corpse; no exact category source established, so arbitrary wreckage remains ineligible.'}],
 'preservedInheritedHeldIdentities':dec.get('retainedInheritedHeldIds',[]),
 'qualifications':dec.get('qualifications',[]),
 'blockingWholeSpellIds':[],
 'runtimeSelectionEnabled':False,'canonicalApproval':False,'implementationApproval':False,'humanPlaytest':False,'balanceApproval':False,'cosmologyApproval':False,'domainClosure':False,'releaseApproval':False}
dump(CAND/'HOLD_REGISTER.json',hold_register)
now=datetime.now(timezone.utc).isoformat()
# Assemble the two exact accepted spell procedures with immutable native cards and explicit audit scope.
model={'id':'DD-RANK9-MASSUNDEATH2-DIRECTOR-RETURN214','sourceAuthority':{'reviewedApplied':804,'pending':44,'acceptedUnapplied':0,'completeStandaloneProcedures':528,'scopedInterfaces':173},'spells':[],'qualifications':dec.get('qualifications',[]),'holdRegister':'HOLD_REGISTER.json','originalSourceArchive':bind_repo('docs/audit/2026-10-08/full-game/DD_Rank9_Mass_Undeath_2_Source_Conference_02.zip'),'directorReturnArchive':bind_repo(REC/'DD_Rank9_MassUndeath2_Director_Return214_DELTA.zip')}
for i,p in enumerate(procedures):
 sid=p['id']; old=byid[sid]
 model['spells'].append({'id':sid,'name':old['name'],'accepted':True,'applied':False,'completeNativeAndAccessUnchanged':p['nativeCardUnchanged'],'procedure':{
  'id':sid,'reviewId':REVIEW,'status':'static-authored-director-accepted-unapplied','directorStatus':p['status'],'nativeEnvelopeUnchanged':p['nativeCardUnchanged'],
  'sharedProcedure':p['sharedProcedure'],'spellLocalProcedure':p['spellLocalProcedure'],'profileFile':p['profileFile'],
  'questionDispositionIds':p['sourceQuestionIds'],'sourceQuestionIds':p['sourceQuestionIds'],'sourceLinks':p['sourceLinks'],
  'blockingHoldIds':p['blockingHoldIds'],'conditionalHoldIds':p['conditionalHoldIds'],'caseIds':p['caseIds'],'priorCasePath':p['priorCasePath'],
  'qualifications':p['qualifications'],'sourceStatusNotice':p['sourceStatusNotice']},
  'questionDispositionIds':p['sourceQuestionIds'],'caseIndex':{'caseIds':p['caseIds'],'newCaseFiles':[f'cases/{x}.json' for x in p['caseIds'] if x.startswith(('FE214-','PU214-'))],'preservedCasesExternal':'prior/Return213.zip!cases/<caseId>.json'},'runtimeSelectionEnabled':False})
model['spells'][1]['procedure']['status']='static-authored-director-accepted-unapplied'
dump(CAND/'MODEL.json',model)
# Capture all provenance without repacking the large source or director archives.
ret_dm=binding(REC/'DD_Rank9_MassUndeath2_Director_Return214_DELTA_DELIVERY.json')
ret_archive=binding(REC/'DD_Rank9_MassUndeath2_Director_Return214_DELTA.zip')
orig_dm=binding(REC/'DD_Rank9_MassUndeath2_Director_Return214_DELIVERY.json')
semantic_audit=binding(REC/'RETURN214_SEMANTIC_INDEPENDENT_AUDIT.json')
source_archive=binding('docs/audit/2026-10-08/full-game/DD_Rank9_Mass_Undeath_2_Source_Conference_02.zip')
prior_archive=binding(BASE/'rank9_mass_undeath2_return213_received/DD_Rank9_MassUndeath2_Director_Return213_HELD.zip')
evidence={
 'id':'RANK9-MASSUNDEATH2-RETURN-EVIDENCE-BINDINGS-214','directorReturnDelta':ret_archive,'deliveryManifest':ret_dm,'originalDeliveryManifest':orig_dm,
 'externalPriorReturn213':prior_archive,'sourceConference02':source_archive,'independentAudit':semantic_audit,
 'directorDecision':bind_repo(REC/'extracted/DIRECTOR_DECISION_214.json'),'procedureSource':bind_repo(REC/'extracted/PROCEDURES_214.json'),
 'sourceRuleMap':bind_repo(REC/'extracted/RULE_SOURCE_MAP.json'),'sourceVerification':bind_repo(REC/'extracted/SOURCE_VERIFICATION_214.json'),
 'actorAccessCheck':bind_repo(REC/'extracted/ACTOR_ACCESS_CHECK_214.json'),'semanticNumericalCheck':bind_repo(REC/'extracted/SEMANTIC_NUMERICAL_CHECK_214.json'),
 'dataIntegrityCheck':bind_repo(REC/'extracted/DATA_INTEGRITY_CHECK_214.json'),'semanticFailureCheck':bind_repo(REC/'extracted/INDEPENDENT_SEMANTIC_FAILURE_CHECK_214.json'),
 'caseCount':30,'newCaseCount':13,'preservedCaseCount':17,'events':847,'forwardOperations':1694,'inverseOperations':1694,
 'caseEvidence':'Director delta ZIP plus byte-exact external Return213 archive. Delta omitted only prior/Return213.zip and records its required external SHA256/CRC/byte binding.',
 'sourceBindingCount':13,'allRuleSourcesVerifiedLocalAndInSourceConference':True,'noReviewIndexOrCanonicalChangesInDirectorPacket':True}
dump(CAND/'RETURN_EVIDENCE_BINDINGS.json',evidence)
exact_acceptance={'id':'RANK9-MASSUNDEATH2-EXACT-AUTHORED-ACCEPTANCE-214','recordedAtUtc':now,'status':'TWO_EXACT_STATIC_AUTHORED_PROCEDURES_ACCEPTED_WITH_TWO_RETAINED_CONDITIONAL_BOUNDARIES','acceptedIds':ACCEPTED,'heldIds':[],'blockers':[],
 'directorDecision':bind_repo(REC/'extracted/DIRECTOR_DECISION_214.json'),'directorReturn':ret_archive,'deliveryManifest':ret_dm,'independentAudit':semantic_audit,
 'candidateEnvelope':bind_repo(CAND/'MODEL.json'),'evidenceBindings':bind_repo(CAND/'RETURN_EVIDENCE_BINDINGS.json'),'candidatePackageManifest':'CANDIDATE_PACKAGE_MANIFEST.json',
 'countsBefore':{'reviewed':804,'pending':44,'acceptedUnapplied':0,'completeStandaloneProcedures':528},'countsAfter':{'reviewed':806,'pending':42,'acceptedUnapplied':0,'completeStandaloneProcedures':530},
 'retainedConditionalBoundaries':['MU214-C01-CONSUMED-REMAINS-RESURRECTION','MU214-C02-CONSTRUCTED-CORPSE'],'runtimeSelectionEnabled':False,'canonicalRuntimeApplicationPerformed':False}
dump(CAND/'EXACT_ACCEPTANCE_214.json',exact_acceptance)
# Candidate package manifest binds every candidate file except itself.
files=[]
for p in sorted(CAND.iterdir()):
 if p.is_file() and p.name!='CANDIDATE_PACKAGE_MANIFEST.json':
  b=p.read_bytes(); files.append({'path':p.name,'bytes':len(b),'sha256':sha(b),'crc32':f'{zlib.crc32(b)&0xffffffff:08x}'})
manifest={'id':'RANK9-MASSUNDEATH2-CANDIDATE-PACKAGE-MANIFEST-214','files':files}
dump(CAND/'CANDIDATE_PACKAGE_MANIFEST.json',manifest)
model_binding=bind_repo(CAND/'MODEL.json')
# Prepare and validate exact index operations in memory before writing the index.
idx_after=copy.deepcopy(idx_before); after_entries={e['id']:e for e in idx_after['entries']}; operations=[]
for i,sid in enumerate(ACCEPTED):
 old=copy.deepcopy(after_entries[sid]); model_entry=model['spells'][i]
 after={'id':sid,'name':old['name'],'authoredStatus':'reviewed-authored-operational-playtest','procedureFile':'../spell_candidates/rank9_massundeath2_reviewed_214/MODEL.json','procedurePointer':f'/spells/{i}/procedure','wholeCardPointer':f'/spells/{i}','sourceStatus':old['sourceStatus'],'priorCatalogSelectionStatusUnchanged':True,
  'reviewId':REVIEW,'runtimeSelectionEnabled':False,'completeEnvelopeBinding':model_binding,'retainedHoldRegister':'HOLD_REGISTER.json','sourceCatalogWholeCardPointer':old['wholeCardPointer'],'wholeCardIdField':'id'}
 after_entries[sid].clear(); after_entries[sid].update(after)
 operations.append({'op':'replace-entry','identity':sid,'index':next(j for j,e in enumerate(idx_before['entries']) if e['id']==sid),'before':old,'after':copy.deepcopy(after),'directorProposal':{'id':sid,'applied':False,'beforeEntry':old,'proposedEntry':copy.deepcopy(after)}})
idx_after['authoredCounts']={'reviewed':806,'pending':42}
idx_after['additionalStandaloneEnvelopes'].append({'file':'../spell_candidates/rank9_massundeath2_reviewed_214/MODEL.json','binding':model_binding,'reviewId':REVIEW,'acceptedIds':ACCEPTED,'unacceptedIds':[],
 'excludedPendingIds':[e['id'] for e in idx_after['entries'] if e['authoredStatus']=='pending-authored-procedure'],'authority':{'path':BASE.joinpath('RANK9MASSUNDEATH2_EXACT_ACCEPTANCE_214.json').as_posix(),'bytes':0,'sha256':''},
 'applicationReceipt':'docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9MASSUNDEATH2_APPLICATION_214.json','sourceArchive':source_archive,'deliveryManifest':ret_dm,'scope':'TWO_EXACT_STATIC_AUTHORED_PROCEDURES_ACCEPTED_WITH_RETAINED_CONDITIONAL_BOUNDARIES','runtimeSelectionEnabled':False})
check(idx_after['authoredCounts']=={'reviewed':806,'pending':42},'Index count computation wrong')
check(sum(e['authoredStatus']=='pending-authored-procedure' for e in idx_after['entries'])==42,'Pending index row count wrong')
check(all(after_entries[sid]['sourceStatus']=='blocked-pending-operational-review' for sid in ACCEPTED),'Native source status was changed')
check(all(e==byid[e['id']] for e in idx_after['entries'] if e['id'] not in ACCEPTED),'An unrelated index entry changed')
# Add exact authority binding to the appended envelope after acceptance has its final binding.
acceptance_binding=bind_repo(CAND/'EXACT_ACCEPTANCE_214.json')
idx_after['additionalStandaloneEnvelopes'][-1]['authority']={'path':'docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9MASSUNDEATH2_EXACT_ACCEPTANCE_214.json','bytes':acceptance_binding['bytes'],'sha256':acceptance_binding['sha256']}
# The added envelope's authority is deliberately outside the candidate self-manifest to avoid a hash cycle.
ops_path=BASE/'RANK9MASSUNDEATH2_INDEX_OPERATIONS_214.json'
idx_after_raw=(json.dumps(idx_after,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
# Exact semantic inverse: restore both entries/counts and remove precisely the appended envelope.
restored=copy.deepcopy(idx_after); restored['authoredCounts']=copy.deepcopy(idx_before['authoredCounts']); restored['entries']=copy.deepcopy(entries_before); restored['additionalStandaloneEnvelopes']=copy.deepcopy(idx_before['additionalStandaloneEnvelopes'])
check(restored==idx_before,'Inverse index operations do not restore the exact semantic input')
# Save byte-exact baseline and then apply the verified new index.
before_copy=BASE/'authored_review_index.before_massundeath2_214.json'; before_copy.write_bytes(raw_before)
INDEX.write_bytes(idx_after_raw)
index_after_binding=binding(INDEX)
operations_doc={'id':'RANK9MASSUNDEATH2-INDEX-OPERATIONS-214','before':{'path':before_copy.as_posix(),'bytes':len(raw_before),'sha256':sha(raw_before)},'after':{'path':INDEX.as_posix(),'bytes':index_after_binding['bytes'],'sha256':index_after_binding['sha256']},'afterAuthority':{'reviewed':806,'pending':42,'acceptedUnapplied':0},'operations':operations,'inverseOperations':[{'op':'replace-entry','identity':o['identity'],'after':o['before'],'before':o['after']} for o in operations]+[{'op':'restore-authoredCounts','before':{'reviewed':806,'pending':42},'after':{'reviewed':804,'pending':44}},{'op':'remove-additionalStandaloneEnvelope','index':len(idx_before['additionalStandaloneEnvelopes'])}], 'additionalEnvelopeAppend':{'index':len(idx_before['additionalStandaloneEnvelopes']),'value':idx_after['additionalStandaloneEnvelopes'][-1]},'inverseSemanticExact':True,'onlyIdentityIds':ACCEPTED,'catalogBefore':catalog_binding,'catalogChanged':False}
dump(ops_path,operations_doc)
# Verify persisted application exactly matches in-memory proposal, with no catalog change.
persisted=json.loads(INDEX.read_text(encoding='utf-8')); cat_after=binding(CAT)
check(persisted==idx_after,'Persisted index differs from planned update')
check(cat_after==catalog_binding,'Catalog changed during application')
check(persisted['authoredCounts']=={'reviewed':806,'pending':42} and sum(e['authoredStatus']=='pending-authored-procedure' for e in persisted['entries'])==42,'Persisted authority counts incorrect')
check(all(next(e for e in persisted['entries'] if e['id']==sid)['sourceStatus']=='blocked-pending-operational-review' for sid in ACCEPTED),'Source status changed')
# Refresh pending audit and queue for the next current-authority batch.
queue0=json.loads(OLD_QUEUE.read_text(encoding='utf-8')); groups=[]
for g0 in queue0['currentPendingGroups']:
 g=copy.deepcopy(g0); g['pendingIds']=[x for x in g['pendingIds'] if x not in ACCEPTED]
 if not g['pendingIds']: continue
 g['pendingCount']=len(g['pendingIds']); g['status']='PENDING_FRESH_DIRECTOR_PACKET_FOR_CURRENT_AUTHORITY'; g['freshPacketRequiredForCurrentAuthority']=True; groups.append(g)
all_pending=[sid for g in groups for sid in g['pendingIds']]
check(len(all_pending)==42 and len(set(all_pending))==42,'Refreshed queue not exactly 42 unique pending IDs')
cat_byid={s['id']:i for i,s in enumerate(cat_before['spells']) if 'id' in s}
for sid in all_pending: check(sid in cat_byid and next(e for e in persisted['entries'] if e['id']==sid)['authoredStatus']=='pending-authored-procedure',f'Pending target missing from index/catalog: {sid}')
pending_audit={'id':'CURRENT42-PENDING-IDENTITY-AUDIT-214','recordedAtUtc':now,'authority':{'reviewedApplied':806,'pending':42,'acceptedUnapplied':0},'exactPendingCount':42,'allPendingIds':all_pending,'groups':groups,'allPendingIdsExistInNativeCatalog':True,'noPendingTargetWasSilentlyAccepted':True}
pending_path=BASE/'CURRENT42_PENDING_IDENTITY_AUDIT_214.json'; dump(pending_path,pending_audit)
next_group=groups[0]
next_suggestions=[]
for g in groups:
 next_suggestions.append(g)
next={'group':next_group['group'],'pendingIds':next_group['pendingIds'],'pendingCount':next_group['pendingCount'],'status':'PENDING_FRESH_DIRECTOR_PACKET_FOR_CURRENT_AUTHORITY','freshPacketRequiredForCurrentAuthority':True,'historicalCandidate':next_group.get('candidate'),'historicalArchive':next_group.get('archive')}
queue={'id':'SPELL-REVIEW-QUEUE-214','recordedAtUtc':now,'supersedesQueue':{'path':OLD_QUEUE.as_posix(),'sha256':binding(OLD_QUEUE)['sha256']},'currentAuthority':{'reviewedApplied':806,'pending':42,'acceptedUnapplied':0,'completeStandaloneProcedures':530,'scopedInterfaces':173},
 'currentIndexBinding':index_after_binding,'currentCatalogBinding':catalog_binding,'currentPendingGroups':groups,'nextSuggestedGroups':next_suggestions[:5],'nextGroup':next_group['group'],'next':next,
 'justAppliedBatch':{'reviewId':REVIEW,'group':'rank9-mass-undeath2','acceptedIds':ACCEPTED,'appliedIds':ACCEPTED,'heldIds':[],'blockers':[],'conditionalBoundaryHoldIds':['MU214-C01-CONSUMED-REMAINS-RESURRECTION','MU214-C02-CONSTRUCTED-CORPSE'],'application':'RANK9MASSUNDEATH2_APPLICATION_214.json'},
 'pendingIdentityAudit':{'path':pending_path.as_posix(),'bytes':binding(pending_path)['bytes'],'sha256':binding(pending_path)['sha256']},
 'currentReturnAudit':semantic_audit,'currentReturnDelivery':ret_dm,'currentReturnArchive':ret_archive,'currentReturnDecision':bind_repo(REC/'extracted/DIRECTOR_DECISION_214.json'),'parentQueue':OLD_QUEUE.as_posix(),'pendingCount':42}
queue_path=BASE/'CURRENT_SPELL_QUEUE_214.json'; dump(queue_path,queue)
# Exact acceptance and application receipts.
application={'id':'RANK9MASSUNDEATH2-APPLICATION-214','recordedAtUtc':now,'status':'APPLIED_TWO_EXACT_ACCEPTED_AUTHORED_PROCEDURES_TO_REVIEW_INDEX','acceptedIds':ACCEPTED,'unacceptedIds':[],'directorDecision':bind_repo(REC/'extracted/DIRECTOR_DECISION_214.json'),'directorReturn':ret_archive,'deliveryManifest':ret_dm,'independentAudit':semantic_audit,'candidateEnvelope':bind_repo(CAND/'MODEL.json'),'candidatePackageManifest':bind_repo(CAND/'CANDIDATE_PACKAGE_MANIFEST.json'),'evidenceBindings':bind_repo(CAND/'RETURN_EVIDENCE_BINDINGS.json'),'indexBefore':{'path':before_copy.as_posix(),'bytes':len(raw_before),'sha256':sha(raw_before)},'indexAfter':index_after_binding,'indexOperations':bind_repo(ops_path),'catalogBindingUnchanged':catalog_binding,'countsBefore':{'reviewed':804,'pending':44},'countsAfter':{'reviewed':806,'pending':42},'completeReviewedStandaloneProcedures':{'before':528,'after':530},'sourceStatusPreservedAsBlocked':True,'catalogChanged':False,'runtimeSelectionEnabled':False,'canonicalRuntimeApplicationPerformed':False,'githubChanges':False,'retainedConditionalBoundaries':['MU214-C01-CONSUMED-REMAINS-RESURRECTION','MU214-C02-CONSTRUCTED-CORPSE']}
app_path=BASE/'RANK9MASSUNDEATH2_APPLICATION_214.json'; dump(app_path,application)
validation={'id':'RANK9MASSUNDEATH2-APPLICATION-VALIDATION-214','status':'PASS','checks':[
 {'check':'Return214 exact explicit acceptance independently audited before application','pass':True},
 {'check':'Only field-of-endless-dead and plague-of-undeath changed from pending to reviewed authored procedures','pass':True},
 {'check':'Both native catalog cards, source statuses and all class-access routes remain unchanged','pass':True},
 {'check':'Both row pointers resolve to the candidate envelope and exact spell procedures','pass':True},
 {'check':'Two conditional boundary holds and seven inherited pending identities remain preserved','pass':True},
 {'check':'Review index inverse operation restores exact semantic 804/44 input','pass':True},
 {'check':'Catalog bytes are unchanged; no canonical/runtime selection was enabled','pass':True},
 {'check':'Current catalog still contains all 42 pending identities','pass':True}],
 'countsBefore':{'reviewed':804,'pending':44},'countsAfter':{'reviewed':806,'pending':42},'currentAuthorityAfter':queue['currentAuthority'],'pendingIdentityAudit':pending_audit,'indexAfter':index_after_binding,'catalogAfter':catalog_binding,'applicationReceipt':bind_repo(app_path),'runtimeSelectionEnabled':False,'runtimeExecuted':False,'githubChanges':False}
validation_path=BASE/'RANK9MASSUNDEATH2_APPLICATION_VALIDATION_214.json'; dump(validation_path,validation)
# Current handoff and concise snapshot.
handoff={'id':'CURRENT-HANDOFF-214','recordedAtUtc':now,'status':'RETURN214_EXACT_ACCEPTANCES_APPLIED_806_42_NEXT_BATCH_READY','currentAuthority':queue['currentAuthority'],'currentIndexBinding':index_after_binding,'currentCatalogBinding':catalog_binding,
 'latestBatch':{'group':'rank9-mass-undeath2','ids':ACCEPTED,'acceptedIds':ACCEPTED,'heldIds':[],'blockers':[],'conditionalBoundaryHoldIds':['MU214-C01-CONSUMED-REMAINS-RESURRECTION','MU214-C02-CONSTRUCTED-CORPSE'],'directorDecision':bind_repo(REC/'extracted/DIRECTOR_DECISION_214.json'),'directorReturn':ret_archive,'independentAudit':semantic_audit,'application':bind_repo(app_path),'validation':bind_repo(validation_path)},
 'preservedOtherHolds':dec.get('retainedInheritedHeldIds',[]),'nextStep':{'group':next_group['group'],'pendingIds':next_group['pendingIds'],'pendingCount':len(next_group['pendingIds']),'status':'READY_TO_REQUEST_FRESH_DIRECTOR_PACKET'},'appliedThisStep':True,'githubChanges':False}
handoff_path=BASE/'CURRENT_HANDOFF_214.json'; dump(handoff_path,handoff)
snapshot=f"""# Current Spell Review Snapshot — Return 214\n\nAuthority after the exact accepted batch: **806 applied / 42 pending / 0 accepted-unapplied**.\n\nApplied to the authored review index: `field-of-endless-dead`, `plague-of-undeath`. Their native catalog cards remain blocked for runtime selection; this records static authored procedures only.\n\nThe independent audit passed 22 checks, including exact bindings for 13 rule sources, the complete 30-case/847-event replay and inverse audit, and the source-bound Null/save/damage histories. The two retained conditional boundaries are consumed-remains resurrection eligibility and a source-recognized constructed corpse. Seven unrelated inherited holds remain unchanged.\n\nNext current pending group: **{next_group['group']}** — {', '.join(next_group['pendingIds'])}.\n\nNo canonical or runtime change and no GitHub push was made in this step.\n"""
(BASE/'CURRENT_SPELL_REVIEW_SNAPSHOT_214.md').write_text(snapshot,encoding='utf-8')
# Emit next group director request locally for exact reuse in the browser.
req=f"""Current-authority director continuation after Return214\n\nCodex independently audited and applied only the two explicit Return214 acceptances. Current authority is 806 reviewed/applied / 42 pending / 0 accepted-unapplied; current index SHA-256 is {index_after_binding['sha256']}; catalog SHA-256 remains {catalog_binding['sha256']}.\n\nPlease review only current pending group {next_group['group']}, exact pending identities: {', '.join(next_group['pendingIds'])}. These are the current pending subset of the historical source-conference group; do not include identities already reviewed or otherwise not in this exact list. Use the source conference packet and exact current catalog/index bytes already available in this chat or the repository source archive.\n\nFor each exact identity, return an explicit accepted/held decision with blocker IDs and conditional boundary IDs. Bind the fresh 806/42/0 authority, preserve all prior unrelated holds and passing evidence, verify sources/access/semantics and forward/inverse traces, and return a matching delivery manifest and archive. Keep any genuine missing external premises conditional only when the original requirements allow it. Do not apply anything to the index, canonical/runtime files, or GitHub; Codex will independently audit and apply only explicit acceptances before refreshing your next authority.\n\nCurrent next-group source candidate: {next_group.get('candidate',{}).get('path')} (SHA-256 {next_group.get('candidate',{}).get('sha256')}). Source conference archive: {next_group.get('archive',{}).get('path')} (SHA-256 {next_group.get('archive',{}).get('sha256')}).\n"""
req_path=BASE/'RANK9_PSYCHICFEAR7_RETURN214_REQUEST.txt'; req_path.write_text(req,encoding='utf-8')
print(json.dumps({'status':'PASS','application':str(app_path),'validation':str(validation_path),'indexAfter':index_after_binding,'authority':queue['currentAuthority'],'nextGroup':next['group'],'nextPendingIds':next['pendingIds'],'candidate':str(CAND),'request':str(req_path)},indent=2))
