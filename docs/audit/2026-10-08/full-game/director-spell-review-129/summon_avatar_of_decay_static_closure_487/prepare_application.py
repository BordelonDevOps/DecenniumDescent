"""Prepare one exact static-review application; never edits native catalog or old evidence."""
import copy,hashlib,json,shutil,zlib
from pathlib import Path
def locate_repository():
 for base in [Path.cwd(), *Path(__file__).resolve().parents]:
  for candidate in [base, base/'decay_repo']:
   if (candidate/'DescentReviewChanges').is_dir(): return candidate
 raise RuntimeError('Run within the repository or beside the decay_repo staging checkout')
ROOT=locate_repository()
A=Path('docs/audit/2026-10-08/full-game/director-spell-review-129');O=A/'summon_avatar_of_decay_static_closure_487'
C=Path('DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9decay_static_reviewed_487')
INDEX=Path('DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json');CAT=INDEX.parent/'catalog.json'
PAY=A/'rank9_summon_avatar_of_decay_return333_received/payload';PROC=PAY/'input/05_RETURN285_AVATAR_PROCEDURE.json'
BASE='c6d6a3a0e084008fc260dc6096c2b01fd77e67d6';SCOPE='STATIC_AUTHORED_PROCEDURE_REVIEW_ONLY';ID='summon-avatar-of-decay'
def read(p):return json.loads((ROOT/p).read_bytes())
def binding(p):
 b=(ROOT/p).read_bytes();return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'crc32':f'{zlib.crc32(b)&0xffffffff:08x}'}
written=[]
def write(p,d):
 f=ROOT/p;f.parent.mkdir(parents=True,exist_ok=True);f.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n');written.append(str(p));return binding(p)

oldindex=read(INDEX);oldqueue=read(A/'CURRENT_SPELL_QUEUE_478.json');indexbefore=binding(INDEX);catalogbinding=binding(CAT)
assert indexbefore['sha256']=='0c69755ec80df390b4e8676bfdd81db63f9429f6faf1f23d74bbd99c0856684b'
assert catalogbinding['sha256']=='f52cf6a4a4673897615a74c7c67dcba798c431362d4357e71ee552cc7c5d31f8'
assert read(O/'VALIDATION_487.json')['status']=='PASS'
proc=read(PROC);native=read(CAT)['spells'][670];assert native==proc['nativeSourceAndAccess']
quals=read(PAY/'evidence/RETURN285_QUALIFICATIONS.json')['qualifications'];qualids=[q['id'] for q in quals]
oldcoverage=read(PAY/'PRESERVED_OUTCOMES.json')
remaining=[x for x in oldqueue['remainingPendingIds'] if x!=ID];priority=[x for x in oldqueue['continuingPriorityOrder'] if x!=ID]
before=oldqueue['currentAuthority'];after={**before,'reviewedApplied':834,'pending':14,'acceptedUnapplied':0,'completeStandaloneProcedures':558}
r1=binding(O/'SH333_R01_R1_WITNESS_487_TESTONLY.json');r2=binding(O/'SH333_R02_R1_WITNESS_487_TESTONLY.json')
seal3=binding(A/'summon_avatar_of_decay_r03_mind_blank_witness_408/DIRECTOR_R03_SEAL_408.json');seal4=binding(A/'summon_avatar_of_decay_r04_paired_aura_witness_409/DIRECTOR_R04_SEAL_409.json')
coverage=write(C/'CASE_COVERAGE.json',{
 'id':'DECAY-CASE-COVERAGE-487','scope':SCOPE,'historicalInventoryBinding':binding(PAY/'PRESERVED_OUTCOMES.json'),
 'historicalCases':oldcoverage['exactCaseBindings'],'historicalTotals':oldcoverage['historicalTotals'],'historicalCasesReplayed':False,'historicalCasesOrLabelsChanged':False,
 'residuals':[
 {'id':'SH333-R01','status':'PASS_ADOPTED_TEST_ONLY_COMPONENT_SUFFICIENCY','witness':r1,'criteria':'Complete paid competing Mental Binding integration under exact Repack03; earlier Decay reservation, shared guard, ordinary Ferry attack, repeat saves, passive aura, original deadline and no refunds.'},
 {'id':'SH333-R02','status':'PASS_REVISED_STATIC_OBLIGATION_ONLY','witness':r2,'revision':'SH333-R02-OBLIGATION-REVISION-01','criteria':'Abstract eligibility loss and return; cancellation, reservation release, related maxima/pair recalculation without healing, prospective agency and no revival. Actual type-changing provider remains unqualified.'},
 {'id':'SH333-R03','status':'SEALED_TEST_ONLY_PRESERVED','seal':seal3,'scope':'Existing-relay Mind Blank integration only. No new replay or seal.'},
 {'id':'SH333-R04','status':'SEALED_TEST_ONLY_PRESERVED','seal':seal4,'scope':'Paired conditional paid Decay aura arbitration only. No new replay or seal.'}],
 'openStaticIntegrations':[],'validation':binding(O/'VALIDATION_487.json'),'actualCampaignEvents':0,'runtimeExecuted':False})
