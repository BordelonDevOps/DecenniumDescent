"""Record prepared resonance-field sources, actual GPT acknowledgement and pending intake."""
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
previous=A/'ACTIVE_AUTHORING_CHECKPOINT_RANK8_ACCEPTANCE_UNITY_INTAKE_75.json'
out=A/'ACTIVE_AUTHORING_CHECKPOINT_RANK9_RESONANCE_FIELDS_76.json'
oldq=R/'data/director/spell_review/remaining_work_queue_62.json';newq=oldq.with_name('remaining_work_queue_63.json')
prepfile=A/'RANK9_RESONANCE_FIELDS_3_SOURCE_CONFERENCE_01_PREPARATION.json'
report=out.with_name(out.stem+'_CHECK.json');navbackup=A/'navigation-before-rank9-resonance-fields-76';script=A/Path(__file__).name
assert not any(p.exists() for p in [out,newq,report,navbackup,script])
cp,q0,prep=map(read,[previous,oldq,prepfile]);q=deepcopy(q0);candidate=read(G/prep['candidate']['path']);sc=read(G/prep['check']['path'])
checks=[]
def ck(n,v):checks.append({'check':n,'passed':bool(v)});assert v,n
ck('Exact checkpoint75',info(previous)['sha256']=='43ee2e1598d044009fea96e6a337f1d43ac4b1487f6b1b3d0329d37a92785cf9')
ck('Exact queue62',info(oldq)==cp['currentWorkQueue'])
protected=[previous,oldq,R/'data/public/spell_playtests/catalog.json',R/'data/playtest/game_development_coverage.json']
for k in ['currentAuthoredIndex','currentAcceptedInterfaceRegistry','decisionLedger']:
 b=cp[k];ck('Current authority '+k,info(G/b['path'])==b);protected.append(G/b['path'])
for b in cp['canonicalHelperBaselinesUnchanged']:
 ck('Current canonical helper '+b['path'],info(G/b['path'])==b);protected.append(G/b['path'])
original={p:p.read_bytes() for p in protected}
for k in ['candidate','archive','manifest','check','request']:ck('Complete prepared artifact '+k,info(G/prep[k]['path'])==prep[k])
ck('Complete source-only preparation',prep['status']=='PREPARED_UNSENT' and prep['identityCount']==prep['placementCount']==3 and prep['sourceCount']==99 and prep['questionCount']==24 and prep['riskCounts']=={'C':3} and sc['checkCount']==296 and sc['failures']==0 and not candidate['currentVectors'] and candidate['newRuleAdoptions']==candidate['cosmologyDecisions']==0)
ck('24 unselected decisions',len(candidate['questions'])==24 and not any(x['decisionSelected'] for x in candidate['questions']))
ck('Nine applied comparisons and full pending archive',len(candidate['completeAppliedCounterparts'])==9 and len(candidate['pendingComparisonsNotAuthority'])==1 and len(candidate['completeClassFeatureComparisons'])==7 and len(candidate['currentAcceptedInterfaceComparisons'])==28)
ids=[x['spellId'] for x in candidate['records']]
ck('Exact three identities',set(ids)=={'arc-furnace','resonance-singularity','resonance-nexus-supreme'})
ck('Previously ungrouped',all(next(x for x in q['rows'] if x['id']==sid)['currentGroup'] is None for sid in ids))
rp=A/'RANK7_READY_DEADLINE_RETURN_03_AVAILABLE_75.json';available=read(rp);np=G/available['actualFinal']['path'];native=read(np)
ck('Preserved actual completed Rank7 reply',info(np)==available['actualFinal'] and any(i.get('id')=='b7cc95cd-bc1a-40c7-802a-b09859e01d9c' for t in native['turns'] for i in t['items']))
sp=A/'GPT_PART5_STATUS_SYNC_15_NATIVE.json';sync=read(sp)
ck('Actual status15 sent',sync['turns'][0]['id']=='85484c42-73a8-49d0-bb3f-5e1da9161a08')
ack=next(i for i in sync['turns'][0]['items'] if i['type']=='agentMessage')
ck('Actual completed acknowledgement45',ack['id']=='efff6dc2-f1df-44b5-b43f-4011c7b8c057' and 'accepted-but-unapplied total is now 45' in ack['text'])
return_status={'availabilityReceipt':info(rp),'actualFinal':info(np),'actualAssistant':available['actualAssistant'],'reportedArchive':deepcopy(available['reportedArchive']),'reportedModel':deepcopy(available['reportedModel']),'archiveDownloaded':False,'localVerificationComplete':False,'semanticAcceptanceClaimed':False,'implementationApplied':False,'status':'Complete reply received; full original archive download remains pending after browser attachment failures. This is neither acceptance nor semantic rejection. No regeneration requested.'}
group={'group':'rank9-resonance-fields3','phase':'source-conference-prepared-unsent','identities':ids,'identityCount':3,'candidate':prep['candidate'],'preparation':info(prepfile),'archive':prep['archive'],'adopted':False,'sourceCount':99,'placementCount':3,'questionCount':24,'riskCounts':{'C':3},'currentCaseCount':0,'latestObservedStatus':'Complete Arc Furnace, Resonance Singularity and Supreme Nexus source conference:99 full sources,24 unselected questions,9 applied counterparts,7 full class features,28 scoped interface records and296 preservation checks. Preserve native amplification,absorption/conversion and enhancement/half-cost benefits.'}
phase7='ready-deadline-return-available-download-pending'
for g in q['groups']:
 if g['group']=='rank7-identity-casting5':
  g['previousObservationBefore76']={k:deepcopy(g.get(k)) for k in ['phase','latestObservedStatus']}
  g.update(phase=phase7,latestObservedStatus=return_status['status'],currentReadyDeadlineReturn=deepcopy(return_status))
