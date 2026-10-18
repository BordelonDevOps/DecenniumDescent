"""Register five source conferences while preserving all spell/domain gates."""
from collections import Counter
from copy import deepcopy
from datetime import datetime, timezone
import ast, json, subprocess, sys
from apply_di7_ap_as_01 import G, R, A, info, encoded


def read(p): return json.loads(p.read_bytes())


def main():
    base = R/'data/director/spell_review'; oldq = base/'remaining_work_queue_19.json'; newq = base/'remaining_work_queue_20.json'
    oldcp = A/'ACTIVE_AUTHORING_CHECKPOINT_RANK7_IDENTITY_CASTING_26.json'; cp = A/'ACTIVE_AUTHORING_CHECKPOINT_RANK7_PERCEPTION_27.json'
    delta = A/'RANK7_PERCEPTION_27_NAVIGATION_DELTA.json'; report = A/'RANK7_PERCEPTION_27_CHECK.json'
    keep = A/'navigation-before-rank7-perception-27'
    assert not any(p.exists() for p in [newq, cp, delta, report, keep])
    now = datetime.now(timezone.utc).isoformat(); checks = []
    def ck(n, v): checks.append({'check': n, 'passed': bool(v)}); assert v, n
    pp = A/'RANK7_PERCEPTION_5_SOURCE_CONFERENCE_01_PREPARATION.json'; prep = read(pp); candidate = read(G/prep['candidate']['path'])
    for k in ['candidate', 'archive', 'manifest', 'check', 'request']: ck('Exact conference '+k, info(G/prep[k]['path']) == prep[k])
    ids = [r['spellId'] for r in candidate['records']]
    q = deepcopy(read(oldq)); previous = deepcopy(q)
    group = {'group': 'rank7-perception5', 'phase': 'source-conference-prepared-unsent', 'identities': ids, 'identityCount': 5,
        'candidate': prep['candidate'], 'preparation': info(pp), 'archive': prep['archive'], 'adopted': False,
        'earlierCompleteProcedures': 0, 'newCurrentEncounters': 0, 'riskCounts': candidate['riskCounts']}
    q['groups'].append(group)
    for row in q['rows']:
        if row['id'] in ids:
            ck('Previously ungrouped '+row['id'], row['currentGroup'] is None)
            row['previousPhaseBeforeConference27'] = row['currentPhase']
            row.update(currentGroup=group['group'], currentPhase=group['phase'],
                nextAction='Confer with actual GPT on all21 unselected source decisions and complete evidence. Resolve tactile terrain, six image scripts, complete unnoticeability, Speed0 and compelled historical repetition before procedures/cases. Preparation is not adoption.')
    q['sourceBindings'].extend([info(oldq), info(pp), prep['candidate'], prep['archive'], prep['check']])
    q.update(id='REMAINING-WORK-QUEUE-20', recordedAtUtc=now, previousQueue=info(oldq),
        pendingDistribution=dict(Counter(r['currentPhase'] for r in q['rows'])),
        preparedOrActualReviewIdentityCount=158, originalSourceOrReceiptWorkCount=165)
    ck('323 identities/order retained', [r['id'] for r in q['rows']] == [r['id'] for r in previous['rows']] and len(q['rows']) == 323)
    ck('22 disjoint groups158 identities', len(q['groups']) == 22 and sum(g['identityCount'] for g in q['groups']) == len({i for g in q['groups'] for i in g['identities']}) == 158)
    ck('165 ungrouped', sum(r['currentGroup'] is None for r in q['rows']) == 165)
    ck('All previous groups unchanged', q['groups'][:-1] == previous['groups'])
    for before, after in zip(previous['rows'], q['rows']):
        ck('Original full source/access/member '+before['id'], all(before[k] == after[k] for k in ['currentIndexEntryUnchanged', 'completeCurrentSourceAndAccess', 'previousAuthoringMapRowUnchanged', 'semanticAcceptanceClaimed']))
    for b in q['sourceBindings']: ck('Exact queue source '+b['path'], info(G/b['path']) == b)
    index = R/'data/public/spell_playtests/authored_review_index.json'; ib = info(index)
    ck('525 reviewed323 pending', read(index)['authoredCounts'] == {'reviewed': 525, 'pending': 323})
    pushp = G/'docs/audit/2026-10-18/github-snapshot-classes-rank8/PUSH_RECEIPT.json'; push = read(pushp)
    ck('Verified checkpoint25 push receipt', push['commit'] == push['remoteMain'] == '7142a4f7e9c6088dbd1c92bd2ea3bde3891f42a9' and push['expectedBlobsVerified'] == 25264 and push['trackedEntriesDeleted'] == 0)
    start = G/'START_HERE.md'; guide = R/'docs/DEVELOPMENT_DIRECTION.md'; builder = R/'tools/build_review_map.py'
    ledger = R/'data/playtest/game_development_coverage.json'; mapfile = G/'REVIEW_MAP.html'; buildfile = A/'REVIEW_MAP_BUILD.json'
    raw = {p: p.read_bytes() for p in [start, guide, builder, ledger, mapfile, buildfile]}; edits = {}
    added = '**Rank-seven perception and control sources:** The [five-spell source conference](docs/audit/2026-10-08/full-game/RANK7_PERCEPTION_5_SOURCE_CONFERENCE_01_PREPARATION.json) preserves49 full sources, five placements,13 reviewed spell counterparts and21 unselected decisions.236 source/access/authority/preservation checks pass. Inescapable Labyrinth and Mirage Legion are individually tierB; Mindtrap Echo, Mirage Arcane and Perfect Veil are tierC. Tactile terrain, six harmless spell-performing images, complete unnoticeability, Speed0 and historical action repetition retain their original promises. These procedures and cases still await actual GPT; pending Illusion14/Control15/terrain/Project Image proposals supply no new authority.'
    github = '**GitHub preservation:** Commit `7142a4f7e9c6088dbd1c92bd2ea3bde3891f42a9` contains work through checkpoint25, including class-copy integration and the rank-eight damage conference.25,264 expected blobs were verified, with no prior tracked files deleted. See the [verified receipt](docs/audit/2026-10-18/github-snapshot-classes-rank8/PUSH_RECEIPT.json). Rank-seven identity/casting and perception source conferences, checkpoints26–27 and handoff03 remain local pending a later snapshot.'
    for p in [start, guide]:
        text = raw[p].decode('utf8').replace(oldcp.name, cp.name).replace('[checkpoint26]', '[checkpoint27]').replace('latest observation was 45% remaining', 'latest observation was 44% remaining')
        parts = text.split('\n\n')
        for prefix in ['**Remaining spell work:**', '**GitHub preservation:**']:
            ck('One navigation paragraph '+prefix+p.name, sum(x.startswith(prefix) for x in parts) == 1)
        for n, s in enumerate(parts):
            if s.startswith('**Remaining spell work:**'):
                parts[n] = s.replace('Queue19', 'Queue20').replace('remaining_work_queue_19.json', 'remaining_work_queue_20.json').replace('153 in twenty-one active/prepared groups and 170', '158 in twenty-two active/prepared groups and 165')+'\n\n'+(added if p == start else added.replace('(docs/audit/', '(../../../docs/audit/'))
            elif s.startswith('**GitHub preservation:**'):
                parts[n] = github if p == start else github.replace('(docs/audit/', '(../../../docs/audit/')
            elif s.startswith('**GPT continuation required:**'):
                link = 'docs/audit/2026-10-08/full-game/GPT_CONTINUATION_05_HANDOFF_03_PREPARATION.json'
                if p == guide: link = '../../../'+link
                parts[n] = '**GPT continuation required:** Part4 reached its explicit conversation-length limit; no Illusion14 final exists. The [current prepared handoff03]('+link+') contains56 current-context source files and five full nested progress/source archives through checkpoint26. Its initial Illusion14 and current-acceptance archives remain separate full attachments. Creating Part5 still awaits the owner response; no delivery or approval is inferred. The later perception5 packet and queue20/checkpoint27 supplement that frozen handoff when relevant; handoff03 does not claim to include them.'
        edits[p] = '\n\n'.join(parts).replace('Actual joint work continues in Part 4; EPI-08–14 is applied, while the consumable and environment packets await their own later review.', 'Part4 is now at its conversation-length limit; EPI-08–14 is applied, while consumable and environment packets await review in the authorized continuation.')
    cov = read(ledger); before_cov = deepcopy(cov)
    cov.setdefault('activeOrdinarySpellReviewHistory', []).append(deepcopy(cov['activeOrdinarySpellReview']))
    code = raw[builder].decode('utf8'); tail = ' + read(A / "RANK7_IDENTITY_CASTING_26_NAVIGATION_DELTA.json")["changes"]\n'
    ck('One previous navigation tail', code.count(tail) == 1)
    code = code.replace(tail, tail.rstrip('\n')+' + read(A / "RANK7_PERCEPTION_27_NAVIGATION_DELTA.json")["changes"]\n')
    featured = [('Current checkpoint27 — rank-seven perception sources', cp.relative_to(G).as_posix()), ('Current323 pending identities — queue20', newq.relative_to(G).as_posix())]
    code = code.replace('    featured = [\n', '    featured = [\n'+''.join('        '+repr(x)+',\n' for x in featured), 1).replace('Current checkpoint26 — rank-seven identity/casting sources', 'Checkpoint26 history — rank-seven identity/casting sources').replace('Current323 pending identities — queue19', 'Queue19 history — before perception source preparation')
    code = code.replace('    pending = [\n', '    pending = [\n        '+repr(('Rank7 perception5 —21 questions,2B/3C, UNSENT', pp.name))+',\n', 1)
    scope = 'Video game only.525 reviewed/323 pending;249 standalone;173 scoped interfaces. Part4 full; Part5 creation awaiting owner authorization; no Illusion final. Queue20:158 identities in22 active/prepared groups,165 ungrouped. Rank7 perception5 preserves49 sources/5 placements/21 unselected questions/236 checks,2B3C; no new procedures/cases. Other packets and copy integrations remain UNSENT. Handoff03 is current through checkpoint26 and includes five full nested archives; later perception5/queue20 supplement it. All75 domain gates unchanged. Verified push7142a4f through checkpoint25; later source packets/handoff/checkpoints local. Allowance44percentremaining; continue to review completion or20percent.'
    nodes = [v for n in ast.walk(ast.parse(code)) if isinstance(n, ast.Dict) for k, v in zip(n.keys, n.values) if isinstance(k, ast.Constant) and k.value == 'notebookReview']
    ck('One map status', len(nodes) == 1); code = code.replace(ast.get_source_segment(code, nodes[0]), repr(scope), 1); compile(code, str(builder), 'exec')
    saved = []
    for p, b in raw.items():
        dst = keep/p.relative_to(G); dst.parent.mkdir(parents=True, exist_ok=True); dst.write_bytes(b)
        ck('Exact prior navigation preserved '+p.name, dst.read_bytes() == b)
        saved.append({'source': info(p), 'preservedCopy': info(dst)})
    (keep/'PRESERVATION_MANIFEST.json').write_bytes(encoded(saved)); newq.write_bytes(encoded(q))
    cov['activeOrdinarySpellReview'].update(recordedAtUtc=now, currentQueue=info(newq), rank7Perception5SourceConference=info(pp))
    ck('All75 full domain rows unchanged', cov['aspects'] == before_cov['aspects'] and len(cov['aspects']) == 75)
    ledger.write_bytes(encoded(cov))
    for p, t in edits.items(): p.write_text(t, encoding='utf8', newline='\n')
    builder.write_text(code, encoding='utf8', newline='\n')
    changes = [{'before': next({**s['source'], 'preservedCopy': s['preservedCopy']['path']} for s in saved if s['source']['path'] == p.relative_to(G).as_posix()), 'after': info(p)} for p in [start, guide, ledger, builder]]
    delta.write_bytes(encoded({'recordedAtUtc': now, 'changes': changes, 'newRuleAdoptionsByNavigation': 0, 'all75DomainGatesUnchanged': True, 'sourceInformationDeleted': 0}))
    checkpoint = deepcopy(read(oldcp))
    checkpoint['previousPreparedContinuationAt26'] = deepcopy(checkpoint['latestPreparedContinuation'])
    checkpoint.update(id='ACTIVE-AUTHORING-RANK7-PERCEPTION-27', recordedAtUtc=now, status=scope, previousCheckpoint=info(oldcp),
        currentWorkQueue=info(newq), remainingPreparedGroups=q['groups'], rank7Perception5SourceConference=info(pp),
        lastUsageObservation={'usedPercent': 56, 'remainingPercent': 44, 'windowMinutes': 10080, 'secondary': 'unavailable'},
        latestVerifiedGitHubBackup={'commit': push['commit'], 'receipt': info(pushp), 'coverage': 'Work through checkpoint25;25264 expected blobs verified;0 prior tracked files deleted.'},
        verifiedGitHubPush=info(pushp),
        laterLocalWork=checkpoint['laterLocalWork']+['Handoff03:56 current-context sources and5 full nested archives, prepared UNSENT.', 'Rank7 perception5 source conference,21 questions/49 sources/236 checks; queue20/checkpoint27.'],
        latestPreparedContinuation=info(A/'GPT_CONTINUATION_05_HANDOFF_03_PREPARATION.json'),
        coverageLedger=info(ledger), navigationDelta=info(delta), preservedNavigation=info(keep/'PRESERVATION_MANIFEST.json'),
        continuationCurrencyQualification='Handoff03 is current through checkpoint26; perception5/queue20/checkpoint27 are later supplemental context. Preserve the frozen handoff and send full cohort packets when actually reviewing them.')
    cp.write_bytes(encoded(checkpoint))
    run = subprocess.run([sys.executable, '-X', 'utf8', str(builder)], capture_output=True, text=True, encoding='utf8')
    ck('Review map build '+run.stderr[-1200:], run.returncode == 0)
    build = read(buildfile); ck('No missing links', not build['missingLinks']); ck('Authored index unchanged', info(index) == ib)
    checkpoint['navigation'] = {'map': info(mapfile), 'build': info(buildfile), 'existingDistinctLinks': build['existingDistinctLinks'], 'missingLinks': []}
    cp.write_bytes(encoded(checkpoint))
    report.write_bytes(encoded({'checkpoint': info(cp), 'queue': info(newq), 'checks': checks, 'checkCount': len(checks),
        'failures': 0, 'links': build['existingDistinctLinks'], 'indexUnchanged': ib, 'all75DomainGatesUnchanged': True,
        'newRuleAdoptions': 0, 'runtimeTestsExecuted': 0, 'sourceInformationDeleted': 0}))
    print(json.dumps({'checkpoint': info(cp), 'queue': info(newq), 'checks': len(checks), 'links': build['existingDistinctLinks'], 'failures': 0}))


if __name__ == '__main__': main()
