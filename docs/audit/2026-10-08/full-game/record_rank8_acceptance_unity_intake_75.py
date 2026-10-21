"""Checkpoint exact six-spell acceptance, actual Rank7 dispatch, and Unity intake."""
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
old=A/'ACTIVE_AUTHORING_CHECKPOINT_RANK7_DEADLINE_SEMANTICS_74.json'
out=A/'ACTIVE_AUTHORING_CHECKPOINT_RANK8_ACCEPTANCE_UNITY_INTAKE_75.json'
oldq=R/'data/director/spell_review/remaining_work_queue_61.json';newq=oldq.with_name('remaining_work_queue_62.json')
checkpath=out.with_name(out.stem+'_CHECK.json');navbackup=A/'navigation-before-rank8-acceptance-unity-intake-75';script=A/Path(__file__).name
assert not any(p.exists() for p in [out,newq,checkpath,navbackup,script])
checks=[]
def ck(name,value):checks.append({'check':name,'passed':bool(value)});assert value,name
cp=read(old);q0=read(oldq);q=deepcopy(q0)
ck('Exact checkpoint74',info(old)['sha256']=='504e570b9ece51253e67759b388214fb8d2d876f00a0938792f30db14000c8f4')
ck('Exact queue61',info(oldq)==cp['currentWorkQueue'])
protected=[old,oldq,R/'data/public/spell_playtests/catalog.json',R/'data/playtest/game_development_coverage.json']
for key in ['currentAuthoredIndex','currentAcceptedInterfaceRegistry','decisionLedger']:
 b=cp[key];ck('Authority '+key,info(G/b['path'])==b);protected.append(G/b['path'])
for b in cp['canonicalHelperBaselinesUnchanged']:
 ck('Canonical helper '+b['path'],info(G/b['path'])==b);protected.append(G/b['path'])
