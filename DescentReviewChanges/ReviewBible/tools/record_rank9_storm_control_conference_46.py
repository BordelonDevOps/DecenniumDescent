"""Record six complete source conferences and diagnostic evidence without rule adoption."""
from collections import Counter
from copy import deepcopy
from datetime import datetime, timezone
import json
from apply_di7_ap_as_01 import G, R, A, info, encoded

def read(p): return json.loads(p.read_bytes())

def main():
    now = datetime.now(timezone.utc).isoformat()
    qp = R/'data/director/spell_review/remaining_work_queue_37.json'
    outq = qp.with_name('remaining_work_queue_38.json')
    previous = A/'ACTIVE_AUTHORING_CHECKPOINT_RANK9_CATASTROPHE_45.json'
    outcp = A/'ACTIVE_AUTHORING_CHECKPOINT_RANK9_STORM_CONTROL_46.json'
    check = A/'ACTIVE_AUTHORING_CHECKPOINT_RANK9_STORM_CONTROL_46_CHECK.json'
    keep = A/'navigation-before-rank9-storm-control-46'
    pp = A/'RANK9_STORM_CONTROL_6_SOURCE_CONFERENCE_01_PREPARATION.json'
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
    ck('Complete source check', sourcecheck['checkCount'] == 292 and sourcecheck['failures'] == 0 and len(candidate['completeAppliedCounterparts']) == 10)
    ids = [r['spellId'] for r in candidate['records']]
    ck('Six previously ungrouped identities', len(set(ids)) == 6 and all(next(r for r in q['rows'] if r['id'] == sid)['currentGroup'] is None for sid in ids))
    group = {'group':'rank9-storm-control6', 'phase':'source-conference-prepared-unsent',
        'identities':ids, 'identityCount':6, 'candidate':prep['candidate'], 'preparation':info(pp),
        'archive':prep['archive'], 'adopted':False, 'sourceCount':78, 'placementCount':6,
        'questionCount':25, 'riskCounts':{'B':2,'C':4}, 'currentCaseCount':0,
        'latestObservedStatus':'Six complete native sources,10 applied counterparts and25 unselected decisions preserve actual pull/time-stop/fire pulses/varied storm/five lightning strikes/cannot-escape containment.'}
    q['groups'].append(group)
    for before,row in zip(q0['rows'],q['rows']):
        if row['id'] in ids:
            row.update(currentGroup=group['group'], currentPhase=group['phase'], semanticAcceptanceClaimed=False,
                nextAction='Confer on the complete storm/control6 sources and25 questions; select substantive timing, geometry, state, five-strike and confinement choices before full procedure/vector authorship.',
                sourceConferencePreparation=info(pp))
        ck('Full source/index/history unchanged '+row['id'],all(before[k] == row[k] for k in ['completeCurrentSourceAndAccess','currentIndexEntryUnchanged','previousAuthoringMapRowUnchanged']))
    q.update(id='REMAINING-WORK-QUEUE-38',recordedAtUtc=now,previousQueue=info(qp),
        preparedOrActualReviewIdentityCount=227,originalSourceOrReceiptWorkCount=96,
        pendingDistribution=dict(Counter(r['currentPhase'] for r in q['rows'])),latestSourceConference=info(pp))
    q['sourceBindings'].extend([info(pp),prep['candidate'],prep['archive'],prep['check']])
    q['limitations'] += ' Rank9 storm/control6 adds78 full sources,six placements and25 unselected questions.292 preservation checks are not semantic acceptance.96 ungrouped identities remain,all actualrank9.39 accepted identities remain unapplied.'
    ck('323 pending across36 groups and96 ungrouped',len(q['rows']) == 323 and len(q['groups']) == 36 and sum(r['currentGroup'] is not None for r in q['rows']) == 227 and sum(r['currentGroup'] is None for r in q['rows']) == 96)
    ck('39 accepted identities remain unapplied',sum(r['currentPhase'] in ['actual-exact-accepted-integration-staged-not-applied','actual-full-conference-accepted-successor-not-applied'] for r in q['rows']) == 39)
    ck('Remaining ungrouped allrank9',all(min(a['rank'] for a in r['completeCurrentSourceAndAccess']['classAccess'].values()) == 9 for r in q['rows'] if r['currentGroup'] is None))
    pushp = G/'docs/audit/2026-10-18/github-snapshot-rank9-sources/PUSH_RECEIPT.json'; push = read(pushp)
    ck('Verified latest backup',push['commit'] == push['remoteMain'] == '372cb8a66d590811014ecbc8fc7c51ef5c67d955' and push['trackedEntriesDeleted'] == 0)
    diagp = A/'COPIED_FEAT_PART5_LOCAL_DEFECT_REPRODUCTION_02.json'; diag = read(diagp)
    ck('Six independently reproduced groups',diag['totalLocallyReproducedDefectGroupsAcrossReceipts'] == 6 and diag['unchangedArchivedPythonFiles'] == 38 and not diag['implementationApplied'])
    start=G/'START_HERE.md';direction=R/'docs/DEVELOPMENT_DIRECTION.md';mapfile=G/'REVIEW_MAP.html'
    nav={p:p.read_bytes() for p in [start,direction,mapfile]};after={};base='docs/audit/2026-10-08/full-game/'
    for p,prefix in [(start,''),(direction,'../../../')]:
        text=nav[p].decode('utf-8-sig');marker='**Current position — 18 October 2026:**'
        ck('One current position marker '+p.name,text.count(marker)==1)
        notice='**Latest work — rank-nine storms and control:** [Checkpoint46]('+prefix+base+outcp.name+') and [Queue38]('+prefix+outq.relative_to(G).as_posix()+') add six spells with78 full sources,10 applied counterparts and25 unselected decisions.292 preservation checks pass.227 pending identities have review groups;96 rank9 identities remain ungrouped. [Additional local diagnostics]('+prefix+base+diagp.name+') bring the independently reproduced copied-feat defects to six groups. GPT reports preparing its correction archive; the final is not yet received. Applied525/323/249 and39 accepted-but-unapplied identities remain unchanged.\n\n'
        after[p]=text.replace(marker,notice+marker,1).encode('utf8')
    html=nav[mapfile].decode('utf-8-sig');pos=html.index('</h1>')+len('</h1>')
    banner='<section class="sequence" aria-label="Latest storm and control preparation"><p><strong>Checkpoint46:six rank9 storm/control sources prepared.</strong>78 sources,10 applied counterparts,25 unselected decisions;292 preservation checks. Queue38:227 grouped pending identities,96 ungrouped rank9. Six copied-feat defect groups reproduced; final GPT correction archive pending. No rule application. <a href="'+base+outcp.name+'">Latest checkpoint</a> · <a href="'+outq.relative_to(G).as_posix()+'">Queue38</a></p></section>'
    after[mapfile]=(html[:pos]+banner+html[pos:]).encode('utf8')
    ck('All domain content retained',after[mapfile].decode().replace(banner,'')==html)
    keep.mkdir()
    for p,b in nav.items():(keep/p.name).write_bytes(b)
    outq.write_bytes(encoded(q))
    for p,b in after.items():p.write_bytes(b)
    cp.update(id='ACTIVE-AUTHORING-RANK9-STORM-CONTROL-46',recordedAtUtc=now,
        status='Six rank9 storm/control sources prepared; six copied-feat defect groups preserved; actual GPT final pending and39 accepted spells remain unapplied.',
        previousCheckpoint=info(previous),currentWorkQueue=info(outq),preparedGroupCount=36,
        groupedPendingIdentities=227,ungroupedPendingIdentities=96,rank9StormControl6SourceConference=info(pp),
        navigation=[info(p) for p in after],preservedNavigation=[info(keep/p.name) for p in nav],
        latestVerifiedGitHubBackup={'commit':push['commit'],'throughCheckpoint':45,'receipt':info(pushp)},
        laterLocalWork='Diagnostics02, GPT catch-up/recovery observations, storm/control6 source packet and Queue38/checkpoint46 are later local work after verified backup372cb8a.',
        additionalLocalCopiedFeatDiagnostics=info(diagp),additionalLocalDiagnosticScript=info(A/'inspect_copy_part5_defects_02.py'),
        lastUsageObservation={'usedPercent':77,'remainingPercent':23,'secondaryUnavailable':True,'stopAtRemainingPercent':20},
        preparedGptFollowup={'request':info(A/'GPT_PART5_COPIED_FEAT_LOCAL_FINDINGS_06_UNSENT.txt'),'sent':False,'reason':'Do not interrupt the active copied-feat review. Update this pre-46 draft with the newest queue before sending.'},
        nextAction='Receive the actual copied-feat final archive, independently verify complete corrections and compare six local defect groups. Continue96 ungrouped rank9 identities; preserve owner-reserved implementation.')
    cp['activeGptReviewAtLastVerifiedObservation'].update(
        browserProof=info(A/'GPT_PART5_COPY_REVIEW_04_PROGRESS_46_UI.txt'),
        lastVisibleProgress='GPT reports regression tests complete and a manifest-bound archive prepared. No final download is visible yet. Its claimed47 tests/fixes remain unverified locally.',
        finalReceived=False,observedAtUtc=now)
    cp['gptCatchupRecovery']=info(A/'GPT_PART5_PERTINENT_CHECK_02_RECOVERY_STATUS.json')
    outcp.write_bytes(encoded(cp))
    for p,b in protected.items():ck('Protected authority unchanged '+p.relative_to(G).as_posix(),p.read_bytes()==b)
    check.write_bytes(encoded({'recordedAtUtc':now,'scope':'Source preparation, complete history/diagnostic preservation and navigation only.',
        'checkpoint':info(outcp),'queue':info(outq),'checks':checks,'checkCount':len(checks),'failureCount':0,
        'newRuleAdoptions':0,'sourceInformationDeleted':0,'runtimeTestsExecuted':0}))
    print(json.dumps({'checkpoint':info(outcp),'queue':info(outq),'check':info(check),'checks':len(checks),'grouped':227,'ungrouped':96}))

if __name__=='__main__':main()
