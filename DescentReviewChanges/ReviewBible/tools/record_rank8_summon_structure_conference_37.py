"""Add prepared source coverage without changing spell membership or domain gates."""
from copy import deepcopy
from collections import Counter
from datetime import datetime, timezone
import json
from apply_di7_ap_as_01 import G,R,A,info,encoded

def read(p):return json.loads(p.read_bytes())
def main():
 now=datetime.now(timezone.utc).isoformat();qp=R/'data/director/spell_review/remaining_work_queue_29.json';outq=qp.with_name('remaining_work_queue_30.json');cpp=A/'ACTIVE_AUTHORING_CHECKPOINT_RANK8_LIFE_FORM_36.json';outcp=A/'ACTIVE_AUTHORING_CHECKPOINT_RANK8_SUMMON_STRUCTURE_37.json';check=A/'ACTIVE_AUTHORING_CHECKPOINT_RANK8_SUMMON_STRUCTURE_37_CHECK.json';keep=A/'navigation-before-rank8-summon-structure-37'
 assert not any(p.exists() for p in [outq,outcp,check,keep])
 pp=A/'RANK8_SUMMON_STRUCTURE_5_SOURCE_CONFERENCE_01_PREPARATION.json';prep=read(pp);candidate=read(G/prep['candidate']['path']);q0=read(qp);q=deepcopy(q0);cp0=read(cpp);checks=[]
 def ck(n,v):checks.append({'check':n,'passed':bool(v)});assert v,n
 idx=R/'data/public/spell_playtests/authored_review_index.json';cov=R/'data/playtest/game_development_coverage.json';cat=idx.with_name('catalog.json');reg=R/'data/director/spell_review/accepted_interface_registry_06.json'
 protected={p:p.read_bytes() for p in [idx,cov,cat,reg,qp,cpp]}
 ck('Prepared source conference is unsent with zero adoption',prep['status']=='PREPARED_UNSENT' and candidate['newRuleAdoptions']==0 and not candidate['currentVectors'])
 ck('Actual packet binding intact',info(G/prep['candidate']['path'])==prep['candidate'] and info(G/prep['archive']['path'])==prep['archive'])
 ids=[r['spellId'] for r in candidate['records']];group={'group':'rank8-summon-structure5','phase':'source-conference-prepared-unsent','identities':ids,'identityCount':5,'candidate':prep['candidate'],'preparation':info(pp),'archive':prep['archive'],'adopted':False,'sourceCount':68,'placementCount':5,'questionCount':20,'riskCounts':{'B':1,'C':4},'currentCaseCount':0,'latestObservedStatus':'Full source packet prepared and not yet sent. All recommendations unselected; no procedure/case adoption.'}
 ck('Five new ungrouped identities',len(set(ids))==5 and all(next(r for r in q['rows'] if r['id']==ident)['currentGroup'] is None for ident in ids))
 q['groups'].append(group)
 for before,row in zip(q0['rows'],q['rows']):
  if row['id'] in ids:
   row['currentGroup']=group['group'];row['currentPhase']=group['phase'];row['semanticAcceptanceClaimed']=False;row['nextAction']='Deliver full rank8 summon/structure5 packet after the current GPT review; resolve20 actual questions before authoring complete procedures/cases.';row['sourceConferencePreparation']=info(pp)
  ck('Complete source/index/history preserved '+row['id'],all(before[k]==row[k] for k in ['completeCurrentSourceAndAccess','currentIndexEntryUnchanged','previousAuthoringMapRowUnchanged']))
 q['id']='REMAINING-WORK-QUEUE-30';q['recordedAtUtc']=now;q['previousQueue']=info(qp);q['preparedOrActualReviewIdentityCount']=190;q['originalSourceOrReceiptWorkCount']=133;q['pendingDistribution']=dict(Counter(r['currentPhase'] for r in q['rows']));q['latestSourceConference']=info(pp)
 q['sourceBindings'].extend([info(pp),prep['candidate'],prep['archive'],prep['check']]);q['limitations']+=' New summon/structure5 supplies68 full sources and20 unselected questions;256 checks verify preservation, not semantic acceptance.'
 ck('323 pending preserved with190 grouped133 other',len(q['rows'])==323 and len(q['groups'])==29 and sum(r['currentGroup'] is not None for r in q['rows'])==190 and sum(r['currentGroup'] is None for r in q['rows'])==133)
 ck('Accepted24 remain staged',sum(r['currentPhase']=='actual-exact-accepted-integration-staged-not-applied' for r in q['rows'])==24)
 start=G/'START_HERE.md';direction=R/'docs/DEVELOPMENT_DIRECTION.md';mapfile=G/'REVIEW_MAP.html';nav_before={p:p.read_bytes() for p in [start,direction,mapfile]};newnav={};base='docs/audit/2026-10-08/full-game/'
 for p,prefix in [(start,''),(direction,'../../../')]:
  text=nav_before[p].decode('utf-8-sig');marker='**Current position — 18 October 2026:**';ck('One live position marker '+p.name,text.count(marker)==1)
  notice='**Rank-eight summon and structure source checkpoint:** [Checkpoint37]('+prefix+base+outcp.name+') and [Queue30]('+prefix+outq.relative_to(G).as_posix()+') add Summon Greater Water Pet, Summon Archlich Shade, Faction Paragon, Conjure Sky Fortress and Shifting Fortress to source-review preparation. The [full five-spell packet]('+prefix+base+pp.name+') preserves68 sources, five placements,11 currently reviewed counterparts and two exact accepted Companion10 comparisons;20 choices remain unselected and256 source/preservation checks pass. The Water Pet is individually tierB; the other four are tierC. **This packet is UNSENT; no new procedure, case or rule is adopted.** Queue30 covers190 pending identities in29 groups, with133 still ungrouped. Actual applied counts remain525/323/249; the24 accepted identities remain staged. The recovered-source Control15 review is still active.\n\n'
  text=text.replace(marker,notice+marker,1);text=text.replace('[checkpoint36]('+prefix+base+cpp.name+')','[checkpoint37]('+prefix+base+outcp.name+')',1);text=text.replace('latest observation was 33% remaining','latest observation was 32% remaining',1);newnav[p]=text.encode('utf8')
 html=nav_before[mapfile].decode('utf-8-sig');pos=html.index('</h1>')+len('</h1>');banner='<section class="sequence" aria-label="Latest source preparation"><p><strong>Checkpoint37:five rank8 summon/structure sources prepared.</strong> Summon Greater Water Pet, Summon Archlich Shade, Faction Paragon, Conjure Sky Fortress and Shifting Fortress retain their complete sources.20 decisions remain unselected;256 preservation checks pass. Queue30:190 pending identities in29 prepared/active groups,133 ungrouped. Applied525/323 membership is unchanged;24 accepted spells remain staged. <a href="'+base+outcp.name+'">Latest checkpoint</a> · <a href="'+outq.relative_to(G).as_posix()+'">Queue30</a> · <a href="'+base+pp.name+'">Full source packet</a></p></section>'
 newnav[mapfile]=(html[:pos]+banner+html[pos:]).encode('utf8');ck('Embedded75-domain map data unchanged',newnav[mapfile].decode().replace(banner,'')==html)
 keep.mkdir()
 for p,b in nav_before.items():(keep/p.name).write_bytes(b)
 outq.write_bytes(encoded(q))
 for p,b in newnav.items():p.write_bytes(b)
 cp={'id':'ACTIVE-AUTHORING-RANK8-SUMMON-STRUCTURE-37','recordedAtUtc':now,'status':'Five new rank8 source identities prepared; Control15 full review remains active;24 exact acceptances staged and unapplied.','developmentDirection':'video-game-only','previousCheckpoint':info(cpp),'currentAuthoredIndex':info(idx),'authoredCounts':cp0['authoredCounts'],'currentWorkQueue':info(outq),'preparedGroupCount':29,'groupedPendingIdentities':190,'ungroupedPendingIdentities':133,'rank8SummonStructure5SourceConference':info(pp),'accepted24IntegrationPlan':cp0['accepted24IntegrationPlan'],'accepted24StagingCheck':cp0['accepted24StagingCheck'],'activeGptReviewAtLastVerifiedObservation':cp0['activeGptReviewAtLastVerifiedObservation'],'ownerImplementationReservation':cp0['ownerImplementationReservation'],'proposedSixCorrectionsPreflight':cp0['proposedSixCorrectionsPreflight'],'coverageLedger':info(cov),'currentAcceptedInterfaceRegistry':info(reg),'latestVerifiedGitHubBackup':cp0['latestVerifiedGitHubBackup'],'laterLocalWork':'All work after checkpoint32 remains local, including accepted returns, source recovery,24-spell staging, checkpoints35–37 and the new life/form4 and summon/structure5 packets.','lastUsageObservation':{'usedPercent':68,'remainingPercent':32,'secondaryUnavailable':True,'stopAtRemainingPercent':20},'navigation':[info(p) for p in newnav],'preservedNavigation':[info(keep/p.name) for p in nav_before],'nextAction':'Receive and verify actual full Control15 final without interrupting its live run. Inform GPT of exact staged24 checks and deliver the next prepared source conference. Continue the remaining source queue, keeping all accepted/pending scopes separate. No rule/index implementation before the owner’s reserved instruction.','newRuleAdoptions':0,'runtimeTestsExecuted':0,'all75DomainGatesUnchanged':True,'wholeGameComplete':False,'sourceInformationDeleted':0}
 cp['activeGptReviewAtLastVerifiedObservation']=deepcopy(cp['activeGptReviewAtLastVerifiedObservation'])
 cp['activeGptReviewAtLastVerifiedObservation']['observedProgress']=info(A/'CONTROL15_PART5_RECOVERED_PROGRESS_04_UI.txt')
 cp['activeGptReviewAtLastVerifiedObservation']['latestVisibleStatus']='Creating control review archive generation script; final not yet delivered.'
 outcp.write_bytes(encoded(cp))
 for p,b in protected.items():ck('Protected authority unchanged '+p.relative_to(G).as_posix(),p.read_bytes()==b)
 for p in [outcp,outq,pp,G/prep['archive']['path']]:ck('New navigation target exists '+p.name,p.exists())
 check.write_bytes(encoded({'recordedAtUtc':now,'scope':'Prepared source coverage and navigation only; no semantic or runtime adoption.','checkpoint':info(outcp),'queue':info(outq),'checks':checks,'checkCount':len(checks),'failureCount':0,'sourceInformationDeleted':0,'runtimeTestsExecuted':0}))
 print(json.dumps({'checkpoint':info(outcp),'queue':info(outq),'check':info(check),'checks':len(checks),'grouped':190,'ungrouped':133,'appliedCounts':cp['authoredCounts']}))

if __name__=='__main__':main()
