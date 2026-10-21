"""One-shot checkpoint and cumulative original-case evidence register."""
from pathlib import Path
from copy import deepcopy
from datetime import datetime,timezone
import json,hashlib
G=Path(r'C:\Github\DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game'
PRE=A/'ACTIVE_AUTHORING_CHECKPOINT_SKILL_CASEBOOK_94.json';OLD_COVER=A/'FEAT335_ORIGINAL_CASEBOOK_REVIEW_COVERAGE_94.json'
OUT=A/'ACTIVE_AUTHORING_CHECKPOINT_CRAFTING_CASEBOOK_95.json';CHECK=A/'ACTIVE_AUTHORING_CHECKPOINT_CRAFTING_CASEBOOK_95_CHECK.json';COVER=A/'FEAT335_ORIGINAL_CASEBOOK_REVIEW_COVERAGE_95.json';BACKUP=A/'navigation-before-crafting-casebook-95';SAVED=A/Path(__file__).name
for p in (OUT,CHECK,COVER,BACKUP,SAVED):assert not p.exists(),str(p)
def j(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def enc(v):return (json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode()
def info(p):
 b=p.read_bytes();return {'path':p.relative_to(G).as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def planned(p,b):return {'path':p.relative_to(G).as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def put(p,b):
 with p.open('xb') as f:f.write(b)
checks=[]
def ck(n,ok):checks.append({'check':n,'pass':bool(ok)});assert ok,n
prior=j(PRE);cp=deepcopy(prior)
ck('Checkpoint94 exact',info(PRE)['sha256']=='b15d6d3d69d4d8c134e685ec19ce1430531ef9d7d779a5b2feaea58b1cf686a9')
for row in [prior['currentAuthoredIndex'],prior['currentAcceptedInterfaceRegistry'],prior['currentWorkQueue'],*prior['canonicalHelperBaselinesUnchanged']]:ck('Protected baseline '+row['path'],info(G/row['path'])==row)
rp=A/'FEAT335_CRAFTING_ORIGINAL_CASEBOOK_REVIEW_95.json';r=j(rp);archive=A/'DD_Feat335_Crafting_Casebook_Review_95.zip'
ck('Exact full crafting report',info(rp)['sha256']=='65458b39b5063a76a3171ae7625604081737e6c4c33e41184c02ee7c5692a0b3')
ck('Exact full crafting archive',info(archive)['sha256']=='5a91a5d589d28112337621e9097c77ae4b82f2434c36989cd6033a46d1ae2222')
ck('192 successful source/arithmetic checks',r['passed']==192 and r['failed']==0 and all(x['pass'] for x in r['checks']))
ck('24 full procedures48 original cases3 boundaries',len(r['completeSelectedRecords'])==24 and len(r['originalCaseReviews'])==48 and len(r['additionalBoundaryReviews'])==3)
ck('40 bounded calculations agree',len(r['numericAndStateCalculations'])==40 and all(x['calculatedResult']==x['expectedResult'] for x in r['numericAndStateCalculations']))
for row in r['sourceBindings']:ck('Full source unchanged '+row['path'],info(G/row['path'])==row)
ck('No runtime canonical or parent promotion',not r['parent335Accepted'] and not r['canonicalApplied'] and r['runtimeTestsExecuted']==0)
old=j(OLD_COVER);coverage=deepcopy(old)
ck('Exact previous register',info(OLD_COVER)['sha256']=='e3c8b9091f434a693a9fb3e6a3cdd7c53c431faa3af2136bf2453e58032fe90c')
new_reviews={x['id']:n for n,x in enumerate(r['originalCaseReviews'])};new_fa={x['id']:n for n,x in enumerate(r['additionalBoundaryReviews'])};old_reviewed={x['id'] for x in old['ordinary']['positions'] if x['reviewedByThisFullCaseRegister']};old_fa={x['id'] for x in old['additional']['positions'] if x['reviewedByThisFullCaseRegister']}
ck('48 new original positions do not duplicate previous118',len(new_reviews)==48 and len(old_reviewed)==118 and not set(new_reviews)&old_reviewed)
ck('3 new boundaries do not duplicate previous3',len(new_fa)==3 and len(old_fa)==3 and not set(new_fa)&old_fa)
coverage['id']='FEAT335-ORIGINAL-CASEBOOK-REVIEW-COVERAGE-95';coverage['recordedAtUtc']=datetime.now(timezone.utc).isoformat();coverage['previousRegister']=info(OLD_COVER)
coverage['basis']='Cumulative full original-position authored semantic reviews: general_exploration93, skill94 and crafting95. Earlier targeted/composition diagnostics remain separate and are not automatically counted as full original-case review.'
coverage['reviewReports']=[*old['reviewReports'],info(rp)]
for row in coverage['ordinary']['positions']:
 if row['id'] in new_reviews:row.update(reviewedByThisFullCaseRegister=True,reviewEvidencePointer='/originalCaseReviews/'+str(new_reviews[row['id']]),reviewEvidenceReport=info(rp),status='COMPLETE_STATED_CASE_SEMANTIC_REVIEW')
for row in coverage['additional']['positions']:
 if row['id'] in new_fa:row.update(reviewedByThisFullCaseRegister=True,reviewEvidencePointer='/additionalBoundaryReviews/'+str(new_fa[row['id']]),reviewEvidenceReport=info(rp),status='COMPLETE_STATED_CASE_SEMANTIC_REVIEW')
coverage['ordinary']['reviewed']=166;coverage['ordinary']['outsideCurrentFullCaseReview']=494
coverage['additional']['reviewed']=6;coverage['additional']['outsideCurrentFullBoundaryReview']=22
coverage['completedCohorts']=['general_exploration','skill','crafting']
ck('All660 originals retained with166 exact review links',len(coverage['ordinary']['positions'])==660 and sum(x['reviewedByThisFullCaseRegister'] for x in coverage['ordinary']['positions'])==166)
ck('All28 boundaries retained with6 exact review links',len(coverage['additional']['positions'])==28 and sum(x['reviewedByThisFullCaseRegister'] for x in coverage['additional']['positions'])==6)
ck('Original identity and source pointers preserved',all(all(new[k]==before[k] for k in ['id','featId','cohort','originalSourcePointer']) for before,new in zip(old['ordinary']['positions'],coverage['ordinary']['positions'])))
ck('Earlier original-case evidence untouched',all(before==new for before,new in zip(old['ordinary']['positions'],coverage['ordinary']['positions']) if before['id'] not in new_reviews))
ck('Earlier boundary evidence untouched',all(before==new for before,new in zip(old['additional']['positions'],coverage['additional']['positions']) if before['id'] not in new_fa))
coverage_bytes=enc(coverage);obs=A/'GPT_BESTIARY_ACTIVE_OBSERVATION_95.txt';ck('Bestiary remains actively generating','button "Stop"' in obs.read_text(encoding='utf-8'))
cp['id']='ACTIVE-AUTHORING-CRAFTING-CASEBOOK-95';cp['recordedAtUtc']=datetime.now(timezone.utc).isoformat();cp['previousCheckpoint']=info(PRE)
cp['status']='Progress:24 full crafting-feat procedures,48 original examples and3 FA boundaries reviewed with40 bounded calculations and192 checks. Cumulative full-case coverage166/660 original positions and6/28 boundaries. GPT Bestiary still active; Unity latest completed decision unchanged. Canonical integration remains reserved.'
cp['previousGoalTurnClassification']={'turn':94,'classification':'progress','evidence':prior['featSkillCasebook94']['report']}
cp['featCraftingCasebook95']={'report':info(rp),'archive':info(archive),'coverageRegister':planned(COVER,coverage_bytes),'coverage':r['coverage'],'cumulativeOriginalPositionsReviewed':166,'remainingOriginalPositionsInRegister':494,'cumulativeAdditionalBoundariesReviewed':6,'remainingAdditionalBoundariesInRegister':22,'checks':192,'failed':0,'fullSourceFiles':len(r['sourceBindings']),'archiveMembers':31,'findings':r['reviewFindings'],'remainingScope':r['remainingScope'],'actuallySentToGpt':False,'canonicalApplied':False,'parent335Accepted':False,'runtimeTestsExecuted':0}
cp['previousGptObservationBefore95']=deepcopy(prior['activeGptReviewAtLastVerifiedObservation']);cp['activeGptReviewAtLastVerifiedObservation']['latestObservation95']=info(obs)
cp['activeGptReviewAtLastVerifiedObservation']['latestObservedStatus']='Browser Stop and active-thinking notice remain. Native Part5 latest user is5395ae3e-01ef-4b42-bae4-9c17af13f3fb with no completed Bestiary reply; latest completed assistant83cafb84-ba74-462c-ac6e-0b45563d11d5 remains the previously accepted Resonance follow-through. No interruption, send or upload.'
cp['bestiaryActualDispatch89']['latestObservation95']=info(obs)
cp['pertinentNotebookRecheck95']={'part5':{'threadId':'6ad4a867-f330-83e9-829e-bf2bb41a6c09','title':'Calibration Review Part 5','latestUser':'5395ae3e-01ef-4b42-bae4-9c17af13f3fb','latestCompletedAssistant':'83cafb84-ba74-462c-ac6e-0b45563d11d5','activeBrowserObservation':info(obs),'newCompletedDecisionObserved':False},'unity':{'threadId':'6ad64114-2364-83e9-8764-bc55988b0479','title':'Unity Development Setup','latestUser':'41d5797f-d115-4cce-90fd-8ccc835b86cb','latestCompletedAssistant':'b0572b7f-e15c-4d11-8353-86853e0329c6','newCompletedDecisionObserved':False},'method':'Fresh native read_thread for both notebooks plus current browser DOM confirmation of active Part5 response.'}
cp['nextAction']='Continue full original feat casebook review, next general_defense31 feats/62 positions, preserving source-specific controls and earlier holds; current register leaves494 original positions and22 FA boundaries. On actual Bestiary completion preserve/download/read its full return before adapting and sending the prepared91 full linked Fishing/Cooking dependency supplement and Resonance acceptance acknowledgment as needed. Exploration93, skill94 and crafting95 packets remain local and unsent. Keep FT84-derived and copy-release preparation-only successor chains separate pending full parent335 exact review.'
cp['lastUsageObservation']={'usedPercent':56,'remainingPercent':44,'resetsAt':1793110625,'stopAtRemainingPercent':20,'source':'Fresh get_usage_limits at start95'}
cp['laterLocalWork']='Checkpoints73–95 remain local after last separately verified GitHub backup through72; no push in95.'
nav=[G/'START_HERE.md',R/'docs/DEVELOPMENT_DIRECTION.md',G/'REVIEW_MAP.html'];old_nav={};prepared={}
for p in nav:
 row=next(x for x in prior['navigation'] if x['path']==p.relative_to(G).as_posix());ck('Exact previous navigation '+p.name,info(p)==row);raw=old_nav[p]=p.read_bytes()
 if p.suffix=='.html':
  pos=raw.find(b'>',raw.find(b'<body'))+1;note=('<aside><p><strong>Checkpoint95:</strong> Crafting review adds24 full procedures,48 original cases and3 boundary cases; cumulative full-case review166/660 plus6/28 boundaries. Parent335 pending. <a href="docs/audit/2026-10-08/full-game/'+OUT.name+'">Current record</a>. GPT Bestiary remains active.</p></aside>\n').encode()
 else:
  pos=raw.find(b'\n')+1;prefix='docs/audit/2026-10-08/full-game/' if p.name=='START_HERE.md' else '../../../docs/audit/2026-10-08/full-game/';note=('\n**Current checkpoint — crafting casebook:** [Checkpoint95]('+prefix+OUT.name+') records24 full crafting procedures,48 original cases and3 additional boundaries, with40 bounded calculations. Cumulative full-case coverage166/660 and6/28 boundaries. Accepted FT84 successors remain in the isolated review copy; parent335 and runtime remain unapproved. GPT Bestiary is still active; Unity notebook latest decision is unchanged.\n').encode()
 ck('Valid insertion '+p.name,pos>0);new=raw[:pos]+note+raw[pos:];ck('All prior navigation bytes retained '+p.name,new[:pos]+new[pos+len(note):]==raw);prepared[p]=new
cp['navigation']=[planned(p,prepared[p]) for p in nav];cp['preservedNavigation']=[planned(BACKUP/p.name,old_nav[p]) for p in nav]
ck('Every earlier checkpoint field retained',set(prior).issubset(cp));ck('No spell-count or approval change',cp['acceptedButUnapplied']==53 and cp['authoredCounts']==prior['authoredCounts'] and not cp['implementationApplied'])
payload=enc(cp);script=Path(__file__).read_bytes();validation=enc({'id':'CHECKPOINT95-VALIDATION','checkpoint':planned(OUT,payload),'checks':checks,'passed':len(checks),'failed':0,'script':planned(SAVED,script),'anyNewGptMessageSent':False})
BACKUP.mkdir()
for p in nav:put(BACKUP/p.name,old_nav[p]);p.write_bytes(prepared[p])
put(SAVED,script);put(COVER,coverage_bytes);put(OUT,payload);put(CHECK,validation)
print(json.dumps({'checkpoint':info(OUT),'check':info(CHECK),'coverage':info(COVER),'passed':len(checks),'failed':0,'newGptMessageSent':False},indent=2))
