import hashlib,json,pathlib,subprocess
REPO=pathlib.Path(r'C:\ep480fix')
BASE='3236606a65bb54d7bd1f1156c106e3aef2cb3d08'
ANCHOR='38fec0bbf19a4480098eb10ab0d992b055790ada'
AUDIT='docs/audit/2026-10-08/full-game/director-spell-review-129/'
CAND='DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9timefate6_reviewed_192/'
CAT='DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json'
IDX='DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json'
QUEUE=AUDIT+'CURRENT_SPELL_QUEUE_481.json'
HANDOFF=AUDIT+'CURRENT_HANDOFF_481.json'
PENDING=AUDIT+'CURRENT12_PENDING_IDENTITY_AUDIT_481.json'
FATE_RECON=AUDIT+'fate_rewrite_identity_reconciliation_2026-11-03/'
FATE_WITNESS=AUDIT+'fate_rewrite_ep480_interface_witness_2026-11-03/'
COLLAPSE=AUDIT+'collapse_timeline_current_authority_review_2026-11-03/'
EP=AUDIT+'eternal_prophecy_identity_reconciliation_2026-11-02/'
R320=AUDIT+'rank9_fate_rewrite_return320_received/'
R323=AUDIT+'rank9_eternal_prophecy_return323_received/'
OUT=REPO/pathlib.Path(AUDIT+'fate_rewrite_static_identity_disposition_2026-11-03')

def git(*args):return subprocess.check_output(['git','-C',str(REPO),*args])
def raw(commit,path):return git('show',f'{commit}:{path}')
def j(commit,path):return json.loads(raw(commit,path).decode('utf-8-sig'))
def blob(commit,path):return git('rev-parse',f'{commit}:{path}').decode().strip()
def sh(data):return hashlib.sha256(data).hexdigest()
def write(name,obj):
 p=OUT/name;p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');return p
OUT.mkdir(parents=True,exist_ok=True)

queue=j(BASE,QUEUE);handoff=j(BASE,HANDOFF);pending=j(BASE,PENDING)
catalog=j(BASE,CAT);index=j(BASE,IDX)
catrow=next(r for r in catalog['spells'] if r['id']=='fate-rewrite')
idxrow=next(r for r in index['entries'] if r['id']=='fate-rewrite')
catptr=f"/spells/{catalog['spells'].index(catrow)}";idxptr=f"/entries/{index['entries'].index(idxrow)}"
proc=j(BASE,CAND+'procedures/fate-rewrite.json')
recon_path=FATE_RECON+'FATE_REWRITE_IDENTITY_RECONCILIATION_01.json'
recon=j(BASE,recon_path)
recon_pass_path=FATE_RECON+'CODEX_TRANSCRIBED_DIRECTOR_REVIEW_PASS_FATE_REWRITE_IDENTITY_01.json'
recon_pass=j(BASE,recon_pass_path)
recon_manifest_path=FATE_RECON+'PACKET_MANIFEST_FATE_REWRITE_IDENTITY_01.json'
recon_manifest=j(BASE,recon_manifest_path)
witness_pass_path=FATE_WITNESS+'CODEX_TRANSCRIBED_DIRECTOR_REVIEW_PASS_03.json'
witness_pass=j(BASE,witness_pass_path)
r320_decision=j(BASE,R320+'DIRECTOR_DECISION.json')
r320_b04=j(BASE,R320+'BLOCKER_REASSESSMENT.json')
r323_b02=j(BASE,R323+'BLOCKER_REASSESSMENT.json')
r322_b05=j(BASE,AUDIT+'rank9_collapse_timeline_return322_received/BLOCKER_REASSESSMENT.json')
collapse_pass_path=COLLAPSE+'CODEX_TRANSCRIBED_DIRECTOR_REVIEW_PASS_COLLAPSE_TIMELINE_CURRENT_AUTHORITY_01.json'
collapse_pass=j(BASE,collapse_pass_path)
ep_accept_path=EP+'CODEX_TRANSCRIBED_DIRECTOR_IDENTITY_ACCEPTANCE_EP480_01.json'
ep_accept=j(BASE,ep_accept_path)
ep_application_path=EP+'APPLICATION_EP480_STATIC_01.json'
ep_application=j(BASE,ep_application_path)

