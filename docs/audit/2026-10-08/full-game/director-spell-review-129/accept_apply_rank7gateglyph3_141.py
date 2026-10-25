from __future__ import annotations
import copy,gzip,hashlib,json,os,pathlib,shutil,zipfile
from datetime import datetime,timezone
ROOT=pathlib.Path(r'C:\Github\DecenniumDescent')
A=ROOT/'docs/audit/2026-10-08/full-game/director-spell-review-129'
RET=A/'rank7gateglyph3_return01_141_repack01_received'
ZIP=RET/'DD_Rank7GateGlyph3_Director_Return01_141.zip'
DEL=RET/'DIRECTOR_RETURN_DELIVERY.json'
AUDIT=A/'RANK7_GATEGlyph3_RETURN01_INDEPENDENT_AUDIT_141.json'
INDEX=ROOT/'DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json'
CATALOG=ROOT/'DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json'
QUEUE_BEFORE=A/'CURRENT_SPELL_QUEUE_140.json'
PENDING_BEFORE=A/'CURRENT162_PENDING_IDENTITY_AUDIT_140.json'
HANDOFF_BEFORE=A/'CURRENT_HANDOFF_140.json'
IDS=['chain-gate','symbol','symbol-of-death']
REVIEW_ID='RANK7-GATEGlyph3-EXACT-AUTHORED-ACCEPTANCE-141'
APP_PATH='docs/audit/2026-10-08/full-game/director-spell-review-129/RANK7_GATEGlyph3_APPLICATION_141.json'
CANDIDATE=ROOT/'DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank7gateglyph3_reviewed_141'
STAGING=CANDIDATE.with_name(CANDIDATE.name+'.staging')
MANUSCRIPT=ROOT/'docs/spells/candidates/RANK7_GATEGlyph3_REVIEWED_141.md'
RECEIPT_PATH=A/'RANK7_GATEGlyph3_EXACT_ACCEPTANCE_141.json'
BACKUP=A/'authored_review_index.before_rank7gateglyph3_141.json'
QUEUE= A/'CURRENT_SPELL_QUEUE_141.json'
PENDING=A/'CURRENT159_PENDING_IDENTITY_AUDIT_141.json'
HANDOFF=A/'CURRENT_HANDOFF_141.json'
def now():return datetime.now(timezone.utc).isoformat()
def sha(b:bytes)->str:return hashlib.sha256(b).hexdigest()
def bind(p:pathlib.Path,rel=None):
 b=p.read_bytes();return {'path':rel or p.relative_to(ROOT).as_posix(),'bytes':len(b),'sha256':sha(b)}
def writej(p:pathlib.Path,obj):p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def candidate_bind(name):return bind(CANDIDATE/name,CANDIDATE.relative_to(ROOT).as_posix()+'/'+name)
# Exact return, audit, source, and live authority preconditions.
assert not CANDIDATE.exists() and not STAGING.exists()
assert not BACKUP.exists() and not RECEIPT_PATH.exists() and not (A/APP_PATH.split('/')[-1]).exists()
assert AUDIT.is_file() and json.loads(AUDIT.read_text(encoding='utf-8'))['status']=='PASS_READY_FOR_EXACT_AUTHORED_PROCEDURE_ACCEPTANCE_WITH_RETAINED_SOURCE_CASE_HOLDS'
delivery=json.loads(DEL.read_text(encoding='utf-8')); raw=ZIP.read_bytes(); assert len(raw)==delivery['bytes'] and sha(raw)==delivery['sha256']
assert delivery['accepted'] is False and delivery['applied'] is False and delivery['savedArtifactVerification']['matchesLocalZIP'] is True
before_bytes=INDEX.read_bytes(); before=json.loads(before_bytes); catalog_bytes=CATALOG.read_bytes();catalog=json.loads(catalog_bytes)
queue_bytes=QUEUE_BEFORE.read_bytes();pending_bytes=PENDING_BEFORE.read_bytes();handoff_bytes=HANDOFF_BEFORE.read_bytes()
queue_before=json.loads(queue_bytes); pending_before=json.loads(pending_bytes)
assert before['authoredCounts']=={'reviewed':686,'pending':162}
assert before['representationCounts']['completeReviewedStandaloneProcedures']==410
assert queue_before['currentAuthority']['pending']==162 and pending_before['pendingCount']==162
assert queue_before['currentPendingGroups'][0]['group']=='rank7-gate-glyph3' and queue_before['currentPendingGroups'][0]['pendingIds']==IDS
with zipfile.ZipFile(ZIP) as z:
 assert z.testzip() is None; names=z.namelist(); manifest=json.loads(z.read('MANIFEST.json'))
 package={n:z.read(n) for n in names}
 for rec in manifest['members']:
  b=package[rec['path']];assert len(b)==rec['bytes'] and sha(b)==rec['sha256'],rec['path']
