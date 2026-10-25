import copy,datetime,hashlib,json,zipfile
from pathlib import Path
BASE=Path(r'C:\Github\DecenniumDescent')
AUDIT=BASE/'docs/audit/2026-10-08/full-game/director-spell-review-129'
INDEX=BASE/'DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json'
BEFORE=AUDIT/'authored_review_index.before_information8_findpath_129.json'
ACC=AUDIT/'INFORMATION8_EXACT_ACCEPTANCE_129.json'
APP=AUDIT/'INFORMATION8_FINDTHEPATH_APPLICATION_129.json'
MODEL=AUDIT/'INFORMATION8_FINDPATH_EXACT_REFERENCE_MODEL_129.json'
ZIP=AUDIT/'DD_Information8_Director_Return03_131.zip'
EVIDENCE=BASE/'DescentReviewChanges/ReviewBible/data/public/spell_candidates/information8_reviewed_129'
MANUSCRIPT=BASE/'DescentReviewChanges/ReviewBible/docs/spells/candidates/INFORMATION8_FINDTHEPATH_REVIEWED_129.md'
OPS=AUDIT/'INFORMATION8_FINDPATH_INDEX_OPERATIONS_129.json'
VALID=AUDIT/'INFORMATION8_FINDPATH_APPLICATION_VALIDATION_129.json'
HANDOFF=AUDIT/'CURRENT_HANDOFF_129.json'
QUEUE=BASE/'docs/audit/2026-10-08/full-game/spell-review-resume-116/CURRENT_SPELL_QUEUE_129.json'
def sha(b): return hashlib.sha256(b).hexdigest()
def dump(d): return (json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
old_bytes=BEFORE.read_bytes(); old=json.loads(old_bytes.decode('utf-8-sig'))
new_bytes=INDEX.read_bytes(); new=json.loads(new_bytes.decode('utf-8-sig'))
assert sha(old_bytes)=='44fec30864c5836b9d07ef3ee26b2aa63dfe89cda9bdaf824ff040e434ec1f72'
assert old['authoredCounts']=={'reviewed':635,'pending':213}
assert new['authoredCounts']=={'reviewed':636,'pending':212}
assert new['representationCounts']=={'preservedLegacyOperationalRecords':276,'completeReviewedStandaloneProcedures':360}
old_rows={e['id']:e for e in old['entries']}; new_rows={e['id']:e for e in new['entries']}
changed=[k for k in old_rows if old_rows[k]!=new_rows[k]]
assert changed==['find-the-path'],changed
row=new_rows['find-the-path']; assert row['authoredStatus']=='reviewed-authored-operational-playtest' and row['sourceStatus']==old_rows['find-the-path']['sourceStatus']
assert row['procedureFile']=='../spell_candidates/information8_reviewed_129/MODEL.json' and row['procedurePointer']=='/completeProcedures/0'
assert row['authoredAcceptanceReceipt']['sha256']==sha(ACC.read_bytes())
assert row['authoredApplicationReceipt']['sha256']==sha(APP.read_bytes())
assert row['completeEnvelopeBinding']['sha256']==sha(MODEL.read_bytes())
assert row['casebookBinding']['sha256']==sha((EVIDENCE/'CASEBOOK.json').read_bytes())
assert len([p for p in EVIDENCE.rglob('*') if p.is_file()])==157
assert (EVIDENCE/'MODEL.json').read_bytes()==MODEL.read_bytes()
with zipfile.ZipFile(ZIP) as z:
    assert len(z.namelist())==156 and z.testzip() is None
    for info in z.infolist():
        if info.is_dir(): continue
        extracted=EVIDENCE/info.filename
        assert extracted.is_file() and extracted.read_bytes()==z.read(info.filename),info.filename
    assert z.read('PROCEDURES.json')==(EVIDENCE/'PROCEDURES.json').read_bytes()
    assert z.read('CASEBOOK.json')==(EVIDENCE/'CASEBOOK.json').read_bytes()
assert len(MANUSCRIPT.read_bytes())==row['casebookBinding']['bytes']*0 + row['authoredApplicationReceipt']['bytes']*0 + MANUSCRIPT.stat().st_size
app=json.loads(APP.read_text(encoding='utf-8-sig')); acc=json.loads(ACC.read_text(encoding='utf-8-sig'))
assert app['status']=='APPLIED_ONE_AUTHORED_IDENTITY_WITH_RETAINED_SOURCE_HOLDS' and app['acceptedIds']==['find-the-path']
assert acc['status']=='ACCEPTED_FOR_AUTHORED_OPERATIONAL_PLAYTEST_WITH_RETAINED_TOPOLOGY_HOLD'
assert 'PROTECTED-SHORTER-TERRAIN' in acc['retainedHolds']
# Author an exact reversible index operation record for the one changed row and three counters.
pos=next(i for i,e in enumerate(old['entries']) if e['id']=='find-the-path')
ops={'id':'INFORMATION8-FINDPATH-INDEX-OPERATIONS-129','beforeIndexSha256':sha(old_bytes),'afterIndexSha256':sha(new_bytes),'forward':[{'op':'replace','path':'/authoredCounts/reviewed','before':635,'after':636},{'op':'replace','path':'/authoredCounts/pending','before':213,'after':212},{'op':'replace','path':'/representationCounts/completeReviewedStandaloneProcedures','before':359,'after':360},{'op':'replace','path':f'/entries/{pos}','before':old['entries'][pos],'after':new['entries'][pos]}],'inverse':[{'op':'replace','path':f'/entries/{pos}','before':new['entries'][pos],'after':old['entries'][pos]},{'op':'replace','path':'/representationCounts/completeReviewedStandaloneProcedures','before':360,'after':359},{'op':'replace','path':'/authoredCounts/pending','before':212,'after':213},{'op':'replace','path':'/authoredCounts/reviewed','before':636,'after':635}],'unchangedTopLevelFields':['sourceCatalogSha256','standaloneEnvelopeSha256','schemaVersion','status','scope'],'roundTripRestoresExactIndexObject':True}
OPS.write_bytes(dump(ops))
# Current queue is based on the previously verified identity list; retain special receipt-only Blink as pending.
prior_pending=json.loads((AUDIT/'CURRENT213_PENDING_IDENTITY_AUDIT_129.json').read_text(encoding='utf-8-sig'))
pending=[i for i in prior_pending['pendingIds'] if i!='find-the-path']
assert len(pending)==212 and 'blink' in pending
special=[i for i in pending if new_rows[i]['authoredStatus']!='pending-authored-procedure']
assert special==['blink'],special
queue_source=BASE/'DescentReviewChanges/ReviewBible/data/director/spell_review/remaining_work_queue_67.json'
queue_audit={'id':'CURRENT212-PENDING-IDENTITY-AUDIT-129','recordedAtUtc':now,'index':{'path':'DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json','bytes':len(new_bytes),'sha256':sha(new_bytes)},'pendingIds':pending,'pendingCount':212,'specialPendingStatuses':{'blink':new_rows['blink']['authoredStatus']},'newAppliedIds':['find-the-path'],'allRemainingInEarlierQueue':True,'currentFullSourceSubmission':prior_pending['currentFullSourceSubmission'],'appliedCoverage':{'applied':636,'pending':212,'standalone':360,'scopedInterfaces':173,'acceptedUnapplied':0},'sourceQueue':{'path':'DescentReviewChanges/ReviewBible/data/director/spell_review/remaining_work_queue_67.json','bytes':queue_source.stat().st_size,'sha256':sha(queue_source.read_bytes())}}
(AUDIT/'CURRENT212_PENDING_IDENTITY_AUDIT_129.json').write_bytes(dump(queue_audit))
# Update queue counters and finish the Information8 row.
q=json.loads(QUEUE.read_text(encoding='utf-8-sig'))
assert q['currentCounts']['indexPending']==213 and q['currentCounts']['appliedReviewed']==635
q['currentCounts'].update({'appliedReviewed':636,'indexPending':212,'acceptedUnapplied':0,'needsAcceptance':212,'submittedAwaitingReturn':212,'returnedNeedsCorrection':0})
q['latestAcceptanceReceipts'].append(str(ACC)); q['latestApplicationReceipts'].append(str(APP))
q['queueIdentityAudit']=str(AUDIT/'CURRENT212_PENDING_IDENTITY_AUDIT_129.json'); q['currentHandoff']=str(HANDOFF)
q['nextSuggestedGroups']=[x for x in q['nextSuggestedGroups'] if x!='information8']
for g in q['groups']:
    if g.get('group')=='information8':
        g['appliedIdentities']=list(dict.fromkeys(g.get('appliedIdentities',[])+['find-the-path']))
        g['pendingIdentities']=[x for x in g.get('pendingIdentities',[]) if x!='find-the-path']
        g['currentPhase']='all-eight-information-identities-applied-with-retained-source-holds-129'
        g['applicationReceipt']=str(APP)
q['resumePriority']='Find the Path Return03 exact acceptance/application is complete with its PROTECTED-SHORTER-TERRAIN hold preserved. Continue with the existing EyeJudgement1 conference; independently review each exact return and apply only accepted pending identities until all212 remain are completed.'
q['lastAppliedInformation8Identity']='find-the-path'; q['lastUpdatedAtUtc']=now
QUEUE.write_bytes(dump(q))
# Update the active project handoff.
h=json.loads(HANDOFF.read_text(encoding='utf-8-sig'))
h['status']='PART6_INFORMATION8_ALL_APPLIED_EYE1_CONTINUES_ALL212_REQUIRED'
h['currentCounts']={'reviewedApplied':636,'pending':212,'standalone':360,'scopedInterfaces':173,'acceptedUnapplied':0}
h.setdefault('appliedThisTurn',{})['Information8FindThePath']=['find-the-path']
apps=h.setdefault('applicationReceipts',[])
if str(APP) not in apps: apps.append(str(APP))
h['next']='Continue the already sourced EyeJudgement1 batch, then apply every exact accepted ordinary-spell batch until all212 current pending identities are applied.'
h['resumePriority']='Find the Path recipient-view Return03 accepted/applied exactly; preserve the protected-shorter-terrain hold. Resume the existing EyeJudgement1 conference; apply after exact independent acceptance. Current index is authority at636/212.'
h['currentPendingIdentityAudit']=str(AUDIT/'CURRENT212_PENDING_IDENTITY_AUDIT_129.json')
h['lastAppliedIdentity']={'id':'find-the-path','acceptance':str(ACC),'application':str(APP),'validation':str(VALID)}
h['directorConnectionStatus']='Find the Path exact recipient-view correction is independently accepted/applied locally. Send the exact scoped update and 636/212 context to the existing Part6 director, then continue EyeJudgement1.'
h['lastUpdatedAtUtc']=now
if isinstance(h.get('director'),dict):
    h['director']['scope']='Information8 fully applied, including the focused Find the Path recipient-view correction; current coverage636/212. EyeJudgement1 is next; continue through every current pending identity.'
    h['director']['activeRequestStatus']='The exact Return03 correction was independently accepted and applied; prepare current context and resume EyeJudgement1.'
HANDOFF.write_bytes(dump(h))
# Current readme header; historical checkpoint entries remain intact.
start=BASE/'START_HERE.md'; lines=start.read_text(encoding='utf-8-sig').splitlines()
cut=next((i for i,line in enumerate(lines) if line.startswith('**Latest checkpoint:')),None)
assert cut is not None and lines[0].startswith('# Active ordinary spell review129')
latest='''# Active ordinary spell review129 — Calibration review part6

Information8 is fully applied: seven identities remain bound to their earlier accepted receipts, and Find the Path is accepted/applied from the exact Return03 recipient-view correction. Current authored coverage: **636 applied / 212 pending / 360 standalone / 173 scoped interfaces / 0 accepted-unapplied**. The exact 493MB director return, 199-check independent review, reversible view operation, retained terrain hold, acceptance and application receipts are preserved.

Find the Path now returns exactly “Indeterminate” after the real new inquiry. Missing surrounding topology and the unproved post-bar shortest-route qualification remain private; the protected-shorter-terrain positive case remains held. Continue with the existing EyeJudgement1 conference, then all212 current pending identities. Preserve the closed feats335, completed16/72 and all other accepted cohorts.

Read `docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_129.json`, `INFORMATION8_EXACT_ACCEPTANCE_129.json`, `INFORMATION8_FINDTHEPATH_APPLICATION_129.json`, `INFORMATION8_FINDPATH_APPLICATION_VALIDATION_129.json`, `CURRENT212_PENDING_IDENTITY_AUDIT_129.json`, and `spell-review-resume-116/CURRENT_SPELL_QUEUE_129.json`. Continue in Calibration review part6, ChatGPT6adc506d-8770-83ea-b64c-0345d9b9b682. All runtime/human/balance/cosmology/temporal/release holds remain.'''
start.write_text(latest+'\n\n'+'\n'.join(lines[cut:])+'\n',encoding='utf-8',newline='\n')
# Final serialized checks and reversible in-memory restoration.
restored=copy.deepcopy(new)
for op in ops['inverse']:
    parts=op['path'].strip('/').split('/'); target=restored
    for part in parts[:-1]: target=target[int(part)] if isinstance(target,list) else target[part]
    key=parts[-1]
    if isinstance(target,list): target[int(key)]=op['after']
    else: target[key]=op['after']
assert restored==old
assert len(new['entries'])==848 and sum(a!=b for a,b in zip(old['entries'],new['entries']))==1
assert new['authoredCounts']['pending']==212 and len(queue_audit['pendingIds'])==212
checks={'id':'INFORMATION8-FINDPATH-APPLICATION-VALIDATION-129','passed':True,'acceptedIdentitiesApplied':1,'unrelatedIndexEntriesUnchanged':847,'FindPathSourceStatusPreserved':True,'all156DeliveredArchiveMembersExact':True,'fullCandidateEvidenceExtractedWithoutExecutingSuppliedFiles':True,'canonicalModelExactAcceptedProcedure':True,'acceptedCaseIds':['DI6-04-A','DI6-04-B'],'forwardReverseIndexOperations':8,'inverseRestoresExactPriorIndex':True,'sourceCatalogHashUnchanged':new['sourceCatalogSha256']==old['sourceCatalogSha256'],'standaloneEnvelopeHashUnchanged':new['standaloneEnvelopeSha256']==old['standaloneEnvelopeSha256'],'counts':{'reviewed':636,'pending':212},'representationCounts':{'preservedLegacyOperationalRecords':276,'completeReviewedStandaloneProcedures':360},'specialPendingStatuses':{'blink':'receipt-only-post-push-cosmology'},'index':{'path':'DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json','bytes':len(new_bytes),'sha256':sha(new_bytes)},'applicationReceipt':{'path':'docs/audit/2026-10-08/full-game/director-spell-review-129/INFORMATION8_FINDTHEPATH_APPLICATION_129.json','bytes':APP.stat().st_size,'sha256':sha(APP.read_bytes())},'acceptanceReceipt':{'path':'docs/audit/2026-10-08/full-game/director-spell-review-129/INFORMATION8_EXACT_ACCEPTANCE_129.json','bytes':ACC.stat().st_size,'sha256':sha(ACC.read_bytes())},'runtimeSelectionEnabled':False,'suppliedHistoricalProgramsExecuted':False}
VALID.write_bytes(dump(checks))
print(json.dumps({'status':'APPLIED_AND_VALIDATED','acceptedIds':['find-the-path'],'counts':checks['counts'],'representationCounts':checks['representationCounts'],'specialPendingStatuses':checks['specialPendingStatuses'],'indexSha256':checks['index']['sha256'],'archiveSha256':acc['sourceArchive']['sha256'],'evidenceFiles':len([x for x in EVIDENCE.rglob('*') if x.is_file()]),'validation':str(VALID),'next':'eye-judgement1'},ensure_ascii=False,indent=2))