recon=write(O/'IDENTITY_RECONCILIATION_487.json',{
 'id':'DECAY-IDENTITY-RECONCILIATION-487','identity':ID,'scope':SCOPE,'baseCommit':BASE,'queueBefore':binding(A/'CURRENT_SPELL_QUEUE_478.json'),
 'sourceProcedure':binding(PROC),'currentCatalog':catalogbinding,'currentCatalogPointer':'/spells/670','currentIndexBefore':indexbefore,'currentIndexPointer':'/entries/670',
 'originalDecision':binding(PAY/'DIRECTOR_DECISION.json'),'originalResiduals':binding(PAY/'RESIDUAL_BRANCH_DISPOSITIONS.json'),'coverage':coverage,
 'retainedQualificationsBinding':binding(PAY/'evidence/RETURN285_QUALIFICATIONS.json'),'retainedQualificationIds':qualids,
 'staticBlockerReadyToClose':['SH202-B03'],'openStaticIntegrations':[],
 'qualificationClarification':{'SH202-H12':'Historical no-application receipt remains byte-exact. Current owner instruction delegates execution of this separately accepted static-only application; no blanket application or native/runtime promotion.','SH333-R02':'Actual type-changing source, access, paid activation and campaign qualification remain unresolved; explicit revision satisfies only the static authored test obligation.'},
 'factsNotInferred':['campaign existence or play','new class powers','actual type-changing source','runtime selectability','balance/cosmology/domain/release approval'],
 'newWitnessProvenance':'Constructed by the assistant under current delegated owner instruction and exact reviewed contracts; not user-authored gameplay.'})
accept=write(O/'DIRECTOR_ACCEPTANCE_487.json',{
 'id':'SH202-B03-DECAY-STATIC-ACCEPTANCE-487','decision':'ACCEPT','scope':SCOPE,'accepted':True,'applied':False,
 'acceptedIds':[ID],'appliedIds':[],'heldIds':remaining,'closedBlockerIds':['SH202-B03'],'closedResidualIds':['SH333-R01','SH333-R02','SH333-R03','SH333-R04'],
 'retainedQualificationIds':qualids,'reconciliation':recon,'retainedProcedure':binding(PROC),'coverage':coverage,'validation':binding(O/'VALIDATION_487.json'),
 'applicationAuthorizedIds':[ID],'applicationAuthorization':'Apply only this exact static-authored procedure envelope to the authored-review index and successor queue/handoff. User delegated completion/application; no native catalog, source procedure, historical witness/seal or runtime modification.',
 'authorityBefore':before,'authorityAfterDecision':{**before,'pending':14,'acceptedUnapplied':1},
 'R02ActualProviderQualified':False,'runtimeSelectionEnabled':False,'campaignOccurrence':False,'newEvidenceSealIssued':False,
 'nextAfterApplication':{'identity':'reverse-gravity-field','blocker':'IE204-B02','order':priority}})
