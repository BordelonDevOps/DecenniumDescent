"""Record source preparation and current GPT direction without applying gameplay changes."""
from collections import Counter
from copy import deepcopy
from datetime import datetime, timezone
import json
from apply_di7_ap_as_01 import G, R, A, info, encoded


def read(path):
    return json.loads(path.read_bytes())


def main():
    now = datetime.now(timezone.utc).isoformat()
    qp = R / 'data/director/spell_review/remaining_work_queue_40.json'
    outq = qp.with_name('remaining_work_queue_41.json')
    previous = A / 'ACTIVE_AUTHORING_CHECKPOINT_RANK9_DEATH_RECOVERY_49.json'
    outcp = A / 'ACTIVE_AUTHORING_CHECKPOINT_RANK9_DEFENSE_FORM_50.json'
    check = A / 'ACTIVE_AUTHORING_CHECKPOINT_RANK9_DEFENSE_FORM_50_CHECK.json'
    keep = A / 'navigation-before-rank9-defense-form-50'
    pp = A / 'RANK9_DEFENSE_FORM_8_SOURCE_CONFERENCE_01_PREPARATION.json'
    ledger = A / 'PERTINENT_GPT_DECISIONS_2026_10_20_01.json'
    reconciliation = A / 'GPT_DIRECTION_AND_UNITY_ASSESSMENT_RECONCILIATION_50.json'
    assert not any(p.exists() for p in [outq, outcp, check, keep, reconciliation])
    q0 = read(qp)
    q = deepcopy(q0)
    cp = deepcopy(read(previous))
    prep = read(pp)
    candidate = read(G / prep['candidate']['path'])
    sourcecheck = read(G / prep['check']['path'])
    checks = []

    def ck(label, ok):
        checks.append({'check': label, 'passed': bool(ok)})
        assert ok, label

    protected_paths = [qp, previous, ledger,
        R / 'data/public/spell_playtests/authored_review_index.json',
        R / 'data/public/spell_playtests/catalog.json',
        R / 'data/playtest/game_development_coverage.json',
        R / 'data/director/spell_review/accepted_interface_registry_06.json',
        G / 'docs/game-design/SOURCE_EVIDENCE.json']
    protected_paths += [G / record['path'] for record in cp['canonicalHelperBaselinesUnchanged']]
    protected = {p: p.read_bytes() for p in protected_paths}
    ck('Exact packet artifact bindings', all(info(G / prep[k]['path']) == prep[k]
       for k in ['candidate', 'archive', 'check', 'manifest', 'request']))
    ck('Unsent preservation-only packet', prep['status'] == 'PREPARED_UNSENT'
       and candidate['newRuleAdoptions'] == candidate['cosmologyDecisions'] == 0
       and not candidate['currentVectors'])
    ck('All source checks pass', sourcecheck['checkCount'] == 312
       and sourcecheck['failures'] == 0 and prep['sourceCount'] == 87
       and len(candidate['completeAppliedCounterparts']) == 10)
    ids = [r['spellId'] for r in candidate['records']]
    ck('Eight previously ungrouped identities', len(set(ids)) == 8
       and all(next(r for r in q['rows'] if r['id'] == sid)['currentGroup'] is None for sid in ids))
    ck('Expected identities and packet totals', set(ids) == {
        'absolute-immunity', 'astral-shell', 'divine-shield', 'eternal-protection',
        'elemental-shell', 'body-to-void', 'timeless-form', 'invulnerable-sphere'}
       and prep['identityCount'] == prep['placementCount'] == 8
       and prep['questionCount'] == 26 and prep['riskCounts'] == {'C': 6, 'B': 2})
    group = {'group': 'rank9-defense-form8', 'phase': 'source-conference-prepared-unsent',
        'identities': ids, 'identityCount': 8, 'candidate': prep['candidate'],
        'preparation': info(pp), 'archive': prep['archive'], 'adopted': False,
        'sourceCount': 87, 'placementCount': 8, 'questionCount': 26,
        'riskCounts': {'C': 6, 'B': 2}, 'currentCaseCount': 0,
        'latestObservedStatus': 'Eight complete native identities, eight placements, ten applied counterparts and 26 unselected questions preserve immunity, reflection, full forms, temporal interactions and closed barriers.'}
    q['groups'].append(group)
    for before, row in zip(q0['rows'], q['rows']):
        if row['id'] in ids:
            row.update(currentGroup=group['group'], currentPhase=group['phase'],
                semanticAcceptanceClaimed=False,
                nextAction='Confer on defense/form8, including all 26 scoped questions; author complete useful procedures and source-qualified cases after decisions.',
                sourceConferencePreparation=info(pp))
        ck('Complete source/index/history retained ' + row['id'], all(before[k] == row[k]
           for k in ['completeCurrentSourceAndAccess', 'currentIndexEntryUnchanged', 'previousAuthoringMapRowUnchanged']))
    q.update(id='REMAINING-WORK-QUEUE-41', recordedAtUtc=now, previousQueue=info(qp),
        preparedOrActualReviewIdentityCount=249, originalSourceOrReceiptWorkCount=74,
        pendingDistribution=dict(Counter(r['currentPhase'] for r in q['rows'])),
        latestSourceConference=info(pp), latestOwnerDecisionLedger=info(ledger))
    q['sourceBindings'].extend([info(pp), prep['candidate'], prep['archive'], prep['check']])
    q['limitations'] += ' Defense/form8 adds 87 full sources, eight placements and 26 unselected questions; 312 preservation checks are not semantic acceptance. Current ungrouped rank9 count is 74. Older counts in retained history describe their original checkpoints. Preparation-only copied-feat Ready remains under GPT review; 39 accepted identities remain unapplied.'
    ck('323 pending across 39 groups and 74 ungrouped', len(q['rows']) == 323
       and len(q['groups']) == 39 and sum(r['currentGroup'] is not None for r in q['rows']) == 249
       and sum(r['currentGroup'] is None for r in q['rows']) == 74)
    ck('39 accepted but unapplied', sum(r['currentPhase'] in [
        'actual-exact-accepted-integration-staged-not-applied',
        'actual-full-conference-accepted-successor-not-applied'] for r in q['rows']) == 39)
    ck('Remaining ungrouped actual rank9', all(min(a['rank'] for a in
        r['completeCurrentSourceAndAccess']['classAccess'].values()) == 9
        for r in q['rows'] if r['currentGroup'] is None))
    pushp = G / 'docs/audit/2026-10-20/github-snapshot-owner-direction48/PUSH_RECEIPT.json'
    push = read(pushp)
    ck('Remote backup verified', push['commit'] == push['remoteMain'] ==
       '7f31e24274b216470ccce57d4e456d7bdc585961'
       and push['trackedEntriesDeleted'] == 0 and push['worktreeClean'])
    livep = A / 'GPT_PART5_READY_08_RECHECK_AT_50_NATIVE.json'
    unityp = A / 'GPT_UNITY_DIRECTION_RECHECK_AT_50_NATIVE.json'
    live = read(livep)
    unity = read(unityp)
    ck('Existing GPT request remains active', live['thread']['id'] ==
       '6ad4a867-f330-83e9-829e-bf2bb41a6c09' and live['thread']['status']['type'] == 'active'
       and live['turns'][0]['id'] == '645d2ea1-1dd1-418f-aae2-4596255253ea')
    oldunity = read(A / 'GPT_UNITY_DEVELOPMENT_SETUP_2026_10_20_NATIVE.json')
    ck('Unity direction has no later turns since preserved owner discussion',
       unity['thread']['id'] == oldunity['thread']['id'] and
       [(t['id'], t['items']) for t in unity['turns']] == [(t['id'], t['items']) for t in oldunity['turns']])
    start = G / 'START_HERE.md'
    direction = R / 'docs/DEVELOPMENT_DIRECTION.md'
    mapfile = G / 'REVIEW_MAP.html'
    design = G / 'docs/game-design/UNITY_DESIGN_EVALUATION.md'
    nav = {p: p.read_bytes() for p in [start, direction, mapfile, design]}
    after = {}
    base = 'docs/audit/2026-10-08/full-game/'
    historical_evidence = read(G / 'docs/game-design/SOURCE_EVIDENCE.json')
    ck('Preserved design assessment matches original evidence',
       info(design)['sha256'] == historical_evidence['assessmentDocument']['sha256'])
    for p, prefix in [(start, ''), (direction, '../../../')]:
        raw = nav[p]
        pos = raw.index(b'\n') + 1
        notice = ('\n**Latest review checkpoint — 20 October 2026:** [Checkpoint 50]('
            + prefix + base + outcp.name + ') and [Queue 41]('
            + prefix + outq.relative_to(G).as_posix()
            + ') include eight prepared rank9 defense/form spells: 87 complete sources, eight placements, 26 unselected questions and 312 preservation checks. There are 249 grouped pending identities and 74 ungrouped. GPT is still reviewing the preparation-only Ready successor. Applied counts remain 525 reviewed / 323 pending / 249 standalone, with 39 accepted but unapplied. [Owner direction]('
            + prefix + base + ledger.name
            + ') governs the SNES-style Unity CRPG: direct exploration, tactical combat, companion resource management and ongoing AI engineering support. The older Unity evaluation now points to this direction. GitHub backup remains verified through checkpoint 48; checkpoints 49–50 are later local work.\n').encode()
        after[p] = raw[:pos] + notice + raw[pos:]
        ck('Original navigation retained ' + p.name, after[p].replace(notice, b'', 1) == raw)
    raw = nav[mapfile]
    pos = raw.index(b'</h1>') + len(b'</h1>')
    banner = ('<section class="sequence" aria-label="Latest defense and form preparation"><p><strong>Checkpoint 50: eight rank9 defense/form sources prepared.</strong> 87 complete sources, eight placements, 26 unselected decisions; 312 preservation checks. Queue 41: 249 grouped pending identities, 74 ungrouped. Owner direction remains the three-mode SNES-style Unity CRPG with ongoing AI engineering support. Preparation-only Ready review remains active. <a href="'
        + base + outcp.name + '">Current checkpoint</a> · <a href="'
        + base + ledger.name + '">Owner decisions</a></p></section>').encode()
    after[mapfile] = raw[:pos] + banner + raw[pos:]
    ck('All domain content retained', after[mapfile].replace(banner, b'', 1) == raw)
    raw = nav[design]
    pos = raw.index(b'\n') + 1
    notice = ('\n> **Current owner direction — 20 October 2026:** The later [GPT decision ledger](../audit/2026-10-08/full-game/'
        + ledger.name + ') governs: a video-game-only, SNES-style Unity CRPG combining direct-control exploration (running, jumping and mapped interactions), deep tactical combat, and crafting/research/companion resource assignments. AI provides continuing engineering and rules-review support; the owner retains design authority.\n>\n> The 17 October evaluation below is preserved history. Its party-command recommendation and statements that visual style/control direction are wholly undecided are superseded by that later direction. Exact camera, traversal, clock conversion, combat transition, cooperative details and first playable scope still require reconciliation. GPT’s shared C# simulation architecture is a proposal, not an implemented engine. [SOURCE_EVIDENCE.json](SOURCE_EVIDENCE.json) continues to describe the [unchanged original assessment](../audit/2026-10-08/full-game/navigation-before-rank9-defense-form-50/UNITY_DESIGN_EVALUATION.md). No gameplay rules are implemented by this notice.\n').encode()
    after[design] = raw[:pos] + notice + raw[pos:]
    ck('Original design assessment retained byte-for-byte', after[design].replace(notice, b'', 1) == raw)
    keep.mkdir()
    for p, data in nav.items():
        (keep / p.name).write_bytes(data)
    outq.write_bytes(encoded(q))
    for p, data in after.items():
        p.write_bytes(data)
    reconciliation.write_bytes(encoded({'id': 'GPT-DIRECTION-AND-UNITY-ASSESSMENT-RECONCILIATION-50',
        'recordedAtUtc': now, 'nativeObservations': [info(livep), info(unityp)],
        'existingDecisionLedger': info(ledger), 'newOwnerDecisionsFound': 0,
        'readyReviewStatus': 'Existing request still active; no successor received.',
        'designAssessmentBefore': info(keep / design.name), 'designAssessmentAfter': info(design),
        'historicalEvidenceUnchanged': info(G / 'docs/game-design/SOURCE_EVIDENCE.json'),
        'change': 'Added a current-direction notice to the historical Unity assessment, preserving every original byte and its original evidence.',
        'implementationApplied': False, 'sourceInformationDeleted': 0}))
    cp.update(id='ACTIVE-AUTHORING-RANK9-DEFENSE-FORM-50', recordedAtUtc=now,
        status='Eight rank9 defense/form identities prepared; current GPT direction rechecked and older Unity assessment reconciled by a preservation notice. Ready successor review remains active.',
        previousCheckpoint=info(previous), currentWorkQueue=info(outq), preparedGroupCount=39,
        groupedPendingIdentities=249, ungroupedPendingIdentities=74,
        rank9DefenseForm8SourceConference=info(pp), gptDirectionReconciliation=info(reconciliation),
        navigation=[info(p) for p in after], preservedNavigation=[info(keep / p.name) for p in nav],
        latestPreviouslyVerifiedGitHubBackup={'commit': push['commit'], 'throughCheckpoint': 48, 'receipt': info(pushp)},
        laterLocalWork='Death/recovery7 and defense/form8, queues 40–41, checkpoints 49–50, fresh native observations, the Unity assessment notice and post-push receipt are later local work.',
        lastUsageObservation={'usedPercent': 6, 'remainingPercent': 94, 'stopAtRemainingPercent': 20},
        previousGoalTurnClassification='progress: prepared defense/form8; recovered current GPT discussion and reconciled navigation without mechanic application.',
        nextAction='Retrieve the active preparation-only Ready successor and verify its exact return. Continue already-delivered Rank8Damage6/Rank7IdentityCasting5, then remaining source conferences and 74 ungrouped rank9 identities. Preserve the owner implementation reservation and stop at 20 percent remaining.')
    cp['activeGptReviewAtLastVerifiedObservation'].update(nativeConfirmation=info(livep),
        sent=True, completedResponseReceived=False)
    outcp.write_bytes(encoded(cp))
    for p, data in protected.items():
        ck('Protected authority unchanged ' + p.relative_to(G).as_posix(), p.read_bytes() == data)
    check.write_bytes(encoded({'recordedAtUtc': now, 'checkpoint': info(outcp), 'queue': info(outq),
        'checks': checks, 'checkCount': len(checks), 'failureCount': 0, 'newRuleAdoptions': 0,
        'sourceInformationDeleted': 0, 'runtimeTestsExecuted': 0,
        'scope': 'Queue source/history preservation, current GPT observations, navigation and design-assessment reconciliation; no semantic or runtime acceptance.'}))
    print(json.dumps({'checkpoint': info(outcp), 'queue': info(outq), 'check': info(check),
        'checks': len(checks), 'grouped': 249, 'ungrouped': 74}))


if __name__ == '__main__':
    main()
