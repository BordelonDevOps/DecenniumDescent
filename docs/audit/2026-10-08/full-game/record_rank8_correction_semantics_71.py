"""Record completed bounded semantic review and one prepared follow-up question."""
from pathlib import Path
from datetime import datetime,timezone
from collections import Counter
from copy import deepcopy
import hashlib,json
G=Path(r'C:\Github\DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game'
def read(p):return json.loads(p.read_bytes())
def enc(x):return (json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode()
def info(p):
 b=p.read_bytes();return {'path':p.relative_to(G).as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def main():
 old=A/'ACTIVE_AUTHORING_CHECKPOINT_RANK8_RETURN_RANK7_DISPATCH_70.json';out=A/'ACTIVE_AUTHORING_CHECKPOINT_RANK8_CORRECTION_SEMANTICS_71.json';report=out.with_name(out.stem+'_CHECK.json')
 newq=R/'data/director/spell_review/remaining_work_queue_58.json';backup=A/'navigation-before-rank8-correction-semantics-71';saved=A/Path(__file__).name
 assert not any(p.exists() for p in [out,report,newq,backup,saved])
 cp=read(old);oldq=G/cp['currentWorkQueue']['path'];q0=read(oldq);q=deepcopy(q0);checks=[]
 def ck(name,ok):checks.append({'check':name,'passed':bool(ok)});assert ok,name
 ck('Exact checkpoint70',info(old)['sha256']=='f6724f9a309a400f917841d5323a6d2a0c9fab769119fea8c74088cb52b154b1')
 protected=[old,R/'data/public/spell_playtests/catalog.json',R/'data/playtest/game_development_coverage.json']
 for key in ['currentWorkQueue','currentAuthoredIndex','currentAcceptedInterfaceRegistry','decisionLedger']:
  b=cp[key];ck('Authority '+key,info(G/b['path'])==b);protected.append(G/b['path'])
 for b in cp['canonicalHelperBaselinesUnchanged']:
  ck('Helper '+b['path'],info(G/b['path'])==b);protected.append(G/b['path'])
 originals={p:p.read_bytes() for p in protected}
 sempath=A/'RANK8_DAMAGE6_PART5_CORRECTION_RETURN_02_SEMANTIC_RECONCILIATION_70.json';sem=read(sempath)
 preppath=A/'RANK8_DAMAGE6_CAST_HISTORY_CORRECTION_02_PREPARATION.json';prep=read(preppath)
 ck('334 applicable diagnostics and one source qualification',sem['diagnosticCheckCount']==334 and sem['diagnosticFailures']==1 and sem['findingsCount']==1 and sum(x['passed'] for x in sem['diagnosticChecks'])==333)
 ck('All eight original findings reconciled',len(sem['originalFindingDispositions'])==8 and all(x['localDisposition']=='CORRECTION_SEMANTICALLY_RECONCILED_AT_SUPPLIED_INPUTS' for x in sem['originalFindingDispositions']))
 ck('No claimed runtime or new acceptance',sem['newAcceptedIdentities']==sem['canonicalChanges']==sem['runtimeTestsExecuted']==0 and sem['downloadedCodeExecuted'] is False)
 for key in ['request','archive','manifest','semanticReview']:ck('Prepared full follow-up '+key,info(G/prep[key]['path'])==prep[key])
 ck('One question remains actually unsent',prep['status']=='PREPARED_UNSENT' and prep['questionCount']==1)
 statuspath=A/'GPT_PART5_RANK7_CORRECTION_STATUS_71.json';status=read(statuspath)
 ck('Same real Rank7 request still pending',status['lastUserTurn']=='da1a6a38-58f0-48f8-a594-1edade3d774f' and status['assistantFinalPresent'] is False)
 evidence={'semanticReview':info(sempath),'originalUnmodifiedDiagnostics':sem['originalUnmodifiedDiagnosticReport'],'originalFindingsReconciled':8,'applicableDiagnostics':334,'diagnosticsPassed':333,'outstandingQuestion':'RD8-LOCAL70-01','completeFollowUpPreparation':info(preppath),'followUpArchive':prep['archive'],'followUpSent':False,'newAcceptedIdentities':0,'implementationApplied':False}
 for group in q['groups']:
  if group['group']!='rank8-damage6':continue
  group['previousObservationBefore71']={k:deepcopy(group[k]) for k in ['phase','latestObservedStatus']}
  group.update(phase='corrected-return-one-cast-history-qualification-pending',latestObservedStatus='All eight original corrections independently reconciled;333 of334 applicable diagnostics pass. One additional Anchor prepared-family history qualification affects nine supporting actor sheets. Full follow-up packet prepared UNSENT while Rank7 correction12 continues.',independentCorrectionSemanticReview=evidence)
 for row in q['rows']:
  if row.get('currentGroup')!='rank8-damage6':continue
  row['previousObservationBefore71']={k:deepcopy(row[k]) for k in ['currentPhase','nextAction']}
  row.update(currentPhase='corrected-return-one-cast-history-qualification-pending',nextAction='After active Rank7 correction12 finishes, confer on the single bound supporting-Anchor cast-history qualification using the full prepared packet; preserve all eight reconciled corrections and all originals. No cohort acceptance or implementation yet.')
 q['previousSummaryBefore71']={k:deepcopy(q[k]) for k in ['limitations','pendingDistribution']}
 q.update(id='REMAINING-WORK-QUEUE-58',recordedAtUtc=datetime.now(timezone.utc).isoformat(),previousQueue=info(oldq),pendingDistribution=dict(Counter(x['currentPhase'] for x in q['rows'])),currentRank8CorrectionSemanticReview=evidence)
 q['latestActualReviewEvidence'].extend([info(sempath),info(preppath),info(statuspath)])
 q['limitations']='Current71: all eight Rank8 correction findings reconciled;334 applicable diagnostics,333 pass and one additional Anchor cast-history qualification. Follow-up13 prepared unsent. Rank7 correction12 actually submitted; latest native has no final and browser shows ongoing output/Stop.50 groups/307 grouped/16 ungrouped pending identities. Applied525/323/249/173 and39 accepted-but-unapplied unchanged. No runtime,implementation,balance,cosmology or release acceptance. GitHub backup remains through65.'
 ck('All full source/history rows exact',len(q['rows'])==323 and all(all(a[k]==b[k] for k in ['id','completeCurrentSourceAndAccess','currentIndexEntryUnchanged','previousAuthoringMapRowUnchanged','semanticAcceptanceClaimed']) for a,b in zip(q['rows'],q0['rows'])))
 ck('Every unrelated full group exact',all(a==b for a,b in zip(q['groups'],q0['groups']) if a['group']!='rank8-damage6'))
 ck('Group membership unchanged',all(a['identities']==b['identities'] and a['candidate']==b['candidate'] for a,b in zip(q['groups'],q0['groups'])))
 ck('Counts and source bindings unchanged',len(q['groups'])==50 and q['ordinarySpellCounts']==q0['ordinarySpellCounts'] and q['sourceBindings']==q0['sourceBindings'] and sum(x['currentGroup'] is not None for x in q['rows'])==307 and sum(x['currentGroup'] is None for x in q['rows'])==16)
 for b in cp['navigation']:ck('Previous navigation '+b['path'],info(G/b['path'])==b)
 paths=[G/'START_HERE.md',R/'docs/DEVELOPMENT_DIRECTION.md',G/'REVIEW_MAP.html'];nav={p:p.read_bytes() for p in paths};backup.mkdir()
 for p,b in nav.items():(backup/p.name).write_bytes(b)
 newq.write_bytes(enc(q));base='docs/audit/2026-10-08/full-game/'
 for p,prefix in [(paths[0],''),(paths[1],'../../../')]:
  raw=nav[p];pos=raw.index(b'\n')+1
  notice=('\n**Current semantic review — 20 October 2026:** [Checkpoint71]('+prefix+base+out.name+') reconciles all eight Rank8 corrections.334 applicable diagnostics leave one supporting-Wizard cast-history question; its full follow-up packet is prepared unsent. GPT is working on the actual Rank7 correction12 request. Queue58 retains307 grouped/16 ungrouped pending identities. Applied525/323/249,173 interfaces and39 accepted-but-unapplied are unchanged. Owner implementation reservation remains; GitHub backup through65.\n').encode()
  p.write_bytes(raw[:pos]+notice+raw[pos:]);ck('Original navigation retained '+p.name,p.read_bytes().replace(notice,b'',1)==raw)
 p=paths[2];raw=nav[p];pos=raw.index(b'</h1>')+len(b'</h1>')
 notice=('<section class="sequence" aria-label="Current correction semantic review"><p><strong>Checkpoint71: eight Rank8 corrections reconciled.</strong>One supporting-Wizard cast-history question remains; follow-up prepared. GPT continues Rank7 correction12. Queue58 preserves307 grouped/16 ungrouped pending identities. No rules applied. <a href="'+base+out.name+'">Current checkpoint</a></p></section>').encode()
 p.write_bytes(raw[:pos]+notice+raw[pos:]);ck('Original map retained',p.read_bytes().replace(notice,b'',1)==raw)
 cp['previousGptObservationBefore71']=deepcopy(cp['activeGptReviewAtLastVerifiedObservation'])
 cp['activeGptReviewAtLastVerifiedObservation'].update(latestRecheck=info(statuspath),latestObservedStatus='Actual Rank7 correction12 remains the latest user message; native has no assistant final while browser shows continuing source/tool output and Stop. Do not interrupt or duplicate.')
 cp.update(id='ACTIVE-AUTHORING-RANK8-CORRECTION-SEMANTICS-71',recordedAtUtc=datetime.now(timezone.utc).isoformat(),previousCheckpoint=info(old),status='Eight original Rank8 findings independently reconciled; one additional supporting-caster history qualification prepared for GPT. Rank7 corrections still responding.',currentWorkQueue=info(newq),rank8CorrectionIndependentSemanticReview=evidence,navigation=[info(p) for p in paths],preservedNavigation=[info(backup/p.name) for p in paths],lastUsageObservation={'usedPercent':26,'remainingPercent':74,'stopAtRemainingPercent':20},queueObservationSupersession='Queue58 updates Rank8 review status only; full membership,all sources and39 accepted-but-unapplied unchanged.',nextAction='Receive complete Rank7 correction12 when available; send prepared Rank8 Anchor-history question13 afterward. Continue independent remaining16 rank9 source preparations and full pending conferences while preserving owner implementation reservation.',laterLocalWork='Checkpoints66–71,Queue58,Rank8 semantic review/follow-up and Rank7 exchange remain local after verified backup through65.',previousGoalTurnClassification='Progress: independent arithmetic/geometry/state review reconciles eight corrections and prepares one additional source-bound history qualification; original diagnostic correction explicitly preserved.')
 ck('No applied or accepted increment',cp['authoredCounts']=={'reviewed':525,'pending':323,'standalone':249,'total':848} and cp['acceptedButUnapplied']==39 and not cp['implementationApplied'])
 out.write_bytes(enc(cp));saved.write_bytes(Path(__file__).read_bytes())
 for p,b in originals.items():ck('Protected authority unchanged '+p.relative_to(G).as_posix(),p.read_bytes()==b)
 report.write_bytes(enc({'checkpoint':info(out),'queue':info(newq),'checks':checks,'checkCount':len(checks),'failures':0,'sourceInformationDeleted':0,'implementationApplied':False,'scope':'Review evidence,source/history/queue/navigation preservation; not runtime or whole-game completion.'}))
 print(json.dumps({'checkpoint':info(out),'queue':info(newq),'report':info(report),'checks':len(checks),'failures':0}))
if __name__=='__main__':main()
