"""Register six newly prepared source conferences without promoting any spell."""
from collections import Counter
from copy import deepcopy
from datetime import datetime, timezone
import ast, json, subprocess, sys
from apply_di7_ap_as_01 import G, R, A, info, encoded


def read(p): return json.loads(p.read_bytes())


def main():
    base = R/'data/director/spell_review'; oldq = base/'remaining_work_queue_17.json'; newq = base/'remaining_work_queue_18.json'
    oldcp = A/'ACTIVE_AUTHORING_CHECKPOINT_COPY_CLASSES_24.json'; cp = A/'ACTIVE_AUTHORING_CHECKPOINT_RANK8_DAMAGE_25.json'
    delta = A/'RANK8_DAMAGE_25_NAVIGATION_DELTA.json'; report = A/'RANK8_DAMAGE_25_CHECK.json'; keep = A/'navigation-before-rank8-damage-25'
    assert not any(p.exists() for p in [newq, cp, delta, report, keep])
    now = datetime.now(timezone.utc).isoformat(); checks = []
    def ck(n, v): checks.append({'check': n, 'passed': bool(v)}); assert v, n
    pp = A/'RANK8_DAMAGE_6_SOURCE_CONFERENCE_01_PREPARATION.json'; prep = read(pp); candidate = read(G/prep['candidate']['path'])
    for k in ['candidate', 'archive', 'manifest', 'check', 'request']: ck('Exact source conference '+k, info(G/prep[k]['path']) == prep[k])
    ids = [r['spellId'] for r in candidate['records']]
    q = deepcopy(read(oldq)); previous = deepcopy(q)
    group = {'group': 'rank8-damage6', 'phase': 'source-conference-prepared-unsent', 'identities': ids, 'identityCount': 6,
        'candidate': prep['candidate'], 'preparation': info(pp), 'archive': prep['archive'], 'adopted': False,
        'earlierCompleteProcedures': 0, 'newCurrentEncounters': 0, 'riskCounts': candidate['riskCounts']}
    q['groups'].append(group)
    for row in q['rows']:
        if row['id'] in ids:
            ck('Previously ungrouped '+row['id'], row['currentGroup'] is None)
            row['previousPhaseBeforeConference25'] = row['currentPhase']
            row.update(currentGroup=group['group'], currentPhase=group['phase'],
                nextAction='Confer with actual GPT on all20 exact questions and complete sources/counterparts. Resolve real type/range/duration, corpse consumption, exile and illusion forks before procedures/cases. Preparation is not adoption.')
    q['sourceBindings'].extend([info(oldq), info(pp), prep['candidate'], prep['archive'], prep['check']])
    q.update(id='REMAINING-WORK-QUEUE-18', recordedAtUtc=now, previousQueue=info(oldq),
        pendingDistribution=dict(Counter(r['currentPhase'] for r in q['rows'])),
        preparedOrActualReviewIdentityCount=148, originalSourceOrReceiptWorkCount=175)
    ck('323 identity/order preservation', [r['id'] for r in q['rows']] == [r['id'] for r in previous['rows']] and len(q['rows']) == 323)
    ck('20 disjoint groups148 identities', len(q['groups']) == 20 and sum(g['identityCount'] for g in q['groups']) == len({i for g in q['groups'] for i in g['identities']}) == 148)
    ck('175 ungrouped', sum(r['currentGroup'] is None for r in q['rows']) == 175)
    for before, after in zip(previous['rows'], q['rows']):
        ck('Original complete source/access/member '+before['id'], all(before[k] == after[k] for k in ['currentIndexEntryUnchanged', 'completeCurrentSourceAndAccess', 'previousAuthoringMapRowUnchanged', 'semanticAcceptanceClaimed']))
    for b in q['sourceBindings']: ck('Exact queue source '+b['path'], info(G/b['path']) == b)
    index = R/'data/public/spell_playtests/authored_review_index.json'; ib = info(index)
    ck('525 reviewed323 pending', read(index)['authoredCounts'] == {'reviewed': 525, 'pending': 323})
    start = G/'START_HERE.md'; guide = R/'docs/DEVELOPMENT_DIRECTION.md'; builder = R/'tools/build_review_map.py'
    ledger = R/'data/playtest/game_development_coverage.json'; mapfile = G/'REVIEW_MAP.html'; buildfile = A/'REVIEW_MAP_BUILD.json'
    raw = {p: p.read_bytes() for p in [start, guide, builder, ledger, mapfile, buildfile]}; edits = {}
    added = '**Rank-eight damage and interaction sources:** The [six-spell source conference](docs/audit/2026-10-08/full-game/RANK8_DAMAGE_6_SOURCE_CONFERENCE_01_PREPARATION.json) preserves51 full sources, six placements,12 accepted counterpart cards/casebooks and20 unselected decisions.240 source/authority/preservation checks pass. Deep Crust Spike, Molecular Destabilization, Soul Pyre, Incendiary Cloud, Dimensional Break and Illusory Wall of Doom remain pending, with four tierB/two tierC records. Their mixed damage, corpse consumption, exile, perception and duration conflicts await actual GPT. No new procedure, operational case or approval is claimed.'
    for p in [start, guide]:
        text = raw[p].decode('utf8').replace(oldcp.name, cp.name).replace('[checkpoint24]', '[checkpoint25]').replace('latest observation was 47% remaining', 'latest observation was 46% remaining')
        parts = text.split('\n\n'); prefix = '**Remaining spell work:**'
        ck('One remaining-work paragraph '+p.name, sum(x.startswith(prefix) for x in parts) == 1)
        for n, s in enumerate(parts):
            if s.startswith(prefix):
                parts[n] = s.replace('Queue17', 'Queue18').replace('remaining_work_queue_17.json', 'remaining_work_queue_18.json').replace('142 in nineteen active/prepared groups and 181', '148 in twenty active/prepared groups and 175')+'\n\n'+(added if p == start else added.replace('(docs/audit/', '(../../../docs/audit/'))
            elif s.startswith('**GitHub preservation:**'):
                parts[n] = s.replace('The new class-copy integration and checkpoint24 are local', 'The new class-copy integration, rank-eight damage conference and checkpoint25 are local')
        edits[p] = '\n\n'.join(parts)
    cov = read(ledger); before_cov = deepcopy(cov)
    cov.setdefault('activeOrdinarySpellReviewHistory', []).append(deepcopy(cov['activeOrdinarySpellReview']))
    code = raw[builder].decode('utf8'); tail = ' + read(A / "COPY_CLASSES_24_NAVIGATION_DELTA.json")["changes"]\n'
    ck('One previous navigation tail', code.count(tail) == 1)
    code = code.replace(tail, tail.rstrip('\n')+' + read(A / "RANK8_DAMAGE_25_NAVIGATION_DELTA.json")["changes"]\n')
    featured = [('Current checkpoint25 — rank-eight source decisions', cp.relative_to(G).as_posix()), ('Current323 pending identities — queue18', newq.relative_to(G).as_posix())]
    code = code.replace('    featured = [\n', '    featured = [\n'+''.join('        '+repr(x)+',\n' for x in featured), 1).replace('Current checkpoint24 — Shaman/Mirrorsage copy integration', 'Checkpoint24 history — Shaman/Mirrorsage copy integration').replace('Current323 pending identities — queue17', 'Queue17 history — before rank-eight damage preparation')
    code = code.replace('    pending = [\n', '    pending = [\n        '+repr(('Rank8 damage6 —20 questions,4B/2C, UNSENT', pp.name))+',\n', 1)
    scope = 'Video game only.525 reviewed/323 pending;249 standalone;173 scoped interfaces. Part4 at conversation-length limit; Part5 creation awaiting owner authorization. No Illusion final. Queue18:148 identities in20 active/prepared groups,175 ungrouped. Rank8 damage6 preserves51 sources/6 placements/20 unselected questions/240 checks,4B2C; no new procedures/cases. Agreed copy integrations retain136+115+205 scoped checks, all progress UNSENT. Full Ready/class Echo/runtime and other limits remain open. All75 domain gates unchanged. Last verified push e2fb430 covers checkpoint23; class-copy/rank8/checkpoint25 local. Latest allowance46percentremaining; continue to review completion or20percent.'
    nodes = [v for n in ast.walk(ast.parse(code)) if isinstance(n, ast.Dict) for k, v in zip(n.keys, n.values) if isinstance(k, ast.Constant) and k.value == 'notebookReview']
    ck('One map status', len(nodes) == 1); code = code.replace(ast.get_source_segment(code, nodes[0]), repr(scope), 1); compile(code, str(builder), 'exec')
    saved = []
    for p, b in raw.items():
        dst = keep/p.relative_to(G); dst.parent.mkdir(parents=True, exist_ok=True); dst.write_bytes(b)
        saved.append({'source': info(p), 'preservedCopy': info(dst)})
    (keep/'PRESERVATION_MANIFEST.json').write_bytes(encoded(saved)); newq.write_bytes(encoded(q))
    cov['activeOrdinarySpellReview'].update(recordedAtUtc=now, currentQueue=info(newq), rank8Damage6SourceConference=info(pp))
    ck('All75 full domain rows unchanged', cov['aspects'] == before_cov['aspects'] and len(cov['aspects']) == 75)
    ledger.write_bytes(encoded(cov))
    for p, t in edits.items(): p.write_text(t, encoding='utf8', newline='\n')
    builder.write_text(code, encoding='utf8', newline='\n')
    changes = [{'before': next({**s['source'], 'preservedCopy': s['preservedCopy']['path']} for s in saved if s['source']['path'] == p.relative_to(G).as_posix()), 'after': info(p)} for p in [start, guide, ledger, builder]]
    delta.write_bytes(encoded({'recordedAtUtc': now, 'changes': changes, 'newRuleAdoptionsByNavigation': 0, 'all75DomainGatesUnchanged': True, 'sourceInformationDeleted': 0}))
    checkpoint = deepcopy(read(oldcp))
    checkpoint.update(id='ACTIVE-AUTHORING-RANK8-DAMAGE-25', recordedAtUtc=now, status=scope, previousCheckpoint=info(oldcp),
        currentWorkQueue=info(newq), remainingPreparedGroups=q['groups'], rank8Damage6SourceConference=info(pp), lastUsageObservation={'usedPercent': 54, 'remainingPercent': 46, 'windowMinutes': 10080, 'secondary': 'unavailable'},
        coverageLedger=info(ledger), navigationDelta=info(delta), preservedNavigation=info(keep/'PRESERVATION_MANIFEST.json'))
    checkpoint['laterLocalWork'].append('Rank8 damage6 full source conference,20 questions/51 sources/240 preservation checks; queue18/checkpoint25.')
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
