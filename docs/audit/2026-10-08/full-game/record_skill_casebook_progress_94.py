"""One-shot checkpoint and cumulative full-position casebook coverage."""
from pathlib import Path
from copy import deepcopy
from datetime import datetime,timezone
import json,hashlib
G=Path(r'C:\Github\DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game'
PRE=A/'ACTIVE_AUTHORING_CHECKPOINT_EXPLORATION_CASEBOOK_93.json';OLD_COVER=A/'FEAT335_ORIGINAL_CASEBOOK_REVIEW_COVERAGE_93.json'
OUT=A/'ACTIVE_AUTHORING_CHECKPOINT_SKILL_CASEBOOK_94.json';CHECK=A/'ACTIVE_AUTHORING_CHECKPOINT_SKILL_CASEBOOK_94_CHECK.json';COVER=A/'FEAT335_ORIGINAL_CASEBOOK_REVIEW_COVERAGE_94.json';BACKUP=A/'navigation-before-skill-casebook-94';SAVED=A/Path(__file__).name
for p in (OUT,CHECK,COVER,BACKUP,SAVED):assert not p.exists(),str(p)
def j(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def enc(v):return (json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode()
def info(p):
 b=p.read_bytes();return {'path':p.relative_to(G).as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def planned(p,b):return {'path':p.relative_to(G).as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def put(p,b):
 with p.open('xb') as f:f.write(b)
checks=[]
def ck(name,ok):checks.append({'check':name,'pass':bool(ok)});assert ok,name
prior=j(PRE);cp=deepcopy(prior)
ck('Checkpoint93 exact',info(PRE)['sha256']=='87b6e1081ad6928d69737146313aa23b59c89965d7e423ec14448f4c9cdabf51')
for row in [prior['currentAuthoredIndex'],prior['currentAcceptedInterfaceRegistry'],prior['currentWorkQueue'],*prior['canonicalHelperBaselinesUnchanged']]:ck('Protected canonical baseline '+row['path'],info(G/row['path'])==row)
rp=A/'FEAT335_SKILL_ORIGINAL_CASEBOOK_REVIEW_94.json';r=j(rp);archive=A/'DD_Feat335_Skill_Casebook_Review_94.zip'
ck('Exact full skill report',info(rp)['sha256']=='d04323633e550386598f866660ffa595cab0dd7cf16be3fe99bbb1228f5650cb')
ck('Exact complete skill archive',info(archive)['sha256']=='f786580c7229caa18c2c0b5cb9adac9eb6bcfe1ae942caa4f5a5ebbcf388cf2a')
ck('189 successful source/arithmetic checks',r['passed']==189 and r['failed']==0 and all(c['pass'] for c in r['checks']))
ck('25 full procedures and50 individually reviewed cases',len(r['completeSelectedRecords'])==25 and len(r['originalCaseReviews'])==50)
ck('34 bounded calculations correct',len(r['numericAndStateCalculations'])==34 and all(c['calculatedResult']==c['expectedResult'] for c in r['numericAndStateCalculations']))
for row in r['sourceBindings']:ck('Full reviewed source unchanged '+row['path'],info(G/row['path'])==row)
ck('No runtime or parent acceptance',not r['parent335Accepted'] and not r['canonicalApplied'] and r['runtimeTestsExecuted']==0)
old=j(OLD_COVER);coverage=deepcopy(old)
ck('Exact previous coverage register',info(OLD_COVER)['sha256']=='71b50921e75aededffc0e21ab626346daac49723783f961cb4db0a011d5bfa9b')
new_reviews={x['id']:n for n,x in enumerate(r['originalCaseReviews'])};old_reviewed={x['id'] for x in old['ordinary']['positions'] if x['reviewedByThisFullCaseRegister']}
ck('New50 positions do not duplicate prior68',len(new_reviews)==50 and len(old_reviewed)==68 and not set(new_reviews)&old_reviewed)
coverage['id']='FEAT335-ORIGINAL-CASEBOOK-REVIEW-COVERAGE-94';coverage['recordedAtUtc']=datetime.now(timezone.utc).isoformat();coverage['previousRegister']=info(OLD_COVER)
coverage['basis']='Cumulative full original-position semantic reviews for general_exploration93 and skill94. Older targeted/composition diagnostics remain separately preserved and do not automatically count as complete casebook review.'
coverage['reviewReports']=[old['reviewReport'],info(rp)]
for row in coverage['ordinary']['positions']:
 if row['id'] in old_reviewed:row['reviewEvidenceReport']=old['reviewReport']
 if row['id'] in new_reviews:
  row.update(reviewedByThisFullCaseRegister=True,reviewEvidencePointer='/originalCaseReviews/'+str(new_reviews[row['id']]),reviewEvidenceReport=info(rp),status='COMPLETE_STATED_CASE_SEMANTIC_REVIEW')
for row in coverage['additional']['positions']:
 if row['reviewedByThisFullCaseRegister']:row['reviewEvidenceReport']=old['reviewReport']
coverage['ordinary']['reviewed']=118;coverage['ordinary']['outsideCurrentFullCaseReview']=542
coverage['completedCohorts']=['general_exploration','skill']
ck('All660 original positions remain and118 have exact evidence',len(coverage['ordinary']['positions'])==660 and sum(x['reviewedByThisFullCaseRegister'] for x in coverage['ordinary']['positions'])==118)
ck('All28 boundaries remain with3 reviewed',len(coverage['additional']['positions'])==28 and sum(x['reviewedByThisFullCaseRegister'] for x in coverage['additional']['positions'])==3)
ck('Original identity/source-position fields preserved',all(all(new[k]==before[k] for k in ['id','featId','cohort','originalSourcePointer']) for before,new in zip(old['ordinary']['positions'],coverage['ordinary']['positions'])))
coverage_bytes=enc(coverage);obs=A/'GPT_BESTIARY_ACTIVE_OBSERVATION_94.txt';ck('Bestiary still actively generating','button "Stop"' in obs.read_text(encoding='utf-8'))
cp['id']='ACTIVE-AUTHORING-SKILL-CASEBOOK-94';cp['recordedAtUtc']=datetime.now(timezone.utc).isoformat();cp['previousCheckpoint']=info(PRE)
cp['status']='Progress: all25 skill-feat procedures and50 original examples reviewed, including exact accepted FT84 Spell Scribe successor, with34 bounded calculations and189 source/arithmetic checks. Cumulative full-case register now covers118/660 original positions and3/28 FA boundaries; no runtime or parent acceptance. Bestiary GPT response remains active.'
cp['previousGoalTurnClassification']={'turn':93,'classification':'progress','evidence':prior['featExplorationCasebook93']['report']}
cp['featSkillCasebook94']={'report':info(rp),'archive':info(archive),'coverageRegister':planned(COVER,coverage_bytes),'coverage':r['coverage'],'cumulativeOriginalPositionsReviewed':118,'remainingOriginalPositionsInRegister':542,'cumulativeAdditionalBoundariesReviewed':3,'remainingAdditionalBoundariesInRegister':25,'checks':189,'failed':0,'fullSourceFiles':len(r['sourceBindings']),'archiveMembers':26,'remainingScope':r['remainingScope'],'findings':r['reviewFindings'],'actuallySentToGpt':False,'canonicalApplied':False,'parent335Accepted':False,'runtimeTestsExecuted':0}
cp['previousGptObservationBefore94']=deepcopy(prior['activeGptReviewAtLastVerifiedObservation']);cp['activeGptReviewAtLastVerifiedObservation']['latestObservation94']=info(obs)
cp['activeGptReviewAtLastVerifiedObservation']['latestObservedStatus']='Browser Stop remains present while the existing Bestiary response is still thinking. No completed return observed or interrupted; no new message or upload.'
cp['bestiaryActualDispatch89']['latestObservation94']=info(obs)
cp['nextAction']='Continue the remaining full feat casebook cohorts against exact selected procedures; coverage94 leaves542 original positions and25 FA boundaries outside completed whole-position reviews. FT84 successors and copy-release preparation-only successors remain separate unapplied integration chains. On actual Bestiary completion, preserve/download/inspect its whole return before the prepared current Fishing/Cooking dependency supplement and Resonance acceptance acknowledgment are sent as needed. The exploration93 and skill94 full review packets are local and unsent.'
cp['lastUsageObservation']={'usedPercent':56,'remainingPercent':44,'resetsAt':1793110625,'stopAtRemainingPercent':20,'source':'Fresh get_usage_limits near checkpoint94'}
cp['laterLocalWork']='Checkpoints73–94 remain local after the last separately verified GitHub backup through72; no push in94.'
nav=[G/'START_HERE.md',R/'docs/DEVELOPMENT_DIRECTION.md',G/'REVIEW_MAP.html'];old_nav={};prepared={}
for p in nav:
 row=next(x for x in prior['navigation'] if x['path']==p.relative_to(G).as_posix());ck('Exact previous navigation '+p.name,info(p)==row);raw=old_nav[p]=p.read_bytes()
 if p.suffix=='.html':
  pos=raw.find(b'>',raw.find(b'<body'))+1;note=('<aside><p><strong>Checkpoint94:</strong> Full skill-feat review adds25 procedures and50 original examples. Cumulative full-case review118/660, plus3/28 FA boundaries; parent335 pending. <a href="docs/audit/2026-10-08/full-game/'+OUT.name+'">Current record</a>. GPT Bestiary response still active.</p></aside>\n').encode()
 else:
  pos=raw.find(b'\n')+1;prefix='docs/audit/2026-10-08/full-game/' if p.name=='START_HERE.md' else '../../../docs/audit/2026-10-08/full-game/';note=('\n**Current checkpoint — skill casebook:** [Checkpoint94]('+prefix+OUT.name+') records all25 skill-feat procedures and50 original cases, supported by34 bounded calculations. Cumulative full-case coverage is118/660 original positions and3/28 additional boundaries. Exact FT84 Spell Scribe wording is retained in the isolated review copy. Parent335 and runtime remain unapproved; GPT Bestiary generation is still active.\n').encode()
 ck('Valid insertion '+p.name,pos>0);new=raw[:pos]+note+raw[pos:];ck('All previous navigation bytes preserved '+p.name,new[:pos]+new[pos+len(note):]==raw);prepared[p]=new
cp['navigation']=[planned(p,prepared[p]) for p in nav];cp['preservedNavigation']=[planned(BACKUP/p.name,old_nav[p]) for p in nav]
ck('Every prior checkpoint field retained',set(prior).issubset(cp));ck('No ordinary-spell count or approval change',cp['acceptedButUnapplied']==53 and cp['authoredCounts']==prior['authoredCounts'] and not cp['implementationApplied'])
payload=enc(cp);script=Path(__file__).read_bytes();validation=enc({'id':'CHECKPOINT94-VALIDATION','checkpoint':planned(OUT,payload),'checks':checks,'passed':len(checks),'failed':0,'script':planned(SAVED,script),'anyNewGptMessageSent':False})
BACKUP.mkdir()
for p in nav:put(BACKUP/p.name,old_nav[p]);p.write_bytes(prepared[p])
put(SAVED,script);put(COVER,coverage_bytes);put(OUT,payload);put(CHECK,validation)
print(json.dumps({'checkpoint':info(OUT),'check':info(CHECK),'coverage':info(COVER),'passed':len(checks),'failed':0,'newGptMessageSent':False},indent=2))
