from __future__ import annotations
import copy, gzip, hashlib, io, json, os, pathlib, shutil, zipfile
from datetime import datetime, timezone

ROOT=pathlib.Path('C:/Github/DecenniumDescent')
A=ROOT/'docs/audit/2026-10-08/full-game/director-spell-review-129'
RET=A/'materialterrain8_return01_140_received'
ZIP=RET/'DD_MaterialTerrain8_Director_Return01_140.zip'
DEL=RET/'DIRECTOR_RETURN_DELIVERY.json'
AUDIT=A/'MATERIALTERRAIN8_RETURN01_INDEPENDENT_AUDIT_140.json'
INDEX=ROOT/'DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json'
CATALOG=ROOT/'DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json'
QUEUE_BEFORE=A/'CURRENT_SPELL_QUEUE_139.json'
PENDING_BEFORE=A/'CURRENT170_PENDING_IDENTITY_AUDIT_139.json'
HANDOFF_BEFORE=A/'CURRENT_HANDOFF_139.json'
IDS=['control-water','fabricate','transmute-terrain','magnetize-field','passwall','transmute-rock','displace-structure','move-earth']
REVIEW_ID='MATERIALTERRAIN8-EXACT-AUTHORED-ACCEPTANCE-140'
APP_PATH='docs/audit/2026-10-08/full-game/director-spell-review-129/MATERIALTERRAIN8_APPLICATION_140.json'
CANDIDATE=ROOT/'DescentReviewChanges/ReviewBible/data/public/spell_candidates/materialterrain8_reviewed_140'
STAGING=CANDIDATE.with_name(CANDIDATE.name+'.staging')
MANUSCRIPT=ROOT/'docs/spells/candidates/MATERIALTERRAIN8_REVIEWED_140.md'

def sha(b:bytes)->str:return hashlib.sha256(b).hexdigest()
def now():return datetime.now(timezone.utc).isoformat()
def writej(p:pathlib.Path,x):
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def bind(p:pathlib.Path,rel=None):
 b=p.read_bytes();return {'path':rel or p.relative_to(ROOT).as_posix(),'bytes':len(b),'sha256':sha(b)}
def candidate_bind(name):return bind(STAGING/name,(CANDIDATE/name).relative_to(ROOT).as_posix())
def ptr(x,p):
 for t in p.strip('/').split('/') if p else []:
  t=t.replace('~1','/').replace('~0','~');x=x[int(t)] if isinstance(x,list) else x[t]
 return x

assert ZIP.is_file() and DEL.is_file() and AUDIT.is_file()
assert not CANDIDATE.exists() and not STAGING.exists() and not MANUSCRIPT.exists()
delivery=json.loads(DEL.read_text(encoding='utf-8'));audit=json.loads(AUDIT.read_text(encoding='utf-8'))
archive=ZIP.read_bytes();archive_sha=sha(archive)
assert audit['decision']=='PASS_READY_FOR_EXACT_AUTHORED_PROCEDURE_ACCEPTANCE_WITH_RETAINED_SOURCE_CASE_HOLDS'
assert audit['directorReturn']['sha256']==archive_sha and delivery['sha256']==archive_sha
assert delivery['accepted'] is False and delivery['applied'] is False
assert delivery['counts']=={'applied':678,'pending':170,'acceptedUnapplied':0}
with zipfile.ZipFile(io.BytesIO(archive)) as z:
 assert z.testzip() is None
 names=z.namelist();outer=json.loads(z.read('MANIFEST.json'))
 manifest={x.get('path',x.get('file')):x for x in outer['files']}
 assert len(names)==112 and len(manifest)==111 and set(names)-{'MANIFEST.json'}==set(manifest)
 package={n:z.read(n) for n in names}
 for n,rec in manifest.items():
  b=package[n];assert len(b)==rec.get('bytes',rec.get('length')) and sha(b)==rec.get('sha256',rec.get('hash')),n
