"""Read-only packaging inventory; does not certify a player export or lore."""
from collections import deque
from datetime import datetime, timezone
import json
from pathlib import Path
import re
from apply_di7_ap_as_01 import G, R, A, info, encoded


def inventory(directory):
    return [info(p) for p in sorted(directory.rglob('*')) if p.is_file()]


def source_graph(root):
    entry = root / 'src/app/page.tsx'
    pending = deque([entry]); visited = {}; edges = []; unresolved = []
    # Static import/export-from and literal dynamic import/require only. This
    # records source reachability, not bundler output, execution or data secrecy.
    patterns = [re.compile(r'''(?:import|export)\s+[^;]*?\bfrom\s*['"]([^'"]+)['"]'''),
                re.compile(r'''\bimport\s*['"]([^'"]+)['"]'''),
                re.compile(r'''\b(?:import|require)\s*\(\s*['"]([^'"]+)['"]\s*\)''')]
    while pending:
        p = pending.popleft()
        if p in visited: continue
        visited[p] = info(p)
        if p.suffix not in {'.ts', '.tsx', '.js', '.jsx', '.mjs', '.cjs'}: continue
        text = p.read_text(encoding='utf-8-sig')
        hits = sorted({(m.start(), m.group(1)) for pattern in patterns for m in pattern.finditer(text)})
        for offset, specifier in hits:
            if specifier.startswith('@/'):
                target = root / 'src' / specifier[2:]
            elif specifier.startswith('.'):
                target = p.parent / specifier
            else: continue
            choices = [target] + [Path(str(target) + ext) for ext in ['.ts', '.tsx', '.js', '.jsx', '.mjs', '.json']]
            choices += [target / ('index' + ext) for ext in ['.ts', '.tsx', '.js', '.jsx', '.json']]
            matches = [q.resolve() for q in choices if q.is_file()]
            matches = list(dict.fromkeys(matches))
            row = {'importer': p.relative_to(G).as_posix(), 'line': text[:offset].count('\n') + 1,
                   'specifier': specifier}
            if len(matches) != 1:
                unresolved.append({**row, 'candidateMatches': [str(q) for q in matches]}); continue
            q = matches[0]
            assert q.is_relative_to(G.resolve())
            edges.append({**row, 'target': q.relative_to(G).as_posix()}); pending.append(q)
    data_files = [b for p, b in visited.items() if p.suffix == '.json' or 'data' in p.relative_to(root).parts]
    return {'entry': info(entry), 'entryUsesClientDirective': '"use client"' in entry.read_text(encoding='utf-8-sig').splitlines()[0],
            'bindings': list(visited.values()), 'localImportEdges': edges, 'unresolvedLocalImports': unresolved,
            'sourceReachableData': data_files, 'compiledBundleInspected': False,
            'scope': 'Literal local source imports only. External packages, computed paths, tree shaking, network endpoints and actual UI permissions are not certified. Lore payloads are hashed only, not reviewed.'}