q['groups'].append(group)
for old,row in zip(q0['rows'],q['rows']):
 if row['id'] in ids:
  row.update(currentGroup=group['group'],currentPhase=group['phase'],semanticAcceptanceClaimed=False,sourceConferencePreparation=info(prepfile),nextAction='Confer on24 source-specific unselected questions with complete native and accepted comparison evidence. Preserve actual50percent allied spell damage,all-magic absorption/conversion,and all-magic enhancement with half Resonance costs. No selection or application yet.')
 elif row['currentGroup']=='rank7-identity-casting5':
  row['previousObservationBefore76']={k:deepcopy(row.get(k)) for k in ['currentPhase','nextAction']}
  row.update(currentPhase=phase7,nextAction='Recover complete original116,652,484-byte Ready-deadline Return03; compare reported hash, independently reconstruct six changes and boundary diagnostic before acceptance. Do not execute downloaded Python or request unnecessary regeneration.',semanticAcceptanceClaimed=False)
 else:ck('Unaffected complete row '+row['id'],row==old)
 ck('Complete source/index/history retained '+row['id'],all(row[k]==old[k] for k in ['completeCurrentSourceAndAccess','currentIndexEntryUnchanged','previousAuthoringMapRowUnchanged']))
q['previousSummaryBefore76']={k:deepcopy(q0[k]) for k in ['limitations','pendingDistribution','preparedOrActualReviewIdentityCount','originalSourceOrReceiptWorkCount']}
q.update(id='REMAINING-WORK-QUEUE-63',recordedAtUtc=datetime.now(timezone.utc).isoformat(),previousQueue=info(oldq),preparedOrActualReviewIdentityCount=312,originalSourceOrReceiptWorkCount=11,pendingDistribution=dict(Counter(x['currentPhase'] for x in q['rows'])),latestSourceConference=info(prepfile),currentRank7ReadyDeadlineReturn=deepcopy(return_status),latestGptStatusSynchronization={'native':info(sp),'actualUserTurn':'85484c42-73a8-49d0-bb3f-5e1da9161a08','actualAssistant':'efff6dc2-f1df-44b5-b43f-4011c7b8c057','acceptedButUnappliedAcknowledged':45,'newReviewRequested':False})
q['sourceBindings'].extend([info(prepfile),prep['candidate'],prep['archive'],prep['check'],info(rp),info(sp)]);q['latestActualReviewEvidence'].extend([info(np),info(sp)])
q['limitations']='Current76: applied525 reviewed/323 pending/249 standalone/173 interfaces;45accepted-unapplied. Rank7 Ready Return03 complete reply received,full116,652,484-byte archive download and local validation pending due browser-control failure; no new acceptance or semantic rejection. GPT actual status15 acknowledges45 and no re-authoring.52groups cover312pending identities;11rank9 remain ungrouped. New resonance-fields3 packet:99complete sources,24unselected questions,296checks. No selected semantics,runtime,balance,cosmology or canonical application. Latest verified GitHub backup through72. Owner implementation reservation retained.'
ck('All323pending accounted',len(q['rows'])==323 and len(q['groups'])==52 and sum(x['currentGroup'] is not None for x in q['rows'])==312 and sum(x['currentGroup'] is None for x in q['rows'])==11)
ck('45accepted remain unapplied',sum(x['currentPhase'] in ['actual-exact-accepted-integration-staged-not-applied','actual-full-conference-accepted-successor-not-applied'] for x in q['rows'])==45)
for a,b in zip(q['groups'][:-1],q0['groups']):
 if a['group']!='rank7-identity-casting5':ck('Prior group fully unchanged '+a['group'],a==b)
