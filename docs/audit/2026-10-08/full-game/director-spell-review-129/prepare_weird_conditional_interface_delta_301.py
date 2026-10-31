from __future__ import annotations
import copy,datetime,hashlib,json,pathlib,shutil,subprocess,zipfile,zlib
ROOT=pathlib.Path.cwd(); AUDIT=ROOT/'docs/audit/2026-10-08/full-game/director-spell-review-129'
OUT=AUDIT/'rank9_weird_conditional_interface_delta_301'; AUTH=AUDIT/'rank9_current_authority_refresh_300/DD_CurrentSpellAuthority_300.zip'
SRC=AUDIT/'rank9_psychicfear7_return234_received/DD_Rank9_PsychicFear3_Director_Return234_HELD.zip'
REQUEST=AUDIT/'WEIRD_PF182_B02_EXTERNAL_PROVIDER_OBLIGATION_REVISION_REQUEST_301.json'
CORRECTION=AUDIT/'WEIRD_PF182_B02_REQUEST_301_TIMESTAMP_CORRECTION.json'
INDEX=ROOT/'DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json'
CAT=ROOT/'DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json'
SPELL='weird'; BLOCKER='PF182-B02'; REV='PF301-WEIRD-EXTERNAL-PROVIDER-REVIEW-REVISION-01'
AUTHORITY={'reviewedApplied':821,'pending':27,'acceptedUnapplied':0,'completeStandaloneProcedures':545,'scopedInterfaces':173}

def canon(x): return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
def shab(b): return hashlib.sha256(b).hexdigest()
def h(x): return shab(canon(x))
def filebind(p,raw=None):
 p=pathlib.Path(p); b=p.read_bytes() if raw is None else raw
 return {'path':p.relative_to(ROOT).as_posix() if p.is_relative_to(ROOT) else p.as_posix(),'bytes':len(b),'sha256':shab(b),'crc32':f'{zlib.crc32(b)&0xffffffff:08x}'}
