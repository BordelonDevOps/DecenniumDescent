import json,pathlib,hashlib,zlib,copy,zipfile
W=pathlib.Path(r'C:\Github\DecenniumDescent-review-push-134')
B=W/'docs/audit/2026-10-08/full-game/director-spell-review-129'
def bind(path):
    raw=(W/path).read_bytes()
    return {'path':path.replace('\\','/'),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'crc32':f'{zlib.crc32(raw)&0xffffffff:08x}'}
planPath='docs/audit/2026-10-08/full-game/director-spell-review-129/UNRAVEL_IDENTITY_MD196_B02_INTEGRATED_WITNESS_252.json'
planAuditPath='docs/audit/2026-10-08/full-game/director-spell-review-129/UNRAVEL_IDENTITY_MD196_B02_INTEGRATED_WITNESS_252_AUDIT.json'
replayPath='docs/audit/2026-10-08/full-game/director-spell-review-129/UNRAVEL_IDENTITY_MD196_B02_FORWARD_INVERSE_REPLAY_253.json'
replayAuditPath='docs/audit/2026-10-08/full-game/director-spell-review-129/UNRAVEL_IDENTITY_MD196_B02_FORWARD_INVERSE_REPLAY_253_AUDIT.json'
formPath='DescentReviewChanges/ReviewBible/data/playtest/druid_form_profiles.json'
pendingPath='docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT36_PENDING_IDENTITY_AUDIT_250.json'
indexPath='DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json'
catalogPath='DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json'
planBind=bind(planPath); planAuditBind=bind(planAuditPath); replayBind=bind(replayPath); replayAuditBind=bind(replayAuditPath); formBind=bind(formPath); pendingBind=bind(pendingPath)
idxBind=bind(indexPath); catBind=bind(catalogPath)
queue=json.loads((B/'CURRENT_SPELL_QUEUE_251.json').read_text(encoding='utf-8'))
queue.update({'id':'CURRENT-SPELL-QUEUE-252','recordedAtUtc':'2026-10-30T11:57:00+00:00','supersedesQueue':'CURRENT_SPELL_QUEUE_251.json','status':'36_IDENTITIES_REMAIN_UNRAVEL_MD196_B02_INTEGRATED_WITNESS_READY_FOR_DIRECTOR_RECHECK'})
queue['next']={'group':None,'pendingIds':[],'pendingCount':0,'status':'INTEGRATED_WITNESS_AND_REPLAY_PREPARED_FOR_GPT_DIRECTOR_RECHECK','nextAction':'SEND_UNRAVEL_INTEGRATED_WITNESS_252_AND_REVERSIBLE_REPLAY_253_TO_GPT_DIRECTOR'}
queue['activeReview']={'identity':'unravel-identity','group':'rank9-memorydenial6','blocker':'MD196-B02','stage':'INTEGRATED_WITNESS_REPLAY_READY_FOR_DIRECTOR_RECHECK','plan':planBind,'planAudit':planAuditBind,'replay':replayBind,'replayAudit':replayAuditBind,'supplementalFormRegister':formBind,'sourcePacket241':queue.get('currentSourcePacket')}
queue['currentWitnessPlan']=planBind
queue['currentIntegratedReplay']=replayBind
queue['unreviewedPendingIds']=[]
queue['nextPendingIds']=[]
queue['pendingCount']=36
queuePath=B/'CURRENT_SPELL_QUEUE_252.json'
queuePath.write_text(json.dumps(queue,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
queueBind=bind(queuePath.relative_to(W).as_posix())
handoff=json.loads((B/'CURRENT_HANDOFF_251.json').read_text(encoding='utf-8'))
handoff.update({'id':'CURRENT-HANDOFF-252','recordedAtUtc':'2026-10-30T11:57:00+00:00','status':'36_REMAIN_MD196_B02_INTEGRATED_WITNESS_REPLAY_READY_FOR_GPT','nextStep':'Send the source-bound integrated witness and reversible replay to GPT. Resolve the Mind Blank duration and Arch Dispel perceivability rulings, then continue only through exact director acceptance and independent application audit.'})
handoff['currentBlocker']={'identity':'unravel-identity','blockerId':'MD196-B02','stage':'INTEGRATED_WITNESS_AND_REPLAY_READY_FOR_GPT_DIRECTOR_RECHECK'}
handoff['currentWitnessPlan']=planBind
handoff['currentWitnessPlanAudit']=planAuditBind
handoff['currentIntegratedReplay']=replayBind
handoff['currentIntegratedReplayAudit']=replayAuditBind
handoff['supplementalLocalFormRegister']=formBind|{'status':'separately bound supplemental source; not a Packet241 member'}
handoff['currentQueueBinding']=queueBind
handoff['stateCorrection']={'id':'CURRENT-REVIEW-STATE-CORRECTION-252','path':'docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_REVIEW_STATE_CORRECTION_252.json'}
handoffPath=B/'CURRENT_HANDOFF_252.json'
handoffPath.write_text(json.dumps(handoff,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
handoffBind=bind(handoffPath.relative_to(W).as_posix())
correction=json.loads((B/'CURRENT_REVIEW_STATE_CORRECTION_251.json').read_text(encoding='utf-8'))
correction.update({'id':'CURRENT-REVIEW-STATE-CORRECTION-252','recordedAtUtc':'2026-10-30T11:57:00+00:00','status':'PASS_CURRENT_WITNESS_AND_REPLAY_POINTERS_REFRESHED_HISTORICAL_RECORDS_PRESERVED','supersedes':'CURRENT_REVIEW_STATE_CORRECTION_251.json','oldRecordsPreservedByteForByte':True})
correction['corrections'].append({'field':'currentIntegratedReplay','priorValue':None,'replacement':replayBind,'reason':'Add the newly source-bound Unravel Identity reversible state replay; no identity status change.'})
correction['corrections'][3]['replacement']=planBind
correction['currentWitnessPlan']=planBind
correction['currentIntegratedReplay']=replayBind
correction['currentQueue']=queueBind
correction['currentHandoff']={'path':str(handoffPath.relative_to(W)).replace('\\','/')}
correction['currentIndexPendingAudit']=pendingBind
correction['supplementalLocalFormRegister']=formBind|{'status':'supplemental, outside Packet241'}
correction['sourceAuthority']={'path':'docs/audit/2026-10-08/full-game/director-spell-review-129/rank9_memorydenial6_current_source_241_prepared/DD_Rank9_MemoryDenial6_CurrentSource_241.zip','bytes':175700171,'sha256':'8a4aeeaa5d19470004dc7518cb0d986644c3f846fde43729c726823c47da018e','crc32':'379b4c0c'}
corrPath=B/'CURRENT_REVIEW_STATE_CORRECTION_252.json'
corrPath.write_text(json.dumps(correction,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
corrBind=bind(corrPath.relative_to(W).as_posix())
# Seal is acyclic: it binds finalized correction, handoff, queue, plan/replay, audit, current index/catalog and supplemental register.
seal={'id':'CURRENT-REVIEW-STATE-CORRECTION-SEAL-252','status':'PASS','correction':corrBind,'handoff':handoffBind,'queue':queueBind,'plan':planBind,'planAudit':planAuditBind,'replay':replayBind,'replayAudit':replayAuditBind,'index':idxBind,'catalog':catBind,'supplementalFormRegister':formBind,'historicalRecordsPreserved':True}
sealPath=B/'CURRENT_REVIEW_STATE_CORRECTION_SEAL_252.json'
sealPath.write_text(json.dumps(seal,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
sealBind=bind(sealPath.relative_to(W).as_posix())
# Submission packet with exact member list; Packet241 remains a previously attached source dependency and is not recopied.
members=[
(planPath,'current/UNRAVEL_IDENTITY_MD196_B02_INTEGRATED_WITNESS_252.json'),
(planAuditPath,'current/UNRAVEL_IDENTITY_MD196_B02_INTEGRATED_WITNESS_252_AUDIT.json'),
(replayPath,'current/UNRAVEL_IDENTITY_MD196_B02_FORWARD_INVERSE_REPLAY_253.json'),
(replayAuditPath,'current/UNRAVEL_IDENTITY_MD196_B02_FORWARD_INVERSE_REPLAY_253_AUDIT.json'),
(formPath,'supplemental_sources/druid_form_profiles.json'),
(pendingPath,'authority/CURRENT36_PENDING_IDENTITY_AUDIT_250.json'),
(str(queuePath.relative_to(W)).replace('\\','/'),'authority/CURRENT_SPELL_QUEUE_252.json'),
(str(handoffPath.relative_to(W)).replace('\\','/'),'authority/CURRENT_HANDOFF_252.json'),
(str(corrPath.relative_to(W)).replace('\\','/'),'authority/CURRENT_REVIEW_STATE_CORRECTION_252.json'),
(str(sealPath.relative_to(W)).replace('\\','/'),'authority/CURRENT_REVIEW_STATE_CORRECTION_SEAL_252.json')]
manifest={'id':'UNRAVEL-IDENTITY-MD196-B02-SUBMISSION-MANIFEST-253','status':'PREPARED_FOR_GPT_DIRECTOR_RECHECK','scope':['unravel-identity / MD196-B02 only'],'authority':{'reviewedApplied':812,'pending':36,'acceptedUnapplied':0,'acceptedThisPacket':[],'appliedThisPacket':[]},'priorSourcePacket241':{'path':'docs/audit/2026-10-08/full-game/director-spell-review-129/rank9_memorydenial6_current_source_241_prepared/DD_Rank9_MemoryDenial6_CurrentSource_241.zip','bytes':175700171,'sha256':'8a4aeeaa5d19470004dc7518cb0d986644c3f846fde43729c726823c47da018e','alreadyAttachedInGPTThread':True},'members':[],'decisionBoundary':'Static actor/procedure/replay only. Requests rulings on Earth Warden profile, UI251-FORM-LOSS, familiar callback, end-turn Dissonance, Mind Blank persistence, and Arch Dispel perceivability. No acceptance/application requested from this packet.'}
for src,dst in members: manifest['members'].append({'archivePath':dst,**bind(src)})
manifestPath=B/'UNRAVEL_IDENTITY_MD196_B02_SUBMISSION_MANIFEST_253.json'
manifestPath.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
zipPath=B/'DD_Rank9_MemoryDenial6_UnravelIdentity_IntegratedWitness_253.zip'
with zipfile.ZipFile(zipPath,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for src,dst in members: z.write(W/src,dst)
    z.write(manifestPath,'MANIFEST.json')
zipBind=bind(zipPath.relative_to(W).as_posix())
delivery={'id':'DD-RANK9-MEMORYDENIAL6-UNRAVEL-INTEGRATED-WITNESS-253-DELIVERY','status':'READY','archive':zipBind,'manifest':bind(manifestPath.relative_to(W).as_posix()),'members':manifest['members'],'packet241Dependency':manifest['priorSourcePacket241'],'acceptanceRequested':False,'applicationRequested':False}
deliveryPath=B/'DD_Rank9_MemoryDenial6_UnravelIdentity_IntegratedWitness_253_DELIVERY.json'
deliveryPath.write_text(json.dumps(delivery,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'queue':queueBind,'handoff':handoffBind,'correction':corrBind,'seal':sealBind,'manifest':bind(manifestPath.relative_to(W).as_posix()),'zip':zipBind,'delivery':bind(deliveryPath.relative_to(W).as_posix()),'members':len(members)},ensure_ascii=False,indent=2))