original={p:info(p) for p in protected}
ap=A/'RANK8_DAMAGE6_PART5_EXACT_AUTHORING_ACCEPTANCE_75.json';accept=read(ap)
ck('Exact six accepted, not applied',accept['identityCount']==6 and accept['resultingAcceptedButUnapplied']==45 and not accept['implementationApplied'] and accept['ownerImplementationReservationRetained'])
for k in ['selectedSuccessor','archive','localSemanticReview','localPreservation','actualGptFinal','priorSemanticReview','holdRegister']:ck('Accepted exact artifact '+k,info(G/accept[k]['path'])==accept[k])
sem=read(G/accept['localSemanticReview']['path']);pre=read(G/accept['localPreservation']['path'])
ck('141 passing delta semantic checks',sem['diagnosticCheckCount']==141 and sem['diagnosticFailures']==0)
ck('1498 passing preservation checks',pre['checkCount']==1498 and pre['failures']==0)
ck('Five prior whole-case holds retained',accept['retainedWholePositiveCaseHolds']==['IN6-09-A','IN6-09-B','EN5-01-A','EN5-01-B','EN6-03-B'])
pp=A/'RANK7_IDENTITY_CASTING5_READY_DEADLINE_CORRECTION_02_PREPARATION.json';prep=read(pp)
np=A/'GPT_PART5_RANK7_READY_DEADLINE_CORRECTION_14_DISPATCH_NATIVE.json';native=read(np)
dp=A/'GPT_PART5_RANK7_READY_DEADLINE_CORRECTION_14_DISPATCH_TEXT.txt'
ck('Actual Rank7 follow-up14',native['turns'][0]['id']=='0a9e0b92-ece2-4815-84d4-3b2baf6f4712')
attachment=next(x for x in native['attachments'] if x['name']=='DD_Rank7_Identity_Casting5_Ready_Deadline_Correction_02.zip')
temp=Path(attachment['path']);bound=G/prep['archive']['path']
ck('Full actual attachment matches prepared archive',temp.read_bytes()==bound.read_bytes() and info(bound)==prep['archive'])
dispatch={'threadId':'6ad4a867-f330-83e9-829e-bf2bb41a6c09','title':'Calibration Review Part 5','userTurn':'0a9e0b92-ece2-4815-84d4-3b2baf6f4712','request':info(dp),'fullPreparedRequest':prep['request'],'archive':prep['archive'],'nativeConfirmation':info(np),'sent':True,'completedResponseReceived':False,'attachmentBytesIndependentlyVerified':True,'actualAttachmentPath':str(temp),'scope':'RIC5-LOCAL74-01: six current Ready deadlines62 corrected to actual next regular own START61. The release at60.9 remains legal. Preserve all earlier corrections and procedures.','latestObservedStatus':'Browser shows Working for13m2s: boundary and retained tests pass; finishing archive/mirror verification. No final yet. Do not interrupt.','screenshotLocalOnly':str(W/'gpt-rank7-deadline-dispatch75.jpg'),'historicalCountInSubmittedMessage':39,'countAfterLaterLocalRank8Acceptance':45}
up=A/'UNITY_DEVELOPMENT_DIRECTIONS_INTAKE_75.json';unity=read(up)
ck('Unity intake preserves owner context without implementation',not unity['implementationApplied'] and not unity['unityProjectCreated'] and unity['ownerImplementationReservationRetained'] and unity['briefSectionsRead']==list(range(1,19)))
for b in unity['artifacts']:ck('Exact Unity evidence '+b['path'],info(G/b['path'])==b)
rank8={'receipt':info(ap),'status':accept['status'],'selectedSuccessor':accept['selectedSuccessor'],'archive':accept['archive'],'localSemanticReview':accept['localSemanticReview'],'localPreservation':accept['localPreservation'],'actualGptFinal':accept['actualGptFinal'],'holdRegister':accept['holdRegister'],'newAcceptedButUnapplied':6,'acceptedButUnappliedTotal':45,'implementationApplied':False,'semanticCheckCount':141,'preservationCheckCount':1498,'failures':0,'scope':accept['scope']}
phase8='actual-full-conference-accepted-successor-not-applied';phase7='ready-deadline-correction-actually-sent'
status8='Exact Rank8 six-spell successor independently accepted with retained qualifications and holds.1498 preservation checks and141 additional semantic checks pass. Six new accepted-unapplied, total45. Canonical implementation remains reserved by owner.'
status7='Complete follow-up14 actually sent with byte-verified63,264,719-byte archive. GPT finishing six Ready-deadline state corrections and boundary diagnostic; no final response yet. No Rank7 acceptance.'
for group in q['groups']:
 if group['group'] in ['rank8-damage6','rank7-identity-casting5']:
  group['previousObservationBefore75']={k:deepcopy(group.get(k)) for k in ['phase','latestObservedStatus','semanticAcceptanceClaimed']}
 if group['group']=='rank8-damage6':
  group.update(phase=phase8,latestObservedStatus=status8,semanticAcceptanceClaimed=True,semanticAcceptanceScope=accept['scope'],selectedSuccessor=accept['selectedSuccessor'],actualFinalAssistant=accept['actualAssistantTurn'],exactAcceptanceReceipt=info(ap),fullReturnArchive=accept['archive'],holdRegister=accept['holdRegister'],localVerification=deepcopy(rank8),adopted=False)
 if group['group']=='rank7-identity-casting5':
  group.update(phase=phase7,latestObservedStatus=status7,actualUserTurn=dispatch['userTurn'],actualDeadlineCorrectionDispatch=deepcopy(dispatch),semanticAcceptanceClaimed=False)
for before,row in zip(q0['rows'],q['rows']):
 if row['currentGroup'] in ['rank8-damage6','rank7-identity-casting5']:
  row['previousObservationBefore75']={k:deepcopy(row.get(k)) for k in ['currentPhase','nextAction','semanticAcceptanceClaimed']}
 if row['currentGroup']=='rank8-damage6':row.update(currentPhase=phase8,nextAction='Await separate owner integration instruction; use exact acceptance75 and preserve all holds. Accepted review is not applied catalog coverage.',semanticAcceptanceClaimed=True,exactAcceptanceReceipt=info(ap))
 elif row['currentGroup']=='rank7-identity-casting5':row.update(currentPhase=phase7,nextAction=status7,semanticAcceptanceClaimed=False)
 else:ck('Unchanged complete pending row '+row['id'],row==before)
 ck('Original complete source/index/history retained '+row['id'],all(row[k]==before[k] for k in ['completeCurrentSourceAndAccess','currentIndexEntryUnchanged','previousAuthoringMapRowUnchanged']))
