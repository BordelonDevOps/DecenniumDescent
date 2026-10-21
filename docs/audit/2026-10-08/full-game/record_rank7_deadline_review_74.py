"""Preserve semantic reconciliation, prepared follow-up, and actual pending GPT status."""
from pathlib import Path
from datetime import datetime,timezone
from copy import deepcopy
from collections import Counter
import hashlib,json
G=Path(r'C:\Github\DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game'
W=Path(r'C:\Users\cbord\Documents\ChatGPT\Decennium Descent\audit_work')
def read(p):return json.loads(p.read_bytes())
def enc(x):return (json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode()
def info(p):
 b=p.read_bytes();return {'path':p.relative_to(G).as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
old=A/'ACTIVE_AUTHORING_CHECKPOINT_GITHUB_RANK7_CORRECTIONS_73.json'
out=A/'ACTIVE_AUTHORING_CHECKPOINT_RANK7_DEADLINE_SEMANTICS_74.json'
oldq=R/'data/director/spell_review/remaining_work_queue_60.json';newq=oldq.with_name('remaining_work_queue_61.json')
checkpath=A/'ACTIVE_AUTHORING_CHECKPOINT_RANK7_DEADLINE_SEMANTICS_74_CHECK.json'
navbackup=A/'navigation-before-rank7-deadline-semantics-74';nativepath=A/'GPT_PART5_RECHECK_74_NATIVE.json';script=A/Path(__file__).name
assert not any(p.exists() for p in [out,newq,checkpath,navbackup,nativepath,script])
checks=[]
def ck(name,value):checks.append({'check':name,'passed':bool(value)});assert value,name
cp=read(old);q0=read(oldq);q=deepcopy(q0)
ck('Exact checkpoint73',info(old)['sha256']=='837c337dc197d5018521ce0e9b9c690e1928c187925db7daccd0fe7cc390f89e')
ck('Exact queue60',info(oldq)==cp['currentWorkQueue'])
protected=[old,oldq,R/'data/public/spell_playtests/catalog.json',R/'data/playtest/game_development_coverage.json']
for key in ['currentAuthoredIndex','currentAcceptedInterfaceRegistry','decisionLedger']:
 b=cp[key];ck('Authority '+key,info(G/b['path'])==b);protected.append(G/b['path'])
for b in cp['canonicalHelperBaselinesUnchanged']:
 ck('Canonical helper '+b['path'],info(G/b['path'])==b);protected.append(G/b['path'])
original={p:info(p) for p in protected}
rp=A/'RANK7_IDENTITY_CASTING5_PART5_CORRECTION_RETURN_02_SEMANTIC_RECONCILIATION_74.json';review=read(rp)
pp=A/'RANK7_IDENTITY_CASTING5_READY_DEADLINE_CORRECTION_02_PREPARATION.json';prep=read(pp)
ck('554 diagnostics with one bounded state defect',review['diagnosticCheckCount']==554 and review['diagnosticFailures']==review['findingsCount']==1)
ck('All three prior findings reconciled',len(review['priorFindingDispositions'])==3 and all(x['status'].startswith('RECONCILED') for x in review['priorFindingDispositions']))
ck('Exactly six stale state fields',len(review['findings'][0]['evidence']['locations'])==6 and all(x['actual']==62 and x['expected']==61 for x in review['findings'][0]['evidence']['locations']))
ck('Nine overstrict diagnostics transparently withdrawn',len(review['diagnosticCorrection']['withdrawnChecks'])==9)
ck('Prepared is not sent or accepted',not prep['sent'] and not prep['implementationApplied'] and prep['newAcceptedIdentities']==0 and prep['allArchiveBytesReopenedAndCompared'])
for key in ['archive','request','semanticReview','originalReturn','manifest']:ck('Prepared complete artifact '+key,info(G/prep[key]['path'])==prep[key])
native=read(W/nativepath.name);turn=native['turns'][0]
ck('Actual follow-up13 still latest user',turn['id']=='04a9a52b-a43d-4ee5-b0a8-c961aeea3da6')
ck('No completed assistant return in current native observation',not any(x['type']=='agentMessage' for x in turn['items']))
nativepath.write_bytes((W/nativepath.name).read_bytes())
semantic={'report':info(rp),'originalDiagnosticReport':info(A/'RANK7_IDENTITY_CASTING5_PART5_CORRECTION_RETURN_02_SEMANTIC_REVIEW_74.json'),
 'verdict':review['verdict'],'checks':554,'failures':1,'reconciledOriginalFindingGroups':3,'remainingFinding':'RIC5-LOCAL74-01','remainingLocations':6,
 'newAcceptedIdentities':0,'implementationApplied':False,'nextPreparedCorrection':{'preparation':info(pp),'archive':prep['archive'],'request':prep['request'],'sent':False}}
phase='ready-deadline-correction-prepared-not-sent'
status='Three original correction groups independently reconciled.554 diagnostics:553 pass,one Ready deadline mismatch across six current states. Complete follow-up14 prepared,unsent while GPT completes Rank8 history13.'
for group in q['groups']:
 if group['group']=='rank7-identity-casting5':
  group['previousObservationBefore74']={'phase':group['phase'],'latestObservedStatus':group['latestObservedStatus']}
  group.update(phase=phase,latestObservedStatus=status,correctionReturn02IndependentSemanticReview=deepcopy(semantic))
for before,row in zip(q0['rows'],q['rows']):
 if row['currentGroup']=='rank7-identity-casting5':
  row['previousObservationBefore74']={k:deepcopy(row.get(k)) for k in ['currentPhase','nextAction','semanticAcceptanceClaimed']}
  row.update(currentPhase=phase,nextAction=status,semanticAcceptanceClaimed=False)
 else:ck('Unchanged complete pending row '+row['id'],row==before)
 ck('Original complete source/index/history retained '+row['id'],all(row[k]==before[k] for k in ['completeCurrentSourceAndAccess','currentIndexEntryUnchanged','previousAuthoringMapRowUnchanged']))
q['previousSummaryBefore74']={k:deepcopy(q0[k]) for k in ['limitations','pendingDistribution']}
q.update(id='REMAINING-WORK-QUEUE-61',recordedAtUtc=datetime.now(timezone.utc).isoformat(),previousQueue=info(oldq),pendingDistribution=dict(Counter(x['currentPhase'] for x in q['rows'])),currentRank7CorrectionSemanticReview=deepcopy(semantic))
q['sourceBindings'].extend([info(rp),info(pp),prep['archive'],info(nativepath)])
q['latestActualReviewEvidence'].append(info(nativepath))
q['limitations']='Current74: Rank7 three original corrections independently reconciled; one remaining Ready deadline62 versus actual61 defect.554 applicable diagnostics,553 passes. Follow-up14 fully prepared but NOT SENT. GPT still completing Rank8 history13; no final return yet. Applied525/323/249,173interfaces,39accepted-unapplied unchanged.51groups309grouped14ungrouped. No runtime,gameplay,balance,cosmology or canonical adoption. Owner reserves implementation.'
ck('Exact queue population retained',len(q['rows'])==323 and len(q['groups'])==51 and q['preparedOrActualReviewIdentityCount']==309 and q['originalSourceOrReceiptWorkCount']==14)
ck('Accepted count unchanged',sum(x['currentPhase'] in ['actual-exact-accepted-integration-staged-not-applied','actual-full-conference-accepted-successor-not-applied'] for x in q['rows'])==39)
ck('Five Rank7 pending phases updated',sum(x['currentPhase']==phase for x in q['rows'])==5)
for b in cp['navigation']:ck('Prior navigation exact '+b['path'],info(G/b['path'])==b)
navpaths=[G/'START_HERE.md',R/'docs/DEVELOPMENT_DIRECTION.md',G/'REVIEW_MAP.html'];nav={p:p.read_bytes() for p in navpaths};navbackup.mkdir()
for p,b in nav.items():(navbackup/p.name).write_bytes(b)
newq.write_bytes(enc(q));base='docs/audit/2026-10-08/full-game/'
for p,prefix in [(navpaths[0],''),(navpaths[1],'../../../')]:
 raw=nav[p];pos=raw.index(b'\n')+1
 notice=('\n**Current semantic review — 20 October2026:** [Checkpoint74]('+prefix+base+out.name+') records reconciliation of all three original Rank7 correction groups.554 local diagnostics leave one stale Ready deadline in six states; [follow-up14]('+prefix+base+pp.name+') is prepared and UNSENT while GPT completes Rank8 history13. [Queue61]('+prefix+newq.relative_to(G).as_posix()+') retains309 grouped/14 ungrouped pending. Applied525/323/249,173interfaces and39accepted-unapplied unchanged. Latest verified GitHub backup remains through72.\n').encode()
 p.write_bytes(raw[:pos]+notice+raw[pos:]);ck('Original navigation preserved '+p.name,p.read_bytes().replace(notice,b'',1)==raw)
p=navpaths[2];raw=nav[p];pos=raw.index(b'</h1>')+len(b'</h1>')
notice=('<section class="sequence" aria-label="Current Rank7 semantic review"><p><strong>Checkpoint74: three Rank7 corrections reconciled.</strong>554 diagnostics leave one Ready deadline mismatch in six states. Complete follow-up14 prepared, not sent; GPT still completing Rank8 history13. No new acceptance or implementation. <a href="'+base+out.name+'">Current checkpoint</a></p></section>').encode()
p.write_bytes(raw[:pos]+notice+raw[pos:]);ck('Original review map preserved',p.read_bytes().replace(notice,b'',1)==raw)
cp['previousGptObservationBefore74']=deepcopy(cp['activeGptReviewAtLastVerifiedObservation'])
cp['activeGptReviewAtLastVerifiedObservation'].update(latestNativeObservation=info(nativepath),completedResponseReceived=False,latestObservedStatus='Actual conference13 remains latest; native observation contains no final assistant and browser still shows Stop during artifact generation. Do not interrupt.')
cp.update(id='ACTIVE-AUTHORING-RANK7-DEADLINE-SEMANTICS-74',recordedAtUtc=datetime.now(timezone.utc).isoformat(),previousCheckpoint=info(old),currentWorkQueue=info(newq),
 rank7CorrectionIndependentSemanticReview=semantic,status=status,navigation=[info(p) for p in navpaths],preservedNavigation=[info(navbackup/p.name) for p in navpaths],
 lastUsageObservation={'usedPercent':30,'remainingPercent':70,'stopAtRemainingPercent':20},
 previousGoalTurnClassification='Progress:73 preserved Rank7 Return02 with1057 checks and actually submitted Rank8 history13. Current74 reconciles original Rank7 corrections, diagnoses six remaining stale deadline fields and prepares complete follow-up14.',
 laterLocalWork='Full Rank7 Return02,intake73,actual Rank8 dispatch13,semantic review74,full prepared deadline correction14,Queue61 and this checkpoint remain local after verified GitHub backup through72.',
 nextAction='Receive and preserve complete Rank8 history Return03 without interruption; then submit prepared Rank7 deadline follow-up14 with full63,264,719-byte packet. Independently reconstruct/review Rank8 successor. Continue remaining14 ungrouped rank9 source preparations; retain implementation reservation and20percent credit floor.',
 queueObservationSupersession='Queue61 preserves complete source/index/history and prior observations; updates only five Rank7 phases and carries actual pending Rank8 conference13.')
ck('No acceptance or implementation increase',cp['authoredCounts']=={'reviewed':525,'pending':323,'standalone':249,'total':848} and cp['acceptedButUnapplied']==39 and not cp['implementationApplied'])
out.write_bytes(enc(cp));script.write_bytes(Path(__file__).read_bytes())
for p,b in original.items():ck('Protected authority unchanged '+p.relative_to(G).as_posix(),info(p)==b)
checkpath.write_bytes(enc({'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'checkpoint':info(out),'queue':info(newq),'checks':checks,'checkCount':len(checks),'failures':0,'newRuleAdoptions':0,'runtimeTestsExecuted':0,'sourceInformationDeleted':0,'scope':'Review/status/source preservation checks, not engine or balance approval.'}))
print(json.dumps({'checkpoint':info(out),'queue':info(newq),'report':info(checkpath),'checks':len(checks),'failures':0}))
