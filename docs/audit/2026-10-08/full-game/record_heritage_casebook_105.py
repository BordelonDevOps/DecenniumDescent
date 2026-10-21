"""Register all remaining stated feat cases and preserve live reconciliation evidence."""
from pathlib import Path
from datetime import datetime,timezone
from copy import deepcopy
import json,hashlib,zipfile
G=Path(r'C:\Github\DecenniumDescent');A=G/'docs/audit/2026-10-08/full-game'
PRE=A/'ACTIVE_AUTHORING_CHECKPOINT_MAGIC_EXTENDED_AND_BESTIARY_104.json';OLD=A/'FEAT335_ORIGINAL_CASEBOOK_REVIEW_COVERAGE_104.json'
OUT=A/'ACTIVE_AUTHORING_CHECKPOINT_ALL_FEAT_CASES_105.json';CHECK=A/'ACTIVE_AUTHORING_CHECKPOINT_ALL_FEAT_CASES_105_CHECK.json';COVER=A/'FEAT335_ORIGINAL_CASEBOOK_REVIEW_COVERAGE_105.json';BACK=A/'navigation-before-all-feat-cases-105';SAVED=A/Path(__file__).name
for p in (OUT,CHECK,COVER,BACK,SAVED):assert not p.exists(),str(p)
def j(p):return json.loads(p.read_bytes())
def enc(v):return (json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode()
def info(p,b=None):
 if b is None:b=p.read_bytes()
 return {'path':p.relative_to(G).as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def put(p,b):
 with p.open('xb') as f:f.write(b)
checks=[]
def ck(n,ok):checks.append({'check':n,'pass':bool(ok)});assert ok,n
prior=j(PRE);cp=deepcopy(prior)
ck('Exact checkpoint104',info(PRE)['sha256']=='c781d38ed33bedae685858f16ab504cd450a338153cf3de38d1402045852f6cf')
for row in [prior['currentAuthoredIndex'],prior['currentAcceptedInterfaceRegistry'],prior['currentWorkQueue'],*prior['canonicalHelperBaselinesUnchanged']]:ck('Protected '+row['path'],info(G/row['path'])==row)
rp=A/'FEAT335_HERITAGE_MUTATION_CASEBOOK_REVIEW_105.json';r=j(rp);archive=A/'DD_Feat335_Heritage_Mutation_105.zip'
ck('Exact full report',info(rp)['sha256']=='5e68f6299cd2060bce5d62112e4646d63709f1f98dcc0660f5087a0658e0d071')
ck('Exact complete archive',info(archive)['sha256']=='b39a7bb79aedcd6399caa6de35f9c1af2209940f1e50b06628ae9da870cb596f')
ck('351 checks34 bounded calculations',r['passed']==351 and r['failed']==0 and all(x['pass'] for x in r['checks']) and len(r['numericAndStateCalculations'])==34 and all(x['calculatedResult']==x['expectedResult'] for x in r['numericAndStateCalculations']))
for row in r['sourceBindings']:ck('Source retained '+row['path'],info(G/row['path'])==row)
with zipfile.ZipFile(archive) as z:
 ck('62 unique CRC-valid members',len(z.namelist())==len(set(z.namelist()))==62 and z.testzip() is None)
 manifest=json.loads(z.read('MANIFEST.json'));mapping=json.loads(z.read('SOURCE_MAP.json'))
 ck('57 full mapped sources',len(mapping)==57)
 ck('Complete manifest',set(x['path'] for x in manifest['files'])==set(z.namelist())-{'MANIFEST.json'})
 for row in manifest['files']:
  b=z.read(row['path']);ck('Package '+row['path'],len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256'])
 for row in mapping:ck('Mapped source '+row['member'],z.read(row['member'])==(G/row['path']).read_bytes())
old=j(OLD);coverage=deepcopy(old);ck('Exact prior coverage',info(OLD)['sha256']=='c6607ad7fe3c5369de3087576d846a933cd9b99cfecd7c10e96254f619717f1d')
new={x['id']:i for i,x in enumerate(r['originalCaseReviews'])};fa={x['id']:i for i,x in enumerate(r['additionalBoundaryReviews'])};oldids={x['id'] for x in old['ordinary']['positions'] if x['reviewedByThisFullCaseRegister']};oldfa={x['id'] for x in old['additional']['positions'] if x['reviewedByThisFullCaseRegister']}
ck('44new originals distinct from616',len(new)==44 and len(oldids)==616 and not set(new)&oldids)
ck('4new boundaries distinct from24',set(fa)=={'FA-06','FA-22','FA-23','FA-24'} and len(oldfa)==24 and not set(fa)&oldfa)
coverage.update(id='FEAT335-ORIGINAL-CASEBOOK-REVIEW-COVERAGE-105',recordedAtUtc=datetime.now(timezone.utc).isoformat(),previousRegister=info(OLD),basis='All nine cohorts:660 original stated-case positions and28 additional boundaries independently read and reviewed against exact full source/current procedures. This completes the stated-case review register, not parent335 assembly, actual campaign authentication, engine execution, balance or publication approval.',reviewReports=[*old['reviewReports'],info(rp)])
for row in coverage['ordinary']['positions']:
 if row['id'] in new:row.update(reviewedByThisFullCaseRegister=True,reviewEvidencePointer='/originalCaseReviews/'+str(new[row['id']]),reviewEvidenceReport=info(rp),status='COMPLETE_STATED_CASE_SEMANTIC_REVIEW')
for row in coverage['additional']['positions']:
 if row['id'] in fa:row.update(reviewedByThisFullCaseRegister=True,reviewEvidencePointer='/additionalBoundaryReviews/'+str(fa[row['id']]),reviewEvidenceReport=info(rp),status='COMPLETE_STATED_CASE_SEMANTIC_REVIEW')
coverage['ordinary'].update(reviewed=660,outsideCurrentFullCaseReview=0);coverage['additional'].update(reviewed=28,outsideCurrentFullBoundaryReview=0)
coverage['completedCohorts']=[*old['completedCohorts'],'heritage_mutation'];coverage['partialCohorts']=[]
ck('All44 exact heritage case positions',{x['id'] for x in coverage['ordinary']['positions'] if x['cohort']=='heritage_mutation'}=={f'HM-{i:02d}-E0{k}' for i in range(1,23) for k in (1,2)})
ck('All660 originals reviewed',len(coverage['ordinary']['positions'])==660 and all(x['reviewedByThisFullCaseRegister'] for x in coverage['ordinary']['positions']))
ck('All28 boundaries reviewed',len(coverage['additional']['positions'])==28 and all(x['reviewedByThisFullCaseRegister'] for x in coverage['additional']['positions']))
ck('Nine distinct completed cohorts',len(coverage['completedCohorts'])==len(set(coverage['completedCohorts']))==9)
ck('All previous original reviews unchanged',all(x==y for x,y in zip(old['ordinary']['positions'],coverage['ordinary']['positions']) if x['id'] not in new))
ck('All previous boundary reviews unchanged',all(x==y for x,y in zip(old['additional']['positions'],coverage['additional']['positions']) if x['id'] not in fa))
cache={}
for row in coverage['ordinary']['positions']+coverage['additional']['positions']:
 binding=row.get('reviewEvidenceReport',coverage['reviewReport']);path=G/binding['path']
 if str(path) not in cache:
  ck('Exact full position report '+path.name,info(path)==binding);cache[str(path)]=j(path)
 value=cache[str(path)]
 for key in row['reviewEvidencePointer'].split('/')[1:]:value=value[int(key)] if isinstance(value,list) else value[key.replace('~1','/').replace('~0','~')]
 if 'featId' in value:resolved_feat=value['featId']
 elif 'completeOriginalBoundary' in value:resolved_feat=value['completeOriginalBoundary']['featId']
 else:resolved_feat=value['completeOriginalDisposition']['featId']
 ck('Bound actual review position '+row['id'],value['id']==row['id'] and resolved_feat==row['featId'])
coverbytes=enc(coverage)
native=A/'GPT_BESTIARY_RECONCILIATION_NATIVE_105.json';visible=A/'GPT_BESTIARY_RECONCILIATION_VISIBLE_105.txt';n=j(native);vs=visible.read_text(encoding='utf-8')
ck('Exact request unchanged',n['turns'][0]['id']=='c06ad34e-a672-44dc-af8f-462031ed7ddf')
ck('Visible running reconciliation with new source work','button "Stop"' in vs and 'R105-CONSTRICT-01' in vs and 'SELECTED_WORDING.json' in vs)
ck('No completed native assistant successor yet',not any(x['type']=='agentMessage' for x in n['turns'][0]['items']))
cp.update(id='ACTIVE-AUTHORING-ALL-FEAT-STATED-CASES-105',recordedAtUtc=datetime.now(timezone.utc).isoformat(),previousCheckpoint=info(PRE),status='Progress: all22 heritage/mutation records44originals4boundaries reviewed with34 bounded calculations351checks; all660 original statedcases and28 additionalboundaries now individually source-linked across9cohorts. Parent335 exact assembly/acceptance remains pending. GPT visibly continues five-fork bestiary reconciliation; no final successor received.')
cp['previousGoalTurnClassification']={'turn':104,'classification':'progress','evidence':prior['bestiaryDualDelivery104']['reconstruction'],'reason':'Finished extended magic; preserved both new GPT final bestiary deliveries, independently reconstructed all original/model bytes, and dispatched five concrete semantic forks.'}
cp['featHeritageMutationCasebook105']={'report':info(rp),'archive':info(archive),'coverageRegister':info(COVER,coverbytes),'coverage':r['coverage'],'cumulativeOriginalPositionsReviewed':660,'remainingOriginalPositionsInRegister':0,'cumulativeAdditionalBoundariesReviewed':28,'remainingAdditionalBoundariesInRegister':0,'checks':351,'failed':0,'fullSourceFiles':57,'archiveMembers':62,'findings':r['reviewFindings'],'remainingScope':r['remainingScope'],'allOriginalPositionsIndividuallyBound':True,'actuallySentToGpt':False,'canonicalApplied':False,'parent335Accepted':False,'runtimeTestsExecuted':0}
cp['activeGptReviewAtLastVerifiedObservation'].update(latestNativeRecord=info(native),latestObservation105=info(visible),latestObservedStatus='Same reconciliation request still has no completed native assistant item. Native status says idle, but fresh browser shows Stop and live new R105 source/reconciliation work. Treat as active observed workflow; no interruption or duplicate message.')
cp['notebookRecheck105']={'reviewNative':info(native),'reviewVisible':info(visible),'newMessagesSent':0,'newFinalSuccessorReceived':False,'activeGenerationInterrupted':False,'statusDiscrepancy':'Native idle versus live browser Stop; continued live page wins for noninterruption.'}
cp['registrationRecovery105']={'preservedFailedScripts':[info(A/'record_heritage_casebook_105_failed_boundary_shape.py'),info(A/'record_heritage_casebook_105_failed_disposition_shape.py')],'failure':'Historical boundary review schemas retain featId inside completeOriginalBoundary or completeOriginalDisposition instead of an outer duplicate. Both failed attempts stopped before outputs/navigation writes.','repair':'Resolve exact featId from the observed outer or two explicit nested source schemas. No identity check removed; all688 positions still checked.'}
cp['nextAction']='Assemble the complete parent335 review candidate in a separate derived directory: combine exact D92FT84 successors, later copy/Ready preparation-only policy and all seven profiles, full current acquisition evidence, and explicit carried mental-effect predicate. Reconstruct independent public allowlist/full9manuscripts and all finite supplements, preserve all335 originals/eight unchanged/null2, then audit FXC01-12 and send complete actual candidate/source/evidence package toGPT for exact joint review. All660/28statedcases are now covered; do not review them again merely to increasecounts. Check and preserve GPT bounded R105 bestiary reconciliation when final, independently validate beforeselection; continue wholeReturn02semanticreview. No supplied-codeexecution, successfulscript reruns, canonical promotion, Unity checkout overlap or cosmology changes.'
cp['lastUsageObservation']={'usedPercent':71,'remainingPercent':29,'resetsAt':1793110625,'stopAtRemainingPercent':20,'source':'Fresh get_usage_limits after heritage review105'}
cp['laterLocalWork']='Review checkpoints73-105 local after last verified GitHub backup through72. No push105. Separate user Unity task has independent delivery-checkout work; preserve it.'
nav=[G/x['path'] for x in prior['navigation']];raws={};prepared={}
for p in nav:
 raw=p.read_bytes();raws[p]=raw;row=next(x for x in prior['navigation'] if x['path']==p.relative_to(G).as_posix());ck('Navigation precondition '+p.name,info(p,raw)==row)
 if p.suffix=='.html':
  pos=raw.find(b'>',raw.find(b'<body'))+1;note=('<aside><p><strong>Checkpoint105:</strong> All660 original feat cases and28 additional boundaries reviewed across9cohorts. Heritage/mutation22records adds44originals4boundaries. Parent335 assembly and joint acceptance remain open. <a href="docs/audit/2026-10-08/full-game/'+OUT.name+'">Current record</a>. GPT bestiary reconciliation remains in progress.</p></aside>\n').encode()
 else:
  pos=raw.find(b'\n')+1;prefix='docs/audit/2026-10-08/full-game/' if p.name=='START_HERE.md' else '../../../docs/audit/2026-10-08/full-game/';note=('\n**Current review checkpoint:** [Checkpoint105]('+prefix+OUT.name+') completes all660 original feat-case positions and28 additional boundaries across9cohorts. Last22 heritage/mutation records add44originals,4boundaries and34 bounded calculations/351checks. Complete parent335 assembly/joint review and bestiary reconciliation remain open; no runtime, balance or whole-game approval.\n').encode()
 ck('Navigation insertion '+p.name,pos>0);prepared[p]=raw[:pos]+note+raw[pos:];ck('Prior navigation intact '+p.name,prepared[p][:pos]+prepared[p][pos+len(note):]==raw)
cp['navigation']=[info(p,prepared[p]) for p in nav];cp['preservedNavigation']=[info(BACK/p.name,raws[p]) for p in nav]
ck('Prior checkpoint fields retained',set(prior).issubset(cp));ck('Counts and authority unchanged',cp['authoredCounts']==prior['authoredCounts'] and cp['acceptedButUnapplied']==53 and not cp['implementationApplied'])
payload=enc(cp);validation=enc({'id':'CHECKPOINT105-VALIDATION','checkpoint':info(OUT,payload),'checks':checks,'passed':len(checks),'failed':0,'script':info(SAVED,Path(__file__).read_bytes()),'newGptMessagesSent':0,'runtimeTestsExecuted':0})
BACK.mkdir()
for p in nav:
 put(BACK/p.name,raws[p]);assert p.read_bytes()==raws[p];p.write_bytes(prepared[p])
for p,b in [(SAVED,Path(__file__).read_bytes()),(COVER,coverbytes),(OUT,payload),(CHECK,validation)]:put(p,b)
print(json.dumps({'checkpoint':info(OUT),'check':info(CHECK),'coverage':info(COVER),'passed':len(checks),'failed':0},indent=2))
