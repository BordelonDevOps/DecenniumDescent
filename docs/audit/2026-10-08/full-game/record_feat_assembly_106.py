from pathlib import Path
import json,hashlib,datetime,shutil
G=Path(r'C:\Github\DecenniumDescent');A=G/'docs/audit/2026-10-08/full-game'
P=A/'ACTIVE_AUTHORING_CHECKPOINT_FEAT_ASSEMBLY_106.json'
assert not P.exists()
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(b):return hashlib.sha256(b).hexdigest()
def bind(p):
    b=p.read_bytes();return {'path':p.relative_to(G).as_posix(),'bytes':len(b),'sha256':sha(b)}
old=A/'ACTIVE_AUTHORING_CHECKPOINT_ALL_FEAT_CASES_105.json';d=read(old)
checks=[]
def ck(n,r):checks.append({'name':n,'passed':bool(r)});assert r,n
for b in d['canonicalHelperBaselinesUnchanged']+[d['currentAuthoredIndex'],d['currentAcceptedInterfaceRegistry']]:
    ck('Protected authority unchanged '+b['path'],bind(G/b['path'])==b)
s=read(A/'FEAT335_ASSEMBLY_RECEIPT_106.json');a=read(A/'FEAT335_ACQUISITION_EVIDENCE_RECEIPT_106.json')
for receipt in [s,a]:
    ck('Successful bounded assembly '+receipt['id'],receipt['failed']==0 and not receipt['canonicalApplied'])
    for k in ['zip','report']:
        b=receipt[k];p=Path(b['path']);raw=p.read_bytes()
        ck('Actual deliverable '+p.name,len(raw)==b['bytes'] and sha(raw)==b['sha256'])
