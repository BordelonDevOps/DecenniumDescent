"""One-shot registration of MX21-40 and current noninterrupted GPT observation."""
from pathlib import Path
from datetime import datetime,timezone
from copy import deepcopy
import json,hashlib
G=Path(r'C:\Github\DecenniumDescent');A=G/'docs/audit/2026-10-08/full-game'
PRE=A/'ACTIVE_AUTHORING_CHECKPOINT_MAGIC_EXTENDED_PART01_102.json';OLD=A/'FEAT335_ORIGINAL_CASEBOOK_REVIEW_COVERAGE_102.json'
OUT=A/'ACTIVE_AUTHORING_CHECKPOINT_MAGIC_EXTENDED_PART02_103.json';CHECK=A/'ACTIVE_AUTHORING_CHECKPOINT_MAGIC_EXTENDED_PART02_103_CHECK.json';COVER=A/'FEAT335_ORIGINAL_CASEBOOK_REVIEW_COVERAGE_103.json';BACK=A/'navigation-before-magic-extended-part02-103';SAVED=A/Path(__file__).name
for p in (OUT,CHECK,COVER,BACK,SAVED):assert not p.exists(),str(p)
def j(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def enc(v):return (json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode()
def info(p,b=None):
 if b is None:b=p.read_bytes()
 return {'path':p.relative_to(G).as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def put(p,b):
 with p.open('xb') as f:f.write(b)
checks=[]
def ck(n,ok):checks.append({'check':n,'pass':bool(ok)});assert ok,n
prior=j(PRE);cp=deepcopy(prior)
ck('Exact checkpoint102',info(PRE)['sha256']=='73ef8b7630307b7d9e4d05ac1954d0d6aab10f2449c3867a3a0eb27c11f7460c')
for row in [prior['currentAuthoredIndex'],prior['currentAcceptedInterfaceRegistry'],prior['currentWorkQueue'],*prior['canonicalHelperBaselinesUnchanged']]:ck('Protected '+row['path'],info(G/row['path'])==row)
rp=A/'FEAT335_MAGIC_EXTENDED_PART02_CASEBOOK_REVIEW_103.json';r=j(rp);archive=A/'DD_Feat335_Magic_Extended_Part02_103.zip';recovery=A/'FEAT335_MAGIC_EXTENDED_PART02_PACKAGE_RECOVERY_103.json';pack=j(recovery)
ck('Exact full report',info(rp)['sha256']=='6b9c00db9a7d0fca9b0880bafd7921d059e1b45ee1a60e683689663874f65bc4')
ck('Exact complete archive',info(archive)['sha256']=='9f35ef20db5660a472a8f049931c5df374cae16922fc8940136282e79347677f')
ck('Exact packaging recovery',info(recovery)['sha256']=='8e3ab30dedb7bbd5ec58159e37ef7aa9da4449d0db4fa5a35a885e2702785e1f')
ck('280 checks31 bounded calculations',r['passed']==280 and r['failed']==0 and all(x['pass'] for x in r['checks']) and len(r['numericAndStateCalculations'])==31 and all(x['calculatedResult']==x['expectedResult'] for x in r['numericAndStateCalculations']))
ck('Recovery complete with every source and member',pack['sourceFiles']==31 and pack['archiveMembers']==37 and pack['everyMemberExact'] and pack['everySourceUnchanged'] and pack['originalReportUnchanged'] and pack['archive']==info(archive))
for row in r['sourceBindings']:ck('Source retained '+row['path'],info(G/row['path'])==row)
for row in pack['preservedPartialFiles']:ck('Partial output retained '+row['path'],info(G/row['path'])==row)
old=j(OLD);coverage=deepcopy(old);ck('Exact prior coverage',info(OLD)['sha256']=='31a102cfe64d742a00ec33180b2f29c674b8727ed95a10b1cd12c3e1355acc91')
new={x['id']:i for i,x in enumerate(r['originalCaseReviews'])};fa={x['id']:i for i,x in enumerate(r['additionalBoundaryReviews'])};oldids={x['id'] for x in old['ordinary']['positions'] if x['reviewedByThisFullCaseRegister']};oldfa={x['id'] for x in old['additional']['positions'] if x['reviewedByThisFullCaseRegister']}
ck('40new originals distinct from540',len(new)==40 and len(oldids)==540 and not set(new)&oldids)
ck('2new boundaries distinct from19',len(fa)==2 and len(oldfa)==19 and not set(fa)&oldfa)
coverage.update(id='FEAT335-ORIGINAL-CASEBOOK-REVIEW-COVERAGE-103',recordedAtUtc=datetime.now(timezone.utc).isoformat(),previousRegister=info(OLD),basis='Seven complete cohorts plus magic_extended MX01-MX40:80/116 originals andFA04/16/20/21. Extended remains40/58 records, not complete. Actual acquisition/world prerequisites remain conditional.',reviewReports=[*old['reviewReports'],info(rp)])
for row in coverage['ordinary']['positions']:
 if row['id'] in new:row.update(reviewedByThisFullCaseRegister=True,reviewEvidencePointer='/originalCaseReviews/'+str(new[row['id']]),reviewEvidenceReport=info(rp),status='COMPLETE_STATED_CASE_SEMANTIC_REVIEW')
for row in coverage['additional']['positions']:
 if row['id'] in fa:row.update(reviewedByThisFullCaseRegister=True,reviewEvidencePointer='/additionalBoundaryReviews/'+str(fa[row['id']]),reviewEvidenceReport=info(rp),status='COMPLETE_STATED_CASE_SEMANTIC_REVIEW')
coverage['ordinary'].update(reviewed=580,outsideCurrentFullCaseReview=80);coverage['additional'].update(reviewed=21,outsideCurrentFullBoundaryReview=7)
coverage['partialCohorts']=[{'cohort':'magic_extended','recordsReviewed':40,'recordsTotal':58,'questionRange':'MX01-MX40','originalCasesReviewed':80,'originalCasesTotal':116,'additionalReviewed':['FA-04','FA-16','FA-20','FA-21'],'reports':[prior['featMagicExtendedPart01_102']['report'],info(rp)],'remainingQuestionRange':'MX41-MX58'}]
ck('580of660 exact reviewed positions',len(coverage['ordinary']['positions'])==660 and sum(x['reviewedByThisFullCaseRegister'] for x in coverage['ordinary']['positions'])==580)
ck('21of28 exact reviewed boundaries',len(coverage['additional']['positions'])==28 and sum(x['reviewedByThisFullCaseRegister'] for x in coverage['additional']['positions'])==21)
ck('All previous original reviews unchanged',all(x==y for x,y in zip(old['ordinary']['positions'],coverage['ordinary']['positions']) if x['id'] not in new))
ck('All previous boundary reviews unchanged',all(x==y for x,y in zip(old['additional']['positions'],coverage['additional']['positions']) if x['id'] not in fa))
ck('No whole extended-cohort approval',coverage['completedCohorts']==old['completedCohorts'] and 'magic_extended' not in coverage['completedCohorts'])
coverbytes=enc(coverage)
native=A/'GPT_BESTIARY_RECOVERY_PART01_NATIVE_103.json';active=A/'GPT_BESTIARY_RECOVERY_PART01_ACTIVE_103.txt';unity=A/'GPT_UNITY_NOTEBOOK_RECHECK_103.json';n=j(native);u=j(unity)
ck('Exact dispatched request still latest native',n['turns'][0]['id']=='b82cd045-2ee8-4187-95b4-d0302f3f8d91' and n['thread']['status']['type']=='active')
ck('Visible active response without interruption','ChatGPT is responding' in active.read_text(encoding='utf-8') and 'button "Stop"' in active.read_text(encoding='utf-8'))
ck('Unity brief identities unchanged',u['turnIdentitySummary'][0]['id']=='41d5797f-d115-4cce-90fd-8ccc835b86cb' and any(i['id']=='b0572b7f-e15c-4d11-8353-86853e0329c6' for i in u['turnIdentitySummary'][0]['items']))
cp.update(id='ACTIVE-AUTHORING-MAGIC-EXTENDED-PART02-103',recordedAtUtc=datetime.now(timezone.utc).isoformat(),previousCheckpoint=info(PRE),status='Progress: MX21-40 full review adds40 originals2boundaries31 bounded calculations280checks. Cumulative580/660originals21/28boundaries; extended40/58records remains partial. Windows path-length packaging recovered with full exact source map. GPT Part01 still active; no new final return or rules promoted.')
cp['previousGoalTurnClassification']={'turn':102,'classification':'progress','evidence':prior['featMagicExtendedPart01_102']['report'],'reason':'20fullrecords40originals2boundaries reviewed and actual bounded bestiary request delivered.'}
cp['featMagicExtendedPart02_103']={'report':info(rp),'archive':info(archive),'packagingRecovery':info(recovery),'coverageRegister':info(COVER,coverbytes),'coverage':r['coverage'],'cumulativeOriginalPositionsReviewed':580,'remainingOriginalPositionsInRegister':80,'cumulativeAdditionalBoundariesReviewed':21,'remainingAdditionalBoundariesInRegister':7,'checks':280,'failed':0,'fullSourceFiles':31,'archiveMembers':37,'findings':r['reviewFindings'],'remainingScope':r['remainingScope'],'actuallySentToGpt':False,'canonicalApplied':False,'parent335Accepted':False,'runtimeTestsExecuted':0}
cp['activeGptReviewAtLastVerifiedObservation'].update(latestNativeRecord=info(native),latestObservation103=info(active),latestObservedStatus='Bestiary RecoveryPart01 remains active in both native and visible browser state. No completed response/new output artifact observed; left running and no new message sent. Unity notebook newest user/assistant identities unchanged from101.')
cp['notebookRecheck103']={'reviewNative':info(native),'reviewVisible':info(active),'unityIdentityCheck':info(unity),'newMessagesSent':0,'newFinalBestiaryReturnReceived':False,'activeGenerationInterrupted':False,'newUnityDirections':False}
cp['nextAction']='Finish remaining extended magic MX41-MX58:18records36originals3boundariesFA17/18/26; then heritage_mutation22records44originals4boundaries. Current total580/660originals21/28boundaries, not whole-game completion. Preserve ArcaneAdaptation original/internal/public/laterCOPY-READY-ALLOWANCE-02 full successors and actual standalone TrueStrike/Haste. GPTRecoveryPart01 remains active: do notinterrupt; save full final bounded text and actual artifacts immediately when complete, then independently review before acceptance and continue remaining bounded bestiary parts. Actual dispatched status was500/17; local580/21 and fullcasebooks remainunsent. Parent335 actualacquisition/copy/mental-predicate assembly/jointreview stillpending. No overlapping Unity delivery-checkout edits or canonical promotion.'
cp['lastUsageObservation']={'usedPercent':68,'remainingPercent':32,'resetsAt':1793110625,'stopAtRemainingPercent':20,'source':'Fresh get_usage_limits after MX21-40 review and packaging recovery'}
cp['laterLocalWork']='Review checkpoints73-103 local after last verified GitHub backup through72. No push103. Separate user Unity task has independent delivery-checkout work; preserve it.'
nav=[G/x['path'] for x in prior['navigation']];raws={};prepared={}
for p in nav:
 raw=p.read_bytes();raws[p]=raw;row=next(x for x in prior['navigation'] if x['path']==p.relative_to(G).as_posix());ck('Navigation precondition '+p.name,info(p,raw)==row)
 if p.suffix=='.html':
  pos=raw.find(b'>',raw.find(b'<body'))+1;note=('<aside><p><strong>Checkpoint103:</strong> Magic MX21-40 adds40 original reviews and2 boundaries; cumulative580/660 and21/28.31 bounded calculations,280 checks. Extended magic40/58 remains open. <a href="docs/audit/2026-10-08/full-game/'+OUT.name+'">Current record</a>. GPT bestiary RecoveryPart01 is still active.</p></aside>\n').encode()
 else:
  pos=raw.find(b'\n')+1;prefix='docs/audit/2026-10-08/full-game/' if p.name=='START_HERE.md' else '../../../docs/audit/2026-10-08/full-game/';note=('\n**Current review checkpoint:** [Checkpoint103]('+prefix+OUT.name+') preserves MX21-40:20 records,40 originals,2 boundaries,31 bounded calculations and280 checks. Cumulative580/660 originals and21/28 boundaries; extended magic40/58 remains partial. Full package verified after a path-length recovery; all original sources preserved. GPT bestiary RecoveryPart01 remains active. No canonical promotion.\n').encode()
 ck('Navigation insertion '+p.name,pos>0);prepared[p]=raw[:pos]+note+raw[pos:];ck('Prior navigation intact '+p.name,prepared[p][:pos]+prepared[p][pos+len(note):]==raw)
cp['navigation']=[info(p,prepared[p]) for p in nav];cp['preservedNavigation']=[info(BACK/p.name,raws[p]) for p in nav]
ck('Prior checkpoint fields retained',set(prior).issubset(cp));ck('Counts and authority unchanged',cp['authoredCounts']==prior['authoredCounts'] and cp['acceptedButUnapplied']==53 and not cp['implementationApplied'])
payload=enc(cp);validation=enc({'id':'CHECKPOINT103-VALIDATION','checkpoint':info(OUT,payload),'checks':checks,'passed':len(checks),'failed':0,'script':info(SAVED,Path(__file__).read_bytes()),'newGptMessagesSent':0,'runtimeTestsExecuted':0})
BACK.mkdir()
for p in nav:
 put(BACK/p.name,raws[p]);assert p.read_bytes()==raws[p];p.write_bytes(prepared[p])
for p,b in [(SAVED,Path(__file__).read_bytes()),(COVER,coverbytes),(OUT,payload),(CHECK,validation)]:put(p,b)
print(json.dumps({'checkpoint':info(OUT),'check':info(CHECK),'coverage':info(COVER),'passed':len(checks),'failed':0},indent=2))
