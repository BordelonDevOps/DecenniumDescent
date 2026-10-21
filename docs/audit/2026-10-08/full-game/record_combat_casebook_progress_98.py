"""One-shot combat casebook checkpoint with cumulative exact evidence links."""
from pathlib import Path
from copy import deepcopy
from datetime import datetime,timezone
import json,hashlib
G=Path(r'C:\Github\DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game'
PRE=A/'ACTIVE_AUTHORING_CHECKPOINT_DEFENSE_CASEBOOK_97.json';OLD=A/'FEAT335_ORIGINAL_CASEBOOK_REVIEW_COVERAGE_97.json'
OUT=A/'ACTIVE_AUTHORING_CHECKPOINT_COMBAT_CASEBOOK_98.json';CHECK=A/'ACTIVE_AUTHORING_CHECKPOINT_COMBAT_CASEBOOK_98_CHECK.json';COVER=A/'FEAT335_ORIGINAL_CASEBOOK_REVIEW_COVERAGE_98.json';BACK=A/'navigation-before-combat-casebook-98';SAVED=A/Path(__file__).name
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
ck('Exact checkpoint97',info(PRE)['sha256']=='eab05537877c60ed4ca0ac2d92fb8bb466d32c63a30018a3b0ef687268ee214c')
for row in [prior['currentAuthoredIndex'],prior['currentAcceptedInterfaceRegistry'],prior['currentWorkQueue'],*prior['canonicalHelperBaselinesUnchanged']]:ck('Protected baseline '+row['path'],info(G/row['path'])==row)
rp=A/'FEAT335_COMBAT_ORIGINAL_CASEBOOK_REVIEW_98.json';r=j(rp);archive=A/'DD_Feat335_Combat_Casebook_Review_98.zip'
ck('Exact complete combat report',info(rp)['sha256']=='4d4bf4c930bab294aa16d0eb1be7b47a972736a609ed3e6b122f167388c44ad8')
ck('Exact full combat archive',info(archive)['sha256']=='4a19a881532ff4e1ea696588a2cb9fa50046640d5d056b13c8cfcf26d2133d7a')
ck('395 passing source/arithmetic checks',r['passed']==395 and r['failed']==0 and all(x['pass'] for x in r['checks']))
ck('47 complete procedures94 original cases2 boundaries',len(r['completeSelectedRecords'])==47 and len(r['originalCaseReviews'])==94 and len(r['additionalBoundaryReviews'])==2)
ck('62 bounded reference calculations agree',len(r['numericAndStateCalculations'])==62 and all(x['calculatedResult']==x['expectedResult'] for x in r['numericAndStateCalculations']))
for row in r['sourceBindings']:ck('Full source unchanged '+row['path'],info(G/row['path'])==row)
ck('No runtime canonical or parent promotion',not r['parent335Accepted'] and not r['canonicalApplied'] and r['runtimeTestsExecuted']==0)
old=j(OLD);coverage=deepcopy(old)
ck('Exact previous register97',info(OLD)['sha256']=='04f370dbbfd4c48a951f95eb2fe3ac8bad26bcf2cbd7fe8d4d6428ab6a69d233')
new_reviews={x['id']:n for n,x in enumerate(r['originalCaseReviews'])};new_fa={x['id']:n for n,x in enumerate(r['additionalBoundaryReviews'])}
old_reviewed={x['id'] for x in old['ordinary']['positions'] if x['reviewedByThisFullCaseRegister']};old_fa={x['id'] for x in old['additional']['positions'] if x['reviewedByThisFullCaseRegister']}
ck('94 new original cases do not duplicate228',len(new_reviews)==94 and len(old_reviewed)==228 and not set(new_reviews)&old_reviewed)
ck('2 new boundaries do not duplicate10',len(new_fa)==2 and len(old_fa)==10 and not set(new_fa)&old_fa)
coverage['id']='FEAT335-ORIGINAL-CASEBOOK-REVIEW-COVERAGE-98';coverage['recordedAtUtc']=datetime.now(timezone.utc).isoformat();coverage['previousRegister']=info(OLD)
coverage['basis']='Cumulative full original-position authored semantic reviews: general_exploration93, skill94, crafting95, general_defense97 and combat98. Targeted earlier diagnostics remain separate; preserved original and current replacement examples are one original position, not two.'
coverage['reviewReports']=[*old['reviewReports'],info(rp)]
for row in coverage['ordinary']['positions']:
 if row['id'] in new_reviews:row.update(reviewedByThisFullCaseRegister=True,reviewEvidencePointer='/originalCaseReviews/'+str(new_reviews[row['id']]),reviewEvidenceReport=info(rp),status='COMPLETE_STATED_CASE_SEMANTIC_REVIEW')
for row in coverage['additional']['positions']:
 if row['id'] in new_fa:row.update(reviewedByThisFullCaseRegister=True,reviewEvidencePointer='/additionalBoundaryReviews/'+str(new_fa[row['id']]),reviewEvidenceReport=info(rp),status='COMPLETE_STATED_CASE_SEMANTIC_REVIEW')
coverage['ordinary']['reviewed']=322;coverage['ordinary']['outsideCurrentFullCaseReview']=338;coverage['additional']['reviewed']=12;coverage['additional']['outsideCurrentFullBoundaryReview']=16;coverage['completedCohorts']=[*old['completedCohorts'],'combat']
ck('All660 original positions with322 exact review links',len(coverage['ordinary']['positions'])==660 and sum(x['reviewedByThisFullCaseRegister'] for x in coverage['ordinary']['positions'])==322)
ck('All28 additional positions with12 exact review links',len(coverage['additional']['positions'])==28 and sum(x['reviewedByThisFullCaseRegister'] for x in coverage['additional']['positions'])==12)
ck('Original identities and pointers retained',all(all(before[k]==new[k] for k in ['id','featId','cohort','originalSourcePointer']) for before,new in zip(old['ordinary']['positions'],coverage['ordinary']['positions'])))
ck('All earlier ordinary evidence unchanged',all(before==new for before,new in zip(old['ordinary']['positions'],coverage['ordinary']['positions']) if before['id'] not in new_reviews))
ck('All earlier boundary evidence unchanged',all(before==new for before,new in zip(old['additional']['positions'],coverage['additional']['positions']) if before['id'] not in new_fa))
coverage_bytes=enc(coverage);obs=A/'GPT_BESTIARY_REPLACEMENT_ACTIVE_OBSERVATION_98.txt'
ck('BestiaryReturn02 actively generating now','button "Stop"' in obs.read_text(encoding='utf-8') and 'Working for 30m 37s' in obs.read_text(encoding='utf-8'))
cp['id']='ACTIVE-AUTHORING-COMBAT-CASEBOOK-98';cp['recordedAtUtc']=datetime.now(timezone.utc).isoformat();cp['previousCheckpoint']=info(PRE)
cp['status']='Progress:47 full combat procedures,94 original examples and2 FA boundaries reviewed with62 bounded calculations and395 checks. Cumulative322/660 originals and12/28 boundaries. GPT new BestiaryReturn02 remains actively generating; no canonical integration.'
cp['previousGoalTurnClassification']={'turn':97,'classification':'progress','evidence':prior['featDefenseCasebook97']['report']}
cp['featCombatCasebook98']={'report':info(rp),'archive':info(archive),'coverageRegister':planned(COVER,coverage_bytes),'coverage':r['coverage'],'cumulativeOriginalPositionsReviewed':322,'remainingOriginalPositionsInRegister':338,'cumulativeAdditionalBoundariesReviewed':12,'remainingAdditionalBoundariesInRegister':16,'checks':395,'failed':0,'fullSourceFiles':22,'archiveMembers':26,'findings':r['reviewFindings'],'remainingScope':r['remainingScope'],'actuallySentToGpt':False,'canonicalApplied':False,'parent335Accepted':False,'runtimeTestsExecuted':0}
cp['previousGptObservationBefore98']=deepcopy(prior['activeGptReviewAtLastVerifiedObservation']);cp['activeGptReviewAtLastVerifiedObservation']['latestObservation98']=info(obs)
cp['activeGptReviewAtLastVerifiedObservation']['latestObservedStatus']='Browser shows active Stop,30m37s working and thinking-more notice. Return02 not complete, received or accepted. Interim79-trait andDC15/3d8force PressureWave statements remain unverified pending final actual source-linked artifacts. No interruption/restart/message/upload.'
cp['bestiaryReplacementDispatch96']['latestObservation98']=info(obs)
cp['pertinentNotebookRecheck98']={'browserRecord':info(obs),'actualReturn02User':'09fd693b-be2d-4274-bc1e-57ac20f4b422','newCompletedReturnObserved':False,'newMessagesSent':0,'unityLastVerifiedNativeRecord':prior['pertinentNotebookRecheck97']['nativeRecord'],'qualification':'Browser checked live in98; Unity native notebook was last checked97, no new98 claim.'}
cp['nextAction']='Continue full original feat casebook review next general_combat58 procedures/116 originals plusFA05/11/12.338 originals and16 boundaries remain. When GPT BestiaryReturn02 actually completes, immediately preserve/download all full returned artifacts, then independently verify counts, native text/traits/PressureWave, meaningful positive encounters, operations and held interfaces before acceptance. No restart solely from elapsed thinking.93/94/95/97/98 full casebook packets remain local unsent; communicate substantive conclusions at the next actual conference. Preserve defense mental-predicate final-assembly dependency and all parent335/source-world/copy holds.'
cp['lastUsageObservation']={'usedPercent':60,'remainingPercent':40,'resetsAt':1793110625,'stopAtRemainingPercent':20,'source':'Fresh get_usage_limits at start and after casebook98'}
cp['laterLocalWork']='Checkpoints73–98 remain local after last separately verified GitHub backup through72; no push in98.'
nav=[G/'START_HERE.md',R/'docs/DEVELOPMENT_DIRECTION.md',G/'REVIEW_MAP.html'];old_nav={};prepared={}
for p in nav:
 row=next(x for x in prior['navigation'] if x['path']==p.relative_to(G).as_posix());ck('Exact previous navigation '+p.name,info(p)==row);raw=old_nav[p]=p.read_bytes()
 if p.suffix=='.html':
  pos=raw.find(b'>',raw.find(b'<body'))+1;note=('<aside><p><strong>Checkpoint98:</strong> Combat review adds47 full procedures,94 original cases and2 boundaries with62 bounded calculations. Cumulative322/660 originals and12/28 boundaries. <a href="docs/audit/2026-10-08/full-game/'+OUT.name+'">Current record</a>. Parent335 pending; GPT BestiaryReturn02 actively generating.</p></aside>\n').encode()
 else:
  pos=raw.find(b'\n')+1;prefix='docs/audit/2026-10-08/full-game/' if p.name=='START_HERE.md' else '../../../docs/audit/2026-10-08/full-game/';note=('\n**Current checkpoint — combat casebook:** [Checkpoint98]('+prefix+OUT.name+') records47 full combat procedures,94 original cases and2 additional boundaries, with62 bounded calculations and395 checks. Cumulative full-case coverage322/660 plus12/28 boundaries. Four prior replacement examples and all original text remain preserved. Parent335 and runtime remain pending; GPT BestiaryReturn02 is still actively generating.\n').encode()
 ck('Valid insertion '+p.name,pos>0);new=raw[:pos]+note+raw[pos:];ck('All earlier navigation bytes retained '+p.name,new[:pos]+new[pos+len(note):]==raw);prepared[p]=new
cp['navigation']=[planned(p,prepared[p]) for p in nav];cp['preservedNavigation']=[planned(BACK/p.name,old_nav[p]) for p in nav]
ck('Every earlier checkpoint field retained',set(prior).issubset(cp));ck('No spell count acceptance or application change',cp['acceptedButUnapplied']==53 and cp['authoredCounts']==prior['authoredCounts'] and not cp['implementationApplied'])
payload=enc(cp);script=Path(__file__).read_bytes();validation=enc({'id':'CHECKPOINT98-VALIDATION','checkpoint':planned(OUT,payload),'checks':checks,'passed':len(checks),'failed':0,'script':planned(SAVED,script),'anyNewGptMessageSent':False})
BACK.mkdir()
for p in nav:put(BACK/p.name,old_nav[p]);p.write_bytes(prepared[p])
for p,b in [(SAVED,script),(COVER,coverage_bytes),(OUT,payload),(CHECK,validation)]:put(p,b)
print(json.dumps({'checkpoint':info(OUT),'check':info(CHECK),'coverage':info(COVER),'passed':len(checks),'failed':0},indent=2))
