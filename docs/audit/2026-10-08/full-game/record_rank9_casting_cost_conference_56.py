"""Record a source-only casting/cost conference; preserve applied rules and all prior evidence."""
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
    previous=A/'ACTIVE_AUTHORING_CHECKPOINT_RANK9_TIME_FATE_55.json'
    outcp=A/'ACTIVE_AUTHORING_CHECKPOINT_RANK9_CASTING_COST_56.json'
    oldq=R/'data/director/spell_review/remaining_work_queue_45.json'
    outq=oldq.with_name('remaining_work_queue_46.json')
    pp=A/'RANK9_CASTING_COST_5_SOURCE_CONFERENCE_01_PREPARATION.json'
    checkp=A/'ACTIVE_AUTHORING_CHECKPOINT_RANK9_CASTING_COST_56_CHECK.json'
    keep=A/'navigation-before-rank9-casting-cost-56'
    nativep=A/'GPT_PART5_RANK8_LIVE_AT_CASTING_COST_56_NATIVE.json'
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
    ck('Source-only five-identity five-placement packet',prep['status']=='PREPARED_UNSENT' and
        prep['identityCount']==5 and prep['placementCount']==5 and prep['sourceCount']==117 and
        prep['questionCount']==32 and prep['riskCounts']=={'C':5} and
        sc['checkCount']==341 and sc['failures']==0 and not candidate['currentVectors'] and
        candidate['newRuleAdoptions']==candidate['cosmologyDecisions']==0)
    ck('Twelve complete applied counterparts and four full pending archives',len(candidate['completeAppliedCounterparts'])==12
        and len(candidate['pendingComparisonsNotAuthority'])==4
        and all('completeConferenceArchive' in x for x in candidate['pendingComparisonsNotAuthority']))
    ids=[r['spellId'] for r in candidate['records']]
    ck('Previously ungrouped source identities',len(set(ids))==5 and all(next(r for r in q['rows'] if r['id']==sid)['currentGroup'] is None for sid in ids))
    group={'group':'rank9-casting-cost5','phase':'source-conference-prepared-unsent','identities':ids,'identityCount':5,
        'candidate':prep['candidate'],'preparation':info(pp),'archive':prep['archive'],'adopted':False,
        'sourceCount':117,'placementCount':5,'questionCount':32,'riskCounts':{'C':5},'currentCaseCount':0,
        'latestObservedStatus':'Five complete source identities,five native placements and32 unselected decisions preserve any-spell invocation and cost/component/time waiver,instant rituals,formerly known rank9 replay,all-available-RP pricing and demi-lich/free-necrotic casting.'}
    q['groups'].append(group)
    for old,row in zip(q0['rows'],q['rows']):
        if row['id'] in ids:
            row.update(currentGroup=group['group'],currentPhase=group['phase'],semanticAcceptanceClaimed=False,
                sourceConferencePreparation=info(pp),nextAction='Confer on all32 casting/cost questions with full sources; author complete useful procedures and positive cases after explicit scoped decisions.')
        ck('Complete source/index/history retained '+row['id'],all(old[k]==row[k] for k in ['completeCurrentSourceAndAccess','currentIndexEntryUnchanged','previousAuthoringMapRowUnchanged']))
    q.update(id='REMAINING-WORK-QUEUE-46',recordedAtUtc=now,previousQueue=info(oldq),
        preparedOrActualReviewIdentityCount=275,originalSourceOrReceiptWorkCount=48,
        pendingDistribution=dict(Counter(r['currentPhase'] for r in q['rows'])),latestSourceConference=info(pp))
    q['sourceBindings'].extend([info(pp),prep['candidate'],prep['archive'],prep['check']])
    q['limitations']+=' Current casting/cost5 packet adds117 complete source artifacts,five placements and32 unselected questions;341 preservation checks do not imply acceptance.275 pending identities are grouped and48 rank9 identities remain ungrouped. Actual Rank8Damage6 review continues; Ready successor is locally verified and unapplied.'
    ck('323 pending across43 groups;275 grouped and48 ungrouped',len(q['rows'])==323 and len(q['groups'])==43
        and sum(r['currentGroup'] is not None for r in q['rows'])==275
        and sum(r['currentGroup'] is None for r in q['rows'])==48)
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
        notice=('\n**Latest source preparation — 20 October 2026:** [Checkpoint 56]('+prefix+base+outcp.name+') and [Queue 46]('+prefix+outq.relative_to(G).as_posix()+') add five rank9 casting/cost identities:117 complete source artifacts,five placements,32 unselected questions and341 preservation checks.275 pending identities are grouped;48 remain ungrouped. GPT is reviewing Rank8Damage6. The exact preparation-only Ready proposal is locally verified and unapplied. Applied525/323/249 and39 accepted-but-unapplied identities are unchanged; GitHub backup is verified through52.\n').encode()
        p.write_bytes(raw[:pos]+notice+raw[pos:]);ck('Original navigation retained '+p.name,p.read_bytes().replace(notice,b'',1)==raw)
    p=navpaths[2];raw=nav[p];pos=raw.index(b'</h1>')+len(b'</h1>')
    banner=('<section class="sequence" aria-label="Current rank9 casting and cost preparation"><p><strong>Checkpoint56: five rank9 casting/cost sources prepared.</strong>117 complete source artifacts,five native placements,32 unselected questions;341 preservation checks. Queue46:275 grouped pending identities,48 ungrouped. GPT is actively reviewing Rank8Damage6; no gameplay implementation. <a href="'+base+outcp.name+'">Current checkpoint</a></p></section>').encode()
    p.write_bytes(raw[:pos]+banner+raw[pos:]);ck('All original domain content retained',p.read_bytes().replace(banner,b'',1)==raw)
    cp.update(id='ACTIVE-AUTHORING-RANK9-CASTING-COST-56',recordedAtUtc=now,
        previousCheckpoint=info(previous),currentWorkQueue=info(outq),preparedGroupCount=43,
        groupedPendingIdentities=275,ungroupedPendingIdentities=48,rank9CastingCost5SourceConference=info(pp),
        status='Five complete rank9 casting/cost identities prepared without selections; actual Rank8Damage6 conference remains active.',
        navigation=[info(p) for p in navpaths],preservedNavigation=[info(keep/p.name) for p in navpaths],
        lastUsageObservation={'usedPercent':10,'remainingPercent':90,'stopAtRemainingPercent':20},
        previousGoalTurnClassification='progress: prepared full casting/cost5 sources and updated queue/navigation without mechanic application.',
        laterLocalWork='Post-push checkpoints53-55 and this casting/cost5 packet,Queue46,checkpoint56 and associated navigation/GPT evidence follow verified GitHub backup through52. The failed initial Windows long-path packaging attempt is retained with a recovery receipt; the distinct complete packet verified successfully.',
        nextAction='Retrieve the live Rank8Damage6 conference,then Rank7IdentityCasting5. Continue complete prepared conferences and48 ungrouped rank9 identities,retaining owner implementation reservation and source fidelity. Stop at20 percent remaining.')
    cp['activeGptReviewAtLastVerifiedObservation']['nativeConfirmation']=info(nativep)
    cp['castingPacketPackagingRecovery']=info(A/'RANK9_CASTING_COST_5_PACKAGING_RECOVERY_01.json')
    outcp.write_bytes(encoded(cp))
    for p,raw in protected.items():ck('Protected authority unchanged '+p.relative_to(G).as_posix(),p.read_bytes()==raw)
    checkp.write_bytes(encoded({'recordedAtUtc':now,'checkpoint':info(outcp),'queue':info(outq),'checks':checks,
        'checkCount':len(checks),'failures':0,'newRuleAdoptions':0,'runtimeTestsExecuted':0,'sourceInformationDeleted':0,
        'scope':'Source/history/queue/navigation preservation only; no semantic or runtime adoption.'}))
    print(json.dumps({'checkpoint':info(outcp),'queue':info(outq),'checks':len(checks),'check':info(checkp)}))

if __name__=='__main__':main()