q['previousSummaryBefore75']={k:deepcopy(q[k]) for k in ['limitations','pendingDistribution','currentRank8CorrectionSemanticReview','currentRank7CorrectionSemanticReview']}
q.update(id='REMAINING-WORK-QUEUE-62',recordedAtUtc=datetime.now(timezone.utc).isoformat(),previousQueue=info(oldq),pendingDistribution=dict(Counter(x['currentPhase'] for x in q['rows'])),currentRank8ExactAcceptance=deepcopy(rank8),currentRank8CorrectionSemanticReview=deepcopy(rank8),currentRank7ReadyDeadlineActualDispatch=deepcopy(dispatch),acceptedButUnappliedTotalCurrent=45)
q['currentRank7CorrectionSemanticReview']['nextPreparedCorrection'].update(sent=True,actualDispatch=deepcopy(dispatch))
q['sourceBindings'].extend([info(ap),accept['archive'],accept['localSemanticReview'],accept['localPreservation'],info(np),info(up)])
q['latestActualReviewEvidence'].extend([accept['actualGptFinal'],info(np)])
q['limitations']='Current75: six Rank8 authored successors accepted after1498 preservation and141 additional semantic checks, with retained conditional inputs/holds; accepted-unapplied45. Complete Rank7 follow-up14 actually sent, GPT finishing return; not accepted. Applied525reviewed/323pending/249standalone of848,173interfaces unchanged.51groups309grouped14ungrouped. Unity brief preserved and owner direction traced; no Unity project verified, no implementation. Owner canonical implementation reservation remains. No runtime, balance, gameplay, cosmology or publication approval.'
ck('Exact queue population retained',len(q['rows'])==323 and len(q['groups'])==51 and q['preparedOrActualReviewIdentityCount']==309 and q['originalSourceOrReceiptWorkCount']==14)
ck('45 accepted-unapplied identities',sum(x['currentPhase'] in ['actual-exact-accepted-integration-staged-not-applied',phase8] for x in q['rows'])==45)
ck('Six Rank8 IDs match exact acceptance',{x['id'] for x in q['rows'] if x['currentGroup']=='rank8-damage6'}==set(accept['identities']))
ck('Five Rank7 pending dispatches',sum(x['currentPhase']==phase7 for x in q['rows'])==5)
ck('Historical staged24 count retained',q['exactAcceptedAwaitingApplication']==q0['exactAcceptedAwaitingApplication']==24)
for b in cp['navigation']:ck('Prior navigation exact '+b['path'],info(G/b['path'])==b)
navpaths=[G/'START_HERE.md',R/'docs/DEVELOPMENT_DIRECTION.md',G/'REVIEW_MAP.html'];nav={p:p.read_bytes() for p in navpaths}
navbackup.mkdir()
for p,b in nav.items():(navbackup/p.name).write_bytes(b)
newq.write_bytes(enc(q));base='docs/audit/2026-10-08/full-game/'
for p,prefix in [(navpaths[0],''),(navpaths[1],'../../../')]:
 raw=nav[p];pos=raw.index(b'\n')+1
 notice=('\n**Current review — 20 October 2026:** [Checkpoint75]('+prefix+base+out.name+') records six Rank8 authored successors accepted but unapplied (45 total), and the actual Rank7 deadline follow-up14. [Queue62]('+prefix+newq.relative_to(G).as_posix()+') retains309 grouped/14 ungrouped pending. [Unity brief intake]('+prefix+base+up.name+') preserves the owner’s SNES-style exploration/tactical/resource-management direction and original GPT artifacts; engine implementation has not begun. Applied525/323/249 and173interfaces unchanged. Latest verified GitHub backup remains through72.\n').encode()
 p.write_bytes(raw[:pos]+notice+raw[pos:]);ck('Original navigation preserved '+p.name,p.read_bytes().replace(notice,b'',1)==raw)
