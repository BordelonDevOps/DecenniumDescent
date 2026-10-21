"""One-shot checkpoint: concrete healing progress, full Resonance intake, actual GPT conference."""
from pathlib import Path
from copy import deepcopy
from datetime import datetime,timezone
import json,hashlib
G=Path(r'C:\Github\DecenniumDescent');A=G/'docs/audit/2026-10-08/full-game'
PRE=A/'ACTIVE_AUTHORING_CHECKPOINT_FEAT_WORK_SEMANTIC_REVIEW_88.json'
OUT=A/'ACTIVE_AUTHORING_CHECKPOINT_HEALING_BESTIARY_DISPATCH_89.json'
CHECK=A/'ACTIVE_AUTHORING_CHECKPOINT_HEALING_BESTIARY_DISPATCH_89_CHECK.json'
SAVED=A/Path(__file__).name;BACKUP=A/'navigation-before-healing-bestiary-dispatch-89'
for p in [OUT,CHECK,SAVED,BACKUP]:assert not p.exists(),str(p)
def j(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def enc(x):return (json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode()
def info(p):
 b=p.read_bytes();return {'path':p.relative_to(G).as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
checks=[]
def ck(name,value):
 checks.append({'check':name,'pass':bool(value)});assert value,name
prior=j(PRE);cp=deepcopy(prior)
for row in [prior['currentAuthoredIndex'],prior['currentAcceptedInterfaceRegistry'],prior['currentWorkQueue'],*prior['canonicalHelperBaselinesUnchanged']]:ck('Canonical baseline unchanged '+row['path'],info(G/row['path'])==row)
healing=j(A/'FEAT335_HEALING_COMPOSITIONS_89.json');intake=j(A/'RANK9_RESONANCE_FIELDS3_RECEIPT_RETURN02_INTAKE_89.json')
ck('Healing56 cases405 passes',healing['caseCount']==56 and healing['passed']==405 and healing['failed']==0 and all(c['pass'] for c in healing['checks']))
ck('Healing15 full sources retained',len(healing['sourceBindings'])==15 and len(healing['fullSelectedFeatRecords'])==7)
ck('Resonance Return02 intake233 passes',intake['passed']==233 and intake['failed']==0 and all(c['pass'] for c in intake['checks']))
ck('Resonance source/semantic boundary remains pending',intake['fileCount']==50 and intake['incrementalOperations']==6 and not intake['semanticReviewComplete'] and not intake['exactAuthorshipAccepted'])
native=j(A/'GPT_BESTIARY_SENT_NATIVE_89.json');turn=native['turns'][0]
ck('Actual Bestiary dispatch turn',turn['id']=='5395ae3e-01ef-4b42-bae4-9c17af13f3fb')
message='\n'.join(c['text'] for i in turn['items'] if i['type']=='userMessage' for c in i['content'] if c['type']=='text')
draft=(A/'CODEX_BESTIARY_ACTUAL_DISPATCH_REQUEST_89.txt').read_text(encoding='utf-8')
ck('Complete actual message matches prepared draft',message.split('\n\n[User attached ')[0].strip()==draft.strip())
ck('Two actual attachment annotation','[User attached 2 files;' in message)
ack=(A/'CODEX_FT84_ACCEPTANCE_FOLLOWUP_88.txt').read_text(encoding='utf-8')
ck('Full prior FT84 acknowledgment actually sent',ack.strip() in message)
ck('Source archive exact',info(A/'DD_Bestiary_Complete_Source_Prepared_v3_81.zip')==prior['bestiaryNextDispatchArchives'][0])
ck('EX58 supplement exact',info(A/'DD_Bestiary_Current_EX58_Context_82.zip')==prior['bestiaryNextDispatchArchives'][1])
ck('Generation actually observed after dispatch','button "Stop"' in (A/'GPT_BESTIARY_SENT_89.txt').read_text(encoding='utf-8'))
complete=j(A/'GPT_RESONANCE_RECEIPT_COMPLETE_NATIVE_89.json')
ck('Completed Resonance assistant identified',any(x.get('id')=='83cafb84-ba74-462c-ac6e-0b45563d11d5' for x in complete['turns'][0]['items']))
cp['id']='ACTIVE-AUTHORING-HEALING-BESTIARY-DISPATCH-89';cp['recordedAtUtc']=datetime.now(timezone.utc).isoformat();cp['previousCheckpoint']=info(PRE)
cp['status']='Concrete progress:56 healing composition cases/405 checks preserved with15 full sources; complete Resonance Feedback Return02 downloaded,50files preserved and233 local intake/reconstruction checks passed; Bestiary V3 plus current EX58 source conference actually sent to GPT, which is responding. Canonical implementation unchanged.'
cp['previousGoalTurnClassification']={'turn':88,'classification':'progress','evidence':prior['completedFeatTimeInterfacesReturn01']['independentSemanticReview']}
cp['featHealingCompositions89']={'report':info(A/'FEAT335_HEALING_COMPOSITIONS_89.json'),'archive':info(A/'DD_Feat335_Healing_Compositions_89.zip'),'cases':56,'checks':405,'failures':0,'fullSourceFiles':15,'fullSelectedFeatRecords':7,'fullPrerequisiteRecords':1,'runtimeTestsExecuted':0,'parent335Accepted':False,'sentToGpt':False,'summaryActuallyReportedToGpt':True,'remainingScope':healing['remainingScope']}
cp['healingSourcePreparation87']['diagnosticsWritten']=True
cp['healingSourcePreparation87']['followThrough89']=info(A/'FEAT335_HEALING_COMPOSITIONS_89.json')
cp['healingSourcePreparation87']['status']='Earlier preparation fulfilled by the bounded89 diagnostics; all original source findings retained. This does not close the parent335 or all healing interactions.'
cp['completedResonanceReceiptReturn02']={'actualUserTurn':'5ee6be18-389e-400a-9f43-739f5ce09243','actualAssistant':'83cafb84-ba74-462c-ac6e-0b45563d11d5','native':info(A/'GPT_RESONANCE_RECEIPT_COMPLETE_NATIVE_89.json'),'browser':info(A/'GPT_RESONANCE_RECEIPT_COMPLETE_89.txt'),'archive':intake['archive'],'model':intake['model'],'intake':info(A/'RANK9_RESONANCE_FIELDS3_RECEIPT_RETURN02_INTAKE_89.json'),'intakeChecks':233,'files':50,'incrementalOperations':6,'completeArtifactReplacements':12,'fullReceiptContractRead':True,'full31DiagnosticSemanticReviewComplete':False,'exactAuthorshipAccepted':False,'canonicalApplied':False,'reportedGptDiagnostics':intake['reportedGptDiagnostics'],'nextReview':'Read all31 receipt diagnostics and their exact source-qualified inputs; independently check two full branch receipt additions, old-state stripping, payment/award, source-key replay, spent-round denial, next-round eligibility and invalid persistence boundaries. Preserve all original3procedures/6shared/24questions/7main/28branches and four conditional branches.'}
cp['currentResonanceReceiptActualDispatch']['completedResponseReceived']=True
cp['currentResonanceReceiptActualDispatch']['activeGenerationVerified']=False
cp['currentResonanceReceiptActualDispatch']['latestObservedStatus']='Completed Return02 received89; full semantic reconciliation remains next.'
cp['completedFeatTimeInterfacesReturn01']['acknowledgmentActuallySent']=True
cp['completedFeatTimeInterfacesReturn01']['acknowledgmentActualUserTurn']=turn['id']
dispatch={'threadId':'6ad4a867-f330-83e9-829e-bf2bb41a6c09','threadTitle':'Calibration Review Part 5','group':'complete-bestiary-v3-current-ex58-source-conference','actualUserTurn':turn['id'],'request':info(A/'CODEX_BESTIARY_ACTUAL_DISPATCH_REQUEST_89.txt'),'attachments':prior['bestiaryNextDispatchArchives'],'native':info(A/'GPT_BESTIARY_SENT_NATIVE_89.json'),'browserObservation':info(A/'GPT_BESTIARY_SENT_89.txt'),'screenshot':info(A/'GPT_BESTIARY_SENT_89.png'),'activeGenerationVerified':True,'completedResponseReceived':False,'latestObservedStatus':'ChatGPT responding to complete6582-character message and two verified attached source archives. No final return yet.','boundary':'No sealed-dossier content review or new cosmology; owner-reserved canonical implementation unchanged.'}
cp['previousGptObservationBefore89']=prior['activeGptReviewAtLastVerifiedObservation'];cp['activeGptReviewAtLastVerifiedObservation']=dispatch;cp['bestiaryActualDispatch89']=dispatch
cp['bestiaryPreparationLabelsAreHistoricalAfter89']='The inherited fields named bestiaryUnsentArchive/bestiaryNextDispatchArchives/bestiaryNextDispatchRequest preserve original preparation bindings. The two archives were actually sent in turn5395ae3e-01ef-4b42-bae4-9c17af13f3fb; do not resend merely because an older filename/field/status says UNSENT.'
cp['nextAction']='Independently complete Resonance Return02 receipt semantic review while GPT develops the already-dispatched Bestiary V3/current EX58 conference. Then continue parent335 remaining physical/social/world-copy and exact semantic gates; the healing packet is locally prepared but not submitted for parent acceptance. Preserve all accepted-unapplied packages and whole-positive-case holds; no canonical integration without the owner-reserved implementation path.'
cp['lastUsageObservation']={'usedPercent':51,'remainingPercent':49,'resetsAt':1793110625,'stopAtRemainingPercent':20,'source':'Fresh get_usage_limits near end89'}
cp['laterLocalWork']='Checkpoints73–89 remain local after the last separately verified GitHub backup through72; no push in89.'
nav=[G/'START_HERE.md',G/'DescentReviewChanges/ReviewBible/docs/DEVELOPMENT_DIRECTION.md',G/'REVIEW_MAP.html'];old={p:p.read_bytes() for p in nav};prepared={}
for p in nav:
 if p.suffix=='.html':
  pos=old[p].find(b'>',old[p].find(b'<body'))+1
  notice=('<aside><p><strong>Checkpoint89:</strong> Healing56 cases/405 checks; Resonance receipt return preserved with233 intake checks; complete Bestiary V3/current EX58 review now with GPT. <a href="docs/audit/2026-10-08/full-game/'+OUT.name+'">Current record</a>. Canonical files unchanged.</p></aside>\n').encode()
 else:
  rel='docs/audit/2026-10-08/full-game/' if p.name=='START_HERE.md' else '../../../docs/audit/2026-10-08/full-game/'
  pos=old[p].find(b'\n')+1
  notice=('\n**Current checkpoint — 20 October 2026:** [Checkpoint89]('+rel+OUT.name+') preserves56 healing cases/405 checks and the complete Resonance Feedback return with233 intake checks. The complete Bestiary V3/current EX58 conference was actually sent and GPT is responding. Resonance receipt semantics remain under review; canonical files and525/323/249/173 coverage with50 accepted-unapplied spell identities are unchanged.\n').encode()
 ck('Valid insertion '+p.name,pos>0);new=old[p][:pos]+notice+old[p][pos:];ck('All earlier navigation bytes retained '+p.name,new[:pos]+new[pos+len(notice):]==old[p]);prepared[p]=new
ck('Every prior checkpoint field retained',set(prior).issubset(cp))
ck('Counts/implementation unchanged',cp['authoredCounts']==prior['authoredCounts'] and cp['acceptedButUnapplied']==50 and not cp['implementationApplied'])
BACKUP.mkdir();preserved=[]
for p in nav:
 dst=BACKUP/p.name
 with dst.open('xb') as f:f.write(old[p])
 preserved.append(info(dst));p.write_bytes(prepared[p])
cp['navigation']=[info(p) for p in nav];cp['preservedNavigation']=preserved
with SAVED.open('xb') as f:f.write(Path(__file__).read_bytes())
with OUT.open('xb') as f:f.write(enc(cp))
result={'id':'CHECKPOINT89-VALIDATION','checkpoint':info(OUT),'checks':checks,'passed':len(checks),'failed':0,'script':info(SAVED)}
with CHECK.open('xb') as f:f.write(enc(result))
print(json.dumps({'checkpoint':info(OUT),'check':info(CHECK),'passed':len(checks),'failed':0,'activeGptUserTurn':turn['id']},indent=2))
