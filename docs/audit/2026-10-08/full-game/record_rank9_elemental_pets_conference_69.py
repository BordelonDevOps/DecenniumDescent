"""Record two source preparations; retain full preceding records and canonical rules."""
from pathlib import Path
from datetime import datetime,timezone
from collections import Counter
from copy import deepcopy
import hashlib,json
G=Path(r'C:\Github\DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game'
def read(p):return json.loads(p.read_bytes())
def enc(x):return (json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
def info(p):
 b=p.read_bytes();return {'path':p.relative_to(G).as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def main():
 previous=A/'ACTIVE_AUTHORING_CHECKPOINT_RANK7_SEMANTIC_REVIEW_68.json';out=A/'ACTIVE_AUTHORING_CHECKPOINT_RANK9_ELEMENTAL_PETS_69.json'
 oldq=R/'data/director/spell_review/remaining_work_queue_55.json';newq=oldq.with_name('remaining_work_queue_56.json')
 prepfile=A/'RANK9_ELEMENTAL_PETS_2_SOURCE_CONFERENCE_01_PREPARATION.json'
 report=A/'ACTIVE_AUTHORING_CHECKPOINT_RANK9_ELEMENTAL_PETS_69_CHECK.json';navbackup=A/'navigation-before-rank9-elemental-pets-69';script=A/Path(__file__).name
 assert not any(p.exists() for p in [out,newq,report,navbackup,script])
 cp,q0,prep=map(read,[previous,oldq,prepfile]);q=deepcopy(q0);candidate=read(G/prep['candidate']['path']);sc=read(G/prep['check']['path'])
 checks=[]
 def ck(name,ok):checks.append({'check':name,'passed':bool(ok)});assert ok,name
 ck('Exact checkpoint68',info(previous)['sha256']=='2c2ebe319a7aaa634bcc21460716fce0115c013a6ceb9407f0b35792e9c37a52')
 ck('Exact preceding queue55',info(oldq)==cp['currentWorkQueue'])
 protected=[previous,oldq,R/'data/public/spell_playtests/catalog.json',R/'data/playtest/game_development_coverage.json']
 for key in ['currentAuthoredIndex','currentAcceptedInterfaceRegistry','decisionLedger']:
  b=cp[key];ck('Current authority '+key,info(G/b['path'])==b);protected.append(G/b['path'])
 for b in cp['canonicalHelperBaselinesUnchanged']:
  ck('Canonical helper '+b['path'],info(G/b['path'])==b);protected.append(G/b['path'])
 original={p:p.read_bytes() for p in protected}
 for k in ['candidate','archive','manifest','check','request']:ck('Complete prepared artifact '+k,info(G/prep[k]['path'])==prep[k])
 ck('Full two-identity packet remains source-only',prep['status']=='PREPARED_UNSENT' and prep['identityCount']==2 and prep['placementCount']==2 and prep['sourceCount']==107 and prep['questionCount']==24 and prep['riskCounts']=={'C':2} and sc['checkCount']==337 and sc['failures']==0 and not candidate['currentVectors'] and candidate['newRuleAdoptions']==candidate['cosmologyDecisions']==0)
 ck('All24 questions remain unselected',len(candidate['questions'])==24 and not any(x['decisionSelected'] for x in candidate['questions']))
 ck('Complete applied/pending/class comparisons',len(candidate['completeAppliedCounterparts'])==11 and len(candidate['pendingComparisonsNotAuthority'])==2 and len(candidate['completeClassFeatureComparisons'])==7)
 ids=[x['spellId'] for x in candidate['records']]
 ck('Exactly Convergence and Fusion',set(ids)=={'elemental-convergence','elemental-fusion'})
 ck('Both previously ungrouped',all(next(x for x in q['rows'] if x['id']==sid)['currentGroup'] is None for sid in ids))
 group={'group':'rank9-elemental-pets2','phase':'source-conference-prepared-unsent','identities':ids,'identityCount':2,
  'candidate':prep['candidate'],'preparation':info(prepfile),'archive':prep['archive'],'adopted':False,'sourceCount':107,
  'placementCount':2,'questionCount':24,'riskCounts':{'C':2},'currentCaseCount':0,
  'latestObservedStatus':'Both complete sources preserve four simultaneous base pets and real pet fusion with shared stats/two-spell benefit.24 choices remain unselected,including concentration bridge,actual second casting opportunity and conserved body/resource histories.'}
 q['groups'].append(group)
 for old,row in zip(q0['rows'],q['rows']):
  if row['id'] in ids:
   row.update(currentGroup=group['group'],currentPhase=group['phase'],semanticAcceptanceClaimed=False,
    sourceConferencePreparation=info(prepfile),nextAction='Confer on24 source-bound elemental-pet questions using all four actual base profiles,complete greater-pet comparisons,class gates,concentration,body/custody/action and Null interfaces. Return complete useful positive procedures/cases; no selection or implementation yet.')
  else:ck('Unaffected complete row '+row['id'],row==old)
  ck('Complete source/index/history retained '+row['id'],all(row[k]==old[k] for k in ['completeCurrentSourceAndAccess','currentIndexEntryUnchanged','previousAuthoringMapRowUnchanged']))
 q['previousSummaryBefore69']={k:deepcopy(q0[k]) for k in ['limitations','pendingDistribution','preparedOrActualReviewIdentityCount','originalSourceOrReceiptWorkCount']}
 q.update(id='REMAINING-WORK-QUEUE-56',recordedAtUtc=datetime.now(timezone.utc).isoformat(),previousQueue=info(oldq),
  preparedOrActualReviewIdentityCount=307,originalSourceOrReceiptWorkCount=16,
  pendingDistribution=dict(Counter(x['currentPhase'] for x in q['rows'])),latestSourceConference=info(prepfile))
 q['sourceBindings'].extend([info(prepfile),prep['candidate'],prep['archive'],prep['check']])
 q['latestActualReviewEvidence'].append(info(A/'GPT_PART5_RANK8_STATUS_69.json'))
 q['limitations']='Current through checkpoint69: applied525 reviewed/323 pending/249 standalone and173 interfaces;39 accepted-but-unapplied. Rank7 complete return has three local semantic findings and a full prepared UNSENT correction packet. Rank8 correction11 actually submitted; fresh native observation has no assistant final and browser still displays Analyzing/Stop. No interruption or duplicate request.50 groups cover307 pending identities;16 rank9 identities remain ungrouped. Elemental-pets2 preserves107 full source artifacts,2 placements,24 unselected questions,11 applied counterparts,2 full pending conferences and337 source-preservation checks. No semantic acceptance,runtime or cosmology adoption. Verified GitHub backup remains through65. Owner implementation reservation and separate completion gates remain.'
 ck('Complete323 pending coverage',len(q['rows'])==323 and len(q['groups'])==50 and sum(x['currentGroup'] is not None for x in q['rows'])==307 and sum(x['currentGroup'] is None for x in q['rows'])==16)
 ck('Exactly39 accepted but unapplied',sum(x['currentPhase'] in ['actual-exact-accepted-integration-staged-not-applied','actual-full-conference-accepted-successor-not-applied'] for x in q['rows'])==39)
 ck('Every earlier full group unchanged',q['groups'][:-1]==q0['groups'])
 ck('All remaining ungrouped rank9',all(min(a['rank'] for a in x['completeCurrentSourceAndAccess']['classAccess'].values())==9 for x in q['rows'] if x['currentGroup'] is None))
 ck('Current pending distribution reconciles actual rows',sum(q['pendingDistribution'].values())==323 and q['pendingDistribution']==dict(Counter(x['currentPhase'] for x in q['rows'])))
 for b in cp['navigation']:ck('Exact preceding navigation '+b['path'],info(G/b['path'])==b)
 navpaths=[G/'START_HERE.md',R/'docs/DEVELOPMENT_DIRECTION.md',G/'REVIEW_MAP.html'];nav={p:p.read_bytes() for p in navpaths}
 navbackup.mkdir()
 for p,b in nav.items():(navbackup/p.name).write_bytes(b)
 newq.write_bytes(enc(q));base='docs/audit/2026-10-08/full-game/'
 for p,prefix in [(navpaths[0],''),(navpaths[1],'../../../')]:
  raw=nav[p];pos=raw.index(b'\n')+1
  notice=('\n**Latest source preparation — 20 October 2026:** [Checkpoint69]('+prefix+base+out.name+') and [Queue56]('+prefix+newq.relative_to(G).as_posix()+') add Elemental Convergence and Elemental Fusion:107 complete sources,24 unselected questions and337 preservation checks.50 groups cover307 pending identities;16 remain ungrouped. Rank7 needs three bounded corrections (packet prepared,unsent); GPT still displays Rank8 processing. Applied525/323/249,173 interfaces and39 accepted-but-unapplied remain unchanged. Owner implementation reservation retained; verified GitHub backup through65.\n').encode('utf-8')
  p.write_bytes(raw[:pos]+notice+raw[pos:]);ck('Original navigation retained '+p.name,p.read_bytes().replace(notice,b'',1)==raw)
 p=navpaths[2];raw=nav[p];pos=raw.index(b'</h1>')+len(b'</h1>')
 notice=('<section class="sequence" aria-label="Current elemental pet source preparation"><p><strong>Checkpoint69: Elemental Convergence and Fusion prepared.</strong>107 full sources,24 unselected questions,337 preservation checks. Queue56:307 grouped pending identities,16 ungrouped. Rank7 corrections prepared; Rank8 still processing. No rules applied. <a href="'+base+out.name+'">Current checkpoint</a></p></section>').encode('utf-8')
 p.write_bytes(raw[:pos]+notice+raw[pos:]);ck('Original map retained',p.read_bytes().replace(notice,b'',1)==raw)
 cp['previousGptObservationBefore69']=deepcopy(cp['activeGptReviewAtLastVerifiedObservation'])
 cp['activeGptReviewAtLastVerifiedObservation']['latestRecheck']=info(A/'GPT_PART5_RANK8_STATUS_69.json')
 cp['activeGptReviewAtLastVerifiedObservation']['latestObservedStatus']='Native idle with no assistant final; fresh browser still shows Analyzing and Stop on correction11. No successor received,no interruption. Visible activity is not a backend progress guarantee.'
 cp.update(id='ACTIVE-AUTHORING-RANK9-ELEMENTAL-PETS-69',recordedAtUtc=datetime.now(timezone.utc).isoformat(),previousCheckpoint=info(previous),
  currentWorkQueue=info(newq),preparedGroupCount=50,groupedPendingIdentities=307,ungroupedPendingIdentities=16,
  rank9ElementalPets2SourceConference=info(prepfile),
  status='Two complete elemental-pet source conferences prepared together without selecting rules. Rank7 correction package remains unsent while Rank8 correction response is unfinished.',
  navigation=[info(p) for p in navpaths],preservedNavigation=[info(navbackup/p.name) for p in navpaths],
  lastUsageObservation={'usedPercent':24,'remainingPercent':76,'stopAtRemainingPercent':20},
  previousGoalTurnClassification='Progress: checkpoint68 saved independent Rank7 semantic diagnostics and three-finding full correction package. Current69 prepares two remaining source identities and reconciles queue/navigation.',
  laterLocalWork='Checkpoints66–69,Rank7 semantic review/correction preparation,elemental-pets2,Queue56 and current observations remain local after verified backup through65.',
  nextAction='Receive completed Rank8 correction artifacts when available; then send prepared Rank7 correction12 without interrupting. Continue remaining16 ungrouped rank9 sources and all pending full conferences. Preserve owner implementation reservation and stop at20 percent remaining.',
  queueObservationSupersession='Queue56 preserves every previous full group and row source,groups two previously ungrouped identities,and recalculates stale pendingDistribution/limitations from actual current rows. Older summaries remain preserved.')
 ck('No new applied or accepted rules',cp['authoredCounts']=={'reviewed':525,'pending':323,'standalone':249,'total':848} and cp['acceptedButUnapplied']==39 and cp['implementationApplied'] is False)
 out.write_bytes(enc(cp));script.write_bytes(Path(__file__).read_bytes())
 for p,b in original.items():ck('Protected authority unchanged '+p.relative_to(G).as_posix(),p.read_bytes()==b)
 report.write_bytes(enc({'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'checkpoint':info(out),'queue':info(newq),
  'checks':checks,'checkCount':len(checks),'failures':0,'newRuleAdoptions':0,'runtimeTestsExecuted':0,'sourceInformationDeleted':0,
  'scope':'Complete source/history/queue/navigation preservation; no gameplay semantic acceptance or runtime/cosmology implementation.'}))
 print(json.dumps({'checkpoint':info(out),'queue':info(newq),'report':info(report),'checks':len(checks),'failures':0}))
if __name__=='__main__':main()
