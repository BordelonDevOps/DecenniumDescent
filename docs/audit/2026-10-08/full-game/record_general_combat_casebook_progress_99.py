"""One-shot cumulative general combat checkpoint; preserves all earlier evidence."""
from pathlib import Path
from copy import deepcopy
from datetime import datetime,timezone
import json,hashlib
G=Path(r'C:\Github\DecenniumDescent'); R=G/'DescentReviewChanges/ReviewBible'; A=G/'docs/audit/2026-10-08/full-game'
PRE=A/'ACTIVE_AUTHORING_CHECKPOINT_COMBAT_CASEBOOK_98.json'; OLD=A/'FEAT335_ORIGINAL_CASEBOOK_REVIEW_COVERAGE_98.json'
OUT=A/'ACTIVE_AUTHORING_CHECKPOINT_GENERAL_COMBAT_CASEBOOK_99.json'; CHECK=A/'ACTIVE_AUTHORING_CHECKPOINT_GENERAL_COMBAT_CASEBOOK_99_CHECK.json'; COVER=A/'FEAT335_ORIGINAL_CASEBOOK_REVIEW_COVERAGE_99.json'; BACK=A/'navigation-before-general-combat-casebook-99'; SAVED=A/Path(__file__).name
for p in [OUT,CHECK,COVER,BACK,SAVED]: assert not p.exists(),str(p)
def j(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def enc(v): return (json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode()
def planned(p,b): return {'path':p.relative_to(G).as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def info(p): return planned(p,p.read_bytes())
def put(p,b):
 with p.open('xb') as f: f.write(b)
checks=[]
def ck(n,ok): checks.append({'check':n,'pass':bool(ok)}); assert ok,n
prior=j(PRE); cp=deepcopy(prior)
ck('Exact checkpoint98',info(PRE)['sha256']=='5024fd5e8d763c8c76b33280967ddf767f8ab742c5d3d993428d6addf786b309')
for row in [prior['currentAuthoredIndex'],prior['currentAcceptedInterfaceRegistry'],prior['currentWorkQueue'],*prior['canonicalHelperBaselinesUnchanged']]: ck('Protected baseline '+row['path'],info(G/row['path'])==row)
rp=A/'FEAT335_GENERAL_COMBAT_ORIGINAL_CASEBOOK_REVIEW_99.json'; r=j(rp); archive=A/'DD_Feat335_General_Combat_Casebook_Review_99.zip'
ck('Exact full general combat report',info(rp)['sha256']=='0c5abedcf1f322f910b8580ee4b60112592cf7e7236f25df87611e2166c12ae7')
ck('Exact complete archive',info(archive)['sha256']=='3900bb6a1b62c0d0b7480439505baf4f701f71e0ff87ac8f89ab1720926cddbf')
ck('484 passing source and bounded checks',r['passed']==484 and r['failed']==0 and all(x['pass'] for x in r['checks']))
ck('58 procedures116 originals3 boundaries',len(r['completeSelectedRecords'])==58 and len(r['originalCaseReviews'])==116 and len(r['additionalBoundaryReviews'])==3)
ck('65 bounded calculations agree',len(r['numericAndStateCalculations'])==65 and all(x['calculatedResult']==x['expectedResult'] for x in r['numericAndStateCalculations']))
for row in r['sourceBindings']: ck('Complete source unchanged '+row['path'],info(G/row['path'])==row)
ck('No runtime canonical or parent promotion',not r['parent335Accepted'] and not r['canonicalApplied'] and r['runtimeTestsExecuted']==0)
old=j(OLD); coverage=deepcopy(old)
ck('Exact prior coverage98',info(OLD)['sha256']=='67c1d5e305f1274cdbc98e213bbd61885217e58ed453fbad7565a1016ac14417')
new_reviews={x['id']:n for n,x in enumerate(r['originalCaseReviews'])}; new_fa={x['id']:n for n,x in enumerate(r['additionalBoundaryReviews'])}
old_reviewed={x['id'] for x in old['ordinary']['positions'] if x['reviewedByThisFullCaseRegister']}; old_fa={x['id'] for x in old['additional']['positions'] if x['reviewedByThisFullCaseRegister']}
ck('116 new positions distinct from322 earlier',len(new_reviews)==116 and len(old_reviewed)==322 and not set(new_reviews)&old_reviewed)
ck('3 new boundaries distinct from12 earlier',len(new_fa)==3 and len(old_fa)==12 and not set(new_fa)&old_fa)
coverage['id']='FEAT335-ORIGINAL-CASEBOOK-REVIEW-COVERAGE-99'; coverage['recordedAtUtc']=datetime.now(timezone.utc).isoformat(); coverage['previousRegister']=info(OLD)
coverage['basis']='Cumulative complete original-position semantic reviews: general_exploration93, skill94, crafting95, general_defense97, combat98 and general_combat99. Earlier targeted diagnostics remain separate; original and current replacement versions occupy the same original position.'
coverage['reviewReports']=[*old['reviewReports'],info(rp)]
for row in coverage['ordinary']['positions']:
 if row['id'] in new_reviews: row.update(reviewedByThisFullCaseRegister=True,reviewEvidencePointer='/originalCaseReviews/'+str(new_reviews[row['id']]),reviewEvidenceReport=info(rp),status='COMPLETE_STATED_CASE_SEMANTIC_REVIEW')
for row in coverage['additional']['positions']:
 if row['id'] in new_fa: row.update(reviewedByThisFullCaseRegister=True,reviewEvidencePointer='/additionalBoundaryReviews/'+str(new_fa[row['id']]),reviewEvidenceReport=info(rp),status='COMPLETE_STATED_CASE_SEMANTIC_REVIEW')
coverage['ordinary']['reviewed']=438; coverage['ordinary']['outsideCurrentFullCaseReview']=222; coverage['additional']['reviewed']=15; coverage['additional']['outsideCurrentFullBoundaryReview']=13; coverage['completedCohorts']=[*old['completedCohorts'],'general_combat']
ck('660 original identities with438 exact review links',len(coverage['ordinary']['positions'])==660 and sum(x['reviewedByThisFullCaseRegister'] for x in coverage['ordinary']['positions'])==438)
ck('28 boundary identities with15 exact review links',len(coverage['additional']['positions'])==28 and sum(x['reviewedByThisFullCaseRegister'] for x in coverage['additional']['positions'])==15)
ck('All original identity and source pointers preserved',all(all(before[k]==after[k] for k in ['id','featId','cohort','originalSourcePointer']) for before,after in zip(old['ordinary']['positions'],coverage['ordinary']['positions'])))
ck('All earlier original review evidence unchanged',all(before==after for before,after in zip(old['ordinary']['positions'],coverage['ordinary']['positions']) if before['id'] not in new_reviews))
ck('All earlier boundary evidence unchanged',all(before==after for before,after in zip(old['additional']['positions'],coverage['additional']['positions']) if before['id'] not in new_fa))
coverage_bytes=enc(coverage); obs=A/'GPT_BESTIARY_REPLACEMENT_ACTIVE_OBSERVATION_99.txt'; observed=obs.read_text(encoding='utf-8')
ck('GPT Return02 actively generating at observation99','button "Stop"' in observed and 'Working for 51m 14s' in observed)
cp['id']='ACTIVE-AUTHORING-GENERAL-COMBAT-CASEBOOK-99'; cp['recordedAtUtc']=datetime.now(timezone.utc).isoformat(); cp['previousCheckpoint']=info(PRE)
cp['status']='Progress:58 full general combat procedures,116 originals and3 additional boundaries reviewed with65 bounded calculations and484 checks. Cumulative438/660 original positions and15/28 boundaries. GPT BestiaryReturn02 still actively generating; no canonical integration.'
cp['previousGoalTurnClassification']={'turn':98,'classification':'progress','evidence':prior['featCombatCasebook98']['report']}
cp['featGeneralCombatCasebook99']={'report':info(rp),'archive':info(archive),'coverageRegister':planned(COVER,coverage_bytes),'coverage':r['coverage'],'cumulativeOriginalPositionsReviewed':438,'remainingOriginalPositionsInRegister':222,'cumulativeAdditionalBoundariesReviewed':15,'remainingAdditionalBoundariesInRegister':13,'checks':484,'failed':0,'fullSourceFiles':24,'archiveMembers':28,'findings':r['reviewFindings'],'remainingScope':r['remainingScope'],'actuallySentToGpt':False,'canonicalApplied':False,'parent335Accepted':False,'runtimeTestsExecuted':0}
cp['previousGptObservationBefore99']=deepcopy(prior['activeGptReviewAtLastVerifiedObservation']); cp['activeGptReviewAtLastVerifiedObservation']['latestObservation99']=info(obs)
cp['activeGptReviewAtLastVerifiedObservation']['latestObservedStatus']='Browser shows active Stop and51m14s working, with thinking-more notice. Return02 not completed, downloaded or accepted. Interim79-trait andDC15/3d8force PressureWave statements await full actual source-linked artifacts. New progress also describes one shared formation budget with explicit member positions, and Recipe173 capture versus later harvest receipts. No interruption, restart or duplicate message.'
cp['bestiaryReplacementDispatch96']['latestObservation99']=info(obs)
cp['pertinentNotebookRecheck99']={'browserRecord':info(obs),'actualReturn02User':'09fd693b-be2d-4274-bc1e-57ac20f4b422','newCompletedReturnObserved':False,'newMessagesSent':0,'unityLastVerifiedNativeRecord':prior['pertinentNotebookRecheck97']['nativeRecord'],'qualification':'Live browser checked99. Unity native notebook last checked97; no99 freshness claim.'}
cp['nextAction']='Continue remaining full feat original-case review with magic_core31 procedures/62 originals, then magic_extended116 and heritage_mutation44.222 originals and13 boundaries remain. Preserve explicit finite-table, real acquisition, copy, mental-predicate final-assembly and joint-parent335 holds. When GPT BestiaryReturn02 completes, immediately save/download its full actual files and independently inspect original counts/text/traits, PressureWave source, positive encounters, recipes, operations and all held interfaces. Do not interrupt solely because thinking is long. Local93/94/95/97/98/99 full casebook packets remain unsent; carry substantive conclusions into the next actual GPT conference.'
cp['lastUsageObservation']={'usedPercent':61,'remainingPercent':39,'resetsAt':1793110625,'stopAtRemainingPercent':20,'source':'Fresh get_usage_limits during turn99 before final casebook write'}
cp['laterLocalWork']='Checkpoints73–99 remain local after last separately verified GitHub backup through72; no push in99.'
nav=[G/'START_HERE.md',R/'docs/DEVELOPMENT_DIRECTION.md',G/'REVIEW_MAP.html']; old_nav={}; prepared={}
for p in nav:
 row=next(x for x in prior['navigation'] if x['path']==p.relative_to(G).as_posix()); ck('Exact prior navigation '+p.name,info(p)==row); raw=old_nav[p]=p.read_bytes()
 if p.suffix=='.html':
  pos=raw.find(b'>',raw.find(b'<body'))+1; note=('<aside><p><strong>Checkpoint99:</strong> General combat adds58 full procedures,116 original cases and3 boundaries with65 bounded calculations. Cumulative438/660 originals and15/28 boundaries. <a href="docs/audit/2026-10-08/full-game/'+OUT.name+'">Current record</a>. Parent335 pending; GPT BestiaryReturn02 actively generating.</p></aside>\n').encode()
 else:
  pos=raw.find(b'\n')+1; prefix='docs/audit/2026-10-08/full-game/' if p.name=='START_HERE.md' else '../../../docs/audit/2026-10-08/full-game/'; note=('\n**Current checkpoint — general combat casebook:** [Checkpoint99]('+prefix+OUT.name+') records58 full procedures,116 original cases and3 additional boundaries, with65 bounded calculations and484 checks. Cumulative full-case coverage438/660 plus15/28 boundaries. Seven prior example replacements and all sources remain preserved. Parent335 and runtime remain pending; GPT BestiaryReturn02 is still actively generating.\n').encode()
 ck('Valid insertion '+p.name,pos>0); new=raw[:pos]+note+raw[pos:]; ck('All earlier navigation bytes retained '+p.name,new[:pos]+new[pos+len(note):]==raw); prepared[p]=new
cp['navigation']=[planned(p,prepared[p]) for p in nav]; cp['preservedNavigation']=[planned(BACK/p.name,old_nav[p]) for p in nav]
ck('Every earlier checkpoint field retained',set(prior).issubset(cp)); ck('No spell count or application change',cp['acceptedButUnapplied']==53 and cp['authoredCounts']==prior['authoredCounts'] and not cp['implementationApplied'])
payload=enc(cp); script=Path(__file__).read_bytes(); validation=enc({'id':'CHECKPOINT99-VALIDATION','checkpoint':planned(OUT,payload),'checks':checks,'passed':len(checks),'failed':0,'script':planned(SAVED,script),'anyNewGptMessageSent':False})
BACK.mkdir()
for p in nav: put(BACK/p.name,old_nav[p]); p.write_bytes(prepared[p])
for p,b in [(SAVED,script),(COVER,coverage_bytes),(OUT,payload),(CHECK,validation)]: put(p,b)
print(json.dumps({'checkpoint':info(OUT),'check':info(CHECK),'coverage':info(COVER),'passed':len(checks),'failed':0},indent=2))
