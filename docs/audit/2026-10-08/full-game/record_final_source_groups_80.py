from pathlib import Path
from copy import deepcopy
from datetime import datetime,timezone
from collections import Counter
import json,hashlib
G=Path(r'C:\Github\DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game'
oldcp=A/'ACTIVE_AUTHORING_CHECKPOINT_RANK7_RECOVERY_ACCEPTED_79.json';oldq=R/'data/director/spell_review/remaining_work_queue_66.json';newq=oldq.with_name('remaining_work_queue_67.json');out=A/'ACTIVE_AUTHORING_CHECKPOINT_ALL_PENDING_GROUPED_80.json';report=A/'ACTIVE_AUTHORING_CHECKPOINT_ALL_PENDING_GROUPED_80_CHECK.json';backup=A/'navigation-before-all-pending-grouped-80';dispatch=A/'RANK9_RESONANCE_FIELDS3_ACTUAL_DISPATCH_80.json'
for p in [newq,out,report,backup]:assert not p.exists(),str(p)
def enc(v):return (json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode()
def j(p):return json.loads(p.read_bytes())
def info(p):
 b=p.read_bytes();return {'path':p.relative_to(G).as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
checks=[]
def ck(s,b):
 checks.append({'check':s,'passed':bool(b)})
 if not b:raise AssertionError(s)
cp=j(oldcp);q0=j(oldq);q=deepcopy(q0);native=A/'GPT_PART5_RANK9_RESONANCE_FIELDS3_DISPATCH_NATIVE_80.json';nv=j(native);prepfile=A/'RANK9_RESONANCE_FIELDS3_DISPATCH_PREPARATION_80.json';dp=j(prepfile);browser=A/'GPT_PART5_RANK9_RESONANCE_FIELDS3_LIVE_LATEST_80.txt'
ck('Correct previous checkpoint79',info(oldcp)['sha256']=='ad8c04966e578038887c04633f669b6c31bec344451c47b180a5820b267c7451');ck('Exact queue66',info(oldq)==cp['currentWorkQueue']);ck('50accepted still unapplied',cp['acceptedButUnapplied']==q['acceptedButUnappliedTotalCurrent']==50 and not cp['implementationApplied'])
ck('Actual native user dispatch',nv['turns'][0]['id']=='fcee2fb1-a2d9-4ee5-b2dc-9c9fb75f9194');ck('Same actual live generation','button "Stop"' in browser.read_text(encoding='utf-8') and 'Working for 11m 3s' in browser.read_text(encoding='utf-8'))
attachmentEvidence=[]
for b in [dp['primary'],dp['supplement']]:
 p=G/b['path'];ck('Exact dispatched source '+p.name,info(p)==b);a=next(x for x in nv['attachments'] if x['name']==p.name);raw=Path(a['path']).read_bytes();ck('Actual uploaded complete bytes '+p.name,raw==p.read_bytes());attachmentEvidence.append({'name':p.name,'localSource':b,'nativeAttachmentPath':a['path'],'byteComparisonPassed':True})
de={'id':'RANK9-RESONANCE-FIELDS3-ACTUAL-DISPATCH-80','recordedAtUtc':datetime.now(timezone.utc).isoformat(),'threadId':'6ad4a867-f330-83e9-829e-bf2bb41a6c09','threadTitle':'Calibration Review Part 5','actualUserTurn':'fcee2fb1-a2d9-4ee5-b2dc-9c9fb75f9194','request':dp['request'],'preparation':info(prepfile),'native':info(native),'attachments':attachmentEvidence,'latestLiveBrowserObservation':info(browser),'status':'Actual source conference submitted with both exact archives; live generation verified. Final artifacts and independent review pending.','acceptedButUnapplied':50,'sourceInformationDeleted':0,'implementationApplied':False}
if dispatch.exists():
 saved=j(dispatch);ck('Preserve already recorded exact dispatch after stopped preflight',{k:v for k,v in saved.items() if k!='recordedAtUtc'}=={k:v for k,v in de.items() if k!='recordedAtUtc'});de=saved
else:dispatch.write_bytes(enc(de))
newgroups=[]
for groupid,stem,counts in [('rank9-projection-confinement2','RANK9_PROJECTION_CONFINEMENT_2_SOURCE_CONFERENCE_01',(135,462,6,50)),('rank9-miracle-reality2','RANK9_MIRACLE_REALITY_2_SOURCE_CONFERENCE_01',(153,556,3,45))]:
 pf=A/(stem+'_PREPARATION.json');p=j(pf);candidate=j(G/p['candidate']['path']);check=j(G/p['check']['path']);ids=[x['spellId'] for x in candidate['records']]
 ck(groupid+' exact sources/checks/placements/interfaces',p['sourceCount']==counts[0] and check['checkCount']==counts[1] and p['placementCount']==counts[2] and p['interfaceCount']==counts[3] and check['failures']==0)
 ck(groupid+' 24unselected questions',len(candidate['questions'])==24 and all(not x['decisionSelected'] for x in candidate['questions']))
 for key in ['candidate','archive','check','manifest','request']:ck(groupid+' exact prepared '+key,info(G/p[key]['path'])==p[key])
 group={'group':groupid,'phase':'source-conference-prepared-unsent','identities':ids,'identityCount':2,'candidate':p['candidate'],'preparation':info(pf),'archive':p['archive'],'adopted':False,'sourceCount':counts[0],'placementCount':counts[2],'questionCount':24,'riskCounts':{'C':2},'currentCaseCount':0,'latestObservedStatus':'Full native placements/access, history and current scoped comparisons prepared with24unselected choices; no selected operation, semantic acceptance or cosmology promotion.'}
 newgroups.append(group);q['groups'].append(group);q['sourceBindings'].extend([info(pf),p['candidate'],p['archive'],p['check']])
resonance=next(g for g in q['groups'] if set(g['identities'])=={'arc-furnace','resonance-singularity','resonance-nexus-supreme'})
resonance['previousObservationBefore80']={k:deepcopy(resonance.get(k)) for k in ['phase','latestObservedStatus']};resonance.update(phase='actual-source-conference-review-in-progress',actualSourceConferenceDispatch=info(dispatch),latestObservedStatus=de['status'])
newids={sid:group for group in newgroups for sid in group['identities']}
for before,row in zip(q0['rows'],q['rows']):
 if row['id'] in newids:
  group=newids[row['id']];ck('Previously ungrouped '+row['id'],before['currentGroup'] is None);row.update(currentGroup=group['group'],currentPhase=group['phase'],semanticAcceptanceClaimed=False,sourceConferencePreparation=group['preparation'],nextAction='Submit the complete source conference after the current review. Preserve every native benefit, actual access and original cosmology evidence; select missing mechanics explicitly with GPT. No canonical application or imported rules.')
 elif row['id'] in resonance['identities']:
  row['previousObservationBefore80']={k:deepcopy(row[k]) for k in ['currentPhase','nextAction']};row.update(currentPhase='actual-source-conference-review-in-progress',actualSourceConferenceDispatch=info(dispatch),nextAction='Receive and preserve the actual three-spell GPT return; independently verify full source bindings, selected effects, state/price/conversion/stacking examples and reversible artifact values before acceptance.')
 else:ck('Unaffected complete row '+row['id'],row==before)
 ck('Full original source/access/index/history '+row['id'],all(row[k]==before[k] for k in ['completeCurrentSourceAndAccess','currentIndexEntryUnchanged','previousAuthoringMapRowUnchanged']))
ck('All323pending identities grouped exactly once',len(q['rows'])==323 and len(q['groups'])==56 and all(x['currentGroup'] is not None for x in q['rows']) and len([sid for g in q['groups'] for sid in g['identities']])==len(set(sid for g in q['groups'] for sid in g['identities']))==323)
ck('50accepted-unapplied unchanged',sum(x['currentPhase'] in ['actual-exact-accepted-integration-staged-not-applied','actual-full-conference-accepted-successor-not-applied'] for x in q['rows'])==50)
for a,b in zip(q['groups'],q0['groups']):
 if a['group']!=resonance['group']:ck('Prior entire group preserved '+a['group'],a==b)
q['previousSummaryBefore80']={k:deepcopy(q0[k]) for k in ['limitations','pendingDistribution','preparedOrActualReviewIdentityCount','originalSourceOrReceiptWorkCount']}
q.update(id='REMAINING-WORK-QUEUE-67',recordedAtUtc=datetime.now(timezone.utc).isoformat(),previousQueue=info(oldq),preparedOrActualReviewIdentityCount=323,originalSourceOrReceiptWorkCount=0,pendingDistribution=dict(Counter(x['currentPhase'] for x in q['rows'])),currentResonanceFields3ActualDispatch=info(dispatch),latestGptStatusSynchronization=info(A/'GPT_PART5_STATUS_SYNC_16_COMPLETED_NATIVE.json'),limitations='Current80: all323pending identities now have full source/review groups,56groups and0ungrouped. This is source preparation/coverage, not completion of their semantic reviews.50accepted-unapplied;applied525/323/249/173unchanged. Actual ResonanceFields3 conference is generating with both exact source/current-context archives. Final four source identities prepared in two cohorts with48unselected choices. All holds and owner implementation reservation remain. Latest verified GitHub backup through72.')
q['sourceBindings'].extend([info(dispatch),info(native),info(browser),info(A/'GPT_PART5_STATUS_SYNC_16_COMPLETED_NATIVE.json')]);q['latestActualReviewEvidence'].extend([info(native),info(browser)]);newq.write_bytes(enc(q))
protected=[cp['currentAuthoredIndex'],cp['currentAcceptedInterfaceRegistry'],*cp['canonicalHelperBaselinesUnchanged']];protected.append(info(R/'data/public/spell_playtests/catalog.json'))
for x in protected:ck('Protected predecessor '+x['path'],info(G/x['path'])==x)
for x in cp['navigation']:ck('Exact prior navigation '+x['path'],info(G/x['path'])==x)
navs=[G/'START_HERE.md',R/'docs/DEVELOPMENT_DIRECTION.md',G/'REVIEW_MAP.html'];nav={p:p.read_bytes() for p in navs};backup.mkdir()
for p,b in nav.items():(backup/p.name).write_bytes(b)
base='docs/audit/2026-10-08/full-game/'
for p,prefix in [(navs[0],''),(navs[1],'../../../')]:
 raw=nav[p];pos=raw.index(b'\n')+1;notice=('\n**Current source checkpoint — 20 October 2026:** [Checkpoint 80]('+prefix+base+out.name+') and [Queue 67]('+prefix+newq.relative_to(G).as_posix()+') cover every pending spell: **323 grouped, 0 ungrouped, 56 review groups**. Astral Projection, Imprisonment, Greater Divine Intervention and Wish now have complete source packets with48unselected choices. GPT is reviewing Resonance Fields3.50accepted-unapplied;applied525/323/249 and173interfaces unchanged. Source coverage is not review completion; implementation remains reserved.\n').encode();p.write_bytes(raw[:pos]+notice+raw[pos:]);ck('Prior navigation retained '+p.name,p.read_bytes().replace(notice,b'',1)==raw)
p=navs[2];raw=nav[p];pos=raw.index(b'</h1>')+5;notice=('<section class="sequence" aria-label="Every pending spell grouped"><p><strong>Checkpoint 80: all323pending spells have source/review groups.</strong>56groups,0ungrouped; reviews still pending. GPT is reviewing Resonance Fields3.50accepted-unapplied;canonical baseline unchanged. <a href="'+base+out.name+'">Current checkpoint</a></p></section>').encode();p.write_bytes(raw[:pos]+notice+raw[pos:]);ck('Prior review map retained',p.read_bytes().replace(notice,b'',1)==raw)
cp['previousGptObservationBefore80']=deepcopy(cp['activeGptReviewAtLastVerifiedObservation']);cp['activeGptReviewAtLastVerifiedObservation']={'threadId':de['threadId'],'threadTitle':de['threadTitle'],'group':resonance['group'],'actualUserTurn':de['actualUserTurn'],'dispatch':info(dispatch),'browserObservation':info(browser),'activeGenerationVerified':True,'completedResponseReceived':False,'latestObservedStatus':de['status']}
cp.update(id='ACTIVE-AUTHORING-ALL-PENDING-GROUPED-80',recordedAtUtc=datetime.now(timezone.utc).isoformat(),previousCheckpoint=info(oldcp),currentWorkQueue=info(newq),preparedGroupCount=56,groupedPendingIdentities=323,ungroupedPendingIdentities=0,rank9ProjectionConfinement2SourceConference=newgroups[0]['preparation'],rank9MiracleReality2SourceConference=newgroups[1]['preparation'],currentResonanceFields3ActualDispatch=info(dispatch),latestCompletedGptSynchronization=info(A/'GPT_PART5_STATUS_SYNC_16_COMPLETED_NATIVE.json'),status='All pending spell identities grouped with complete source preparation. Actual GPT Resonance Fields3 review is running; no additional acceptance or implementation.',navigation=[info(p) for p in navs],preservedNavigation=[info(backup/p.name) for p in navs],lastUsageObservation={'usedPercent':38,'remainingPercent':62,'stopAtRemainingPercent':20,'resetsAt':1793110625},previousGoalTurnClassification='Progress:79 downloaded/verified the complete Rank7recovery,accepted five scoped successors and completed GPT status synchronization. Current80 actually dispatched the next3spell conference and prepared the final4ungrouped identities in two complete packets.',laterLocalWork='All73–80 source/review/recovery artifacts and queues/checkpoints remain local after verified GitHub backup through72.',nextAction='Receive/download the same active ResonanceFields3 return and independently review its complete native benefits, selected mechanics, exact reversible artifacts and meaningful full-state interactions. Continue remaining prepared source conferences. Preserve all holds, owner implementation reservation and separate runtime/balance/cosmology/release gates.')
out.write_bytes(enc(cp))
for x in protected:ck('Protected authority unchanged '+x['path'],info(G/x['path'])==x)
(A/Path(__file__).name).write_bytes(Path(__file__).read_bytes());report.write_bytes(enc({'checkpoint':info(out),'queue':info(newq),'actualDispatch':info(dispatch),'checkCount':len(checks),'failures':0,'checks':checks,'newRuleAdoptions':0,'runtimeTestsExecuted':0,'sourceInformationDeleted':0,'scope':'Complete source preparation, actual GPT dispatch and exact queue/navigation preservation; no review completion or runtime proof claimed.'}))
print(json.dumps({'checkpoint':info(out),'queue':info(newq),'report':info(report),'checks':len(checks),'failures':0,'grouped':323,'ungrouped':0,'groups':56}))
