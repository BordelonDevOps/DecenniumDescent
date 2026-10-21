"""One-shot partial-cohort registration and actual bestiary recovery dispatch."""
from pathlib import Path
from copy import deepcopy
from datetime import datetime,timezone
import json,hashlib
G=Path(r'C:\Github\DecenniumDescent'); R=G/'DescentReviewChanges/ReviewBible'; A=G/'docs/audit/2026-10-08/full-game'
PRE=A/'ACTIVE_AUTHORING_CHECKPOINT_NOTEBOOK_RECHECK_101.json'; OLD=A/'FEAT335_ORIGINAL_CASEBOOK_REVIEW_COVERAGE_100.json'
OUT=A/'ACTIVE_AUTHORING_CHECKPOINT_MAGIC_EXTENDED_PART01_102.json'; CHECK=A/'ACTIVE_AUTHORING_CHECKPOINT_MAGIC_EXTENDED_PART01_102_CHECK.json'; COVER=A/'FEAT335_ORIGINAL_CASEBOOK_REVIEW_COVERAGE_102.json'; BACK=A/'navigation-before-magic-extended-part01-102'; SAVED=A/Path(__file__).name
for p in (OUT,CHECK,COVER,BACK,SAVED):assert not p.exists(),str(p)
def j(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def enc(v):return (json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
def info(p,b=None):
 if b is None:b=p.read_bytes()
 return {'path':p.relative_to(G).as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def put(p,b):
 with p.open('xb') as f:f.write(b)
checks=[]
def ck(n,ok):checks.append({'check':n,'pass':bool(ok)});assert ok,n
prior=j(PRE);cp=deepcopy(prior)
ck('Exact checkpoint101',info(PRE)['sha256']=='bc6f8b3ab97f63b3ae05e6a371c3658ab9bbf6828631c517589393981d076feb')
for row in [prior['currentAuthoredIndex'],prior['currentAcceptedInterfaceRegistry'],prior['currentWorkQueue'],*prior['canonicalHelperBaselinesUnchanged']]:ck('Protected '+row['path'],info(G/row['path'])==row)
rp=A/'FEAT335_MAGIC_EXTENDED_PART01_CASEBOOK_REVIEW_102.json';r=j(rp);archive=A/'DD_Feat335_Magic_Extended_Part01_102.zip'
ck('Exact full report',info(rp)['sha256']=='17a70b4b0f10bfa5f601a35cf78a6fafdcb92c4979470b73a205c275fc65e53b')
ck('Exact full source packet',info(archive)['sha256']=='c1e66d54c0162474301906a8ad338ec67d883a50e804895ab21e6c4e525c7812')
ck('249 checks24 bounded projections',r['passed']==249 and r['failed']==0 and all(x['pass'] for x in r['checks']) and len(r['numericAndStateCalculations'])==24 and all(x['calculatedResult']==x['expectedResult'] for x in r['numericAndStateCalculations']))
for row in r['sourceBindings']:ck('Source retained '+row['path'],info(G/row['path'])==row)
old=j(OLD);coverage=deepcopy(old);ck('Exact prior coverage',info(OLD)['sha256']=='d232e63da77637dea773bf1d477ae9331605dde272ddac06ce23cfcdfa0c6fee')
new={x['id']:i for i,x in enumerate(r['originalCaseReviews'])};fa={x['id']:i for i,x in enumerate(r['additionalBoundaryReviews'])}
old_ids={x['id'] for x in old['ordinary']['positions'] if x['reviewedByThisFullCaseRegister']};old_fa={x['id'] for x in old['additional']['positions'] if x['reviewedByThisFullCaseRegister']}
ck('40 new originals distinct from500',len(new)==40 and len(old_ids)==500 and not set(new)&old_ids)
ck('2 new boundaries distinct from17',len(fa)==2 and len(old_fa)==17 and not set(fa)&old_fa)
coverage['id']='FEAT335-ORIGINAL-CASEBOOK-REVIEW-COVERAGE-102';coverage['recordedAtUtc']=datetime.now(timezone.utc).isoformat();coverage['previousRegister']=info(OLD)
coverage['basis']='Prior seven complete cohorts through100 plus magic_extended MX01-MX20 (40 originals,FA04/16). This is20 of58 extended records; magic_extended is not a completed cohort. Actual acquisition/world prerequisites remain conditional.'
coverage['reviewReports']=[*old['reviewReports'],info(rp)]
for row in coverage['ordinary']['positions']:
 if row['id'] in new:row.update(reviewedByThisFullCaseRegister=True,reviewEvidencePointer='/originalCaseReviews/'+str(new[row['id']]),reviewEvidenceReport=info(rp),status='COMPLETE_STATED_CASE_SEMANTIC_REVIEW')
for row in coverage['additional']['positions']:
 if row['id'] in fa:row.update(reviewedByThisFullCaseRegister=True,reviewEvidencePointer='/additionalBoundaryReviews/'+str(fa[row['id']]),reviewEvidenceReport=info(rp),status='COMPLETE_STATED_CASE_SEMANTIC_REVIEW')
coverage['ordinary']['reviewed']=540;coverage['ordinary']['outsideCurrentFullCaseReview']=120;coverage['additional']['reviewed']=19;coverage['additional']['outsideCurrentFullBoundaryReview']=9
coverage['partialCohorts']=[{'cohort':'magic_extended','recordsReviewed':20,'recordsTotal':58,'questionRange':'MX01-MX20','originalCasesReviewed':40,'originalCasesTotal':116,'additionalReviewed':['FA-04','FA-16'],'report':info(rp),'remainingQuestionRange':'MX21-MX58'}]
ck('540of660 exact reviewed positions',len(coverage['ordinary']['positions'])==660 and sum(x['reviewedByThisFullCaseRegister'] for x in coverage['ordinary']['positions'])==540)
ck('19of28 exact reviewed boundaries',len(coverage['additional']['positions'])==28 and sum(x['reviewedByThisFullCaseRegister'] for x in coverage['additional']['positions'])==19)
ck('Prior reviewed originals retained',all(x==y for x,y in zip(old['ordinary']['positions'],coverage['ordinary']['positions']) if x['id'] not in new))
ck('Prior reviewed boundaries retained',all(x==y for x,y in zip(old['additional']['positions'],coverage['additional']['positions']) if x['id'] not in fa))
ck('No full extended-cohort claim',coverage['completedCohorts']==old['completedCohorts'] and 'magic_extended' not in coverage['completedCohorts'])
coverage_bytes=enc(coverage)
request=A/'CODEX_BESTIARY_RECOVERY_PART01_REQUEST_102.txt';native=A/'GPT_BESTIARY_RECOVERY_PART01_SENT_NATIVE_102.json';sent=A/'GPT_BESTIARY_RECOVERY_PART01_SENT_102.txt';proof=A/'GPT_BESTIARY_RECOVERY_PART01_SENT_102.png';active=A/'GPT_BESTIARY_RECOVERY_PART01_ACTIVE_102.txt'
n=j(native);user=n['turns'][0]['items'][0]
ck('One exact native request persisted',user['id']=='b82cd045-2ee8-4187-95b4-d0302f3f8d91' and user['content'][0]['text'].rstrip('\n')==request.read_text(encoding='utf-8').rstrip('\n'))
ck('Visible exact request responding','Deliver Bestiary Recovery Part01 now' in sent.read_text(encoding='utf-8') and 'button "Stop"' in sent.read_text(encoding='utf-8'))
ck('Latest visible active response retained','ChatGPT is responding' in active.read_text(encoding='utf-8') and 'button "Stop"' in active.read_text(encoding='utf-8'))
cp['id']='ACTIVE-AUTHORING-MAGIC-EXTENDED-PART01-102';cp['recordedAtUtc']=datetime.now(timezone.utc).isoformat();cp['previousCheckpoint']=info(PRE)
cp['status']='Progress:20 full extended-magic records40 original cases2 boundaries reviewed,24 bounded projections249checks. Cumulative540/660 originals19/28 boundaries. Extended cohort still partial. Bestiary RecoveryPart01 actual request delivered and visibly active; no rules promoted.'
cp['previousGoalTurnClassification']={'turn':101,'classification':'progress','evidence':prior['bestiaryUnavailableReturn02_101']['native'],'reason':'New completed GPT report confirmed missing remote outputs, all four local source archives verified, next recovery action changed.'}
cp['featMagicExtendedPart01_102']={'report':info(rp),'archive':info(archive),'coverageRegister':info(COVER,coverage_bytes),'coverage':r['coverage'],'cumulativeOriginalPositionsReviewed':540,'remainingOriginalPositionsInRegister':120,'cumulativeAdditionalBoundariesReviewed':19,'remainingAdditionalBoundariesInRegister':9,'checks':249,'failed':0,'fullSourceFiles':28,'archiveMembers':32,'findings':r['reviewFindings'],'remainingScope':r['remainingScope'],'actuallySentToGpt':False,'summaryActuallySentToGpt':False,'canonicalApplied':False,'parent335Accepted':False,'runtimeTestsExecuted':0}
cp['previousGptObservationBefore102']=deepcopy(prior['activeGptReviewAtLastVerifiedObservation']);cp['activeGptReviewAtLastVerifiedObservation'].update({'conference':'Bestiary Recovery Part01: BV3-04/05/06, bounded delivery toward full unchanged scope','actualUser':user['id'],'latestNativeRecord':info(native),'latestObservation102':info(active),'latestObservedStatus':'Fresh reload showed completed availability response and idle composer before single dispatch. Exact new request now persisted natively and visible with ChatGPT-is-responding/Stop. Recovery reconstruction explicitly permitted using newly written steps; no successful script rerun or supplied code execution. No completed Part01 result yet.'})
cp['bestiaryRecoveryPart01Dispatch102']={'threadId':'6ad4a867-f330-83e9-829e-bf2bb41a6c09','userId':user['id'],'request':info(request),'native':info(native),'browserSent':info(sent),'proof':info(proof),'latestActiveObservation':info(active),'actuallySent':True,'responseActive':True,'newResultReceived':False,'newResultAccepted':False,'scope':['BV3-04','BV3-05','BV3-06'],'wholeBestiaryScopeRetained':True,'fullFeatCasebooksUploaded':False}
cp['nextAction']='Continue magic_extended MX21-MX58 (38records76originals5additional boundaries), then heritage_mutation22/44/4. Parent335 remains pending with120originals9boundaries not yet in the full register. GPT RecoveryPart01 is active: do not interrupt. Save full final bounded text immediately, download real artifacts, independently verify complete sources/procedures/cases before acceptance, then continue remaining bestiary chunks and final complete assembly. Preserve all source archives, missing-return history, five whole-positive-case holds and sealed boundaries. Actual Part01 request communicated500/17; current540/19 and all full casebook archives remain unsent. Separate Unity task owns its Stage0/1 implementation; avoid overlapping changes. No canonical promotion/runtime/gameplay/balance/cosmology/release approval.'
cp['lastUsageObservation']={'usedPercent':66,'remainingPercent':34,'resetsAt':1793110625,'stopAtRemainingPercent':20,'source':'Fresh get_usage_limits after extended-magic Part01 review'}
cp['laterLocalWork']='Review checkpoints73-102 local after last verified GitHub backup through72. No push in102. Separate active Unity task has independent delivery-checkout work; preserve it.'
nav=[G/x['path'] for x in prior['navigation']];orig={};prepared={}
for p in nav:
 row=next(x for x in prior['navigation'] if x['path']==p.relative_to(G).as_posix());raw=p.read_bytes();orig[p]=raw;ck('Navigation precondition '+p.name,info(p,raw)==row)
 if p.suffix=='.html':
  pos=raw.find(b'>',raw.find(b'<body'))+1;note=('<aside><p><strong>Checkpoint102:</strong> Extended magic MX01-20 adds40 original reviews and2 boundaries; cumulative540/660 and19/28.24 bounded projections,249 checks. Extended cohort remains open. <a href="docs/audit/2026-10-08/full-game/'+OUT.name+'">Current record</a>. GPT bestiary RecoveryPart01 is active.</p></aside>\n').encode()
 else:
  pos=raw.find(b'\n')+1;prefix='docs/audit/2026-10-08/full-game/' if p.name=='START_HERE.md' else '../../../docs/audit/2026-10-08/full-game/';note=('\n**Current review checkpoint:** [Checkpoint102]('+prefix+OUT.name+') preserves20 extended-magic records,40 original cases and2 boundaries with24 bounded projections and249 checks. Cumulative540/660 originals and19/28 boundaries; extended magic remains partial. GPT is working on the actually delivered bestiary RecoveryPart01 request. No canonical rules were promoted.\n').encode()
 ck('Insertion point '+p.name,pos>0);prepared[p]=raw[:pos]+note+raw[pos:];ck('All prior navigation retained '+p.name,prepared[p][:pos]+prepared[p][pos+len(note):]==raw)
cp['navigation']=[info(p,prepared[p]) for p in nav];cp['preservedNavigation']=[info(BACK/p.name,orig[p]) for p in nav]
ck('Previous checkpoint fields retained',set(prior).issubset(cp));ck('Membership and authority unchanged',cp['authoredCounts']==prior['authoredCounts'] and cp['acceptedButUnapplied']==53 and not cp['implementationApplied'])
payload=enc(cp);validation=enc({'id':'CHECKPOINT102-VALIDATION','checkpoint':info(OUT,payload),'checks':checks,'passed':len(checks),'failed':0,'script':info(SAVED,Path(__file__).read_bytes()),'newGptMessagesSent':1,'runtimeTestsExecuted':0})
BACK.mkdir()
for p in nav:
 put(BACK/p.name,orig[p]);assert p.read_bytes()==orig[p],str(p);p.write_bytes(prepared[p])
for p,b in [(SAVED,Path(__file__).read_bytes()),(COVER,coverage_bytes),(OUT,payload),(CHECK,validation)]:put(p,b)
print(json.dumps({'checkpoint':info(OUT),'check':info(CHECK),'coverage':info(COVER),'passed':len(checks),'failed':0},indent=2))
