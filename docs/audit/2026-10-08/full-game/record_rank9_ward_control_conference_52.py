"""Record a source-only ward conference; preserve applied rules and all prior evidence."""
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
    previous=A/'ACTIVE_AUTHORING_CHECKPOINT_READY_SUCCESSOR_RANK8_REVIEW_51.json'
    outcp=A/'ACTIVE_AUTHORING_CHECKPOINT_RANK9_WARD_CONTROL_52.json'
    oldq=R/'data/director/spell_review/remaining_work_queue_42.json'
    outq=oldq.with_name('remaining_work_queue_43.json')
    pp=A/'RANK9_WARD_CONTROL_6_SOURCE_CONFERENCE_01_PREPARATION.json'
    checkp=A/'ACTIVE_AUTHORING_CHECKPOINT_RANK9_WARD_CONTROL_52_CHECK.json'
    keep=A/'navigation-before-rank9-ward-control-52'
    nativep=A/'GPT_PART5_RANK8_LIVE_AT_WARD_CONTROL_52_NATIVE.json'
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
    ck('Source-only six-identity seven-placement packet',prep['status']=='PREPARED_UNSENT' and
        prep['identityCount']==6 and prep['placementCount']==7 and prep['sourceCount']==91 and
        prep['questionCount']==24 and prep['riskCounts']=={'C':6} and
        sc['checkCount']==319 and sc['failures']==0 and not candidate['currentVectors'] and
        candidate['newRuleAdoptions']==candidate['cosmologyDecisions']==0)
    ck('Nine complete applied counterparts and four full pending archives',len(candidate['completeAppliedCounterparts'])==9
        and len(candidate['pendingComparisonsNotAuthority'])==4
        and all('completeConferenceArchive' in x for x in candidate['pendingComparisonsNotAuthority']))
    ids=[r['spellId'] for r in candidate['records']]
    ck('Previously ungrouped source identities',len(set(ids))==6 and all(next(r for r in q['rows'] if r['id']==sid)['currentGroup'] is None for sid in ids))
    group={'group':'rank9-ward-control6','phase':'source-conference-prepared-unsent','identities':ids,'identityCount':6,
        'candidate':prep['candidate'],'preparation':info(pp),'archive':prep['archive'],'adopted':False,
        'sourceCount':91,'placementCount':7,'questionCount':24,'riskCounts':{'C':6},'currentCaseCount':0,
        'latestObservedStatus':'Six complete source identities and24 unselected decisions preserve all-spell reflection,all-magic ending,both RealityAnchor placements,permanent site protection,all-harm24hour protection and seven prismatic layers.'}
    q['groups'].append(group)
    for old,row in zip(q0['rows'],q['rows']):
        if row['id'] in ids:
            row.update(currentGroup=group['group'],currentPhase=group['phase'],semanticAcceptanceClaimed=False,
                sourceConferencePreparation=info(pp),nextAction='Confer on all24 ward/control questions with full sources; author complete useful procedures and positive cases after explicit scoped decisions.')
        ck('Complete source/index/history retained '+row['id'],all(old[k]==row[k] for k in ['completeCurrentSourceAndAccess','currentIndexEntryUnchanged','previousAuthoringMapRowUnchanged']))
    q.update(id='REMAINING-WORK-QUEUE-43',recordedAtUtc=now,previousQueue=info(oldq),
        preparedOrActualReviewIdentityCount=255,originalSourceOrReceiptWorkCount=68,
        pendingDistribution=dict(Counter(r['currentPhase'] for r in q['rows'])),latestSourceConference=info(pp))
    q['sourceBindings'].extend([info(pp),prep['candidate'],prep['archive'],prep['check']])
    q['limitations']+=' Current ward/control6 packet adds91 complete source artifacts,seven placements and24 unselected questions;319 preservation checks do not imply acceptance.255 pending identities are grouped and68 rank9 identities remain ungrouped. Actual Rank8Damage6 review continues; Ready successor is locally verified and unapplied.'
    ck('323 pending across40 groups;255 grouped and68 ungrouped',len(q['rows'])==323 and len(q['groups'])==40
        and sum(r['currentGroup'] is not None for r in q['rows'])==255
        and sum(r['currentGroup'] is None for r in q['rows'])==68)
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
        notice=('\n**Latest source preparation — 20 October 2026:** [Checkpoint 52]('+prefix+base+outcp.name+') and [Queue 43]('+prefix+outq.relative_to(G).as_posix()+') add six rank9 ward/control identities:91 complete source artifacts,seven placements,24 unselected questions and319 preservation checks.255 pending identities are grouped;68 remain ungrouped. GPT is reviewing Rank8Damage6. The exact preparation-only Ready proposal is locally verified and unapplied. Applied525/323/249 and39 accepted-but-unapplied identities are unchanged; GitHub backup remains through48.\n').encode()
        p.write_bytes(raw[:pos]+notice+raw[pos:]);ck('Original navigation retained '+p.name,p.read_bytes().replace(notice,b'',1)==raw)
    p=navpaths[2];raw=nav[p];pos=raw.index(b'</h1>')+len(b'</h1>')
    banner=('<section class="sequence" aria-label="Current rank9 ward preparation"><p><strong>Checkpoint52: six rank9 ward/control sources prepared.</strong>91 complete source artifacts,seven native placements,24 unselected questions;319 preservation checks. Queue43:255 grouped pending identities,68 ungrouped. GPT is actively reviewing Rank8Damage6; no gameplay implementation. <a href="'+base+outcp.name+'">Current checkpoint</a></p></section>').encode()
    p.write_bytes(raw[:pos]+banner+raw[pos:]);ck('All original domain content retained',p.read_bytes().replace(banner,b'',1)==raw)
    cp.update(id='ACTIVE-AUTHORING-RANK9-WARD-CONTROL-52',recordedAtUtc=now,
        previousCheckpoint=info(previous),currentWorkQueue=info(outq),preparedGroupCount=40,
        groupedPendingIdentities=255,ungroupedPendingIdentities=68,rank9WardControl6SourceConference=info(pp),
        status='Six complete rank9 ward/control identities prepared without selections; actual Rank8Damage6 conference remains active.',
        navigation=[info(p) for p in navpaths],preservedNavigation=[info(keep/p.name) for p in navpaths],
        lastUsageObservation={'usedPercent':7,'remainingPercent':93,'stopAtRemainingPercent':20},
        previousGoalTurnClassification='progress: prepared full ward/control6 sources and updated queue/navigation without mechanic application.',
        laterLocalWork='Checkpoints49–52, queues40–43, three new rank9 source conferences,Ready successor/preflight,owner ledger02 and subsequent navigation/GPT evidence follow verified GitHub backup through48.',
        nextAction='Retrieve the live Rank8Damage6 conference,then Rank7IdentityCasting5. Continue complete prepared conferences and68 ungrouped rank9 identities,retaining owner implementation reservation and source fidelity. Stop at20 percent remaining.')
    cp['activeGptReviewAtLastVerifiedObservation']['nativeConfirmation']=info(nativep)
    outcp.write_bytes(encoded(cp))
    for p,raw in protected.items():ck('Protected authority unchanged '+p.relative_to(G).as_posix(),p.read_bytes()==raw)
    checkp.write_bytes(encoded({'recordedAtUtc':now,'checkpoint':info(outcp),'queue':info(outq),'checks':checks,
        'checkCount':len(checks),'failures':0,'newRuleAdoptions':0,'runtimeTestsExecuted':0,'sourceInformationDeleted':0,
        'scope':'Source/history/queue/navigation preservation only; no semantic or runtime adoption.'}))
    print(json.dumps({'checkpoint':info(outcp),'queue':info(outq),'checks':len(checks),'check':info(checkp)}))

if __name__=='__main__':main()