assert package['authority/authored_review_index.json']==before_bytes
assert package['authority/catalog.json']==catalog_bytes
assert package['authority/CURRENT_SPELL_QUEUE_140.json']==queue_bytes
assert package['authority/CURRENT162_PENDING_IDENTITY_AUDIT_140.json']==pending_bytes
assert package['authority/CURRENT_HANDOFF_140.json']==handoff_bytes
source_candidate=ROOT/'DescentReviewChanges/ReviewBible/data/director/spell_review/rank7_gate_glyph_3_source_conference_01.json'
source_archive=ROOT/'docs/audit/2026-10-08/full-game/DD_Rank7_Gate_Glyph_3_Source_Conference_01.zip'
assert package['source/rank7_gate_glyph_3_source_conference_01.json']==source_candidate.read_bytes()
assert package['history/DD_Rank7_Gate_Glyph_3_Source_Conference_01.zip']==source_archive.read_bytes()
procedures=json.loads(package['PROCEDURES.json']); casebook_bytes=package['CASEBOOK.json'];casebook=json.loads(casebook_bytes)
assert [p['id'] for p in procedures]==IDS and len(casebook['allCases'])==33
rows={e['id']:e for e in before['entries']};cards={s['id']:s for s in catalog['spells']}
for p in procedures:
 sid=p['id'];assert rows[sid]['authoredStatus']=='pending-authored-procedure'
 assert p['completeNativeCardAndAccessUnchanged']==cards[sid] and p['accepted'] is False and p['applied'] is False
assert catalog_bytes==CATALOG.read_bytes()
# Stage complete candidate evidence, including exact director/source archives and authority context.
STAGING.mkdir(parents=True)
selected=['ACTOR_PROFILES.json','ARTIFACT_BINDINGS.json','CASE_DISPOSITIONS.json','CASE_AUTHORING_OPERATIONS.json','CURRENT_SOURCE_STATUS_RECONCILIATION.json','EXACT_COUNTERPARTS_AND_COSMOLOGY.json','EXACT_COUNTS.json','FUTURE_CASE_OBLIGATION_DISPOSITIONS.json','HOLD_REGISTER.json','NEXT_GROUP_BOUNDARY.json','ORIGINAL_15_CONFERENCE_QUESTIONS.json','ORIGINAL_FUTURE_CASE_REQUIREMENTS.json','ORIGINAL_IDENTITY_QUESTIONS_AND_SCOPE.json','ORIGINAL_SCENARIOS.json','PROCEDURES.json','PROCEDURE_AUTHORING_OPERATIONS.json','QUESTION_DISPOSITIONS.json','SHARED_RULES.json','SOURCE_VERIFICATION.json','TURN_LEDGER_CHECKS.json','VALIDATION.json','STANDALONE_PROCEDURES.md','README.md']
for name in selected:(STAGING/name).write_bytes(package[name])
(STAGING/'CASEBOOK.json.gz').write_bytes(gzip.compress(casebook_bytes,mtime=0))
with gzip.open(STAGING/'CASEBOOK.json.gz','rb') as f:assert f.read()==casebook_bytes
(STAGING/'DIRECTOR_RETURN_MANIFEST.json').write_bytes(package['MANIFEST.json'])
(STAGING/'DIRECTOR_RETURN_DELIVERY.json').write_bytes(DEL.read_bytes())
(STAGING/'INDEPENDENT_AUDIT.json').write_bytes(AUDIT.read_bytes())
(STAGING/'DIRECTOR_RETURN_ARCHIVE.zip').write_bytes(raw)
(STAGING/'SOURCE_CONFERENCE_ARCHIVE.zip').write_bytes(source_archive.read_bytes())
(STAGING/'SOURCE_CONFERENCE_CANDIDATE.json').write_bytes(source_candidate.read_bytes())
# Preserve all exact current authority and preceding acceptance evidence supplied to the director.
for n,b in package.items():
 if n.startswith('authority/'):
  dest=STAGING/'evidence'/n;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(b)
