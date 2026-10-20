"""One-shot source-preparation checkpoint; does not apply spell or cosmology rules."""
from copy import deepcopy
from collections import Counter
from datetime import datetime, timezone
import json
from record_rank9_memory_denial_conference_57 import G,R,A,read,encoded,info

def main():
    now=datetime.now(timezone.utc).isoformat()
    previous=A/'ACTIVE_AUTHORING_CHECKPOINT_RANK9_KNOWLEDGE_REVELATION_60.json'
    outcp=A/'ACTIVE_AUTHORING_CHECKPOINT_RANK9_PLANAR_GATES_61.json'
    oldq=R/'data/director/spell_review/remaining_work_queue_49.json'
    outq=oldq.with_name('remaining_work_queue_50.json')
    pp=A/'RANK9_PLANAR_GATES_5_SOURCE_CONFERENCE_01_PREPARATION.json'
    checkp=A/'ACTIVE_AUTHORING_CHECKPOINT_RANK9_PLANAR_GATES_61_CHECK.json'
    keep=A/'navigation-before-rank9-planar-gates-61'
    nativep=A/'GPT_PART5_RANK7_LIVE_AT_PLANAR_GATES_61_NATIVE.json'
    browserp=A/'GPT_PART5_RANK7_BROWSER_STATUS_60.json'
    assert not any(p.exists() for p in [outcp,outq,checkp,keep])
    cp,q0,prep,native=map(read,[previous,oldq,pp,nativep]);q=deepcopy(q0)
    candidate=read(G/prep['candidate']['path']);sc=read(G/prep['check']['path']);checks=[]
    def ck(label,ok):
        checks.append({'check':label,'passed':bool(ok)});assert ok,label
    protected_paths=[previous,oldq,R/'data/public/spell_playtests/catalog.json',R/'data/playtest/game_development_coverage.json']
    protected_paths += [G/cp[k]['path'] for k in ['currentAuthoredIndex','currentAcceptedInterfaceRegistry','decisionLedger']]
    protected_paths += [G/b['path'] for b in cp['canonicalHelperBaselinesUnchanged']]
    protected={p:p.read_bytes() for p in protected_paths}
    ck('Exact full packet artifact bindings',all(info(G/prep[k]['path'])==prep[k] for k in ['candidate','archive','manifest','check','request']))
    ck('Source-only five-identity seven-placement packet',prep['status']=='PREPARED_UNSENT' and
        prep['identityCount']==5 and prep['placementCount']==7 and prep['sourceCount']==132 and
        prep['questionCount']==30 and prep['riskCounts']=={'C':5} and
        sc['checkCount']==406 and sc['failures']==0 and not candidate['currentVectors'] and
        candidate['newRuleAdoptions']==candidate['cosmologyDecisions']==0)
    ck('Eleven complete applied comparisons and four full pending archives',len(candidate['completeAppliedCounterparts'])==11 and
        len(candidate['pendingComparisonsNotAuthority'])==4 and all('completeConferenceArchive' in x for x in candidate['pendingComparisonsNotAuthority']))
    ck('All30 questions remain unselected',len(candidate['questions'])==30 and all(not x['decisionSelected'] for x in candidate['questions']))
    ids=[r['spellId'] for r in candidate['records']]
    ck('Previously ungrouped source identities',len(set(ids))==5 and all(next(r for r in q['rows'] if r['id']==sid)['currentGroup'] is None for sid in ids))
    group={'group':'rank9-planar-gates5','phase':'source-conference-prepared-unsent','identities':ids,'identityCount':5,
        'candidate':prep['candidate'],'preparation':info(pp),'archive':prep['archive'],'adopted':False,
        'sourceCount':132,'placementCount':7,'questionCount':30,'riskCounts':{'C':5},'currentCaseCount':0,
        'latestObservedStatus':'Five complete planar/gate sources with30 unselected decisions preserve broad portal reach,permanent known-place gates,automatic type-based exile,specific-plane effect immunity and permanent extradimensional fortification. No new cosmology or operating procedure selected.'}
    q['groups'].append(group)
    for old,row in zip(q0['rows'],q['rows']):
        if row['id'] in ids:
            row.update(currentGroup=group['group'],currentPhase=group['phase'],semanticAcceptanceClaimed=False,
                sourceConferencePreparation=info(pp),nextAction='Confer on all30 planar/gate questions with complete sources,current owner corrections and actual travel,body,custody,expedition and clock interfaces; author useful full procedures and positive cases after scoped decisions.')
        else:ck('Unaffected complete queue row retained '+row['id'],row==old)
        ck('Full source/index/history retained '+row['id'],all(old[k]==row[k] for k in ['completeCurrentSourceAndAccess','currentIndexEntryUnchanged','previousAuthoringMapRowUnchanged']))
    q['previousSummaryBefore61']={'limitations':q0['limitations'],'preparedOrActualReviewIdentityCount':286,'originalSourceOrReceiptWorkCount':37}
    q.update(id='REMAINING-WORK-QUEUE-50',recordedAtUtc=now,previousQueue=info(oldq),
        preparedOrActualReviewIdentityCount=291,originalSourceOrReceiptWorkCount=32,
        pendingDistribution=dict(Counter(r['currentPhase'] for r in q['rows'])),latestSourceConference=info(pp))
    q['sourceBindings'].extend([info(pp),prep['candidate'],prep['archive'],prep['check']])
    q['limitations']='Current through checkpoint61: applied525/323/249 and173 interfaces unchanged;39 accepted-but-unapplied. Rank8Damage6 retains8 local findings and its unsent correction packet. Rank7IdentityCasting5 remains active in a fresh native observation.46 groups cover291 pending identities;32 rank9 identities remain ungrouped. The new planar/gates5 packet preserves132 complete sources,seven placements,30 unselected questions and406 source checks. Earlier summaries remain history. No semantic acceptance,runtime or cosmology adoption;owner implementation reservation and all separate completion gates remain.'
    ck('323 pending across46 groups;291 grouped and32 ungrouped',len(q['rows'])==323 and len(q['groups'])==46 and
        sum(r['currentGroup'] is not None for r in q['rows'])==291 and sum(r['currentGroup'] is None for r in q['rows'])==32)
    ck('39 accepted but unapplied unchanged',sum(r['currentPhase'] in ['actual-exact-accepted-integration-staged-not-applied','actual-full-conference-accepted-successor-not-applied'] for r in q['rows'])==39)
    ck('Remaining ungrouped native rank9',all(min(a['rank'] for a in r['completeCurrentSourceAndAccess']['classAccess'].values())==9 for r in q['rows'] if r['currentGroup'] is None))
    ck('Every earlier group unchanged',q['groups'][:-1]==q0['groups'])
    ck('Actual rank7 request remains active',native['thread']['id']=='6ad4a867-f330-83e9-829e-bf2bb41a6c09' and
        native['thread']['status']['type']=='active' and native['turns'][0]['id']=='300380f5-c52b-471a-9eb5-f8251396eac2' and
        not any(x['type']=='agentMessage' for x in native['turns'][0]['items']))
    navpaths=[G/'START_HERE.md',R/'docs/DEVELOPMENT_DIRECTION.md',G/'REVIEW_MAP.html']
    nav={p:p.read_bytes() for p in navpaths};base='docs/audit/2026-10-08/full-game/'
    keep.mkdir()
    for p,raw in nav.items():(keep/p.name).write_bytes(raw)
    outq.write_bytes(encoded(q))
    for p,prefix in [(navpaths[0],''),(navpaths[1],'../../../')]:
        raw=nav[p];pos=raw.index(b'\n')+1
        notice=('\n**Latest source preparation — 20 October 2026:** [Checkpoint 61]('+prefix+base+outcp.name+') and [Queue 50]('+prefix+outq.relative_to(G).as_posix()+') add five rank9 planar/gate identities:132 complete source artifacts,seven placements,30 unselected questions and406 preservation checks.291 pending identities are grouped;32 remain ungrouped. GPT continues Rank7IdentityCasting5; Rank8Damage6 awaits eight bounded corrections. Applied525/323/249 and39 accepted-but-unapplied stay unchanged. No new cosmology or gameplay rule applied; GitHub backup is verified through57.\n').encode()
        p.write_bytes(raw[:pos]+notice+raw[pos:]);ck('Original navigation retained '+p.name,p.read_bytes().replace(notice,b'',1)==raw)
    p=navpaths[2];raw=nav[p];pos=raw.index(b'</h1>')+len(b'</h1>')
    banner=('<section class="sequence" aria-label="Current rank9 planar gate preparation"><p><strong>Checkpoint61: five rank9 planar/gate sources prepared.</strong>132 complete artifacts,seven placements,30 unselected questions;406 preservation checks. Queue50:291 grouped pending identities,32 ungrouped. GPT continues Rank7IdentityCasting5; Rank8 requires bounded corrections. No gameplay or cosmology adoption. <a href="'+base+outcp.name+'">Current checkpoint</a></p></section>').encode()
    p.write_bytes(raw[:pos]+banner+raw[pos:]);ck('All original domain content retained',p.read_bytes().replace(banner,b'',1)==raw)
    cp.update(id='ACTIVE-AUTHORING-RANK9-PLANAR-GATES-61',recordedAtUtc=now,
        previousCheckpoint=info(previous),currentWorkQueue=info(outq),preparedGroupCount=46,
        groupedPendingIdentities=291,ungroupedPendingIdentities=32,rank9PlanarGates5SourceConference=info(pp),
        status='Five complete rank9 planar/gate identities prepared without selections; actual Rank7IdentityCasting5 remains active. Rank8 corrections remain prepared unsent.',
        navigation=[info(p) for p in navpaths],preservedNavigation=[info(keep/p.name) for p in navpaths],
        lastUsageObservation={'usedPercent':15,'remainingPercent':85,'stopAtRemainingPercent':20},
        previousGoalTurnClassification='progress: full planar/gates5 sources,30 explicit unselected questions and406 source checks; queue/navigation updated without rule or canon application.',
        laterLocalWork='Checkpoints58-60,Rank8 return/semantic findings/correction packet,knowledge/revelation5,and this planar/gates5 packet,Queue50,checkpoint61 and navigation follow verified GitHub backup through57.',
        nextAction='Do not interrupt active Rank7IdentityCasting5. Preserve/verify its completed response,then deliver the prepared Rank8 bounded corrections and require a full successor. Continue32 ungrouped rank9 sources while preserving owner implementation reservation. Stop at20 percent remaining.')
    cp['activeGptReviewAtLastVerifiedObservation']['nativeConfirmation']=info(nativep)
    cp['activeGptReviewAtLastVerifiedObservation']['latestBrowserStatus']=info(browserp)
    cp['activeGptReviewAtLastVerifiedObservation']['note']='Fresh native observation confirms ongoing Rank7 response without a completed final. The preserved preceding browser refresh also showed live Stop control. No interruption or new message.'
    cp['queueObservationSupersession']='Queue50 preserves all earlier groups and changes only five previously ungrouped identities into a source-only conference. Queue48 status corrections and Queue49 knowledge preparation remain intact.'
    outcp.write_bytes(encoded(cp))
    for p,raw in protected.items():ck('Protected authority unchanged '+p.relative_to(G).as_posix(),p.read_bytes()==raw)
    checkp.write_bytes(encoded({'recordedAtUtc':now,'checkpoint':info(outcp),'queue':info(outq),'checks':checks,
        'checkCount':len(checks),'failures':0,'newRuleAdoptions':0,'runtimeTestsExecuted':0,'sourceInformationDeleted':0,
        'scope':'Source/history/queue/navigation preservation only; no semantic acceptance,engine runtime or cosmology adoption.'}))
    print(json.dumps({'checkpoint':info(outcp),'queue':info(outq),'checks':len(checks),'check':info(checkp)}))

if __name__=='__main__':main()
