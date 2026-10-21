"""One-shot checkpoint and finite original-case review coverage register."""
from pathlib import Path
from copy import deepcopy
from collections import Counter
from datetime import datetime,timezone
import json,hashlib

G=Path(r'C:\Github\DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game'
PRE=A/'ACTIVE_AUTHORING_CHECKPOINT_FEAT_DERIVED_MIRRORS_92.json'
OUT=A/'ACTIVE_AUTHORING_CHECKPOINT_EXPLORATION_CASEBOOK_93.json';CHECK=A/'ACTIVE_AUTHORING_CHECKPOINT_EXPLORATION_CASEBOOK_93_CHECK.json'
COVER=A/'FEAT335_ORIGINAL_CASEBOOK_REVIEW_COVERAGE_93.json';BACKUP=A/'navigation-before-exploration-casebook-93';SAVED=A/Path(__file__).name
for p in (OUT,CHECK,COVER,BACKUP,SAVED):assert not p.exists(),str(p)
def j(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def enc(v):return (json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode()
def sha(b):return hashlib.sha256(b).hexdigest()
def info(p):
 b=p.read_bytes();return {'path':p.relative_to(G).as_posix(),'bytes':len(b),'sha256':sha(b)}
def planned(p,b):return {'path':p.relative_to(G).as_posix(),'bytes':len(b),'sha256':sha(b)}
def put(p,b):
 with p.open('xb') as f:f.write(b)
checks=[]
def ck(name,ok):checks.append({'check':name,'pass':bool(ok)});assert ok,name
prior=j(PRE);cp=deepcopy(prior)
ck('Checkpoint92 exact',info(PRE)['sha256']=='91210d4dbdea8e9199ceff172d91f0c52a387a183ed87e28d60b7c521bb4f8e8')
for row in [prior['currentAuthoredIndex'],prior['currentAcceptedInterfaceRegistry'],prior['currentWorkQueue'],*prior['canonicalHelperBaselinesUnchanged']]:ck('Protected canonical baseline '+row['path'],info(G/row['path'])==row)
rp=A/'FEAT335_EXPLORATION_ORIGINAL_CASEBOOK_REVIEW_93.json';report=j(rp)
ck('Exact full original-case review report',info(rp)['sha256']=='ac2f12df49630b64e6cef4ca5b163c669e911338259508223a7c5eca6933a92c')
ck('All268 source/numeric checks passed',report['passed']==268 and report['failed']==0 and all(x['pass'] for x in report['checks']))
ck('68 complete original cases and3 boundary reviews',len(report['originalCaseReviews'])==68 and len(report['additionalBoundaryReviews'])==3)
ck('35 bounded projections with actual matching results',len(report['numericAndStateCalculations'])==35 and all(x['calculatedResult']==x['expectedResult'] for x in report['numericAndStateCalculations']))
for row in report['sourceBindings']:ck('Reviewed source unchanged '+row['path'],info(G/row['path'])==row)
case_path=R/'data/director/feat_candidates/exact_01/example_dispositions.json';fa_path=R/'data/director/feat_candidates/exact_01/additional_boundary_expectations.json';candidate_path=R/'data/director/feat_candidates/exact_01/candidate.json'
cases=j(case_path)['cases'];fa=j(fa_path)['cases'];records={x['id']:x for x in j(candidate_path)['records']}
reviewed={x['id']:n for n,x in enumerate(report['originalCaseReviews'])};reviewed_fa={x['id']:n for n,x in enumerate(report['additionalBoundaryReviews'])}
rows=[]
for x in cases:
 rows.append({'id':x['id'],'featId':x['featId'],'cohort':records[x['featId']]['cohort'],'originalSourcePointer':x['sourcePointer'],'reviewedByThisFullCaseRegister':x['id'] in reviewed,'reviewEvidencePointer':'/originalCaseReviews/'+str(reviewed[x['id']]) if x['id'] in reviewed else None,'status':'COMPLETE_STATED_CASE_SEMANTIC_REVIEW' if x['id'] in reviewed else 'OUTSIDE_THIS_REGISTER_REVIEW_NOT_YET_RECORDED'})
fa_rows=[{'id':x['id'],'featId':x['featId'],'reviewedByThisFullCaseRegister':x['id'] in reviewed_fa,'reviewEvidencePointer':'/additionalBoundaryReviews/'+str(reviewed_fa[x['id']]) if x['id'] in reviewed_fa else None,'status':'COMPLETE_STATED_BOUNDARY_SEMANTIC_REVIEW' if x['id'] in reviewed_fa else 'OUTSIDE_THIS_REGISTER_REVIEW_NOT_YET_RECORDED'} for x in fa]
ck('Full660 case identities retained once',len(rows)==len({x['id'] for x in rows})==660)
ck('Full28 FA identities retained once',len(fa_rows)==len({x['id'] for x in fa_rows})==28)
ck('All exact reviewed cases linked to the actual source',set(reviewed).issubset({x['id'] for x in cases}) and all(x['completeOriginalDisposition']==next(c for c in cases if c['id']==x['id']) for x in report['originalCaseReviews']))
coverage={'id':'FEAT335-ORIGINAL-CASEBOOK-REVIEW-COVERAGE-93','recordedAtUtc':datetime.now(timezone.utc).isoformat(),'basis':'This new finite register tracks full original-position semantic reviews, starting with the complete general_exploration cohort93. Older targeted/composition diagnostics remain separate evidence and are neither erased nor automatically counted as full-casebook reviews.','reviewReport':info(rp),'originalCasebook':info(case_path),'additionalBoundaryCasebook':info(fa_path),'fullCandidate':info(candidate_path),'ordinary':{'total':660,'reviewed':68,'outsideCurrentFullCaseReview':592,'byCohort':dict(Counter(x['cohort'] for x in rows)),'positions':rows},'additional':{'total':28,'reviewed':3,'outsideCurrentFullBoundaryReview':25,'positions':fa_rows},'qualification':'These are authored semantic review positions, not runtime tests, whole-feature acceptance, numerical balance or a whole-game completion percentage. All actual world/actor/provider premises retain their stated qualifications.','canonicalApplied':False,'parent335Accepted':False}
coverage_bytes=enc(coverage)
obs=A/'GPT_BESTIARY_ACTIVE_OBSERVATION_93.txt';ck('Live Bestiary observed active','button "Stop"' in obs.read_text(encoding='utf-8'))
cp['id']='ACTIVE-AUTHORING-EXPLORATION-CASEBOOK-93';cp['recordedAtUtc']=datetime.now(timezone.utc).isoformat();cp['previousCheckpoint']=info(PRE)
cp['status']='Progress: full authored semantic review of31 general-exploration feat procedures,68 original example positions and3 FA boundaries;35 separate bounded reference calculations and268 successful source/arithmetic checks. A complete660+28 coverage register preserves every remaining position. GPT Bestiary response still active.'
cp['previousGoalTurnClassification']={'turn':92,'classification':'progress','evidence':prior['featDerivedMirrors92']['report']}
cp['featExplorationCasebook93']={'report':info(rp),'archive':info(A/'DD_Feat335_Exploration_Casebook_Review_93.zip'),'coverageRegister':planned(COVER,coverage_bytes),'coverage':report['coverage'],'checks':268,'failed':0,'fullSourceFiles':len(report['sourceBindings']),'archiveMembers':19,'remainingScope':report['remainingScope'],'findings':report['reviewFindings'],'actuallySentToGpt':False,'canonicalApplied':False,'parent335Accepted':False,'runtimeTestsExecuted':0}
cp['previousGptObservationBefore93']=deepcopy(prior['activeGptReviewAtLastVerifiedObservation'])
cp['activeGptReviewAtLastVerifiedObservation']['latestObservation93']=info(obs)
cp['activeGptReviewAtLastVerifiedObservation']['latestObservedStatus']='Browser Stop remains present. Latest native completed-history read still ends at the same actual Bestiary request5395ae3e-01ef-4b42-bae4-9c17af13f3fb with no assistant final. No interruption, upload or new send.'
cp['bestiaryActualDispatch89']['latestObservation93']=info(obs)
cp['nextAction']='Continue full original-casebook review in another feat cohort using the finite coverage register93:592 original positions and25 FA boundaries remain outside its completed scope. Keep earlier composition evidence and exact FT84/copy successors distinct. When the existing Bestiary response finishes, preserve/download/inspect the full return, then send the prepared missing Fishing/Cooking dependency supplement and Resonance acceptance acknowledgment as actually needed. The new exploration full packet remains local. No canonical integration.'
cp['lastUsageObservation']={'usedPercent':55,'remainingPercent':45,'resetsAt':1793110625,'stopAtRemainingPercent':20,'source':'Fresh get_usage_limits near checkpoint93'}
cp['laterLocalWork']='Checkpoints73–93 remain local after the last separately verified GitHub backup through72; no push in93.'
nav=[G/'START_HERE.md',R/'docs/DEVELOPMENT_DIRECTION.md',G/'REVIEW_MAP.html'];old={};prepared={}
for p in nav:
 row=next(x for x in prior['navigation'] if x['path']==p.relative_to(G).as_posix());ck('Exact previous navigation '+p.name,info(p)==row);raw=old[p]=p.read_bytes()
 if p.suffix=='.html':
  pos=raw.find(b'>',raw.find(b'<body'))+1
  note=('<aside><p><strong>Checkpoint93:</strong> Full exploration feat casebook review:31 procedures,68 original cases,3 FA boundaries and35 reference calculations. All660+28 positions preserved in the review register. <a href="docs/audit/2026-10-08/full-game/'+OUT.name+'">Current record</a>. Parent335 pending; GPT Bestiary response still active.</p></aside>\n').encode()
 else:
  pos=raw.find(b'\n')+1;prefix='docs/audit/2026-10-08/full-game/' if p.name=='START_HERE.md' else '../../../docs/audit/2026-10-08/full-game/'
  note=('\n**Current checkpoint — exploration casebook:** [Checkpoint93]('+prefix+OUT.name+') records full semantic review of31 feat procedures,68 original cases and3 additional boundaries, plus35 bounded reference calculations. The complete660+28 coverage register preserves all remaining positions. This is authored review, not runtime or parent335 acceptance. GPT Bestiary generation remains active; no canonical application or new send.\n').encode()
 ck('Valid insertion '+p.name,pos>0);new=raw[:pos]+note+raw[pos:];ck('Full prior navigation preserved '+p.name,new[:pos]+new[pos+len(note):]==raw);prepared[p]=new
cp['navigation']=[planned(p,prepared[p]) for p in nav];cp['preservedNavigation']=[planned(BACKUP/p.name,old[p]) for p in nav]
ck('Every prior checkpoint field retained',set(prior).issubset(cp))
ck('No ordinary spell count or approval change',cp['acceptedButUnapplied']==53 and cp['authoredCounts']==prior['authoredCounts'] and not cp['implementationApplied'])
payload=enc(cp);script=Path(__file__).read_bytes();validation=enc({'id':'CHECKPOINT93-VALIDATION','checkpoint':planned(OUT,payload),'checks':checks,'passed':len(checks),'failed':0,'script':planned(SAVED,script),'anyNewGptMessageSent':False})
BACKUP.mkdir()
for p in nav:put(BACKUP/p.name,old[p]);p.write_bytes(prepared[p])
put(SAVED,script);put(COVER,coverage_bytes);put(OUT,payload);put(CHECK,validation)
print(json.dumps({'checkpoint':info(OUT),'check':info(CHECK),'coverage':info(COVER),'passed':len(checks),'failed':0,'newGptMessageSent':False},indent=2))
