"""One-shot continuity record for the owner's requested GPT check."""
from pathlib import Path
from copy import deepcopy
from datetime import datetime,timezone
import hashlib,json
G=Path(r'C:\Github\DecenniumDescent');A=G/'docs/audit/2026-10-08/full-game'
PRE=A/'ACTIVE_AUTHORING_CHECKPOINT_RESONANCE_SEMANTIC_REVIEW_86.json'
OUT=A/'ACTIVE_AUTHORING_CHECKPOINT_GPT_PERTINENT_INTAKE_87.json'
CHECK=A/'ACTIVE_AUTHORING_CHECKPOINT_GPT_PERTINENT_INTAKE_87_CHECK.json'
SAVED=A/Path(__file__).name;BACKUP=A/'navigation-before-gpt-pertinent-intake-87'
for p in [OUT,CHECK,SAVED,BACKUP]:assert not p.exists(),str(p)
def j(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def enc(d):return (json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode()
def info(p):
 b=p.read_bytes();return {'path':p.relative_to(G).as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
checks=[]
def ck(label,v):
 checks.append({'check':label,'pass':bool(v)})
 assert v,label
prior=j(PRE);cp=deepcopy(prior)
for row in [prior['currentAuthoredIndex'],prior['currentAcceptedInterfaceRegistry'],prior['currentWorkQueue'],*prior['canonicalHelperBaselinesUnchanged']]:
 ck('Canonical baseline unchanged '+row['path'],info(G/row['path'])==row)
intake=j(A/'FEAT335_WORK_COMPOSITIONS_PART5_RETURN01_INTAKE_87.json')
ck('Intake completed with286 passes',intake['passed']==286 and intake['failed']==0 and all(x['pass'] for x in intake['checks']))
native=j(A/'GPT_RESONANCE_RECEIPT_SENT_NATIVE_87.json')
turn=native['turns'][0]
ck('Exact actual dispatch turn',turn['id']=='5ee6be18-389e-400a-9f43-739f5ce09243')
message='\n'.join(c['text'] for i in turn['items'] if i['type']=='userMessage' for c in i['content'] if c['type']=='text')
draft=(A/'GPT_RESONANCE_RECEIPT_REQUEST_87_VERIFIED.txt').read_text(encoding='utf-8')
ck('Complete sent text matches verified draft',message.split('\n\n[User attached ')[0].strip()==draft.strip())
ck('One actual attachment annotation','[User attached 1 file;' in message)
packet=info(A/'DD_Resonance_Fields3_Receipt_Followthrough_86.zip')
ck('Prepared packet intact',packet['bytes']==937873 and packet['sha256']=='3477ed0f3143da0e4e8c8c40bbc31dfbbbcc18760416e8a5f9ee3521f5e6ae09')
brief=info(A/'unity-development-directions-75/Decennium_Descent_Unity_Codex_Directions.md')
ck('Unity brief matches existing intake',brief['bytes']==35493 and brief['sha256']=='cfca586c7351f7ac913523a3b9cde076bc3e92f4301404f1f78b608db6145369')
cp['id']='ACTIVE-AUTHORING-GPT-PERTINENT-INTAKE-87'
cp['recordedAtUtc']=datetime.now(timezone.utc).isoformat()
cp['status']='Owner-requested GPT check complete. Unity direction and complete brief confirmed preserved. GPT completed FT84 questions; all34 return files preserved and51 JSON operations reconstructed/reversed with286 passing local checks. Authored semantic review remains pending. Resonance Feedback history follow-through actually sent and GPT responding.'
cp['previousCheckpoint']=info(PRE)
cp['previousGptObservationBefore87']=prior['activeGptReviewAtLastVerifiedObservation']
cp['pertinentNotebookRecheck87']={
 'checkedThreads':[{'id':'6ad4a867-f330-83e9-829e-bf2bb41a6c09','title':'Calibration Review Part 5'},{'id':'6ad64114-2364-83e9-8764-bc55988b0479','title':'Unity Development Setup'}],
 'existingOwnerDirection':'SNES-style Unity CRPG; direct-control exploration, deep tactical combat, companion-driven crafting/research/resource management; ongoing AI engineering oversight. Existing ledger remains controlling; assistant recommendations do not establish a new combat cadence.',
 'ownerDirectionLedger':info(A/'PERTINENT_GPT_DECISIONS_2026_10_20_02.json'),
 'unityBrief':brief,'latestUnityAssistant':'b0572b7f-e15c-4d11-8353-86853e0329c6',
 'newOwnerDecisionIdentifiedInFreshRead':False,
 'newCompletedReview':'FT84-Q01/Q02/Q03 return received this turn; proposed and unapplied.'}
cp['completedFeatTimeInterfacesReturn01']={
 'actualAssistant':'8b206110-876a-4334-bf18-b9810f18952f',
 'actualUserTurn':'e4fba178-593e-4596-915e-b408935b1b8e',
 'native':info(A/'GPT_FEAT_TIME_INTERFACES_COMPLETE_NATIVE_87.json'),
 'browser':info(A/'GPT_FEAT_TIME_INTERFACES_COMPLETE_87.txt'),
 'archive':intake['archive'],'model':intake['model'],
 'intake':info(A/'FEAT335_WORK_COMPOSITIONS_PART5_RETURN01_INTAKE_87.json'),
 'selectedProcedures':info(A/'feat335-work-compositions84-part5-return-01/SELECTED_PROCEDURES.json'),
 'casebook':info(A/'feat335-work-compositions84-part5-return-01/CASEBOOK.json'),
 'handoff':info(A/'feat335-work-compositions84-part5-return-01/CODEX_HANDOFF.md'),
 'localChecks':286,'localFailures':0,'jsonOperations':51,'completeSuccessorFiles':7,
 'sourceConferenceCompleted':True,'fullLocalSemanticReviewCompleted':False,'exactAuthorshipAccepted':False,'parent335Accepted':False,
 'selectedScopeSummary':['Qualifying complete written ritual-copy route gets Spell Scribe half-time; teacher-only remains eight hours/rank. Actual material categories govern reductions independently.','NEW fifteen-active-minute phases plus exact final remainder for only ordinary LA07 Translate/Decipher and existing-available-formula research lacking specific phases.','Craftsman applies to authorized physical construction: Contraption five uninterrupted minutes; Trapsetter fifteen active minutes with usable partial work retained over pauses; explicit temper and kill-zone exclusions remain.'],
 'reportedGptDiagnostics':intake['reportedGptDiagnostics']}
dispatch={'threadId':'6ad4a867-f330-83e9-829e-bf2bb41a6c09','threadTitle':'Calibration Review Part 5','group':'resonance-fields3-feedback-receipt-follow-through','actualUserTurn':turn['id'],'request':info(A/'GPT_RESONANCE_RECEIPT_REQUEST_87_VERIFIED.txt'),'attachment':packet,'native':info(A/'GPT_RESONANCE_RECEIPT_SENT_NATIVE_87.json'),'browserObservation':info(A/'GPT_RESONANCE_RECEIPT_SENT_87.txt'),'screenshot':info(A/'GPT_RESONANCE_RECEIPT_SENT_87.png'),'activeGenerationVerified':True,'completedResponseReceived':False,'latestObservedStatus':'ChatGPT responding after exact full request and one complete attachment; no final return yet.'}
cp['activeGptReviewAtLastVerifiedObservation']=dispatch
cp['currentResonanceReceiptActualDispatch']=dispatch
cp['nextAction']='Independently review the six exact FT84 procedure successors, three question dispositions and57 full cases while GPT resolves the already-sent Resonance Feedback receipt question. Preserve and reconcile the complete Resonance return before independent exact acceptance. Then continue remaining335 healing/reserve/world compositions and prepared Bestiary V3+EX58 conference. Canonical implementation remains owner-reserved.'
cp['healingSourcePreparation87']={'diagnosticsWritten':False,'status':'Read-only source exploration; no new healing approval. Resume after FT84 review.','sourceFindings':['Warrior foundation is d12 with later fixed base7; do not use an assumed d10.','GAMEPLAY_LOOP_CANON Short Rest: one hour, at most two beneficial rests between Long Rests. Long Rest: one Watch, once per24hours, recover half EXPENDED Hit Dice rounded up. Core Wounds reduce that recovered maximum by1 each, never each healing die.','Quick Recovery candidate adds PB once at first actual Hit Die healing event per completed rest; blocked or excess first event spends the entitlement. Ordinary healing reductions and Critical caps remain.']}
cp['lastUsageObservation']={'usedPercent':47,'remainingPercent':53,'resetsAt':1793110625,'stopAtRemainingPercent':20,'source':'Fresh get_usage_limits during87'}
cp['laterLocalWork']='Checkpoints73–87 remain local after the last separately verified GitHub backup through72; no push in87.'
# Preserve navigation byte-for-byte before adding a short current pointer.
nav=[G/'START_HERE.md',G/'DescentReviewChanges/ReviewBible/docs/DEVELOPMENT_DIRECTION.md',G/'REVIEW_MAP.html']
old={p:p.read_bytes() for p in nav}
BACKUP.mkdir()
preserved=[]
for p in nav:
 dst=BACKUP/p.name
 with dst.open('xb') as f:f.write(old[p])
 preserved.append(info(dst))
 if p.suffix=='.html':
  notice=('<aside><p><strong>Checkpoint87:</strong> GPT\u2019s three feat timing answers are preserved;286 local integrity and reconstruction checks pass. Full semantic review remains pending. Resonance Feedback follow-through is now with GPT. <a href="docs/audit/2026-10-08/full-game/'+OUT.name+'">Current record</a>.</p></aside>\n').encode()
  pos=old[p].find(b'>',old[p].find(b'<body'))+1
 else:
  rel='docs/audit/2026-10-08/full-game/' if p.name=='START_HERE.md' else '../../../docs/audit/2026-10-08/full-game/'
  notice=('\n**Current checkpoint \u2014 20 October 2026:** [Checkpoint87]('+rel+OUT.name+') preserves GPT\u2019s completed three-question feat return:34 files,51 reversible JSON operations and286 passing local intake checks. Full semantic review remains pending. The Resonance Feedback receipt question has been sent to GPT. Applied525/323/249,173 interfaces and50 accepted-unapplied remain unchanged.\n').encode()
  pos=old[p].find(b'\n')+1
 ck('Navigation insertion point '+p.name,pos>0)
 new=old[p][:pos]+notice+old[p][pos:]
 p.write_bytes(new)
 ck('All prior navigation bytes retained '+p.name,new[:pos]+new[pos+len(notice):]==old[p])
cp['navigation']=[info(p) for p in nav];cp['preservedNavigation']=preserved
ck('All previous checkpoint fields carried',set(prior).issubset(cp))
ck('Canonical approval counts unchanged',cp['authoredCounts']==prior['authoredCounts'] and cp['acceptedButUnapplied']==50 and not cp['implementationApplied'])
with SAVED.open('xb') as f:f.write(Path(__file__).read_bytes())
with OUT.open('xb') as f:f.write(enc(cp))
report={'id':'CHECKPOINT87-VALIDATION','checkpoint':info(OUT),'checks':checks,'passed':len(checks),'failed':0,'script':info(SAVED)}
with CHECK.open('xb') as f:f.write(enc(report))
print(json.dumps({'checkpoint':info(OUT),'check':info(CHECK),'passed':len(checks),'failed':0,'activeGptUserTurn':turn['id']},indent=2))
