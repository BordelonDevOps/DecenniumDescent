"""Advance complete source preparation and retain verified live recovery observation."""
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
previous=A/'ACTIVE_AUTHORING_CHECKPOINT_ALIGNMENT_FACTION_RANK7_RECOVERY_77.json';out=A/'ACTIVE_AUTHORING_CHECKPOINT_RANK9_MASS_UNDEATH_78.json'
oldq=R/'data/director/spell_review/remaining_work_queue_64.json';newq=oldq.with_name('remaining_work_queue_65.json')
prepfile=A/'RANK9_MASS_UNDEATH_2_SOURCE_CONFERENCE_01_PREPARATION.json';report=out.with_name(out.stem+'_CHECK.json');navbackup=A/'navigation-before-rank9-mass-undeath-78';script=A/Path(__file__).name
assert not any(p.exists() for p in [out,newq,report,navbackup,script])
cp,q0,prep=map(read,[previous,oldq,prepfile]);q=deepcopy(q0);candidate=read(G/prep['candidate']['path']);sc=read(G/prep['check']['path']);checks=[]
def ck(n,v):checks.append({'check':n,'passed':bool(v)});assert v,n
ck('Exact checkpoint77',info(previous)['sha256']=='14801b3040adb0f60da1d599262747d62cc47106c5d5f8e56880589446ca6a32')
ck('Exact queue64',info(oldq)==cp['currentWorkQueue'])
protected=[previous,oldq,R/'data/public/spell_playtests/catalog.json',R/'data/playtest/game_development_coverage.json']
for k in ['currentAuthoredIndex','currentAcceptedInterfaceRegistry','decisionLedger']:
 b=cp[k];ck('Current authority '+k,info(G/b['path'])==b);protected.append(G/b['path'])
for b in cp['canonicalHelperBaselinesUnchanged']:
 ck('Current helper '+b['path'],info(G/b['path'])==b);protected.append(G/b['path'])
original={p:p.read_bytes() for p in protected}
for k in ['candidate','archive','manifest','check','request']:ck('Complete prepared artifact '+k,info(G/prep[k]['path'])==prep[k])
ck('Complete source preparation',prep['status']=='PREPARED_UNSENT' and prep['identityCount']==prep['placementCount']==2 and prep['sourceCount']==121 and prep['questionCount']==24 and prep['riskCounts']=={'C':2} and sc['checkCount']==350 and sc['failures']==0)
ck('24unique unselected questions',len(candidate['questions'])==len({q['id'] for q in candidate['questions']})==24 and not any(x['decisionSelected'] for x in candidate['questions']))
ck('Source-only no promotion',not candidate['currentVectors'] and candidate['newRuleAdoptions']==candidate['cosmologyDecisions']==0)
ctx=candidate['acceptedButUnappliedCompanionContext']
ck('Complete comparison scope',len(candidate['completeAppliedCounterparts'])==11 and len(candidate['completeClassSources'])==8 and len(candidate['currentAcceptedInterfaceComparisons'])==33 and len(ctx['fullEightAcceptedArtifacts'])==8 and len(ctx['completeOriginalInputArchives'])==2 and len(ctx['completeRelevantCompanionComparisons'])==7)
for b in ctx['fullEightAcceptedArtifacts']+ctx['completeOriginalInputArchives']:ck('Exact complete Companion comparison '+b['path'],info(G/b['path'])==b)
ids=[x['spellId'] for x in candidate['records']];ck('Exact two identities',ids==['field-of-endless-dead','plague-of-undeath'])
bp=A/'GPT_PART5_RANK7_RECOVERY_LIVE_78.txt';browser=bp.read_text('utf-8')
ck('Same live recovery observed','button "Stop"' in browser and 'Packaging Deterministic Recovery Archive' in browser and '6ad4a867-f330-83e9-829e-bf2bb41a6c09' in browser)
ck('Existing actual Rank7 recovery retained',cp['activeGptReviewAtLastVerifiedObservation']['userTurn']=='6ddb2852-f2fe-4293-b8a8-a326e5723067' and cp['currentRank7ExactModelRecovery']['reportedModelRecovered']['sha256']=='949ef5c6a1f05c1b0823d9ec4e10cd3e387a0c8c918680e95fa0047b60e40e3a')
status='Same submitted Rank7 recovery remains visibly generating. GPT reports exact input/model and reversal checks,deadline boundary checks and three reconstruction paths passing;two inherited evidence summaries synchronized to MODEL. Full final response/files remain pending. These live assertions are not independent local verification or acceptance.'
group={'group':'rank9-mass-undeath2','phase':'source-conference-prepared-unsent','identities':ids,'identityCount':2,'candidate':prep['candidate'],'preparation':info(prepfile),'archive':prep['archive'],'adopted':False,'sourceCount':121,'placementCount':2,'questionCount':24,'riskCounts':{'C':2},'currentCaseCount':0,'latestObservedStatus':'Field8permanent controlled skeletons/zombies andPlague ALLcorpses in1mile preserved.121full sources,24unselected questions,11applied counterparts,7accepted-unapplied Companion comparisons,8full accepted artifacts,2original archives,33scoped interfaces and350preservation checks. No selected procedure.'}
for g in q['groups']:
 if g['group']=='rank7-identity-casting5':
  g['previousObservationBefore78']={k:deepcopy(g.get(k)) for k in ['latestObservedStatus']};g.update(latestObservedStatus=status,latestRecoveryBrowserObservation=info(bp))