p=navpaths[2];raw=nav[p];pos=raw.index(b'</h1>')+len(b'</h1>')
notice=('<section class="sequence" aria-label="Current acceptance and Unity intake"><p><strong>Checkpoint75: six Rank8 successors accepted;45 total accepted-unapplied.</strong> Rank7 deadline follow-up14 actually sent. Unity brief and owner direction preserved; no engine implementation. Applied coverage unchanged. <a href="'+base+out.name+'">Current checkpoint</a></p></section>').encode()
p.write_bytes(raw[:pos]+notice+raw[pos:]);ck('Original review map preserved',p.read_bytes().replace(notice,b'',1)==raw)
cp['previousGptObservationBefore75']=deepcopy(cp['activeGptReviewAtLastVerifiedObservation'])
cp['previousRank8SemanticObservationBefore75']=deepcopy(cp['rank8CorrectionIndependentSemanticReview'])
cp.update(id='ACTIVE-AUTHORING-RANK8-ACCEPTANCE-UNITY-INTAKE-75',recordedAtUtc=datetime.now(timezone.utc).isoformat(),previousCheckpoint=info(old),currentWorkQueue=info(newq),acceptedButUnapplied=45,
 activeGptReviewAtLastVerifiedObservation=dispatch,rank8CorrectionIndependentSemanticReview=deepcopy(rank8),completedRank8Damage6CastHistoryReturn03=deepcopy(rank8),unityDevelopmentDirectionsIntake=info(up),status=status8+' '+status7,
 navigation=[info(p) for p in navpaths],preservedNavigation=[info(navbackup/p.name) for p in navpaths],lastUsageObservation={'usedPercent':33,'remainingPercent':67,'stopAtRemainingPercent':20,'resetsAt':1793110625},
 previousGoalTurnClassification='Progress:74 reconciled three original Rank7 finding groups and prepared exact deadline follow-up14. Current75 independently accepted six Rank8 successors, actually submitted14, and preserved pertinent Unity directions with owner evidence.',
 laterLocalWork='All work after verified backup through72 remains local: Rank7 Return02, reviews73-74, actual follow-up14; Rank8 Return03, acceptance75; Unity directions intake; Queue62 and checkpoint75.',
 nextAction='Receive and preserve complete Rank7 deadline Return03 without interrupting generation, independently verify exact six-field correction and full boundary diagnostic, then inform GPT of six Rank8 accepted successors and45 total. Continue remaining14 rank9 source preparation. Preserve owner implementation reservation and20percent credit floor.',
 queueObservationSupersession='Queue62 preserves all323 complete source/index/history rows and all51 groups; updates only six Rank8 acceptance and five Rank7 actual-dispatch phases. Historical preparation/dispatch statements remain timestamped evidence.')
cp['rank7CorrectionIndependentSemanticReview']['nextPreparedCorrection'].update(sent=True,actualDispatch=deepcopy(dispatch))
ck('Applied counts unchanged',cp['authoredCounts']=={'reviewed':525,'pending':323,'standalone':249,'total':848} and not cp['implementationApplied'])
ck('Owner implementation reservation retained',cp['ownerImplementationReservationRetained'])
out.write_bytes(enc(cp));script.write_bytes(Path(__file__).read_bytes())
for p,b in original.items():ck('Protected authority unchanged '+p.relative_to(G).as_posix(),info(p)==b)
checkpath.write_bytes(enc({'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'checkpoint':info(out),'queue':info(newq),'checks':checks,'checkCount':len(checks),'failures':0,'newAcceptedButUnappliedIdentities':6,'newRuleAdoptions':0,'runtimeTestsExecuted':0,'sourceInformationDeleted':0,'scope':'Review/status/source-preservation checks. No engine, balance, or publication approval.'}))
print(json.dumps({'checkpoint':info(out),'queue':info(newq),'report':info(checkpath),'checks':len(checks),'failures':0,'acceptedButUnapplied':45}))
