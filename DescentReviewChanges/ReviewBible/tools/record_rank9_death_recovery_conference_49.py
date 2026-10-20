"""Record completed source preparation and verified backup; retain all mechanics unchanged."""
from collections import Counter
from copy import deepcopy
from datetime import datetime,timezone
import json
from apply_di7_ap_as_01 import G,R,A,info,encoded

def read(p):return json.loads(p.read_bytes())

def main():
    now=datetime.now(timezone.utc).isoformat()
    qp=R/'data/director/spell_review/remaining_work_queue_39.json';outq=qp.with_name('remaining_work_queue_40.json')
    previous=A/'ACTIVE_AUTHORING_CHECKPOINT_GPT_OWNER_DIRECTION_48.json'
    outcp=A/'ACTIVE_AUTHORING_CHECKPOINT_RANK9_DEATH_RECOVERY_49.json'
    check=A/'ACTIVE_AUTHORING_CHECKPOINT_RANK9_DEATH_RECOVERY_49_CHECK.json'
    keep=A/'navigation-before-rank9-death-recovery-49'
    pp=A/'RANK9_DEATH_RECOVERY_7_SOURCE_CONFERENCE_01_PREPARATION.json'
    assert not any(p.exists() for p in [outq,outcp,check,keep])
    q0=read(qp);q=deepcopy(q0);cp=deepcopy(read(previous));prep=read(pp)
    candidate=read(G/prep['candidate']['path']);sourcecheck=read(G/prep['check']['path']);checks=[]
    def ck(label,ok):
        checks.append({'check':label,'passed':bool(ok)});assert ok,label
    protected={p:p.read_bytes() for p in [qp,previous,R/'data/public/spell_playtests/authored_review_index.json',
        R/'data/public/spell_playtests/catalog.json',R/'data/playtest/game_development_coverage.json',
        R/'data/director/spell_review/accepted_interface_registry_06.json']}
    ck('Exact packet artifact bindings',all(info(G/prep[k]['path'])==prep[k] for k in ['candidate','archive','check','manifest','request']))
    ck('Unsent preservation-only packet',prep['status']=='PREPARED_UNSENT' and candidate['newRuleAdoptions']==candidate['cosmologyDecisions']==0 and not candidate['currentVectors'])
    ck('All source checks pass',sourcecheck['checkCount']==265 and sourcecheck['failures']==0 and prep['sourceCount']==74 and len(candidate['completeAppliedCounterparts'])==8)
    ids=[r['spellId'] for r in candidate['records']]
    ck('Seven previously ungrouped identities',len(set(ids))==7 and all(next(r for r in q['rows'] if r['id']==sid)['currentGroup'] is None for sid in ids))
    group={'group':'rank9-death-recovery7','phase':'source-conference-prepared-unsent','identities':ids,'identityCount':7,
        'candidate':prep['candidate'],'preparation':info(pp),'archive':prep['archive'],'adopted':False,
        'sourceCount':74,'placementCount':10,'questionCount':22,'riskCounts':{'C':6,'B':1},'currentCaseCount':0,
        'latestObservedStatus':'Seven complete native identities,ten placements,eight applied counterparts and22 unselected questions preserve actual death,damage,healing,return and resource operations.'}
    q['groups'].append(group)
    for before,row in zip(q0['rows'],q['rows']):
        if row['id'] in ids:
            row.update(currentGroup=group['group'],currentPhase=group['phase'],semanticAcceptanceClaimed=False,
                nextAction='Confer on death/recovery7,including all22 scoped questions; author complete useful procedures and actual source-qualified cases only after decisions.',
                sourceConferencePreparation=info(pp))
        ck('Complete source/index/history retained '+row['id'],all(before[k]==row[k] for k in ['completeCurrentSourceAndAccess','currentIndexEntryUnchanged','previousAuthoringMapRowUnchanged']))
    q.update(id='REMAINING-WORK-QUEUE-40',recordedAtUtc=now,previousQueue=info(qp),
        preparedOrActualReviewIdentityCount=241,originalSourceOrReceiptWorkCount=82,
        pendingDistribution=dict(Counter(r['currentPhase'] for r in q['rows'])),latestSourceConference=info(pp),
        latestOwnerDecisionLedger=info(A/'PERTINENT_GPT_DECISIONS_2026_10_20_01.json'))
    q['sourceBindings'].extend([info(pp),prep['candidate'],prep['archive'],prep['check'],info(A/'PERTINENT_GPT_DECISIONS_2026_10_20_01.json')])
    q['limitations']+=' Death/recovery7 adds74 full sources,10placements and22 unselected questions;265 preservation checks are not semantic acceptance.82 ungrouped rank9 identities remain. Preparation-only copied-feat Ready supersedes older both-round proposal; exact successor is under actual GPT review.39 accepted identities remain unapplied.'
    ck('323 pending across38 groups and82 ungrouped',len(q['rows'])==323 and len(q['groups'])==38 and sum(r['currentGroup'] is not None for r in q['rows'])==241 and sum(r['currentGroup'] is None for r in q['rows'])==82)
    ck('39 accepted but unapplied',sum(r['currentPhase'] in ['actual-exact-accepted-integration-staged-not-applied','actual-full-conference-accepted-successor-not-applied'] for r in q['rows'])==39)
    ck('Remaining ungrouped actualrank9',all(min(a['rank'] for a in r['completeCurrentSourceAndAccess']['classAccess'].values())==9 for r in q['rows'] if r['currentGroup'] is None))
    pushp=G/'docs/audit/2026-10-20/github-snapshot-owner-direction48/PUSH_RECEIPT.json';push=read(pushp)
    ck('Remote backup verified',push['commit']==push['remoteMain']=='7f31e24274b216470ccce57d4e456d7bdc585961' and push['trackedEntriesDeleted']==0 and push['worktreeClean'])
    livep=A/'GPT_PART5_READY_08_LIVE_AT_DEATH_RECOVERY_49_NATIVE.json';live=read(livep)
    ck('Actual existing GPT request remains active',live['thread']['id']=='6ad4a867-f330-83e9-829e-bf2bb41a6c09' and live['thread']['status']['type']=='active' and live['turns'][0]['id']=='645d2ea1-1dd1-418f-aae2-4596255253ea')
    start=G/'START_HERE.md';direction=R/'docs/DEVELOPMENT_DIRECTION.md';mapfile=G/'REVIEW_MAP.html'
    nav={p:p.read_bytes() for p in [start,direction,mapfile]};after={};base='docs/audit/2026-10-08/full-game/'
    for p,prefix in [(start,''),(direction,'../../../')]:
        raw=nav[p];pos=raw.index(b'\n')+1
        notice=('\n**Latest source preparation —20 October2026:** [Checkpoint49]('+prefix+base+outcp.name+') and [Queue40]('+prefix+outq.relative_to(G).as_posix()+') add seven rank9 death/recovery spells,74 complete sources,10placements and22 unselected questions.265 source checks pass;241 pending identities are grouped and82 remain ungrouped. GPT is reviewing the preparation-only Ready successor. Applied525/323/249 and39 accepted-but-unapplied identities remain unchanged. [GitHub7f31e24](https://github.com/BordelonDevOps/DecenniumDescent/commit/7f31e24274b216470ccce57d4e456d7bdc585961) verifies backup through48 with zero file deletions; this packet and checkpoint are later local work. Owner three-mode direction and the implementation reservation remain active.\n').encode()
        after[p]=raw[:pos]+notice+raw[pos:]
        ck('Original navigation preserved '+p.name,after[p].replace(notice,b'',1)==raw)
    raw=nav[mapfile];marker=b'</h1>';pos=raw.index(marker)+len(marker)
    banner=('<section class="sequence" aria-label="Latest death and recovery preparation"><p><strong>Checkpoint49: seven rank9 death/recovery sources prepared.</strong>74 complete sources,10 placements,22 unselected decisions;265 preservation checks. Queue40:241 grouped pending identities,82 ungrouped. Owner direction:SNES-style CRPG with exploration,tactical combat and companion management. Preparation-only copied-feat Ready supersedes the old both-round proposal; exact review remains active. No rule implementation. <a href="'+base+outcp.name+'">Current checkpoint</a> · <a href="'+base+'PERTINENT_GPT_DECISIONS_2026_10_20_01.json">Owner decisions</a></p></section>').encode()
    after[mapfile]=raw[:pos]+banner+raw[pos:]
    ck('All domain content retained',after[mapfile].replace(banner,b'',1)==raw)
    keep.mkdir()
    for p,b in nav.items():(keep/p.name).write_bytes(b)
    outq.write_bytes(encoded(q))
    for p,b in after.items():p.write_bytes(b)
    cp.update(id='ACTIVE-AUTHORING-RANK9-DEATH-RECOVERY-49',recordedAtUtc=now,
        status='Seven rank9 death/recovery sources prepared; owner direction and correction evidence verified on GitHub through48; preparation-only Ready exact successor review remains active.',
        previousCheckpoint=info(previous),currentWorkQueue=info(outq),preparedGroupCount=38,
        groupedPendingIdentities=241,ungroupedPendingIdentities=82,rank9DeathRecovery7SourceConference=info(pp),
        navigation=[info(p) for p in after],preservedNavigation=[info(keep/p.name) for p in nav],
        latestPreviouslyVerifiedGitHubBackup={'commit':push['commit'],'throughCheckpoint':48,'receipt':info(pushp)},
        laterLocalWork='Death/recovery7,Queue40/checkpoint49,live GPT observation and the post-push receipt are later local work.',
        lastUsageObservation={'usedPercent':5,'remainingPercent':95,'stopAtRemainingPercent':20},
        previousGoalTurnClassification='progress: recorded actual owner decisions,verified supplement02 and updated navigation without mechanic application.',
        nextAction='Retrieve the existing active preparation-only Ready successor request; verify exact return before any integration. Continue the already-delivered Rank8Damage6/Rank7IdentityCasting5 and82 remaining rank9 source identities. Preserve owner implementation reservation and stop at20percent remaining.')
    cp['activeGptReviewAtLastVerifiedObservation'].update(nativeConfirmation=info(livep),sent=True,completedResponseReceived=False)
    outcp.write_bytes(encoded(cp))
    for p,b in protected.items():ck('Protected authority unchanged '+p.relative_to(G).as_posix(),p.read_bytes()==b)
    check.write_bytes(encoded({'recordedAtUtc':now,'checkpoint':info(outcp),'queue':info(outq),'checks':checks,
        'checkCount':len(checks),'failureCount':0,'newRuleAdoptions':0,'sourceInformationDeleted':0,'runtimeTestsExecuted':0,
        'scope':'Full queue membership/source/history preservation,navigation and verified backup; no semantic or runtime acceptance.'}))
    print(json.dumps({'checkpoint':info(outcp),'queue':info(outq),'check':info(check),'checks':len(checks),'grouped':241,'ungrouped':82}))

if __name__=='__main__':main()

