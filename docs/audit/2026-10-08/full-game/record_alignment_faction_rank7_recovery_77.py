"""Record source preparation and exact-model recovery with actual GPT dispatch evidence."""
from pathlib import Path
from datetime import datetime,timezone
from copy import deepcopy
from collections import Counter
import hashlib,json
G=Path(r'C:\Github\DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game'
def read(p):return json.loads(p.read_bytes())
def enc(x):return (json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode()
def info(p):
 b=p.read_bytes();return {'path':p.relative_to(G).as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
previous=A/'ACTIVE_AUTHORING_CHECKPOINT_RANK9_RESONANCE_FIELDS_76.json';out=A/'ACTIVE_AUTHORING_CHECKPOINT_ALIGNMENT_FACTION_RANK7_RECOVERY_77.json'
oldq=R/'data/director/spell_review/remaining_work_queue_63.json';newq=oldq.with_name('remaining_work_queue_64.json')
prepfile=A/'RANK9_ALIGNMENT_FACTION_PURIFICATION_5_SOURCE_CONFERENCE_01_PREPARATION.json';report=out.with_name(out.stem+'_CHECK.json')
navbackup=A/'navigation-before-alignment-faction-rank7-recovery-77';script=A/Path(__file__).name;dispatchText=A/'GPT_PART5_RANK7_EXACT_MODEL_RECOVERY_77_DISPATCH_TEXT.txt'
assert not any(p.exists() for p in [out,newq,report,navbackup,script,dispatchText])
cp,q0,prep=map(read,[previous,oldq,prepfile]);q=deepcopy(q0);candidate=read(G/prep['candidate']['path']);sc=read(G/prep['check']['path']);checks=[]
def ck(n,v):checks.append({'check':n,'passed':bool(v)});assert v,n
ck('Exact checkpoint76',info(previous)['sha256']=='c226a0a550c84d9c5fc934121ad53648a93d59e5b7d4d25137685695d79b08d9')
ck('Exact queue63',info(oldq)==cp['currentWorkQueue'])
protected=[previous,oldq,R/'data/public/spell_playtests/catalog.json',R/'data/playtest/game_development_coverage.json']
for k in ['currentAuthoredIndex','currentAcceptedInterfaceRegistry','decisionLedger']:
 b=cp[k];ck('Current authority '+k,info(G/b['path'])==b);protected.append(G/b['path'])
for b in cp['canonicalHelperBaselinesUnchanged']:
 ck('Current helper '+b['path'],info(G/b['path'])==b);protected.append(G/b['path'])
original={p:p.read_bytes() for p in protected}
for k in ['candidate','archive','manifest','check','request']:ck('Exact prepared artifact '+k,info(G/prep[k]['path'])==prep[k])
ck('Complete preparation',prep['status']=='PREPARED_UNSENT' and prep['identityCount']==5 and prep['placementCount']==6 and prep['sourceCount']==124 and prep['questionCount']==28 and prep['riskCounts']=={'C':5} and sc['checkCount']==399 and sc['failures']==0)
ck('All28questions unselected',len(candidate['questions'])==28 and not any(x['decisionSelected'] for x in candidate['questions']))
ck('Complete comparison scope',len(candidate['completeAppliedCounterparts'])==21 and len(candidate['completeClassSources'])==7 and len(candidate['currentAcceptedInterfaceComparisons'])==38)
ck('No proposed procedure promoted',candidate['newRuleAdoptions']==candidate['cosmologyDecisions']==0 and not candidate['currentVectors'])
ids=[x['spellId'] for x in candidate['records']]
ck('Exact five identities',set(ids)=={'alignment-ascension','alignment-perfection','faction-incarnate','faction-perfection','corruption-purification'})
recoveryfile=A/'RANK7_EXACT_MODEL_RECOVERY_77.json';recovery=read(recoveryfile)
for k in ['model','originalModel','archive','manifest','operations','check','request','reportedFinal','actualUnavailableResponse']:ck('Recovered exact binding '+k,info(G/recovery[k]['path'])==recovery[k])
ck('Exact reported MODEL recovered',recovery['model']['sha256']=='949ef5c6a1f05c1b0823d9ec4e10cd3e387a0c8c918680e95fa0047b60e40e3a' and recovery['model']['bytes']==12000315)
ck('Original archive and mirrors not claimed recovered',not recovery['originalReturn03ZipRecovered'] and not recovery['completeReturn03ArtifactSetRecovered'] and recovery['newAcceptedIdentities']==0)
np=A/'GPT_PART5_RANK7_EXACT_MODEL_RECOVERY_77_DISPATCH_NATIVE.json';native=read(np);turn=native['turns'][0]
ck('Actual recovery submission',turn['id']=='6ddb2852-f2fe-4293-b8a8-a326e5723067')
u=next(i for i in turn['items'] if i['type']=='userMessage');text='\n'.join(c['text'] for c in u['content'] if c['type']=='text')
ck('Sent exact model and packet identity',recovery['model']['sha256'] in text and recovery['archive']['sha256'] in text and '45accepted-unapplied' in text)
attachment=next(x for x in native['attachments'] if x['name']=='DD_Rank7_Exact_Model_Recovery_77.zip');attachmentBytes=Path(attachment['path']).read_bytes()
ck('Actual uploaded attachment byte-identical',attachmentBytes==(G/recovery['archive']['path']).read_bytes())
bp=A/'GPT_PART5_RANK7_EXACT_MODEL_RECOVERY_77_BROWSER_STATUS.txt';browser=bp.read_text('utf-8')
ck('Actual browser confirms live generation despite native idle summary','button "Stop"' in browser and 'Working for 3m 14s' in browser and 'MODEL byte-identically' in browser)
missing=read(G/recovery['actualUnavailableResponse']['path']);mi=next(i for t in missing['turns'] for i in t['items'] if i['type']=='agentMessage')
ck('Actual GPT missing-original reply',mi['id']=='fb44cecc-7a8b-43b1-8ed6-0813b3ccfea0' and 'exact Return03 ZIP is unavailable' in mi['text'])
status='Original Return03 archive unavailable in current GPT session. Entire reported MODEL independently reconstructed exactly from six deadline changes; complete recovery packet actually uploaded and GPT visibly processing. Complete current artifact recovery and independent acceptance remain pending.'
group={'group':'rank9-alignment-faction-purification5','phase':'source-conference-prepared-unsent','identities':ids,'identityCount':5,'candidate':prep['candidate'],'preparation':info(prepfile),'archive':prep['archive'],'adopted':False,'sourceCount':124,'placementCount':6,'questionCount':28,'riskCounts':{'C':5},'currentCaseCount':0,'latestObservedStatus':'Five identities/six placements,124full sources,28unselected questions,21full applied counterparts,seven complete class sources,38scoped interfaces and399preservation checks. All original benefits and conflicts remain explicit; no selected procedure.'}
phase7='exact-model-recovered-full-artifact-recovery-submitted'
rs={'recoveryReceipt':info(recoveryfile),'reportedModelRecovered':recovery['model'],'recoveryArchive':recovery['archive'],'actualUnavailableReply':recovery['actualUnavailableResponse'],'dispatch':info(np),'actualUserTurn':turn['id'],'browserObservation':info(bp),'actualUploadedAttachmentBytesVerified':True,'originalReturn03ArchiveRecovered':False,'fullCurrentArtifactSetVerified':False,'semanticAcceptanceClaimed':False,'status':status}
for g in q['groups']:
 if g['group']=='rank7-identity-casting5':
  g['previousObservationBefore77']={k:deepcopy(g.get(k)) for k in ['phase','latestObservedStatus']};g.update(phase=phase7,latestObservedStatus=status,currentExactModelRecovery=deepcopy(rs))
q['groups'].append(group)
for old,row in zip(q0['rows'],q['rows']):
 if row['id'] in ids:
  ck('Previously ungrouped '+row['id'],old['currentGroup'] is None)
  row.update(currentGroup=group['group'],currentPhase=group['phase'],semanticAcceptanceClaimed=False,sourceConferencePreparation=info(prepfile),nextAction='Submit full five-identity source conference after active Rank7 recovery finishes. Resolve28genuine questions preserving Ascension form/insight,purification,real maximum reputation and useful faction embodiment; no source-only choice is adopted.')
 elif row['currentGroup']=='rank7-identity-casting5':
  row['previousObservationBefore77']={k:deepcopy(row.get(k)) for k in ['currentPhase','nextAction']};row.update(currentPhase=phase7,nextAction='Preserve completed GPT recovery response and download full current artifacts. Verify exact recovered MODEL and all documentary/state mirrors,source bindings,alternative paths and60.9/61/61.1 boundary before acceptance. Do not claim original missing ZIP recovery or execute downloaded Python.',semanticAcceptanceClaimed=False)
 else:ck('Unaffected full row '+row['id'],row==old)
 ck('Original complete source/index/history preserved '+row['id'],all(row[k]==old[k] for k in ['completeCurrentSourceAndAccess','currentIndexEntryUnchanged','previousAuthoringMapRowUnchanged']))
q['previousSummaryBefore77']={k:deepcopy(q0[k]) for k in ['limitations','pendingDistribution','preparedOrActualReviewIdentityCount','originalSourceOrReceiptWorkCount']}
q.update(id='REMAINING-WORK-QUEUE-64',recordedAtUtc=datetime.now(timezone.utc).isoformat(),previousQueue=info(oldq),preparedOrActualReviewIdentityCount=317,originalSourceOrReceiptWorkCount=6,pendingDistribution=dict(Counter(x['currentPhase'] for x in q['rows'])),latestSourceConference=info(prepfile),currentRank7ExactModelRecovery=deepcopy(rs))
q['sourceBindings'].extend([info(prepfile),prep['candidate'],prep['archive'],prep['check'],info(recoveryfile),info(np),info(bp)]);q['latestActualReviewEvidence'].extend([recovery['actualUnavailableResponse'],info(np),info(bp)])
q['limitations']='Current77:applied525reviewed/323pending/249standalone/173interfaces;45accepted-unapplied.53groups cover317pending;6rank9 remain ungrouped. Five alignment/faction/purification identities prepared with124full sources,28unselected questions,399checks. Exact reported Rank7 MODEL recovered; original fullZIP unavailable in GPT session. Complete recovery packet actually submitted and observed generating; no new semantic acceptance or canonical application. Latest verified GitHub backup through72. Owner implementation reservation retained.'
ck('All323pending accounted',len(q['rows'])==323 and len(q['groups'])==53 and sum(x['currentGroup'] is not None for x in q['rows'])==317 and sum(x['currentGroup'] is None for x in q['rows'])==6)
ck('45accepted still unapplied',sum(x['currentPhase'] in ['actual-exact-accepted-integration-staged-not-applied','actual-full-conference-accepted-successor-not-applied'] for x in q['rows'])==45)
for a,b in zip(q['groups'][:-1],q0['groups']):
 if a['group']!='rank7-identity-casting5':ck('Prior group unchanged '+a['group'],a==b)
ck('Five Rank7 recovery rows',sum(x['currentPhase']==phase7 for x in q['rows'])==5)
ck('Exact remaining six',set(x['id'] for x in q['rows'] if x['currentGroup'] is None)=={'astral-projection','divine-intervention-greater','field-of-endless-dead','imprisonment','plague-of-undeath','wish'})
ck('Exact distribution',sum(q['pendingDistribution'].values())==323)
for b in cp['navigation']:ck('Prior navigation exact '+b['path'],info(G/b['path'])==b)
navpaths=[G/'START_HERE.md',R/'docs/DEVELOPMENT_DIRECTION.md',G/'REVIEW_MAP.html'];nav={p:p.read_bytes() for p in navpaths}
navbackup.mkdir()
for p,b in nav.items():(navbackup/p.name).write_bytes(b)
newq.write_bytes(enc(q));dispatchText.write_text(text+'\n',encoding='utf-8',newline='\n');base='docs/audit/2026-10-08/full-game/'
for p,prefix in [(navpaths[0],''),(navpaths[1],'../../../')]:
 raw=nav[p];pos=raw.index(b'\n')+1;notice=('\n**Current source/recovery checkpoint —20October2026:** [Checkpoint77]('+prefix+base+out.name+') and [Queue64]('+prefix+newq.relative_to(G).as_posix()+') preserve five Rank9 alignment/faction/purification identities:124full sources,28unselected questions,399checks.53groups cover317pending;6remain ungrouped. Exact reported Rank7 MODEL recovered locally and sent to GPT for complete artifact recovery; original ZIP remains unavailable.45accepted-unapplied;applied525/323/249 and173interfaces unchanged. Latest verified GitHub backup through72.\n').encode();p.write_bytes(raw[:pos]+notice+raw[pos:]);ck('Prior navigation retained '+p.name,p.read_bytes().replace(notice,b'',1)==raw)
p=navpaths[2];raw=nav[p];pos=raw.index(b'</h1>')+len(b'</h1>');notice=('<section class="sequence" aria-label="Current alignment faction and Rank7 recovery"><p><strong>Checkpoint77: five Rank9 source identities prepared; exact Rank7 MODEL recovered.</strong>124full sources,28unselected questions,399checks. Queue64:317grouped/6ungrouped. GPT recovery submitted;45accepted-unapplied;no new rules applied. <a href="'+base+out.name+'">Current checkpoint</a></p></section>').encode();p.write_bytes(raw[:pos]+notice+raw[pos:]);ck('Prior review map retained',p.read_bytes().replace(notice,b'',1)==raw)
cp['previousGptObservationBefore77']=deepcopy(cp['activeGptReviewAtLastVerifiedObservation'])
cp['activeGptReviewAtLastVerifiedObservation']={'threadId':native['thread']['id'],'title':native['thread']['title'],'userTurn':turn['id'],'request':info(dispatchText),'fullPreparedRequest':recovery['request'],'archive':recovery['archive'],'nativeConfirmation':info(np),'sent':True,'completedResponseReceived':False,'attachmentBytesIndependentlyVerified':True,'actualAttachmentPath':attachment['path'],'scope':'Keep exact recovered Rank7 MODEL; deliver complete current mirrors and scoped Ready boundary evidence with newly identified recovery packaging. Original unavailable archive identity retained.','latestObservedStatus':status,'browserObservation':info(bp),'activeGenerationVerified':True,'nativeStatusQualification':'Native thread snapshot reports idle/completed user message; actual same-tab DOM visibly shows Working and Stop. Browser is the current generation observation. Re-poll before later claims.','screenshotLocalOnly':r'C:\Users\cbord\Documents\ChatGPT\Decennium Descent\audit_work\gpt-rank7-exact-recovery-dispatch77.png'}
cp.update(id='ACTIVE-AUTHORING-ALIGNMENT-FACTION-RANK7-RECOVERY-77',recordedAtUtc=datetime.now(timezone.utc).isoformat(),previousCheckpoint=info(previous),currentWorkQueue=info(newq),preparedGroupCount=53,groupedPendingIdentities=317,ungroupedPendingIdentities=6,rank9AlignmentFactionPurification5SourceConference=info(prepfile),currentRank7ExactModelRecovery=deepcopy(rs),status='Five remaining Rank9 identities prepared without selected rules. Exact reported Rank7 MODEL recovered from preserved original bytes and six deadline changes; complete artifact recovery actually submitted to GPT.',navigation=[info(p) for p in navpaths],preservedNavigation=[info(navbackup/p.name) for p in navpaths],lastUsageObservation={'usedPercent':36,'remainingPercent':64,'stopAtRemainingPercent':20,'resetsAt':1793110625},previousGoalTurnClassification='The immediate owner-directed GPT check reverified already-preserved Unity directions; no new authored state. Revalidated and took next safe actions: exact Rank7 model recovery/actual full-packet dispatch and five-identity source preparation. Current77 is concrete progress; no impasse.',laterLocalWork='All73–77 source/review/recovery artifacts,actual GPT messages and queues/checkpoints remain local after verified GitHub backup through72.',nextAction='Re-poll actual live GPT recovery, preserve full return and independently verify all current artifacts before Rank7 acceptance. Continue six remaining ungrouped rank9 preparations and queued full-source conferences; preserve original history,owner implementation reservation and20percent usage floor.',queueObservationSupersession='Queue64 preserves every source/index/history row,adds five source identities and replaces stale Rank7 download-pending observation with exact-model-recovered/current-artifact-recovery-submitted. No semantic acceptance is inferred.')
ck('No new acceptance/application',cp['authoredCounts']=={'reviewed':525,'pending':323,'standalone':249,'total':848} and cp['acceptedButUnapplied']==45 and not cp['implementationApplied'])
out.write_bytes(enc(cp));script.write_bytes(Path(__file__).read_bytes())
for p,b in original.items():ck('Protected authority unchanged '+p.relative_to(G).as_posix(),p.read_bytes()==b)
report.write_bytes(enc({'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'checkpoint':info(out),'queue':info(newq),'checks':checks,'checkCount':len(checks),'failures':0,'newRuleAdoptions':0,'runtimeTestsExecuted':0,'sourceInformationDeleted':0,'scope':'Source/history/queue/navigation preservation,exact recovered model bindings and actual upload evidence; no new authored acceptance/runtime/cosmology implementation.'}))
print(json.dumps({'checkpoint':info(out),'queue':info(newq),'report':info(report),'checks':len(checks),'failures':0,'remainingUngrouped':6}))
