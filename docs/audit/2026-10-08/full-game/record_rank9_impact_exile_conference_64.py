"""Record four source-only impact/exile identities without applying rules or canon."""
from copy import deepcopy
from collections import Counter
from datetime import datetime, timezone
import json
from record_rank9_memory_denial_conference_57 import G,R,A,read,encoded,info

def main():
    now=datetime.now(timezone.utc).isoformat()
    previous=A/'ACTIVE_AUTHORING_CHECKPOINT_RANK9_SUMMON_HOSTS_63.json'
    outcp=A/'ACTIVE_AUTHORING_CHECKPOINT_RANK9_IMPACT_EXILE_64.json'
    oldq=R/'data/director/spell_review/remaining_work_queue_51.json'
    outq=oldq.with_name('remaining_work_queue_52.json')
    pp=A/'RANK9_IMPACT_EXILE_4_SOURCE_CONFERENCE_01_PREPARATION.json'
    checkp=A/'ACTIVE_AUTHORING_CHECKPOINT_RANK9_IMPACT_EXILE_64_CHECK.json'
    keep=A/'navigation-before-rank9-impact-exile-64'
    nativep=A/'GPT_PART5_RANK7_LIVE_AT_IMPACT_EXILE_64_NATIVE.json'
    browserp=A/'GPT_PART5_RANK7_BROWSER_STATUS_64.json'
    assert not any(p.exists() for p in [outcp,outq,checkp,keep])
    cp,q0,prep,native=map(read,[previous,oldq,pp,nativep]);q=deepcopy(q0)
    candidate=read(G/prep['candidate']['path']);sc=read(G/prep['check']['path']);checks=[]
    def ck(label,ok):
        checks.append({'check':label,'passed':bool(ok)});assert ok,label
    protected_paths=[previous,oldq,R/'data/public/spell_playtests/catalog.json',R/'data/playtest/game_development_coverage.json']
    protected_paths += [G/cp[k]['path'] for k in ['currentAuthoredIndex','currentAcceptedInterfaceRegistry','decisionLedger']]
    protected_paths += [G/b['path'] for b in cp['canonicalHelperBaselinesUnchanged']]
    protected={p:p.read_bytes() for p in protected_paths}
    ck('Exact preceding checkpoint63',info(previous)['sha256']=='7112a8d0d336020b9f4656cecd69483c1088e23f408335071311623b82760b83')
    ck('Exact Queue51 binding',info(oldq)==cp['currentWorkQueue'])
    ck('Full packet artifact bindings',all(info(G/prep[k]['path'])==prep[k] for k in ['candidate','archive','manifest','check','request']))
    ck('Four complete source-only impact/exile identities',prep['status']=='PREPARED_UNSENT' and prep['identityCount']==4 and prep['placementCount']==4 and prep['sourceCount']==149 and prep['questionCount']==26 and prep['riskCounts']=={'C':4} and sc['checkCount']==452 and sc['failures']==0 and not candidate['currentVectors'] and candidate['newRuleAdoptions']==candidate['cosmologyDecisions']==0)
    ck('Thirteen complete applied counterparts and four full pending archives',len(candidate['completeAppliedCounterparts'])==13 and len(candidate['pendingComparisonsNotAuthority'])==4 and all('completeConferenceArchive' in x for x in candidate['pendingComparisonsNotAuthority']))
    ck('All26 choices unselected',len(candidate['questions'])==26 and all(not x['decisionSelected'] for x in candidate['questions']))
    rank8=candidate['unacceptedRank8DamageComparison']
    ck('Unaccepted Rank8 return/findings/corrections fully bound',all(info(G/b['path'])==b for k,b in rank8.items() if k!='qualification') and len(rank8)==9)
    ids=[r['spellId'] for r in candidate['records']]
    ck('Four previously ungrouped identities',len(set(ids))==4 and all(next(r for r in q['rows'] if r['id']==sid)['currentGroup'] is None for sid in ids))
    group={'group':'rank9-impact-exile4','phase':'source-conference-prepared-unsent','identities':ids,'identityCount':4,'candidate':prep['candidate'],'preparation':info(pp),'archive':prep['archive'],'adopted':False,'sourceCount':149,'placementCount':4,'questionCount':26,'riskCounts':{'C':4},'currentCaseCount':0,'latestObservedStatus':'Four full impact/exile sources preserve5d12force hammer/1roundStunned,everything lifted60ft in60ft radius with actual Falling,12d10chosen-energy bodily explosion/resistance bypass,and12d6force/Prone/banishment.26 choices remain unselected. Complete unaccepted Rank8 findings remain comparison evidence.'}
    q['groups'].append(group)
    for old,row in zip(q0['rows'],q['rows']):
        if row['id'] in ids:
            row.update(currentGroup=group['group'],currentPhase=group['phase'],semanticAcceptanceClaimed=False,sourceConferencePreparation=info(pp),nextAction='Confer on26 source-local questions with complete damage/body/geometry/clock/control/exile evidence. Author full positive procedures/cases without imported Falling rules,omitted riders,automatic death or unapproved Rank8 authority.')
        else:ck('Unaffected complete queue row retained '+row['id'],row==old)
        ck('Complete source/index/history retained '+row['id'],all(old[k]==row[k] for k in ['completeCurrentSourceAndAccess','currentIndexEntryUnchanged','previousAuthoringMapRowUnchanged']))
    q['previousSummaryBefore64']={'limitations':q0['limitations'],'preparedOrActualReviewIdentityCount':q0['preparedOrActualReviewIdentityCount'],'originalSourceOrReceiptWorkCount':q0['originalSourceOrReceiptWorkCount']}
    q.update(id='REMAINING-WORK-QUEUE-52',recordedAtUtc=now,previousQueue=info(oldq),preparedOrActualReviewIdentityCount=300,originalSourceOrReceiptWorkCount=23,pendingDistribution=dict(Counter(r['currentPhase'] for r in q['rows'])),latestSourceConference=info(pp))
    q['sourceBindings'].extend([info(pp),prep['candidate'],prep['archive'],prep['check']])
    q['limitations']='Current through checkpoint64: applied525/323/249 and173 interfaces unchanged;39 accepted-but-unapplied. Rank8Damage6 retains8 local findings and an unsent correction packet. Rank7IdentityCasting5 remains active in fresh native and visible browser observations.48 groups cover300 pending identities;23 rank9 identities remain ungrouped. Impact/exile4 preserves149 full sources,4 placements,26 unselected questions and452 preservation checks. No semantic acceptance,runtime or cosmology adoption. Backup through61 is verified; owner implementation reservation and separate completion gates remain.'
    ck('323 pending across48 groups;300 grouped and23 ungrouped',len(q['rows'])==323 and len(q['groups'])==48 and sum(r['currentGroup'] is not None for r in q['rows'])==300 and sum(r['currentGroup'] is None for r in q['rows'])==23)
    ck('39 accepted but unapplied unchanged',sum(r['currentPhase'] in ['actual-exact-accepted-integration-staged-not-applied','actual-full-conference-accepted-successor-not-applied'] for r in q['rows'])==39)
    ck('Remaining ungrouped all rank9',all(min(a['rank'] for a in r['completeCurrentSourceAndAccess']['classAccess'].values())==9 for r in q['rows'] if r['currentGroup'] is None))
    ck('Every earlier group unchanged',q['groups'][:-1]==q0['groups'])
    ck('Actual Rank7 request active without completed response',native['thread']['id']=='6ad4a867-f330-83e9-829e-bf2bb41a6c09' and native['thread']['status']['type']=='active' and native['turns'][0]['id']=='300380f5-c52b-471a-9eb5-f8251396eac2' and not any(x['type']=='agentMessage' for x in native['turns'][0]['items']))
    browser=read(browserp)
    ck('Visible Stop control observed without interruption',browser['visibleStopControl']==2045 and not browser['messageSent'] and not browser['interrupted'])
    for b in cp['navigation']:ck('Previous navigation binding '+b['path'],info(G/b['path'])==b)
    navpaths=[G/'START_HERE.md',R/'docs/DEVELOPMENT_DIRECTION.md',G/'REVIEW_MAP.html']
    nav={p:p.read_bytes() for p in navpaths};base='docs/audit/2026-10-08/full-game/'
    keep.mkdir()
    for p,raw in nav.items():(keep/p.name).write_bytes(raw)
    outq.write_bytes(encoded(q))
    for p,prefix in [(navpaths[0],''),(navpaths[1],'../../../')]:
        raw=nav[p];pos=raw.index(b'\n')+1
        notice=('\n**Latest source preparation — 20 October 2026:** [Checkpoint64]('+prefix+base+outcp.name+') and [Queue52]('+prefix+outq.relative_to(G).as_posix()+') add four rank9 impact/exile identities:149 full source artifacts,4 placements,26 unselected questions and452 preservation checks.300 pending identities are grouped;23 remain ungrouped. GPT continues Rank7IdentityCasting5; Rank8 awaits8 bounded corrections. Applied525/323/249 and39 accepted-but-unapplied stay unchanged. Backup is verified through61; no gameplay or cosmology application.\n').encode()
        p.write_bytes(raw[:pos]+notice+raw[pos:]);ck('Original navigation retained '+p.name,p.read_bytes().replace(notice,b'',1)==raw)
    p=navpaths[2];raw=nav[p];pos=raw.index(b'</h1>')+len(b'</h1>')
    banner=('<section class="sequence" aria-label="Current rank9 impact and exile preparation"><p><strong>Checkpoint64: four rank9 impact/exile sources prepared.</strong>149 full sources,4 placements,26 unselected questions;452 preservation checks. Queue52:300 grouped pending identities,23 ungrouped. GPT continues Rank7; Rank8 corrections remain queued. No gameplay or cosmology adoption. <a href="'+base+outcp.name+'">Current checkpoint</a></p></section>').encode()
    p.write_bytes(raw[:pos]+banner+raw[pos:]);ck('Full original review map retained',p.read_bytes().replace(banner,b'',1)==raw)
    cp.update(id='ACTIVE-AUTHORING-RANK9-IMPACT-EXILE-64',recordedAtUtc=now,previousCheckpoint=info(previous),currentWorkQueue=info(outq),preparedGroupCount=48,groupedPendingIdentities=300,ungroupedPendingIdentities=23,rank9ImpactExile4SourceConference=info(pp),status='Four complete rank9 impact/exile sources prepared without selections; actual Rank7 remains active and Rank8 corrections remain unsent.',navigation=[info(p) for p in navpaths],preservedNavigation=[info(keep/p.name) for p in navpaths],lastUsageObservation={'usedPercent':17,'remainingPercent':83,'stopAtRemainingPercent':20},previousGoalTurnClassification='progress: full impact/exile4 source conference with26 explicit unresolved questions,149 full sources and452 preservation checks; queue/navigation updated with all canonical authorities unchanged.',laterLocalWork='Checkpoint62/63,summon-hosts5,and this impact-exile4 packet,Queue52,checkpoint64 and navigation follow verified GitHub backup through61.',nextAction='Do not interrupt active Rank7IdentityCasting5. Preserve/verify its final return,then deliver prepared Rank8 bounded corrections and require a complete successor. Continue23 ungrouped rank9 sources and full pending conferences. Preserve owner implementation reservation; stop at20 percent remaining.')
    cp['activeGptReviewAtLastVerifiedObservation']['nativeConfirmation']=info(nativep)
    cp['activeGptReviewAtLastVerifiedObservation']['latestBrowserStatus']=info(browserp)
    cp['activeGptReviewAtLastVerifiedObservation']['note']='Fresh native request remains active; visible Chrome Stop control2045 confirms ongoing response. No interruption or new message.'
    cp['queueObservationSupersession']='Queue52 preserves every earlier group and changes only four previously ungrouped identities into source-only preparation. Existing Rank8 correction status remains intact.'
    outcp.write_bytes(encoded(cp))
    for p,raw in protected.items():ck('Protected authority unchanged '+p.relative_to(G).as_posix(),p.read_bytes()==raw)
    checkp.write_bytes(encoded({'recordedAtUtc':now,'checkpoint':info(outcp),'queue':info(outq),'checks':checks,'checkCount':len(checks),'failures':0,'newRuleAdoptions':0,'runtimeTestsExecuted':0,'sourceInformationDeleted':0,'scope':'Full source/history/queue/navigation preservation only; no semantic acceptance,engine runtime or cosmology adoption.'}))
    print(json.dumps({'checkpoint':info(outcp),'queue':info(outq),'checks':len(checks),'check':info(checkp)}))

if __name__=='__main__':main()
