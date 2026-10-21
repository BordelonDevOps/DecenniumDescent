"""One-shot magic-core progress checkpoint and actual GPT continuation evidence."""
from pathlib import Path
from copy import deepcopy
from datetime import datetime,timezone
import json,hashlib
G=Path(r'C:\Github\DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game'
PRE=A/'ACTIVE_AUTHORING_CHECKPOINT_GENERAL_COMBAT_CASEBOOK_99.json';OLD=A/'FEAT335_ORIGINAL_CASEBOOK_REVIEW_COVERAGE_99.json'
OUT=A/'ACTIVE_AUTHORING_CHECKPOINT_MAGIC_CORE_CASEBOOK_100.json';CHECK=A/'ACTIVE_AUTHORING_CHECKPOINT_MAGIC_CORE_CASEBOOK_100_CHECK.json';COVER=A/'FEAT335_ORIGINAL_CASEBOOK_REVIEW_COVERAGE_100.json';BACK=A/'navigation-before-magic-core-casebook-100';SAVED=A/Path(__file__).name
for p in [OUT,CHECK,COVER,BACK,SAVED]:assert not p.exists(),str(p)
def j(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def enc(v):return (json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode()
def planned(p,b):return {'path':p.relative_to(G).as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def info(p):return planned(p,p.read_bytes())
def put(p,b):
 with p.open('xb') as f:f.write(b)
checks=[]
def ck(n,ok):checks.append({'check':n,'pass':bool(ok)});assert ok,n
prior=j(PRE);cp=deepcopy(prior)
ck('Exact checkpoint99',info(PRE)['sha256']=='126ca6e3883ae07168e8fd38eae4ec27b7b52b35da3d7108457315202211cc51')
for row in [prior['currentAuthoredIndex'],prior['currentAcceptedInterfaceRegistry'],prior['currentWorkQueue'],*prior['canonicalHelperBaselinesUnchanged']]:ck('Protected baseline '+row['path'],info(G/row['path'])==row)
rp=A/'FEAT335_MAGIC_CORE_ORIGINAL_CASEBOOK_REVIEW_100.json';r=j(rp);archive=A/'DD_Feat335_Magic_Core_Casebook_Review_100.zip'
ck('Exact complete magic-core report',info(rp)['sha256']=='acda8cd74ea8e4af615c6770bf5b48d192f6f9b2a1d7c9a0cffcbe8d14b4b6c2')
ck('Exact complete source archive',info(archive)['sha256']=='3fe87afa966f6eb21acf2477b4f62c86bac89a632566be4544ac055cfffcfbbe')
ck('1674 source and reference checks passed',r['passed']==1674 and r['failed']==0 and all(x['pass'] for x in r['checks']))
ck('31 full records62 original positions2 boundaries',len(r['completeSelectedRecords'])==31 and len(r['originalCaseReviews'])==62 and len(r['additionalBoundaryReviews'])==2)
ck('37 bounded projections agree',len(r['numericAndStateCalculations'])==37 and all(x['calculatedResult']==x['expectedResult'] for x in r['numericAndStateCalculations']))
for row in r['sourceBindings']:ck('Full source preserved '+row['path'],info(G/row['path'])==row)
ck('No canonical runtime or parent promotion',not r['canonicalApplied'] and not r['parent335Accepted'] and r['runtimeTestsExecuted']==0)
old=j(OLD);coverage=deepcopy(old);ck('Exact previous coverage99',info(OLD)['sha256']=='c42ac6e9acaf1cb4e013f4e91bd411b54bac4e1865c66b4ebb69be04cdf4efae')
new_reviews={x['id']:n for n,x in enumerate(r['originalCaseReviews'])};new_fa={x['id']:n for n,x in enumerate(r['additionalBoundaryReviews'])}
old_reviewed={x['id'] for x in old['ordinary']['positions'] if x['reviewedByThisFullCaseRegister']};old_fa={x['id'] for x in old['additional']['positions'] if x['reviewedByThisFullCaseRegister']}
ck('62 new originals distinct from438',len(new_reviews)==62 and len(old_reviewed)==438 and not set(new_reviews)&old_reviewed)
ck('2 new boundaries distinct from15',len(new_fa)==2 and len(old_fa)==15 and not set(new_fa)&old_fa)
coverage['id']='FEAT335-ORIGINAL-CASEBOOK-REVIEW-COVERAGE-100';coverage['recordedAtUtc']=datetime.now(timezone.utc).isoformat();coverage['previousRegister']=info(OLD)
coverage['basis']='Cumulative full stated-case reviews: general_exploration93, skill94, crafting95, general_defense97, combat98, general_combat99 and magic_core100. The magic cohort includes two correctly unavailable wrappers, not executable travel/binding cases. Targeted earlier diagnostics are separate.'
coverage['reviewReports']=[*old['reviewReports'],info(rp)]
for row in coverage['ordinary']['positions']:
 if row['id'] in new_reviews:row.update(reviewedByThisFullCaseRegister=True,reviewEvidencePointer='/originalCaseReviews/'+str(new_reviews[row['id']]),reviewEvidenceReport=info(rp),status='COMPLETE_STATED_CASE_SEMANTIC_REVIEW')
for row in coverage['additional']['positions']:
 if row['id'] in new_fa:row.update(reviewedByThisFullCaseRegister=True,reviewEvidencePointer='/additionalBoundaryReviews/'+str(new_fa[row['id']]),reviewEvidenceReport=info(rp),status='COMPLETE_STATED_CASE_SEMANTIC_REVIEW')
coverage['ordinary']['reviewed']=500;coverage['ordinary']['outsideCurrentFullCaseReview']=160;coverage['additional']['reviewed']=17;coverage['additional']['outsideCurrentFullBoundaryReview']=11;coverage['completedCohorts']=[*old['completedCohorts'],'magic_core']
ck('660 original identities500 exact reviewed positions',len(coverage['ordinary']['positions'])==660 and sum(x['reviewedByThisFullCaseRegister'] for x in coverage['ordinary']['positions'])==500)
ck('28 boundary identities17 exact reviewed positions',len(coverage['additional']['positions'])==28 and sum(x['reviewedByThisFullCaseRegister'] for x in coverage['additional']['positions'])==17)
ck('All original source identity pointers preserved',all(all(before[k]==after[k] for k in ['id','featId','cohort','originalSourcePointer']) for before,after in zip(old['ordinary']['positions'],coverage['ordinary']['positions'])))
ck('Every earlier original review retained',all(before==after for before,after in zip(old['ordinary']['positions'],coverage['ordinary']['positions']) if before['id'] not in new_reviews))
ck('Every earlier boundary review retained',all(before==after for before,after in zip(old['additional']['positions'],coverage['additional']['positions']) if before['id'] not in new_fa))
coverage_bytes=enc(coverage)
terminal=A/'GPT_BESTIARY_RETURN02_TERMINAL_WITHOUT_DELIVERY_100.txt';native_before=A/'GPT_BESTIARY_RETURN02_NATIVE_NO_DELIVERY_100.json';request=A/'CODEX_BESTIARY_RETURN02_CONTINUATION_REQUEST_100.txt';sent=A/'GPT_BESTIARY_RETURN02_CONTINUATION_SENT_100.txt';proof=A/'GPT_BESTIARY_RETURN02_CONTINUATION_SENT_100.png';native_after=A/'GPT_BESTIARY_RETURN02_POST_DISPATCH_NATIVE_100.json'
ck('Fresh terminal view retained before dispatch','Worked for 39m 48s' in terminal.read_text(encoding='utf-8') and 'button "Stop"' not in terminal.read_text(encoding='utf-8'))
sent_text=sent.read_text(encoding='utf-8');ck('Actual continuation visibly present and responding','Please continue the existing Bestiary Return02 work to complete delivery.' in sent_text and '500/660' in sent_text and 'ChatGPT is responding' in sent_text and 'button "Stop"' in sent_text)
ck('Native before record says idle',json.loads(j(native_before)['content'][0]['text'])['thread']['status']['type']=='idle')
ck('Native after says active though latest persisted turn lags',json.loads(j(native_after)['content'][0]['text'])['thread']['status']['type']=='active')
cp['id']='ACTIVE-AUTHORING-MAGIC-CORE-CASEBOOK-100';cp['recordedAtUtc']=datetime.now(timezone.utc).isoformat();cp['previousCheckpoint']=info(PRE)
cp['status']='Progress:31 complete magic-core records (29 proposed procedures and2 unavailable wrappers),62 originals and2 boundaries reviewed with37 bounded calculations and1674 source/reference checks. Cumulative500/660 originals and17/28 boundaries. Actual GPT continuation100 delivered after fresh terminal/no-delivery evidence; GPT responding again. No canonical integration.'
cp['previousGoalTurnClassification']={'turn':99,'classification':'progress','evidence':prior['featGeneralCombatCasebook99']['report']}
cp['featMagicCoreCasebook100']={'report':info(rp),'archive':info(archive),'coverageRegister':planned(COVER,coverage_bytes),'coverage':r['coverage'],'cumulativeOriginalPositionsReviewed':500,'remainingOriginalPositionsInRegister':160,'cumulativeAdditionalBoundariesReviewed':17,'remainingAdditionalBoundariesInRegister':11,'checks':1674,'failed':0,'fullSourceFiles':23,'archiveMembers':27,'findings':r['reviewFindings'],'remainingScope':r['remainingScope'],'actuallySentToGpt':False,'summaryActuallySentToGpt':True,'canonicalApplied':False,'parent335Accepted':False,'runtimeTestsExecuted':0}
cp['previousGptObservationBefore100']=deepcopy(prior['activeGptReviewAtLastVerifiedObservation']);cp['activeGptReviewAtLastVerifiedObservation']['latestObservation100']=info(sent)
cp['activeGptReviewAtLastVerifiedObservation']['latestObservedStatus']='Initial old review tab later showed Unity Development Setup. Newly opened actual Part5 tab125747444 showed Worked39m48s and noStop, corroborated by native idle and no delivered final return. A single explicit continue-existing-work request was then sent through send_message_to_thread. Early post-dispatch snapshots/native message listing lagged; final browser visibly contains the exact new user request and active ChatGPT-is-responding/Stop. No Stop control, regeneration or scratch restart was used; no duplicate dispatch. Return02 files remain undelivered/unaccepted.'
cp['bestiaryReturn02Continuation100']={'threadId':'6ad4a867-f330-83e9-829e-bf2bb41a6c09','title':'Calibration Review Part 5','browserTabId':'125747444','priorSourceRequestUserId':'09fd693b-be2d-4274-bc1e-57ac20f4b422','newMessageId':'not-yet-in-native-persisted-turn-list; exact browser text verified','terminalBrowserEvidence':info(terminal),'nativeBeforeEvidence':info(native_before),'exactSentRequest':info(request),'browserDeliveryEvidence':info(sent),'screenshot':info(proof),'nativeAfterEvidence':info(native_after),'actuallySent':True,'dispatchCount':1,'responseActiveAtLastObservation':True,'newReturnReceived':False,'newReturnAccepted':False,'summaryCoverageActuallyCommunicated':{'originals':500,'originalTotal':660,'boundaries':17,'boundaryTotal':28},'fullCasebookPacketsUploaded':False}
cp['pertinentNotebookRecheck100']={'browserRecord':info(sent),'unityLastVerifiedNativeRecord':prior['pertinentNotebookRecheck97']['nativeRecord'],'qualification':'The formerly bound user tab now points to Unity. No new Unity native content review is claimed; a separate actual Part5 tab was opened for continuation. Original Unity tabs left intact.'}
cp['nextAction']='Continue full magic_extended58 procedures/116 originals and its exact additional boundaries, then heritage_mutation22/44.160 originals and11 boundaries remain. GPT continuation100 is visibly active: wait for actual completion without interrupting. Immediately download and preserve delivered full Return02 artifacts, verify real sources/traits/PressureWave/positive encounters/operations before acceptance, and preserve all five whole positive holds. Actual continued response files may differ from missing Return01; never reuse reported old hashes. Full93/94/95/97/98/99/100 casebook archives remain local unsent; their500/660 and17/28 status was genuinely communicated. Keep parent335 finite-table/acquisition/copy/mental-predicate final-assembly and joint-conference obligations.'
cp['lastUsageObservation']={'usedPercent':63,'remainingPercent':37,'resetsAt':1793110625,'stopAtRemainingPercent':20,'source':'Fresh get_usage_limits after magic_core100 and GPT continuation dispatch'}
cp['laterLocalWork']='Checkpoints73–100 local after last separately verified GitHub backup through72; no push in100.'
nav=[G/'START_HERE.md',R/'docs/DEVELOPMENT_DIRECTION.md',G/'REVIEW_MAP.html'];old_nav={};prepared={}
for p in nav:
 row=next(x for x in prior['navigation'] if x['path']==p.relative_to(G).as_posix());ck('Exact previous navigation '+p.name,info(p)==row);raw=old_nav[p]=p.read_bytes()
 if p.suffix=='.html':
  pos=raw.find(b'>',raw.find(b'<body'))+1;note=('<aside><p><strong>Checkpoint100:</strong> Magic core review adds62 original cases and2 boundaries; two cosmology payloads remain unavailable. Cumulative500/660 originals and17/28 boundaries. <a href="docs/audit/2026-10-08/full-game/'+OUT.name+'">Current record</a>. GPT received continuation and progress update; bestiary files still pending.</p></aside>\n').encode()
 else:
  pos=raw.find(b'\n')+1;prefix='docs/audit/2026-10-08/full-game/' if p.name=='START_HERE.md' else '../../../docs/audit/2026-10-08/full-game/';note=('\n**Current checkpoint — magic core casebook:** [Checkpoint100]('+prefix+OUT.name+') preserves31 full records,62 original examples and2 boundaries, with37 bounded calculations and1674 source/reference checks. Cumulative500/660 original positions plus17/28 boundaries. Astral Projection/Planar Binding stay unavailable. GPT received the actual continuation request and current totals; full bestiary delivery and parent335 review remain pending.\n').encode()
 ck('Valid insertion '+p.name,pos>0);new=raw[:pos]+note+raw[pos:];ck('All older navigation bytes retained '+p.name,new[:pos]+new[pos+len(note):]==raw);prepared[p]=new
cp['navigation']=[planned(p,prepared[p]) for p in nav];cp['preservedNavigation']=[planned(BACK/p.name,old_nav[p]) for p in nav]
ck('Every previous checkpoint field retained',set(prior).issubset(cp));ck('No spell count acceptance or application change',cp['acceptedButUnapplied']==53 and cp['authoredCounts']==prior['authoredCounts'] and not cp['implementationApplied'])
payload=enc(cp);script=Path(__file__).read_bytes();validation=enc({'id':'CHECKPOINT100-VALIDATION','checkpoint':planned(OUT,payload),'checks':checks,'passed':len(checks),'failed':0,'script':planned(SAVED,script),'anyNewGptMessageSent':True,'newMessagesSent':1})
BACK.mkdir()
for p in nav:put(BACK/p.name,old_nav[p]);p.write_bytes(prepared[p])
for p,b in [(SAVED,script),(COVER,coverage_bytes),(OUT,payload),(CHECK,validation)]:put(p,b)
print(json.dumps({'checkpoint':info(OUT),'check':info(CHECK),'coverage':info(COVER),'passed':len(checks),'failed':0},indent=2))
