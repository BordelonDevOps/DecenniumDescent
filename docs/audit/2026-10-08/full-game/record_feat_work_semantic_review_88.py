"""One-shot continuity record; preserve originals and canonical baselines."""
from pathlib import Path
from copy import deepcopy
from datetime import datetime, timezone
import json,hashlib
G=Path(r'C:\Github\DecenniumDescent');A=G/'docs/audit/2026-10-08/full-game'
PRE=A/'ACTIVE_AUTHORING_CHECKPOINT_GPT_PERTINENT_INTAKE_87.json'
OUT=A/'ACTIVE_AUTHORING_CHECKPOINT_FEAT_WORK_SEMANTIC_REVIEW_88.json'
CHECK=A/'ACTIVE_AUTHORING_CHECKPOINT_FEAT_WORK_SEMANTIC_REVIEW_88_CHECK.json'
SAVED=A/Path(__file__).name;BACKUP=A/'navigation-before-feat-work-semantic-review-88'
for p in [OUT,CHECK,SAVED,BACKUP]:assert not p.exists(),str(p)
def j(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def enc(x):return (json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode()
def info(p):
 b=p.read_bytes();return {'path':p.relative_to(G).as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
checks=[]
def ck(label,ok):
 checks.append({'check':label,'pass':bool(ok)})
 assert ok,label
prior=j(PRE);cp=deepcopy(prior)
for row in [prior['currentAuthoredIndex'],prior['currentAcceptedInterfaceRegistry'],prior['currentWorkQueue'],*prior['canonicalHelperBaselinesUnchanged']]:
 ck('Canonical unchanged '+row['path'],info(G/row['path'])==row)
reportfile=A/'FEAT335_WORK_COMPOSITIONS_INDEPENDENT_SEMANTIC_REVIEW_88.json';report=j(reportfile)
ck('Independent report449 passes',report['passed']==449 and report['failed']==0 and all(x['pass'] for x in report['checks']))
ck('Exact reviewed return model',report['model']['bytes']==93363 and report['model']['sha256']=='758ab64c8948d1112f16a397da71082256c3d5a7c27442e453b6f737317971d2')
ck('All authored cases read',report['review']['completeCasesRead']==57 and report['review']['completeOriginalAndSuccessorProceduresRead']==6 and report['review']['questionsReadInFull']==3)
ck('Review is unapplied and parent remains pending',not report['canonicalApplied'] and not report['parent335Accepted'] and not report['runtimeExecuted'])
native=j(A/'GPT_PERTINENT_RECHECK_NATIVE_88.json');unity=j(A/'GPT_UNITY_RECHECK_NATIVE_88.json')
ck('Latest Resonance user turn unchanged',native['turns'][0]['id']=='5ee6be18-389e-400a-9f43-739f5ce09243')
ck('Latest Unity user/assistant unchanged',unity['turns'][0]['id']=='41d5797f-d115-4cce-90fd-8ccc835b86cb' and any(i.get('id')=='b0572b7f-e15c-4d11-8353-86853e0329c6' for i in unity['turns'][0]['items']))
dom=(A/'GPT_RESONANCE_IN_PROGRESS_88.txt').read_text(encoding='utf-8')
ck('Authoritative browser generation active at observation','button "Stop"' in dom)
cp['id']='ACTIVE-AUTHORING-FEAT-WORK-SEMANTIC-REVIEW-88';cp['recordedAtUtc']=datetime.now(timezone.utc).isoformat()
cp['previousCheckpoint']=info(PRE)
cp['status']='Independent full FT84 semantic review complete: three scoped authored dispositions and six successor procedures accepted for later integration,449 checks passed; no canonical change or parent335 acceptance. GPT Resonance receipt follow-through remains generating. Latest notebook and Unity direction freshly checked and preserved.'
entry=cp['completedFeatTimeInterfacesReturn01']
entry['fullLocalSemanticReviewCompleted']=True
entry['exactAuthorshipAccepted']=True
entry['acceptanceScope']='Only the exact three FT84 dispositions and six reviewed operative successors in the received MODEL; all seven holds retained, including unseen mirrors and actual content prerequisites. Parent335 and all canonical selection flags remain unapproved.'
entry['independentSemanticReview']=info(reportfile)
entry['independentSemanticChecks']=449;entry['independentSemanticFailures']=0
entry['canonicalApplied']=False;entry['parent335Accepted']=False
entry['sevenHolds']=report['holds']['holds']
entry['independentWholePositiveCaseHolds']=report['holds']['independentWholePositiveCaseHolds']
entry['pendingAcknowledgment']=info(A/'CODEX_FT84_ACCEPTANCE_FOLLOWUP_88.txt')
entry['acknowledgmentActuallySent']=False
cp['pertinentNotebookRecheck88']={'part5Native':info(A/'GPT_PERTINENT_RECHECK_NATIVE_88.json'),'unityNative':info(A/'GPT_UNITY_RECHECK_NATIVE_88.json'),'newOwnerDecisionIdentified':False,'unityBriefAlreadyPreserved':prior['pertinentNotebookRecheck87']['unityBrief'],'continuity':'No new combat cadence selected. Existing owner direction and full Unity development brief remain preserved. Freshly completed independent feat authored review is separate from canonical/Unity implementation.'}
cp['activeGptReviewAtLastVerifiedObservation']=deepcopy(prior['activeGptReviewAtLastVerifiedObservation'])
cp['activeGptReviewAtLastVerifiedObservation']['browserObservation']=info(A/'GPT_RESONANCE_IN_PROGRESS_88.txt')
cp['activeGptReviewAtLastVerifiedObservation']['latestObservedStatus']='Browser Stop remains active; preliminary visible receipt design is not a final return. Do not interrupt or treat provisional generated code as accepted.'
cp['activeGptReviewAtLastVerifiedObservation']['completedResponseReceived']=False
cp['activeGptReviewAtLastVerifiedObservation']['activeGenerationVerified']=True
cp['nextAction']='Receive completed Resonance durable Feedback receipt return, preserve exact files, independently verify full affected mirrors and replay/round semantics before accepting the three spells. Send prepared FT84 acceptance acknowledgment only after active generation finishes. Meanwhile continue remaining335 healing/reserve/world compositions; Bestiary V3+EX58 packet remains prepared and unsent. Canonical implementation remains owner-reserved.'
cp['lastUsageObservation']={'usedPercent':49,'remainingPercent':51,'resetsAt':1793110625,'stopAtRemainingPercent':20,'source':'Fresh get_usage_limits during88'}
cp['laterLocalWork']='Checkpoints73–88 remain local after last separately verified GitHub backup through72; no push in88.'
nav=[G/'START_HERE.md',G/'DescentReviewChanges/ReviewBible/docs/DEVELOPMENT_DIRECTION.md',G/'REVIEW_MAP.html']
old={p:p.read_bytes() for p in nav};prepared={}
for p in nav:
 if p.suffix=='.html':
  pos=old[p].find(b'>',old[p].find(b'<body'))+1
  notice=('<aside><p><strong>Checkpoint88:</strong> Three scoped feat work rulings accepted as authored proposals after449 independent checks across57 cases. Parent335 remains pending; canonical files unchanged. GPT Resonance follow-through still in progress. <a href="docs/audit/2026-10-08/full-game/'+OUT.name+'">Current record</a>.</p></aside>\n').encode()
 else:
  rel='docs/audit/2026-10-08/full-game/' if p.name=='START_HERE.md' else '../../../docs/audit/2026-10-08/full-game/'
  pos=old[p].find(b'\n')+1
  notice=('\n**Current checkpoint — 20 October 2026:** [Checkpoint88]('+rel+OUT.name+') records accepted scoped feat work authorship:3 dispositions,6 successors,57 cases and449 passing independent checks. Parent335 remains pending; canonical files unchanged. GPT Resonance receipt review remains active. Applied525/323/249,173 interfaces and50 accepted-unapplied spell identities remain unchanged.\n').encode()
 ck('Valid navigation insertion '+p.name,pos>0)
 new=old[p][:pos]+notice+old[p][pos:]
 ck('Prior navigation bytes retained '+p.name,new[:pos]+new[pos+len(notice):]==old[p])
 prepared[p]=new
ck('All prior checkpoint fields retained',set(prior).issubset(cp))
ck('Applied counts unchanged',cp['authoredCounts']==prior['authoredCounts'] and cp['acceptedButUnapplied']==50 and not cp['implementationApplied'])
BACKUP.mkdir();preserved=[]
for p in nav:
 dst=BACKUP/p.name
 with dst.open('xb') as f:f.write(old[p])
 preserved.append(info(dst));p.write_bytes(prepared[p])
cp['navigation']=[info(p) for p in nav];cp['preservedNavigation']=preserved
with SAVED.open('xb') as f:f.write(Path(__file__).read_bytes())
with OUT.open('xb') as f:f.write(enc(cp))
result={'id':'CHECKPOINT88-VALIDATION','checkpoint':info(OUT),'checks':checks,'passed':len(checks),'failed':0,'script':info(SAVED)}
with CHECK.open('xb') as f:f.write(enc(result))
print(json.dumps({'checkpoint':info(OUT),'check':info(CHECK),'passed':len(checks),'failed':0},indent=2))