parent=read(PAY/'components/SH333-RIDER-CANCEL.json')['initialState']['world'];body=parent['bodies']['A:cast1:body1']
profilefields=['spellId','nativeHP','type','size','box','massLb','abilities','walk','hands','resistances','immunities','attack','aura','carryLb','pushDragLb','loadCapacity','baseAC']
model=write(C/'MODEL.json',{
 'schemaVersion':1,'id':'RANK9-DECAY-STATIC-REVIEWED-487','reviewId':'SH202-B03-DECAY-STATIC-ACCEPTANCE-487','status':'DIRECTOR_ACCEPTED_STATIC_AUTHORED_PROCEDURE_REVIEW_ONLY',
 'acceptedIds':[ID],'heldIds':[],'closedBlockerIds':['SH202-B03'],'retainedQualificationIds':qualids,'sourceProcedureBinding':binding(PROC),'directorAcceptance':accept,'caseEvidence':coverage,
 'spells':[{'id':ID,'name':'Summon Avatar of Decay','nativeCard':native,
 'procedure':{'commonProcedure':proc['commonProcedure'],'spellLocalProcedure':proc['spellLocalProcedure'],'questionIds':proc['questionIds'],'bodyProfileIds':proc['bodyProfileIds'],'staticProfileProjection':{k:body[k] for k in profilefields},'profileProjectionSource':{**binding(PAY/'components/SH333-RIDER-CANCEL.json'),'pointer':'/initialState/world/bodies/A:cast1:body1','qualification':'Exact retained conditional body values; creation/controller bonuses remain separately calculated by commonProcedure/stats. No generated campaign creature.'}},
 'sourceProcedureRecord':proc,'directorProcedureRecord':{'status':'ACCEPTED_STATIC_AUTHORED_PROCEDURE_REVIEW_ONLY','accepted':True,'closedBlockerIds':['SH202-B03'],'retainedQualificationIds':qualids,'sourceStatusUnchanged':True},'caseEvidence':coverage,'identityReconciliation':recon}],
 'sharedRequirements':{'scope':'Exact retained common procedure only; no shared/global rule widening.','qualifications':quals,'actualProviderQualificationRequired':True,'R02ReviewOnlyRevision':'SH333-R02-OBLIGATION-REVISION-01; abstract eligibility input is not a gameplay source'},
 'runtimeSelectionEnabled':False,'implementationApproved':False,'humanPlayApproved':False,'balanceApproved':False,'cosmologyModified':False,'domainClosure':False,'releaseApproved':False,'nativeCatalogChanged':False,'historicalEvidenceChanged':False})
package=write(C/'CANDIDATE_PACKAGE_MANIFEST.json',{'id':'DECAY-CANDIDATE-PACKAGE-487','scope':SCOPE,'members':[model,coverage],'acceptedIds':[ID],'sourceProcedure':binding(PROC),'qualificationSource':binding(PAY/'evidence/RETURN285_QUALIFICATIONS.json'),'acceptance':accept})
application=write(O/'APPLICATION_487.json',{
 'id':'DECAY-STATIC-APPLICATION-487','status':'APPLIED_TO_AUTHORED_REVIEW_INDEX_ONLY','acceptedIds':[ID],'appliedIds':[ID],'heldIds':remaining,'applicationScope':SCOPE,
 'authorization':binding(O/'DELEGATED_TESTONLY_AUTHORIZATION_487.json'),'exactDirectorAcceptance':accept,'model':model,'caseCoverage':coverage,'candidatePackage':package,'indexBefore':indexbefore,'indexTargetPointer':'/entries/670',
 'authorityBefore':before,'authorityAfter':after,'closedBlockerIds':['SH202-B03'],'retainedQualificationIds':qualids,'catalogUnchanged':catalogbinding,'sourceProcedureUnchanged':binding(PROC),
 'applicationTransaction':'Receipt, model, authored index and successor queue/handoff publish in one commit; this receipt does not rewrite any historical record.',
 'oldHoldAndSealsUnchanged':True,'runtimeSelectionEnabled':False,'campaignStateChanged':False,'canonicalRulesChanged':False,'unrelatedIdentityRowsChanged':False,'nextIdentity':'reverse-gravity-field'})
