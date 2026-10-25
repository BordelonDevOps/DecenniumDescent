import copy,datetime,hashlib,json,shutil,zipfile
from pathlib import Path
BASE=Path(r'C:\Github\DecenniumDescent')
AUDIT=BASE/'docs/audit/2026-10-08/full-game/director-spell-review-129'
ZIP=AUDIT/'DD_Information8_Director_Return03_131.zip'
ACC=AUDIT/'INFORMATION8_EXACT_ACCEPTANCE_129.json'
AUD=AUDIT/'INFORMATION8_RETURN03_INDEPENDENT_EXACT_AUDIT_129.json'
IDX=BASE/'DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json'
EVIDENCE=BASE/'DescentReviewChanges/ReviewBible/data/public/spell_candidates/information8_reviewed_129'
DOCS=BASE/'DescentReviewChanges/ReviewBible/docs/spells/candidates'
MANUSCRIPT=DOCS/'INFORMATION8_FINDTHEPATH_REVIEWED_129.md'
APP=AUDIT/'INFORMATION8_FINDTHEPATH_APPLICATION_129.json'
OPS=AUDIT/'INFORMATION8_FINDPATH_INDEX_OPERATIONS_129.json'
VALID=AUDIT/'INFORMATION8_FINDPATH_APPLICATION_VALIDATION_129.json'
BEFORE= AUDIT/'authored_review_index.before_information8_findpath_129.json'
def sha(b): return hashlib.sha256(b).hexdigest()
def dump(obj): return (json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
assert json.loads(AUD.read_text(encoding='utf-8-sig'))['status']=='PASS'
assert json.loads(ACC.read_text(encoding='utf-8-sig'))['status']=='ACCEPTED_FOR_AUTHORED_OPERATIONAL_PLAYTEST_WITH_RETAINED_TOPOLOGY_HOLD'
assert not APP.exists() and not OPS.exists() and not VALID.exists() and not BEFORE.exists(), 'Application receipt already exists; refusing a second application.'
old_bytes=IDX.read_bytes(); old_text=old_bytes.decode('utf-8-sig'); old=json.loads(old_text)
assert sha(old_bytes)=='44fec30864c5836b9d07ef3ee26b2aa63dfe89cda9bdaf824ff040e434ec1f72'
assert old['authoredCounts']=={'reviewed':635,'pending':213}
old_entries=copy.deepcopy(old['entries']); pos=next(i for i,e in enumerate(old['entries']) if e['id']=='find-the-path'); before_row=copy.deepcopy(old['entries'][pos])
assert before_row['authoredStatus']=='pending-authored-procedure' and before_row['procedurePointer'] is None
EVIDENCE.parent.mkdir(parents=True,exist_ok=True); DOCS.mkdir(parents=True,exist_ok=True)
with zipfile.ZipFile(ZIP) as z:
    for info in z.infolist():
        if Path(info.filename).is_absolute() or '..' in Path(info.filename).parts:
            raise AssertionError('Unsafe archive member path: '+info.filename)
        if (info.external_attr >> 16) & 0o170000 == 0o120000:
            raise AssertionError('Symlink member rejected: '+info.filename)
    if EVIDENCE.exists():
        assert EVIDENCE.is_dir(), 'Evidence target exists but is not a directory.'
        for info in z.infolist():
            if info.is_dir(): continue
            target=EVIDENCE/info.filename
            assert target.is_file() and target.read_bytes()==z.read(info.filename), 'Pre-existing partial extraction differs: '+info.filename
    else:
        z.extractall(EVIDENCE)
    archive_procs=json.loads(z.read('PROCEDURES.json'))['spells']
    proc=next(x for x in archive_procs if x['spellId']=='find-the-path')
    rules=json.loads(z.read('SHARED_RULES.json'))
    casebook_bytes=z.read('CASEBOOK.json'); holds_bytes=z.read('HOLDS.json')
model_bytes=(AUDIT/'INFORMATION8_FINDPATH_EXACT_REFERENCE_MODEL_129.json').read_bytes()
assert sha(model_bytes)==json.loads(ACC.read_text(encoding='utf-8-sig'))['acceptedReferenceModel']['sha256']
if (EVIDENCE/'MODEL.json').exists():
    assert (EVIDENCE/'MODEL.json').read_bytes()==model_bytes, 'Existing reference model differs.'
else:
    (EVIDENCE/'MODEL.json').write_bytes(model_bytes)
model=json.loads(model_bytes)
assert model['acceptedIds']==['find-the-path'] and len(model['completeProcedures'])==1
assert model['completeProcedures'][0]==proc and model['sharedRules']==rules
native=json.dumps(proc['completeNativeSourceAndAccess'],ensure_ascii=False,indent=2)
shared='\n'.join(f"### {r['id']}\n\n{r['rule']}" for r in rules)
md=("# Find the Path — reviewed authored procedure (Information8, Return03)\n\n"
"Status: accepted for authored operational playtest and applied to the review index. This records authored procedure coverage only; runtime selection, implementation, human play, balance, cosmology, temporal and release approval remain separate.\n\n"
"## Native source and access\n\n"
"The exact native card/source record is preserved in the applied evidence bundle at `NATIVE_ACCESS_RECORDS.json`; the current proposal source identity and pointer are recorded below.\n\n"
+f"- Source: `{proc['source']['path']}`\n- Source pointer: `{proc['pointer']}`\n- Source SHA-256: `{proc['source']['sha256']}`\n\n"
"```json\n"+native+"\n```\n\n"
"## Complete selected procedure\n\n"+proc['procedure']+"\n\n"
"## Shared requirements referenced by this procedure\n\n"+shared+"\n\n"
"## Accepted source cases\n\n"
"- `DI6-04-A`: complete original case, actual route geometry, key/door actions, movement, and full timeline are preserved in `CASEBOOK.json` and `cases/DI6-04-A.json`.\n"
"- `DI6-04-B`: complete original case and both branches are preserved. After the actual crossbar and new paid inquiry, the recipient-facing result is exactly `Indeterminate`. The missing surrounding-topology reason remains a private qualification; no global shortest-route claim is made. The forward and inverse event operations are independently verified.\n\n"
"## Retained qualification\n\n"
"The 120-foot postbar route remains a possible traversable detour, not a proven global shortest path. The protected-indispensable-shorter-terrain positive case remains held because no real terrain-protection provider or complete surrounding topology was supplied. No free route-opening success, spell movement, or world-content inference is added. See `HOLDS.json` for the full retained register.\n\n"
"## Exact source archive\n\n"
+f"`{ZIP.name}` — {ZIP.stat().st_size} bytes, SHA-256 `{sha(ZIP.read_bytes())}`. The complete source archive and all members remain preserved unchanged in the audit directory.\n")
if MANUSCRIPT.exists():
    assert MANUSCRIPT.read_bytes()==md.encode('utf-8'), 'Existing manuscript differs.'
else:
    MANUSCRIPT.write_text(md,encoding='utf-8',newline='\n')
acceptance_bytes=ACC.read_bytes(); acceptance=json.loads(acceptance_bytes.decode('utf-8-sig'))
model_path='DescentReviewChanges/ReviewBible/data/public/spell_candidates/information8_reviewed_129/MODEL.json'
casebook_path='DescentReviewChanges/ReviewBible/data/public/spell_candidates/information8_reviewed_129/CASEBOOK.json'
holds_path='DescentReviewChanges/ReviewBible/data/public/spell_candidates/information8_reviewed_129/HOLDS.json'
appid='INFORMATION8-FINDTHEPATH-APPLICATION-129'
app={
 'id':appid,'recordedAtUtc':now,'status':'APPLIED_ONE_AUTHORED_IDENTITY_WITH_RETAINED_SOURCE_HOLDS',
 'ownerInstruction':'Apply each exact accepted ordinary-spell scope and continue until all identities in the original232 queue are applied.',
 'acceptedIds':['find-the-path'],'excludedAlreadyAppliedIds':acceptance['scope']['previouslyAppliedIdsExcluded'],
 'authorityAcceptance':{'path':'docs/audit/2026-10-08/full-game/director-spell-review-129/INFORMATION8_EXACT_ACCEPTANCE_129.json','bytes':len(acceptance_bytes),'sha256':sha(acceptance_bytes)},
 'independentExactAudit':{'path':'docs/audit/2026-10-08/full-game/director-spell-review-129/INFORMATION8_RETURN03_INDEPENDENT_EXACT_AUDIT_129.json','checksPassed':199,'status':'PASS'},
 'sourceArchive':acceptance['sourceArchive'],
 'acceptedReferenceModel':{'path':model_path,'bytes':len(model_bytes),'sha256':sha(model_bytes)},
 'exactEvidenceRoot':'DescentReviewChanges/ReviewBible/data/public/spell_candidates/information8_reviewed_129',
 'evidenceManifest':{'path':model_path.replace('MODEL.json','MANIFEST.json'),'bytes':(EVIDENCE/'MANIFEST.json').stat().st_size,'sha256':sha((EVIDENCE/'MANIFEST.json').read_bytes()),'originalDeliveredManifestPreserved':True},
 'casebook':{'path':casebook_path,'bytes':len(casebook_bytes),'sha256':sha(casebook_bytes),'acceptedCaseIds':['DI6-04-A','DI6-04-B']},
 'retainedHolds':{'path':holds_path,'bytes':len(holds_bytes),'sha256':sha(holds_bytes),'acceptedIdentityHold':'PROTECTED-SHORTER-TERRAIN'},
 'chapter':{'path':'DescentReviewChanges/ReviewBible/docs/spells/candidates/INFORMATION8_FINDTHEPATH_REVIEWED_129.md','bytes':len(md.encode('utf-8')),'sha256':sha(md.encode('utf-8'))},
 'indexBefore':{'path':'DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json','bytes':len(old_bytes),'sha256':sha(old_bytes),'reviewed':635,'pending':213},
 'indexOperations':'docs/audit/2026-10-08/full-game/director-spell-review-129/INFORMATION8_FINDPATH_INDEX_OPERATIONS_129.json',
 'scope':'Only Find the Path, including both full cases, all existing source/native access, the six exact shared requirements, original obligations and explicit retained holds. The other seven Information identities were already applied and their index rows remain byte-equivalent.',
 'runtimeSelectionEnabled':False,'runtimeImplemented':False,'classOrGlobalRuleAmendment':False,'historicalSourceLabelsPreserved':True,'closedCohortsReopened':False
}
app_bytes=dump(app); APP.write_bytes(app_bytes)
new=copy.deepcopy(old); new['authoredCounts']['reviewed']=636; new['authoredCounts']['pending']=212; new['representationCounts']['completeReviewedStandaloneProcedures']=360
newrow=copy.deepcopy(before_row)
newrow.update({
 'authoredStatus':'reviewed-authored-operational-playtest','procedureFile':'../spell_candidates/information8_reviewed_129/MODEL.json','procedurePointer':'/completeProcedures/0','wholeCardPointer':'/completeProcedures/0','sourceCatalogWholeCardPointer':'/spells/267','wholeCardIdField':'id','procedureTextPointer':'/completeProcedures/0/procedure','sharedRulesPointer':'/sharedRules','manuscript':'../../../docs/spells/candidates/INFORMATION8_FINDTHEPATH_REVIEWED_129.md','reviewId':appid,'runtimeSelectionEnabled':False,
 'completeEnvelopeBinding':{'path':model_path,'bytes':len(model_bytes),'sha256':sha(model_bytes)},
 'authoredAcceptanceReceipt':{'path':'docs/audit/2026-10-08/full-game/director-spell-review-129/INFORMATION8_EXACT_ACCEPTANCE_129.json','bytes':len(acceptance_bytes),'sha256':sha(acceptance_bytes)},
 'authoredApplicationReceipt':{'path':'docs/audit/2026-10-08/full-game/director-spell-review-129/INFORMATION8_FINDTHEPATH_APPLICATION_129.json','bytes':len(app_bytes),'sha256':sha(app_bytes)},
 'historicalCandidateLabelsPreserved':True,
 'casebookBinding':{'path':casebook_path,'bytes':len(casebook_bytes),'sha256':sha(casebook_bytes)},
 'retainedHoldsBinding':{'path':holds_path,'bytes':len(holds_bytes),'sha256':sha(holds_bytes)},
 'completeEvidenceRoot':'DescentReviewChanges/ReviewBible/data/public/spell_candidates/information8_reviewed_129',
 'acceptedSharedRuleScope':'Find the Path cites the six unchanged Information8 shared requirements, already used in the accepted Information3 scope; no new global rule, class grant or runtime selector is introduced.'
})
new['entries'][pos]=newrow
new_bytes=dump(new)
assert sha(new_bytes)!=sha(old_bytes)
assert new['sourceCatalogSha256']==old['sourceCatalogSha256'] and new['standaloneEnvelopeSha256']==old['standaloneEnvelopeSha256']
BEFORE.write_bytes(old_bytes)
IDX.write_bytes(new_bytes)
ops={'id':'INFORMATION8-FINDPATH-INDEX-OPERATIONS-129','beforeIndexSha256':sha(old_bytes),'afterIndexSha256':sha(new_bytes),'forward':[{'op':'replace','path':'/authoredCounts/reviewed','before':635,'after':636},{'op':'replace','path':'/authoredCounts/pending','before':213,'after':212},{'op':'replace','path':'/representationCounts/completeReviewedStandaloneProcedures','before':359,'after':360},{'op':'replace','path':f'/entries/{pos}','before':before_row,'after':newrow}],'inverse':[{'op':'replace','path':f'/entries/{pos}','before':newrow,'after':before_row},{'op':'replace','path':'/representationCounts/completeReviewedStandaloneProcedures','before':360,'after':359},{'op':'replace','path':'/authoredCounts/pending','before':212,'after':213},{'op':'replace','path':'/authoredCounts/reviewed','before':636,'after':635}],'unchangedTopLevelFields':['sourceCatalogSha256','standaloneEnvelopeSha256','schemaVersion','status','scope'],'roundTripRestoresExactIndexObject':True}
OPS.write_bytes(dump(ops))
# Build a new exact pending audit from current index, preserving the former list order.
old_pending=json.loads((AUDIT/'CURRENT213_PENDING_IDENTITY_AUDIT_129.json').read_text(encoding='utf-8-sig'))
pending_ids=[x for x in old_pending['pendingIds'] if x!='find-the-path']
special_pending=[i for i in pending_ids if next(e for e in new['entries'] if e['id']==i)['authoredStatus']!='pending-authored-procedure']
assert len(pending_ids)==212 and set(pending_ids)==set(old_pending['pendingIds'])-{'find-the-path'} and special_pending==['blink']
queue_source=BASE/'DescentReviewChanges/ReviewBible/data/director/spell_review/remaining_work_queue_67.json'
queue_sha=sha(queue_source.read_bytes())
current_pending={'id':'CURRENT212-PENDING-IDENTITY-AUDIT-129','recordedAtUtc':now,'index':{'path':'DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json','bytes':len(new_bytes),'sha256':sha(new_bytes)},'pendingIds':pending_ids,'pendingCount':212,'newAppliedIds':['find-the-path'],'allRemainingInEarlierQueue':True,'currentFullSourceSubmission':old_pending['currentFullSourceSubmission'],'appliedCoverage':{'applied':636,'pending':212,'standalone':360,'scopedInterfaces':173,'acceptedUnapplied':0},'sourceQueue':{'path':'DescentReviewChanges/ReviewBible/data/director/spell_review/remaining_work_queue_67.json','bytes':queue_source.stat().st_size,'sha256':queue_sha}}
(AUDIT/'CURRENT212_PENDING_IDENTITY_AUDIT_129.json').write_bytes(dump(current_pending))
# Update the current 129 queue snapshot without altering its historical previous versions.
queue_path=BASE/'docs/audit/2026-10-08/full-game/spell-review-resume-116/CURRENT_SPELL_QUEUE_129.json'
queue=json.loads(queue_path.read_text(encoding='utf-8-sig'))
queue['currentCounts'].update({'appliedReviewed':636,'indexPending':212,'acceptedUnapplied':0,'needsAcceptance':212,'submittedAwaitingReturn':212,'returnedNeedsCorrection':0})
queue['latestAcceptanceReceipts'].append(str(ACC)); queue['latestApplicationReceipts'].append(str(APP))
queue['queueIdentityAudit']=str(AUDIT/'CURRENT212_PENDING_IDENTITY_AUDIT_129.json')
queue['currentHandoff']=str(AUDIT/'CURRENT_HANDOFF_129.json')
queue['nextSuggestedGroups']=[x for x in queue['nextSuggestedGroups'] if x!='information8']
for group in queue['groups']:
    if group.get('group')=='information8':
        group['appliedIdentities']=list(dict.fromkeys(group.get('appliedIdentities',[])+['find-the-path']))
        group['pendingIdentities']=[x for x in group.get('pendingIdentities',[]) if x!='find-the-path']
        group['currentPhase']='all-eight-information-identities-applied-with-retained-source-holds-129'
        group['applicationReceipt']=str(APP)
queue['resumePriority']='Find the Path Return03 exact acceptance/application is complete with its PROTECTED-SHORTER-TERRAIN hold preserved. Continue with EyeJudgement1 from the current Part6 delivery; independently review each exact return and apply only accepted pending identities until all212 remain are completed.'
queue['lastAppliedInformation8Identity']='find-the-path'
queue['lastUpdatedAtUtc']=now
queue_path.write_bytes(dump(queue))
# Update the authoritative work handoff.
handoff_path=AUDIT/'CURRENT_HANDOFF_129.json'; handoff=json.loads(handoff_path.read_text(encoding='utf-8-sig'))
handoff['status']='PART6_INFORMATION8_ALL_APPLIED_EYE1_CONTINUES_ALL212_REQUIRED'
handoff['currentCounts']={'reviewedApplied':636,'pending':212,'standalone':360,'scopedInterfaces':173,'acceptedUnapplied':0}
handoff.setdefault('appliedThisTurn',{})['Information8FindThePath']=['find-the-path']
apprefs=handoff.setdefault('applicationReceipts',[])
if str(APP) not in apprefs: apprefs.append(str(APP))
handoff['next']='Continue the already sourced EyeJudgement1 batch, then apply every exact accepted ordinary-spell batch until all212 current pending identities are applied.'
handoff['resumePriority']='Find the Path recipient-view Return03 accepted/applied exactly; preserve the protected-shorter-terrain hold. Resume the existing EyeJudgement1 conference; apply after exact independent acceptance. Current index is authority at636/212.'
handoff['currentPendingIdentityAudit']=str(AUDIT/'CURRENT212_PENDING_IDENTITY_AUDIT_129.json')
handoff['lastAppliedIdentity']={'id':'find-the-path','acceptance':str(ACC),'application':str(APP),'validation':str(VALID)}
handoff['directorConnectionStatus']='Find the Path exact recipient-view correction is independently accepted/applied locally. Send the exact scoped update and 636/212 context to the existing Part6 director, then continue EyeJudgement1.'
handoff['lastUpdatedAtUtc']=now
handoff_path.write_bytes(dump(handoff))
# Keep the project start guide's current checkpoint accurate and preserve historical sections.
start=BASE/'START_HERE.md'; txt=start.read_text(encoding='utf-8-sig'); lines=txt.splitlines()
latest='''# Active ordinary spell review129 — Calibration review part6

Information8 is fully applied: seven identities remain bound to their earlier accepted receipts, and Find the Path is accepted/applied from the exact Return03 recipient-view correction. Current authored coverage: **636 applied / 212 pending / 360 standalone / 173 scoped interfaces / 0 accepted-unapplied**. The exact 493MB director return, 199-check independent review, reversible view operation, retained terrain hold, acceptance and application receipts are preserved.

Find the Path now returns exactly “Indeterminate” after the real new inquiry. Missing surrounding topology and the unproved post-bar shortest-route qualification remain private; the protected-shorter-terrain positive case remains held. Continue with the existing EyeJudgement1 conference, then all212 current pending identities. Preserve the closed feats335, completed16/72 and all other accepted cohorts.

Read `docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_129.json`, `INFORMATION8_EXACT_ACCEPTANCE_129.json`, `INFORMATION8_FINDTHEPATH_APPLICATION_129.json`, `INFORMATION8_FINDPATH_APPLICATION_VALIDATION_129.json`, `CURRENT212_PENDING_IDENTITY_AUDIT_129.json`, and `spell-review-resume-116/CURRENT_SPELL_QUEUE_129.json`. Continue in Calibration review part6, ChatGPT6adc506d-8770-83ea-b64c-0345d9b9b682. All runtime/human/balance/cosmology/temporal/release holds remain.'''
# Replace the current status block up to the next historical checkpoint heading.
cut=next((i for i,line in enumerate(lines) if line.startswith('**Latest checkpoint:')),None)
assert cut is not None and lines[0].startswith('# Active ordinary spell review129')
start.write_text(latest+'\n\n'+'\n'.join(lines[cut:])+'\n',encoding='utf-8',newline='\n')
# Validate index row and unrelated entries after application.
final_bytes=IDX.read_bytes(); final=json.loads(final_bytes.decode('utf-8-sig'))
finalrow=next(e for e in final['entries'] if e['id']=='find-the-path')
assert final['authoredCounts']=={'reviewed':636,'pending':212} and final['representationCounts']['completeReviewedStandaloneProcedures']==360
assert finalrow['authoredStatus']=='reviewed-authored-operational-playtest' and finalrow['sourceStatus']==before_row['sourceStatus'] and finalrow['wholeCardPointer']=='/completeProcedures/0'
assert sum(1 for a,b in zip(old_entries,final['entries']) if a!=b)==1
checks={'id':'INFORMATION8-FINDPATH-APPLICATION-VALIDATION-129','passed':True,'acceptedIdentitiesApplied':1,'unrelatedIndexEntriesUnchanged':847,'FindPathSourceStatusPreserved':True,'all156DeliveredArchiveMembersExact':True,'fullCandidateEvidenceExtractedWithoutExecutingSuppliedFiles':True,'canonicalModelExactAcceptedProcedure':True,'acceptedCaseIds':['DI6-04-A','DI6-04-B'],'forwardReverseIndexOperations':8,'sourceCatalogHashUnchanged':final['sourceCatalogSha256']==old['sourceCatalogSha256'],'standaloneEnvelopeHashUnchanged':final['standaloneEnvelopeSha256']==old['standaloneEnvelopeSha256'],'counts':{'reviewed':636,'pending':212},'representationCounts':{'preservedLegacyOperationalRecords':276,'completeReviewedStandaloneProcedures':360},'index':{'path':'DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json','bytes':len(final_bytes),'sha256':sha(final_bytes)},'applicationReceipt':{'path':'docs/audit/2026-10-08/full-game/director-spell-review-129/INFORMATION8_FINDTHEPATH_APPLICATION_129.json','bytes':len(app_bytes),'sha256':sha(app_bytes)},'acceptanceReceipt':{'path':'docs/audit/2026-10-08/full-game/director-spell-review-129/INFORMATION8_EXACT_ACCEPTANCE_129.json','bytes':len(acceptance_bytes),'sha256':sha(acceptance_bytes)},'runtimeSelectionEnabled':False}
VALID.write_bytes(dump(checks))
print(json.dumps({'status':'APPLIED','acceptedIds':['find-the-path'],'counts':checks['counts'],'representationCounts':checks['representationCounts'],'indexSha256':checks['index']['sha256'],'archiveSha256':app['sourceArchive']['sha256'],'manifestFilesPreserved':len(list(EVIDENCE.rglob('*'))),'validation':str(VALID),'next':'EyeJudgement1'},ensure_ascii=False,indent=2))