assert queue['currentAuthority']['reviewedApplied']==836 and queue['currentAuthority']['pending']==12 and queue['currentAuthority']['acceptedUnapplied']==0
assert queue['nextIdentity']=='fate-rewrite' and queue['nextBlockerIds']==['TF192-B04'] and queue['nextDependencyIds']==['TF192-B02']
assert queue['continuingPriorityOrder'][:2]==['fate-rewrite','collapse-timeline']
assert sh(raw(BASE,CAT))==queue['currentCatalogBinding']['sha256'] and len(raw(BASE,CAT))==queue['currentCatalogBinding']['bytes']
assert sh(raw(BASE,IDX))==queue['currentIndexBinding']['sha256'] and len(raw(BASE,IDX))==queue['currentIndexBinding']['bytes']
assert catrow['status']=='blocked-pending-operational-review' and catrow['operational'] is None
assert idxrow['authoredStatus']=='pending-authored-procedure'
assert proc['accepted'] is False and proc['applied'] is False and proc['blockerIds']==['TF192-B04']
assert 'TF192-B04' in proc['holdIds'] and 'TF192-H-HISTORY' in proc['holdIds'] and 'TF192-H-DEATH' in proc['holdIds']
assert proc['currentCatalogSourceAndAccessUnchanged']==catrow and proc['currentIndexEntryUnchanged']==idxrow
assert recon_pass['disposition']=='PASS_STATIC_AUTHORED_PROCEDURE_REVIEW_ONLY_RECONCILIATION'
assert recon_pass['reviewedCommit']=='4cf33ffbd0a1eb51be5ac13c0709f4e2af9b87d3'
assert recon_pass['reconciliation']['sha256']=='7cda9e3f14afd8a1254b81c37e13eda72495b41af97c3928cdef07c5df45ea8b'
assert recon_pass['scopeLimits']['identityAccepted'] is False and recon_pass['scopeLimits']['identityApplied'] is False
assert recon_pass['verified']['B02AndB04RemainOpen'] is True
assert r320_b04['status']=='OPEN' and r323_b02['status']=='OPEN'
assert len(r323_b02['missingWitnessParts'])==3
assert collapse_pass['disposition']=='PASS_STATIC_CURRENT_AUTHORITY_RECONCILIATION_ONLY'
assert ep_accept['decision']['disposition']=='ACCEPT' and ep_application['status']=='APPLIED_TO_AUTHORED_REVIEW_INDEX_ONLY'