q['groups'].append(group)
for old,row in zip(q0['rows'],q['rows']):
 if row['id'] in ids:
  ck('Previously ungrouped '+row['id'],old['currentGroup'] is None);row.update(currentGroup=group['group'],currentPhase=group['phase'],semanticAcceptanceClaimed=False,sourceConferencePreparation=info(prepfile),nextAction='Submit complete two-spell source conference after the active review. Preserve8permanent controlled bodies andallcorpses within1mile;choose complete useful profiles,body/control lifecycles and mass-order procedure explicitly. No arbitrary quantity cap or historical monster-name substitution.')
 else:ck('Unaffected complete row '+row['id'],row==old)
 ck('Full original source/index/history preserved '+row['id'],all(row[k]==old[k] for k in ['completeCurrentSourceAndAccess','currentIndexEntryUnchanged','previousAuthoringMapRowUnchanged']))
q['previousSummaryBefore78']={k:deepcopy(q0[k]) for k in ['limitations','pendingDistribution','preparedOrActualReviewIdentityCount','originalSourceOrReceiptWorkCount']}
q.update(id='REMAINING-WORK-QUEUE-65',recordedAtUtc=datetime.now(timezone.utc).isoformat(),previousQueue=info(oldq),preparedOrActualReviewIdentityCount=319,originalSourceOrReceiptWorkCount=4,pendingDistribution=dict(Counter(x['currentPhase'] for x in q['rows'])),latestSourceConference=info(prepfile),latestRecoveryBrowserObservation=info(bp))
q['sourceBindings'].extend([info(prepfile),prep['candidate'],prep['archive'],prep['check'],info(bp)]);q['latestActualReviewEvidence'].append(info(bp))
q['limitations']='Current78:applied525reviewed/323pending/249standalone/173interfaces;45accepted-unapplied.54groups cover319pending;4rank9 remain ungrouped. Mass-undeath2prepared with121full sources,24unselected questions,350checks. Same actual Rank7 recovery visibly generating andpackaging;no final files or new local acceptance. Original Return03 ZIP remains unavailable;exactreportedMODEL is preserved locally. Latest verified GitHub backup through72. Owner implementation reservation retained.'
ck('All323pending accounted',len(q['rows'])==323 and len(q['groups'])==54 and sum(x['currentGroup'] is not None for x in q['rows'])==319 and sum(x['currentGroup'] is None for x in q['rows'])==4)
ck('45accepted unapplied retained',sum(x['currentPhase'] in ['actual-exact-accepted-integration-staged-not-applied','actual-full-conference-accepted-successor-not-applied'] for x in q['rows'])==45)
for a,b in zip(q['groups'][:-1],q0['groups']):
 if a['group']!='rank7-identity-casting5':ck('Prior group unchanged '+a['group'],a==b)
ck('Exact four remaining',set(x['id'] for x in q['rows'] if x['currentGroup'] is None)=={'astral-projection','divine-intervention-greater','imprisonment','wish'})
ck('Distribution total',sum(q['pendingDistribution'].values())==323)
for b in cp['navigation']:ck('Previous navigation exact '+b['path'],info(G/b['path'])==b)
navpaths=[G/'START_HERE.md',R/'docs/DEVELOPMENT_DIRECTION.md',G/'REVIEW_MAP.html'];nav={p:p.read_bytes() for p in navpaths};navbackup.mkdir()
for p,b in nav.items():(navbackup/p.name).write_bytes(b)
newq.write_bytes(enc(q));base='docs/audit/2026-10-08/full-game/'
for p,prefix in [(navpaths[0],''),(navpaths[1],'../../../')]:
 raw=nav[p];pos=raw.index(b'\n')+1;notice=('\n**Current source checkpoint —20October2026:** [Checkpoint78]('+prefix+base+out.name+') and [Queue65]('+prefix+newq.relative_to(G).as_posix()+') add Field of Endless Dead and Plague of Undeath:121full sources,24unselected questions,350checks.54groups cover319pending;4remain ungrouped. GPT is packaging the separate Rank7exact-model recovery.45accepted-unapplied;applied525/323/249 and173interfaces unchanged. Latest verified GitHub backup through72.\n').encode();p.write_bytes(raw[:pos]+notice+raw[pos:]);ck('Prior navigation retained '+p.name,p.read_bytes().replace(notice,b'',1)==raw)