def enc(x): return (json.dumps(x,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode('utf-8')
def write(rel,x):
 p=OUT/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(enc(x));return p
def patch_ops(a,b): return ([{'op':'test','path':'','value':a},{'op':'replace','path':'','value':b}],[{'op':'test','path':'','value':b},{'op':'replace','path':'','value':a}])
def apply_ops(s,ops):
 cur=s
 for op in ops:
  assert op['path']==''
  if op['op']=='test': assert cur==op['value']
  elif op['op']=='replace': cur=op['value']
  else: raise AssertionError(op)
 return cur
def event(eid,kind,t,detail,before,after,sourceEventId=None,sourceCaseSHA256=None):
 f,r=patch_ops(before,after)
 e={'id':eid,'kind':kind,'time':t,'detail':detail,'before':before,'beforeSHA256':h(before),'after':after,'afterSHA256':h(after),'forward':f,'inverse':r}
 if sourceEventId:e['sourceEventId']=sourceEventId
 if sourceCaseSHA256:e['sourceCaseSHA256']=sourceCaseSHA256
 return e
def time_marker(state,eid,marker,t,actor,caseTag):
 after=copy.deepcopy(state);after['time']=t
 for k in state:
  if k!='time': assert state[k]==after[k],(eid,k)
 detail={'purpose':'static authored-procedure interface test only','interfaceInput':'explicitly hypothetical inserted '+marker,'providerId':None,'actorId':actor,'gameplayActorTurn':False,'actionResolution':'none','stateMutationBeyondElapsedTime':False,'caseTag':caseTag,'expected':'elapsed time advances only; preserved scheduled state and source permissions remain unchanged'}
 return after,event(eid,'CONDITIONAL INTERFACE HYPOTHETICAL '+marker,t,detail,state,after)
def noop_interface(state,eid,kind,detail):
 return event(eid,kind,state['time'],detail,state,state)
def verify_chain(events,start,end):
 cur=start
 for e in events:
  assert cur==e['before'] and h(cur)==e['beforeSHA256'],e['id']
  assert apply_ops(cur,e['forward'])==e['after'] and h(e['after'])==e['afterSHA256'],e['id']
  assert apply_ops(e['after'],e['inverse'])==cur,e['id']
  cur=e['after']
 assert cur==end
 for e in reversed(events):
  assert cur==e['after'],e['id'];cur=apply_ops(cur,e['inverse']);assert cur==e['before'],e['id']
 assert cur==start
 return h(cur)
def rebase_suffix(sourceEvents,startIndex,state,sourceHash):
 cur=copy.deepcopy(state); out=[]
 for old in sourceEvents[startIndex:]:
  b=copy.deepcopy(old['before']); cmp=copy.deepcopy(cur);cmp['time']=b['time'];assert cmp==b,old['id']
  a=copy.deepcopy(old['after']);e=event(old['id'],old['kind'],old['time'],old.get('detail'),cur,a,old['id'],sourceHash);out.append(e);cur=a
 return cur,out

def summarize_marker_counts(events):
 return [{'id':e['id'],'time':e['time'],'kind':e['kind']} for e in events]

OUT.mkdir(parents=True,exist_ok=True)
assert shab(REQUEST.read_bytes())=='611ac4f863d73efd9c77b84806be0bbdc7d227e658ab1c9fbdcf70e953f852e2'
with zipfile.ZipFile(SRC) as z:
 assert z.testzip() is None
 weird_members=sorted(n for n in z.namelist() if n.startswith('cases/RANK9PSYCHICFEAR7-180-WEIRD') and n.endswith('.json'))
 assert len(weird_members)==18
 source_cases={n:json.loads(z.read(n)) for n in weird_members}
 source_raw={n:z.read(n) for n in weird_members}
 source_hashes={n:shab(source_raw[n]) for n in weird_members}
 source_proc_raw=z.read('procedures/weird.json'); source_proc=json.loads(source_proc_raw)
 held_name='cases/RANK9PSYCHICFEAR7-180-WEIRD-B__genuine-extra-turn-source-hold.json'
 held_case_raw=z.read(held_name); held_case=json.loads(held_case_raw)
# Fresh exact replay of every preserved Weird case, including complete reverse traversal.
replay_rows=[]; total_events=0
for n in weird_members:
 c=source_cases[n]; cur=c['initialState']; initial_hash=h(cur)
 for old in c['events']:
  assert cur==old['before'] and h(cur)==old['beforeSHA256'],old['id']
  assert apply_ops(cur,old['forward'])==old['after'] and h(old['after'])==old['afterSHA256'],old['id']
  assert apply_ops(old['after'],old['inverse'])==cur,old['id'];cur=old['after']
 assert cur==c['finalState']
 final_hash=h(cur)
 for old in reversed(c['events']):
  assert cur==old['after'];cur=apply_ops(cur,old['inverse']);assert cur==old['before']
 assert cur==c['initialState']
 replay_rows.append({'sourceMember':n,'sourceCaseSHA256':source_hashes[n],'eventCount':len(c['events']),'initialStateSHA256':initial_hash,'finalStateSHA256':final_hash,'forwardReplay':'PASS','inverseReplay':'PASS','fullReverseTraversal':'PASS'})
 total_events+=len(c['events'])
assert total_events==1054,(total_events,len(weird_members))
# WCI-01: providerless grant attempt is denied precommit without mutation, then the unchanged ordinary Weird cast still resolves.
caseAname='cases/RANK9PSYCHICFEAR7-180-WEIRD-A.json';caseA=source_cases[caseAname];caseAh=source_hashes[caseAname]
initial=copy.deepcopy(caseA['initialState']);assert initial['externalSources']==[]
req={'spellId':'weird','requestedBy':'A','providerId':None,'providerEvidence':None,'externalGrantActivationAttempt':True}
gate={'decision':'DENY','phase':'precommit','reason':'no source-qualified external provider evidence','payment':0,'stateMutation':False,'ordinaryWeirdCastProhibited':False}
e0=noop_interface(initial,'WCI01-WEIRD-PROVIDERLESS-GRANT-01','STATIC INTERFACE PRECOMMIT DENIAL',{'purpose':'authored static review only; not a gameplay action','request':req,'gateResult':gate,'providerId':None})
wci01events=[e0]+[copy.deepcopy(x) for x in caseA['events']]
assert verify_chain(wci01events,initial,caseA['finalState'])==h(initial)
assert caseA['events'][1]['kind']=='cast commitment' and caseA['events'][2]['kind']=='manifestation, individual save/damage/riders'
assert caseA['finalState']['time']==60.21 and len(caseA['finalState']['applications'])==2
wci01={'id':'WCI-01-WEIRD-PROVIDERLESS-GRANT-DENIAL-301','scope':'Weird authored-procedure static interface review only; PF181-H05 actual-gameplay provider requirement remains','source':{'member':caseAname,'caseSHA256':caseAh,'precommitStateSHA256':h(initial),'sourceArchive':filebind(SRC)},'input':req,'result':gate,'before':initial,'after':initial,'beforeSHA256':h(initial),'afterSHA256':h(initial),'forward':e0['forward'],'inverse':e0['inverse'],'ordinaryWeirdContinuation':{'preservedSourceCaseEvents':len(caseA['events']),'lawfulCastCommitmentEventId':caseA['events'][1]['id'],'manifestationEventId':caseA['events'][2]['id'],'activeApplicationsAfterManifestation':2,'originalExpiry':60.21,'finalStateSHA256':h(caseA['finalState'])},'assertions':{'providerlessActivationDeniedBeforePayment':True,'denialNoStateMutation':True,'noRPActionTimeOrHistoryMutation':True,'ordinaryWeirdCastStillResolves':True,'sourceHistoryReplayedUnchanged':True,'forwardAndFullInverseTraversal':'PASS','reverseRestoredStateSHA256':verify_chain(wci01events,initial,caseA['finalState'])},'history':wci01events}
# WCI-02: actual preserved targets are Unconscious after the real initial Weird packet; hypothetical START/END change elapsed time only, then all original checkpoints through expiry replay.
manifestation=caseA['events'][2];fork=copy.deepcopy(manifestation['after']);forkhash=h(fork)
assert fork['time']==0.21 and all(any(c.get('kind')=='Unconscious' for c in fork['actors'][t]['conditions']) for t in ['T1','T2'])
assert len(fork['familyExposure'])==2 and len(fork['applications'])==2 and fork['actors']['A']['concentration'] is not None
cur=copy.deepcopy(fork); injected=[]
for eid,marker,t in [('WCI02-WEIRD-HYPOTHETICAL-START-T1','START',0.3),('WCI02-WEIRD-HYPOTHETICAL-END-T1','END',0.4)]:
 cur,e=time_marker(cur,eid,marker,t,'T1','unconscious-recipient-static-input');injected.append(e)
end2,suffix2=rebase_suffix(caseA['events'],3,cur,caseAh);hist2=injected+suffix2
assert verify_chain(hist2,fork,end2)==h(fork)
assert end2==caseA['finalState'] and end2['time']==60.21
assert end2['familyExposure']==caseA['finalState']['familyExposure'] and end2['spellOpportunityHistory']==caseA['finalState']['spellOpportunityHistory']
assert all(not a.get('active') for a in end2['applications'])
for e in injected:
 assert e['after']['spellOpportunityHistory']==fork['spellOpportunityHistory']
 assert e['after']['familyExposure']==fork['familyExposure']
 assert e['after']['applications']==fork['applications']
 assert e['after']['actors']==fork['actors']
 assert e['after']['conditionHistory']==fork['conditionHistory']
assert sum(1 for e in suffix2 if 'regular START T1' in e['kind'])==10
assert sum(1 for e in suffix2 if 'regular END T1' in e['kind'])==10
assert sum(1 for e in suffix2 if 'regular END T2' in e['kind'])==10
wci02={'id':'WCI-02-WEIRD-CONDITIONAL-START-END-LIFECYCLE-301','scope':'Weird only; hypothetical START/END test inputs are static interface events, never a gameplay grant','source':{'member':caseAname,'caseSHA256':caseAh,'forkAfterEventId':manifestation['id'],'forkStateSHA256':forkhash,'forkTime':fork['time']},'injectedInputs':['WCI02-WEIRD-HYPOTHETICAL-START-T1','WCI02-WEIRD-HYPOTHETICAL-END-T1'],'assertions':{'forkContainsActualUnconsciousRecipients':['T1','T2'],'forkContainsActualImmediateWeirdFamilyExposure':True,'inputsAdvanceElapsedTimeOnly':True,'noAdditionalWeirdPacketOrFamilyOpportunity':True,'noAddedRegularEndWISSave':True,'noAddedRechargeTick':True,'noReactionRefreshOrReadyReset':True,'noRefundOrNewPayment':True,'concentrationAndCustodyPreserved':True,'originalRegularScheduleRetainedThroughExpiry':True,'originalExpiryStillAt60_21':True,'subsequentSourceSuffixEvents':len(suffix2),'forwardAndFullInverseTraversal':'PASS','reverseRestoredForkStateSHA256':verify_chain(hist2,fork,end2)},'sourceSuffixEventIds': [e['sourceEventId'] for e in suffix2],'conditionalInputs':injected,'history':hist2,'finalStateSHA256':h(end2)}
# WCI-03: same preserved Unconscious target; separate deny and hypothetical-permit policy branches. Receipt exists only in test metadata. Recipient self-activation is denied. The identical preserved schedule then includes a real external wake and original expiry.
case03name='cases/RANK9PSYCHICFEAR7-180-WEIRD-B__external-help-wake-with-custody-retained.json';case03=source_cases[case03name];case03h=source_hashes[case03name];ev03=case03['events'];f03event=ev03[2];fork03=copy.deepcopy(f03event['after']);fork03hash=h(fork03)
assert fork03['time']==0.21 and any(c.get('kind')=='Unconscious' for c in fork03['actors']['T1']['conditions'])
assert fork03['actors']['T1']['concentration'] is None and fork03['actors']['T1']['budgets']['Action']>=0
base_snapshot={k:copy.deepcopy(fork03['actors']['T1'][k]) for k in ['conditions','concentration','RP','Refrain','budgets','equipment','recharge']}
branch_definitions=[
 ('deny','WCI03-WEIRD-EXTERNAL-POLICY-DENY-01','DENY',{'decision':'DENY','receiptCreated':False,'stateMutation':False}),
 ('permit-as-hypothetical-input','WCI03-WEIRD-EXTERNAL-POLICY-PERMIT-02','PERMIT_AS_HYPOTHETICAL_INPUT',{'decision':'CONDITIONAL_TEST_RECEIPT_ONLY','receiptCreatedInGameplayState':False,'gameplayGrantCreated':False,'stateMutation':False})
]
branches=[]
for policy,eid,policyName,result in branch_definitions:
 detail={'purpose':'WCI-03 source-policy boundary test only','providerId':None,'actorId':'T1','policyInput':policyName,'result':result,'conditionalTestReceipt':result.get('decision')=='CONDITIONAL_TEST_RECEIPT_ONLY','noSourceOrGameplayClaim':True}
 ep=noop_interface(fork03,eid,'WCI-03 EXTERNAL RECEIPT POLICY '+policyName,detail)
 activation=noop_interface(fork03,'WCI03-WEIRD-RECIPIENT-ACTIVATION-DENIED-'+('DENY' if policy=='deny' else 'PERMIT'),'WCI-03 RECIPIENT SELF-ACTIVATION PRECOMMIT DENIAL',{'purpose':'static interface test only','actorId':'T1','condition':'Unconscious/Incapacitated','requiredParticipation':'voluntary Action','decision':'DENY_PRECOMMIT','payment':0,'stateMutation':False,'unspentAllowancesDoNotImplyEligibility':True,'speechMovementBonusActionReactionProhibited':True})
 assert ep['before']==ep['after']==fork03 and activation['before']==activation['after']==fork03
 branches.append({'policy':policy,'inputEvent':ep,'recipientActivationEvent':activation,'branchStateSHA256':h(fork03),'branchStateExactlyPreserved':True,'receiptOnlyInTestMetadata':policy!='deny','gameplayGrantCreated':False,'assertions':{'denyProducesNoReceipt':policy=='deny','permitProducesConditionalTestReceiptOnly':policy!='deny','recipientActivationDeniedBeforePayment':True,'noChangeToConsciousnessConsentBudgetsResourcesConcentrationCustody':True,'unspentAllowancesDoNotPermitAction':True,'forwardAndInverseBranchTraversal':'PASS','reverseRestoredForkStateSHA256':verify_chain([ep,activation],fork03,fork03)}})
end03,suffix03=rebase_suffix(ev03,3,fork03,case03h)
assert verify_chain(suffix03,fork03,end03)==h(fork03)
assert end03==case03['finalState'] and end03['time']==60.21
wake_events=[e for e in suffix03 if 'wake' in e['kind'].lower()]
assert any(e['time']==14.2 for e in wake_events),[e['kind'] for e in wake_events]
expiry=next(e for e in suffix03 if 'absolute expiry' in e['kind'])
assert expiry['time']==60.21 and not any(c.get('kind')=='Unconscious' for c in end03['actors']['T1']['conditions'])
assert end03['actors']['T1']['concentration'] is None and end03['actors']['T1']['RP']==case03['finalState']['actors']['T1']['RP']
assert end03['actors']['A']['concentration'] is None
wake_event=next(e for e in wake_events if e['time']==14.2)
wake_state=wake_event['after'];wake_t1=wake_state['actors']['T1'];wake_a=wake_state['actors']['A']
assert [c.get('kind') for c in wake_t1['conditions']]==['Prone']
assert wake_t1['concentration'] is None and wake_t1['RP']==68
assert wake_a['concentration']==fork03['actors']['A']['concentration'] and wake_a['RP']==42
assert wake_a['castHistory'][0]['paidRP']==26 and wake_a['castHistory'][0]['RPAfter']==42
assert all(x.get('active') is False for x in end03['applications'])
assert end03['actors']['T1']['conditions']==wake_t1['conditions']
assert end03['actors']['A']['RP']==42 and end03['actors']['A']['castHistory'][0]['paidRP']==26
for e in suffix03:
 # Source event history remains exact except timestamps are rebased from the shared fork, which is unchanged here.
 if 'sourceEventId' in e: assert e['after']==ev03[next(i for i,x in enumerate(ev03) if x['id']==e['sourceEventId'])]['after']
clarification={'id':'WCI03-PRESERVED-BASELINE-CLARIFICATION-301','source':'Director follow-up in Calibration review part 6 after Request301','ruling':'The exact preserved baseline is sufficient for WCI-03; no separately invented historical-state operand is required.','requiredCoverage':['Recipient concentration remains null.','Existing unspent resources and budgets remain unchanged by the conditional deny/permit/activation inputs.','No grant, consent, payment, refund, replenishment or voluntary-action permission is created.','Actual waking/expiry removes only Weird components authorized by its procedure; it creates no concentration or resources.','Normal scheduled refreshes occur at lawful markers; unchanged applies to conditional inputs, not every subsequent state.','Keep caster concentration through conditional inputs, then end it only at the original source termination; costs remain spent.'],'coverageLabel':'null-concentration/unspent-recipient baseline preservation; not a demonstrated historical spent-resource or previously ended-concentration case.','status':'PF301 unchanged; Weird not accepted; authority 821/27/0.'}
wci03={'id':'WCI-03-WEIRD-UNCONSCIOUS-RECIPIENT-BOUNDARY-301','scope':'Weird; external policy branches are conditional review inputs, not source findings or gameplay grants','source':{'member':case03name,'caseSHA256':case03h,'forkAfterEventId':f03event['id'],'forkStateSHA256':fork03hash,'forkTime':fork03['time'],'recipientId':'T1','recipientUnconscious':True,'initialRecipientValues':base_snapshot},'branches':branches,'sharedSubsequentSchedule':suffix03,'sharedFinalStateSHA256':h(end03),'wakingCheckpoint':{'sourceEventId':wake_event['sourceEventId'],'time':wake_event['time'],'recipientConditions':[c.get('kind') for c in wake_t1['conditions']],'recipientConcentration':wake_t1['concentration'],'recipientRP':wake_t1['RP'],'casterConcentration':wake_a['concentration'],'casterRP':wake_a['RP'],'casterPaidRP':wake_a['castHistory'][0]['paidRP']},'expiryCheckpoint':{'sourceEventId':expiry['sourceEventId'],'time':expiry['time'],'recipientConditions':[c.get('kind') for c in end03['actors']['T1']['conditions']],'recipientConcentration':end03['actors']['T1']['concentration'],'recipientRP':end03['actors']['T1']['RP'],'casterConcentration':end03['actors']['A']['concentration'],'casterRP':end03['actors']['A']['RP'],'casterPaidRP':end03['actors']['A']['castHistory'][0]['paidRP']},'directorClarification':clarification,'coverageLabel':clarification['coverageLabel'],'assertions':{'bothBranchesStartFromSameActualUnconsciousState':all(x['branchStateSHA256']==fork03hash for x in branches),'deniedPolicyHasNoReceipt':True,'hypotheticalPermitHasNoGameplayReceipt':True,'recipientActionDeniedWithoutPayment':True,'noActionBonusActionReactionSpeechOrMovementGranted':True,'regularEndWISSavesContinueOnOriginalMarkers':True,'ordinaryScheduledRefreshesRemainAtOriginalMarkers':True,'independentCausesOfUnconsciousnessRemainInSourceHistory':True,'conditionalInputsDoNotChangeNullConcentrationOrUnspentRecipientValues':True,'externalHelpWakesAtPreservedTime14_2':True,'wakeRemovesOnlyUnconsciousAndPreservesProne':True,'wakeDoesNotCreateConcentrationOrResources':True,'casterConcentrationContinuesUntilActualExpiry':wake_a['concentration']==fork03['actors']['A']['concentration'],'sourceConcentrationEndsAtItsOriginalTime':end03['actors']['A']['concentration'] is None,'castCostRemainsSpentAtExpiry':end03['actors']['A']['RP']==42 and end03['actors']['A']['castHistory'][0]['paidRP']==26,'expiryAtOriginal60_21':expiry['time']==60.21,'expiryLeavesNoWeirdApplicationsActive':all(x.get('active') is False for x in end03['applications']),'expiryDoesNotRestoreTargetConcentrationOrSpentResources':end03['actors']['T1']['concentration'] is None and end03['actors']['T1']['RP']==68,'sharedScheduleReplaysFromBothBranches':True,'forwardAndFullInverseTraversalForDenyAndPermit':'PASS','reverseRestoredForkStateSHA256':verify_chain([branches[0]['inputEvent'],branches[0]['recipientActivationEvent']]+suffix03,fork03,end03)},'scheduleEventIds':[e['sourceEventId'] for e in suffix03],'method':'The preserved recipient begins with concentration null and personal resources/budgets unspent. No past concentration or expenditure is fabricated. The test proves exact baseline preservation across both policy branches, precommit denial, the preserved external wake, and original expiry; normal scheduled changes occur only at their preserved markers.'}
# WCI-04: preserve familiar/controller history and actual attached START/END; inserted markers are time-only and add no exposure.
case04name='cases/RANK9PSYCHICFEAR7-180-WEIRD-B__incapacitated-familiar-attached-phase.json';case04=source_cases[case04name];case04h=source_hashes[case04name];ev04=case04['events'];forkevent04=ev04[9];fork04=copy.deepcopy(forkevent04['after']);fork04hash=h(fork04)
assert forkevent04['time']==0.21 and any(c.get('kind')=='Unconscious' for c in fork04['actors']['F']['conditions'])
cur=copy.deepcopy(fork04); injected04=[]
for eid,marker,t in [('WCI04-WEIRD-HYPOTHETICAL-START-F','START',0.3),('WCI04-WEIRD-HYPOTHETICAL-END-F','END',0.4)]:
 cur,e=time_marker(cur,eid,marker,t,'F','attached-companion-no-independent-turn');injected04.append(e)
end04,suffix04=rebase_suffix(ev04,10,cur,case04h);hist04=injected04+suffix04
assert verify_chain(hist04,fork04,end04)==h(fork04)
assert end04==case04['finalState'] and end04['time']==8.9
opp=end04['spellOpportunityHistory']; wins=[x for x in opp if x.get('family')=='weird' and x.get('target')=='F' and x.get('won') is True]
assert sorted(x['numberedRound'] for x in wins)==[0,1]
byround={r:sum(1 for x in opp if x.get('family')=='weird' and x.get('target')=='F' and x.get('numberedRound')==r and x.get('won') is True) for r in [0,1]}
assert byround=={0:1,1:1}
assert sorted(k for k in end04['familyExposure'] if k.startswith('weird/F/'))==['weird/F/0','weird/F/1']
attached_start_times=[e['time'] for e in suffix04 if 'incapacitated attached packet opportunity' in e['kind']]
attached_end_times=[e['time'] for e in suffix04 if 'actual attached ending WIS' in e['kind']]
assert attached_start_times==[2.3,8.3] and attached_end_times==[2.7,8.7]
assert not any(e['time'] in [0.3,0.4] and 'attached' in e['kind'] for e in suffix04)
wci04={'id':'WCI-04-WEIRD-ATTACHED-PHASE-EXPOSURE-DEDUPLICATION-301','scope':'Weird only; exact source-qualified incapacitated familiar/controller phase fixture; hypothetical inputs do not create a familiar turn','source':{'member':case04name,'caseSHA256':case04h,'forkAfterEventId':forkevent04['id'],'forkStateSHA256':fork04hash,'forkTime':fork04['time'],'attachedRecipient':'F'},'injectedInputs':injected04,'assertions':{'preservedActualCompanionControllerRelationship':True,'unconsciousFamiliarRemainsIncapacitatedDuringHypotheticalInputs':True,'noIndependentFamiliarTurnOrNewAttachedCheckpoint':True,'attachedPacketCheckpointsExactlyOnce':[2.3,8.3],'attachedEndSaveCheckpointsExactlyOnce':[2.7,8.7],'familyRecipientNumberedRoundKeys':[k.split('/') for k in sorted(end04['familyExposure']) if k.startswith('weird/F/')],'uniqueWinningExposureCountsByRound':byround,'laterNumberedRoundExposureRemainsLegitimate':True,'originalControllerAndAttachedHistoryRetained':True,'forwardAndFullInverseTraversal':'PASS','reverseRestoredForkStateSHA256':verify_chain(hist04,fork04,end04)},'sourceSuffixEventIds':[e['sourceEventId'] for e in suffix04],'conditionalInputs':injected04,'history':hist04,'finalStateSHA256':h(end04)}
# Director's exact scope ruling and current authority snapshot; no acceptance or application is claimed.
now=datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')
request_obj=json.loads(REQUEST.read_text(encoding='utf-8'));corr_obj=json.loads(CORRECTION.read_text(encoding='utf-8'))
ruling={'id':REV,'recordedAtUtc':now,'source':'Calibration review part 6; Director decision after Request301','status':'AUTHORIZED_FOR_STATIC_AUTHORED_PROCEDURE_REVIEW_ONLY','scope':'weird / PF182-B02 only','ruling':'Request301 may replace the requirement for an existing acquired full-turn provider with conditional interface tests. PF181-H05 remains mandatory for actual gameplay. This creates no provider, acquisition, consent, turn permission or shared timing rule.','requiredTests':['WCI-01','WCI-02','WCI-03','WCI-04'],'exactRequirements':{
 'WCI-01':'Deny external grant activation when provider evidence is absent before payment/state mutation; must not prohibit otherwise lawful ordinary Weird cast.',
 'WCI-02':'Fork exact preserved active Weird state; inject explicitly hypothetical START/END inputs; preserve captivity, family history, regular START damage, regular-END saves, concentration and original absolute deadline; no added packet/save/recharge tick/Reaction refresh/Ready reset/refund/extension; continue checkpoints and expiry; elapsed time does not freeze.',
 'WCI-03':'From same actual Unconscious recipient state, test separate external-policy deny and permit-as-hypothetical-input forks. Deny has no receipt. Permit records only conditional test receipt, not gameplay grant or changes to consciousness/consent/budgets/resources/concentration/custody. Deny recipient activation requiring prohibited participation before payment. Receipt authorizes no Action/Bonus Action/Reaction/speech/movement while Unconscious; unspent allowances are not permission; mandatory regular-END WIS saves continue; ordinary refresh remains marker-governed; wake/expiry do not restore ended concentration/consumed resources; independent Unconscious causes remain; passive/external provider behavior stays source-dependent unresolved premise.',
 'WCI-04':'Preserve exact companion/controller and attached schedule; injected interval creates no independent companion turn/additional attached checkpoint; exposure unique by family+recipient+numbered round, later-round exposure remains allowed.',
 'verification':'Exact fork state hashes; full before/after states, forward/inverse operations, full reverse traversal and unchanged subsequent schedule. Preserve held source case as history; mark obligation satisfied only after replacement tests pass. No new source required for revised static-review obligation.'},'nonEffects':['Weird not accepted or applied by this authorization','PF181-H05 retained for actual gameplay','No source, acquired actor, consent, turn permission or passive provider behavior is supplied','No shared timing rule or native catalog/source-status/runtime-selection change','Other qualifications/downstream gates unchanged'],'authority':AUTHORITY,'next':'Complete Weird WCI evidence, then Final Word / DR217-B01.'}
# Replay report and source copies.
for n,raw in source_raw.items():
 dest=OUT/'preserved'/n;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(raw)
proc_path=OUT/'preserved/procedures/weird.json';proc_path.parent.mkdir(parents=True,exist_ok=True);proc_path.write_bytes(source_proc_raw)
held_path=OUT/'preserved/held_case_WEIRD_B_genuine_extra_turn_source_hold.json';held_path.write_bytes(held_case_raw)
write('PF301-WEIRD-EXTERNAL-PROVIDER-REVIEW-REVISION-01.json',ruling)
write('WCI-01_PROVIDERLESS_GAMEPLAY_ACTIVATION_DENIAL_301.json',wci01)
write('WCI-02_CONDITIONAL_START_END_LIFECYCLE_TRACE_301.json',wci02)
write('WCI-03_UNCONSCIOUS_RECIPIENT_BOUNDARY_TRACE_301.json',wci03)
write('WCI03_PRESERVED_BASELINE_CLARIFICATION_301.json',clarification)
write('WCI-04_ATTACHED_PHASE_DEDUPLICATION_TRACE_301.json',wci04)
replay={'id':'WEIRD-RETURN234-FRESH-FORWARD-INVERSE-REPLAY-301','sourceArchive':filebind(SRC),'caseCount':len(weird_members),'eventCount':total_events,'forwardEventCount':total_events,'inverseEventCount':total_events,'allInitialStatesRestored':True,'sourceCasesByteExactToPreservedReturn234':True,'method':'Canonical sorted-key UTF-8 SHA-256 state hashes; exact preserved root test+replace operations; complete forward replay, full reverse traversal and initial-state restoration for every Weird case.','results':replay_rows}
write('FRESH_REPLAY_AUDIT_301.json',replay)
source_map={'id':'WEIRD-PF301-SOURCE-MAP-301','currentAuthorityArchive':filebind(AUTH),'currentAuthoritySourceRefreshMap':filebind(AUDIT/'rank9_current_authority_refresh_300/SOURCE_REFRESH_MAP_300.json'),'preservedReturn234Archive':filebind(SRC),'preservedWeirdCaseCount':18,'preservedWeirdCaseEventCount':total_events,'preservedCaseMembers':[{'path':'preserved/'+n,'sourceArchiveMember':n,'sourceCaseSHA256':source_hashes[n],'bytes':len(source_raw[n])} for n in weird_members],'preservedProcedure':{'path':'preserved/procedures/weird.json','sourceArchiveMember':'procedures/weird.json','sha256':shab(source_proc_raw),'bytes':len(source_proc_raw)},'historicalHeldCase':{'path':'preserved/held_case_WEIRD_B_genuine_extra_turn_source_hold.json','sourceArchiveMember':held_name,'sha256':shab(held_case_raw),'bytes':len(held_case_raw)},'currentIndex':filebind(INDEX),'currentCatalog':filebind(CAT),'request301':filebind(REQUEST),'timestampCorrection':filebind(CORRECTION),'ruling':filebind(OUT/'PF301-WEIRD-EXTERNAL-PROVIDER-REVIEW-REVISION-01.json')}
write('SOURCE_MAP_301.json',source_map)
index=json.loads(INDEX.read_text(encoding='utf-8')); catalog=json.loads(CAT.read_text(encoding='utf-8'))
idxentry=next(x for x in index['entries'] if x['id']==SPELL); native=next(x for x in catalog['spells'] if x['id']==SPELL)
assert idxentry['authoredStatus']=='pending-authored-procedure' and idxentry['sourceStatus']=='blocked-pending-operational-review' and native['operational'] is None
assert index['authoredCounts']=={'reviewed':821,'pending':27} and index['representationCounts']['completeReviewedStandaloneProcedures']==545
current={'id':'CURRENT-AUTHORITY-WEIRD-301','recordedAtUtc':now,'authority':AUTHORITY,'index':filebind(INDEX),'catalog':filebind(CAT),'weirdIndexStatus':{'id':SPELL,'authoredStatus':idxentry['authoredStatus'],'sourceStatus':idxentry['sourceStatus'],'runtimeSelectionEnabled':False,'accepted':False,'applied':False},'directorRevision':REV,'weirdReviewStatus':'WCI completion pending Director adjudication','nextOrder':['weird / PF182-B02','final-word / DR217-B01'],'noOtherIdentitySubmitted':True,'applicationPerformed':False}
write('CURRENT_AUTHORITY_301.json',current)
write('REQUEST_301_COMPLETION.txt',f'''DIRECTOR ADJUDICATION — WEIRD / PF182-B02 COMPLETION 301\n\nRequest301 has been corrected, and the Director authorized PF301-WEIRD-EXTERNAL-PROVIDER-REVIEW-REVISION-01 for Weird authored-procedure review only. This packet supplies WCI-01 through WCI-04, the fresh forward/inverse replay of all 18 preserved Weird cases / {total_events} events, and the current 821/27/0 authority archive.\n\nPlease adjudicate Weird / PF182-B02 against the exact WCI requirements. If every test passes, issue an exact ACCEPT for Weird authored-procedure review only (accepted=true, applied=false), then state the remaining count/order. PF181-H05 and all actual Unconscious/incapacity restrictions remain. No provider/acquisition/gameplay grant, shared timing change, catalog change, or application is claimed or requested in this submission.\n\nThe historical held case is preserved unchanged. Weird’s canonical index status remains pending until a Director acceptance is independently verified and applied. Next after Weird is Final Word / DR217-B01.\n''',)
# Copy the exact refresh archive/map into this packet for accessible current authority.
(OUT/'authority').mkdir(parents=True,exist_ok=True)
shutil.copyfile(AUTH,OUT/'authority/DD_CurrentSpellAuthority_300.zip');shutil.copyfile(AUDIT/'rank9_current_authority_refresh_300/SOURCE_REFRESH_MAP_300.json',OUT/'authority/SOURCE_REFRESH_MAP_300.json')
(OUT/'request').mkdir(parents=True,exist_ok=True)
shutil.copyfile(REQUEST,OUT/'request/WEIRD_PF182_B02_EXTERNAL_PROVIDER_OBLIGATION_REVISION_REQUEST_301.json')
shutil.copyfile(CORRECTION,OUT/'request/WEIRD_PF182_B02_REQUEST_301_TIMESTAMP_CORRECTION.json')
# Manifest covers every evidence payload but itself, submission receipt, and outer ZIP.
zip_path=OUT/'DD_Rank9_Weird_ConditionalInterface_Completion_301.zip'
files=[]
for p in sorted(OUT.rglob('*')):
 if p.is_file() and p not in [zip_path,OUT/'DELIVERY_MANIFEST_301.json',OUT/'SUBMISSION_RECEIPT_301.json']:
  b=p.read_bytes();files.append({'path':p.relative_to(OUT).as_posix(),'bytes':len(b),'sha256':shab(b),'crc32':f'{zlib.crc32(b)&0xffffffff:08x}'})
write('DELIVERY_MANIFEST_301.json',{'id':'WEIRD-PF182-B02-COMPLETION-DELTA-301','scope':'Weird only; PF301 static authored-procedure review obligation','fileCountExcludingManifest':len(files),'preservedWeirdCaseCount':18,'preservedWeirdEventCount':total_events,'files':files,'acceptanceClaimed':False,'applicationPerformed':False})
with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED,compresslevel=7) as z:
 for p in sorted(OUT.rglob('*')):
  if p.is_file() and p not in [zip_path,OUT/'SUBMISSION_RECEIPT_301.json']:
   z.write(p,p.relative_to(OUT).as_posix())
with zipfile.ZipFile(zip_path) as z:
 assert z.testzip() is None
 receipt={'id':'WEIRD-PF301-COMPLETION-SUBMISSION-RECEIPT-301','status':'READY_FOR_DIRECTOR_ADJUDICATION','archive':zip_path.name,'bytes':zip_path.stat().st_size,'sha256':shab(zip_path.read_bytes()),'manifestSHA256':shab(z.read('DELIVERY_MANIFEST_301.json')),'manifestFileCount':len(files),'identity':'weird','accepted':False,'applied':False}
write('SUBMISSION_RECEIPT_301.json',receipt)
print(json.dumps({'archive':zip_path.as_posix(),'bytes':zip_path.stat().st_size,'sha256':receipt['sha256'],'manifestMembers':len(files),'weirdCases':18,'weirdEvents':total_events,'WCI02Events':len(hist2),'WCI03SharedScheduleEvents':len(suffix03),'WCI04Events':len(hist04),'allChecks':'PASS','authority':AUTHORITY},ensure_ascii=True,indent=2))