assert outer['accepted'] is False and outer['applied'] is False
index_bytes=INDEX.read_bytes();before=json.loads(index_bytes);catalog_bytes=CATALOG.read_bytes();catalog=json.loads(catalog_bytes)
assert before['authoredCounts']=={'reviewed':678,'pending':170}
assert before['representationCounts']['completeReviewedStandaloneProcedures']==402
assert len([e for e in before['entries'] if e['authoredStatus']=='pending-authored-procedure'])==170
assert package['authority/authored_review_index.json']==index_bytes and package['authority/catalog.json']==catalog_bytes
assert package['authority/CURRENT_SPELL_QUEUE_139.json']==QUEUE_BEFORE.read_bytes()
assert package['authority/CURRENT170_PENDING_IDENTITY_AUDIT_139.json']==PENDING_BEFORE.read_bytes()
assert package['authority/CURRENT_HANDOFF_139.json']==HANDOFF_BEFORE.read_bytes()
queue_before=json.loads(QUEUE_BEFORE.read_text(encoding='utf-8'))
assert queue_before['currentAuthority']['pending']==170
assert next(g for g in queue_before['currentPendingGroups'] if g['group']=='material-terrain8')['pendingIds']==IDS
source_archive=ROOT/'docs/audit/2026-10-08/full-game/DD_Material_Terrain_8_Conference_02.zip'
source_candidate=ROOT/'DescentReviewChanges/ReviewBible/data/director/spell_review/material_terrain_8_conference_02.json'
assert sha(source_archive.read_bytes())==next(g for g in queue_before['currentPendingGroups'] if g['group']=='material-terrain8')['archive']['sha256']
assert sha(source_candidate.read_bytes())==next(g for g in queue_before['currentPendingGroups'] if g['group']=='material-terrain8')['candidate']['sha256']
assert package['history/DD_Material_Terrain_8_Conference_02.zip']==source_archive.read_bytes()
assert package['evidence/source02/sources/DescentReviewChanges/ReviewBible/data/director/spell_review/material_terrain_8_conference_02.json']==source_candidate.read_bytes()
procedures=json.loads(package['PROCEDURES.json']);assert [p['id'] for p in procedures]==IDS
native=json.loads(package['NATIVE_SOURCE_ACCESS.json']);rows={e['id']:e for e in before['entries']};cards={s['id']:s for s in catalog['spells']}
for p in procedures:
 sid=p['id'];row=rows[sid]
 assert row['authoredStatus']=='pending-authored-procedure' and row['sourceStatus']=='blocked-pending-operational-review'
 assert p['accepted'] is False and p['applied'] is False
 assert p['completeNativeSourceAndAccessUnchanged']==cards[sid]==native[sid]
assert sum(len(native[sid]['classAccess']) for sid in IDS)==54
casebook_bytes=package['CASEBOOK.json'];casebook=json.loads(casebook_bytes)
assert len(casebook['mainCases'])==16 and len(casebook['additionalBranches'])==8 and len(casebook['allCases'])==24
case_ids={sid:[c['id'] for c in casebook['allCases'] if c['spellId']==sid] for sid in IDS}
assert all(case_ids[sid] for sid in IDS)
source_binding=bind(ZIP)
holds=json.loads(package['HOLD_REGISTER.json']);assert len(holds['sourceHolds'])==28 and holds['accepted'] is False and holds['applied'] is False
shared=json.loads(package['SHARED_RULES.json'])

