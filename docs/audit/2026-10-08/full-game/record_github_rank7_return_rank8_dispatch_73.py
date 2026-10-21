"""Record backup72, full Rank7 correction intake and actual Rank8 follow-up13."""
from pathlib import Path
from datetime import datetime,timezone
from copy import deepcopy
from collections import Counter
import hashlib,json
G=Path(r'C:\Github\DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game'
W=Path(r'C:\Users\cbord\Documents\ChatGPT\Decennium Descent\audit_work')
def read(p):return json.loads(p.read_bytes())
def enc(x):return (json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
def info(p):
 b=p.read_bytes();return {'path':p.relative_to(G).as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def main():
 old=A/'ACTIVE_AUTHORING_CHECKPOINT_RANK9_MATERIAL_FORGING_72.json';out=A/'ACTIVE_AUTHORING_CHECKPOINT_GITHUB_RANK7_CORRECTIONS_73.json'
 oldq=R/'data/director/spell_review/remaining_work_queue_59.json';newq=oldq.with_name('remaining_work_queue_60.json')
 report=A/'ACTIVE_AUTHORING_CHECKPOINT_GITHUB_RANK7_CORRECTIONS_73_CHECK.json';backup=A/'navigation-before-github-rank7-corrections-73'
 script=A/Path(__file__).name
 copies=['GPT_PART5_RANK8_CAST_HISTORY_CORRECTION_13_DISPATCH_NATIVE.json','GPT_PART5_RANK8_CAST_HISTORY_CORRECTION_13_DISPATCH_TEXT.txt','RANK7_CORRECTION_RETURN02_DOWNLOAD_RECEIPT_73.json']
 assert not any(p.exists() for p in [out,newq,report,backup,script]+[A/n for n in copies])
 checks=[]
 def ck(n,v):checks.append({'check':n,'passed':bool(v)});assert v,n
 cp=read(old);q0=read(oldq);q=deepcopy(q0)
 ck('Exact checkpoint72',info(old)['sha256']=='de4828bf5b37c07e24cf76fd04550619991d0c20e1a33da3e0197c421132777a')
 ck('Exact queue59',info(oldq)==cp['currentWorkQueue'])
 protected=[old,oldq,R/'data/public/spell_playtests/catalog.json',R/'data/playtest/game_development_coverage.json']
 for key in ['currentAuthoredIndex','currentAcceptedInterfaceRegistry','decisionLedger']:
  b=cp[key];ck('Current authority '+key,info(G/b['path'])==b);protected.append(G/b['path'])
 for b in cp['canonicalHelperBaselinesUnchanged']:
  ck('Canonical helper '+b['path'],info(G/b['path'])==b);protected.append(G/b['path'])
 original={p:p.read_bytes() for p in protected}
 pushp=G/'docs/audit/2026-10-20/github-snapshot-material-forging72/PUSH_RECEIPT.json';push=read(pushp)
 ck('Verified remote backup through72',push['commit']==push['remoteMain']=='9367b319e460134a3fc35b530da29ecbe6224b6a' and push['snapshotCommit']=='5b49fbf2c49621ce93380d0ecc6e19062f31755b' and push['baseCommit']=='10b299c4af637032f40fab1704f60548ef1a9a1a' and push['worktreeClean'])
 ck('Full backup and retention',push['expectedBlobsVerified']==29766 and push['totalCommitEntries']==29965 and push['priorTrackedEntriesPreserved']==29412 and push['trackedEntriesDeleted']==push['sourceInformationDeleted']==0)
 prefp=A/'RANK7_IDENTITY_CASTING5_PART5_CORRECTION_RETURN_02_LOCAL_PREFLIGHT.json';pref=read(prefp)
 ck('1057 independent preservation/replay checks',pref['checkCount']==1057 and pref['failures']==0 and not pref['implementationApplied'] and pref['sourceFiles']==68 and pref['contextFiles']==10 and pref['manifestFiles']==72 and pref['oldReturnMembersPreserved']==51)
 ck('Exact11/38 reversible paths and15 replacements',pref['incrementalOperationsForwardAndReverse']==11 and pref['alternativeComposedOperationsForwardAndReverse']==38 and pref['fullArtifactReplacements']==15)
 for key in ['archive','model','nativeFinal']:ck('Current Rank7 corrected artifact '+key,info(G/pref[key]['path'])==pref[key])
 native=read(W/copies[0]);msg=next(i for t in native['turns'] for i in t['items'] if i['type']=='userMessage')
 ck('Actual Rank8 followup user turn',msg['id']=='04a9a52b-a43d-4ee5-b0a8-c961aeea3da6')
 content=next(i['text'] for i in msg['content'] if i['type']=='text');ck('Actual submitted text exact',(W/copies[1]).read_text('utf-8').rstrip('\n')==content.rstrip('\n'))
 attachment=next(a for a in native['attachments'] if a['name']=='DD_Rank8_Damage6_Cast_History_Correction_02.zip')
 ab=(A/attachment['name']).read_bytes();ck('Actual attached file complete',Path(attachment['path']).read_bytes()==ab and len(ab)==17596751 and hashlib.sha256(ab).hexdigest()=='bf32ada9d9e21b491a45c53b44a8bc1974f35213b2636ebad77ad53583fbe0e4')
 for n in copies:(A/n).write_bytes((W/n).read_bytes());ck('Preserved full dispatch/download evidence '+n,(A/n).read_bytes()==(W/n).read_bytes())
 dispatch={'threadId':'6ad4a867-f330-83e9-829e-bf2bb41a6c09','title':'Calibration Review Part 5','userTurn':msg['id'],
  'request':info(A/copies[1]),'fullPreparedRequest':info(A/'GPT_PART5_RANK8_CAST_HISTORY_CORRECTION_13_REQUEST.txt'),
  'archive':info(A/attachment['name']),'nativeConfirmation':info(A/copies[0]),'sent':True,'completedResponseReceived':False,
  'attachmentBytesIndependentlyVerified':True,'scope':'One additional Anchor supporting-caster first-family history qualification; eight original findings remain independently reconciled.',
  'latestObservedStatus':'Actual submitted user message and exact attachment verified. Browser screenshot shows GPT working on all nine supporting sheets. No finished Return03 received at this checkpoint.',
  'screenshotLocalOnly':str(W/'gpt-rank8-history-dispatch73.jpg')}
 ret={k:pref[k] for k in ['archive','model','nativeFinal','assistantTurn']}
 ret.update(localPreflight=info(prefp),status='FULL_CORRECTED_RETURN_PRESERVED_PENDING_INDEPENDENT_SEMANTIC_REVIEW',
  preservationChecks=1057,sourceFiles=68,laterContextFiles=10,manifestFiles=72,originalReturnMembers=51,
  incrementalOperations=11,alternativeSourceOperations=38,completeArtifactReplacements=15,mainCases=10,independentBranches=39,conditionalBranches=11,
  newAcceptedIdentities=0,implementationApplied=False,semanticNext='Independently check original three finding groups and separately disclosed cadence changes in RIC5-01-B-f,RIC5-02-A-a,RIC5-01-A-g. Do not promote based solely on preserved/replayed data.')
 updates={'rank7-identity-casting5':('corrected-return-pending-independent-semantic-review','Full correction Return02 preserved with1057 checks; unchanged procedures/questions/holds; three supplied findings plus three additional cadence repairs await independent semantic acceptance.'),
  'rank8-damage6':('cast-history-followup-actually-sent','All eight original findings remain reconciled. The one additional Anchor history qualification is actually submitted in conference13 after Rank7 completed; response pending.')}
 affected=set()
 for g in q['groups']:
  if g['group'] not in updates:continue
  phase,status=updates[g['group']];g['previousObservationBefore73']={'phase':g['phase'],'latestObservedStatus':g['latestObservedStatus']}
  g.update(phase=phase,latestObservedStatus=status);affected.update(g['identities'])
  if g['group']=='rank7-identity-casting5':g['completedCorrectionReturn02']=deepcopy(ret)
  else:g['actualCastHistoryFollowup13']=deepcopy(dispatch)
 ck('Exactly11 affected pending identities',len(affected)==11)
 for prev,row in zip(q0['rows'],q['rows']):
  if row['id'] in affected:
   row['previousObservationBefore73']={k:deepcopy(row.get(k)) for k in ['currentPhase','nextAction','semanticAcceptanceClaimed']}
   phase,status=updates[row['currentGroup']];row.update(currentPhase=phase,nextAction=status,semanticAcceptanceClaimed=False)
  else:ck('Unchanged complete pending row '+row['id'],row==prev)
  ck('Original source/index/history retained '+row['id'],all(row[k]==prev[k] for k in ['completeCurrentSourceAndAccess','currentIndexEntryUnchanged','previousAuthoringMapRowUnchanged']))
 q['previousSummaryBefore73']={k:deepcopy(q0[k]) for k in ['limitations','pendingDistribution']}
 q.update(id='REMAINING-WORK-QUEUE-60',recordedAtUtc=datetime.now(timezone.utc).isoformat(),previousQueue=info(oldq),pendingDistribution=dict(Counter(x['currentPhase'] for x in q['rows'])))
 q['sourceBindings'].extend([info(prefp),pref['archive'],pref['model'],dispatch['nativeConfirmation'],info(pushp)])
 q['latestActualReviewEvidence'].extend([pref['nativeFinal'],dispatch['nativeConfirmation']])
 q['limitations']='Current through73: backup through72 verified on GitHub; all29412 prior tracked entries retained. Rank7 correction Return02 preserved with1057 independent source/history/mirror/reconstruction checks; three original findings and three new disclosed cadence repairs need semantic review. Rank8 Anchor history follow-up13 actually submitted after Rank7 finished; no completed successor yet. Applied525 reviewed/323 pending/249 standalone/173 interfaces and39 accepted-but-unapplied unchanged.51 groups cover309 pending identities;14 remain ungrouped rank9. No gameplay,runtime,balance or cosmology adoption. Owner implementation reservation remains.'
 ck('Queue membership retained',len(q['rows'])==323 and len(q['groups'])==51 and q['preparedOrActualReviewIdentityCount']==309 and q['originalSourceOrReceiptWorkCount']==14)
 ck('Exactly39 accepted unapplied remain',sum(x['currentPhase'] in ['actual-exact-accepted-integration-staged-not-applied','actual-full-conference-accepted-successor-not-applied'] for x in q['rows'])==39)
 ck('Pending distribution exact',sum(q['pendingDistribution'].values())==323)
 for b in cp['navigation']:ck('Previous navigation exact '+b['path'],info(G/b['path'])==b)
 navpaths=[G/'START_HERE.md',R/'docs/DEVELOPMENT_DIRECTION.md',G/'REVIEW_MAP.html'];nav={p:p.read_bytes() for p in navpaths};backup.mkdir()
 for p,b in nav.items():(backup/p.name).write_bytes(b)
 newq.write_bytes(enc(q));base='docs/audit/2026-10-08/full-game/'
 for p,prefix in [(navpaths[0],''),(navpaths[1],'../../../')]:
  raw=nav[p];pos=raw.index(b'\n')+1
  notice=('\n**Current backup and correction review — 20 October 2026:** [Checkpoint73]('+prefix+base+out.name+') records the verified [GitHub backup through72]('+push['url']+'). All29,412 prior tracked entries remain. Rank7 correction Return02 is preserved with1,057 independent reconstruction checks; semantic acceptance remains pending. Rank8 Anchor history follow-up13 is now actually sent. [Queue60]('+prefix+newq.relative_to(G).as_posix()+') retains309 grouped/14 ungrouped pending identities. Applied525/323/249,173 interfaces and39 accepted-but-unapplied unchanged; owner implementation reservation retained.\n').encode('utf-8')
  p.write_bytes(raw[:pos]+notice+raw[pos:]);ck('Prior navigation preserved '+p.name,p.read_bytes().replace(notice,b'',1)==raw)
 p=navpaths[2];raw=nav[p];pos=raw.index(b'</h1>')+len(b'</h1>')
 notice=('<section class="sequence" aria-label="Verified backup and ongoing correction review"><p><strong>Checkpoint73: backup through72 verified; Rank7 correction received.</strong>1,057 preservation/replay checks; semantic review pending. Rank8 follow-up13 actually sent. Queue60:309 grouped/14 ungrouped. No new rules applied. <a href="'+base+out.name+'">Current checkpoint</a> · <a href="'+push['url']+'">Verified GitHub commit</a></p></section>').encode('utf-8')
 p.write_bytes(raw[:pos]+notice+raw[pos:]);ck('Previous map preserved',p.read_bytes().replace(notice,b'',1)==raw)
 cp['previousGptObservationBefore73']=deepcopy(cp['activeGptReviewAtLastVerifiedObservation'])
 cp.update(id='ACTIVE-AUTHORING-GITHUB-RANK7-CORRECTIONS-73',recordedAtUtc=datetime.now(timezone.utc).isoformat(),previousCheckpoint=info(old),
  currentWorkQueue=info(newq),completedRank7IdentityCasting5CorrectionReturn02=ret,activeGptReviewAtLastVerifiedObservation=dispatch,
  latestPreviouslyVerifiedGitHubBackup={'commit':push['commit'],'snapshotCommit':push['snapshotCommit'],'throughCheckpoint':72,'receipt':info(pushp),'url':push['url']},
  status='Backup through72 verified; complete Rank7 correction Return02 preserved and reconstructed. Rank8 Anchor history follow-up13 actually submitted. Neither cohort newly accepted or applied.',
  navigation=[info(p) for p in navpaths],preservedNavigation=[info(backup/p.name) for p in navpaths],
  lastUsageObservation={'usedPercent':28,'remainingPercent':72,'stopAtRemainingPercent':20},
  previousGoalTurnClassification='Progress: checkpoint72 completed full material-forging2 source preparation. Current73 pushed and verified the backup,received/reconstructed the full Rank7 correction and actually sent Rank8 follow-up13.',
  laterLocalWork='Rank7 correction Return02 and1057-check preflight,actual Rank8 follow-up13,Queue60,this checkpoint and navigation arrived after the verified GitHub backup through72 and remain local for the next backup.',
  nextAction='Independently review the three original Rank7 correction groups and three newly disclosed cadence repairs. Receive full Rank8 history successor without interrupting. Continue14 ungrouped rank9 identities and remaining pending conferences. Preserve implementation reservation and20percent remaining limit.',
  queueObservationSupersession='Queue60 retains all previous full source/index/history fields and groups; updates only the11 affected review phases,retains prior observations,and recalculates current distribution.')
 ck('No gameplay application or acceptance increment',cp['authoredCounts']=={'reviewed':525,'pending':323,'standalone':249,'total':848} and cp['acceptedButUnapplied']==39 and not cp['implementationApplied'])
 out.write_bytes(enc(cp));script.write_bytes(Path(__file__).read_bytes())
 for p,b in original.items():ck('Protected authority unchanged '+p.relative_to(G).as_posix(),p.read_bytes()==b)
 report.write_bytes(enc({'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'checkpoint':info(out),'queue':info(newq),'checks':checks,'checkCount':len(checks),'failures':0,
  'newRuleAdoptions':0,'runtimeTestsExecuted':0,'sourceInformationDeleted':0,'scope':'Verified backup,intake,actual dispatch and complete source/history/queue/navigation preservation; no semantic acceptance or implementation.'}))
 print(json.dumps({'checkpoint':info(out),'queue':info(newq),'report':info(report),'checks':len(checks),'failures':0}))
if __name__=='__main__':main()