ck('Exactly five pending Rank7 return rows',sum(x['currentPhase']==phase7 for x in q['rows'])==5)
ck('Remaining11allrank9',all(min(a['rank'] for a in x['completeCurrentSourceAndAccess']['classAccess'].values())==9 for x in q['rows'] if x['currentGroup'] is None))
ck('Exact distribution',sum(q['pendingDistribution'].values())==323)
for b in cp['navigation']:ck('Previous navigation exact '+b['path'],info(G/b['path'])==b)
navpaths=[G/'START_HERE.md',R/'docs/DEVELOPMENT_DIRECTION.md',G/'REVIEW_MAP.html'];nav={p:p.read_bytes() for p in navpaths};navbackup.mkdir()
for p,b in nav.items():(navbackup/p.name).write_bytes(b)
newq.write_bytes(enc(q));base='docs/audit/2026-10-08/full-game/'
for p,prefix in [(navpaths[0],''),(navpaths[1],'../../../')]:
 raw=nav[p];pos=raw.index(b'\n')+1
 notice=('\n**Current source preparation — 20 October 2026:** [Checkpoint76]('+prefix+base+out.name+') and [Queue63]('+prefix+newq.relative_to(G).as_posix()+') add Arc Furnace, Resonance Singularity and Supreme Nexus:99 complete sources,24 unselected questions,296 preservation checks.52 groups cover312 pending identities;11 remain ungrouped. Rank7 corrected return is available, with full archive download/local verification pending. GPT has acknowledged45 accepted-but-unapplied; applied525/323/249 and173interfaces remain unchanged. Latest verified GitHub backup through72.\n').encode()
 p.write_bytes(raw[:pos]+notice+raw[pos:]);ck('Previous navigation preserved '+p.name,p.read_bytes().replace(notice,b'',1)==raw)
p=navpaths[2];raw=nav[p];pos=raw.index(b'</h1>')+len(b'</h1>')
notice=('<section class="sequence" aria-label="Current resonance field source preparation"><p><strong>Checkpoint76: three Rank9 resonance-field sources prepared.</strong>99 full sources,24 unselected questions,296 checks. Queue63:312 grouped/11 ungrouped pending. Rank7 complete reply received; archive download and validation pending. GPT acknowledges45 accepted-unapplied; no new rules applied. <a href="'+base+out.name+'">Current checkpoint</a></p></section>').encode()
p.write_bytes(raw[:pos]+notice+raw[pos:]);ck('Previous review map preserved',p.read_bytes().replace(notice,b'',1)==raw)
cp['previousGptObservationBefore76']=deepcopy(cp['activeGptReviewAtLastVerifiedObservation'])
cp['activeGptReviewAtLastVerifiedObservation'].update(completedResponseReceived=True,latestNativeObservation=info(np),latestObservedStatus=return_status['status'],latestCompletedAssistant=available['actualAssistant'],latestStatusSynchronization=deepcopy(q['latestGptStatusSynchronization']),activeGenerationVerified=False)
cp.update(id='ACTIVE-AUTHORING-RANK9-RESONANCE-FIELDS-76',recordedAtUtc=datetime.now(timezone.utc).isoformat(),previousCheckpoint=info(previous),currentWorkQueue=info(newq),preparedGroupCount=52,groupedPendingIdentities=312,ungroupedPendingIdentities=11,rank9ResonanceFields3SourceConference=info(prepfile),completedRank7ReadyDeadlineReturn03=deepcopy(return_status),status='Three remaining Rank9 identities prepared with complete sources and24 unselected decisions. Rank7 completed return awaits full archive recovery/local verification. GPT actual status synchronization confirms45 accepted-unapplied.',navigation=[info(p) for p in navpaths],preservedNavigation=[info(navbackup/p.name) for p in navpaths],lastUsageObservation={'usedPercent':34,'remainingPercent':66,'stopAtRemainingPercent':20,'resetsAt':1793110625},previousGoalTurnClassification='Progress:75 accepted six exact Rank8 authored successors with retained qualifications,submitted Rank7 follow-up,preserved Unity directions,and recorded completed Rank7 reply. Current76 prepared three full remaining source identities and completed actual GPT status synchronization; browser failure does not block independent source work.',laterLocalWork='All73–76 artifacts,Rank8 acceptance75,Unity intake,Rank7 available reply,actual GPT status15,resonance-fields3 source packet,Queue63 and checkpoint76 remain local after verified GitHub backup through72.',nextAction='Recover original Rank7 Ready Return03 archive through supported browser when connection works; independently reconstruct and semantically verify before accepting. Continue remaining11 ungrouped rank9 source preparations and full-source GPT conferences. Preserve originals,implementation reservation and20percent usage floor.',queueObservationSupersession='Queue63 preserves every original complete source/index/history row,adds one three-identity source group and updates five Rank7 phases from generation to completed-return/download-pending. Prior reports remain exact history.')
ck('No new acceptance or application',cp['authoredCounts']=={'reviewed':525,'pending':323,'standalone':249,'total':848} and cp['acceptedButUnapplied']==45 and not cp['implementationApplied'])
out.write_bytes(enc(cp));script.write_bytes(Path(__file__).read_bytes())
for p,b in original.items():ck('Protected authority unchanged '+p.relative_to(G).as_posix(),p.read_bytes()==b)
report.write_bytes(enc({'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'checkpoint':info(out),'queue':info(newq),'checks':checks,'checkCount':len(checks),'failures':0,'newRuleAdoptions':0,'runtimeTestsExecuted':0,'sourceInformationDeleted':0,'scope':'Source/history/queue/navigation preservation; no new gameplay semantic acceptance,runtime or cosmology implementation.'}))
print(json.dumps({'checkpoint':info(out),'queue':info(newq),'report':info(report),'checks':len(checks),'failures':0,'remainingUngrouped':11}))