status={
 'schemaVersion':1,
 'id':'CODEX-TRANSCRIBED-DIRECTOR-STATUS-POST-COLLAPSE-TIMELINE-CURRENT-AUTHORITY-PASS-01',
 'classification':'CODEX_TRANSCRIPTION_OF_GPT_DIRECTOR_BROWSER_STATUS_NOT_DIRECTOR_NATIVE_FILE',
 'recordedAtUtc':'2026-11-03T04:10:33Z',
 'sourceConversationUrl':'https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6adc506d-8770-83ea-b64c-0345d9b9b682',
 'reviewedCommit':'fc208cf98f51d5bb19ef58e6a85e2af061ed07e5',
 'reviewedPacketSha256':'e9fb888a01d5060fdd7e90e7501f8c04711329c21a27c39bedaeab330685c273',
 'collapseTimelineReadOnlyReviewComplete':True,
 'noCorrectionOrRepeatedReviewRequired':True,
 'newSourceInspectionAgainstB05B02Permitted':True,
 'newBranchOrPremisesAuthorized':False,
 'blockerStatus':{'TF192-B05':'OPEN','TF192-B02':'OPEN'},
 'minimumEvidence':{
  'TF192-B05':r322_b05['minimumMissingWitness'],
  'TF192-B05CurrentRequirement':j(BASE,AUDIT+'rank9_collapse_timeline_return322_received/BLOCKER_REASSESSMENT.json')['minimumMissingWitness'],
  'TF192-B02CurrentRequirement':r323_b02['minimumMissingWitness'],
  'TF192-B02MissingWitnessParts':[{'id':x['id'],'requirement':x['requirement']} for x in r323_b02['missingWitnessParts']]
 },
 'authorizationBoundary':{
  'existingSourceInspectionNeedsNewOwnerAdoption':False,
  'exceptionalMechanismOrObligationRevisionRequiresScopedAuthorization':True,
  'nativePromiseQualificationRequiresScopedOwnerDecision':True,
  'newCollapseSpecificHypotheticalBranchRequiresScopedAuthorization':True
 },
 'nextReviewTask':{
  'identity':'fate-rewrite',
  'queuePosition':1,
  'action':'Request separate identity-level disposition for STATIC_AUTHORED_PROCEDURE_REVIEW_ONLY using the already-passed reconciliation.',
  'reconciliationSha256':'7cda9e3f14afd8a1254b81c37e13eda72495b41af97c3928cdef07c5df45ea8b',
  'noNewWitnessConstructionOrPremiseAdoption':True,
  'acceptanceDoesNotAutoAdvanceQueue':True
 },
 'queue481':{'reviewedApplied':836,'pending':12,'acceptedUnapplied':0,'nextIdentity':'fate-rewrite','runtimeSelectionEnabled':False},
 'scopeLimits':{'acceptanceIssued':False,'applicationPerformed':False,'blockersClosed':False,'witnessSealed':False,'queueChanged':False}
}
status_path=OUT/'CODEX_TRANSCRIBED_DIRECTOR_STATUS_POST_COLLAPSE_TIMELINE_PASS_01.json'
status_path.write_text(json.dumps(status,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
status_bytes=status_path.read_bytes()

roles={}
def add(path,role):roles.setdefault(path,set()).add(role)
for p,r in [
 (QUEUE,'Current Queue481 authority, order and current source bindings'),
 (HANDOFF,'Current Handoff481 cross-check'),
 (PENDING,'Current pending audit cross-check'),
 (CAT,'Current catalog and Fate Rewrite row'),
 (IDX,'Current authored index and Fate Rewrite row'),
 (CAND+'CANDIDATE_PACKAGE_MANIFEST.json','Fate/time package provenance'),
 (CAND+'DIRECTOR_DECISION.json','Candidate package hold context'),
 (CAND+'SOURCE_BINDINGS.json','Candidate package source bindings'),
 (CAND+'procedures/fate-rewrite.json','Retained Fate Rewrite authored procedure'),
 (recon_path,'Previously reviewed 53-source identity reconciliation'),
 (recon_manifest_path,'Prior reconciliation packet manifest'),
 (FATE_RECON+'DIRECTOR_REVIEW_REQUEST_FATE_REWRITE_IDENTITY_01.md','Prior static reconciliation request and scope'),
 (recon_pass_path,'Director PASS; reconciliation only, not identity acceptance'),
 (witness_pass_path,'Proposal05 TEST_ONLY component PASS; unsealed'),
 (R320+'DIRECTOR_DECISION.json','Fate Rewrite nextScope and sequence authorization'),
 (R320+'BLOCKER_REASSESSMENT.json','Open B04 and minimum missing source history'),
 (R323+'BLOCKER_REASSESSMENT.json','Open B02 and three missing witness parts'),
 (AUDIT+'rank9_collapse_timeline_return322_received/BLOCKER_REASSESSMENT.json','Collapse Timeline B05 minimum evidence'),
 (R323+'DIRECTOR_DECISION.json','Current Eternal Prophecy/B02 hold disposition'),
 (collapse_pass_path,'Completed Collapse Timeline current-authority review, no witness authorization'),
 (ep_accept_path,'Precedent for separate static identity acceptance'),
 (ep_application_path,'Precedent for application only after explicit acceptance'),
]:add(p,r)

bindings=[]
for path in sorted(roles):
 b=raw(BASE,path)
 bindings.append({'path':path,'bytes':len(b),'sha256':sh(b),'gitBlobSha1':blob(BASE,path),'roles':sorted(roles[path])})

packet={
 'schemaVersion':1,
 'id':'FATE-REWRITE-STATIC-IDENTITY-DISPOSITION-01',
 'classification':'DIRECTOR_IDENTITY_LEVEL_DISPOSITION_REQUEST_NO_APPLICATION',
 'baseCommit':BASE,
 'identity':'fate-rewrite',
 'displayName':'Fate Rewrite',
 'requestedScope':'STATIC_AUTHORED_PROCEDURE_REVIEW_ONLY',
 'requestedDisposition':'Please issue ACCEPT for this identity in the stated static-authored-procedure scope, REVISE with exact path/pointer/hash, or HOLD with the precise unmet requirement.',
 'decisionBoundary':{
  'reconciliationReviewAlreadyPassed':True,
  'priorReconciliationDisposition':recon_pass['disposition'],
  'priorReconciliationSha256':recon_pass['reconciliation']['sha256'],
  'identityAcceptanceHasNotBeenIssued':True,
  'identityApplicationHasNotBeenPerformed':True,
  'thisPacketRequestsDispositionOnly':True,
  'noNewOwnerPremiseOrWitnessAdoptionRequested':True,
  'applicationIsSeparateAndOnlyAfterExplicitDirectorAcceptance':True
 },
 'currentAuthority':{
  'queuePath':QUEUE,'queueSha256':sh(raw(BASE,QUEUE)),
  'handoffPath':HANDOFF,'handoffSha256':sh(raw(BASE,HANDOFF)),
  'pendingAuditPath':PENDING,'pendingAuditSha256':sh(raw(BASE,PENDING)),
  'counts':queue['currentAuthority'],
  'nextIdentity':queue['nextIdentity'],
  'nextBlockerIds':queue['nextBlockerIds'],
  'nextDependencyIds':queue['nextDependencyIds'],
  'continuingPriorityOrder':queue['continuingPriorityOrder'],
  'remainingPendingIds':queue['remainingPendingIds'],
  'runtimeSelectionEnabled':queue['runtimeSelectionEnabled'],
  'acceptedUnapplied':queue['acceptedUnapplied']
 },
 'currentSpellRows':{
  'catalog':{'path':CAT,'bytes':len(raw(BASE,CAT)),'sha256':sh(raw(BASE,CAT)),'gitBlobSha1':blob(BASE,CAT),'pointer':catptr,'row':catrow},
  'authoredIndex':{'path':IDX,'bytes':len(raw(BASE,IDX)),'sha256':sh(raw(BASE,IDX)),'gitBlobSha1':blob(BASE,IDX),'pointer':idxptr,'row':idxrow},
  'candidateProcedure':{'path':CAND+'procedures/fate-rewrite.json','sha256':sh(raw(BASE,CAND+'procedures/fate-rewrite.json')),'accepted':proc['accepted'],'applied':proc['applied'],'blockerIds':proc['blockerIds'],'holdIds':proc['holdIds']}
 },
 'priorReconciliation':{
  'path':recon_path,'sha256':sh(raw(BASE,recon_path)),
  'reviewedCommit':recon_pass['reviewedCommit'],
  'reviewedReconciliationSha256':recon_pass['reconciliation']['sha256'],
  'directorDisposition':recon_pass['disposition'],
  'sourceBindingCount':len(recon['sourceBindings']),
  'verified':recon_pass['verified'],
  'scopeLimits':recon_pass['scopeLimits']
 },
 'retainedOpenRequirements':{
  'TF192-B04':{'status':r320_b04['status'],'minimumMissingWitness':r320_b04['minimumMissingWitness']},
  'TF192-B02':{'status':r323_b02['status'],'minimumMissingWitness':r323_b02['minimumMissingWitness'],'missingWitnessParts':[{'id':x['id'],'requirement':x['requirement']} for x in r323_b02['missingWitnessParts']]},
  'qualificationIdsRetained':[h for h in proc['holdIds'] if h.startswith('TF192-H-') or h.startswith('TF192-Q-')],
  'guaranteeProved':False,
  'witnessesSealed':False
 },
 'directorStatusGuidance':{
  'path':'docs/audit/2026-10-08/full-game/director-spell-review-129/fate_rewrite_static_identity_disposition_2026-11-03/CODEX_TRANSCRIBED_DIRECTOR_STATUS_POST_COLLAPSE_TIMELINE_PASS_01.json',
  'sha256':sh(status_bytes),
  'nextStep':'Fate Rewrite remains first. Request a separate identity-level disposition using the already-passed reconciliation; neither reconciliation PASS advances the queue automatically.'
 },
 'requestedAcceptanceSemantics':{
  'acceptedId':'fate-rewrite',
  'scope':'STATIC_AUTHORED_PROCEDURE_REVIEW_ONLY',
  'appliedIds':[],
  'closedBlockerIds':[],
  'retainedOpenBlockerIds':['TF192-B02','TF192-B04'],
  'retainedQualifications':True,
  'witnessesSealed':False,
  'runtimeSelectionEnabled':False,
  'catalogOrNativeSourceChanged':False,
  'queueChangedByDecision':False
 },
 'sourceBindings':bindings,
 'nonAuthorization':{
  'nativeOperationalAcceptance':False,
  'blockerClosure':False,
  'promiseQualificationOrWaiver':False,
  'seal':False,
  'applicationWithinThisRequest':False,
  'runtimeCampaignCanonOrQueueChange':False
 }
}
packet_path=write('FATE_REWRITE_STATIC_IDENTITY_DISPOSITION_01.json',packet)
packet_sha=sh(packet_path.read_bytes())
rel=AUDIT+'fate_rewrite_static_identity_disposition_2026-11-03/'
request=f'''# Director request — Fate Rewrite identity disposition\n\nThe Fate Rewrite static reconciliation has already passed. Please issue the separate identity-level disposition requested in your status guidance, bound to the current main snapshot and the prior reconciliation below. Return `ACCEPT` for `fate-rewrite` under `STATIC_AUTHORED_PROCEDURE_REVIEW_ONLY`, `REVISE` with exact path/pointer/hash, or `HOLD` with the precise gap.\n\n- Packet: https://github.com/BordelonDevOps/DecenniumDescent/blob/main/{rel}FATE_REWRITE_STATIC_IDENTITY_DISPOSITION_01.json\n- Packet SHA-256: `{packet_sha}`\n- Review request: https://github.com/BordelonDevOps/DecenniumDescent/blob/main/{rel}DIRECTOR_REVIEW_REQUEST_FATE_REWRITE_STATIC_IDENTITY_DISPOSITION_01.md\n- Prior passed reconciliation: https://github.com/BordelonDevOps/DecenniumDescent/blob/4cf33ffbd0a1eb51be5ac13c0709f4e2af9b87d3/{FATE_RECON}FATE_REWRITE_IDENTITY_RECONCILIATION_01.json — SHA-256 `7cda9e3f14afd8a1254b81c37e13eda72495b41af97c3928cdef07c5df45ea8b`\n\nThe prior review verified its 53 source bindings, all 17 historical cases, ten question dispositions, and eleven retained H/Q qualifications. The current Queue481 still lists Fate Rewrite first (836 applied / 12 pending / 0 accepted-unapplied), with TF192-B04 open and TF192-B02 as a dependency. Current catalog/index target rows remain pending authored review; the retained procedure is not accepted or applied.\n\nIf accepted, please make the decision explicitly identity-level and static-only. Keep B02/B04 and all qualifications open, `guaranteeProved=false`, witnesses unsealed, runtime disabled, and appliedIds empty. This request does not ask for native operational acceptance, blocker closure, promise qualification, sealing, application, or any canon/runtime/campaign/queue change.\n'''
request_path=OUT/'DIRECTOR_REVIEW_REQUEST_FATE_REWRITE_STATIC_IDENTITY_DISPOSITION_01.md'
request_path.write_text(request,encoding='utf-8')

print(json.dumps({'base':BASE,'packet':str(packet_path),'packetSha256':packet_sha,'bindings':len(bindings),'catalogPointer':catptr,'indexPointer':idxptr,'queue':queue['currentAuthority'],'B02':r323_b02['status'],'B04':r320_b04['status'],'statusReadback':str(status_path)},indent=2))