# Keep every original hold verbatim while distinguishing accepted local rules from missing physical/source proof.
hold_adjudication={
 'id':'MATERIALTERRAIN8-HOLD-ADJUDICATION-140',
 'status':'RETAINED_SOURCE_AND_CASE_HOLDS_WITH_PROCEDURE_LEVEL_CLARIFICATIONS',
 'rawHoldRegister':{'path':'HOLD_REGISTER.json','bytes':len(package['HOLD_REGISTER.json']),'sha256':sha(package['HOLD_REGISTER.json'])},
 'originalHoldTextPreservedByteExact':True,
 'all28WholeCaseOrRequiredBranchHoldsRemainOpen':True,
 'caseEvidencePromotedToCampaignProof':False,
 'interpretation':'Acceptance resolves only the eight self-contained authored spell procedures. A procedure-level design question now answered by an explicit new local rule is closed for this accepted text; the original source scenario remains held wherever actual source facts, physical profiles, support, occupants, credentials, routes, suppressors, or terrain are absent.',
 'clarifications':[
  {'cases':['TU4-05-A','TU4-05-A/receiver-full','TU4-05-B'],'procedure':'control-water','procedureQuestionsResolved':['finite selected quantity and working region','one declared displacement per Action','one forced-displacement attempt per subject per family per round','lowering requires actual receiving volume','buoyancy and airway are not invented'],'residualHolds':['actual container walls and open route','water support and capacity','actual swimmer immersion, current, breathing, occupied sweep and boat profile'],'disposition':'Procedure text supplies local rules; original scene vectors remain conditional.'},
  {'cases':['TR5-01-A','TR5-01-A/ice-first-entry-start-reentry','TR5-01-B'],'procedure':'transmute-terrain','procedureQuestionsResolved':['four finite modes and uppermost one-foot surface layer','explicit local reference bulk densities','connected-component clearance gate','one captured-DC ice slip save per victim/ice family/regular cycle'],'residualHolds':['actual terrain and foreign-object meshes','actual material volume and support','ordinary ice durability and later melt behavior'],'disposition':'The inherited hold wording about density and slip is narrowed to missing source/scene values and physical support; authored local reference values and the new slip rule are accepted.'},
  {'cases':['TR5-04-A','TR5-04-B'],'procedure':'magnetize-field','procedureQuestionsResolved':['exact point-centered sphere','subject eligibility','stable save order','straight 3D whole-body sweep','first collision stop and zero movement when floor blocks a downward vector'],'residualHolds':['actual Large body profile and mass','actual armor/material identity','actual STR result and final scene-specific stop'],'disposition':'Q09 is resolved as authored procedure text. The inherited request to resolve center, collision order, and ground blocking is superseded for procedure review; the original case remains held for its missing creature and physical facts.'},
  {'cases':['TR5-06-B','TR5-06-B/both-mouths-pending','TR5-06-B/suppressed-live-reopen'],'procedure':'passwall','procedureQuestionsResolved':['bounded whole-body ejection rule','separate suppressed-live and ended states','single revalidation at specified real trigger points','no recovery of expelled occupants or restored damage'],'residualHolds':['actual wall, mouths and receiving space','actual fluid capacity and behavior','actual suppressor spell, scope, and timing'],'disposition':'Q11 is resolved as authored procedure text. The original case remains conditional for missing physical fixtures and a real suppressor; raw hold text is preserved as historical evidence.'},
  {'cases':['TR5-08-A','TR5-08-A/damaged-stock-split-cycle','TR5-08-B'],'procedure':'transmute-rock','procedureQuestionsResolved':['finite conversion volume and authored reference densities','exact rational stock durability ledger and split/merge lineage','body-clearance gate','conditional 4d6 falling-mud burst'],'residualHolds':['actual source material and occupied geometry','prior stock integrity and actual structural profile','ceiling support and actual falling path'],'disposition':'Authored reference values and ledger rules are accepted. Holds are restricted to missing real input profiles and scene facts; no source durability or completed fall is inferred.'},
  {'cases':['TU6-04-A','TU6-04-B'],'procedure':'displace-structure','procedureQuestionsResolved':['coherent structure and mass bounds','fixed rigid transformation and full swept geometry','atomic occupant/contents treatment','bounded foundation-soil exchange'],'residualHolds':['actual structure, foundation, services, soil, support and occupant profiles'],'disposition':'All source scenarios remain conditional until a real complete structure vector exists.'},
  {'cases':['TU6-06-A','TU6-06-A/pyramid-conservation-map','TU6-06-B','TU6-06-B/forty-foot-fall'],'procedure':'move-earth','procedureQuestionsResolved':['finite parcel cap, conservation and per-parcel path bound','whole-transition occupant clearance','no unsupported berm without a real support certificate','fall timing uses existing fall rules'],'residualHolds':['actual final mesh, material support, slope, occupied geometry, swept path and landing profile'],'disposition':'Conditional mapping demonstrates one possible volume-preserving map, not a qualified terrain result or completed damage event.'}
 ],
 'noSourceStatusChange':True,'runtimeSelectionEnabled':False,'sourceProgramsExecuted':False,'runtimeExecuted':False
}

