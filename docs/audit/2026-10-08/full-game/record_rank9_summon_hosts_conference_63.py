"""Record complete source preparation; preserve all authority and earlier queue records."""
from copy import deepcopy
from collections import Counter
from datetime import datetime, timezone
import json
from record_rank9_memory_denial_conference_57 import G,R,A,read,encoded,info

def main():
    now=datetime.now(timezone.utc).isoformat()
    previous=A/'ACTIVE_AUTHORING_CHECKPOINT_GITHUB_PLANAR_GATES_62.json'
    outcp=A/'ACTIVE_AUTHORING_CHECKPOINT_RANK9_SUMMON_HOSTS_63.json'
    oldq=R/'data/director/spell_review/remaining_work_queue_50.json'
    outq=oldq.with_name('remaining_work_queue_51.json')
    pp=A/'RANK9_SUMMON_HOSTS_5_SOURCE_CONFERENCE_01_PREPARATION.json'
    checkp=A/'ACTIVE_AUTHORING_CHECKPOINT_RANK9_SUMMON_HOSTS_63_CHECK.json'
    keep=A/'navigation-before-rank9-summon-hosts-63'
    nativep=A/'GPT_PART5_RANK7_LIVE_AT_SUMMON_HOSTS_63_NATIVE.json'
    browserp=A/'GPT_PART5_RANK7_BROWSER_STATUS_63.json'
    assert not any(p.exists() for p in [outcp,outq,checkp,keep])
    cp,q0,prep,native=map(read,[previous,oldq,pp,nativep]);q=deepcopy(q0)
    candidate=read(G/prep['candidate']['path']);sc=read(G/prep['check']['path']);checks=[]
    def ck(label,ok):
        checks.append({'check':label,'passed':bool(ok)});assert ok,label
    protected_paths=[previous,oldq,R/'data/public/spell_playtests/catalog.json',R/'data/playtest/game_development_coverage.json']
    protected_paths += [G/cp[k]['path'] for k in ['currentAuthoredIndex','currentAcceptedInterfaceRegistry','decisionLedger']]
    protected_paths += [G/b['path'] for b in cp['canonicalHelperBaselinesUnchanged']]
    protected={p:p.read_bytes() for p in protected_paths}
    ck('Exact previous checkpoint62',info(previous)['sha256']=='de1cb9d8ca8213f4abe341df1588e57afbdeca74f4d67bc380e5295f7b568652')
    ck('Exact Queue50 binding',info(oldq)==cp['currentWorkQueue'])
    ck('Full packet artifact bindings',all(info(G/prep[k]['path'])==prep[k] for k in ['candidate','archive','manifest','check','request']))
    ck('Five complete source-only summon identities',prep['status']=='PREPARED_UNSENT' and prep['identityCount']==5 and prep['placementCount']==5 and prep['sourceCount']==210 and prep['questionCount']==32 and prep['riskCounts']=={'C':5} and sc['checkCount']==579 and sc['failures']==0 and not candidate['currentVectors'] and candidate['newRuleAdoptions']==candidate['cosmologyDecisions']==0)
    ck('Twelve applied counterparts and two complete pending archives',len(candidate['completeAppliedCounterparts'])==12 and len(candidate['pendingComparisonsNotAuthority'])==2 and all('completeConferenceArchive' in x for x in candidate['pendingComparisonsNotAuthority']))
    ck('All32 questions unselected',len(candidate['questions'])==32 and all(not x['decisionSelected'] for x in candidate['questions']))
    inv=candidate['boundedBestiarySourceInventory']
    ck('All72 original entries retained without operational acceptance',len(inv)==72 and sum(x['directorSealed'] for x in inv)==5 and all(not x['operationalAcceptanceClaimed'] for x in inv))
    ck('Companion exact acceptance content limits retained',candidate['exactAcceptedCompanionContextNotApplied']['contentLimitsUnchanged']['wholeCaseContentHolds']==['IN6-09-A','IN6-09-B'])
    ids=[r['spellId'] for r in candidate['records']]
    ck('Five previously ungrouped identities',len(set(ids))==5 and all(next(r for r in q['rows'] if r['id']==sid)['currentGroup'] is None for sid in ids))
    group={'group':'rank9-summon-hosts5','phase':'source-conference-prepared-unsent','identities':ids,'identityCount':5,'candidate':prep['candidate'],'preparation':info(pp),'archive':prep['archive'],'adopted':False,'sourceCount':210,'placementCount':5,'questionCount':32,'riskCounts':{'C':5},'currentCaseCount':0,'latestObservedStatus':'Five complete summon/host sources and32 unselected decisions preserve elemental/avatar benefits,massive fire serpent,army service,uniqueCR15+herald and all-undead command. Full72-entry original bestiary and exact Companion10 context retained. No profile,rating,eligibility,rule or canon selected.'}
    q['groups'].append(group)
    for old,row in zip(q0['rows'],q['rows']):
        if row['id'] in ids:
            row.update(currentGroup=group['group'],currentPhase=group['phase'],semanticAcceptanceClaimed=False,sourceConferencePreparation=info(pp),nextAction='Confer on32 source-local choices using complete profiles and source evidence; preserve useful positive benefits,actual command budgets,identity,geometry,cargo,agency and ending rules. No unapproved bestiary or CR premise may be declared fulfilled.')
        else:ck('Unaffected complete queue row retained '+row['id'],row==old)
        ck('Complete source/index/history retained '+row['id'],all(old[k]==row[k] for k in ['completeCurrentSourceAndAccess','currentIndexEntryUnchanged','previousAuthoringMapRowUnchanged']))
    q['previousSummaryBefore63']={'limitations':q0['limitations'],'preparedOrActualReviewIdentityCount':q0['preparedOrActualReviewIdentityCount'],'originalSourceOrReceiptWorkCount':q0['originalSourceOrReceiptWorkCount']}
    q.update(id='REMAINING-WORK-QUEUE-51',recordedAtUtc=now,previousQueue=info(oldq),preparedOrActualReviewIdentityCount=296,originalSourceOrReceiptWorkCount=27,pendingDistribution=dict(Counter(r['currentPhase'] for r in q['rows'])),latestSourceConference=info(pp))
    q['sourceBindings'].extend([info(pp),prep['candidate'],prep['archive'],prep['check']])
    q['limitations']='Current through checkpoint63: applied525/323/249 and173 interfaces unchanged;39 accepted-but-unapplied. Rank8Damage6 retains8 local findings and its unsent correction packet. Rank7IdentityCasting5 remains active in fresh native and visible browser observations.47 groups cover296 pending identities;27 rank9 identities remain ungrouped. Summon/hosts5 preserves210 full sources,5 placements,32 unselected questions and579 preservation checks,including72 original bestiary entries. No semantic acceptance,profile/rating,cosmology or runtime adoption. Backup through61 is verified; owner implementation reservation and separate completion gates remain.'
    ck('323 pending across47 groups;296 grouped and27 ungrouped',len(q['rows'])==323 and len(q['groups'])==47 and sum(r['currentGroup'] is not None for r in q['rows'])==296 and sum(r['currentGroup'] is None for r in q['rows'])==27)
    ck('39 accepted but unapplied unchanged',sum(r['currentPhase'] in ['actual-exact-accepted-integration-staged-not-applied','actual-full-conference-accepted-successor-not-applied'] for r in q['rows'])==39)
    ck('Remaining ungrouped all rank9',all(min(a['rank'] for a in r['completeCurrentSourceAndAccess']['classAccess'].values())==9 for r in q['rows'] if r['currentGroup'] is None))
    ck('Every earlier group retained unchanged',q['groups'][:-1]==q0['groups'])
    ck('Actual Rank7 request active without completed response',native['thread']['id']=='6ad4a867-f330-83e9-829e-bf2bb41a6c09' and native['thread']['status']['type']=='active' and native['turns'][0]['id']=='300380f5-c52b-471a-9eb5-f8251396eac2' and not any(x['type']=='agentMessage' for x in native['turns'][0]['items']))
    browser=read(browserp)
    ck('Visible current Stop control observed without interruption',browser['visibleStopControl']==2020 and browser['messageSent']==False and browser['interrupted']==False)
    for b in cp['navigation']:ck('Previous navigation binding '+b['path'],info(G/b['path'])==b)
    navpaths=[G/'START_HERE.md',R/'docs/DEVELOPMENT_DIRECTION.md',G/'REVIEW_MAP.html']
    nav={p:p.read_bytes() for p in navpaths};base='docs/audit/2026-10-08/full-game/'
    keep.mkdir()
    for p,raw in nav.items():(keep/p.name).write_bytes(raw)
    outq.write_bytes(encoded(q))
    for p,prefix in [(navpaths[0],''),(navpaths[1],'../../../')]:
        raw=nav[p];pos=raw.index(b'\n')+1
        notice=('\n**Latest source preparation — 20 October 2026:** [Checkpoint63]('+prefix+base+outcp.name+') and [Queue51]('+prefix+outq.relative_to(G).as_posix()+') add five rank9 summon/host identities:210 complete source artifacts,5 native placements,32 unselected questions and579 preservation checks. All72 original bestiary entries remain source evidence,not approved summon profiles.296 pending identities are grouped;27 remain ungrouped. GPT continues Rank7IdentityCasting5; Rank8 awaits8 bounded corrections. Applied525/323/249 and39 accepted-but-unapplied remain unchanged. Backup is verified through61. No gameplay or cosmology application.\n').encode()
        p.write_bytes(raw[:pos]+notice+raw[pos:]);ck('Original navigation retained '+p.name,p.read_bytes().replace(notice,b'',1)==raw)
    p=navpaths[2];raw=nav[p];pos=raw.index(b'</h1>')+len(b'</h1>')
    banner=('<section class="sequence" aria-label="Current rank9 summon source preparation"><p><strong>Checkpoint63: five rank9 summon/host sources prepared.</strong>210 full sources,5 placements,32 unselected questions;579 preservation checks. Queue51:296 grouped pending identities,27 ungrouped. GPT continues Rank7; Rank8 corrections remain queued. No profile,rating,gameplay or cosmos adopted. <a href="'+base+outcp.name+'">Current checkpoint</a></p></section>').encode()
    p.write_bytes(raw[:pos]+banner+raw[pos:]);ck('Full original review map retained',p.read_bytes().replace(banner,b'',1)==raw)
    cp.update(id='ACTIVE-AUTHORING-RANK9-SUMMON-HOSTS-63',recordedAtUtc=now,previousCheckpoint=info(previous),currentWorkQueue=info(outq),preparedGroupCount=47,groupedPendingIdentities=296,ungroupedPendingIdentities=27,rank9SummonHosts5SourceConference=info(pp),status='Five complete rank9 summon/host identities prepared without selections; actual Rank7 review remains active and Rank8 corrections remain unsent.',navigation=[info(p) for p in navpaths],preservedNavigation=[info(keep/p.name) for p in navpaths],lastUsageObservation={'usedPercent':16,'remainingPercent':84,'stopAtRemainingPercent':20},previousGoalTurnClassification='progress: complete summon/hosts5 source conference with32 unselected questions,210 full source files and579 preservation checks; all72 bestiary entries preserved; queue/navigation updated without canonical implementation.',laterLocalWork='Checkpoint62 and post-push receipt,then summon/hosts5,Queue51,checkpoint63 and navigation follow verified GitHub backup through61.',nextAction='Do not interrupt active Rank7IdentityCasting5. Preserve/verify its final return,then deliver the prepared Rank8 corrections and require a complete successor. Continue27 ungrouped rank9 sources and full pending conferences. Preserve owner implementation reservation; stop at20 percent remaining.')
    cp['activeGptReviewAtLastVerifiedObservation']['nativeConfirmation']=info(nativep)
    cp['activeGptReviewAtLastVerifiedObservation']['latestBrowserStatus']=info(browserp)
    cp['activeGptReviewAtLastVerifiedObservation']['note']='Fresh native request remains active; visible browser has Stop control2020. No interruption or new message.'
    cp['queueObservationSupersession']='Queue51 preserves all earlier groups and changes only five previously ungrouped identities into a source-only conference. Rank8 correction status and all earlier prepared groups remain intact.'
    outcp.write_bytes(encoded(cp))
    for p,raw in protected.items():ck('Protected authority unchanged '+p.relative_to(G).as_posix(),p.read_bytes()==raw)
    checkp.write_bytes(encoded({'recordedAtUtc':now,'checkpoint':info(outcp),'queue':info(outq),'checks':checks,'checkCount':len(checks),'failures':0,'newRuleAdoptions':0,'runtimeTestsExecuted':0,'sourceInformationDeleted':0,'scope':'Complete source/history/queue/navigation preservation; no semantic acceptance,profile/rating validation,engine runtime or cosmology adoption.'}))
    print(json.dumps({'checkpoint':info(outcp),'queue':info(outq),'checks':len(checks),'check':info(checkp)}))

if __name__=='__main__':main()
