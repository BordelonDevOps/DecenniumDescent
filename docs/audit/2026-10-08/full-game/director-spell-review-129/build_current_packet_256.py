import json,pathlib,hashlib,zlib,copy,zipfile
from datetime import datetime,timezone
now=datetime.now(timezone.utc).isoformat(timespec="seconds")
W=pathlib.Path(r'C:\Github\DecenniumDescent-review-push-134')
B=W/'docs/audit/2026-10-08/full-game/director-spell-review-129'
def bind(path):
    raw=(W/path).read_bytes()
    return {'path':path.replace('\\','/'),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'crc32':f'{zlib.crc32(raw)&0xffffffff:08x}'}
planPath='docs/audit/2026-10-08/full-game/director-spell-review-129/UNRAVEL_IDENTITY_MD196_B02_INTEGRATED_WITNESS_256.json'
planAuditPath='docs/audit/2026-10-08/full-game/director-spell-review-129/UNRAVEL_IDENTITY_MD196_B02_INTEGRATED_WITNESS_256_AUDIT.json'
replayPath='docs/audit/2026-10-08/full-game/director-spell-review-129/UNRAVEL_IDENTITY_MD196_B02_FORWARD_INVERSE_REPLAY_256.json'
replayAuditPath='docs/audit/2026-10-08/full-game/director-spell-review-129/UNRAVEL_IDENTITY_MD196_B02_FORWARD_INVERSE_REPLAY_256_AUDIT.json'
formPath='DescentReviewChanges/ReviewBible/data/playtest/druid_form_profiles.json'
pendingPath='docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT36_PENDING_IDENTITY_AUDIT_250.json'
indexPath='DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json'
catalogPath='DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json'
planBind=bind(planPath); planAuditBind=bind(planAuditPath); replayBind=bind(replayPath); replayAuditBind=bind(replayAuditPath); formBind=bind(formPath); pendingBind=bind(pendingPath)
idxBind=bind(indexPath); catBind=bind(catalogPath)
queue=json.loads((B/'CURRENT_SPELL_QUEUE_255.json').read_text(encoding='utf-8'))
queue.update({'id':'CURRENT-SPELL-QUEUE-256','recordedAtUtc':now,'supersedesQueue':'CURRENT_SPELL_QUEUE_255.json','status':'36_IDENTITIES_REMAIN_UNRAVEL_MD196_B02_PACKET256_READY_FOR_EXPLICIT_DIRECTOR_DECISION'})
queue['next']={'group':None,'pendingIds':[],'pendingCount':0,'status':'PACKET256_READY_FOR_GPT_DIRECTOR_RECHECK_AND_EXPLICIT_ACCEPTANCE_DECISION','nextAction':'SEND_UNRAVEL_INTEGRATED_WITNESS_AND_REPLAY_256_TO_GPT_DIRECTOR'}
queue['activeReview']={'identity':'unravel-identity','group':'rank9-memorydenial6','blocker':'MD196-B02','stage':'INTEGRATED_WITNESS_REPLAY_READY_FOR_DIRECTOR_RECHECK','plan':planBind,'planAudit':planAuditBind,'replay':replayBind,'replayAudit':replayAuditBind,'supplementalFormRegister':formBind,'sourcePacket241':queue.get('currentSourcePacket')}
queue['currentWitnessPlan']=planBind
queue['currentIntegratedReplay']=replayBind
queue['unreviewedPendingIds']=[]
queue['nextPendingIds']=[]
queue['pendingCount']=36
queuePath=B/'CURRENT_SPELL_QUEUE_256.json'
queuePath.write_text(json.dumps(queue,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
queueBind=bind(queuePath.relative_to(W).as_posix())
handoff=json.loads((B/'CURRENT_HANDOFF_255.json').read_text(encoding='utf-8'))
handoff.update({'id':'CURRENT-HANDOFF-256','recordedAtUtc':now,'status':'36_REMAIN_MD196_B02_PACKET256_READY_FOR_EXPLICIT_GPT_DECISION','nextStep':'Send packet256 to GPT for explicit Unravel acceptance decision after recheck. If held, resolve the listed correction. Apply only after explicit acceptance and an independent application audit; then request the next pending identity.'})
handoff['currentBlocker']={'identity':'unravel-identity','blockerId':'MD196-B02','stage':'INTEGRATED_WITNESS_AND_REPLAY_READY_FOR_GPT_DIRECTOR_RECHECK'}
handoff['currentWitnessPlan']=planBind
handoff['currentWitnessPlanAudit']=planAuditBind
handoff['currentIntegratedReplay']=replayBind
handoff['currentIntegratedReplayAudit']=replayAuditBind
handoff['supplementalLocalFormRegister']=formBind|{'status':'separately bound supplemental source; not a Packet241 member'}
handoff['currentQueueBinding']=queueBind
handoff['stateCorrection']={'id':'CURRENT-REVIEW-STATE-CORRECTION-256','path':'docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_REVIEW_STATE_CORRECTION_256.json'}
handoffPath=B/'CURRENT_HANDOFF_256.json'
handoffPath.write_text(json.dumps(handoff,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
handoffBind=bind(handoffPath.relative_to(W).as_posix())
correction=json.loads((B/'CURRENT_REVIEW_STATE_CORRECTION_255.json').read_text(encoding='utf-8'))
correction.update({'id':'CURRENT-REVIEW-STATE-CORRECTION-256','recordedAtUtc':now,'status':'PASS_CURRENT_WITNESS_AND_REPLAY_POINTERS_REFRESHED_HISTORICAL_RECORDS_PRESERVED','supersedes':'CURRENT_REVIEW_STATE_CORRECTION_255.json','oldRecordsPreservedByteForByte':True})
correction['corrections'].append({'field':'currentIntegratedReplay','priorValue':correction.get('currentIntegratedReplay'),'replacement':replayBind,'reason':'Replace the prior integrated replay pointer with the fully corrected source-bound Unravel Identity replay; no identity status change.'})
correction['corrections'].append({'field':'currentWitnessPlan','priorValue':correction.get('currentWitnessPlan'),'replacement':planBind,'reason':'Bind the corrected integrated witness plan; no identity status change.'})
correction['currentWitnessPlan']=planBind
correction['currentIntegratedReplay']=replayBind
correction['currentQueue']=queueBind
correction['currentHandoff']={'path':str(handoffPath.relative_to(W)).replace('\\','/')}
correction['currentIndexPendingAudit']=pendingBind
correction['supplementalLocalFormRegister']=formBind|{'status':'supplemental, outside Packet241'}
correction['sourceAuthority']={'path':'docs/audit/2026-10-08/full-game/director-spell-review-129/rank9_memorydenial6_current_source_241_prepared/DD_Rank9_MemoryDenial6_CurrentSource_241.zip','bytes':175700171,'sha256':'8a4aeeaa5d19470004dc7518cb0d986644c3f846fde43729c726823c47da018e','crc32':'379b4c0c'}
corrPath=B/'CURRENT_REVIEW_STATE_CORRECTION_256.json'
corrPath.write_text(json.dumps(correction,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
corrBind=bind(corrPath.relative_to(W).as_posix())
# Seal is acyclic: it binds finalized correction, handoff, queue, plan/replay, audit, current index/catalog and supplemental register.
seal={'id':'CURRENT-REVIEW-STATE-CORRECTION-SEAL-256','status':'PASS','correction':corrBind,'handoff':handoffBind,'queue':queueBind,'plan':planBind,'planAudit':planAuditBind,'replay':replayBind,'replayAudit':replayAuditBind,'index':idxBind,'catalog':catBind,'supplementalFormRegister':formBind,'historicalRecordsPreserved':True}
sealPath=B/'CURRENT_REVIEW_STATE_CORRECTION_SEAL_256.json'
sealPath.write_text(json.dumps(seal,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
sealBind=bind(sealPath.relative_to(W).as_posix())
# Submission packet with exact member list; Packet241 remains a previously attached source dependency and is not recopied.
members=[
(planPath,'current/UNRAVEL_IDENTITY_MD196_B02_INTEGRATED_WITNESS_256.json'),
(planAuditPath,'current/UNRAVEL_IDENTITY_MD196_B02_INTEGRATED_WITNESS_256_AUDIT.json'),
(replayPath,'current/UNRAVEL_IDENTITY_MD196_B02_FORWARD_INVERSE_REPLAY_256.json'),
(replayAuditPath,'current/UNRAVEL_IDENTITY_MD196_B02_FORWARD_INVERSE_REPLAY_256_AUDIT.json'),
(formPath,'supplemental_sources/druid_form_profiles.json'),
(pendingPath,'authority/CURRENT36_PENDING_IDENTITY_AUDIT_250.json'),
(str(queuePath.relative_to(W)).replace('\\','/'),'authority/CURRENT_SPELL_QUEUE_256.json'),
(str(handoffPath.relative_to(W)).replace('\\','/'),'authority/CURRENT_HANDOFF_256.json'),
(str(corrPath.relative_to(W)).replace('\\','/'),'authority/CURRENT_REVIEW_STATE_CORRECTION_256.json'),
(str(sealPath.relative_to(W)).replace('\\','/'),'authority/CURRENT_REVIEW_STATE_CORRECTION_SEAL_256.json')]
manifest={'id':'UNRAVEL-IDENTITY-MD196-B02-SUBMISSION-MANIFEST-256','status':'PREPARED_FOR_GPT_DIRECTOR_RECHECK_AND_EXPLICIT_UNRAVEL_ACCEPTANCE_DECISION','scope':['unravel-identity / MD196-B02 only'],'authority':{'reviewedApplied':812,'pending':36,'acceptedUnapplied':0,'acceptedThisPacket':[],'appliedThisPacket':[]},'priorSourcePacket241':{'path':'docs/audit/2026-10-08/full-game/director-spell-review-129/rank9_memorydenial6_current_source_241_prepared/DD_Rank9_MemoryDenial6_CurrentSource_241.zip','bytes':175700171,'sha256':'8a4aeeaa5d19470004dc7518cb0d986644c3f846fde43729c726823c47da018e','alreadyAttachedInGPTThread':True},'members':[],'decisionBoundary':'The packet requests a fresh review of the complete Unravel Identity witness, 45-transition forward/inverse replay and independent audits, plus an explicit accept-or-hold ruling for Unravel Identity / MD196-B02. UI196-CLOCK excludes the in-progress T5 end: the effect vents Dissonance at :30 but restores availability only at T6 END :36; familiar command permission is false at :30.1 and true after natural expiry at :36. The Arch Dispel branch records target-side removal at :28, linked to the successful helper check, while preserving actual termination :28 separately from scheduled natural expiry :36. Helper Actions remain spent through T1/T3 END, Detect Magic is recorded as ordinary detect-magic, and recharge ticks 2-to-1 at :30 then 1-to-0 at :36. Mind Blank remains conditional because the exact accepted duration procedure is not bound. No acceptance is inferred. Application remains deferred until explicit acceptance and independent application audit.'}
for src,dst in members: manifest['members'].append({'archivePath':dst,**bind(src)})
manifestPath=B/'UNRAVEL_IDENTITY_MD196_B02_SUBMISSION_MANIFEST_256.json'
manifestPath.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
zipPath=B/'DD_Rank9_MemoryDenial6_UnravelIdentity_IntegratedWitness_256.zip'
with zipfile.ZipFile(zipPath,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for src,dst in members: z.write(W/src,dst)
    z.write(manifestPath,'MANIFEST.json')
zipBind=bind(zipPath.relative_to(W).as_posix())
delivery={'id':'DD-RANK9-MEMORYDENIAL6-UNRAVEL-INTEGRATED-WITNESS-256-DELIVERY','status':'READY','archive':zipBind,'manifest':bind(manifestPath.relative_to(W).as_posix()),'members':manifest['members'],'packet241Dependency':manifest['priorSourcePacket241'],'acceptanceRequested':True,'applicationRequested':False}
deliveryPath=B/'DD_Rank9_MemoryDenial6_UnravelIdentity_IntegratedWitness_256_DELIVERY.json'
deliveryPath.write_text(json.dumps(delivery,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'queue':queueBind,'handoff':handoffBind,'correction':corrBind,'seal':sealBind,'manifest':bind(manifestPath.relative_to(W).as_posix()),'zip':zipBind,'delivery':bind(deliveryPath.relative_to(W).as_posix()),'members':len(members)},ensure_ascii=False,indent=2))
