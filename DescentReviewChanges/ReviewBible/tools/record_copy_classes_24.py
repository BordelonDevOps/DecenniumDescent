"""Preserve old navigation, expose class integrations, keep all review gates."""
from copy import deepcopy
from datetime import datetime, timezone
import ast, json, subprocess, sys
from apply_di7_ap_as_01 import G, R, A, info, encoded


def read(p): return json.loads(p.read_bytes())


def main():
    oldcp = A/'ACTIVE_AUTHORING_CHECKPOINT_COPY_PAYLOADS_23.json'
    cp = A/'ACTIVE_AUTHORING_CHECKPOINT_COPY_CLASSES_24.json'
    delta = A/'COPY_CLASSES_24_NAVIGATION_DELTA.json'
    report = A/'COPY_CLASSES_24_CHECK.json'; keep = A/'navigation-before-copy-classes-24'
    assert not any(p.exists() for p in [cp, delta, report, keep])
    checks = []; now = datetime.now(timezone.utc).isoformat()
    def ck(n, v): checks.append({'check': n, 'passed': bool(v)}); assert v, n
    prep = A/'FEAT335_COPY_CLASSES_01_PREPARATION.json'; pr = read(prep)
    result = read(A/'FEAT335_COPY_CLASSES_01_CHECK.json')
    ck('205 bounded class checks; no broad approval', result['checks'] == 205 and not result['failures'] and not result['runtimeApproved'] and not result['wholeGameComplete'])
    for k in ['archive', 'progress', 'request', 'manifest']: ck('Exact new evidence '+k, info(G/pr[k]['path']) == pr[k])
    queue = R/'data/director/spell_review/remaining_work_queue_17.json'; qb = info(queue)
    index = R/'data/public/spell_playtests/authored_review_index.json'; ib = info(index)
    ck('525 reviewed323 pending unchanged', read(index)['authoredCounts'] == {'reviewed': 525, 'pending': 323})
    start = G/'START_HERE.md'; guide = R/'docs/DEVELOPMENT_DIRECTION.md'; builder = R/'tools/build_review_map.py'
    ledger = R/'data/playtest/game_development_coverage.json'; mapfile = G/'REVIEW_MAP.html'; buildfile = A/'REVIEW_MAP_BUILD.json'
    raw = {p: p.read_bytes() for p in [start, guide, builder, ledger, mapfile, buildfile]}; edits = {}
    added = '**Shaman and Mirrorsage copy integration:** [205 checks across22 conditional histories](docs/audit/2026-10-08/full-game/FEAT335_COPY_CLASSES_01_CHECK.json) exercise actual native class abilities/rank limits, paid feat choices and all7 existing copied payloads. The Shaman copy shares a paid totem’s resource/concentration state without consuming its ordinary vent. Mirrorsage uses the existing shared Echo allowance; class and feat release boundaries block each other. Bloodcaller cannot substitute retained RP for lost ordinary spellcasting. The [full66-source update](docs/audit/2026-10-08/full-game/FEAT335_COPY_CLASSES_01_PREPARATION.json) is prepared UNSENT to GPT. Full class capture/Echo casting, Ready, world/runtime integration and other listed limits remain open.'
    for p in [start, guide]:
        text = raw[p].decode('utf8').replace(oldcp.name, cp.name).replace('[checkpoint23]', '[checkpoint24]').replace('latest observation was 49% remaining', 'latest observation was 47% remaining')
        parts = text.split('\n\n'); prefix = '**Copied recipient effects integrated:**'
        ck('One payload paragraph '+p.name, sum(s.startswith(prefix) for s in parts) == 1)
        for i, s in enumerate(parts):
            if s.startswith(prefix):
                s = s.replace('Ready and other class providers remain open', 'Ready and wider provider integrations remain open')
                parts[i] = s+'\n\n'+(added if p == start else added.replace('(docs/audit/', '(../../../docs/audit/'))
            elif s.startswith('**Agreed feat-copy release integration:**'):
                parts[i] = s.replace('keep actual Shaman/Mirrorsage providers, recipient effects, full Ready transactions and live runtime open', 'record the earlier commitment-only boundary; the later payload/class integrations below extend that evidence, while full Ready transactions and live runtime remain open')
            elif s.startswith('**GitHub preservation:**'):
                receipt = 'docs/audit/2026-10-18/github-snapshot-copy-integration/PUSH_RECEIPT.json'
                parts[i] = '**GitHub preservation:** Commit `e2fb43028e21f74c049aab8926bc2f3ed1966a03` contains the prior work through checkpoint23, with25,103 expected blobs verified and no prior tracked files deleted. See the [verified receipt]('+ (receipt if p == start else '../../../'+receipt)+'). The new class-copy integration and checkpoint24 are local pending the next verified snapshot.'
        edits[p] = '\n\n'.join(parts)
    cov = read(ledger); before = deepcopy(cov)
    cov['boundedFeatCopyClassProgress'] = pr['progress']
    ck('All75 full aspect rows unchanged', cov['aspects'] == before['aspects'] and len(cov['aspects']) == 75)
    code = raw[builder].decode('utf8')
    tail = ' + read(A / "COPY_PAYLOADS_23_NAVIGATION_DELTA.json")["changes"]\n'
    ck('One previous tail', code.count(tail) == 1)
    code = code.replace(tail, tail.rstrip('\n')+' + read(A / "COPY_CLASSES_24_NAVIGATION_DELTA.json")["changes"]\n')
    featured = [('Current checkpoint24 — Shaman/Mirrorsage copy integration', cp.relative_to(G).as_posix()),
                ('Class copy integration —205 bounded checks, full runtime open', pr['progress']['path'])]
    code = code.replace('    featured = [\n', '    featured = [\n'+''.join('        '+repr(x)+',\n' for x in featured), 1).replace('Current checkpoint23 — copied recipient effects', 'Checkpoint23 history — copied recipient effects')
    scope = 'Video game only.525 reviewed/323 pending;249 standalone;173 scoped interfaces. Part4 reached its conversation-length limit; Part5 creation remains pending owner authorization. No Illusion final. Queue17 unchanged:142 identities/19 groups,181 ungrouped. Copy integrations:136 commitment checks,115 recipient checks and205 class checks. Actual Shaman totem/ordinary vent shares resource and concentration; Mirrorsage uses its real shared Echo allowance. Class capture/Echo casting, full Ready, world/runtime and stated broader limits remain open. Complete progress archives UNSENT to GPT. No new rule or75-domain gate promotion. Last verified push e2fb430 includes checkpoint23; new class work/checkpoint24 local. Latest allowance47percentremaining; stop at review completion or20percent.'
    nodes = [v for n in ast.walk(ast.parse(code)) if isinstance(n, ast.Dict) for k, v in zip(n.keys, n.values) if isinstance(k, ast.Constant) and k.value == 'notebookReview']
    ck('One map status', len(nodes) == 1)
    code = code.replace(ast.get_source_segment(code, nodes[0]), repr(scope), 1); compile(code, str(builder), 'exec')
    saved = []
    for p, b in raw.items():
        dst = keep/p.relative_to(G); dst.parent.mkdir(parents=True, exist_ok=True); dst.write_bytes(b)
        saved.append({'source': info(p), 'preservedCopy': info(dst)})
    (keep/'PRESERVATION_MANIFEST.json').write_bytes(encoded(saved))
    ledger.write_bytes(encoded(cov))
    for p, t in edits.items(): p.write_text(t, encoding='utf8', newline='\n')
    builder.write_text(code, encoding='utf8', newline='\n')
    changes = [{'before': next({**s['source'], 'preservedCopy': s['preservedCopy']['path']} for s in saved if s['source']['path'] == p.relative_to(G).as_posix()), 'after': info(p)} for p in [start, guide, ledger, builder]]
    delta.write_bytes(encoded({'recordedAtUtc': now, 'changes': changes, 'newRuleAdoptionsByNavigation': 0, 'all75DomainGatesUnchanged': True, 'sourceInformationDeleted': 0}))
    push = G/'docs/audit/2026-10-18/github-snapshot-copy-integration/PUSH_RECEIPT.json'
    checkpoint = deepcopy(read(oldcp))
    checkpoint.update(id='ACTIVE-AUTHORING-COPY-CLASSES-24', recordedAtUtc=now, status=scope, previousCheckpoint=info(oldcp),
        boundedFeatCopyClasses=info(prep), coverageLedger=info(ledger), navigationDelta=info(delta),
        preservedNavigation=info(keep/'PRESERVATION_MANIFEST.json'), verifiedGitHubPush=info(push),
        latestVerifiedGitHubBackup={'commit': 'e2fb43028e21f74c049aab8926bc2f3ed1966a03', 'receipt': info(push), 'coverage': 'Prior work through checkpoint23;25103 expected blobs verified;0 prior tracked files deleted.'},
        laterLocalWork=['Class-copy provider/resource/lifecycle integration,205 checks/22 histories, full66-source GPT update and checkpoint24.'],
        lastUsageObservation={'usedPercent': 53, 'remainingPercent': 47, 'windowMinutes': 10080, 'secondary': 'unavailable'})
    cp.write_bytes(encoded(checkpoint))
    run = subprocess.run([sys.executable, '-X', 'utf8', str(builder)], capture_output=True, text=True, encoding='utf8')
    ck('Map build '+run.stderr[-1000:], run.returncode == 0)
    build = read(buildfile); ck('No missing links', not build['missingLinks'])
    ck('Queue17 and authored index unchanged', info(queue) == qb and info(index) == ib)
    checkpoint['navigation'] = {'map': info(mapfile), 'build': info(buildfile), 'existingDistinctLinks': build['existingDistinctLinks'], 'missingLinks': []}
    cp.write_bytes(encoded(checkpoint))
    report.write_bytes(encoded({'checkpoint': info(cp), 'checks': checks, 'checkCount': len(checks), 'failures': 0,
        'links': build['existingDistinctLinks'], 'queueUnchanged': qb, 'indexUnchanged': ib,
        'all75DomainGatesUnchanged': True, 'newRuleAdoptions': 0, 'sourceInformationDeleted': 0}))
    print(json.dumps({'checkpoint': info(cp), 'checks': len(checks), 'links': build['existingDistinctLinks'], 'failures': 0}))


if __name__ == '__main__': main()
