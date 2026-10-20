"""Record a source-only time/fate conference; preserve applied rules and all prior evidence."""
from pathlib import Path
from copy import deepcopy
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json

G=Path(r'C:\Github\DecenniumDescent')
R=G/'DescentReviewChanges/ReviewBible'
A=G/'docs/audit/2026-10-08/full-game'

def read(p):return json.loads(p.read_bytes())
def encoded(d):return (json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode()
def info(p):
    raw=p.read_bytes();return {'path':p.relative_to(G).as_posix(),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}

def main():
    now=datetime.now(timezone.utc).isoformat()
    previous=A/'ACTIVE_AUTHORING_CHECKPOINT_RANK9_AGENCY_CONTROL_54.json'
    outcp=A/'ACTIVE_AUTHORING_CHECKPOINT_RANK9_TIME_FATE_55.json'
    oldq=R/'data/director/spell_review/remaining_work_queue_44.json'
    outq=oldq.with_name('remaining_work_queue_45.json')
    pp=A/'RANK9_TIME_FATE_6_SOURCE_CONFERENCE_01_PREPARATION.json'
    checkp=A/'ACTIVE_AUTHORING_CHECKPOINT_RANK9_TIME_FATE_55_CHECK.json'
    keep=A/'navigation-before-rank9-time-fate-55'
    nativep=A/'GPT_PART5_RANK8_LIVE_AT_TIME_FATE_55_NATIVE.json'
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
    ck('Source-only six-identity eight-placement packet',prep['status']=='PREPARED_UNSENT' and
        prep['identityCount']==6 and prep['placementCount']==8 and prep['sourceCount']==140 and
        prep['questionCount']==32 and prep['riskCounts']=={'C':5,'B':1} and
        sc['checkCount']==415 and sc['failures']==0 and not candidate['currentVectors'] and
        candidate['newRuleAdoptions']==candidate['cosmologyDecisions']==0)
    ck('Ten complete applied counterparts and five full pending archives',len(candidate['completeAppliedCounterparts'])==10
        and len(candidate['pendingComparisonsNotAuthority'])==5
        and all('completeConferenceArchive' in x for x in candidate['pendingComparisonsNotAuthority']))
    ids=[r['spellId'] for r in candidate['records']]
    ck('Previously ungrouped source identities',len(set(ids))==6 and all(next(r for r in q['rows'] if r['id']==sid)['currentGroup'] is None for sid in ids))
    group={'group':'rank9-time-fate6','phase':'source-conference-prepared-unsent','identities':ids,'identityCount':6,
        'candidate':prep['candidate'],'preparation':info(pp),'archive':prep['archive'],'adopted':False,
        'sourceCount':140,'placementCount':8,'questionCount':32,'riskCounts':{'C':5,'B':1},'currentCaseCount':0,
        'latestObservedStatus':'Six complete source identities,eight native placements and32 unselected decisions preserve both Time Stop variants,enemy d20 rerolls,hour-long foresight defenses,past-event rewrite,alternate battlefield future and guaranteed prophecy.'}
    q['groups'].append(group)
    for old,row in zip(q0['rows'],q['rows']):
        if row['id'] in ids:
            row.update(currentGroup=group['group'],currentPhase=group['phase'],semanticAcceptanceClaimed=False,
                sourceConferencePreparation=info(pp),nextAction='Confer on all32 time/fate questions with full sources; author complete useful procedures and positive cases after explicit scoped decisions.')
        ck('Complete source/index/history retained '+row['id'],all(old[k]==row[k] for k in ['completeCurrentSourceAndAccess','currentIndexEntryUnchanged','previousAuthoringMapRowUnchanged']))
    q.update(id='REMAINING-WORK-QUEUE-45',recordedAtUtc=now,previousQueue=info(oldq),
        preparedOrActualReviewIdentityCount=270,originalSourceOrReceiptWorkCount=53,
        pendingDistribution=dict(Counter(r['currentPhase'] for r in q['rows'])),latestSourceConference=info(pp))
    q['sourceBindings'].extend([info(pp),prep['candidate'],prep['archive'],prep['check']])
    q['limitations']+=' Current time/fate6 packet adds140 complete source artifacts,eight placements and32 unselected questions;415 preservation checks do not imply acceptance.270 pending identities are grouped and53 rank9 identities remain ungrouped. Actual Rank8Damage6 review continues; Ready successor is locally verified and unapplied.'
    ck('323 pending across42 groups;270 grouped and53 ungrouped',len(q['rows'])==323 and len(q['groups'])==42
        and sum(r['currentGroup'] is not None for r in q['rows'])==270
        and sum(r['currentGroup'] is None for r in q['rows'])==53)
    ck('39 accepted but unapplied unchanged',sum(r['currentPhase'] in ['actual-exact-accepted-integration-staged-not-applied','actual-full-conference-accepted-successor-not-applied'] for r in q['rows'])==39)
    ck('Remaining ungrouped native rank9',all(min(a['rank'] for a in r['completeCurrentSourceAndAccess']['classAccess'].values())==9 for r in q['rows'] if r['currentGroup'] is None))
    ck('Actual existing rank8 request remains active',native['thread']['id']=='6ad4a867-f330-83e9-829e-bf2bb41a6c09'
        and native['thread']['status']['type']=='active' and native['turns'][0]['id']=='e642823a-1f56-42e5-b786-8d1e3f5a85f3')
    navpaths=[G/'START_HERE.md',R/'docs/DEVELOPMENT_DIRECTION.md',G/'REVIEW_MAP.html']
    nav={p:p.read_bytes() for p in navpaths};base='docs/audit/2026-10-08/full-game/'
    keep.mkdir()
    for p,raw in nav.items():(keep/p.name).write_bytes(raw)
    outq.write_bytes(encoded(q))
    for p,prefix in [(navpaths[0],''),(navpaths[1],'../../../')]:
        raw=nav[p];pos=raw.index(b'\n')+1
        notice=('\n**Latest source preparation — 20 October 2026:** [Checkpoint 55]('+prefix+base+outcp.name+') and [Queue 45]('+prefix+outq.relative_to(G).as_posix()+') add six rank9 time/fate identities:140 complete source artifacts,eight placements,32 unselected questions and415 preservation checks.270 pending identities are grouped;53 remain ungrouped. GPT is reviewing Rank8Damage6. The exact preparation-only Ready proposal is locally verified and unapplied. Applied525/323/249 and39 accepted-but-unapplied identities are unchanged; GitHub backup is verified through52.\n').encode()
        p.write_bytes(raw[:pos]+notice+raw[pos:]);ck('Original navigation retained '+p.name,p.read_bytes().replace(notice,b'',1)==raw)
    p=navpaths[2];raw=nav[p];pos=raw.index(b'</h1>')+len(b'</h1>')
    banner=('<section class="sequence" aria-label="Current rank9 time and fate preparation"><p><strong>Checkpoint55: six rank9 time/fate sources prepared.</strong>140 complete source artifacts,eight native placements,32 unselected questions;415 preservation checks. Queue45:270 grouped pending identities,53 ungrouped. GPT is actively reviewing Rank8Damage6; no gameplay implementation. <a href="'+base+outcp.name+'">Current checkpoint</a></p></section>').encode()
    p.write_bytes(raw[:pos]+banner+raw[pos:]);ck('All original domain content retained',p.read_bytes().replace(banner,b'',1)==raw)
    cp.update(id='ACTIVE-AUTHORING-RANK9-TIME-FATE-55',recordedAtUtc=now,
        previousCheckpoint=info(previous),currentWorkQueue=info(outq),preparedGroupCount=42,
        groupedPendingIdentities=270,ungroupedPendingIdentities=53,rank9TimeFate6SourceConference=info(pp),
        status='Six complete rank9 time/fate identities prepared without selections; actual Rank8Damage6 conference remains active.',
        navigation=[info(p) for p in navpaths],preservedNavigation=[info(keep/p.name) for p in navpaths],
        lastUsageObservation={'usedPercent':9,'remainingPercent':91,'stopAtRemainingPercent':20},
        previousGoalTurnClassification='progress: prepared full time/fate6 sources and updated queue/navigation without mechanic application.',
        laterLocalWork='Post-push checkpoint53,agency/control9 checkpoint54 and this time/fate6 packet,Queue45,checkpoint55 and associated navigation/GPT evidence follow verified GitHub backup through52.',
        nextAction='Retrieve the live Rank8Damage6 conference,then Rank7IdentityCasting5. Continue complete prepared conferences and53 ungrouped rank9 identities,retaining owner implementation reservation and source fidelity. Stop at20 percent remaining.')
    cp['activeGptReviewAtLastVerifiedObservation']['nativeConfirmation']=info(nativep)
    outcp.write_bytes(encoded(cp))
    for p,raw in protected.items():ck('Protected authority unchanged '+p.relative_to(G).as_posix(),p.read_bytes()==raw)
    checkp.write_bytes(encoded({'recordedAtUtc':now,'checkpoint':info(outcp),'queue':info(outq),'checks':checks,
        'checkCount':len(checks),'failures':0,'newRuleAdoptions':0,'runtimeTestsExecuted':0,'sourceInformationDeleted':0,
        'scope':'Source/history/queue/navigation preservation only; no semantic or runtime adoption.'}))
    print(json.dumps({'checkpoint':info(outcp),'queue':info(outq),'checks':len(checks),'check':info(checkp)}))

if __name__=='__main__':main()