def main():
    output = A / 'PLAYER_DIRECTOR_PACKAGING_INVENTORY_01.json'
    assert not output.exists()
    public = inventory(R / 'data/public'); director = inventory(R / 'data/director')
    assert set(x['path'] for x in public).isdisjoint(x['path'] for x in director)
    flags = []
    for binding in public:
        p = G / binding['path']
        if p.suffix != '.json': continue
        d = json.loads(p.read_bytes())
        if not isinstance(d, dict): continue
        keys = ['schemaVersion', 'status', 'selectionEnabled', 'runtimeImplemented',
                'humanBalanceApproved', 'wholeGameFlowApproved', 'exactReviewReceived']
        flags.append({'file': binding, 'rootDeclarations': {k:d[k] for k in keys if k in d},
                      'missingDeclarationIsNotApproval': True})
    graphs = {'recoveredMain': source_graph(G), 'reviewCandidate': source_graph(R)}
    source_files = [G / 'START_HERE.md', R / 'REPOSITORY_GUIDE.md', R / 'package.json',
                    R / 'next.config.js', G / 'package.json', G / 'next.config.js', Path(__file__)]
    catalog = json.loads((R / 'data/public/spell_playtests/catalog.json').read_bytes())
    review = json.loads((R / 'data/public/spell_playtests/authored_review_index.json').read_bytes())
    legacy_reviewed = sum(x['status'] == 'operational-playtest-draft' for x in catalog['spells'])
    legacy_pending = sum(x['status'] == 'blocked-pending-operational-review' for x in catalog['spells'])
    assert legacy_reviewed == 276 and legacy_pending == 572 and len(catalog['spells']) == 848
    report = {'id': 'PLAYER-DIRECTOR-PACKAGING-INVENTORY-01', 'recordedAtUtc': datetime.now(timezone.utc).isoformat(),
        'status': 'source-inventory-complete-player-release-gate-open',
        'scope': 'Current file boundaries, public root declarations and literal companion entrypoint imports. No content doctrine/cosmology review, secret-free export or full runtime certification.',
        'publicDataFiles': public, 'directorDataFiles': director, 'publicRootDeclarations': flags,
        'counts': {'publicDataFiles': len(public), 'directorDataFiles': len(director),
                   'legacyOperationalSpells': legacy_reviewed, 'legacyPendingSpells': legacy_pending},
        'authoredReviewIndexCounts': review['authoredCounts'],
        'companionSourceGraphs': graphs, 'sourceBindings': [info(p) for p in source_files],
        'findings': [
            {'id': 'PKG-01', 'finding': 'A data/public path is an audience label, not an operational approval gate. Current exact candidates carry selection/runtime/review restrictions. A blanket public-directory copy would also ship pending ordinary records.',
             'needed': 'Final reviewed manifest must distinguish authored approved procedures, candidate-only content, explicit blocked records and post-push receipts; preserve all original data separately.'},
            {'id': 'PKG-02', 'finding': 'The legacy ordinary catalog alone contains276 operational procedures and572 blocked records. The separate authored index carries complete standalone representations as well. A catalog-only export would omit reviewed standalone procedures or misstate pending totals.',
             'needed': 'Use the authored index and its complete versioned representations when assembling the player spell catalog. Preserve source-specific modes and nulls; do not flatten to a lossy legacy adapter.'},
            {'id': 'PKG-03', 'finding': 'Both companion entrypoints statically import broader reference/session components; encounter and bestiary data are source-reachable. These files are not an already-separated player-only application.',
             'needed': 'Keep the current app classified as development/owner tooling until an explicit audience projection and its actual build are validated. Do not infer data isolation from a hidden tab or client selection. This report does not assert current public deployment or adjudicate every imported field.'},
            {'id': 'PKG-04', 'finding': 'The owner start page still describes the expedition source packet as unsent and the feat source decisions as future work, despite later exact expedition and feat source/acquisition evidence.',
             'needed': 'Refresh only the current navigation/status claims with exact receipt links and preserve the complete previous start page.'}],
        'sourceInformationDeleted': 0, 'sourceRulesChanged': 0, 'runtimeChanged': False,
        'playerBundleCreated': False, 'secretFreeExportConfirmed': False, 'wholeGameFlowConfirmed': False,
        'pushed': False, 'cosmologyReviewed': False}
    # Hashes are immutable evidence for this bounded snapshot, not evidence that
    # the imported payloads are public-safe or mechanics-complete.
    for b in public + director + report['sourceBindings']:
        assert info(G / b['path']) == b
    for graph in graphs.values():
        for b in graph['bindings']: assert info(G / b['path']) == b
    output.write_bytes(encoded(report))
    print(json.dumps({'report': info(output), 'counts': report['counts'],
        'sourceReachableDataCounts': {k:len(v['sourceReachableData']) for k,v in graphs.items()},
        'unresolvedLiteralImports': {k:len(v['unresolvedLocalImports']) for k,v in graphs.items()},
        'playerReleaseGateOpen': True}))


if __name__ == '__main__': main()
