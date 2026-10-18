"""Record actual returns and staged integration without adopting pending rules."""
from pathlib import Path
from copy import deepcopy
from collections import Counter
from datetime import datetime, timezone
import hashlib, json, re

G=Path(r'C:\Github\DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game'
def raw(p):return Path('\\\\?\\'+str(p)).read_bytes()
def obj(p):return json.loads(raw(p))
def enc(v):return (json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
def info(p,b=None):
 b=raw(p) if b is None else b
 return {'path':p.relative_to(G).as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def main():
 now=datetime.now(timezone.utc).isoformat(); oldq=R/'data/director/spell_review/remaining_work_queue_27.json';newq=oldq.with_name('remaining_work_queue_28.json'); cp=A/'ACTIVE_AUTHORING_CHECKPOINT_PART5_ACCEPTED_STAGING_35.json';check=A/'ACTIVE_AUTHORING_CHECKPOINT_PART5_ACCEPTED_STAGING_35_CHECK.json';keep=A/'navigation-before-part5-accepted-staging-35'
 assert not any(p.exists() for p in [newq,cp,check,keep])
 idx=R/'data/public/spell_playtests/authored_review_index.json';cat=idx.with_name('catalog.json');cov=R/'data/playtest/game_development_coverage.json';registry=R/'data/director/spell_review/accepted_interface_registry_06.json'
 unchanged={p:raw(p) for p in [idx,cat,cov,registry,oldq]};checks=[]
 def ck(n,v):checks.append({'check':n,'passed':bool(v)});assert v,n
 planp=A/'part5-accepted24-integration-staging-01/INTEGRATION_PLAN.json';plan=obj(planp);stagingcheck=A/'PART5_ACCEPTED24_INTEGRATION_STAGING_01_CHECK.json';q0=obj(oldq);q=deepcopy(q0)
 ck('Staged plan is expressly unapplied',plan['liveIndexModified'] is False and plan['canonicalDestinationsCreated'] is False and obj(stagingcheck)['failureCount']==0)
 cpname=cp.name;queuepath=newq.relative_to(G).as_posix()
 q['id']='REMAINING-WORK-QUEUE-28';q['recordedAtUtc']=now;q['previousQueue']=info(oldq)
 q['limitations']='Applied membership remains525/323/249. Actual GPT accepted Companion10 Exact05 and Illusion14 Exact13 unchanged with holds. Their24 identities are staged, not installed. Control15 full conference is active after recovery of all54 source bindings. Six Control/Ready corrections remain proposed and unapplied. All runtime, balance, cosmology and domain gates remain separate.'
 q['deliveredContextNotYetConferenced']='Full copy release/payload/class packages and Rank8Damage6/Rank7IdentityCasting5 remain delivered for subsequent review. The six scoped Control/Ready corrections are now a real proposed return, independently replay/reverse verified but unapplied. Control15 full review remains active.'
 groups={g['group']:g for g in q['groups']};affected={}
 mapping={'companion-life10-exact-05':'companion-life10','illusion-perception14-exact-13':'illusion-perception14'}
 for cohort in plan['cohorts']:
  name=mapping[cohort['id']];g=groups[name];g['phase']='actual-exact-accepted-integration-staged-not-applied';g['latestObservedStatus']='Actual exact acceptance with unchanged artifacts and retained holds; complete proposed integration staged; live authored index unchanged.';g['actualFinalAssistantTurn']=cohort['actualAssistantMessageId'];g['actualExactAcceptance']=cohort['acceptance'];g['actualExactReturnArchive']=cohort['actualReturnArchive'];g['actualGptThread']='6ad4a867-f330-83e9-829e-bf2bb41a6c09';g['stagedIntegration']=info(planp);g['adopted']=False
  g['actualExactSubmissionUserTurn']='f0f03a31-fb58-4547-823f-21f39b6d0aa4' if name=='illusion-perception14' else 'e7643d79-original-companion-submission-see-native-final'
  if name=='companion-life10':g.pop('actualExactSubmissionUserTurn')
  for ident in cohort['acceptedIds']:affected[ident]=cohort
 control=next(g for g in q['groups'] if g['group']=='control15');control['phase']='actual-full-source-gpt-conference-in-progress';control['latestObservedStatus']='All54 source bindings verified by GPT after19 exact local recoveries; full15-procedure/30-case/13-question review active. No final or cohort acceptance yet.';control['actualUserTurn']='230cc541-987d-460e-b4eb-38f7202e436d';control['actualGptThread']='6ad4a867-f330-83e9-829e-bf2bb41a6c09';control['actualSubmission']=info(A/'CONTROL15_PART5_RECOVERED_SOURCES_01_RECEIPT.json');control['sourceRecoveryProgress']=info(A/'CONTROL15_PART5_RECOVERED_PROGRESS_02_UI.txt');control['proposedCorrectionPreflight']=info(A/'PART5_CORRECTIONS_LOCAL_PREFLIGHT_01.json')
 for row,before in zip(q['rows'],q0['rows']):
  if row['id'] in affected:
   row['currentPhase']='actual-exact-accepted-integration-staged-not-applied';row['semanticAcceptanceClaimed']=True;row['semanticAcceptanceScope']='Exact provisional authored candidate only; all acceptance holds retained; not installed in live index.';row['actualExactAcceptance']=affected[row['id']]['acceptance'];row['integrationStaging']=info(planp);row['nextAction']='Await reserved owner implementation instruction, then revalidate and apply the byte-identical staged files with actual application receipts and preserved holds.'
  elif row['id'] in control['identities']:
   row['currentPhase']=control['phase'];row['nextAction']='Receive the active complete GPT conference and verify its exact return; preserve proposed correction history and content-profile holds.'
  ck('Full source/access/index/history preserved '+row['id'],all(row[k]==before[k] for k in ['currentIndexEntryUnchanged','completeCurrentSourceAndAccess','previousAuthoringMapRowUnchanged']))
 q['pendingDistribution']=dict(Counter(r['currentPhase'] for r in q['rows']));q['exactAcceptedAwaitingApplication']=24;q['sourceCoverageRecoveredForActiveControl15']=54
 q['latestActualReviewEvidence']=[info(A/n) for n in ['GPT_PART5_PERTINENT_RETURNS_01_RECEIPT.json','PART5_CORRECTIONS_LOCAL_PREFLIGHT_01.json','CONTROL15_PART5_RECOVERED_SOURCES_01_RECEIPT.json']]+[info(planp),info(stagingcheck)]
 ck('All323 pending identities and27 groups remain',len(q['rows'])==323 and len(q['groups'])==27 and [r['id'] for r in q['rows']]==[r['id'] for r in q0['rows']])
 ck('Exactly24 accepted remain unapplied',sum(r['currentPhase']=='actual-exact-accepted-integration-staged-not-applied' for r in q['rows'])==24)
 ck('Exactly15 in active recovered-source conference',sum(r['currentPhase']=='actual-full-source-gpt-conference-in-progress' for r in q['rows'])==15)
 start=G/'START_HERE.md';direction=R/'docs/DEVELOPMENT_DIRECTION.md';mapfile=G/'REVIEW_MAP.html';before_nav={p:raw(p) for p in [start,direction,mapfile]};nav={}
 base='docs/audit/2026-10-08/full-game/'
 def notice(prefix):
  return '**Current GPT and integration checkpoint — 18 October 2026:** [Checkpoint35]('+prefix+base+cpname+') and [Queue28]('+prefix+queuepath+') supersede older review-status paragraphs below. Actual GPT accepted **Companion10 Exact05 and Illusion14 Exact13** with all16 artifacts unchanged. The [24-spell integration plan]('+prefix+base+'part5-accepted24-integration-staging-01/INTEGRATION_PLAN.json) stages eight byte-identical files and full membership changes; [831 checks]('+prefix+base+'PART5_ACCEPTED24_INTEGRATION_STAGING_01_CHECK.json) passed. **Nothing is applied:525 reviewed/323 pending/249 standalone remains live;549/299/273 is only projected.** Both exactCR2 Command Undeath case holds retain zero credit; all nine Illusion holds remain. Six Control/Ready corrections are separately preserved and unapplied. The owner reserved implementation for a later instruction. All54 Control15 sources now verify in GPT; the full15-spell/30-case/13-question conference is active. Calibration Review Part5 contains the operative later discussion; Review continuation part5 is standby. Historical source labels, runtime/human/balance/cosmology/75-domain/whole-game/release gates remain separate. These later records are local; GitHubc9c9ffb covers checkpoint32.\n\n'
 for p,prefix in [(start,''),(direction,'../../../')]:
  text=before_nav[p].decode('utf-8-sig');marker='**Current position — 18 October 2026:**';ck('Unique current marker '+p.name,text.count(marker)==1)
  text=text.replace(marker,notice(prefix)+marker,1)
  text=text.replace('[checkpoint34]('+prefix+base+'ACTIVE_AUTHORING_CHECKPOINT_RANK8_MEMORY_CONTROL_34.json)','[checkpoint35]('+prefix+base+cpname+')',1)
  text=text.replace('latest observation was 37% remaining','latest observation was 34% remaining',1)
  nav[p]=text.encode('utf-8')
 html=before_nav[mapfile].decode('utf-8-sig');loc=html.index('</h1>')+len('</h1>');banner='<section class="sequence" aria-label="Current GPT review status"><p><strong>Checkpoint35:24 spells accepted, integration staged.</strong> Applied membership remains525 reviewed/323 pending. Companion10 and Illusion14 exact acceptances retain every hold; eight byte-identical files await the owner’s implementation instruction. All54 Control15 sources are recovered and its full review is active. Older review-status text below is historical. <a href="'+base+cpname+'">Current checkpoint</a> · <a href="'+queuepath+'">Queue28</a> · <a href="'+base+'part5-accepted24-integration-staging-01/README.md">Staged integration</a></p></section>'
 nav[mapfile]=(html[:loc]+banner+html[loc:]).encode('utf-8');ck('Map embedded domain data unchanged',nav[mapfile].decode().replace(banner,'')==html)
 keep.mkdir()
 for p,b in before_nav.items():(keep/p.name).write_bytes(b)
 newq.write_bytes(enc(q))
 for p,b in nav.items():p.write_bytes(b)
 toolsdir=A/'part5-catchup-local-tools-01'
 for name in ['stage_part5_accepted24_01.py','record_part5_acceptance_checkpoint35.py']:
  source=Path(__file__).parent/name;dest=toolsdir/name;ck('New audit tool destination '+name,not dest.exists());dest.write_bytes(raw(source))
 snapshot={'id':'ACTIVE-AUTHORING-PART5-ACCEPTED-STAGING-35','recordedAtUtc':now,'status':'Actual24-spell exact acceptances preserved and integration staged; nothing applied. Full-source Control15 conference active.','developmentDirection':'video-game-only','previousCheckpoint':info(A/'ACTIVE_AUTHORING_CHECKPOINT_RANK8_MEMORY_CONTROL_34.json'),'currentAuthoredIndex':info(idx),'authoredCounts':{'reviewed':525,'pending':323,'standalone':249,'total':848},'currentWorkQueue':info(newq),'currentAcceptedInterfaceRegistry':info(registry),'coverageLedger':info(cov),'accepted24IntegrationPlan':info(planp),'accepted24StagingCheck':info(stagingcheck),'actualReturnsReceipt':info(A/'GPT_PART5_PERTINENT_RETURNS_01_RECEIPT.json'),'proposedSixCorrectionsPreflight':info(A/'PART5_CORRECTIONS_LOCAL_PREFLIGHT_01.json'),'activeGptReview':{'threadId':'6ad4a867-f330-83e9-829e-bf2bb41a6c09','title':'Calibration Review Part 5','userTurn':'230cc541-987d-460e-b4eb-38f7202e436d','scope':'Control15 full source conference:15 procedures,30 cases,13 questions.','sourceBindingsVerifiedByGpt':54,'finalReceived':False,'sourceDelivery':info(A/'CONTROL15_PART5_RECOVERED_SOURCES_01_RECEIPT.json'),'observedProgress':info(A/'CONTROL15_PART5_RECOVERED_PROGRESS_02_UI.txt')},'ownerImplementationReservation':{'actualUserTurn':'ee46d85a-5148-43c3-b3cb-a695ba7e783d','evidence':info(A/'GPT_PART5_CORRECTIONS_AND_BACKLOG_01_NATIVE.json'),'treatment':'Keep exact integration and proposed six corrections reviewable; no rule/index/runtime application before the reserved owner instruction.'},'lastUsageObservation':{'usedPercent':66,'remainingPercent':34,'secondaryUnavailable':True,'stopAtRemainingPercent':20},'latestVerifiedGitHubBackup':{'commit':'c9c9ffb759f3c48ce47a814f03c4e53b2cfeb2a0','throughCheckpoint':32,'receipt':info(G/'docs/audit/2026-10-18/github-snapshot-part5-wards/PUSH_RECEIPT.json')},'laterLocalWork':'Checkpoints33–35, actual accepted returns, six proposed corrections, Control15 source recovery and staged24 integration are local beyond the last push.','preservedNavigation':[info(keep/p.name) for p in before_nav],'navigation':[info(p) for p in nav],'nextAction':'Receive/verify active full Control15 return. Continue independent source/review work and keep GPT informed. Apply accepted24 and six corrections only after the owner’s reserved implementation instruction; revalidate actual live baselines then.','liveIndexModified':False,'canonicalDestinationsCreated':False,'all75DomainGatesUnchanged':True,'runtimeTestsExecuted':0,'wholeGameComplete':False,'sourceInformationDeleted':0}
 cp.write_bytes(enc(snapshot))
 for p,b in unchanged.items():ck('Protected authority unchanged '+p.relative_to(G).as_posix(),raw(p)==b)
 for p in [cp,newq,planp,stagingcheck,A/'part5-accepted24-integration-staging-01/README.md']:ck('New navigation target exists '+p.name,p.exists())
 for p in nav:ck('Written navigation exact '+p.name,raw(p)==nav[p])
 check.write_bytes(enc({'recordedAtUtc':now,'scope':'Review status/queue/navigation reconciliation, no mechanical or applied membership changes.','checkpoint':info(cp),'queue':info(newq),'checks':checks,'checkCount':len(checks),'failureCount':0,'sourceInformationDeleted':0,'runtimeTestsExecuted':0}))
 print(json.dumps({'checkpoint':info(cp),'queue':info(newq),'check':info(check),'checks':len(checks),'appliedMembershipChanged':False}))

if __name__=='__main__':main()
