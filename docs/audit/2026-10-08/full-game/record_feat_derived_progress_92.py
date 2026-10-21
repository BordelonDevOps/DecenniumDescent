"""One-shot source-preserving checkpoint of the derived FT84 review copy."""
from pathlib import Path
from copy import deepcopy
from datetime import datetime,timezone
import json,hashlib

G=Path(r'C:\Github\DecenniumDescent');A=G/'docs/audit/2026-10-08/full-game'
PRE=A/'ACTIVE_AUTHORING_CHECKPOINT_PHYSICAL_SOCIAL_RECIPES_91.json'
OUT=A/'ACTIVE_AUTHORING_CHECKPOINT_FEAT_DERIVED_MIRRORS_92.json'
CHECK=A/'ACTIVE_AUTHORING_CHECKPOINT_FEAT_DERIVED_MIRRORS_92_CHECK.json'
BACKUP=A/'navigation-before-feat-derived-mirrors-92';SAVED=A/Path(__file__).name
for p in (OUT,CHECK,BACKUP,SAVED):assert not p.exists(),str(p)
def j(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def enc(v):return (json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode()
def info(p):
 b=p.read_bytes();return {'path':p.relative_to(G).as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def planned(p,b):return {'path':p.relative_to(G).as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def put(p,b):
 with p.open('xb') as f:f.write(b)
checks=[]
def ck(name,ok):checks.append({'check':name,'pass':bool(ok)});assert ok,name
prior=j(PRE);cp=deepcopy(prior)
ck('Checkpoint91 exact',info(PRE)['sha256']=='993cf2e08c0ad4ff5f37365b6f7417ef2d9f9cd602ecad514867d646edc94e5f')
for row in [prior['currentAuthoredIndex'],prior['currentAcceptedInterfaceRegistry'],prior['currentWorkQueue'],*prior['canonicalHelperBaselinesUnchanged']]:ck('Protected canonical baseline '+row['path'],info(G/row['path'])==row)
rp=A/'FEAT335_FT84_DERIVED_MIRROR_RECONCILIATION_92.json';r=j(rp)
vp=A/'FEAT335_FT84_DERIVED_OPERATIONS_VERIFICATION_92.json';v=j(vp)
archive=A/'DD_Feat335_Derived_Review_Candidate_92.zip'
ck('Exact derived report',info(rp)['sha256']=='398405bb7f540f548992323f36c7eac29bea04fc920bd0e624bf76662fe44245')
ck('Exact derived archive',info(archive)['sha256']=='a7abb70b7c0c2e105cde5858eba68bbb63a267456a60ee3fbfd8ac7e84178363')
ck('Derived reconstruction3040 checks passed',r['passed']==3040 and r['failed']==0 and all(x['pass'] for x in r['checks']))
ck('Eleven new operations independently reconstructed',v['passed']==78 and v['failed']==0 and sum(x['operationCount'] for x in v['operations'])==11 and all(x['pass'] for x in v['checks']))
ck('34 complete artifacts and15 changed artifacts',r['completeArtifactCount']==34 and r['changedArtifactCount']==15 and r['newDerivedMirrorCount']==8)
ck('Full source identity and casebook counts retained',r['authoringIdentityCounts']=={'internal':327,'originalRegistry':335,'public':335,'unchangedReviewed':8,'ordinaryOriginalCasePositions':660,'additionalBoundaryPositions':28,'cohortManuscripts':9,'changedFeatProcedures':6})
ck('Preexisting differences retained',len(r['preexistingPublicInternalProcedureDifferences'])==3 and r['preexistingPublicSharedDifference']['ruleId']=='FS-08')
ck('No parent or runtime approval',not r['parent335Accepted'] and not r['canonicalImplementationApplied'] and r['runtimeTestsExecuted']==0)
notebook=A/'GPT_PERTINENT_RECHECK_92.json';n=j(notebook)
obs=A/'GPT_BESTIARY_ACTIVE_OBSERVATION_92.txt'
ck('Actual browser remains active','button "Stop"' in obs.read_text(encoding='utf-8'))
ck('No unseen completed decision',not n['newCompletedDecisionSincePreviousCheck'])
ck('No new message or upload',not n['newGptMessageSent'] and not r['actuallySentToGpt'])

cp['id']='ACTIVE-AUTHORING-FEAT-DERIVED-MIRRORS-92';cp['recordedAtUtc']=datetime.now(timezone.utc).isoformat();cp['previousCheckpoint']=info(PRE)
cp['status']='Progress: complete isolated FT84 derived review copy prepared with34 complete before/after artifacts; six accepted procedures carried through15 affected files. Eight newly rendered mirrors verified through11 reversible operations. Existing copy-release differences preserved and explicitly flagged. Bestiary GPT response still active.'
cp['previousGoalTurnClassification']={'turn':91,'classification':'progress','evidence':prior['featPhysicalSocial91']['report']}
cp['featDerivedMirrors92']={'report':info(rp),'archive':info(archive),'independentOperationVerification':info(vp),'fullArtifactCount':34,'changedArtifactCount':15,'existingAcceptedSuccessorCount':7,'newMirrorCount':8,'newOperationCount':11,'sourceAndReconstructionChecks':3040,'separateOperationChecks':78,'failures':0,'counts':r['authoringIdentityCounts'],'existingCopyReleaseDifferences':r['preexistingPublicInternalProcedureDifferences'],'existingSharedDifference':r['preexistingPublicSharedDifference'],'remainingScope':r['remainingScope'],'qualification':'These are full-file preservation, exact selected-text, source alignment and reconstruction checks. The entire660+28 casebook has been retained, not newly semantically reviewed or executed. No runtime or parent acceptance.','inverseFormattingQualification':'Two language JSON originals have formatting different from default serialization. Inverse operations recover their complete JSON values; preserved full before files restore original bytes exactly.','actuallySentToGpt':False,'canonicalApplied':False,'parent335Accepted':False,'runtimeTestsExecuted':0}
cp['pertinentNotebookRecheck92']={'record':info(notebook),'latestUnityUser':n['latestUnityUser'],'latestUnityAssistant':n['latestUnityAssistant'],'latestCompletedCalibrationAssistant':n['latestCompletedCalibrationAssistant'],'activeCalibrationRequest':n['activeCalibrationRequest'],'result':'Latest completed decisions already preserved in current ledger and Unity brief. Active Bestiary output is not a completed verdict. No new send; current source supplement remains unsent.'}
cp['previousGptObservationBefore92']=deepcopy(prior['activeGptReviewAtLastVerifiedObservation'])
cp['activeGptReviewAtLastVerifiedObservation']['latestObservation92']=info(obs)
cp['activeGptReviewAtLastVerifiedObservation']['latestObservedStatus']='Live browser still exposes Stop while reading Bestiary source/current EX58. No final Bestiary result received; no interruption or resend.'
cp['bestiaryActualDispatch89']['latestObservation92']=info(obs)
cp['nextAction']='Continue the full original660+28 feat casebook and native/world/copy interface work. Preserve the independent FT84 derived candidate92; it does not replace separate copy-release/preparation-only successor packages. When GPT finishes Bestiary, download/preserve/inspect its full return and perform intake before sending the prepared Fishing/Cooking dependency supplement and Resonance acceptance acknowledgment. No duplicate full Bestiary conference. Canonical implementation stays owner-reserved.'
cp['lastUsageObservation']={'usedPercent':55,'remainingPercent':45,'resetsAt':1793110625,'stopAtRemainingPercent':20,'source':'Fresh get_usage_limits near checkpoint92'}
cp['laterLocalWork']='Checkpoints73–92 remain local after the last separately verified GitHub backup through72; no push in92.'
nav=[G/'START_HERE.md',G/'DescentReviewChanges/ReviewBible/docs/DEVELOPMENT_DIRECTION.md',G/'REVIEW_MAP.html'];old={};prepared={}
for p in nav:
 row=next(x for x in prior['navigation'] if x['path']==p.relative_to(G).as_posix());ck('Exact previous navigation '+p.name,info(p)==row)
 raw=old[p]=p.read_bytes()
 if p.suffix=='.html':
  pos=raw.find(b'>',raw.find(b'<body'))+1
  note=('<aside><p><strong>Checkpoint92:</strong> Six accepted feat work-rule revisions reconciled in an isolated34-artifact review copy; original335 identities and660+28 cases preserved. Existing copy-release differences retained; parent335 pending. <a href="docs/audit/2026-10-08/full-game/'+OUT.name+'">Current record</a>. GPT Bestiary response still active; canonical files unchanged.</p></aside>\n').encode()
 else:
  pos=raw.find(b'\n')+1;prefix='docs/audit/2026-10-08/full-game/' if p.name=='START_HERE.md' else '../../../docs/audit/2026-10-08/full-game/'
  note=('\n**Current checkpoint — derived feat review:** [Checkpoint92]('+prefix+OUT.name+') preserves the six accepted FT84 work-rule revisions across complete feat/shared/language mirrors in an isolated review copy. All335 identities and660+28 case positions remain; three existing copy-feat differences and the FS-08 public addendum are retained for their separate successor integration. Parent335 remains pending. GPT Bestiary generation is still active; no canonical application or new send occurred.\n').encode()
 ck('Valid navigation insertion '+p.name,pos>0);new=raw[:pos]+note+raw[pos:];ck('Complete previous navigation preserved '+p.name,new[:pos]+new[pos+len(note):]==raw);prepared[p]=new
cp['navigation']=[planned(p,prepared[p]) for p in nav]
cp['preservedNavigation']=[planned(BACKUP/p.name,old[p]) for p in nav]
ck('All previous checkpoint fields retained',set(prior).issubset(cp))
ck('No count or approval change',cp['acceptedButUnapplied']==53 and cp['authoredCounts']==prior['authoredCounts'] and not cp['implementationApplied'])
payload=enc(cp);saved=Path(__file__).read_bytes()
validation={'id':'CHECKPOINT92-VALIDATION','checkpoint':planned(OUT,payload),'checks':checks,'passed':len(checks),'failed':0,'script':planned(SAVED,saved),'anyNewGptMessageSent':False}
validation_bytes=enc(validation)
BACKUP.mkdir()
for p in nav:put(BACKUP/p.name,old[p]);p.write_bytes(prepared[p])
put(SAVED,saved);put(OUT,payload);put(CHECK,validation_bytes)
print(json.dumps({'checkpoint':info(OUT),'check':info(CHECK),'passed':len(checks),'failed':0,'newGptMessageSent':False},indent=2))
