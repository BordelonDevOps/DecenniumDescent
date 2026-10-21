from pathlib import Path
from datetime import datetime, timezone
import json, hashlib

G=Path(r'C:\Github\DecenniumDescent')
R=G/'DescentReviewChanges/ReviewBible'
A=G/'docs/audit/2026-10-08/full-game'
OLD=A/'ACTIVE_AUTHORING_CHECKPOINT_RESONANCE_INTAKE_FEAT_RESOLUTION_85.json'
OUT=A/'ACTIVE_AUTHORING_CHECKPOINT_RESONANCE_SEMANTIC_REVIEW_86.json'
CHECK=A/'ACTIVE_AUTHORING_CHECKPOINT_RESONANCE_SEMANTIC_REVIEW_86_CHECK.json'
BACK=A/'navigation-before-resonance-semantic-review-86'
SCRIPT=A/Path(__file__).name
for p in [OUT,CHECK,BACK,SCRIPT]:assert not p.exists(),p
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def encode(v):return (json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
def info(p):
    b=p.read_bytes()
    return {'path':p.relative_to(G).as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
checks=[]
def ck(label,ok):
    checks.append({'check':label,'pass':bool(ok)})
    assert ok,label
cp=read(OLD)
ck('Exact successful checkpoint85',info(OLD)['sha256']=='85dbee021b475d48bab8b441363006d308ad3c09671493627687ef93e38d0020')
oldcheck=read(A/'ACTIVE_AUTHORING_CHECKPOINT_RESONANCE_INTAKE_FEAT_RESOLUTION_85_CHECK.json')
ck('Prior54checkpoint checks passed',oldcheck['checkCount']==54 and oldcheck['failures']==0 and oldcheck['checkpoint']==info(OLD))
diagpath=A/'RANK9_RESONANCE_FIELDS3_INDEPENDENT_SEMANTIC_CHECK_86.json'
diag=read(diagpath)
ck('Independent3099checks passed',diag['checkCount']==3099 and not diag['failures'] and all(c['passed'] for c in diag['checks']))
ck('All35cases134transitions inspected',diag['reviewed']['positiveCases']==7 and diag['reviewed']['branches']==28 and diag['computedCounts']['transitions']==134)
ck('Narrow Feedback question preserved at both exact locations',len(diag['openFindings'])==2)
for row in diag['sourceBindings']:
    actual=info(Path(row['path']))
    ck('Exact reviewed artifact '+Path(row['path']).name,actual['bytes']==row['bytes'] and actual['sha256']==row['sha256'])
prep_path=A/'RESONANCE_FIELDS3_RECEIPT_FOLLOWTHROUGH_PREPARATION_86.json'
prep=read(prep_path)
ck('Follow-through prepared but not sent',prep['status']=='PREPARED_UNSENT')
for key in ['archive','request','manifest']:
    row=prep[key];actual=info(Path(row['path']))
    ck('Exact prepared '+key,actual['bytes']==row['bytes'] and actual['sha256']==row['sha256'])
protected=[cp['currentAuthoredIndex'],cp['currentAcceptedInterfaceRegistry'],cp['currentWorkQueue'],*cp['canonicalHelperBaselinesUnchanged']]
for row in protected:ck('Protected authority '+row['path'],info(G/row['path'])==row)
progress=A/'GPT_FEAT_TIME_INTERFACES_PROGRESS_86.txt'
text=progress.read_text(encoding='utf-8')
ck('Live same three-question feat conference',all(s in text for s in ['Working for 18m 44s','button "Stop"','FT84-Q01','FT84-Q02','FT84-Q03','4-hour qualifying written ritual copies','Finalizing bounded language and crafting review documentation']))
navs=[G/'START_HERE.md',R/'docs/DEVELOPMENT_DIRECTION.md',G/'REVIEW_MAP.html']
for row in cp['navigation']:ck('Prior navigation exact '+row['path'],info(G/row['path'])==row)
originals={p:p.read_bytes() for p in navs}
BACK.mkdir()
for p,b in originals.items():(BACK/p.name).write_bytes(b)
base='docs/audit/2026-10-08/full-game/'
for p,prefix in [(navs[0],''),(navs[1],'../../../')]:
    b=originals[p];pos=b.index(b'\n')+1
    notice=('\n**Current checkpoint — 20 October 2026:** [Checkpoint86]('+prefix+base+OUT.name+') records full semantic reading of the Resonance3 procedures,24dispositions and35scenarios.3099independent local checks pass. One durable Arcane Feedback usage question at2case locations remains for GPT; a complete follow-through packet is prepared but unsent while GPT finishes the3feat timing questions. Applied525/323/249,173interfaces and50accepted-unapplied remain unchanged. [75-domain map]('+prefix+base+'FULL_GAME_CURRENT_REVIEW_MAP_82.md).\n').encode('utf-8')
    p.write_bytes(b[:pos]+notice+b[pos:])
    ck('All prior navigation bytes retained '+p.name,p.read_bytes().replace(notice,b'',1)==b)
p=navs[2];b=originals[p];pos=b.index(b'</h1>')+5
notice=('<section class="sequence" aria-label="Current Resonance semantic review"><p><strong>Checkpoint86: all35 Resonance scenarios read.</strong>3099independent local source,price,resource and arithmetic checks pass. One Feedback usage-record question remains before exact acceptance. GPT is finishing3feat timing dispositions. <a href="'+base+OUT.name+'">Current checkpoint</a> · <a href="'+base+'FULL_GAME_CURRENT_REVIEW_MAP_82.md">75-domain map</a></p></section>').encode('utf-8')
p.write_bytes(b[:pos]+notice+b[pos:]);ck('All prior HTML bytes retained',p.read_bytes().replace(notice,b'',1)==b)
cp['previousGptObservationBefore86']=cp['activeGptReviewAtLastVerifiedObservation']
cp['activeGptReviewAtLastVerifiedObservation']={**cp['activeGptReviewAtLastVerifiedObservation'],'browserObservation':info(progress),'activeGenerationVerified':True,'completedResponseReceived':False,'latestObservedStatus':'Same actual FT84-Q01–Q03 review active at18m44s; finalizing documentation. Preliminary commentary selects4h/rank qualifying written ritual-copy route versus8h/rank teacher route,5minute Contraption and15minute Trapsetter with Craftsman; final exact artifacts not yet received or independently accepted.'}
cp['completedResonanceFields3Return01']['sharedRulesQuestionsAndFullCaseSemanticReviewComplete']=True
cp['completedResonanceFields3Return01']['independentExactAcceptance']=False
cp.update(id='ACTIVE-AUTHORING-RESONANCE-SEMANTIC-REVIEW-86',recordedAtUtc=datetime.now(timezone.utc).isoformat(),previousCheckpoint=info(OLD),
 status='Complete Resonance authored-case semantic reading with3099finite independent checks passed; one durable Feedback once-per-round receipt question remains at2locations. Exact acceptance unchanged. Follow-through source packet prepared and unsent while same live GPT feat timing conference finishes.',
 currentResonanceFields3SemanticReview={'diagnostics':info(diagpath),'reviewed':diag['reviewed'],'computedCounts':diag['computedCounts'],'checkCount':3099,'failures':0,'openFindings':diag['openFindings'],'meaning':'Source/acquisition, finite authored state, price, resource and arithmetic review only. No downloaded code or canonical game runtime executed; no balance or release claim. Native source-qualified deadlines checked, including Influence actual tenth future START63 instead of guessed elapsed63.2.','independentExactAcceptance':False,'nextConferencePreparation':info(prep_path),'preparedArchive':info(Path(prep['archive']['path'])),'preparedRequest':info(Path(prep['request']['path'])),'dispatchStatus':'UNSENT_WHILE_EXISTING_GPT_GENERATION_ACTIVE'},
 navigation=[info(p) for p in navs],preservedNavigation=[info(BACK/p.name) for p in navs],
 lastUsageObservation={'usedPercent':46,'remainingPercent':54,'stopAtRemainingPercent':20,'resetsAt':1793110625},
 previousGoalTurnClassification='Concrete progress: full35Resonance scenario review, actual source comparisons,3099independent checks of134transitions/56casts/22damage applications/16conversion settlements; one narrow source-use-history question identified, fully prepared for GPT. No blocking condition.',
 laterLocalWork='All73–86work remains local after the verified GitHub backup through72.',
 nextAction='Receive the same live feat time3 return without interruption, preserve and independently review exact wording/fullcases. When GPT finishes, send the complete prepared Resonance receipt follow-through packet and verified request; preserve actual sent-message proof. Reconcile Feedback history before exact independent Resonance acceptance. Continue full335 remaining healing/reserve/world/composition gates and prepared Bestiary V3+EX58. Keep all75domain and whole-game gates open; canonical implementation remains reserved.')
OUT.write_bytes(encode(cp))
for row in protected:ck('Authority unchanged at completion '+row['path'],info(G/row['path'])==row)
SCRIPT.write_bytes(Path(__file__).read_bytes())
CHECK.write_bytes(encode({'checkpoint':info(OUT),'checks':checks,'checkCount':len(checks),'failures':0,'newRuleAdoptions':0,'newDomainClosures':0,'canonicalImplementationApplied':False,'runtimeTestsExecuted':0,'sourceInformationDeleted':0}))
print(json.dumps({'checkpoint':info(OUT),'check':info(CHECK),'checks':len(checks),'failures':0}))