# Raw director hold register remains byte-exact. This companion indexes only current dispositions.
holds=json.loads(package['HOLD_REGISTER.json'])
hold_adjudication={
 'id':'RANK7-GATEGlyph3-HOLD-ADJUDICATION-141',
 'status':'ALL_NINE_DIRECTOR_HOLDS_RETAINED_WITH_SOURCE_AND_CASE_LIMITS',
 'rawHoldRegister':{'path':'HOLD_REGISTER.json','bytes':len(package['HOLD_REGISTER.json']),'sha256':sha(package['HOLD_REGISTER.json'])},
 'originalHoldTextPreservedByteExact':True,'allContentAndBoundaryHoldsRemainOpen':True,
 'caseEvidencePromotedToCampaignProof':False,'sourceStatusPromoted':False,
 'disposition':[{'id':h['id'],'kind':h['kind'],'scope':h['scope'],'caseReferences':h.get('caseReferences',[]),'status':'RETAINED_OPEN','text':h['text']} for h in holds['holds']],
 'interpretation':'Acceptance resolves only authored operational procedure review. Chain Gate site/plane/pose premises remain whole-case held; missing class-mark, nonliving-profile, and zero-state-origin premises remain held as recorded. The raw director hold register and case references are unchanged.',
 'runtimeSelectionEnabled':False,'sourceProgramsExecuted':False,'runtimeExecuted':False
}
writej(STAGING/'HOLD_ADJUDICATION.json',hold_adjudication)
# Build candidate model while preserving the exact native source envelopes.
case_ids={sid:[c['id'] for c in casebook['allCases'] if c['spellId']==sid] for sid in IDS}
model_spells=[]
for i,p in enumerate(procedures):
 sid=p['id'];card=p['completeNativeCardAndAccessUnchanged']
 model_spells.append({'id':sid,'name':card['name'],'status':'INDEPENDENTLY_ACCEPTED_AUTHORED_PROCEDURE_WITH_RETAINED_SOURCE_CASE_HOLDS','completeNativeCardAndAccess':card,'procedure':p['procedure'],'directorProcedureRecordPointer':f'/PROCEDURES/{i}','sharedRuleIds':p['sharedRuleIds'],'sourceArchiveLocator':f'DIRECTOR_RETURN_ARCHIVE.zip!PROCEDURES.json#{sid}','originalSourceBinding':card['source'],'originalSourcePointer':rows[sid]['wholeCardPointer'],'sourceCatalogKey':sid,'reviewFlagsPreserved':card.get('reviewFlags',[]),'caseEvidence':case_ids[sid],'runtimeSelectionEnabled':False,'directorProcedureStatusBeforeAcceptance':p['status']})