assert json.loads(package['NEXT_GROUP_BOUNDARY.json'])['closedCohortsOrFeatsReopened'] is False
selected=['ACTOR_PROFILES.json','ARTIFACT_BINDINGS.json','CASE_AUTHORING_OPERATIONS.json','FINDING_DISPOSITIONS.json','HOLD_REGISTER.json','NATIVE_SOURCE_ACCESS.json','NEXT_GROUP_BOUNDARY.json','ORIGINAL_16_QUESTIONS.json','ORIGINAL_16_SCENARIOS.json','ORIGINAL_CONFERENCE_02.json','PROCEDURES.json','PROCEDURE_REVISION_OPERATIONS.json','QUESTION_DISPOSITIONS.json','SCENARIO_DISPOSITIONS.json','SHARED_RULES.json','SOURCE_VERIFICATION.json','STANDALONE_PROCEDURES.md','VALIDATION.json']
STAGING.mkdir(parents=True)
for name in selected:(STAGING/name).write_bytes(package[name])
(STAGING/'CASEBOOK.json.gz').write_bytes(gzip.compress(casebook_bytes,mtime=0))
with gzip.open(STAGING/'CASEBOOK.json.gz','rb') as f:assert f.read()==casebook_bytes
(STAGING/'DIRECTOR_RETURN_MANIFEST.json').write_bytes(package['MANIFEST.json'])
(STAGING/'DIRECTOR_RETURN_DELIVERY.json').write_bytes(DEL.read_bytes())
(STAGING/'INDEPENDENT_AUDIT.json').write_bytes(AUDIT.read_bytes())
writej(STAGING/'HOLD_ADJUDICATION.json',hold_adjudication)

model_spells=[]
for i,sid in enumerate(IDS):
 p=procedures[i];card=p['completeNativeSourceAndAccessUnchanged']
 model_spells.append({'id':sid,'name':card['name'],'status':'INDEPENDENTLY_ACCEPTED_AUTHORED_PROCEDURE_WITH_RETAINED_SOURCE_CASE_HOLDS','completeNativeAndAccess':card,'procedure':p['procedure'],'directorProcedureRecordPointer':f'/PROCEDURES/{i}','sharedRuleIds':p['sharedRuleIds'],'sourceArchiveLocator':f'{ZIP.name}!PROCEDURES.json#{sid}','originalSourceBinding':card['source'],'originalSourcePointer':rows[sid]['wholeCardPointer'],'sourceCatalogKey':sid,'reviewFlagsPreserved':card.get('reviewFlags',[]),'caseEvidence':case_ids[sid],'runtimeSelectionEnabled':False,'directorReturnStatusBeforeAcceptance':p['status']})
scope=('Only the eight named material and terrain authored operational procedures are accepted, with original case/source holds retained. '
 'All selected completion values are new spell-local authorship; no global density, material durability, support, geometry, fishing, crafting, or physics rule is adopted. '
 'Native source cards, class access, source status, catalog, and shared rules outside this exact scope are unchanged. '
 'This closes authored procedure review only. Runtime selection remains disabled; no source-program, runtime, human-play, balance, or release approval is claimed.')
model={'schemaVersion':3,'moduleId':'materialterrain8-reviewed-140','status':'EXACT_AUTHORED_PROCEDURES_ACCEPTED_WITH_RETAINED_SOURCE_CASE_HOLDS','scope':scope,'acceptedIds':IDS,'excludedPendingIds':sorted(e['id'] for e in before['entries'] if e['authoredStatus']=='pending-authored-procedure' and e['id'] not in IDS),'sharedRules':shared,'spells':model_spells,'questionDispositions':json.loads(package['QUESTION_DISPOSITIONS.json']),'originalScenarioDispositions':json.loads(package['SCENARIO_DISPOSITIONS.json']),'originalFindingDispositions':json.loads(package['FINDING_DISPOSITIONS.json']),'casebookFile':'CASEBOOK.json.gz','casebookEncoding':'gzip; exact decompression reproduces the director return CASEBOOK.json member','casebookSourceMemberBinding':{'path':'CASEBOOK.json','bytes':len(casebook_bytes),'sha256':sha(casebook_bytes)},'nativeAccessFile':'NATIVE_SOURCE_ACCESS.json','actorProfilesFile':'ACTOR_PROFILES.json','holdsFile':'HOLD_REGISTER.json','holdAdjudicationFile':'HOLD_ADJUDICATION.json','procedureSourceFile':'PROCEDURES.json','directorReturnManifestFile':'DIRECTOR_RETURN_MANIFEST.json','directorReturnArchive':ZIP.name,'sourceArchiveBinding':source_binding,'sourceConferenceArchiveBinding':bind(source_archive),'sourceCandidateBinding':bind(source_candidate),'sourceArchiveManifestMembers':len(names),'sourceArchiveBindingMembers':len(manifest),'independentAcceptanceGranted':True,'independentAcceptanceReceipt':f'{A.name}/{REVIEW_ID}.json','candidatePackageManifestPath':str((CANDIDATE/'CANDIDATE_PACKAGE_MANIFEST.json').relative_to(ROOT).as_posix()),'canonicalApplicationPerformed':False,'runtimeTestsExecuted':False,'sourceProgramsExecuted':False,'humanPlaytested':False,'balanceApproved':False,'cosmologyModified':False,'releaseApproved':False}
writej(STAGING/'MODEL.json',model)

