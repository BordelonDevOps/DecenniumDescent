from pathlib import Path
import datetime,hashlib,json

G=Path(r'C:\Github\DecenniumDescent');A=G/'docs/audit/2026-10-08/full-game'
PREV=A/'ACTIVE_AUTHORING_CHECKPOINT_JOINT_REVIEW_108.json';OUT=A/'ACTIVE_AUTHORING_CHECKPOINT_JOINT_REVIEW_109.json'
assert not OUT.exists()
def j(p):return json.loads(p.read_bytes())
def bind(p):
    b=p.read_bytes();return {'path':p.relative_to(G).as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def ser(d):return (json.dumps(d,ensure_ascii=False,indent=2)+chr(10)).encode()
def write(p,b):
    with p.open('xb') as f:f.write(b)
checks=[]
def ck(n,v):checks.append({'name':n,'passed':bool(v)});assert v,n
d=j(PREV)
for b in d['canonicalHelperBaselinesUnchanged']+[d['currentAuthoredIndex'],d['currentAcceptedInterfaceRegistry']]:
    ck('Protected source unchanged '+b['path'],bind(G/b['path'])==b)
schedule=j(A/'BESTIARY_SCHEDULE_CONFIRMED_RECEIPT_109.json')
mapping=j(A/'FEAT335_NUMERIC_PHYSICAL_MAPPING_RECEIPT_109.json')
packet=j(A/'JOINT_FOLLOWTHROUGH_PACKET_109.json')
ck('Derived schedule confirmed with exact whole successor',schedule['passed']==111 and schedule['failed']==0 and schedule['successor']['sha256']=='61422722e9a599804e0d9f870135dcba8a4b9d2170b375d6011c09e79dbcf8fb')
ck('Numeric/physical finite map153checks',mapping['passed']==153 and mapping['failed']==0 and mapping['namedAreas']=={'FXC07':10,'FXC08':11})
ck('Prior four mismatches remain historical',j(A/'BESTIARY_RECONCILIATION_CASE_REVIEW_108.json')['failed']==4)
for group in [schedule,mapping]:
    for key in ['archive','report','successor','FXC07','FXC08','newExamples']:
        if key in group:
            b=group[key];actual=bind(Path(b['path']));ck('New artifact binding '+key,actual['bytes']==b['bytes'] and actual['sha256']==b['sha256'])
d.update(id='ACTIVE_AUTHORING_CHECKPOINT_JOINT_REVIEW_109',recordedAtUtc=datetime.datetime.now(datetime.timezone.utc).isoformat(),previousCheckpoint=bind(PREV))
d['status']='Progress: actual GPT schedule confirmation received and exact16-case successor built; all four schedule mismatches resolved without changing mechanics. Planar8-file and FXC06 follow-through actually submitted to GPT and still under live review. FXC07/08 complete named evidence maps and four additional boundary examples assembled locally.'
d['previousGoalTurnClassification']='108 made substantive progress: final bestiary reconstructed, exact four schedule defects identified, Planar eight-file successor and FXC06 map completed.109 resolves the schedule defects and continues the finite parent evidence assembly.'
d['bestiaryFinal108']['historicalPendingFixtureCorrection']=d['bestiaryFinal108'].pop('pendingFixtureCorrection')
d['bestiaryFinal108']['currentFixtureCorrection109']={'status':'EXACT_SUBMITTED_CORRECTION_CONFIRMED_AND_DERIVED','receipt':bind(A/'BESTIARY_SCHEDULE_CONFIRMED_RECEIPT_109.json'),'archive':schedule['archive'],'currentCompleteCasebook':schedule['successor'],'freshChecks':111,'failed':0,'originalCases':16,'changedCases':[8,9,10],'historicalFourMismatchReportUnchanged':True,'wholeBestiaryAccepted':False,'canonicalApplied':False}
d['gptScheduleExchange108'].update(status='Actual final confirmation received109; exact proposal unchanged. Current corrected complete casebook is in bestiary-schedule-confirmed-109/after.',correctionAppliedToCurrentCasebook=True,canonicalApplied=False,actuallyDownloaded=True,actualFinal=bind(A/'bestiary-schedule-confirmed-109/DD_Bestiary_Schedule_108_Confirmation_01.zip'),decision=bind(A/'bestiary-schedule-confirmed-109/decision/DECISION.json'),finalVisible=bind(A/'GPT_SCHEDULE_FINAL_109.txt'))
d['planarReferenceSuccessor108']['packageSentToGpt']=True
d['planarReferenceSuccessor108']['actualSubmission109']='DD_Joint_Followthrough_109.zip includes the full unchanged eight-file package; receipt-only claims replaced by actual upload/send evidence.'
d['featAcceptanceMapping109']={'receipt':bind(A/'FEAT335_NUMERIC_PHYSICAL_MAPPING_RECEIPT_109.json'),'package':mapping['archive'],'FXC07':mapping['FXC07'],'FXC08':mapping['FXC08'],'newExamples':mapping['newExamples'],'namedRequirementAreas':21,'historicalReferenceCases':169,'newBoundaryExamples':4,'checksPassed':153,'failed':0,'failedPackagingAttemptPreserved':bind(A/'FEAT335_NUMERIC_PHYSICAL_FAILED_ATTEMPT_109.json'),'currentDirectory':'docs/audit/2026-10-08/full-game/feat335-numeric-physical-109-v2','actuallySentToGpt':False,'remainingMaps':['FXC04 finite supplement table lifecycle','FXC05 exact acquisition/prerequisite/capacity branches','FXC09 current copy/Ready/command/ritual/plant'],'parentExactAccepted':False,'runtimeExecuted':False,'sourceQualification':'Full current feat/shared-rule records join complete semantic case reviews. Historical report scopes remain unmodified; fresh examples use existing mechanics and distinguish arithmetic from source-adjudicated state. These maps permit parent submission, not approval.'}
d['featAcceptanceMapping108']['remainingMaps']=d['featAcceptanceMapping109']['remainingMaps']
d['gptFollowthrough109']={'packet':packet,'request':bind(A/'GPT_FOLLOWTHROUGH_REQUEST_109.txt'),'actuallyUploaded':True,'actuallySent':True,'sentSnapshot':bind(A/'GPT_FOLLOWTHROUGH_SENT_109.txt'),'sentScreenshot':bind(A/'GPT_FOLLOWTHROUGH_SENT_109.png'),'latestSnapshot':bind(A/'GPT_FOLLOWTHROUGH_PROGRESS_109.txt'),'status':'Live Part5 visibly responding with Stop during the most recent observation; no final verdict claimed. It is inspecting the eight-file Planar mirror follow-through and actually supplied FXC06 full evidence map. Do not interrupt.','generationInterrupted':False}
d['lastUsageObservation']={'usedPercent':76,'remainingPercent':24,'resetsAt':1793110625,'stopAtRemainingPercent':20,'source':'Fresh get_usage_limits during109 after local numeric/physical assembly attempt'}
d['nextAction']='Read full goal and current allowance. Inspect live Calibration Review Part5 without interrupting active generation. Receive actual final bound109Planar/FXC06 follow-through verdict, preserve/download/verify its exact bytes and review any concrete issue. Schedule108 is settled:111local checks reproduce exact922913-byte complete16-case successor hash61422722...8fb; original4failure history remains. FXC03done107; FXC06done108 now in actual GPT review; FXC07/08maps done109-v2 with153checks and4newexamples, not yet submitted. Continue finite FXC04/05/09 maps without redoing660+28 completed cases or rerunning prior successful scripts. Use full335assembly106, ACQ106, current177allowance descriptors and eight Planar108complete overlays; build one complete parent candidate/evidence submission. Keep source-qualified/runtime/human/balance/world gates separate. Broader bestiary Return02 and other domains remain open. Owner-reserved canonical integration, sealed/privacy holds,525/323/249/173+53unapplied and separate Unity task remain protected. Finaljointflow then verifiedGitHubpush then carefulcosmology remains order.'
d['laterLocalWork']='73–109 remain local since the separately verified GitHub baseline. No Git push, canonical gameplay integration or cosmology changes in109.'
backup=A/'navigation-before-joint-review-109';backup.mkdir(exist_ok=False);nav=[];prior=[]
summary='GPT confirmed the exact bestiary schedule correction; the complete corrected examples preserve all mechanics and source history. Planar reference and time/work evidence are in live GPT review. Combat/healing and physical/social requirement maps are assembled; exact full-candidate review remains open.'
for i,b in enumerate(d['navigation']):
    p=G/b['path'];raw=p.read_bytes();bp=backup/(str(i+1)+p.suffix);write(bp,raw);prior.append(bind(bp));text=raw.decode('utf-8-sig')
    link='docs/audit/2026-10-08/full-game/ACTIVE_AUTHORING_CHECKPOINT_JOINT_REVIEW_109.json'
    if p.suffix=='.html':
        ck('HTML main exists','<main>' in text)
        text=text.replace('<main>','<main>'+chr(10)+'<section class="sequence"><p><strong>Current review checkpoint:</strong> <a href="'+link+'">Checkpoint109</a> '+summary+'</p></section>'+chr(10),1)
    else:
        if p.name=='DEVELOPMENT_DIRECTION.md':link='../../../'+link
        first,rest=text.split(chr(10),1);text=first+chr(10)*2+'**Current review checkpoint:** [Checkpoint109]('+link+') '+summary+chr(10)+rest
    p.write_text(text,encoding='utf8');nav.append(bind(p))
d['navigation']=nav;d['preservedNavigation']=prior
write(OUT,ser(d))
for b in prior:ck('Navigation history preserved '+b['path'],bind(G/b['path'])==b)
report={'id':'CHECKPOINT109-REGISTRATION','checkpoint':bind(OUT),'passed':len(checks),'failed':0,'checks':checks,'goalComplete':False}
checkpath=A/'ACTIVE_AUTHORING_CHECKPOINT_JOINT_REVIEW_109_CHECK.json';write(checkpath,ser(report));write(A/Path(__file__).name,Path(__file__).read_bytes())
print(json.dumps({'checkpoint':bind(OUT),'check':bind(checkpath),'passed':len(checks),'failed':0,'usageRemainingPercent':24}))
