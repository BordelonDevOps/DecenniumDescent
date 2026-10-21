from pathlib import Path
import datetime,hashlib,json
G=Path(r'C:\Github\DecenniumDescent');A=G/'docs/audit/2026-10-08/full-game'
PREV=A/'ACTIVE_AUTHORING_CHECKPOINT_JOINT_REVIEW_109.json';OUT=A/'ACTIVE_AUTHORING_CHECKPOINT_JOINT_REVIEW_111.json'
assert not OUT.exists()
def j(p):return json.loads(p.read_bytes())
def bind(p):
 b=p.read_bytes();return {'path':p.relative_to(G).as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def write(p,o):
 with p.open('x',encoding='utf8') as f:json.dump(o,f,ensure_ascii=False,indent=2);f.write('\n')
checks=[]
def ck(n,v):checks.append({'name':n,'passed':bool(v)});assert v,n
d=j(PREV)
for b in d['canonicalHelperBaselinesUnchanged']+[d['currentAuthoredIndex'],d['currentAcceptedInterfaceRegistry']]:ck('Protected unchanged '+b['path'],bind(G/b['path'])==b)
v=j(A/'JOINT_FOLLOWTHROUGH_VERDICT_RECEIPT_110.json');s=j(A/'FEAT335_FXC09_EXACT_MAPPING_RECEIPT_110.json');a=j(A/'FEAT335_FXC05_EXACT_MAPPING_RECEIPT_111.json')
for receipt in [v,s,a]:
 for k in ['archive','report','decision','coverage','sourceMap']:
  if k in receipt:
   b=receipt[k];p=Path(b['path']);actual=bind(p);ck('Artifact '+k+' '+p.name,actual['bytes']==b['bytes'] and actual['sha256']==b['sha256'])
ck('Actual Planar andFXC06 scoped verdict',v['currentPlanarMirrorsConfirmed']==8 and v['currentFXC06NamedAuthoredEvidenceCovered'] is True and v['passed']==46 and v['failed']==0)
ck('FXC05 complete source join',a['passed']==2152 and a['failed']==0 and a['namedAreas']==12)
d.update(id='ACTIVE_AUTHORING_CHECKPOINT_JOINT_REVIEW_111',recordedAtUtc=datetime.datetime.now(datetime.timezone.utc).isoformat(),previousCheckpoint=bind(PREV))
d['status']='Progress110–111: actual GPT Planar8-mirror and FXC06 scoped confirmations preserved. FXC07/08/09 actually sent and in GPT review. Current335 acquisition/capacity evidence map and complete four-gadget field review prepared. No parent335/canonical/runtime/whole-game approval.'
d['previousGoalTurnClassification']='110–111 made substantive progress: actual scoped decision intake; fullFXC09source/evidence assembly; actual07/08/09submission; twelve-area335acquisition mapping; four fullgadgetactivation/lifecycle reviews. No repeated blocker.'
d['gptFollowthrough109'].update(status='Actual final received110. Both submitted new scopes confirmed; no further Planar wording correction required.',actualFinalReceived=True,verdictReceipt=bind(A/'JOINT_FOLLOWTHROUGH_VERDICT_RECEIPT_110.json'),actualDecision=v['decision'],verdicts=v['verdicts'])
d['planarReferenceSuccessor108']['actualGptConfirmation110']=v['verdicts']['item2']
d['featAcceptanceMapping108']['actualGptFXC06Confirmation110']=v['verdicts']['item3']
d['featAcceptanceMapping109']['actuallySentToGpt']=True
d['featAcceptanceMapping109']['actualSubmission110']=bind(A/'FEAT335_FXC070809_PACKET_110.json')
d['featAcceptanceMapping110']={'receipt':bind(A/'FEAT335_FXC09_EXACT_MAPPING_RECEIPT_110.json'),'details':s,'actuallySentToGpt':True,'failedAttemptsPreserved':[bind(A/'FEAT335_FXC09_FAILED_ATTEMPT_110.json'),bind(A/'FEAT335_FXC09_FAILED_ATTEMPT2_110.json')],'scope':'13namedspell-stateareas,47completefeats,13nativecards,42currentReady,68oldcopyhistorieswithdispositions,35component31capture5supplementcases7defects127historicalcalculations. Historical scopes and Ready supersession exact; no runtime.'}
d['gptFXC070809Review110']={'request':bind(A/'GPT_FXC070809_REQUEST_110.txt'),'packet':bind(A/'FEAT335_FXC070809_PACKET_110.json'),'actualSent':True,'sentSnapshot':bind(A/'GPT_FXC070809_SENT_110.txt'),'sentScreenshot':bind(A/'GPT_FXC070809_SENT_110.png'),'progress111':bind(A/'GPT_FXC070809_PROGRESS_111.txt'),'status':'Latest saved observation showed active generation; no completed verdict claimed. Keep same tab and do not interrupt.','generationInterrupted':False}
if (A/'FEAT335_FXC070809_VERDICT_RECEIPT_111.json').exists():
 d['gptFXC070809Review110'].update(status='Actual completed verdict downloaded111; consult exact receipt for scoped decisions and any findings.',receipt=bind(A/'FEAT335_FXC070809_VERDICT_RECEIPT_111.json'),actualFinalReceived=True)
d['featAcceptanceMapping111']={'receipt':bind(A/'FEAT335_FXC05_EXACT_MAPPING_RECEIPT_111.json'),'details':a,'gadgetSubtable':bind(A/'FEAT335_FXC04_GADGET_SUBTABLE_REVIEW_111.json'),'packet':bind(A/'FEAT335_ACQUISITION_GADGET_PACKET_111.json'),'failedAttempt':bind(A/'FEAT335_FXC05_FAILED_ATTEMPT_111.json'),'actuallySentToGpt':(A/'GPT_ACQUISITION_GADGET_SENT_111.txt').exists(),'remaining':['FXC04remainingfinite supplement lifecycle/source joins; fourgadgetsubtableprepared, notfullgateclosure.','ExactGPTnamedFXC05review.','Completeparent335candidate/evidence assembly and exactreview.'],'parentAccepted':False,'runtimeExecuted':False}
d['requirementTextRepair111']={'receipt':bind(A/'FEAT335_REQUIREMENT_TEXT_RECEIPT_111.json'),'details':j(A/'FEAT335_REQUIREMENT_TEXT_RECEIPT_111.json'),'status':'Three empty source-requirement fields repaired in derived full-file copies using exact original contract. Frozen submissions retained. No gameplay change;16source/forward/reverse checks passed. Match actual GPT final proposed successor hashes when received.'}
if d['featAcceptanceMapping111']['actuallySentToGpt']:
 d['featAcceptanceMapping111']['sentSnapshot']=bind(A/'GPT_ACQUISITION_GADGET_SENT_111.txt');d['featAcceptanceMapping111']['sentScreenshot']=bind(A/'GPT_ACQUISITION_GADGET_SENT_111.png')
for k in ['featAcceptanceMapping108','featAcceptanceMapping109']:d[k]['remainingMaps']=d['featAcceptanceMapping111']['remaining']
d['lastUsageObservation']=j(A/'USAGE_OBSERVATION_111.json')
d['featAcceptanceMapping111']['maneuverSubtable']=bind(A/'FEAT335_FXC04_MANEUVER_SUBTABLE_REVIEW_111.json')
d['featAcceptanceMapping111']['laterPreparedUnsentPacket']=bind(A/'FEAT335_ACQUISITION_GADGET_DOC_PACKET_111.json')
d['gptFXC070809Review110']['actualVerdicts111']=j(A/'FEAT335_FXC070809_VERDICT_RECEIPT_111.json')['verdicts']
d['gptFXC070809Review110']['pendingCorrection']='F110-QT-MAP-01: /namedRequirementMap/6/meaning wrongly applies next-START expiry to initiative bank. Actual bank remains usable on any later actual encounter turn while maintained; separateBAspell mode restricts newReactions untilnextSTART. Review/reconstruct exactfinalfourmapoperations on continuation; do not inferfinalFXC09acceptance from interimGPToutput.'
d['status']='Stopped at user20%-remaining limit. Actual final53957-byteGPTverdict confirmsFXC07/08scope, requiresQuickenedThoughtmapcorrection forFXC09. Three documentaryparagraphs repaired beforelimit. FXC05all335map plus4gadget/6maneuverreviews prepared locally; nextGPTpacket remains unsent. Wholegame/parent335 remain open.'
d['nextAction']='Read goal and fresh allowance first. Respect user20%-remaining stop; resume development only within user authorization. Read live Calibration Review Part5 without interrupting generation. Receive actual07/08/09final if not already recorded, download/verify data-only decision, preserve exact scope/remaining gaps. Planar8mirrors andFXC06 alreadyconfirmed110. FXC05twelve-area335join completed111-v2 (2152checks0fail); fourgadgetfullsubtable reviewed111. PacketDD_Feat335_Acquisition_Gadgets_111.zip ready; check actuallySent flag before uploading, never duplicate send. Finish remaining FXC04finite tables and fullparent335 exactassembly using106+ACQ106+Planar108; inherit660+28fullreviews, do not rerun historical successful programs. Current fourgadget activation table exists; oldmissing-table note was a narrowerpacketqualification. Keep allworld/runtime/human/balance/whole-game gates. Owner-reserved canonical integration; separateUnitydeliverycheckout unchanged. Finaljointwholegameflow thenverifiedGitHubpush thencarefulcosmology.'
d['laterLocalWork']='73–111 local since last separately verified GitHub baseline. No push, canonical gameplay integration or cosmology changes by this turn.'
d['nextAction']='USER STOP REACHED:80%used/20%remaining. Goal paused at this explicit threshold; wait for userauthorization to resume. On resume: '+d['nextAction']+' Actual final differs from interimGPTdraft: onlyFXC07/08confirmed. Apply/review exactF110-QT-MAP-01mappingrepair together withthreealreadyindependentlyrepaired documentaryfields; preserve53957-bytefinal and alloldmaps. Do not reuse60648-byteinterimdraftidentity. Sixmaneuverfieldreview also localandunsent; include it in a freshpacket ifuseful. Currentprepared3953198-byteAcquisition_Gadgets_DocRepairpacket is unsent and doesnotincludeQuickenedThoughtrepair or sixmaneuverreview; updatefreshpackage before eventualsubmission.'
backup=A/'navigation-before-joint-review-111';backup.mkdir(exist_ok=False);nav=[];prior=[]
summary='Stopped at20%remaining as requested. GPT confirmed combat/healing and physical/social evidence and identified one Quickened Thought map timing correction. All335 acquisition records and four gadget/six maneuver profiles have local evidence reviews. The next GPT packet is prepared but unsent; full candidate and whole-game review remain open.'
for i,b in enumerate(d['navigation']):
 p=G/b['path'];raw=p.read_bytes();bp=backup/(str(i+1)+p.suffix)
 with bp.open('xb') as f:f.write(raw)
 prior.append(bind(bp));txt=raw.decode('utf-8-sig');link='docs/audit/2026-10-08/full-game/ACTIVE_AUTHORING_CHECKPOINT_JOINT_REVIEW_111.json'
 if p.suffix=='.html':
  ck('HTML main exists','<main>' in txt);txt=txt.replace('<main>','<main>\n<section class="sequence"><p><strong>Current review checkpoint:</strong> <a href="'+link+'">Checkpoint111</a> '+summary+'</p></section>\n',1)
 else:
  if p.name=='DEVELOPMENT_DIRECTION.md':link='../../../'+link
  first,rest=txt.split('\n',1);txt=first+'\n\n**Current review checkpoint:** [Checkpoint111]('+link+') '+summary+'\n'+rest
 p.write_text(txt,encoding='utf8');nav.append(bind(p))
d['navigation']=nav;d['preservedNavigation']=prior;write(OUT,d)
for b in prior:ck('Preserved navigation '+b['path'],bind(G/b['path'])==b)
report={'id':'CHECKPOINT111-REGISTRATION','checkpoint':bind(OUT),'passed':len(checks),'failed':0,'checks':checks,'goalComplete':False}
write(A/'ACTIVE_AUTHORING_CHECKPOINT_JOINT_REVIEW_111_CHECK.json',report)
with (A/Path(__file__).name).open('xb') as f:f.write(Path(__file__).read_bytes())
print(json.dumps({'checkpoint':bind(OUT),'passed':len(checks),'failed':0,'remainingPercent':d['lastUsageObservation']['remainingPercent']}))