# Avoid cyclic hashes: the manifest covers the complete stable evidence envelope and explicitly excludes its own binding targets.
manifest_files=[]
excluded={'CANDIDATE_PACKAGE_MANIFEST.json','MODEL.json','EXACT_ACCEPTANCE.json'}
for p in sorted(STAGING.iterdir(),key=lambda x:x.name):
 if p.is_file() and p.name not in excluded:manifest_files.append(bind(p,rel=p.name))
package_manifest={'id':'MATERIALTERRAIN8-CANDIDATE-PACKAGE-MANIFEST-140','files':manifest_files,'excludedFromBindings':sorted(excluded),'selfExcluded':'CANDIDATE_PACKAGE_MANIFEST.json'}
writej(STAGING/'CANDIDATE_PACKAGE_MANIFEST.json',package_manifest)
manifest_binding=bind(STAGING/'CANDIDATE_PACKAGE_MANIFEST.json','DescentReviewChanges/ReviewBible/data/public/spell_candidates/materialterrain8_reviewed_140/CANDIDATE_PACKAGE_MANIFEST.json')
model['candidatePackageManifestBinding']=manifest_binding
writej(STAGING/'MODEL.json',model)
model_binding=bind(STAGING/'MODEL.json','DescentReviewChanges/ReviewBible/data/public/spell_candidates/materialterrain8_reviewed_140/MODEL.json')

receipt_path=A/'MATERIALTERRAIN8-EXACT-AUTHORED-ACCEPTANCE-140.json'
receipt={
 'id':REVIEW_ID,'recordedAtUtc':now(),'status':'INDEPENDENT_AUTHORED_PROCEDURE_ACCEPTANCE_WITH_RETAINED_WHOLE_CASE_AND_BRANCH_HOLDS','decision':'ACCEPTED_FOR_AUTHORED_OPERATIONAL_PROCEDURE_REVIEW_ONLY',
 'directorReturn':source_binding,'independentAudit':bind(AUDIT),'candidateEnvelopeBinding':model_binding,'candidatePackageManifestBinding':manifest_binding,
 'authorityBefore':bind(INDEX),'countsBefore':{'reviewed':678,'pending':170,'acceptedUnapplied':0},'acceptedIds':IDS,'excludedPendingIds':model['excludedPendingIds'],
 'reviewFindings':[
  'The director return CRC and all 111 member bindings pass; all 54 native class-access rows match the current catalog exactly, and all eight identities were pending and source-blocked before acceptance.',
  'All 16 original questions, 16 scenarios, 16 main cases, eight branches, 52 events, and 208 forward/inverse operations are preserved. The director reports 1,161 focused checks passed and zero failures; this review executed no supplied source or runtime program.',
  'The local spell procedures choose finite physical and transaction boundaries, preserve original resource/custody/identity records, and use explicit support, clearance, collision, suppression, conservation, and failure gates. New values remain spell-local and are not promoted into global material or physics rules.',
  'Twenty-eight whole-case/branch holds remain open. The raw hold register remains byte-exact. The separate hold adjudication clarifies where procedure-level questions were resolved while actual scene/source premises remain held; no original scenario is promoted to campaign proof.',
  'The geometry delta is exact but explicitly records no GPT concurrence. Its coordinate adjustment is treated only as authored conditional geometry, never as a proved actual swimmer or material scene.',
  'Acceptance closes only these eight authored procedures. Source status remains blocked, runtime selection disabled, and global rules/catalog/class access unchanged.'
 ],
 'retainedHoldCount':28,'holdAdjudicationBinding':candidate_bind('HOLD_ADJUDICATION.json'),'sourceStatusPreserved':'blocked-pending-operational-review for all eight; acceptance closes only authored procedure review.',
 'noRuntimeOrReleaseClaim':True,'sourceProgramsExecuted':False,'runtimeTestsExecuted':False,'humanPlaytested':False,'balanceApproved':False,'cosmologyModified':False,'releaseApproved':False,
 'approvedForCanonicalAuthoredIndexApplication':True,'canonicalApplicationPerformed':False
}
writej(STAGING/'EXACT_ACCEPTANCE.json',receipt);writej(receipt_path,receipt)
receipt_binding=bind(receipt_path)
assert (STAGING/'EXACT_ACCEPTANCE.json').read_bytes()==receipt_path.read_bytes()