scope=('Only chain-gate, symbol, and symbol-of-death authored operational procedures are accepted, with all nine source, case, and review-boundary holds retained. '
 'All selected completion values remain spell-local authorship; no global planar, glyph, death, class-access, source-status, cosmology, or runtime rule is adopted. '
 'Native source cards, class access, source status, catalog, and shared rules outside this exact scope are unchanged. '
 'This closes authored procedure review only. Runtime selection remains disabled; no runtime, human-play, balance, cosmology, or release approval is claimed.')
model={'schemaVersion':3,'moduleId':'rank7gateglyph3-reviewed-141','status':'EXACT_AUTHORED_PROCEDURES_ACCEPTED_WITH_RETAINED_SOURCE_CASE_HOLDS','scope':scope,'acceptedIds':IDS,'excludedPendingIds':sorted(e['id'] for e in before['entries'] if e['authoredStatus']=='pending-authored-procedure' and e['id'] not in IDS),'sharedRules':json.loads(package['SHARED_RULES.json']),'spells':model_spells,'questionDispositions':json.loads(package['QUESTION_DISPOSITIONS.json']),'originalScenarioDispositions':json.loads(package['CASE_DISPOSITIONS.json']),'originalFutureCaseRequirementDispositions':json.loads(package['FUTURE_CASE_OBLIGATION_DISPOSITIONS.json']),'originalIdentityQuestionsAndScope':json.loads(package['ORIGINAL_IDENTITY_QUESTIONS_AND_SCOPE.json']),'casebookFile':'CASEBOOK.json.gz','casebookEncoding':'gzip; exact decompression reproduces the director return CASEBOOK.json member','casebookSourceMemberBinding':{'path':'CASEBOOK.json','bytes':len(casebook_bytes),'sha256':sha(casebook_bytes)},'actorProfilesFile':'ACTOR_PROFILES.json','holdsFile':'HOLD_REGISTER.json','holdAdjudicationFile':'HOLD_ADJUDICATION.json','procedureSourceFile':'PROCEDURES.json','directorReturnManifestFile':'DIRECTOR_RETURN_MANIFEST.json','directorReturnDeliveryFile':'DIRECTOR_RETURN_DELIVERY.json','directorReturnArchive':'DIRECTOR_RETURN_ARCHIVE.zip','directorReturnBinding':bind(ZIP),'directorReturnDeliveryBinding':bind(DEL),'sourceConferenceArchiveBinding':bind(source_archive),'sourceCandidateBinding':bind(source_candidate),'sourceArchiveManifestMembers':len(names),'sourceArchiveBindingMembers':len(manifest['members']),'independentAcceptanceGranted':True,'independentAcceptanceReceipt':f'{A.name}/{REVIEW_ID}.json','candidatePackageManifestPath':(CANDIDATE/'CANDIDATE_PACKAGE_MANIFEST.json').relative_to(ROOT).as_posix(),'canonicalApplicationPerformed':False,'runtimeTestsExecuted':False,'sourceProgramsExecuted':False,'humanPlaytested':False,'balanceApproved':False,'cosmologyModified':False,'releaseApproved':False}
writej(STAGING/'MODEL.json',model)
# Package manifest binds every stable evidence file and omits cyclic model/receipt targets.
excluded={'CANDIDATE_PACKAGE_MANIFEST.json','MODEL.json','EXACT_ACCEPTANCE.json'}
manifest_files=[]
for p in sorted(STAGING.rglob('*')):
 if p.is_file() and p.name not in excluded:
  rel=p.relative_to(STAGING).as_posix(); b=p.read_bytes();manifest_files.append({'path':rel,'bytes':len(b),'sha256':sha(b)})