d['id']='ACTIVE_AUTHORING_CHECKPOINT_FEAT_ASSEMBLY_106'
d['recordedAtUtc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
d['previousCheckpoint']=bind(old)
d['status']='Progress: complete derived feat assembly and current acquisition mirrors preserved; exact parent acceptance and bestiary reconciliation remain open.'
d['previousGoalTurnClassification']='Progress:105 completed all660 original feat case positions and28 additional boundaries; no need to repeat them for counts.'
d['featAssembly106']={'receipt':bind(A/'FEAT335_ASSEMBLY_RECEIPT_106.json'),'report':bind(Path(s['report']['path'])),'package':s['zip'],
    'ordinaryPositions':660,'additionalBoundaries':28,'originalIds':335,'unchangedReviewed':8,'nullWrappers':2,
    'sharedRules':16,'cohortChapters':9,'checksPassed':3149,'failed':0,
    'merges':['D92 six FT84 successors retained','Three paid-copy records plus FS08 and all7profile concentration/family/strain fields synchronized','COPY-READY-ALLOWANCE-02 preparation-only selected policy','Already adopted mental predicate carried explicitly in FS05 and both applicable feats'],
    'parentAccepted':False,'newRuntimeImplementation':False,'actuallyUploadedToGpt':False}
d['featAcquisitionAssembly106']={'receipt':bind(A/'FEAT335_ACQUISITION_EVIDENCE_RECEIPT_106.json'),'report':a['report'],'package':a['zip'],
    'currentAcquisition':a['currentAcquisition'],'currentAllowanceDescriptors':a['currentAllowances'],
    'all335Entries':True,'all177AllowanceDescriptors':True,'historicalEvidenceFiles':15,'checksPassed':1976,'failed':0,
    'changedDescriptorIdentities':a['changedDescriptorIdentities'],
    'finding':'The old three copyRelease cadence descriptors incorrectly remained release-worded. Derived mirrors now count direct cast/Ready preparation only, preserving original family identity, acquisition permissions, finite uses and histories.',
    'historicEvidenceNotRerun':True,'all335FullAcquisitionsExecuted':False,'parentAccepted':False,'actuallyUploadedToGpt':False}
d['notebookRecheck106']={'native':bind(A/'GPT_BESTIARY_RECONCILIATION_NATIVE_106.json'),
    'initialVisible':bind(A/'GPT_REVIEW_VISIBLE_106.txt'),'latestVisible':bind(A/'GPT_BESTIARY_RECONCILIATION_VISIBLE_106.txt'),
    'status':'Browser shows active Stop and continuing reconciliation tool output; native idle is not treated as completion.',
    'newMessagesSent':0,'newFinalSuccessorReceived':False,'activeGenerationInterrupted':False,
    'visibleProposedChoices':['Pressure Wave push10ft, no Prone','Same actual emitter/interior witness for30ft/ray','Tail Sweep DEX13 after damage','Constrict paid fixedDC14 skill task escape, separate STR14 admission save','Constrict at most one category larger with free actual coil/contact'],
    'consequence':'New10ftpush can place recipient outside follow-up halberd reach; GPT is replacing that actual old trace. No interim choices or reported checks accepted by visibility alone.',
    'artifactLocalR105IsNotCheckpoint105':True}
d['previousGptObservationBefore106']=d.get('activeGptReviewAtLastVerifiedObservation')
d['activeGptReviewAtLastVerifiedObservation']={'threadId':'6ad4a867-f330-83e9-829e-bf2bb41a6c09','title':'Calibration Review Part 5','status':'active generation confirmed in browser','requestId':'c06ad34e-a672-44dc-af8f-462031ed7ddf','scope':'bounded five-fork bestiary final reconciliation'}
d['lastUsageObservation']={'usedPercent':72,'remainingPercent':28,'resetsAt':1793110625,'stopAtRemainingPercent':20,'source':'Fresh get_usage_limits after derived assembly106'}
d['nextAction']='Read and preserve the completed GPT R105 bestiary reconciliation when available; browser remains active so do not interrupt or send a competing prompt. Independently check actual final download hashes, exact before/after/mirror locators and distinguishing/replacement cases; no supplied-code execution. Continue parent335 FXC01-12 gate-to-evidence mapping using the completed106 candidate plus the106 acquisition appendix as the current acquisition/allowance authority. All660 original+28boundary semantic reviews and9cohorts are done; do not rerun them merely to increasecounts. Bind full current remaining dependencies and prepare exact full-candidate GPT submission after finite gates have evidence. Keep private comparison fields historical, deferred2null,525/323/249/173 and53accepted-unapplied, and four copy helpers unchanged. Canonical gameplay integration remains owner-reserved; no Unity checkout overlap. Whole-game joint agreement then authorized GitHub verification precedes cosmology.'
d['laterLocalWork']='73–106 remain local after last separately verified GitHub baseline;106 packages are new saved derived review artifacts, not a push or canonical application.'
backup=A/'navigation-before-feat-assembly-106';backup.mkdir()
nav=[];saved=[]
for n,b in enumerate(d['navigation']):
    p=G/b['path'];raw=p.read_bytes();target=backup/(str(n+1)+p.suffix);target.write_bytes(raw);saved.append(bind(target))
    text=raw.decode('utf-8-sig')
    link='docs/audit/2026-10-08/full-game/ACTIVE_AUTHORING_CHECKPOINT_FEAT_ASSEMBLY_106.json'
    summary='Checkpoint106 preserves the complete335 feat assembly,9chapters,660 original case reviews and28 boundaries. Copy/Ready and mental-predicate wording is synchronized;177 acquisition descriptors and15 historical evidence files are carried forward. Assembly3149 and acquisition1976 checks pass. Exact parent review and bestiary reconciliation remain open; no runtime or whole-game approval.'
    if p.suffix=='.html':
        insertion='<section class="sequence"><p><strong>Current review checkpoint:</strong> <a href="'+link+'">'+summary+'</a></p></section>\n'
        ck('HTML main insertion exists','<main>' in text);text=text.replace('<main>','<main>\n'+insertion,1)
    else:
        if p.name=='DEVELOPMENT_DIRECTION.md':link='../../../'+link
        first,rest=text.split('\n',1);text=first+'\n\n**Current review checkpoint:** [Checkpoint106]('+link+') '+summary+'\n'+rest
    p.write_text(text,encoding='utf-8');nav.append(bind(p))
d['navigation']=nav;d['preservedNavigation']=saved
P.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for b in saved:ck('Preserved prior navigation '+b['path'],bind(G/b['path'])==b)
check={'id':'CHECKPOINT106-REGISTRATION-CHECK','checkpoint':bind(P),'passed':len(checks),'failed':0,'checks':checks,'wholeGameComplete':False,'canonicalApplied':False}
Q=A/'ACTIVE_AUTHORING_CHECKPOINT_FEAT_ASSEMBLY_106_CHECK.json';Q.write_text(json.dumps(check,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for name in ['assemble_feat335_106.py','assemble_feat_acquisition_evidence_106.py','record_feat_assembly_106.py']:
    src=Path(__file__).parent/name;dst=A/name;assert not dst.exists();shutil.copy2(src,dst)
print(json.dumps({'checkpoint':bind(P),'check':bind(Q),'passed':len(checks),'failed':0,'usageRemainingPercent':28}))