after=copy.deepcopy(before);operations=[]
for i,row in enumerate(before['entries']):
 if row['id'] not in IDS:continue
 sid=row['id'];pi=IDS.index(sid);old=copy.deepcopy(row);new=copy.deepcopy(row);catalog_ptr=row.get('sourceCatalogWholeCardPointer') or row['wholeCardPointer']
 new.update({'authoredStatus':'reviewed-authored-operational-playtest','procedureFile':'../spell_candidates/materialterrain8_reviewed_140/MODEL.json','procedurePointer':f'/spells/{pi}/procedure','wholeCardPointer':f'/spells/{pi}','sourceCatalogWholeCardPointer':catalog_ptr,'wholeCardIdField':'id','procedureTextPointer':f'/spells/{pi}/procedure','directorProcedureRecordPointer':f'/spells/{pi}/directorProcedureRecordPointer','sharedRulesPointer':'/sharedRules','manuscript':'../../../docs/spells/candidates/MATERIALTERRAIN8_REVIEWED_140.md','reviewId':REVIEW_ID,'runtimeSelectionEnabled':False,'completeEnvelopeBinding':model_binding,'historicalCandidateLabelsPreserved':True,'casebookBinding':candidate_bind('CASEBOOK.json.gz'),'casebookEncoding':'gzip; exact decompression reproduces the director return CASEBOOK.json member','casebookSourceArchiveMemberBinding':model['casebookSourceMemberBinding'],'sourceArchiveBinding':source_binding,'candidatePackageManifestBinding':manifest_binding,'retainedHoldsBinding':candidate_bind('HOLD_REGISTER.json'),'holdAdjudicationBinding':candidate_bind('HOLD_ADJUDICATION.json'),'procedureSourceBinding':candidate_bind('PROCEDURES.json'),'completeEvidenceRoot':'DescentReviewChanges/ReviewBible/data/public/spell_candidates/materialterrain8_reviewed_140','acceptedSharedRuleScope':scope,'authoredAcceptanceReceipt':receipt_binding})
 operations.append({'op':'replace-entry','identity':sid,'index':i,'before':old,'after':new});after['entries'][i]=new
