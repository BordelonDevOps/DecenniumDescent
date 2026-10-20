"""Advance review observations while preserving every canonical rule and source."""
from pathlib import Path
from datetime import datetime,timezone
import copy,hashlib,json
G=Path(r'C:\Github\DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game'
def read(p):return json.loads(p.read_bytes())
def enc(x):return (json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
def info(p):
 b=p.read_bytes();return {'path':p.relative_to(G).as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def main():
 old=A/'ACTIVE_AUTHORING_CHECKPOINT_RANK7_RETURN_RANK8_DISPATCH_67.json'
 out=A/'ACTIVE_AUTHORING_CHECKPOINT_RANK7_SEMANTIC_REVIEW_68.json'
 checkpath=A/'ACTIVE_AUTHORING_CHECKPOINT_RANK7_SEMANTIC_REVIEW_68_CHECK.json'
 queueout=R/'data/director/spell_review/remaining_work_queue_55.json'
 navbackup=A/'navigation-before-rank7-semantic-review-68';script=A/Path(__file__).name
 assert not any(p.exists() for p in [out,checkpath,queueout,navbackup,script])
 checks=[]
 def ck(label,ok):
  checks.append({'check':label,'passed':bool(ok)});assert ok,label
 cp=read(old);ck('Exact checkpoint67',info(old)['sha256']=='4c1d39e7db7695fe1684ad2d972a57b15bb1241bad6008c4ca09bb15d85b18fc')
 protected=[old,R/'data/public/spell_playtests/catalog.json',R/'data/playtest/game_development_coverage.json']
 for key in ['currentWorkQueue','currentAuthoredIndex','currentAcceptedInterfaceRegistry','decisionLedger']:
  b=cp[key];ck('Current authoritative binding '+key,info(G/b['path'])==b);protected.append(G/b['path'])
 for b in cp['canonicalHelperBaselinesUnchanged']:
  ck('Unchanged canonical helper '+b['path'],info(G/b['path'])==b);protected.append(G/b['path'])
 originalbytes={p:p.read_bytes() for p in protected}
 reviewpath=A/'RANK7_IDENTITY_CASTING5_PART5_RETURN_01_SEMANTIC_REVIEW_68.json';review=read(reviewpath)
 preppath=A/'RANK7_IDENTITY_CASTING5_LOCAL_CORRECTIONS_01_PREPARATION.json';prep=read(preppath)
 nativepath=A/'GPT_PERTINENT_RECHECK_68.json';native=read(nativepath)
 ck('Complete semantic inventory',review['reviewCoverage']['mainCasesRead']==10 and review['reviewCoverage']['independentBranchesRead']==39 and review['reviewCoverage']['conditionalBranchesRetained']==11)
 ck('Independent diagnostics remain honestly unresolved',review['diagnosticCheckCount']==314 and review['diagnosticFailures']==11 and review['findingsCount']==3 and review['newAcceptedIdentities']==0)
 ck('Packet remains unsent',prep['sent'] is False and prep['status']=='PREPARED_NOT_SENT')
 for k in ['archive','request','semanticReview','originalReturn','manifest']:
  ck('Prepared artifact binding '+k,info(G/prep[k]['path'])==prep[k])
 ck('Native newest actual request is Rank8 correction11',native['part5']['turns'][0]['id']=='939b0d09-faf6-4c89-baa6-759aa484eb2e')
 ck('No completed Rank8 assistant return yet',not any(i['type']=='agentMessage' for t in native['part5']['turns'] for i in t['items']))
 ck('User Unity direction already recorded',native['observations']['unityLatestOwnerTurnAlreadyRecorded']=='7c6cc02d-a5b6-4d38-822e-6565dfd8f1be' and native['observations']['newOwnerDecisionsSinceLedger02']==0)
 correction={'status':'PREPARED_NOT_SENT','preparation':info(preppath),'archive':prep['archive'],'request':prep['request'],
   'sent':False,'findings':3,'submitAfter':'Actual completed Rank8 correction response; do not interrupt current processing.'}
 semantic={'status':'REQUIRES_BOUNDED_CORRECTIONS_NOT_ACCEPTED','report':info(reviewpath),'diagnosticChecks':314,
   'passed':303,'failedDiagnostics':11,'findings':3,'newAcceptedIdentities':0,'preparedCorrectionConference':correction,
   'runtimeTestsExecuted':0,'implementationApplied':False}
 qpath=G/cp['currentWorkQueue']['path'];previous=read(qpath);q=copy.deepcopy(previous)
 ck('Current queue coverage',len(q['groups'])==49 and q['preparedOrActualReviewIdentityCount']==305 and q['originalSourceOrReceiptWorkCount']==18)
 affected={'rank7-identity-casting5','rank8-damage6'}
 for group in q['groups']:
  if group['group'] not in affected:continue
  group['priorObservationBefore68']={k:copy.deepcopy(group[k]) for k in ['phase','latestObservedStatus']}
  if group['group']=='rank7-identity-casting5':
   group.update(phase='returned-conference-requires-local-semantic-corrections',latestObservedStatus='Full local review documents three corrections;314 diagnostics with303 passes and11 failures. Complete correction package prepared but not sent. No acceptance.',localSemanticReview=semantic,newAcceptedIdentities=0)
  else:
   group['latestObservedStatus']='Actual correction11 remains submitted. Native reports idle without an assistant final, but browser displays Analyzing and Stop. No completed corrected artifact received; no restart or interruption.'
 for row in q['rows']:
  if row.get('currentGroup') not in affected:continue
  row['previousObservationBefore68']={k:copy.deepcopy(row[k]) for k in ['currentPhase','nextAction']}
  if row['currentGroup']=='rank7-identity-casting5':
   row.update(currentPhase='returned-conference-requires-local-semantic-corrections',nextAction='After GPT completes Rank8, submit the complete three-finding Rank7 correction packet and independently reconcile every changed full artifact before acceptance.')
  else:row['nextAction']='Receive actual completed Rank8 corrections and full artifacts; latest browser still displays active processing despite native idle status. Do not interrupt or duplicate the request.'
  ck('No acceptance claimed '+row['id'],not row['semanticAcceptanceClaimed'])
 q.update(id='REMAINING-WORK-QUEUE-55',recordedAtUtc=datetime.now(timezone.utc).isoformat(),previousQueue=info(qpath),currentRank7LocalSemanticReview=semantic)
 q['latestActualReviewEvidence'] += [info(reviewpath),info(preppath),info(nativepath)]
 ck('All complete row source identities retained',[r['id'] for r in q['rows']]==[r['id'] for r in previous['rows']] and all(r['completeCurrentSourceAndAccess']==p['completeCurrentSourceAndAccess'] and r['currentIndexEntryUnchanged']==p['currentIndexEntryUnchanged'] for r,p in zip(q['rows'],previous['rows'])))
 ck('Group identity/candidate and unrelated groups unchanged',all(g==p if g['group'] not in affected else g['identities']==p['identities'] and g['candidate']==p['candidate'] for g,p in zip(q['groups'],previous['groups'])))
 ck('Counts and source bindings unchanged',q['ordinarySpellCounts']==previous['ordinarySpellCounts'] and q['sourceBindings']==previous['sourceBindings'])
 queueout.write_bytes(enc(q))
 navpaths=[G/'START_HERE.md',R/'docs/DEVELOPMENT_DIRECTION.md',G/'REVIEW_MAP.html']
 for b in cp['navigation']:ck('Exact previous navigation '+b['path'],info(G/b['path'])==b)
 nav={p:p.read_bytes() for p in navpaths};navbackup.mkdir()
 for p,raw in nav.items():(navbackup/p.name).write_bytes(raw)
 base='docs/audit/2026-10-08/full-game/'
 for p,prefix in [(navpaths[0],''),(navpaths[1],'../../../')]:
  raw=nav[p];pos=raw.index(b'\n')+1
  notice=('\n**Current review — 20 October 2026:** [Checkpoint68]('+prefix+base+out.name+') records the independent Rank7 identity/casting review:314 diagnostics,303 passes,11 failures across three findings (feat acquisition, remaining Action debits, and Erase casting history). Its complete correction packet is prepared and unsent while GPT continues Rank8 corrections. Queue55 preserves49 groups,305 grouped and18 ungrouped pending identities. Applied525/323/249,173 interfaces and39 accepted-but-unapplied remain unchanged; owner implementation reservation retained. Verified GitHub backup still extends through checkpoint65.\n').encode('utf-8')
  p.write_bytes(raw[:pos]+notice+raw[pos:]);ck('Original navigation preserved '+p.name,p.read_bytes().replace(notice,b'',1)==raw)
 p=navpaths[2];raw=nav[p];pos=raw.index(b'</h1>')+len(b'</h1>')
 notice=('<section class="sequence" aria-label="Current Rank7 semantic review"><p><strong>Checkpoint68: Rank7 needs three bounded corrections.</strong> Independent diagnostics:303 pass,11 fail. Full packet prepared, unsent; GPT still processing Rank8. No new accepted or applied rules. <a href="'+base+out.name+'">Current checkpoint</a></p></section>').encode('utf-8')
 p.write_bytes(raw[:pos]+notice+raw[pos:]);ck('Original map preserved',p.read_bytes().replace(notice,b'',1)==raw)
 cp['previousGptObservationBefore68']=copy.deepcopy(cp['activeGptReviewAtLastVerifiedObservation'])
 cp['activeGptReviewAtLastVerifiedObservation']['latestObservedStatus']='Correction11 remains submitted; native idle has no completed assistant response, while actual browser displays Analyzing and Stop. No successor retrieved. Do not interrupt.'
 cp['activeGptReviewAtLastVerifiedObservation']['latestRecheck']=info(nativepath)
 cp['completedRank7IdentityCasting5Return']['status']='FULL_RETURN_PRESERVED_LOCAL_SEMANTIC_REVIEW_REQUIRES_THREE_CORRECTIONS'
 cp['completedRank7IdentityCasting5Return']['localSemanticReview']=semantic
 cp.update(id='ACTIVE-AUTHORING-RANK7-SEMANTIC-REVIEW-68',recordedAtUtc=datetime.now(timezone.utc).isoformat(),previousCheckpoint=info(old),
   status='Rank7 independent semantic review complete for this return: three findings, bounded correction packet prepared but unsent. GPT still processing Rank8 corrections; no acceptance or implementation.',
   currentWorkQueue=info(queueout),currentRank7LocalSemanticReview=semantic,pertinentRecheck=info(nativepath),
   navigation=[info(p) for p in navpaths],preservedNavigation=[info(navbackup/p.name) for p in navpaths],
   queueObservationSupersession='Queue55 updates only existing Rank7/Rank8 review observations. All49 groups,305 grouped and18 ungrouped identities remain.',
   nextAction='Receive completed Rank8 correction artifacts when available; submit full Rank7 correction12 only after that response ends. Continue remaining18 ungrouped rank9 source preparation, including Elemental Convergence/Fusion. No canonical implementation without owner release of reservation.',
   previousGoalTurnClassification='progress: Rank7 preservation and Rank8 actual dispatch at67. Current68 completes independent Rank7 authored semantic review and prepares the full three-finding correction packet.',
   laterLocalWork='Checkpoints66–68, Rank7 semantic review and correction preparation,Queue55 and latest GPT observation remain local work after the verified backup through65.',
   lastUsageObservation={'usedPercent':23,'remainingPercent':77,'stopAtRemainingPercent':20})
 ck('Applied counts and implementation unchanged',cp['authoredCounts']=={'reviewed':525,'pending':323,'standalone':249,'total':848} and cp['acceptedButUnapplied']==39 and not cp['implementationApplied'])
 out.write_bytes(enc(cp));script.write_bytes(Path(__file__).read_bytes())
 for p,b in originalbytes.items():ck('Protected authority retained '+p.relative_to(G).as_posix(),p.read_bytes()==b)
 checkpath.write_bytes(enc({'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'checkpoint':info(out),'queue':info(queueout),
   'checks':checks,'checkCount':len(checks),'failures':0,'scope':'Review/packet/queue/navigation preservation only. The separate semantic diagnostic report intentionally contains11 unresolved failures. No runtime or gameplay acceptance.',
   'sourceInformationDeleted':0,'implementationApplied':False}))
 print(json.dumps({'checkpoint':info(out),'queue':info(queueout),'report':info(checkpath),'checks':len(checks),'failures':0}))
if __name__=='__main__':main()
