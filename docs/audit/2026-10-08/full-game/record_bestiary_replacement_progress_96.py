"""One-shot checkpoint: unavailable generated return, complete replacement dispatch and defense notes."""
from pathlib import Path
from copy import deepcopy
from datetime import datetime,timezone
import json,hashlib
G=Path(r'C:\Github\DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game'
PRE=A/'ACTIVE_AUTHORING_CHECKPOINT_CRAFTING_CASEBOOK_95.json';OUT=A/'ACTIVE_AUTHORING_CHECKPOINT_BESTIARY_REPLACEMENT_96.json';CHECK=A/'ACTIVE_AUTHORING_CHECKPOINT_BESTIARY_REPLACEMENT_96_CHECK.json';BACKUP=A/'navigation-before-bestiary-replacement-96';SAVED=A/Path(__file__).name
for p in (OUT,CHECK,BACKUP,SAVED):assert not p.exists(),str(p)
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
ck('Checkpoint95 exact',info(PRE)['sha256']=='a6ef28893f22e60f827f16b181456f24162d9a4d6f74de59d8c7640d7409f23e')
for row in [prior['currentAuthoredIndex'],prior['currentAcceptedInterfaceRegistry'],prior['currentWorkQueue'],*prior['canonicalHelperBaselinesUnchanged']]:ck('Protected baseline '+row['path'],info(G/row['path'])==row)
prep=A/'BESTIARY_REPLACEMENT_CONTEXT_PREPARATION_96.json';p=j(prep)
ck('Exact replacement preparation',info(prep)['sha256']=='08aaabace87ab2ebda413b02278c03ba663d68b176063a8a80d977eb36caf806')
ck('78 preparation checks pass',p['passed']==78 and p['failed']==0 and all(x['pass'] for x in p['checks']))
for row in p['sourceBindings']+p['externalCompleteArchives']+[p['archive']]:ck('Bound complete source '+row['path'],info(G/row['path'])==row)
defense=A/'FEAT335_DEFENSE_CASEBOOK_SEMANTIC_PREPARATION_96.json';d=j(defense)
ck('Exact defense preparation',info(defense)['sha256']=='c619605b328f2df50116731bcf9039c8bda191d80753cd6bf41988abb00adb32')
ck('31 full defense records62 notes4 boundaries',len(d['completeSelectedRecords'])==31 and len(d['originalCaseSemanticNotes'])==62 and len(d['additionalBoundarySemanticNotes'])==4 and d['completedCoverageRegisterUnchanged'])
for row in d['sourceBindings']:ck('Defense source unchanged '+row['path'],info(G/row['path'])==row)
cover=A/'FEAT335_ORIGINAL_CASEBOOK_REVIEW_COVERAGE_95.json';cv=j(cover)
ck('Completed coverage unchanged166 and6',info(cover)['sha256']=='dd20edf87f6ad527787a243864cf68d233d5db0bcac435abb52b52ac353fe006' and cv['ordinary']['reviewed']==166 and cv['additional']['reviewed']==6)
native=A/'GPT_BESTIARY_REPLACEMENT_SENT_NATIVE_96.json';n=j(native);request=A/'CODEX_BESTIARY_REPLACEMENT_DISPATCH_REQUEST_96.txt';sent=A/'GPT_BESTIARY_REPLACEMENT_SENT_96.txt';screen=A/'GPT_BESTIARY_REPLACEMENT_SENT_96.png'
ck('New actual GPT request native identity',n['turns'][0]['id']=='09fd693b-be2d-4274-bc1e-57ac20f4b422')
msgs=n['turns'][0]['items'];user=next(x for x in msgs if x['type']=='userMessage');text='\n'.join(x.get('text','') for x in user['content'] if x['type']=='text')
ck('Full replacement request appears in native record',request.read_text(encoding='utf-8').strip() in text)
for filename in ['DD_Bestiary_Linked_Recipe_Dependencies_91.zip','DD_Bestiary_Replacement_Current_Context_96.zip']:
 att=next(x for x in n['attachments'] if x['name']==filename);ck('Actual attached complete bytes '+filename,Path(att['path']).read_bytes()==(A/filename).read_bytes())
ck('Replacement generation active in saved browser observation','button "Stop"' in sent.read_text(encoding='utf-8'))
ck('Screenshot preserved',screen.stat().st_size>1000)
unavailable=A/'GPT_BESTIARY_DELIVERY_UNAVAILABLE_NATIVE_96.json';u=j(unavailable);reply=next(x for x in u['turns'][0]['items'] if x['type']=='agentMessage')
ck('Actual unavailable-file response identity',reply['id']=='875710e8-a844-446c-94f3-59d6f60839c0')
cp['id']='ACTIVE-AUTHORING-BESTIARY-REPLACEMENT-96';cp['recordedAtUtc']=datetime.now(timezone.utc).isoformat();cp['previousCheckpoint']=info(PRE)
cp['status']='Progress: preserved completed Bestiary response and explicit generated-file unavailability; received no Return01 MODEL/archive. Prepared and actually sent a complete new Return02 source conference with linked Fishing/Cooking sources and current accepted Resonance/FT84 authority. Defense31/62/4 semantic notes preserved; calculations/mirror verification pending, completed coverage unchanged166/660 and6/28.'
cp['previousGoalTurnClassification']={'turn':95,'classification':'progress','evidence':prior['featCraftingCasebook95']['report']}
cp['bestiaryUndeliveredReturn01_96']={'completedAssistant':'80ad9a5b-067f-41d6-b26c-3814fa6c49d2','fullResponse':info(A/'GPT_BESTIARY_COMPLETED_RESPONSE_96.txt'),'fullNativeRecord':info(A/'GPT_BESTIARY_COMPLETED_NATIVE_96.json'),'reportedArchiveName':'DD_Bestiary_Complete_Source_Part5_Return_01.zip','reportedBytes':54953665,'reportedSha256':'fdc494ae78b85573a08277eb7f6807c296d40ebf384800b16857289125db6ae7','reportedModelBytes':1251665,'reportedModelSha256':'8aa2fc0f74f5e9a144dd457c5ba22da0a0b418d97c1f651260969bb8fc922f1f','status':'PROPOSED_RESPONSE_PRESERVED_GENERATED_FILES_UNAVAILABLE_NOT_RECEIVED_NOT_VERIFIED_NOT_ACCEPTED','actualArchiveReceived':False,'independentIntakePerformed':False,'independentSemanticAcceptance':False,'fileFailureEvidence':info(A/'GPT_BESTIARY_DELIVERY_FAILURE_96.txt'),'repairRequest':info(A/'CODEX_BESTIARY_DELIVERY_REPAIR_REQUEST_96.txt'),'repairUser':'cce70381-6d2f-4b7f-8bf0-49dc9cf77ba9','repairAssistant':'875710e8-a844-446c-94f3-59d6f60839c0','repairResult':info(A/'GPT_BESTIARY_DELIVERY_UNAVAILABLE_RESPONSE_96.txt'),'repairNativeRecord':info(unavailable),'reconstructionPolicy':'New Return02 authoring must be newly identified against preserved original source bytes; old response-only claims are history, not exact lost model/case bytes.'}
cp['bestiaryReplacementDispatch96']={'status':'ACTUALLY_SENT_WITH_TWO_VERIFIED_COMPLETE_ATTACHMENTS_GPT_GENERATING','actualUser':'09fd693b-be2d-4274-bc1e-57ac20f4b422','threadId':'6ad4a867-f330-83e9-829e-bf2bb41a6c09','request':info(request),'nativeRecord':info(native),'browserEvidence':info(sent),'screenshot':info(screen),'currentContextPreparation':info(prep),'currentContextArchive':p['archive'],'linkedRecipeArchive':info(A/'DD_Bestiary_Linked_Recipe_Dependencies_91.zip'),'existingFullInputArchives':p['externalCompleteArchives'][:2],'linkedRecipeAndResonanceAcknowledgmentDelivered':True,'canonicalApplied':False,'independentAcceptance':False,'sealedDossiersRemainContainmentOnly':True}
cp['featDefensePreparation96']={'report':info(defense),'fullProceduresRead':31,'originalCaseNotes':62,'additionalBoundaryNotes':4,'completedCoverageAdded':0,'remaining':d['nextSteps'],'canonicalApplied':False,'runtimeExecuted':False}
cp['previousGptObservationBefore96']=deepcopy(prior['activeGptReviewAtLastVerifiedObservation'])
cp['activeGptReviewAtLastVerifiedObservation']={'conference':'Bestiary complete new Return02 replacement after generated Return01 files became unavailable','threadId':'6ad4a867-f330-83e9-829e-bf2bb41a6c09','actualUser':'09fd693b-be2d-4274-bc1e-57ac20f4b422','latestObservedStatus':'Browser Stop confirms new generation active; native request and both attached archive bytes verified. Do not interrupt.','latestObservation96':info(sent),'latestNativeRecord':info(native)}
cp['bestiaryActualDispatch89']['terminalDisposition96']='Response completed but generated files were unavailable. Full response-only history is preserved; no artifact receipt or acceptance. Superseded operationally by actual new complete-source Return02 dispatch96, not by a claimed byte-identical rebuild.'
cp['bestiaryNextSafeFollowup91']['deliveryUpdate96']='The91 recipe archive was actually uploaded in new replacement request96. The old91 follow-up text remains an unsent historical draft because it assumed a received complete baseline that proved unavailable. Use actual request96.'
cp['resonanceAcceptanceAcknowledgment90']['deliveryUpdate96']='Full original acknowledgment90 included unchanged in the actually uploaded current-context96 archive; exact accepted MODEL/procedures/holds supplied. Request96 explicitly states53 and acceptance scope. No canonical integration.'
cp['nextAction']='Do not interrupt new active Bestiary Return02. Finish defense casebook from complete preparation96: bounded arithmetic/state projections, actual source-position checks and full public/chapter mirrors, then add only completed62 originals/four boundaries to coverage. On actual replacement completion immediately preserve/download/inspect full files; do not infer receipt from links or claimed tests. Resolve any genuine remaining Bestiary questions using the two original full archives and now-delivered recipe91/current-context96 packets. All other goal and parent335 gates remain.'
cp['lastUsageObservation']={'usedPercent':57,'remainingPercent':43,'resetsAt':1793110625,'stopAtRemainingPercent':20,'source':'Fresh get_usage_limits at start96'}
cp['laterLocalWork']='Checkpoints73–96 remain local after latest separately verified GitHub backup through72; no push in96.'
nav=[G/'START_HERE.md',R/'docs/DEVELOPMENT_DIRECTION.md',G/'REVIEW_MAP.html'];old_nav={};prepared={}
for pth in nav:
 row=next(x for x in prior['navigation'] if x['path']==pth.relative_to(G).as_posix());ck('Exact navigation baseline '+pth.name,info(pth)==row);raw=old_nav[pth]=pth.read_bytes()
 if pth.suffix=='.html':
  pos=raw.find(b'>',raw.find(b'<body'))+1;note=('<aside><p><strong>Checkpoint96:</strong> Bestiary Return01 response is preserved but its generated files are unavailable and unaccepted. Complete new Return02 request sent with missing recipes/current rules. Defense31/62/4 notes prepared; completed feat-case coverage unchanged166/660 plus6/28. <a href="docs/audit/2026-10-08/full-game/'+OUT.name+'">Current record</a>.</p></aside>\n').encode()
 else:
  pos=raw.find(b'\n')+1;prefix='docs/audit/2026-10-08/full-game/' if pth.name=='START_HERE.md' else '../../../docs/audit/2026-10-08/full-game/';note=('\n**Current checkpoint — Bestiary replacement:** [Checkpoint96]('+prefix+OUT.name+') preserves the completed but undelivered Return01 response and explicit file-unavailability finding. A complete new Return02 review is now generating with the linked recipe cards and exact current accepted rules. Defense31 procedures/62 examples/four boundaries have semantic notes, with numerical/source-mirror verification pending; completed coverage remains166/660 and6/28. No canonical or runtime approval.\n').encode()
 ck('Valid insertion '+pth.name,pos>0);new=raw[:pos]+note+raw[pos:];ck('Every prior navigation byte preserved '+pth.name,new[:pos]+new[pos+len(note):]==raw);prepared[pth]=new
cp['navigation']=[planned(pth,prepared[pth]) for pth in nav];cp['preservedNavigation']=[planned(BACKUP/pth.name,old_nav[pth]) for pth in nav]
ck('Every prior checkpoint key retained',set(prior).issubset(cp));ck('No spell count or approval change',cp['authoredCounts']==prior['authoredCounts'] and cp['acceptedButUnapplied']==53 and not cp['implementationApplied'])
payload=enc(cp);script=Path(__file__).read_bytes();validation=enc({'id':'CHECKPOINT96-VALIDATION','checkpoint':planned(OUT,payload),'checks':checks,'passed':len(checks),'failed':0,'script':planned(SAVED,script),'newGptRequestsSent':2,'fullInputArchivesUploaded':2,'lostReturnAccepted':False})
BACKUP.mkdir()
for pth in nav:put(BACKUP/pth.name,old_nav[pth]);pth.write_bytes(prepared[pth])
put(SAVED,script);put(OUT,payload);put(CHECK,validation)
print(json.dumps({'checkpoint':info(OUT),'check':info(CHECK),'passed':len(checks),'failed':0,'newBestiaryRequest':cp['bestiaryReplacementDispatch96']['actualUser'],'completedCoverage':[166,6]},indent=2))