p=navpaths[2];raw=nav[p];pos=raw.index(b'</h1>')+len(b'</h1>');notice=('<section class="sequence" aria-label="Current mass undeath source preparation"><p><strong>Checkpoint78: both Rank9 mass-undeath sources prepared.</strong>121full sources,24unselected questions,350checks. Queue65:319grouped/4ungrouped. Rank7recovery still generating;45accepted-unapplied;no new rules applied. <a href="'+base+out.name+'">Current checkpoint</a></p></section>').encode();p.write_bytes(raw[:pos]+notice+raw[pos:]);ck('Prior review map retained',p.read_bytes().replace(notice,b'',1)==raw)
cp['previousGptObservationBefore78']=deepcopy(cp['activeGptReviewAtLastVerifiedObservation']);cp['activeGptReviewAtLastVerifiedObservation'].update(browserObservation=info(bp),latestObservedStatus=status,activeGenerationVerified=True,completedResponseReceived=False)
cp.update(id='ACTIVE-AUTHORING-RANK9-MASS-UNDEATH-78',recordedAtUtc=datetime.now(timezone.utc).isoformat(),previousCheckpoint=info(previous),currentWorkQueue=info(newq),preparedGroupCount=54,groupedPendingIdentities=319,ungroupedPendingIdentities=4,rank9MassUndeath2SourceConference=info(prepfile),status='Two mass-undeath identities prepared with complete source/history and24unselected questions. Same Rank7recovery is visibly generating;complete final files remain pending.',navigation=[info(p) for p in navpaths],preservedNavigation=[info(navbackup/p.name) for p in navpaths],lastUsageObservation={'usedPercent':36,'remainingPercent':64,'stopAtRemainingPercent':20,'resetsAt':1793110625},previousGoalTurnClassification='Progress:77 recovered exact reported Rank7MODEL,actually submitted full recovery packet,and completed five-identity source conference/Queue64. Current78 completed two more full source identities and verified the same live GPT process without restarting it.',laterLocalWork='All73–78 source/review/recovery artifacts and queues/checkpoints remain local after verified GitHub backup through72.',nextAction='Receive/download the completed Rank7recovery artifacts and independently verify their exactMODEL,full mirrors,source bindings and boundary diagnostics before acceptance. Prepare the final four ungrouped identities: Astral Projection has4placements and unresolved plane/body relationship;Imprisonment2placements requires multiple meaningful confinement modes;GreaterDivineIntervention1placement is a Director-determined question/task miracle;Wish2placements saysreshape reality and supplies no imported copy menu. Preserve actual class schools and careful cosmology boundaries. Continue queued full-source GPT conferences.',queueObservationSupersession='Queue65 preserves every prior complete source/index/history row,adds the two mass-undeath sources,and records a fresh same-process GPT observation without claiming final acceptance.')
ck('No new acceptance or implementation',cp['authoredCounts']=={'reviewed':525,'pending':323,'standalone':249,'total':848} and cp['acceptedButUnapplied']==45 and not cp['implementationApplied'])
out.write_bytes(enc(cp));script.write_bytes(Path(__file__).read_bytes())
for p,b in original.items():ck('Protected authority unchanged '+p.relative_to(G).as_posix(),p.read_bytes()==b)
report.write_bytes(enc({'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'checkpoint':info(out),'queue':info(newq),'checks':checks,'checkCount':len(checks),'failures':0,'newRuleAdoptions':0,'runtimeTestsExecuted':0,'sourceInformationDeleted':0,'scope':'Full source/context/queue/navigation preservation and verified live process observation;no new semantic acceptance,runtime,balance orcosmology implementation.'}))
print(json.dumps({'checkpoint':info(out),'queue':info(newq),'report':info(report),'checks':len(checks),'failures':0,'remainingUngrouped':4}))
