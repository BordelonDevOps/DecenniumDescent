from __future__ import annotations
import copy, gzip, hashlib, json, shutil, zipfile
from datetime import datetime, timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]
AUDIT=ROOT/'docs/audit/2026-10-08/full-game/director-spell-review-129'
REC= AUDIT/'rank9_castingcost5_return194_received'
ZIP=REC/'DD_Rank9_CastingCost5_Director_Return194.zip'; DELIVERY=REC/'DD_Rank9_CastingCost5_Director_Return194_DELIVERY.json'
AUDIT_JSON=AUDIT/'RANK9_CASTINGCOST5_RETURN194_INDEPENDENT_AUDIT.json'
INDEX=ROOT/'DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json'
CATALOG=ROOT/'DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json'
Q0=AUDIT/'CURRENT_SPELL_QUEUE_193.json'; H0=AUDIT/'CURRENT_HANDOFF_193.json'; P0=AUDIT/'CURRENT69_PENDING_IDENTITY_AUDIT_193.json'
BACKUP=AUDIT/'authored_review_index.before_castingcost5_194.json'
PKG_REL=Path('DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9castingcost5_reviewed_194')
PKG=ROOT/PKG_REL; STAGE=PKG.with_name(PKG.name+'.staging')
MAN=ROOT/'DescentReviewChanges/ReviewBible/docs/spells/candidates/RANK9_CASTINGCOST5_REVIEWED_194.md'
GROUP=['perfect-spell','ritual-mastery','world-rewrite','resonance-perfection','unholy-ascendance']
ACCEPTED=['ritual-mastery','world-rewrite','resonance-perfection']; UNACCEPTED=['perfect-spell','unholy-ascendance']
BLOCKERS={'perfect-spell':['CC194-B01'],'unholy-ascendance':['CC194-B04']}
NEXT='rank9-memory-denial6'; NEXT_IDS=['mass-willbreaker','mind-collapse','mind-prison-mass','mind-wipe','unmake-spell','unravel-identity']
BEFORE={'reviewed':779,'pending':69}; AFTER={'reviewed':782,'pending':66}; COMPLETE0,COMPLETE1=503,506
REVIEW='RANK9-CASTINGCOST5-EXACT-AUTHORED-ACCEPTANCE-194'; APP='RANK9-CASTINGCOST5-APPLICATION-194'
DEC=AUDIT/'RANK9_CASTINGCOST5_DIRECTOR_DECISION_194.json'; ACC=AUDIT/'RANK9_CASTINGCOST5_EXACT_ACCEPTANCE_194.json'
RCPT=AUDIT/'RANK9_CASTINGCOST5_RETURN194_RECEIPT.json'; APPFILE=AUDIT/'RANK9_CASTINGCOST5_APPLICATION_194.json'
OPS=AUDIT/'RANK9_CASTINGCOST5_INDEX_OPERATIONS_194.json'; P1=AUDIT/'CURRENT66_PENDING_IDENTITY_AUDIT_194.json'
Q1=AUDIT/'CURRENT_SPELL_QUEUE_194.json'; H1=AUDIT/'CURRENT_HANDOFF_194.json'; VALID=AUDIT/'RANK9_CASTINGCOST5_APPLICATION_VALIDATION_194.json'; SNAP=AUDIT/'CURRENT_SPELL_REVIEW_SNAPSHOT_194.md'
def sha(b):return hashlib.sha256(b).hexdigest()
def sha_file(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def jb(v):return (json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode()
def write(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(jb(v))
def bind(p,raw=None):
 b=p.read_bytes() if raw is None else raw; return {'path':p.relative_to(ROOT).as_posix(),'bytes':len(b),'sha256':sha(b)}
def main():
 outputs=[BACKUP,MAN,DEC,ACC,RCPT,APPFILE,OPS,P1,Q1,H1,VALID,SNAP]
 assert not PKG.exists() and all(not p.exists() for p in outputs)
 audit=read(AUDIT_JSON); delivery=read(DELIVERY)
 assert audit['status']=='PASS' and audit['checksPassed']==24 and audit['checksFailed']==0 and audit['applied'] is False
 assert audit['acceptedIds']==ACCEPTED and audit['unacceptedIds']==UNACCEPTED
 assert ZIP.stat().st_size==131568634 and sha_file(ZIP)==delivery['archive']['sha256']==audit['returnArchive']['sha256']=='f6caf05f6677213059762119b07a5eb0add983a5cc5f152fd317d04f328af90c'
 assert delivery['applied'] is False and delivery['acceptedIds']==ACCEPTED and delivery['unacceptedIds']==UNACCEPTED
 assert delivery['authorityUnchanged']=={'reviewedApplied':779,'pending':69,'acceptedUnapplied':0,'completeStandaloneProcedures':503,'scopedInterfaces':173}
 before_raw,catalog_raw=INDEX.read_bytes(),CATALOG.read_bytes(); before,catalog=read(INDEX),read(CATALOG)
 q0,h0,p0=map(read,(Q0,H0,P0)); rows={x['id']:x for x in before['entries']}; cats={x['id']:x for x in catalog['spells']}
 live={x['id'] for x in before['entries'] if x['authoredStatus']=='pending-authored-procedure'}
 assert before['authoredCounts']==BEFORE and before['representationCounts']['completeReviewedStandaloneProcedures']==COMPLETE0
 assert len(live)==69 and set(GROUP)<=live and set(p0['pendingIds'])==live and p0['indexBinding']['sha256']==sha(before_raw)
 assert q0['currentAuthority']['reviewedApplied']==779 and q0['currentAuthority']['pending']==69
 assert all(rows[s]['sourceStatus']=='blocked-pending-operational-review' for s in GROUP)
 timestamp=datetime.now(timezone.utc).isoformat()
 with zipfile.ZipFile(ZIP) as z:
  director=json.loads(z.read('DIRECTOR_DECISION.json')); pdoc=json.loads(z.read('PROCEDURES.json'))
  procs={x['id']:x for x in pdoc}; decs={x['id']:x for x in director['decisions']}; block_records=delivery['blockers']
  assert set(procs)==set(decs)==set(GROUP) and director['acceptedIds']==ACCEPTED and director['unacceptedIds']==UNACCEPTED and director['applied'] is False
  assert director['retainedNamedOutsideScopeBlockers']==['AG190-B01','AG190-B02','TF192-B01','TF192-B02','TF192-B04','TF192-B05']
  assert all(decs[s]['accepted'] and not decs[s]['applied'] and not decs[s]['blockerIds'] for s in ACCEPTED)
  assert all(not decs[s]['accepted'] and decs[s]['blockerIds']==BLOCKERS[s] for s in UNACCEPTED)
  assert all(not procs[s]['applied'] and procs[s]['completeSourceAndAccess']==cats[s] for s in GROUP)
  STAGE.mkdir(parents=True,exist_ok=True)
  keep=['ACTOR_PROFILES.json','ADDITIONAL_SOURCE_BINDINGS.json','AUTHORITY.json','CARRIED_HOLDS_192.json','CASE_DISPOSITIONS.json','CASE_HASH_BINDINGS.json','CLOCK_CHECK.json','COUNTS.json','CURRENT_CONTEXT_193.json','DATA_INTEGRITY_CHECK.json','DIRECTOR_DECISION.json','EVIDENCE_MANIFEST.json','FAILURE_CHECK.md','FINAL_METADATA_CHECK.json','FUTURE_OBLIGATION_DISPOSITIONS.json','HOLD_REGISTER.json','INDEPENDENT_SEMANTIC_FAILURE_CHECK.json','MEMBER_MANIFEST.json','NEXT_QUEUE_GROUP.json','ORIGINAL_OBLIGATIONS.json','ORIGINAL_QUESTIONS.json','PROCEDURES.json','PROPOSAL_OPERATIONS.json','QUESTION_DISPOSITIONS.json','QUESTION_SELECTIONS.md','REQUEST_193.txt','SOURCE_BINDINGS.json','SOURCE_ENVELOPES.json','SOURCE_VERIFICATION.json','STANDALONE_PROCEDURES.md','VALIDATION.json']
  for n in keep:(STAGE/n).write_bytes(z.read(n))
  for n in ['companion_life10.json','magic7_MODEL.json','rank8_damage6.json','transport6_MODEL.json','ward5_MODEL.json']:
   o=STAGE/'additional_sources'/n;o.parent.mkdir(parents=True,exist_ok=True);o.write_bytes(z.read('additional_sources/'+n))
  for sid in GROUP:
   o=STAGE/'procedures'/f'{sid}.json';o.parent.mkdir(parents=True,exist_ok=True);o.write_bytes(z.read(f'procedures/{sid}.json'))
  case_raw=z.read('CASEBOOK.json')
  with (STAGE/'CASEBOOK.json.gz').open('wb') as f:
   with gzip.GzipFile(fileobj=f,mode='wb',filename='',mtime=0,compresslevel=6) as gz:gz.write(case_raw)
  (STAGE/'DIRECTOR_DELIVERY_OBSERVATION.json').write_bytes(DELIVERY.read_bytes());(STAGE/'INDEPENDENT_RETURN_AUDIT.json').write_bytes(AUDIT_JSON.read_bytes())
  arc_bind,del_bind,audit_bind=bind(ZIP),bind(DELIVERY),bind(AUDIT_JSON)
  case_row=next(x for x in delivery['members'] if x['path']=='CASEBOOK.json')
  case_src={'path':'CASEBOOK.json','bytes':case_row['bytes'],'sha256':case_row['sha256']}
  case_bind=bind(ROOT/PKG_REL/'CASEBOOK.json.gz',(STAGE/'CASEBOOK.json.gz').read_bytes())
  cases=json.loads(case_raw); accepted_case_ids={c for s in ACCEPTED for c in decs[s]['caseIds']}
  accepted_events=sum(len(c['events']) for c in cases['cases'] if c['id'] in accepted_case_ids)
  spells=[]
  for pos,s in enumerate(ACCEPTED):
   src=procs[s]
   spells.append({'id':s,'name':rows[s]['name'],'position':pos,'procedure':{'id':'CC194-STATIC-'+s.upper().replace('-','_'),'spellId':s,'status':'director-accepted static authored procedure; applied to authored review index; runtime disabled','accepted':True,'applied':False,'nativeCardUnchanged':copy.deepcopy(src['completeSourceAndAccess']),'procedureContent':src['procedure'],'sharedRequirements':src['commonProcedure'],'newChoices':src['newChoices'],'qualifications':copy.deepcopy(src['qualifications']),'caseIds':copy.deepcopy(decs[s]['caseIds']),'questionIds':copy.deepcopy(src['questionIds']),'holdIds':copy.deepcopy(decs[s]['holdIds']),'directorDecisionId':director['id']},'directorProcedureRecord':copy.deepcopy(src),'nativeCardUnchanged':copy.deepcopy(src['completeSourceAndAccess']),'caseIds':copy.deepcopy(decs[s]['caseIds']),'questionIds':copy.deepcopy(src['questionIds']),'holdIds':copy.deepcopy(decs[s]['holdIds']),'runtimeSelectionEnabled':False})
  unacc={s:{'blockerIds':decs[s]['blockerIds'],'holdIds':decs[s]['holdIds'],'blockerRecords':[copy.deepcopy(b) for b in block_records if s in b['blockingForIds']]} for s in UNACCEPTED}
  model={'schemaVersion':1,'moduleId':'rank9-castingcost5-reviewed-194','status':'THREE_EXACT_AUTHORED_PROCEDURES_ACCEPTED_AND_APPLIED_WITH_TWO_BLOCKERS','scope':'Only three individually accepted static procedures are applied. Perfect Spell and Unholy Ascendance remain pending under CC194-B01 and CC194-B04. Native cards and class routes remain unchanged; runtime and downstream approval gates stay disabled.','acceptedIds':ACCEPTED,'unacceptedIds':UNACCEPTED,'excludedPendingIds':sorted(live-set(ACCEPTED)),'unacceptedHolds':unacc,'inheritedNamedBlockerIds':director['retainedNamedOutsideScopeBlockers'],'sharedRequirements':{'scope':'No global/shared rule changes; native cards and class routes unchanged.','runtimeSelectionEnabled':False},'spells':spells,'caseCoverage':{'caseCount':delivery['counts']['cases'],'acceptedCaseCount':len(accepted_case_ids),'acceptedEventCount':accepted_events,'allCaseReplay':audit['replay']},'returnCounts':delivery['counts'],'sourceArchive':arc_bind,'deliveryManifest':del_bind,'independentAudit':audit_bind,'casebookFile':'CASEBOOK.json.gz','casebookSourceArchiveMemberBinding':case_src,'casebookBinding':case_bind,'runtimeSelectionEnabled':False,'runtimeTestsExecuted':False,'sourceProgramsExecuted':False,'implementationApproved':False,'humanPlaytested':False,'balanceApproved':False,'cosmologyModified':False,'releaseApproved':False,'domainClosure':False}
  write(STAGE/'MODEL.json',model)
  pkg_manifest={'id':'RANK9-CASTINGCOST5-PACKAGE-MANIFEST-194','sourceArchive':arc_bind,'deliveryManifest':del_bind,'independentAudit':audit_bind,'sourceAnchorCommit':audit['sourceCommit'],'files':[]}
  for f in sorted(x for x in STAGE.rglob('*') if x.is_file()):
   b=f.read_bytes();pkg_manifest['files'].append({'path':(PKG_REL/f.relative_to(STAGE)).as_posix(),'bytes':len(b),'sha256':sha(b)})
  write(STAGE/'CANDIDATE_PACKAGE_MANIFEST.json',pkg_manifest)
  manifest_bind=bind(ROOT/PKG_REL/'CANDIDATE_PACKAGE_MANIFEST.json',(STAGE/'CANDIDATE_PACKAGE_MANIFEST.json').read_bytes())
  shutil.move(str(STAGE),str(PKG))
  model_bind=bind(PKG/'MODEL.json'); manifest_bind=bind(PKG/'CANDIDATE_PACKAGE_MANIFEST.json'); case_bind=bind(PKG/'CASEBOOK.json.gz')
  MAN.parent.mkdir(parents=True,exist_ok=True); MAN.write_bytes((PKG/'STANDALONE_PROCEDURES.md').read_bytes())
  shutil.copyfile(INDEX,BACKUP); assert BACKUP.read_bytes()==before_raw
  blockers=unacc
  write(DEC,{'id':director['id'],'recordedAtUtc':timestamp,'decision':'PARTIAL_EXACT_IDENTITY_ACCEPTANCE','acceptedIds':ACCEPTED,'unacceptedIds':UNACCEPTED,'blockers':blockers,'directorReturn':arc_bind,'deliveryManifest':del_bind,'independentAudit':audit_bind,'authorityAtDecision':delivery['authorityUnchanged'],'exactDirectorDecisions':director['decisions'],'inheritedBlockerIdsCarriedForward':director['retainedNamedOutsideScopeBlockers'],'scope':'Static authorship only; no runtime, implementation, human-play, balance, cosmology, domain closure, completion or release approval.','canonicalFilesChangedByDirector':False})
  acceptance={'id':REVIEW,'recordedAtUtc':timestamp,'status':'THREE_EXACT_STATIC_AUTHORED_PROCEDURES_ACCEPTED_WITH_TWO_RETAINED_BLOCKERS','acceptedIds':ACCEPTED,'unacceptedIds':UNACCEPTED,'directorDecision':bind(DEC),'directorReturn':arc_bind,'deliveryManifest':del_bind,'independentAudit':audit_bind,'candidateEnvelope':model_bind,'candidatePackageManifest':manifest_bind,'countsBefore':BEFORE,'countsAfter':AFTER,'completeReviewedStandaloneProceduresBefore':COMPLETE0,'completeReviewedStandaloneProceduresAfter':COMPLETE1,'blockers':blockers,'runtimeSelectionEnabled':False,'canonicalApplicationPerformedByOwner':False}
  write(ACC,acceptance)
  write(RCPT,{'id':'RANK9-CASTINGCOST5-RETURN194-RECEIPT','recordedAtUtc':timestamp,'status':'THREE_ACCEPTED_TWO_BLOCKED_INDEPENDENT_AUDIT_PASSED','reviewedIds':GROUP,'acceptedIds':ACCEPTED,'unacceptedIds':UNACCEPTED,'blockers':blockers,'inheritedBlockerIds':director['retainedNamedOutsideScopeBlockers'],'directorReturn':arc_bind,'deliveryManifest':del_bind,'independentAudit':audit_bind,'sourceAuthority':delivery['authorityUnchanged'],'counts':delivery['counts'],'decisionId':director['id']})
  write(APPFILE,{'id':APP,'recordedAtUtc':timestamp,'status':'APPLIED_THREE_EXACT_AUTHORED_PROCEDURES_WITH_TWO_RETAINED_BLOCKERS','ownerInstruction':'Apply each exact director-accepted ordinary-spell batch, push it to GitHub, and continue until pending reaches zero.','acceptedIds':ACCEPTED,'unacceptedIds':UNACCEPTED,'directorAcceptance':bind(ACC),'directorDecision':bind(DEC),'directorReturnReceipt':bind(RCPT),'directorReturn':arc_bind,'deliveryManifest':del_bind,'independentAudit':audit_bind,'candidateEnvelope':model_bind,'candidatePackageManifest':manifest_bind,'manuscript':bind(MAN),'indexBefore':bind(BACKUP,before_raw),'countsBefore':BEFORE,'countsAfter':AFTER,'completeReviewedStandaloneProcedures':{'before':COMPLETE0,'after':COMPLETE1},'sourceStatusPreservedAsBlocked':True,'catalogChanged':False,'runtimeSelectionEnabled':False})
  app_bind=bind(APPFILE); after=copy.deepcopy(before); ops=[]
  for pos,s in enumerate(ACCEPTED):
   ix=next(i for i,x in enumerate(before['entries']) if x['id']==s); old=before['entries'][ix]; new=copy.deepcopy(old)
   new.update({'authoredStatus':'reviewed-authored-operational-playtest','procedureFile':'../spell_candidates/rank9castingcost5_reviewed_194/MODEL.json','procedurePointer':f'/spells/{pos}/procedure','wholeCardPointer':f'/spells/{pos}','sourceCatalogWholeCardPointer':old.get('sourceCatalogWholeCardPointer') or old['wholeCardPointer'],'wholeCardIdField':'id','procedureTextPointer':f'/spells/{pos}/procedure/procedureContent','directorProcedureRecordPointer':f'/spells/{pos}/directorProcedureRecord','sharedRulesPointer':f'/spells/{pos}/procedure/sharedRequirements','manuscript':'../../../docs/spells/candidates/RANK9_CASTINGCOST5_REVIEWED_194.md','reviewId':APP,'runtimeSelectionEnabled':False,'historicalCandidateLabelsPreserved':True,'completeEvidenceRoot':PKG_REL.as_posix(),'completeEnvelopeBinding':model_bind,'casebookBinding':case_bind,'casebookEncoding':'Deterministic gzip; decompression reproduces the exact CASEBOOK.json member of the director return archive.','casebookSourceArchiveMemberBinding':model['casebookSourceArchiveMemberBinding'],'sourceArchiveBinding':arc_bind,'deliveryManifestBinding':del_bind,'candidatePackageManifestBinding':manifest_bind,'procedureSourceBinding':bind(DEC),'authoredAcceptanceReceipt':bind(ACC),'authoredApplicationReceipt':app_bind})
   assert old['sourceStatus']==new['sourceStatus']=='blocked-pending-operational-review'
   ops.append({'op':'replace-entry','identity':s,'index':ix,'before':copy.deepcopy(old),'after':copy.deepcopy(new)}); after['entries'][ix]=new
  after['additionalStandaloneEnvelopes'].append({'file':'../spell_candidates/rank9castingcost5_reviewed_194/MODEL.json','binding':model_bind,'reviewId':REVIEW,'acceptedIds':ACCEPTED,'unacceptedIds':UNACCEPTED,'excludedPendingIds':sorted(live-set(ACCEPTED)),'authority':bind(ACC),'applicationReceipt':APPFILE.relative_to(ROOT).as_posix(),'sourceArchive':arc_bind,'deliveryManifest':del_bind,'casebookBinding':case_bind,'candidatePackageManifestBinding':manifest_bind,'scope':acceptance['status'],'runtimeSelectionEnabled':False})
  after['authoredCounts']=AFTER; after['representationCounts']['completeReviewedStandaloneProcedures']=COMPLETE1
  pending={x['id'] for x in after['entries'] if x['authoredStatus']=='pending-authored-procedure'}
  assert pending==live-set(ACCEPTED) and len(pending)==66
  inverse=copy.deepcopy(after)
  for op in ops: inverse['entries'][op['index']]=copy.deepcopy(op['before'])
  inverse['additionalStandaloneEnvelopes']=inverse['additionalStandaloneEnvelopes'][:-1]; inverse['authoredCounts']=copy.deepcopy(before['authoredCounts']); inverse['representationCounts']=copy.deepcopy(before['representationCounts']); assert inverse==before
  after_raw=jb(after); tmp=INDEX.with_suffix('.json.castcost194.tmp'); tmp.write_bytes(after_raw); tmp.replace(INDEX); assert CATALOG.read_bytes()==catalog_raw
  write(OPS,{'id':'RANK9-CASTINGCOST5-INDEX-OPERATIONS-194','before':bind(BACKUP,before_raw),'after':bind(INDEX,after_raw),'operations':ops,'inverseSemanticExact':True,'onlyIdentityIds':ACCEPTED})
  groups=[]
  for oldg in q0['currentPendingGroups']:
   left=[s for s in oldg['pendingIds'] if s in pending]
   if not left: continue
   g=copy.deepcopy(oldg);g['pendingIds']=left;g['pendingCount']=len(left)
   if g['group']=='rank9-casting-cost5':g.update({'status':'PARTIAL_RETURN194_THREE_ACCEPTED_APPLIED_TWO_BLOCKED','freshPacketRequiredForCurrentAuthority':True,'blockingReturn':{'ids':UNACCEPTED,'blockers':BLOCKERS,'receipt':RCPT.relative_to(ROOT).as_posix()}})
   if g['group']==NEXT:g.update({'status':'PENDING_FRESH_PACKET_FOR_CURRENT_AUTHORITY','freshPacketRequiredForCurrentAuthority':True})
   groups.append(g)
  ng=next(g for g in groups if g['group']==NEXT); authority={'reviewedApplied':782,'pending':66,'acceptedUnapplied':0,'completeStandaloneProcedures':506,'scopedInterfaces':173}
  pending_doc={'id':'CURRENT66-PENDING-IDENTITY-AUDIT-194','recordedAtUtc':timestamp,'status':'PASSED_EXACT_CURRENT_INDEX_PENDING_SET','indexBinding':bind(INDEX,after_raw),'catalogBinding':bind(CATALOG,catalog_raw),'authoredCounts':AFTER,'pendingCount':66,'pendingIds':sorted(pending),'allPendingExistInSourceCatalog':pending<=set(cats),'acceptedUnapplied':0,'retainedReturn188Blockers':p0.get('retainedReturn188Blockers',{}),'retainedReturn190Blockers':p0.get('retainedReturn190Blockers',{}),'retainedReturn192Blockers':p0.get('retainedReturn192Blockers',{}),'retainedReturn194Blockers':{s:{'blockerIds':BLOCKERS[s],'holdIds':decs[s]['holdIds'],'reason':next(b['missing'] for b in block_records if s in b['blockingForIds'])} for s in UNACCEPTED},'closed335AndCompletedCohortsReopened':False}
  write(P1,pending_doc); next_req={'group':NEXT,'pendingIds':NEXT_IDS,'pendingCount':6,'status':'PENDING_FRESH_PACKET_FOR_CURRENT_AUTHORITY','freshPacketRequiredForCurrentAuthority':True,'candidate':ng.get('candidate'),'archive':ng.get('archive')}
  q1=copy.deepcopy(q0); q1.update({'id':'SPELL-REVIEW-QUEUE-194','recordedAtUtc':timestamp,'currentAuthority':authority,'pendingCount':66,'currentPendingGroups':groups,'justAppliedBatch':{'reviewId':REVIEW,'ids':ACCEPTED,'count':3,'applicationReceipt':APPFILE.relative_to(ROOT).as_posix(),'directorAcceptance':ACC.relative_to(ROOT).as_posix(),'independentAudit':AUDIT_JSON.relative_to(ROOT).as_posix()},'pendingIdentityAudit':{'path':P1.relative_to(ROOT).as_posix(),'pending':66,'sha256':sha(P1.read_bytes())},'nextGroup':NEXT,'next':next_req,'nextPreparedRequest':next_req,'packetStatus':'RANK9_CASTINGCOST5_RETURN194_THREE_APPLIED_TWO_HELD_782_66_NEXT_RANK9_MEMORY_DENIAL6','currentReturnBinding':arc_bind,'currentPreparation':audit_bind,'currentReturnAudit':audit_bind})
  for k in ('sourceConferencePrepared','currentPacket','currentPacketDelivery'):q1.pop(k,None)
  q1['currentSubmission']=bind(RCPT);q1['currentSubmissionBinding']=bind(RCPT);q1['currentReturnBinding']=arc_bind;q1['currentReturnAudit']=audit_bind;write(Q1,q1)
  h1=copy.deepcopy(h0);h1.update({'id':'CURRENT-HANDOFF-194','recordedAtUtc':timestamp,'status':'RANK9_CASTINGCOST5_THREE_APPLIED_TWO_HELD_NEXT_RANK9_MEMORY_DENIAL6_66_PENDING','currentAuthority':authority,'currentIndexBinding':bind(INDEX,after_raw),'currentCatalogBinding':bind(CATALOG,catalog_raw),'pendingIdentityAudit':{'id':pending_doc['id'],'path':P1.relative_to(ROOT).as_posix(),'pendingCount':66,'sha256':sha(P1.read_bytes())},'appliedThisStep':{'reviewId':REVIEW,'ids':ACCEPTED,'count':3,'applicationReceipt':APPFILE.relative_to(ROOT).as_posix(),'directorAcceptance':ACC.relative_to(ROOT).as_posix(),'independentAudit':AUDIT_JSON.relative_to(ROOT).as_posix(),'applicationValidation':{'path':VALID.relative_to(ROOT).as_posix()}},'unacceptedThisStep':{'ids':UNACCEPTED,'blockers':BLOCKERS,'retainedInPendingSet':True},'nextGroup':NEXT,'nextPendingCount':6,'nextPreparedRequest':next_req,'currentQueueBinding':bind(Q1),'currentReturnBinding':arc_bind,'independentAuditBinding':audit_bind,'parentHandoff':H0.relative_to(ROOT).as_posix(),'currentSubmissionBinding':bind(RCPT),'currentReturnAudit':audit_bind,'resumePriority':'Prepare a fresh Memory/Denial6 packet at 782/66 for GPT; audit and apply exact acceptances, push, and continue until pending is zero.'})
  for k in ('sourceConferencePrepared','currentPacket','currentPacketDelivery','currentPreparation'):h1.pop(k,None)
  write(H1,h1); shutil.copyfile(MAN,AUDIT/'RANK9_CASTINGCOST5_REVIEWED_194.md')
  SNAP.write_text(f'# Current ordinary spell-review checkpoint 194\n\nReturn194 passed {audit["checksPassed"]} independent checks: {audit["replay"]["cases"]} cases, {audit["replay"]["events"]} events, {audit["replay"]["forwardPatchOps"]} forward and {audit["replay"]["inversePatchOps"]} inverse operations. Applied exactly {", ".join(ACCEPTED)} as static authored procedures. {UNACCEPTED[0]} and {UNACCEPTED[1]} remain pending under CC194-B01 and CC194-B04. Authority: **782 reviewed / 66 pending / 0 accepted-unapplied**, 506 complete procedures. Next: Rank9 Memory/Denial6.\n',encoding='utf-8',newline='\n')
  start=ROOT/'START_HERE.md';old=start.read_text(encoding='utf-8-sig') if start.exists() else ''
  start.write_text(f'**Current ordinary spell-review handoff [194](docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_194.json):** Applied exactly {", ".join(ACCEPTED)}. Authority is **782 reviewed / 66 pending / 0 accepted-unapplied**. Perfect Spell and Unholy Ascendance remain pending under CC194-B01 and CC194-B04. Next group: Rank9 Memory/Denial6.\n\n'+old,encoding='utf-8',newline='\n')
  checks=[{'check':'Independent audit and bound return ZIP pass','passed':audit['status']=='PASS' and sha_file(ZIP)==arc_bind['sha256']},{'check':'Exactly three accepted IDs applied; two blocked IDs remain pending','passed':[o['identity'] for o in ops]==ACCEPTED and set(UNACCEPTED)<=pending},{'check':'Authority advanced 779/69/503 to 782/66/506','passed':after['authoredCounts']==AFTER and after['representationCounts']['completeReviewedStandaloneProcedures']==COMPLETE1},{'check':'Pending set is exact prior set minus acceptances','passed':pending==live-set(ACCEPTED)},{'check':'Inverse restores original index and catalog is byte-identical','passed':inverse==before and CATALOG.read_bytes()==catalog_raw},{'check':'Every candidate file is manifest-bound','passed':all((ROOT/r['path']).is_file() and (ROOT/r['path']).stat().st_size==r['bytes'] and sha_file(ROOT/r['path'])==r['sha256'] for r in pkg_manifest['files'])},{'check':'Next group and six IDs are correct','passed':q1['nextGroup']==NEXT and ng['pendingIds']==NEXT_IDS},{'check':'Runtime and downstream gates remain off','passed':all(model[k] is False for k in ('runtimeSelectionEnabled','runtimeTestsExecuted','sourceProgramsExecuted','implementationApproved','humanPlaytested','balanceApproved','cosmologyModified','releaseApproved','domainClosure'))}]
  validation={'id':'RANK9-CASTINGCOST5-APPLICATION-VALIDATION-194','recordedAtUtc':timestamp,'status':'PASS' if all(x['passed'] for x in checks) else 'FAIL','checksPassed':sum(x['passed'] for x in checks),'checksFailed':sum(not x['passed'] for x in checks),'checks':checks,'acceptedIds':ACCEPTED,'unacceptedIds':UNACCEPTED,'countsBefore':{**BEFORE,'completeReviewedStandaloneProcedures':COMPLETE0},'countsAfter':{**AFTER,'completeReviewedStandaloneProcedures':COMPLETE1},'indexBefore':bind(BACKUP,before_raw),'indexAfter':bind(INDEX),'catalog':bind(CATALOG),'application':bind(APPFILE),'independentAudit':audit_bind,'pendingIdentityAudit':bind(P1),'queueAfter':bind(Q1),'handoffAfter':bind(H1),'nextGroup':NEXT,'runtimeSelectionEnabled':False}
  write(VALID,validation); assert validation['status']=='PASS',checks
  print(json.dumps({'status':'APPLIED_AND_VALIDATED','acceptedIds':ACCEPTED,'unacceptedIds':UNACCEPTED,'authority':authority,'nextGroup':NEXT,'independentAudit':audit['status'],'validation':validation['status'],'indexSha256':sha_file(INDEX),'candidateManifest':manifest_bind},indent=2))
if __name__=='__main__':main()