index=copy.deepcopy(oldindex);row=index['entries'][670]
row.update(authoredStatus='reviewed-authored-operational-playtest',procedureFile='../spell_candidates/rank9decay_static_reviewed_487/MODEL.json',procedurePointer='/spells/0/procedure',wholeCardPointer='/spells/0',sourceCatalogWholeCardPointer='/spells/670',directorProcedureRecordPointer='/spells/0/directorProcedureRecord',sharedRulesPointer='/sharedRequirements',spellLocalRequirementsPointer='/spells/0/procedure',completeEvidenceRoot=str(C),completeEnvelopeBinding=model,caseEvidenceBindings=coverage,candidatePackageManifestBinding=package,authoredAcceptanceReceipt=accept,authoredApplicationReceipt=application,sourceProcedureBinding=binding(PROC),historicalCoverageBinding=binding(PAY/'PRESERVED_OUTCOMES.json'),coverageReconciliationBinding=recon,reviewId='SH202-B03-DECAY-STATIC-ACCEPTANCE-487',accepted=True,applied=True,closedBlockerIds=['SH202-B03'],retainedQualificationIds=qualids,retainedQualifications=qualids,historicalCandidateLabelsPreserved=True,applicationScope='DECAY_AUTHORED_REVIEW_INDEX_ONLY')
index['authoredCounts']={'reviewed':834,'pending':14};index['representationCounts']['completeReviewedStandaloneProcedures']=558
indexbinding=write(INDEX,index)
queue=copy.deepcopy(oldqueue)
queue.update(id='CURRENT-SPELL-QUEUE-479',supersedesQueue=binding(A/'CURRENT_SPELL_QUEUE_478.json'),currentAuthority=after,currentIndexBinding=indexbinding,remainingPendingIds=remaining,continuingPriorityOrder=priority,nextIdentity='reverse-gravity-field',nextBlockerIds=['IE204-B02'],closureTasksRemaining=14,acceptedIds=[ID],appliedIds=[ID],closedBlockerIdsThisStep=['SH202-B03'],currentApplication=application,pendingIdentityAuditPath=str(A/'CURRENT14_PENDING_IDENTITY_AUDIT_479.json'),currentHandoffPath=str(A/'CURRENT_HANDOFF_479.json'),currentReviewPacket={**recon,'classification':'GPT_DIRECTOR_ACCEPTED_STATIC_AUTHORED_PROCEDURE_REVIEW_ONLY','identityAccepted':True,'identityAppliedToAuthoredIndex':True,'runtimeSelectionEnabled':False},currentDirectorReadback=accept,repackNote='Summon Avatar of Decay accepted and applied only for static authored review. R01/R02 new reversible TEST_ONLY witnesses pass; R03/R04 existing seals retained. SH202-H01-H12 and actual-source/provider/runtime qualifications remain. Next in unchanged relative order: Reverse Gravity Field.',recordedAtUtc='2026-11-02')
qbind=write(A/'CURRENT_SPELL_QUEUE_479.json',queue)
pending=write(A/'CURRENT14_PENDING_IDENTITY_AUDIT_479.json',{'id':'CURRENT14-PENDING-IDENTITY-AUDIT-479','queue':qbind,'index':indexbinding,'currentAuthority':after,'remainingPendingIds':remaining,'continuingPriorityOrder':priority,'firstReviewTasksRemaining':0,'closureTasksRemaining':14,'acceptedUnapplied':0,'nextIdentity':'reverse-gravity-field','unrelatedPendingOrderUnchanged':True})
handoff=write(A/'CURRENT_HANDOFF_479.json',{'id':'CURRENT-HANDOFF-479','supersedes':binding(A/'CURRENT_HANDOFF_478.json'),'queue':qbind,'pendingAudit':pending,'authority':after,'completedIdentity':ID,'application':application,'nextIdentity':'reverse-gravity-field','nextBlockerIds':['IE204-B02'],'continuingPriorityOrder':priority,'instruction':'Complete this first remaining identity before starting the following identity. Preserve each exact static-only source/runtime qualification.','runtimeSelectionEnabled':False,'campaignStateChanged':False,'acceptedUnapplied':0})

for name in ['build_decay.py','verify_decay.py','prepare_application.py']:
 src=Path(__file__).parent/name;dst=ROOT/O/name;shutil.copyfile(src,dst);written.append(str(O/name))
for f in (ROOT/O).glob('*.json'):
 if str(f.relative_to(ROOT)) not in written:written.append(str(f.relative_to(ROOT)))
# Record only intended writes, never the fetched source cache.
Path(__file__).with_name('publish_paths.json').write_text(json.dumps(sorted(set(written)),indent=2)+'\n')
Path(__file__).with_name('index_before.json').write_text(json.dumps(oldindex,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'accepted':[ID],'applied':[ID],'authorityAfter':after,'nextIdentity':priority[0],'files':len(set(written))},indent=2))