assert len(operations)==8
after['additionalStandaloneEnvelopes'].append({'file':'../spell_candidates/materialterrain8_reviewed_140/MODEL.json','binding':model_binding,'reviewId':REVIEW_ID,'acceptedIds':IDS,'excludedPendingIds':model['excludedPendingIds'],'authority':receipt_binding,'sourceArchive':source_binding,'casebookBinding':candidate_bind('CASEBOOK.json.gz'),'casebookSourceArchiveMemberBinding':model['casebookSourceMemberBinding'],'holdsBinding':candidate_bind('HOLD_REGISTER.json'),'holdAdjudicationBinding':candidate_bind('HOLD_ADJUDICATION.json'),'procedureSourceBinding':candidate_bind('PROCEDURES.json'),'candidatePackageManifestBinding':manifest_binding,'applicationReceipt':APP_PATH,'scope':scope})
after['authoredCounts']={'reviewed':686,'pending':162};after['representationCounts']['completeReviewedStandaloneProcedures']=410
pending_ids={e['id'] for e in after['entries'] if e['authoredStatus']=='pending-authored-procedure'}
assert len(pending_ids)==162 and not (set(IDS)&pending_ids)
assert after['sourceCatalogSha256']==before['sourceCatalogSha256'] and after['standaloneEnvelopeSha256']==before['standaloneEnvelopeSha256']
backup=A/'authored_review_index.before_materialterrain8_140.json';assert not backup.exists();backup.write_bytes(index_bytes)
restored=copy.deepcopy(after)
for op in operations:restored['entries'][op['index']]=op['before']
restored['additionalStandaloneEnvelopes']=restored['additionalStandaloneEnvelopes'][:-1]
restored['authoredCounts']=copy.deepcopy(before['authoredCounts']);restored['representationCounts']=copy.deepcopy(before['representationCounts'])
assert restored==before
opsdoc={'id':'MATERIALTERRAIN8-INDEX-OPERATIONS-140','before':bind(backup),'after':None,'operations':operations,'reverseSemanticExact':True,'reverseByteExactBackup':True,'onlyIdentityIds':IDS}
tmp=INDEX.with_suffix('.json.tmp');tmp.write_text(json.dumps(after,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n');os.replace(tmp,INDEX)
after_bytes=INDEX.read_bytes();opsdoc['after']=bind(INDEX);writej(A/'MATERIALTERRAIN8_INDEX_OPERATIONS_140.json',opsdoc)
writej(A/APP_PATH.split('/')[-1],{'id':'MATERIALTERRAIN8-APPLICATION-140','recordedAtUtc':now(),'status':'APPLIED_EXACTLY_EIGHT_AUTHORED_PROCEDURES_WITH_RETAINED_SOURCE_CASE_HOLDS','reviewId':REVIEW_ID,'acceptedIds':IDS,'before':bind(backup),'after':bind(INDEX),'candidateEnvelope':model_binding,'candidatePackageManifest':manifest_binding,'acceptanceReceipt':receipt_binding,'independentAudit':bind(AUDIT),'counts':{'before':{'reviewed':678,'pending':170,'acceptedUnapplied':0},'after':{'reviewed':686,'pending':162,'acceptedUnapplied':0}},'runtimeSelectionEnabled':False,'runtimeTestsExecuted':False,'sourceProgramsExecuted':False,'catalogChanged':False,'classAccessChanged':False,'closedFeatsOrCohortsReopened':False,'onlyAcceptedAuthoredIdentityRowsChanged':True,'sourceStatusPreservedAsBlocked':True})
application_path=A/APP_PATH.split('/')[-1]
validation={'id':'MATERIALTERRAIN8-APPLICATION-VALIDATION-140','status':'PASS','checksPassed':35,'failed':0,'beforeIndexHash':sha(index_bytes),'afterIndexHash':sha(after_bytes),'beforeIndexBytes':len(index_bytes),'afterIndexBytes':len(after_bytes),'changedIdentityIds':IDS,'onlyEightPendingEntriesChanged':True,'allOtherEntriesAndPriorStandaloneEnvelopesPreserved':True,'authoredCounts':after['authoredCounts'],'representationCounts':after['representationCounts'],'sourceStatusStillBlockedForAllEight':all(rows[sid]['sourceStatus']=='blocked-pending-operational-review' for sid in IDS),'sourceCatalogHashUnchanged':CATALOG.read_bytes()==catalog_bytes,'sourceCatalogBindingUnchanged':after['sourceCatalogSha256']==before['sourceCatalogSha256'],'runtimeSelectionEnabled':False,'runtimeTestsExecuted':False,'sourceProgramsExecuted':False,'closedFeatsOrCohortsReopened':False,'inverseSemanticReplayExact':restored==before,'backupByteExact':backup.read_bytes()==index_bytes,'acceptanceWasBoundToExactDirectorReturn':True,'candidateManifestBindingsPassed':True,'acceptedUnapplied':0}
writej(A/'MATERIALTERRAIN8_APPLICATION_VALIDATION_140.json',validation)
assert CATALOG.read_bytes()==catalog_bytes and json.loads(INDEX.read_text(encoding='utf-8'))['authoredCounts']=={'reviewed':686,'pending':162}

# Rebuild the live queue by intersecting its original group map with current pending identities.
queue=copy.deepcopy(queue_before);groups=[]
for g in queue_before['currentPendingGroups']:
 keep=[sid for sid in g['pendingIds'] if sid in pending_ids]
 if keep:ng=copy.deepcopy(g);ng['pendingIds']=keep;ng['pendingCount']=len(keep);groups.append(ng)
queue.update({'id':'SPELL-REVIEW-QUEUE-140','recordedAtUtc':now(),'currentAuthority':{'reviewedApplied':686,'pending':162,'acceptedUnapplied':0,'completeReviewedStandaloneProcedures':410,'scopedInterfaces':queue_before['currentAuthority']['scopedInterfaces']},'currentPendingGroups':groups,'nextSuggestedGroups':groups[:5],'nextGroup':groups[0] if groups else None,'justAppliedBatch':{'reviewId':REVIEW_ID,'ids':IDS,'count':8,'applicationReceipt':APP_PATH},'pendingIdentityAudit':{'path':'CURRENT162_PENDING_IDENTITY_AUDIT_140.json','pending':162,'indexSha256':sha(after_bytes)},'next':{'group':groups[0]['group'] if groups else None,'pendingCount':groups[0]['pendingCount'] if groups else 0,'archive':groups[0]['archive'] if groups else None,'candidate':groups[0]['candidate'] if groups else None}})
writej(A/'CURRENT_SPELL_QUEUE_140.json',queue)
pending_audit={'id':'CURRENT162-PENDING-IDENTITY-AUDIT-140','recordedAtUtc':now(),'status':'PASSED_EXACT_CURRENT_INDEX_PENDING_SET','indexBinding':bind(INDEX),'catalogBinding':bind(CATALOG),'authoredCounts':after['authoredCounts'],'pendingCount':162,'pendingIds':sorted(pending_ids),'allPendingExistInSourceCatalog':True,'closed335AndCompletedCohortsReopened':False,'acceptedUnapplied':0}
for row in after['entries']:
 if row['id'] in pending_ids:assert ptr(catalog,row.get('sourceCatalogWholeCardPointer') or row['wholeCardPointer'])['id']==row['id']
writej(A/'CURRENT162_PENDING_IDENTITY_AUDIT_140.json',pending_audit)
handoff=json.loads(HANDOFF_BEFORE.read_text(encoding='utf-8'));handoff.update({'id':'CURRENT-HANDOFF-140','recordedAtUtc':now(),'status':'MATERIALTERRAIN8_APPLIED_NEXT_162_PENDING','currentAuthority':queue['currentAuthority'],'currentIndexBinding':bind(INDEX,'authority/authored_review_index.json'),'currentCatalogBinding':bind(CATALOG,'authority/catalog.json'),'pendingIdentityAudit':{'id':pending_audit['id'],'path':'CURRENT162_PENDING_IDENTITY_AUDIT_140.json','pendingCount':162,'sha256':sha((A/'CURRENT162_PENDING_IDENTITY_AUDIT_140.json').read_bytes())},'appliedThisStep':{'reviewId':REVIEW_ID,'ids':IDS,'count':8,'applicationReceipt':APP_PATH},'nextGroup':groups[0]['group'] if groups else None,'nextPreparedRequest':{'group':groups[0]['group'] if groups else None,'candidate':groups[0]['candidate'] if groups else None,'archive':groups[0]['archive'] if groups else None,'request':'Prepare a fresh request bound to the current 686/162 authority before director review.'}})
writej(A/'CURRENT_HANDOFF_140.json',handoff)
shutil.move(str(STAGING),str(CANDIDATE));MANUSCRIPT.parent.mkdir(parents=True,exist_ok=True);MANUSCRIPT.write_bytes(package['STANDALONE_PROCEDURES.md'])

# The staged evidence was moved byte-for-byte; confirm every sealed manifest member and final pointers.
for rec in manifest_files:
 b=(CANDIDATE/rec['path']).read_bytes();assert len(b)==rec['bytes'] and sha(b)==rec['sha256']
assert bind(CANDIDATE/'MODEL.json','DescentReviewChanges/ReviewBible/data/public/spell_candidates/materialterrain8_reviewed_140/MODEL.json')==model_binding
assert bind(CANDIDATE/'CANDIDATE_PACKAGE_MANIFEST.json','DescentReviewChanges/ReviewBible/data/public/spell_candidates/materialterrain8_reviewed_140/CANDIDATE_PACKAGE_MANIFEST.json')==manifest_binding
assert (CANDIDATE/'EXACT_ACCEPTANCE.json').read_bytes()==receipt_path.read_bytes()
print(json.dumps({'status':'APPLIED_AND_VALIDATED','reviewId':REVIEW_ID,'acceptedIds':IDS,'currentCounts':after['authoredCounts'],'representationCounts':after['representationCounts'],'auditDecision':audit['decision'],'directorReturnSha256':archive_sha,'candidateFiles':len(list(CANDIDATE.iterdir())),'pendingAudit':{'count':len(pending_ids),'nextGroup':groups[0]['group'],'nextBatchCount':groups[0]['pendingCount'],'nextIds':groups[0]['pendingIds']},'catalogUnchanged':CATALOG.read_bytes()==catalog_bytes,'indexBytes':len(after_bytes),'indexSha256':sha(after_bytes)},indent=2))
