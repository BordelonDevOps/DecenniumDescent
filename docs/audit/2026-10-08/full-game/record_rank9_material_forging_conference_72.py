"""Record complete source-only preparation while preserving preceding evidence."""
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
 previous=A/'ACTIVE_AUTHORING_CHECKPOINT_RANK8_CORRECTION_SEMANTICS_71.json';out=A/'ACTIVE_AUTHORING_CHECKPOINT_RANK9_MATERIAL_FORGING_72.json'
 oldq=R/'data/director/spell_review/remaining_work_queue_58.json';newq=oldq.with_name('remaining_work_queue_59.json')
 prepfile=A/'RANK9_MATERIAL_FORGING_2_SOURCE_CONFERENCE_01_PREPARATION.json'
 report=A/'ACTIVE_AUTHORING_CHECKPOINT_RANK9_MATERIAL_FORGING_72_CHECK.json';navbackup=A/'navigation-before-rank9-material-forging-72';script=A/Path(__file__).name
 observation=A/'GPT_PART5_RANK7_CORRECTION_STATUS_72.json'
 assert not any(p.exists() for p in [out,newq,report,navbackup,script])
 cp,q0,prep=map(read,[previous,oldq,prepfile]);q=deepcopy(q0);candidate=read(G/prep['candidate']['path']);sc=read(G/prep['check']['path'])
 checks=[]
 def ck(name,ok):checks.append({'check':name,'passed':bool(ok)});assert ok,name
 ck('Exact checkpoint71',info(previous)['sha256']=='be9be2fcb1a6c3cb46cab151cba92f29df06ceb96f133b6fed9513bea42c48e2')
 ck('Exact preceding queue58',info(oldq)==cp['currentWorkQueue'])
 protected=[previous,oldq,R/'data/public/spell_playtests/catalog.json',R/'data/playtest/game_development_coverage.json']
 for key in ['currentAuthoredIndex','currentAcceptedInterfaceRegistry','decisionLedger']:
  b=cp[key];ck('Current authority '+key,info(G/b['path'])==b);protected.append(G/b['path'])
 for b in cp['canonicalHelperBaselinesUnchanged']:
  ck('Canonical helper '+b['path'],info(G/b['path'])==b);protected.append(G/b['path'])
 original={p:p.read_bytes() for p in protected}
 for key in ['candidate','archive','manifest','check','request']:ck('Complete prepared artifact '+key,info(G/prep[key]['path'])==prep[key])
 ck('Complete source-only preparation',prep['status']=='PREPARED_UNSENT' and prep['identityCount']==prep['placementCount']==2 and prep['sourceCount']==166 and prep['questionCount']==24 and prep['riskCounts']=={'C':2} and sc['checkCount']==434 and sc['failures']==0 and not candidate['currentVectors'] and candidate['newRuleAdoptions']==candidate['cosmologyDecisions']==0)
 ck('All24 decisions unselected',len(candidate['questions'])==24 and not any(x['decisionSelected'] for x in candidate['questions']))
 ck('Complete applied/pending/class/item comparisons',len(candidate['completeAppliedCounterparts'])==9 and len(candidate['pendingComparisonsNotAuthority'])==3 and len(candidate['completeClassFeatureComparisons'])==2 and len(candidate['completeReviewedItemComparisons'])==2)
 ck('Current687-recipe review preserved',candidate['craftingReviewStatus']['totals']['reviewed']==687 and candidate['craftingReviewStatus']['totals']['unreviewed']==0)
 ids=[x['spellId'] for x in candidate['records']]
 ck('Exactly Eternal Forge and Matter Conversion',set(ids)=={'eternal-forge','matter-conversion'})
 ck('Both previously ungrouped',all(next(x for x in q['rows'] if x['id']==sid)['currentGroup'] is None for sid in ids))
 group={'group':'rank9-material-forging2','phase':'source-conference-prepared-unsent','identities':ids,'identityCount':2,
  'candidate':prep['candidate'],'preparation':info(prepfile),'archive':prep['archive'],'adopted':False,'sourceCount':166,
  'placementCount':2,'questionCount':24,'riskCounts':{'C':2},'currentCaseCount':0,
  'latestObservedStatus':'Both full sources preserve permanent magical weapon/item creation and useful any-material conversion including stone to mithril.24 questions remain unselected; actual687-recipe status and complete item/body/economy histories are supplied.'}
 q['groups'].append(group)
 for old,row in zip(q0['rows'],q['rows']):
  if row['id'] in ids:
   row.update(currentGroup=group['group'],currentPhase=group['phase'],semanticAcceptanceClaimed=False,
    sourceConferencePreparation=info(prepfile),nextAction='Confer on24 exact source questions for permanent magical item creation and material conversion with complete recipe/item/material sources,Director authorization,physical state,finite entitlements,ownership,economy,dispelling and history. No selection or application yet.')
  else:ck('Unaffected complete row '+row['id'],row==old)
  ck('Complete native source/index/history '+row['id'],all(row[k]==old[k] for k in ['completeCurrentSourceAndAccess','currentIndexEntryUnchanged','previousAuthoringMapRowUnchanged']))
 q['previousSummaryBefore72']={k:deepcopy(q0[k]) for k in ['limitations','pendingDistribution','preparedOrActualReviewIdentityCount','originalSourceOrReceiptWorkCount']}
 q.update(id='REMAINING-WORK-QUEUE-59',recordedAtUtc=datetime.now(timezone.utc).isoformat(),previousQueue=info(oldq),
  preparedOrActualReviewIdentityCount=309,originalSourceOrReceiptWorkCount=14,
  pendingDistribution=dict(Counter(x['currentPhase'] for x in q['rows'])),latestSourceConference=info(prepfile))
 q['sourceBindings'].extend([info(prepfile),prep['candidate'],prep['archive'],prep['check']]);q['latestActualReviewEvidence'].append(info(observation))
 q['limitations']='Current through checkpoint72: applied525 reviewed/323 pending/249 standalone/173 interfaces;39 accepted-but-unapplied. Rank7 correction12 actually sent and visibly generating full replacements with Stop; no assistant final received. All8 original Rank8 findings independently reconciled; one additional Anchor history question prepared13 UNSENT.51 groups cover309 pending identities;14 rank9 identities remain ungrouped. Material-forging2 has166 full sources,2 original placements,24 unselected questions,9 applied spells,3 pending conference archives,2 complete reviewed item comparisons and434 preservation checks. All687 current recipes are reviewed; stale early status is historical. No semantic acceptance,runtime or cosmology adoption. GitHub backup verified through65; owner implementation reservation retained.'
 ck('All323 pending covered',len(q['rows'])==323 and len(q['groups'])==51 and sum(x['currentGroup'] is not None for x in q['rows'])==309 and sum(x['currentGroup'] is None for x in q['rows'])==14)
 ck('Exactly39 accepted unapplied',sum(x['currentPhase'] in ['actual-exact-accepted-integration-staged-not-applied','actual-full-conference-accepted-successor-not-applied'] for x in q['rows'])==39)
 ck('Earlier full groups unchanged',q['groups'][:-1]==q0['groups'])
 ck('Remaining ungrouped rank9',all(min(a['rank'] for a in x['completeCurrentSourceAndAccess']['classAccess'].values())==9 for x in q['rows'] if x['currentGroup'] is None))
 ck('Distribution exact',sum(q['pendingDistribution'].values())==323)
 for b in cp['navigation']:ck('Preceding navigation '+b['path'],info(G/b['path'])==b)
 navpaths=[G/'START_HERE.md',R/'docs/DEVELOPMENT_DIRECTION.md',G/'REVIEW_MAP.html'];nav={p:p.read_bytes() for p in navpaths};navbackup.mkdir()
 for p,b in nav.items():(navbackup/p.name).write_bytes(b)
 newq.write_bytes(enc(q));base='docs/audit/2026-10-08/full-game/'
 for p,prefix in [(navpaths[0],''),(navpaths[1],'../../../')]:
  raw=nav[p];pos=raw.index(b'\n')+1
  notice=('\n**Latest source preparation — 20 October 2026:** [Checkpoint72]('+prefix+base+out.name+') and [Queue59]('+prefix+newq.relative_to(G).as_posix()+') add Eternal Forge and Matter Conversion:166 complete sources,24 unselected questions and434 preservation checks.51 groups cover309 pending identities;14 remain ungrouped. GPT is generating Rank7 corrections. Rank8 has one additional Anchor history qualification prepared after all8 original findings were reconciled. Applied525/323/249,173 interfaces and39 accepted-but-unapplied remain unchanged. Current687-recipe reviewed status is preserved. Owner implementation remains reserved; GitHub backup verified through65.\n').encode('utf-8')
  p.write_bytes(raw[:pos]+notice+raw[pos:]);ck('Previous navigation retained '+p.name,p.read_bytes().replace(notice,b'',1)==raw)
 p=navpaths[2];raw=nav[p];pos=raw.index(b'</h1>')+len(b'</h1>')
 notice=('<section class="sequence" aria-label="Current material and forging source preparation"><p><strong>Checkpoint72: Eternal Forge and Matter Conversion prepared.</strong>166 full sources,24 unselected questions,434 preservation checks. Queue59:309 grouped pending identities,14 ungrouped. Rank7 corrections still generating; Rank8 Anchor history follow-up prepared. No new rules applied. <a href="'+base+out.name+'">Current checkpoint</a></p></section>').encode('utf-8')
 p.write_bytes(raw[:pos]+notice+raw[pos:]);ck('Previous map retained',p.read_bytes().replace(notice,b'',1)==raw)
 cp['previousGptObservationBefore72']=deepcopy(cp['activeGptReviewAtLastVerifiedObservation'])
 cp['activeGptReviewAtLastVerifiedObservation']['latestRecheck']=info(observation)
 cp['activeGptReviewAtLastVerifiedObservation']['latestObservedStatus']='Actual Rank7 correction12 remains latest user; native no assistant final; fresh browser shows full artifact replacement generation and Stop. No interruption or duplicate request. Visible activity is not completion.'
 cp.update(id='ACTIVE-AUTHORING-RANK9-MATERIAL-FORGING-72',recordedAtUtc=datetime.now(timezone.utc).isoformat(),previousCheckpoint=info(previous),
  currentWorkQueue=info(newq),preparedGroupCount=51,groupedPendingIdentities=309,ungroupedPendingIdentities=14,rank9MaterialForging2SourceConference=info(prepfile),
  status='Two complete material/forging sources prepared with24 unselected decisions and current crafting status. GPT still completing Rank7 correction12.',
  navigation=[info(p) for p in navpaths],preservedNavigation=[info(navbackup/p.name) for p in navpaths],
  lastUsageObservation={'usedPercent':27,'remainingPercent':73,'stopAtRemainingPercent':20},
  previousGoalTurnClassification='Progress: checkpoint71 reconciled eight Rank8 findings and preserved one additional Anchor history qualification. Current72 completed source preparation for two remaining identities.',
  laterLocalWork='Checkpoints66–72,Rank7 correction dispatch,Rank8 correction review/additional question,elemental-pets2,material-forging2,Queue59 and current observations remain local after verified GitHub backup through65.',
  nextAction='Receive full completed Rank7 correction return when available, preserve and independently validate; then send prepared Rank8 Anchor history13 without interrupting. Continue remaining14 ungrouped rank9 identities and pending conferences. Owner implementation reservation and20percent remaining boundary retained.',
  queueObservationSupersession='Queue59 preserves every previous full group and original row source,groups two previously ungrouped identities and computes current distribution. Older summaries retained.')
 ck('No new application or acceptance',cp['authoredCounts']=={'reviewed':525,'pending':323,'standalone':249,'total':848} and cp['acceptedButUnapplied']==39 and cp['implementationApplied'] is False)
 out.write_bytes(enc(cp));script.write_bytes(Path(__file__).read_bytes())
 for p,b in original.items():ck('Protected authority unchanged '+p.relative_to(G).as_posix(),p.read_bytes()==b)
 report.write_bytes(enc({'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'checkpoint':info(out),'queue':info(newq),
  'checks':checks,'checkCount':len(checks),'failures':0,'newRuleAdoptions':0,'runtimeTestsExecuted':0,'sourceInformationDeleted':0,
  'scope':'Complete source/history/queue/navigation preservation; no gameplay semantic acceptance,runtime or cosmology implementation.'}))
 print(json.dumps({'checkpoint':info(out),'queue':info(newq),'report':info(report),'checks':len(checks),'failures':0}))
if __name__=='__main__':main()