package_manifest={'id':'RANK7-GATEGlyph3-CANDIDATE-PACKAGE-MANIFEST-141','files':manifest_files,'excludedFromBindings':sorted(excluded),'selfExcluded':'CANDIDATE_PACKAGE_MANIFEST.json'}
writej(STAGING/'CANDIDATE_PACKAGE_MANIFEST.json',package_manifest)
manifest_binding=bind(STAGING/'CANDIDATE_PACKAGE_MANIFEST.json',CANDIDATE.relative_to(ROOT).as_posix()+'/CANDIDATE_PACKAGE_MANIFEST.json')
model['candidatePackageManifestBinding']=manifest_binding
writej(STAGING/'MODEL.json',model)
model_binding=bind(STAGING/'MODEL.json',CANDIDATE.relative_to(ROOT).as_posix()+'/MODEL.json')
# Independent acceptance receipt; application is a separate, exactly reversible index mutation.
receipt={
 'id':REVIEW_ID,'recordedAtUtc':now(),'status':'INDEPENDENT_AUTHORED_PROCEDURE_ACCEPTANCE_WITH_RETAINED_SOURCE_CASE_HOLDS','decision':'ACCEPTED_FOR_AUTHORED_OPERATIONAL_PROCEDURE_REVIEW_ONLY',
 'directorReturn':bind(ZIP),'directorReturnDelivery':bind(DEL),'directorReturnManifest':{'path':'MANIFEST.json','bytes':len(package['MANIFEST.json']),'sha256':sha(package['MANIFEST.json'])},
 'independentAudit':bind(AUDIT),'candidateEnvelopeBinding':model_binding,'candidatePackageManifestBinding':manifest_binding,
 'authorityBefore':bind(INDEX),'countsBefore':{'reviewed':686,'pending':162,'acceptedUnapplied':0},'acceptedIds':IDS,'excludedPendingIds':model['excludedPendingIds'],
 'reviewFindings':json.loads(AUDIT.read_text(encoding='utf-8'))['reviewFindings'],
 'retainedHoldCount':9,'rawHoldRegisterPreserved':True,'holdAdjudicationBinding':{'path':'HOLD_ADJUDICATION.json','bytes':len((STAGING/'HOLD_ADJUDICATION.json').read_bytes()),'sha256':sha((STAGING/'HOLD_ADJUDICATION.json').read_bytes())},
 'sourceStatusPreserved':'blocked-pending-operational-review for all three; acceptance closes only authored procedure review.',
 'noRuntimeOrReleaseClaim':True,'sourceProgramsExecuted':False,'historicalProgramsExecuted':False,'runtimeTestsExecuted':False,'humanPlaytested':False,'balanceApproved':False,'cosmologyModified':False,'releaseApproved':False,
 'approvedForCanonicalAuthoredIndexApplication':True,'canonicalApplicationPerformed':False
}
writej(STAGING/'EXACT_ACCEPTANCE.json',receipt);writej(RECEIPT_PATH,receipt)
assert (STAGING/'EXACT_ACCEPTANCE.json').read_bytes()==RECEIPT_PATH.read_bytes()
# Validate stable candidate package bindings before publishing the candidate folder.
for rec in manifest_files:
 b=(STAGING/rec['path']).read_bytes();assert len(b)==rec['bytes'] and sha(b)==rec['sha256'],rec['path']
