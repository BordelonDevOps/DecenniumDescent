"""Register completed MX41-58 review, dual bestiary intake and exact GPT conference."""
from pathlib import Path
from datetime import datetime,timezone
from copy import deepcopy
import json,hashlib,zipfile
G=Path(r'C:\Github\DecenniumDescent');A=G/'docs/audit/2026-10-08/full-game'
PRE=A/'ACTIVE_AUTHORING_CHECKPOINT_MAGIC_EXTENDED_PART02_103.json';OLD=A/'FEAT335_ORIGINAL_CASEBOOK_REVIEW_COVERAGE_103.json'
OUT=A/'ACTIVE_AUTHORING_CHECKPOINT_MAGIC_EXTENDED_AND_BESTIARY_104.json';CHECK=A/'ACTIVE_AUTHORING_CHECKPOINT_MAGIC_EXTENDED_AND_BESTIARY_104_CHECK.json';COVER=A/'FEAT335_ORIGINAL_CASEBOOK_REVIEW_COVERAGE_104.json';BACK=A/'navigation-before-magic-extended-bestiary-104';SAVED=A/Path(__file__).name
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
ck('Exact checkpoint103',info(PRE)['sha256']=='542c5e87bc4a3c6c9e7fedbe68ed4ef1436fa896761185dca08e7c6eb48f2b17')
for row in [prior['currentAuthoredIndex'],prior['currentAcceptedInterfaceRegistry'],prior['currentWorkQueue'],*prior['canonicalHelperBaselinesUnchanged']]:ck('Protected '+row['path'],info(G/row['path'])==row)
rp=A/'FEAT335_MAGIC_EXTENDED_PART03_CASEBOOK_REVIEW_104.json';r=j(rp);archive=A/'DD_Feat335_Magic_Extended_Part03_104.zip'
ck('Exact full report',info(rp)['sha256']=='d9389cd12039a6bc84c6c25aa3883aabcad2fb7841d638acd7d652f0c4bbdc92')
ck('Exact complete archive',info(archive)['sha256']=='ce46039e56d3f04495d5db85bb0a482c559d9d88c1a281edb1627cb4b162bf3e')
ck('257 checks35 bounded calculations',r['passed']==257 and r['failed']==0 and all(x['pass'] for x in r['checks']) and len(r['numericAndStateCalculations'])==35 and all(x['calculatedResult']==x['expectedResult'] for x in r['numericAndStateCalculations']))
for row in r['sourceBindings']:ck('Source retained '+row['path'],info(G/row['path'])==row)
with zipfile.ZipFile(archive) as z:
 ck('37 unique CRC-valid members',len(z.namelist())==len(set(z.namelist()))==37 and z.testzip() is None)
 manifest=json.loads(z.read('MANIFEST.json'));mapping=json.loads(z.read('SOURCE_MAP.json'))
 ck('32 full mapped sources',len(mapping)==32)
 ck('Complete manifest',set(x['path'] for x in manifest['files'])==set(z.namelist())-{'MANIFEST.json'})
 for row in manifest['files']:
  b=z.read(row['path']);ck('Package '+row['path'],len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256'])
 for row in mapping:ck('Mapped source '+row['member'],z.read(row['member'])==(G/row['path']).read_bytes())
old=j(OLD);coverage=deepcopy(old);ck('Exact prior coverage',info(OLD)['sha256']=='4a42d7eadbc8e219f43fcab5d1efba309028d7d895874e824e7c5b714121a8ca')
new={x['id']:i for i,x in enumerate(r['originalCaseReviews'])};fa={x['id']:i for i,x in enumerate(r['additionalBoundaryReviews'])};oldids={x['id'] for x in old['ordinary']['positions'] if x['reviewedByThisFullCaseRegister']};oldfa={x['id'] for x in old['additional']['positions'] if x['reviewedByThisFullCaseRegister']}
ck('36new originals distinct from580',len(new)==36 and len(oldids)==580 and not set(new)&oldids)
ck('3new boundaries distinct from21',set(fa)=={'FA-17','FA-18','FA-26'} and len(oldfa)==21 and not set(fa)&oldfa)
coverage.update(id='FEAT335-ORIGINAL-CASEBOOK-REVIEW-COVERAGE-104',recordedAtUtc=datetime.now(timezone.utc).isoformat(),previousRegister=info(OLD),basis='Eight complete cohorts. Magic_extended MX01-MX58 contains all116 original cases and7 boundary cases across reports102/103/104. Only heritage_mutation44 originals4 boundaries remain. Actual acquisition/world prerequisites and parent335 acceptance remain separate.',reviewReports=[*old['reviewReports'],info(rp)])
for row in coverage['ordinary']['positions']:
 if row['id'] in new:row.update(reviewedByThisFullCaseRegister=True,reviewEvidencePointer='/originalCaseReviews/'+str(new[row['id']]),reviewEvidenceReport=info(rp),status='COMPLETE_STATED_CASE_SEMANTIC_REVIEW')
for row in coverage['additional']['positions']:
 if row['id'] in fa:row.update(reviewedByThisFullCaseRegister=True,reviewEvidencePointer='/additionalBoundaryReviews/'+str(fa[row['id']]),reviewEvidenceReport=info(rp),status='COMPLETE_STATED_CASE_SEMANTIC_REVIEW')
coverage['ordinary'].update(reviewed=616,outsideCurrentFullCaseReview=44);coverage['additional'].update(reviewed=24,outsideCurrentFullBoundaryReview=4)
coverage['completedCohorts']=[*old['completedCohorts'],'magic_extended'];coverage['partialCohorts']=[]
mx=[x for x in coverage['ordinary']['positions'] if x['cohort']=='magic_extended']
ck('All116 exact magic_extended case positions',len(mx)==116 and all(x['reviewedByThisFullCaseRegister'] for x in mx) and {x['id'] for x in mx}=={'MX-'+str(i).zfill(2)+'-E0'+str(k) for i in range(1,59) for k in (1,2)})
ck('All7 exact magic_extended boundaries',all(x in oldfa|set(fa) for x in ['FA-04','FA-16','FA-17','FA-18','FA-20','FA-21','FA-26']))
ck('616of660 exact reviewed positions',len(coverage['ordinary']['positions'])==660 and sum(x['reviewedByThisFullCaseRegister'] for x in coverage['ordinary']['positions'])==616)
ck('24of28 exact reviewed boundaries',len(coverage['additional']['positions'])==28 and sum(x['reviewedByThisFullCaseRegister'] for x in coverage['additional']['positions'])==24)
ck('All previous original reviews unchanged',all(x==y for x,y in zip(old['ordinary']['positions'],coverage['ordinary']['positions']) if x['id'] not in new))
ck('All previous boundary reviews unchanged',all(x==y for x,y in zip(old['additional']['positions'],coverage['additional']['positions']) if x['id'] not in fa))
ck('Only heritage originals remain',all(x['cohort']=='heritage_mutation' for x in coverage['ordinary']['positions'] if not x['reviewedByThisFullCaseRegister']))
coverbytes=enc(coverage)
intake=A/'BESTIARY_DUAL_DELIVERY_INTAKE_104.json';reconstruction=A/'BESTIARY_DUAL_PROPOSAL_RECONSTRUCTION_104.json';ir=j(intake);rr=j(reconstruction)
ck('Independent intake92 checks',ir['checkCount']==92 and ir['failures']==0 and all(x['pass'] for x in ir['checks']))
ck('Independent reconstruction175 checks',rr['passed']==175 and rr['failed']==0 and all(x['pass'] for x in rr['checks']) and len(rr['differences'])==5)
for row in ir['files']:
 b=Path(row['path']).read_bytes();ck('Delivery preserved '+Path(row['path']).name,len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256'])
native=A/'GPT_BESTIARY_RECONCILIATION_NATIVE_104.json';sent=A/'GPT_BESTIARY_RECONCILIATION_SENT_104.txt';request=A/'GPT_BESTIARY_DUAL_DELIVERY_RECONCILIATION_REQUEST_104.txt';shot=A/'GPT_BESTIARY_RECONCILIATION_SENT_104.png';n=j(native)
ck('Exact dispatched request currently active',n['turns'][0]['id']=='c06ad34e-a672-44dc-af8f-462031ed7ddf' and n['thread']['status']['type']=='active')
ck('Visible submission received without interruption','Codex receipt104:' in sent.read_text(encoding='utf-8') and 'ChatGPT is responding' in sent.read_text(encoding='utf-8'))
ck('Both distinct completed prior responses retained',{'592dac0a-6509-4bd1-8868-d46d3a31ac25','44937d90-667f-449e-9838-deb803e41add'}.issubset({x['id'] for x in n['turns'][1]['items']}))
cp.update(id='ACTIVE-AUTHORING-MAGIC-EXTENDED-AND-BESTIARY-104',recordedAtUtc=datetime.now(timezone.utc).isoformat(),previousCheckpoint=info(PRE),status='Progress: extended magic completed58records/116originals/7boundaries across102-104; cumulative616/660originals24/28boundaries. Both new GPT bestiary final deliveries preserved and independently byte/reconstruction checked. Five substantive proposal forks sent for bounded joint reconciliation; neither final independently accepted or applied.')
cp['previousGoalTurnClassification']={'turn':103,'classification':'progress','evidence':prior['featMagicExtendedPart02_103']['report'],'reason':'20fullrecords40originals2boundaries reviewed, with full-source packaging recovery.'}
cp['featMagicExtendedPart03_104']={'report':info(rp),'archive':info(archive),'coverageRegister':info(COVER,coverbytes),'coverage':r['coverage'],'cumulativeOriginalPositionsReviewed':616,'remainingOriginalPositionsInRegister':44,'cumulativeAdditionalBoundariesReviewed':24,'remainingAdditionalBoundariesInRegister':4,'completedExtendedRecords':58,'completedExtendedOriginals':116,'completedExtendedBoundaries':7,'checks':257,'failed':0,'fullSourceFiles':32,'archiveMembers':37,'findings':r['reviewFindings'],'remainingScope':r['remainingScope'],'statusNote':'Report remainingScope reflects its earlier creation time; the subsequent dual bestiary intake and reconciliation below are current.','actuallySentToGpt':False,'summarySentToGpt':True,'canonicalApplied':False,'parent335Accepted':False,'runtimeTestsExecuted':0}
cp['bestiaryDualDelivery104']={'intake':info(intake),'reconstruction':info(reconstruction),'preservedDownloads':[info(Path(x['path'])) for x in ir['files']],'priorFinalUserId':'b82cd045-2ee8-4187-95b4-d0302f3f8d91','priorFinalAssistantIds':['592dac0a-6509-4bd1-8868-d46d3a31ac25','44937d90-667f-449e-9838-deb803e41add'],'completeVisibleBothFinals':info(A/'GPT_BESTIARY_COMBINED_DELIVERY_VISIBLE_104.txt'),'firstFinalVisible':info(A/'GPT_BESTIARY_RECOVERY_PART01_FINAL_RESPONSE_104.txt'),'interimHistoryOnly':info(A/'GPT_BESTIARY_RECOVERY_PART01_INTERIM_OUTPUT_104.txt'),'independentContainerChecks':92,'independentReconstructionChecks':175,'semanticForks':[{'id':x['id'],'status':x['status']} for x in rr['differences']],'wholeReturn02AuthorReportedCounts':j(A/'bestiary-deliveries-104/return02/REVIEW_RECEIPT.json')['counts'],'wholeReturn02AuthorReportedCases':j(A/'bestiary-deliveries-104/return02/REVIEW_RECEIPT.json')['cases'],'wholeSemanticReviewComplete':False,'canonicalApplied':False,'suppliedCodeExecuted':False}
cp['activeGptReviewAtLastVerifiedObservation'].update(conference='Five semantic differences between final Part01 and whole proposed Return02',actualUser='c06ad34e-a672-44dc-af8f-462031ed7ddf',latestNativeRecord=info(native),latestObservation104=info(sent),latestObservedStatus='New bounded reconciliation request visibly submitted and active. Both prior final files are safely local; no generation interrupted.')
cp['notebookRecheck104']={'reviewNative':info(native),'request':info(request),'reviewVisible':info(sent),'proof':info(shot),'newMessagesSent':1,'newFinalBestiaryReturnReceived':True,'activeGenerationInterrupted':False,'newUnityDirections':'not rechecked in104;103 identity evidence retained'}
cp['nextAction']='Continue independent whole-Return02 source/semantic/case review while GPT reconciles five actual Part01/Return02 forks; do not interrupt active generation or accept either proposal by hash/count alone. Save and review the bounded successor when complete. Complete remaining heritage_mutation22records44originals4boundaries, then parent335 actualacquisition/copy/mental-predicate assembly and jointreview. Feat fullcase coverage616/66024/28 is not whole-game completion. Local fullcase reports have not been uploaded toGPT; summary616/24 sent104. Preserve exact source histories and five whole-positive holds. No overlapping Unity delivery-checkout edits or canonical promotion.'
cp['lastUsageObservation']={'usedPercent':69,'remainingPercent':31,'resetsAt':1793110625,'stopAtRemainingPercent':20,'source':'Fresh get_usage_limits during104'}
cp['laterLocalWork']='Review checkpoints73-104 local after last verified GitHub backup through72. No push104. Separate user Unity task has independent delivery-checkout work; preserve it.'
nav=[G/x['path'] for x in prior['navigation']];raws={};prepared={}
for p in nav:
 raw=p.read_bytes();raws[p]=raw;row=next(x for x in prior['navigation'] if x['path']==p.relative_to(G).as_posix());ck('Navigation precondition '+p.name,info(p,raw)==row)
 if p.suffix=='.html':
  pos=raw.find(b'>',raw.find(b'<body'))+1;note=('<aside><p><strong>Checkpoint104:</strong> Extended magic58/58 full-case review complete; cumulative616/660 originals and24/28 boundaries. Both new GPT bestiary deliveries safely preserved and independently reconstructed; five rule differences await joint reconciliation. <a href="docs/audit/2026-10-08/full-game/'+OUT.name+'">Current record</a>.</p></aside>\n').encode()
 else:
  pos=raw.find(b'\n')+1;prefix='docs/audit/2026-10-08/full-game/' if p.name=='START_HERE.md' else '../../../docs/audit/2026-10-08/full-game/';note=('\n**Current review checkpoint:** [Checkpoint104]('+prefix+OUT.name+') completes the58-record extended-magic full-case review; cumulative616/660 originals and24/28 boundaries. Both GPT bestiary finals are safely local;92 container and175 independent reconstruction checks pass. Five proposed-rule differences are withGPT for reconciliation. Heritage/mutation and whole-candidate acceptance remain open.\n').encode()
 ck('Navigation insertion '+p.name,pos>0);prepared[p]=raw[:pos]+note+raw[pos:];ck('Prior navigation intact '+p.name,prepared[p][:pos]+prepared[p][pos+len(note):]==raw)
cp['navigation']=[info(p,prepared[p]) for p in nav];cp['preservedNavigation']=[info(BACK/p.name,raws[p]) for p in nav]
ck('Prior checkpoint fields retained',set(prior).issubset(cp));ck('Counts and authority unchanged',cp['authoredCounts']==prior['authoredCounts'] and cp['acceptedButUnapplied']==53 and not cp['implementationApplied'])
payload=enc(cp);validation=enc({'id':'CHECKPOINT104-VALIDATION','checkpoint':info(OUT,payload),'checks':checks,'passed':len(checks),'failed':0,'script':info(SAVED,Path(__file__).read_bytes()),'newGptMessagesSent':1,'runtimeTestsExecuted':0})
BACK.mkdir()
for p in nav:
 put(BACK/p.name,raws[p]);assert p.read_bytes()==raws[p];p.write_bytes(prepared[p])
for p,b in [(SAVED,Path(__file__).read_bytes()),(COVER,coverbytes),(OUT,payload),(CHECK,validation)]:put(p,b)
print(json.dumps({'checkpoint':info(OUT),'check':info(CHECK),'coverage':info(COVER),'passed':len(checks),'failed':0},indent=2))
