"""Record seven complete sources and the actual copied-feat return without rule adoption."""
from collections import Counter
from copy import deepcopy
from datetime import datetime, timezone
import json
from apply_di7_ap_as_01 import G, R, A, info, encoded

def read(p): return json.loads(p.read_bytes())

def main():
    now = datetime.now(timezone.utc).isoformat()
    qp = R/'data/director/spell_review/remaining_work_queue_38.json'
    outq = qp.with_name('remaining_work_queue_39.json')
    previous = A/'ACTIVE_AUTHORING_CHECKPOINT_RANK9_STORM_CONTROL_46.json'
    outcp = A/'ACTIVE_AUTHORING_CHECKPOINT_RANK9_PSYCHIC_FEAR_47.json'
    check = A/'ACTIVE_AUTHORING_CHECKPOINT_RANK9_PSYCHIC_FEAR_47_CHECK.json'
    keep = A/'navigation-before-rank9-psychic-fear-47'
    pp = A/'RANK9_PSYCHIC_FEAR_7_SOURCE_CONFERENCE_01_PREPARATION.json'
    assert not any(p.exists() for p in [outq, outcp, check, keep])
    q0 = read(qp); q = deepcopy(q0); cp = read(previous); prep = read(pp)
    candidate = read(G/prep['candidate']['path']); sourcecheck = read(G/prep['check']['path']); checks = []
    def ck(label, value):
        checks.append({'check': label, 'passed': bool(value)}); assert value, label
    protected = {p:p.read_bytes() for p in [qp, previous,
        R/'data/public/spell_playtests/authored_review_index.json',
        R/'data/public/spell_playtests/catalog.json', R/'data/playtest/game_development_coverage.json',
        R/'data/director/spell_review/accepted_interface_registry_06.json']}
    ck('All packet bindings exact', all(info(G/prep[k]['path']) == prep[k] for k in ['candidate','archive','check','manifest','request']))
    ck('Preservation-only preparation', prep['status'] == 'PREPARED_UNSENT' and candidate['newRuleAdoptions'] == candidate['cosmologyDecisions'] == 0 and not candidate['currentVectors'])
    ck('Complete source check', sourcecheck['checkCount'] == 303 and sourcecheck['failures'] == 0 and len(candidate['completeAppliedCounterparts']) == 7)
    ids = [r['spellId'] for r in candidate['records']]
    ck('Seven previously ungrouped identities', len(set(ids)) == 7 and all(next(r for r in q['rows'] if r['id'] == sid)['currentGroup'] is None for sid in ids))
    group = {'group':'rank9-psychic-fear7', 'phase':'source-conference-prepared-unsent',
        'identities':ids, 'identityCount':7, 'candidate':prep['candidate'], 'preparation':info(pp),
        'archive':prep['archive'], 'adopted':False, 'sourceCount':84, 'placementCount':10,
        'questionCount':23, 'riskCounts':{'B':4,'C':3}, 'currentCaseCount':0,
        'latestObservedStatus':'Seven full identities,10 placements,seven applied counterparts and23 unselected decisions preserve school variants,head consequences,actual flight,nightmare captivity and secondary effects.'}
    q['groups'].append(group)
    for before,row in zip(q0['rows'],q['rows']):
        if row['id'] in ids:
            row.update(currentGroup=group['group'], currentPhase=group['phase'], semanticAcceptanceClaimed=False,
                nextAction='Confer on psychic/fear7 and23 questions,including actual school variants,head destruction,flight,nightmare captivity and full secondary-effect procedures before authoring vectors.',
                sourceConferencePreparation=info(pp))
        ck('Full source/index/history unchanged '+row['id'],all(before[k] == row[k] for k in ['completeCurrentSourceAndAccess','currentIndexEntryUnchanged','previousAuthoringMapRowUnchanged']))
    q.update(id='REMAINING-WORK-QUEUE-39',recordedAtUtc=now,previousQueue=info(qp),
        preparedOrActualReviewIdentityCount=234,originalSourceOrReceiptWorkCount=89,
        pendingDistribution=dict(Counter(r['currentPhase'] for r in q['rows'])),latestSourceConference=info(pp))
    q['sourceBindings'].extend([info(pp),prep['candidate'],prep['archive'],prep['check']])
    q['limitations'] += ' Rank9 psychic/fear7 adds84 full sources,10 placements and23 unselected questions.303 preservation checks are not semantic acceptance.89 ungrouped identities remain,all actualrank9.39 accepted identities remain unapplied.'
    ck('323 pending across37 groups and89 ungrouped',len(q['rows']) == 323 and len(q['groups']) == 37 and sum(r['currentGroup'] is not None for r in q['rows']) == 234 and sum(r['currentGroup'] is None for r in q['rows']) == 89)
    ck('39 accepted identities remain unapplied',sum(r['currentPhase'] in ['actual-exact-accepted-integration-staged-not-applied','actual-full-conference-accepted-successor-not-applied'] for r in q['rows']) == 39)
    ck('Remaining ungrouped allrank9',all(min(a['rank'] for a in r['completeCurrentSourceAndAccess']['classAccess'].values()) == 9 for r in q['rows'] if r['currentGroup'] is None))
    pushp = G/'docs/audit/2026-10-18/github-snapshot-storm-control46/PUSH_RECEIPT.json'; push = read(pushp)
    ck('Verified latest backup',push['commit'] == push['remoteMain'] == 'ccb9047a76e9807250feee6d72285c268957d20b' and push['trackedEntriesDeleted'] == 0)
    diagp = A/'COPIED_FEAT_PART5_LOCAL_DEFECT_REPRODUCTION_02.json'; diag = read(diagp)
    ck('Six independently reproduced groups',diag['totalLocallyReproducedDefectGroupsAcrossReceipts'] == 6 and diag['unchangedArchivedPythonFiles'] == 38 and not diag['implementationApplied'])
    start=G/'START_HERE.md';direction=R/'docs/DEVELOPMENT_DIRECTION.md';mapfile=G/'REVIEW_MAP.html'
    nav={p:p.read_bytes() for p in [start,direction,mapfile]};after={};base='docs/audit/2026-10-08/full-game/'
    for p,prefix in [(start,''),(direction,'../../../')]:
        text=nav[p].decode('utf-8-sig');marker='**Current position — 18 October 2026:**'
        ck('One current position marker '+p.name,text.count(marker)==1)
        notice='**Latest work — psychic and fear sources:** [Checkpoint47]('+prefix+base+outcp.name+') and [Queue39]('+prefix+outq.relative_to(G).as_posix()+') add seven rank9 spells with84 full sources,10 placements and23 unselected decisions.303 preservation checks pass.234 pending identities have groups;89 remain ungrouped. GPT’s copied-feat final archive is preserved and108 independent integrity checks pass;two locally reproduced defects remain unresolved and were sent back with full evidence. Applied525/323/249 and39 accepted-but-unapplied identities remain unchanged.\n\n'
        after[p]=text.replace(marker,notice+marker,1).encode('utf8')
    html=nav[mapfile].decode('utf-8-sig');pos=html.index('</h1>')+len('</h1>')
    banner='<section class="sequence" aria-label="Latest psychic and fear preparation"><p><strong>Checkpoint47:seven rank9 psychic/fear sources prepared.</strong>84 sources,10 placements,23 unselected decisions;303 preservation checks. Queue39:234 grouped pending identities,89 ungrouped rank9. Actual copied-feat final preserved;two unresolved local defects sent back. No rule application. <a href="'+base+outcp.name+'">Latest checkpoint</a> · <a href="'+outq.relative_to(G).as_posix()+'">Queue39</a></p></section>'
    after[mapfile]=(html[:pos]+banner+html[pos:]).encode('utf8')
    ck('All domain content retained',after[mapfile].decode().replace(banner,'')==html)
    keep.mkdir()
    for p,b in nav.items():(keep/p.name).write_bytes(b)
    outq.write_bytes(encoded(q))
    for p,b in after.items():p.write_bytes(b)
    cp.update(id='ACTIVE-AUTHORING-RANK9-PSYCHIC-FEAR-47',recordedAtUtc=now,
        status='Seven rank9 psychic/fear sources prepared; actual copied-feat final preserved with two unresolved local defects returned for follow-up;39 accepted spells remain unapplied.',
        previousCheckpoint=info(previous),currentWorkQueue=info(outq),preparedGroupCount=37,
        groupedPendingIdentities=234,ungroupedPendingIdentities=89,rank9PsychicFear7SourceConference=info(pp),
        navigation=[info(p) for p in after],preservedNavigation=[info(keep/p.name) for p in nav],
        latestVerifiedGitHubBackup={'commit':push['commit'],'throughCheckpoint':46,'receipt':info(pushp)},
        laterLocalWork='Psychic/fear7,actual copied-feat return/preflight,follow-up07 and Queue39/checkpoint47 are later local work after verified backupccb9047.',
        additionalLocalCopiedFeatDiagnostics=info(diagp),additionalLocalDiagnosticScript=info(A/'inspect_copy_part5_defects_02.py'),
        lastUsageObservation={'usedPercent':79,'remainingPercent':21,'secondaryUnavailable':True,'stopAtRemainingPercent':20},
        preparedGptFollowup={'request':info(A/'GPT_PART5_COPIED_FEAT_TWO_REMAINING_07_REQUEST.txt'),'sent':True,'sendResult':info(A/'GPT_PART5_COPIED_FEAT_TWO_REMAINING_07_SEND_RESULT.json'),'reason':'Actual final read and integrity verified;two remaining defects sent with full independent reproduction cases/script.'},
        nextAction='Receive targeted copied-feat follow-up07; independently inspect full histories and proposed code semantics,including the two remaining local defects. Continue89 ungrouped rank9 sources;stop at20percent remaining and preserve owner-reserved implementation.')
    cp['copiedFeatActualFinal']={'archive':info(A/'DD_Part5_Copied_Feat_Integration_Review_01.zip'),
        'nativeFinal':info(A/'GPT_PART5_COPIED_FEAT_FINAL_01_NATIVE.json'),
        'localPreflight':info(A/'COPIED_FEAT_PART5_RETURN_01_LOCAL_PREFLIGHT.json'),
        'exactCodeOperations':11,'liveBaselines':4,'checks':108,'unresolvedLocalDefectGroups':2,'correctionsApplied':False}
    cp['activeGptReviewAtLastVerifiedObservation']={
        'threadId':'6ad4a867-f330-83e9-829e-bf2bb41a6c09','title':'Calibration Review Part 5',
        'previousCompletedAssistant':'cc11c7e4-e63b-4732-874d-ab68bd9b5901',
        'request':info(A/'GPT_PART5_COPIED_FEAT_TWO_REMAINING_07_REQUEST.txt'),
        'sendResult':info(A/'GPT_PART5_COPIED_FEAT_TWO_REMAINING_07_SEND_RESULT.json'),
        'scope':'Two remaining inactive-Mend-reducer/shared-buffer-expiry defects with complete local cases and script.',
        'priorFinalReceived':True,'newFollowupSent':True,'newFollowupFinalReceived':False,'observedAtUtc':now}
    outcp.write_bytes(encoded(cp))
    for p,b in protected.items():ck('Protected authority unchanged '+p.relative_to(G).as_posix(),p.read_bytes()==b)
    check.write_bytes(encoded({'recordedAtUtc':now,'scope':'Source preparation, complete history/diagnostic preservation and navigation only.',
        'checkpoint':info(outcp),'queue':info(outq),'checks':checks,'checkCount':len(checks),'failureCount':0,
        'newRuleAdoptions':0,'sourceInformationDeleted':0,'runtimeTestsExecuted':0}))
    print(json.dumps({'checkpoint':info(outcp),'queue':info(outq),'check':info(check),'checks':len(checks),'grouped':234,'ungrouped':89}))

if __name__=='__main__':main()