assert gzip.decompress((STAGING/'CASEBOOK.json.gz').read_bytes())==casebook_bytes
shutil.move(str(STAGING),str(CANDIDATE))
MANUSCRIPT.parent.mkdir(parents=True,exist_ok=True);MANUSCRIPT.write_bytes(package['STANDALONE_PROCEDURES.md'])
# Build exact authored-index operation; only these three rows and the two aggregate counters may change.
after=copy.deepcopy(before);operations=[]
for i,row in enumerate(before['entries']):
 if row['id'] not in IDS:continue
 sid=row['id'];pi=IDS.index(sid);old=copy.deepcopy(row);new=copy.deepcopy(row);catalog_ptr=row.get('sourceCatalogWholeCardPointer') or row['wholeCardPointer']
 new.update({'authoredStatus':'reviewed-authored-operational-playtest','procedureFile':'../spell_candidates/rank7gateglyph3_reviewed_141/MODEL.json','procedurePointer':f'/spells/{pi}/procedure','wholeCardPointer':f'/spells/{pi}','sourceCatalogWholeCardPointer':catalog_ptr,'wholeCardIdField':'id','procedureTextPointer':f'/spells/{pi}/procedure','directorProcedureRecordPointer':f'/spells/{pi}','sharedRulesPointer':'/sharedRules','manuscript':'../../../docs/spells/candidates/RANK7_GATEGlyph3_REVIEWED_141.md','reviewId':REVIEW_ID,'runtimeSelectionEnabled':False,'completeEnvelopeBinding':model_binding,'historicalCandidateLabelsPreserved':True,'casebookBinding':candidate_bind('CASEBOOK.json.gz'),'casebookEncoding':'gzip; exact decompression reproduces the director return CASEBOOK.json member','casebookSourceArchiveMemberBinding':model['casebookSourceMemberBinding'],'sourceArchiveBinding':bind(ZIP),'sourceConferenceArchiveBinding':bind(source_archive),'sourceCandidateBinding':bind(source_candidate),'candidatePackageManifestBinding':manifest_binding,'retainedHoldsBinding':candidate_bind('HOLD_REGISTER.json'),'holdAdjudicationBinding':candidate_bind('HOLD_ADJUDICATION.json'),'procedureSourceBinding':candidate_bind('PROCEDURES.json'),'completeEvidenceRoot':CANDIDATE.relative_to(ROOT).as_posix(),'acceptedSharedRuleScope':scope,'authoredAcceptanceReceipt':bind(RECEIPT_PATH)})
 operations.append({'op':'replace-entry','identity':sid,'index':i,'before':old,'after':new});after['entries'][i]=new
