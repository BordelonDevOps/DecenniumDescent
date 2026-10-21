"""One-shot cumulative casebook checkpoint, preserving previous complete evidence."""
from pathlib import Path
from copy import deepcopy
from datetime import datetime,timezone
import json,hashlib
G=Path(r'C:\Github\DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game'
PRE=A/'ACTIVE_AUTHORING_CHECKPOINT_BESTIARY_REPLACEMENT_96.json';OLD=A/'FEAT335_ORIGINAL_CASEBOOK_REVIEW_COVERAGE_95.json'
OUT=A/'ACTIVE_AUTHORING_CHECKPOINT_DEFENSE_CASEBOOK_97.json';CHECK=A/'ACTIVE_AUTHORING_CHECKPOINT_DEFENSE_CASEBOOK_97_CHECK.json';COVER=A/'FEAT335_ORIGINAL_CASEBOOK_REVIEW_COVERAGE_97.json';BACK=A/'navigation-before-defense-casebook-97';SAVED=A/Path(__file__).name
for p in [OUT,CHECK,COVER,BACK,SAVED]:assert not p.exists(),str(p)
def j(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def enc(v):return (json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode()
def info(p):return planned(p,p.read_bytes())
def planned(p,b):return {'path':p.relative_to(G).as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def put(p,b):
 with p.open('xb') as f:f.write(b)
checks=[]
def ck(n,ok):checks.append({'check':n,'pass':bool(ok)});assert ok,n
prior=j(PRE);cp=deepcopy(prior)
ck('Exact checkpoint96',info(PRE)['sha256']=='5ab37b1b01c62c3b24b4480840396f55a65a4d19ae9e2a3682a793b06360cef5')
for row in [prior['currentAuthoredIndex'],prior['currentAcceptedInterfaceRegistry'],prior['currentWorkQueue'],*prior['canonicalHelperBaselinesUnchanged']]:ck('Protected baseline '+row['path'],info(G/row['path'])==row)
rp=A/'FEAT335_DEFENSE_ORIGINAL_CASEBOOK_REVIEW_97.json';r=j(rp);archive=A/'DD_Feat335_Defense_Casebook_Review_97.zip'
ck('Exact full defense report',info(rp)['sha256']=='f37559bdc9bdf082034db5775ba91e1a3c6de99e7d9981965a900aebef3e8e2b')
ck('Exact full defense archive',info(archive)['sha256']=='ad9bc5f49bec12e734be09703226194d2c7736b0ee5af08fd2f6460235192dfc')
ck('282 successful source/arithmetic checks',r['passed']==282 and r['failed']==0 and all(x['pass'] for x in r['checks']))
ck('31 full procedures62 original cases4 boundaries',len(r['completeSelectedRecords'])==31 and len(r['originalCaseReviews'])==62 and len(r['additionalBoundaryReviews'])==4)
ck('42 bounded calculations agree',len(r['numericAndStateCalculations'])==42 and all(x['calculatedResult']==x['expectedResult'] for x in r['numericAndStateCalculations']))
for row in r['sourceBindings']:ck('Full source unchanged '+row['path'],info(G/row['path'])==row)
ck('No runtime canonical or parent promotion',not r['parent335Accepted'] and not r['canonicalApplied'] and r['runtimeTestsExecuted']==0)
old=j(OLD);coverage=deepcopy(old)
ck('Exact previous casebook register95',info(OLD)['sha256']=='dd20edf87f6ad527787a243864cf68d233d5db0bcac435abb52b52ac353fe006')
new_reviews={x['id']:n for n,x in enumerate(r['originalCaseReviews'])};new_fa={x['id']:n for n,x in enumerate(r['additionalBoundaryReviews'])}
old_reviewed={x['id'] for x in old['ordinary']['positions'] if x['reviewedByThisFullCaseRegister']};old_fa={x['id'] for x in old['additional']['positions'] if x['reviewedByThisFullCaseRegister']}
ck('62 new original positions do not duplicate166',len(new_reviews)==62 and len(old_reviewed)==166 and not set(new_reviews)&old_reviewed)
ck('4 new boundaries do not duplicate6',len(new_fa)==4 and len(old_fa)==6 and not set(new_fa)&old_fa)
coverage['id']='FEAT335-ORIGINAL-CASEBOOK-REVIEW-COVERAGE-97';coverage['recordedAtUtc']=datetime.now(timezone.utc).isoformat();coverage['previousRegister']=info(OLD)
coverage['basis']='Cumulative full original-position authored semantic reviews: general_exploration93, skill94, crafting95 and general_defense97. Preparation96 notes and earlier targeted diagnostics are not independently double-counted.'
coverage['reviewReports']=[*old['reviewReports'],info(rp)]
for row in coverage['ordinary']['positions']:
 if row['id'] in new_reviews:row.update(reviewedByThisFullCaseRegister=True,reviewEvidencePointer='/originalCaseReviews/'+str(new_reviews[row['id']]),reviewEvidenceReport=info(rp),status='COMPLETE_STATED_CASE_SEMANTIC_REVIEW')
for row in coverage['additional']['positions']:
 if row['id'] in new_fa:row.update(reviewedByThisFullCaseRegister=True,reviewEvidencePointer='/additionalBoundaryReviews/'+str(new_fa[row['id']]),reviewEvidenceReport=info(rp),status='COMPLETE_STATED_CASE_SEMANTIC_REVIEW')
coverage['ordinary']['reviewed']=228;coverage['ordinary']['outsideCurrentFullCaseReview']=432;coverage['additional']['reviewed']=10;coverage['additional']['outsideCurrentFullBoundaryReview']=18
coverage['completedCohorts']=[*old['completedCohorts'],'general_defense']
ck('All660 original positions with228 exact review links',len(coverage['ordinary']['positions'])==660 and sum(x['reviewedByThisFullCaseRegister'] for x in coverage['ordinary']['positions'])==228)
ck('All28 boundaries with10 exact review links',len(coverage['additional']['positions'])==28 and sum(x['reviewedByThisFullCaseRegister'] for x in coverage['additional']['positions'])==10)
ck('Original identities and source pointers preserved',all(all(new[k]==before[k] for k in ['id','featId','cohort','originalSourcePointer']) for before,new in zip(old['ordinary']['positions'],coverage['ordinary']['positions'])))
ck('Earlier ordinary evidence untouched',all(before==new for before,new in zip(old['ordinary']['positions'],coverage['ordinary']['positions']) if before['id'] not in new_reviews))
ck('Earlier boundary evidence untouched',all(before==new for before,new in zip(old['additional']['positions'],coverage['additional']['positions']) if before['id'] not in new_fa))
coverage_bytes=enc(coverage);obs=A/'GPT_BESTIARY_REPLACEMENT_ACTIVE_OBSERVATION_97.txt';native=A/'GPT_NOTEBOOK_STATUS_97.json'
ck('Bestiary replacement still actively generating','button "Stop"' in obs.read_text(encoding='utf-8'))
n=j(native);unity=json.loads(n['unity']['value']['content'][0]['text']);part5=json.loads(n['part5']['value']['content'][0]['text'])
ck('Actual Return02 request remains latest',part5['turns'][0]['id']=='09fd693b-be2d-4274-bc1e-57ac20f4b422')
ck('Unity latest completed directions unchanged',unity['turns'][0]['id']=='41d5797f-d115-4cce-90fd-8ccc835b86cb' and any(x.get('id')=='b0572b7f-e15c-4d11-8353-86853e0329c6' for x in unity['turns'][0]['items']))
cp['id']='ACTIVE-AUTHORING-DEFENSE-CASEBOOK-97';cp['recordedAtUtc']=datetime.now(timezone.utc).isoformat();cp['previousCheckpoint']=info(PRE)
cp['status']='Progress:31 full defense procedures,62 original cases and4 FA boundaries reviewed with42 bounded calculations and282 checks. Cumulative228/660 ordinary and10/28 additional positions. GPT replacement BestiaryReturn02 remains actively generating; Unity directions unchanged. No canonical integration.'
cp['previousGoalTurnClassification']={'turn':96,'classification':'progress','evidence':prior['bestiaryReplacementDispatch96']}
cp['featDefenseCasebook97']={'report':info(rp),'archive':info(archive),'coverageRegister':planned(COVER,coverage_bytes),'coverage':r['coverage'],'cumulativeOriginalPositionsReviewed':228,'remainingOriginalPositionsInRegister':432,'cumulativeAdditionalBoundariesReviewed':10,'remainingAdditionalBoundariesInRegister':18,'checks':282,'failed':0,'fullSourceFiles':22,'archiveMembers':26,'findings':r['reviewFindings'],'remainingScope':r['remainingScope'],'actuallySentToGpt':False,'canonicalApplied':False,'parent335Accepted':False,'runtimeTestsExecuted':0}
cp['featDefensePreparation96']['completion97']={'report':info(rp),'qualification':'Original notes retained unchanged; only completed full97 source/mirror/calculation review is counted in cumulative register.'}
cp['previousGptObservationBefore97']=deepcopy(prior['activeGptReviewAtLastVerifiedObservation'])
cp['activeGptReviewAtLastVerifiedObservation']['latestObservation97']=info(obs);cp['activeGptReviewAtLastVerifiedObservation']['latestNativeRecord97']=info(native)
cp['activeGptReviewAtLastVerifiedObservation']['latestObservedStatus']='Return02 still active with browser Stop. Interim text proposes79 traits and PressureWaveDC15/3d8force; these are unfinished GPT observations pending exact source comparison and final artifacts, not acceptance. Do not interrupt active response. Lost Return01 remains undelivered/unverified.'
cp['bestiaryReplacementDispatch96']['latestObservation97']=info(obs)
cp['pertinentNotebookRecheck97']={'nativeRecord':info(native),'browserRecord':info(obs),'part5ActualUser':'09fd693b-be2d-4274-bc1e-57ac20f4b422','part5NewCompletedReturn':False,'unityLatestCompletedAssistant':'b0572b7f-e15c-4d11-8353-86853e0329c6','unityNewCompletedDecision':False,'newMessagesSent':0}
cp['nextAction']='Continue full original feat casebook review, next combat cohort47 procedures/94 original positions, while GPT finishes BestiaryReturn02.432 originals and18 boundaries remain. On actual completion immediately preserve full response and download full artifacts; compare independent counts/source/native mechanics and inspect claimed PressureWave/trait corrections, not prior lost Return01 hashes. Defense mental predicate is source-resolved but final assembly must carry its full definition.93/94/95/97 full casebook packets remain local unsent; communicate substantive issues at next actual conference without interrupting generation. Parent335/canonical integration remains reserved.'
cp['lastUsageObservation']={'usedPercent':59,'remainingPercent':41,'resetsAt':1793110625,'stopAtRemainingPercent':20,'source':'Fresh get_usage_limits97 saved with native status'}
cp['laterLocalWork']='Checkpoints73–97 remain local after last separately verified GitHub backup through72; no push in97.'
nav=[G/'START_HERE.md',R/'docs/DEVELOPMENT_DIRECTION.md',G/'REVIEW_MAP.html'];old_nav={};prepared={}
for p in nav:
 row=next(x for x in prior['navigation'] if x['path']==p.relative_to(G).as_posix());ck('Exact prior navigation '+p.name,info(p)==row);raw=old_nav[p]=p.read_bytes()
 if p.suffix=='.html':
  pos=raw.find(b'>',raw.find(b'<body'))+1;note=('<aside><p><strong>Checkpoint97:</strong> Defense review adds31 full procedures,62 original cases and4 boundaries, with42 bounded calculations. Cumulative228/660 originals and10/28 boundaries. Parent335 pending. <a href="docs/audit/2026-10-08/full-game/'+OUT.name+'">Current record</a>. GPT BestiaryReturn02 still active; interim corrections are unverified.</p></aside>\n').encode()
 else:
  pos=raw.find(b'\n')+1;prefix='docs/audit/2026-10-08/full-game/' if p.name=='START_HERE.md' else '../../../docs/audit/2026-10-08/full-game/';note=('\n**Current checkpoint — defense casebook:** [Checkpoint97]('+prefix+OUT.name+') records31 full defense procedures,62 original cases and4 additional boundaries, with42 bounded calculations and282 checks. Cumulative full-case coverage228/660 plus10/28 boundaries. Parent335 and runtime remain pending. The finite mental predicate is preserved from its exact original source and must remain explicit in final assembly. GPT BestiaryReturn02 is still generating; interim trait/Pressure Wave comments are not independently accepted.\n').encode()
 ck('Valid insertion '+p.name,pos>0);new=raw[:pos]+note+raw[pos:];ck('All prior navigation bytes preserved '+p.name,new[:pos]+new[pos+len(note):]==raw);prepared[p]=new
cp['navigation']=[planned(p,prepared[p]) for p in nav];cp['preservedNavigation']=[planned(BACK/p.name,old_nav[p]) for p in nav]
ck('All prior checkpoint fields retained',set(prior).issubset(cp));ck('No spell-count approval or application change',cp['acceptedButUnapplied']==53 and cp['authoredCounts']==prior['authoredCounts'] and not cp['implementationApplied'])
payload=enc(cp);script=Path(__file__).read_bytes();validation=enc({'id':'CHECKPOINT97-VALIDATION','checkpoint':planned(OUT,payload),'checks':checks,'passed':len(checks),'failed':0,'script':planned(SAVED,script),'anyNewGptMessageSent':False})
BACK.mkdir()
for p in nav:put(BACK/p.name,old_nav[p]);p.write_bytes(prepared[p])
for p,b in [(SAVED,script),(COVER,coverage_bytes),(OUT,payload),(CHECK,validation)]:put(p,b)
print(json.dumps({'checkpoint':info(OUT),'check':info(CHECK),'coverage':info(COVER),'passed':len(checks),'failed':0},indent=2))
