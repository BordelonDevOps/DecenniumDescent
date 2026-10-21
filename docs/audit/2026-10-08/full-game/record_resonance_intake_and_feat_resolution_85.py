from pathlib import Path
from copy import deepcopy
from datetime import datetime,timezone
import json,hashlib
G=Path(r'C:\Github\DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game'
OLD=A/'ACTIVE_AUTHORING_CHECKPOINT_FEAT_WORK_COMPOSITIONS_84.json';OUT=A/'ACTIVE_AUTHORING_CHECKPOINT_RESONANCE_INTAKE_FEAT_RESOLUTION_85.json';CHECK=A/'ACTIVE_AUTHORING_CHECKPOINT_RESONANCE_INTAKE_FEAT_RESOLUTION_85_CHECK.json';DISPATCH=A/'FEAT_TIME_INTERFACES_ACTUAL_DISPATCH_85.json';BACKUP=A/'navigation-before-resonance-intake-feat-resolution-85';SAVED=A/Path(__file__).name
for p in [OUT,CHECK,DISPATCH,BACKUP,SAVED]:assert not p.exists(),str(p)
def j(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def enc(x):return (json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
def info(p):
 b=p.read_bytes();return {'path':p.relative_to(G).as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
checks=[]
def ck(label,value):
 checks.append({'check':label,'pass':bool(value)})
 if not value:raise AssertionError(label)
cp=j(OLD);ck('Exact checkpoint84',info(OLD)['sha256']=='9209461d632fdacf98a844bf40661f1eef98163b2882a3544d75f9c387b07d94')
fr=A/'FEAT335_RESOLUTION_CASES_85.json';fv=A/'FEAT335_RESOLUTION_CHECK_85.json';r=j(fr);v=j(fv)
ck('103checks36resolutioncases passed',v['checkCount']==103 and v['failures']==0 and all(x['pass'] for x in v['checks']) and r['caseCount']==36 and len(r['cases'])==36)
ck('Exact new resolution artifacts',info(fr)==v['report'] and info(G/v['archive']['path'])==v['archive'])
for row in r['sourceBindings']:ck('Exact resolution source '+row['path'],info(G/row['path'])==row)
intake=A/'RANK9_RESONANCE_FIELDS3_PART5_RETURN01_INTAKE_85.json';it=j(intake)
reconstruction=A/'RANK9_RESONANCE_FIELDS3_INDEPENDENT_RECONSTRUCTION_85.json';rc=j(reconstruction)
ck('Actual130check intake completed',it['checkCount']==130 and it['failures']==0 and not it['independentExactAcceptance'])
for key in ['archive','model','manifest','nativeResponse','browserResponse']:ck('Exact received artifact '+key,info(G/it[key]['path'])==it[key])
ck('Independent166check complete forward/inverse reconstruction',rc['checkCount']==166 and rc['failures']==0 and all(x['pass'] for x in rc['checks']) and not rc['canonicalMutation'] and not rc['downloadedCodeExecuted'])
ck('Independent reconstruction binds received MODEL',rc['sourceModel']==it['model'])
protected=[cp['currentAuthoredIndex'],cp['currentAcceptedInterfaceRegistry'],cp['currentWorkQueue'],*cp['canonicalHelperBaselinesUnchanged']]
for row in protected:ck('Protected canonical authority '+row['path'],info(G/row['path'])==row)
ck('Canonical and accepted counts unchanged',cp['acceptedButUnapplied']==50 and not cp['implementationApplied'])
native=A/'GPT_FEAT_TIME_INTERFACES_SENT_NATIVE_85.json';nd=j(native);turn=nd['turns'][0]
ck('Actual new GPT user message',turn['id']=='e4fba178-593e-4596-915e-b408935b1b8e')
user=next(x for x in turn['items'] if x['type']=='userMessage');native_message='\n'.join(c['text'] for c in user['content'] if c.get('type')=='text').strip()
attachment_annotation='\n\n[User attached 2 files; file contents were not included]'
ck('Native connector separately annotates both attachments',native_message.endswith(attachment_annotation))
message=native_message[:-len(attachment_annotation)]
request=A/'GPT_FEAT_TIME_INTERFACES_REQUEST_85_VERIFIED.txt';request_text=request.read_text(encoding='utf-8')
ck('Actual sent message equals complete verified request',message.strip()==request_text.strip())
ck('All3exact questions present in actual message',all(q in message for q in ['FT84-Q01','FT84-Q02','FT84-Q03']))
browser=A/'GPT_FEAT_TIME_INTERFACES_HANDOFF_85.txt';bt=browser.read_text(encoding='utf-8');sent=A/'GPT_FEAT_TIME_INTERFACES_SENT_85.txt';st=sent.read_text(encoding='utf-8')
ck('Actual user message has both full source attachments',all('button "'+name+'"' in st for name in ['DD_Feat335_Work_Compositions_84.zip','DD_Feat335_Time_Provisions_Cases_83.zip']))
ck('Specific new GPT process is live at3m7s','Working for 3m 7s' in bt and 'button "Stop"' in bt and 'Reviewed FT84-Q01–Q03 source package artifacts' in bt)
proof=A/'GPT_FEAT_TIME_INTERFACES_SENT_85.png';ck('Visible sent-message screenshot preserved',proof.exists() and proof.stat().st_size>1000)
archives=[A/'DD_Feat335_Work_Compositions_84.zip',A/'DD_Feat335_Time_Provisions_Cases_83.zip']
for p,expected in [(archives[0],cp['featWorkCompositionsDiagnostics']['archive']),(archives[1],cp['featTimeProvisionsDiagnostics']['archive'])]:ck('Exact sent full archive '+p.name,info(p)==expected)
drafts=[A/'GPT_FEAT_TIME_INTERFACES_ACTUAL_REQUEST_85.txt',A/'GPT_FEAT_TIME_INTERFACES_ACTUAL_REQUEST_85_COMPLETE.txt']
DISPATCH.write_bytes(enc({'status':'ACTUALLY_SENT_AND_LIVE','threadId':nd['thread']['id'],'threadTitle':nd['thread']['title'],'actualUserMessageId':turn['id'],'request':info(request),'archives':[info(p) for p in archives],'nativeEvidence':info(native),'sentBrowserEvidence':info(sent),'liveBrowserEvidence':info(browser),'screenshot':info(proof),'questionIds':['FT84-Q01','FT84-Q02','FT84-Q03'],'supersededUnsentComposerDrafts':[info(p) for p in drafts],'draftCorrection':'The prepared84 request contained all questions but repeated its context separator. Pre-send checks caught omittedQ01 in intermediate composer drafts. Neither draft was sent; the final message was composed from all3full JSON dispositions, verified in the textbox and verified against the actual native sent message. All earlier files remain preserved.','resonanceReturnAcknowledged':info(intake),'canonicalImplementationApplied':False}))
navs=[G/'START_HERE.md',R/'docs/DEVELOPMENT_DIRECTION.md',G/'REVIEW_MAP.html'];originals={p:p.read_bytes() for p in navs}
for row in cp['navigation']:ck('Exact prior navigation '+row['path'],info(G/row['path'])==row)
BACKUP.mkdir()
for p,b in originals.items():(BACKUP/p.name).write_bytes(b)
base='docs/audit/2026-10-08/full-game/'
for p,prefix in [(navs[0],''),(navs[1],'../../../')]:
 b=originals[p];pos=b.index(b'\n')+1
 notice=('\n**Current checkpoint — 20 October 2026:** [Checkpoint85]('+prefix+base+OUT.name+') preserves GPT’s complete Resonance Fields3 return:130intake checks and166independent forward/reverse reconstruction checks pass; semantic encounter review remains open.36additional feat resolution cases pass103checks. GPT is now reviewing the3exact feat timing questions with both full source packets. Canonical525/323/249,173interfaces and50accepted-unapplied remain unchanged. [The75-domain map]('+prefix+base+'FULL_GAME_CURRENT_REVIEW_MAP_82.md) remains the overall map.\n').encode('utf-8')
 p.write_bytes(b[:pos]+notice+b[pos:]);ck('Every prior navigation byte retained '+p.name,p.read_bytes().replace(notice,b'',1)==b)
p=navs[2];b=originals[p];pos=b.index(b'</h1>')+5
notice=('<section class="sequence" aria-label="Current Resonance intake and feat resolution"><p><strong>Checkpoint85: complete Resonance return preserved.</strong>Exact forward/reverse reconstruction passes; semantic encounter review is pending.36feat resolution cases pass103checks. GPT is reviewing3targeted feat timing interfaces. <a href="'+base+OUT.name+'">Current checkpoint</a> · <a href="'+base+'FULL_GAME_CURRENT_REVIEW_MAP_82.md">75-domain map</a></p></section>').encode('utf-8');p.write_bytes(b[:pos]+notice+b[pos:]);ck('Every prior review-map byte retained',p.read_bytes().replace(notice,b'',1)==b)
prior=deepcopy(cp['activeGptReviewAtLastVerifiedObservation']);prior.update(completedResponseReceived=True,activeGenerationVerified=False,completionReceipt=info(intake),latestObservedStatus='Completed actual assistant c50fc964-e03a-4efe-ab7b-6e92da1bc82a; full return downloaded, preserved and independently reconstructed. Semantic review pending.')
cp['previousGptObservationBefore85']=prior
cp['activeGptReviewAtLastVerifiedObservation']={'threadId':nd['thread']['id'],'threadTitle':nd['thread']['title'],'group':'feat335-time-interfaces3','actualUserTurn':turn['id'],'dispatch':info(DISPATCH),'browserObservation':info(browser),'activeGenerationVerified':True,'completedResponseReceived':False,'latestObservedStatus':'Actual targeted3question review live at3m7s; source archives and FT84-Q01–Q03 inspected; Stop visible. Native turn status may lag actual browser generation.'}
cp.update(id='ACTIVE-AUTHORING-RESONANCE-INTAKE-FEAT-RESOLUTION-85',recordedAtUtc=datetime.now(timezone.utc).isoformat(),previousCheckpoint=info(OLD),status='Actual ResonanceFields3 Return01 preserved with130intake and166independent reconstruction checks; full semantic encounter review pending.36new feat resolution cases103checks passed. Three exact feat timing questions actually sent with complete83/84archives; GPT review live.',completedResonanceFields3Return01={'receipt':info(intake),'reconstruction':info(reconstruction),'archive':it['archive'],'model':it['model'],'actualAssistantId':'c50fc964-e03a-4efe-ab7b-6e92da1bc82a','independentExactAcceptance':False,'canonicalApplied':False,'fullProceduresRead':True,'sharedRulesQuestionsAndFullCaseSemanticReviewComplete':False},featResolutionDiagnostics={'report':info(fr),'archive':v['archive'],'validation':info(fv),'cases':36,'checkCount':103,'failures':0,'runtimeTestsExecuted':0,'remainingScope':r['remainingScope']},featTimeInterfacesActualDispatch=info(DISPATCH),navigation=[info(p) for p in navs],preservedNavigation=[info(BACKUP/p.name) for p in navs],lastUsageObservation={'usedPercent':43,'remainingPercent':57,'stopAtRemainingPercent':20,'resetsAt':1793110625},previousGoalTurnClassification='84 made concrete progress:78work/repair cases159checks and3real source-interface dispositions.85adds36resolution cases103checks, preserves the actual completed Resonance return, reconstructs its21full-value operations forward/backward exactly, and actually starts the3question GPT follow-through. No blocked condition.',laterLocalWork='All73–85work remains local after the verified GitHub backup through72.',nextAction='Finish independent authored semantic review of complete Resonance shared clauses,24dispositions,7positive encounters/28branches, actual actors/costs/history/all-magic and lifecycle obligations. Receive the same live feat time3 return without interruption. Continue remaining FXC07 healing/reserve and other full335 gates. Bestiary V3 with complete EX58 supplement remains prepared and unsent; all75domain integration and whole-game gates stay open.')
OUT.write_bytes(enc(cp))
for row in protected:ck('Canonical authority unchanged at completion '+row['path'],info(G/row['path'])==row)
SAVED.write_bytes(Path(__file__).read_bytes());CHECK.write_bytes(enc({'checkpoint':info(OUT),'checks':checks,'checkCount':len(checks),'failures':0,'newRuleAdoptions':0,'newDomainClosures':0,'canonicalImplementationApplied':False,'runtimeTestsExecuted':0,'sourceInformationDeleted':0}))
print(json.dumps({'checkpoint':info(OUT),'check':info(CHECK),'dispatch':info(DISPATCH),'checks':len(checks),'failures':0}))