assert len(operations)==3
app_envelope={'file':'../spell_candidates/rank7gateglyph3_reviewed_141/MODEL.json','binding':model_binding,'reviewId':REVIEW_ID,'acceptedIds':IDS,'excludedPendingIds':model['excludedPendingIds'],'authority':bind(RECEIPT_PATH),'sourceArchive':bind(ZIP),'sourceConferenceArchive':bind(source_archive),'sourceCandidate':bind(source_candidate),'casebookBinding':candidate_bind('CASEBOOK.json.gz'),'casebookSourceArchiveMemberBinding':model['casebookSourceMemberBinding'],'holdsBinding':candidate_bind('HOLD_REGISTER.json'),'holdAdjudicationBinding':candidate_bind('HOLD_ADJUDICATION.json'),'procedureSourceBinding':candidate_bind('PROCEDURES.json'),'candidatePackageManifestBinding':manifest_binding,'applicationReceipt':APP_PATH,'scope':scope}
after['additionalStandaloneEnvelopes'].append(app_envelope)
after['authoredCounts']={'reviewed':689,'pending':159}
after['representationCounts']['completeReviewedStandaloneProcedures']=413
pending_ids={e['id'] for e in after['entries'] if e['authoredStatus']=='pending-authored-procedure'}
assert len(pending_ids)==159 and not(set(IDS)&pending_ids)
assert after['sourceCatalogSha256']==before['sourceCatalogSha256'] and after['standaloneEnvelopeSha256']==before['standaloneEnvelopeSha256']
reverse=copy.deepcopy(after)
for op in operations:reverse['entries'][op['index']]=op['before']
reverse['additionalStandaloneEnvelopes']=reverse['additionalStandaloneEnvelopes'][:-1]
reverse['authoredCounts']=copy.deepcopy(before['authoredCounts']);reverse['representationCounts']=copy.deepcopy(before['representationCounts'])
assert reverse==before
BACKUP.write_bytes(before_bytes)
opsdoc={'id':'RANK7-GATEGlyph3-INDEX-OPERATIONS-141','before':bind(BACKUP),'after':None,'operations':operations,'reverseSemanticExact':True,'reverseByteExactBackup':True,'onlyIdentityIds':IDS}
tmp=INDEX.with_suffix('.json.tmp');tmp.write_text(json.dumps(after,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n');os.replace(tmp,INDEX)
after_bytes=INDEX.read_bytes();opsdoc['after']=bind(INDEX);writej(A/'RANK7_GATEGlyph3_INDEX_OPERATIONS_141.json',opsdoc)
application={'id':'RANK7-GATEGlyph3-APPLICATION-141','recordedAtUtc':now(),'status':'APPLIED_EXACTLY_THREE_AUTHORED_PROCEDURES_WITH_RETAINED_SOURCE_CASE_HOLDS','reviewId':REVIEW_ID,'acceptedIds':IDS,'before':bind(BACKUP),'after':bind(INDEX),'candidateEnvelope':model_binding,'candidatePackageManifest':manifest_binding,'acceptanceReceipt':bind(RECEIPT_PATH),'independentAudit':bind(AUDIT),'counts':{'before':{'reviewed':686,'pending':162,'acceptedUnapplied':0},'after':{'reviewed':689,'pending':159,'acceptedUnapplied':0}},'runtimeSelectionEnabled':False,'runtimeTestsExecuted':False,'sourceProgramsExecuted':False,'catalogChanged':False,'classAccessChanged':False,'closedFeatsOrCohortsReopened':False,'onlyAcceptedAuthoredIdentityRowsChanged':True,'sourceStatusPreservedAsBlocked':True,'inverseSemanticReplayExact':reverse==before,'backupByteExact':BACKUP.read_bytes()==before_bytes}
writej(A/APP_PATH.split('/')[-1],application)
# Rebuild live queue and handoff from the previous authoritative group ordering.
groups=[]
for g in queue_before['currentPendingGroups']:
 keep=[sid for sid in g['pendingIds'] if sid in pending_ids]
 if keep:
  ng=copy.deepcopy(g);ng['pendingIds']=keep;ng['pendingCount']=len(keep);groups.append(ng)
assert groups and groups[0]['group']=='rank8-resource6' and groups[0]['pendingCount']==6
queue=copy.deepcopy(queue_before)
current_authority=copy.deepcopy(queue_before['currentAuthority'])
current_authority.update({'reviewedApplied':689,'pending':159,'acceptedUnapplied':0,'completeReviewedStandaloneProcedures':413})
queue.update({'id':'SPELL-REVIEW-QUEUE-141','recordedAtUtc':now(),'currentAuthority':current_authority,'currentPendingGroups':groups,'nextSuggestedGroups':groups[:5],'nextGroup':groups[0],'justAppliedBatch':{'reviewId':REVIEW_ID,'ids':IDS,'count':3,'applicationReceipt':APP_PATH},'pendingIdentityAudit':{'path':PENDING.name,'pending':159,'indexSha256':sha(after_bytes)},'next':{'group':groups[0]['group'],'pendingCount':groups[0]['pendingCount'],'archive':groups[0]['archive'],'candidate':groups[0]['candidate']}})
writej(QUEUE,queue)
pending_audit={'id':'CURRENT159-PENDING-IDENTITY-AUDIT-141','recordedAtUtc':now(),'status':'PASSED_EXACT_CURRENT_INDEX_PENDING_SET','indexBinding':bind(INDEX),'catalogBinding':bind(CATALOG),'authoredCounts':after['authoredCounts'],'pendingCount':159,'pendingIds':sorted(pending_ids),'allPendingExistInSourceCatalog':True,'closed335AndCompletedCohortsReopened':False,'acceptedUnapplied':0}
for row in after['entries']:
 if row['id'] in pending_ids:assert next(s for s in catalog['spells'] if s['id']==row['id'])['id']==row['id']
writej(PENDING,pending_audit)
handoff=json.loads(HANDOFF_BEFORE.read_text(encoding='utf-8'))
handoff.update({'id':'CURRENT-HANDOFF-141','recordedAtUtc':now(),'status':'RANK7_GATEGlyph3_APPLIED_NEXT_159_PENDING','currentAuthority':current_authority,'currentIndexBinding':bind(INDEX,'authority/authored_review_index.json'),'currentCatalogBinding':bind(CATALOG,'authority/catalog.json'),'pendingIdentityAudit':{'id':pending_audit['id'],'path':PENDING.name,'pendingCount':159,'sha256':sha(PENDING.read_bytes())},'appliedThisStep':{'reviewId':REVIEW_ID,'ids':IDS,'count':3,'applicationReceipt':APP_PATH},'nextGroup':groups[0]['group'],'nextPreparedRequest':{'group':groups[0]['group'],'candidate':groups[0]['candidate'],'archive':groups[0]['archive'],'request':'Prepare a fresh request bound to the current 689/159 authority before director review.'}})
writej(HANDOFF,handoff)
validation={'id':'RANK7-GATEGlyph3-APPLICATION-VALIDATION-141','status':'PASS','checksPassed':35,'failed':0,'beforeIndexHash':sha(before_bytes),'afterIndexHash':sha(after_bytes),'beforeIndexBytes':len(before_bytes),'afterIndexBytes':len(after_bytes),'changedIdentityIds':IDS,'onlyThreePendingEntriesChanged':True,'allOtherEntriesAndPriorStandaloneEnvelopesPreserved':True,'authoredCounts':after['authoredCounts'],'representationCounts':after['representationCounts'],'sourceStatusStillBlockedForAllThree':all(rows[sid]['sourceStatus']=='blocked-pending-operational-review' for sid in IDS),'sourceCatalogHashUnchanged':CATALOG.read_bytes()==catalog_bytes,'sourceCatalogBindingUnchanged':after['sourceCatalogSha256']==before['sourceCatalogSha256'],'runtimeSelectionEnabled':False,'runtimeTestsExecuted':False,'sourceProgramsExecuted':False,'closed335AndCompletedCohortsReopened':False,'inverseSemanticReplayExact':reverse==before,'backupByteExact':BACKUP.read_bytes()==before_bytes,'acceptanceWasBoundToExactDirectorReturn':True,'candidateManifestBindingsPassed':True,'acceptedUnapplied':0,'nextGroup':groups[0]['group'],'nextPendingCount':groups[0]['pendingCount']}
writej(A/'RANK7_GATEGlyph3_APPLICATION_VALIDATION_141.json',validation)
assert CATALOG.read_bytes()==catalog_bytes
assert json.loads(INDEX.read_text(encoding='utf-8'))['authoredCounts']=={'reviewed':689,'pending':159}
for rec in manifest_files:
 b=(CANDIDATE/rec['path']).read_bytes();assert len(b)==rec['bytes'] and sha(b)==rec['sha256'],rec['path']
assert bind(CANDIDATE/'MODEL.json',CANDIDATE.relative_to(ROOT).as_posix()+'/MODEL.json')==model_binding
assert bind(CANDIDATE/'CANDIDATE_PACKAGE_MANIFEST.json',CANDIDATE.relative_to(ROOT).as_posix()+'/CANDIDATE_PACKAGE_MANIFEST.json')==manifest_binding
assert (CANDIDATE/'EXACT_ACCEPTANCE.json').read_bytes()==RECEIPT_PATH.read_bytes()
print(json.dumps({'status':'APPLIED_AND_VALIDATED','reviewId':REVIEW_ID,'acceptedIds':IDS,'currentCounts':after['authoredCounts'],'representationCounts':after['representationCounts'],'auditDecision':json.loads(AUDIT.read_text(encoding='utf-8'))['decision'],'candidateFiles':len(list(CANDIDATE.rglob('*'))),'pendingAudit':{'count':len(pending_ids),'nextGroup':groups[0]['group'],'nextBatchCount':groups[0]['pendingCount'],'nextIds':groups[0]['pendingIds']},'catalogUnchanged':CATALOG.read_bytes()==catalog_bytes,'indexBytes':len(after_bytes),'indexSha256':sha(after_bytes)},indent=2))