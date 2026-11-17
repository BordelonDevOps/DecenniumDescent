"""Render/check documentation only. Never executes gameplay or changes runtime."""
from pathlib import Path
from collections import Counter
import argparse
import hashlib
import json
import re
import subprocess

ROOT = Path(__file__).resolve().parents[4]
PACKET = Path(__file__).resolve().parent
STATUS = ROOT / 'docs/unity/IMPLEMENTATION_STATUS.json'
OUTPUT = ROOT / 'docs/unity/IMPLEMENTATION_MAP.md'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def baseline_blobs(revision, paths):
    requests = ''.join(f'{revision}:{p}\n' for p in paths).encode()
    result = subprocess.run(['git', 'cat-file', '--batch'], cwd=ROOT,
                            input=requests, stdout=subprocess.PIPE, check=True)
    output = result.stdout
    offset = 0
    blobs = {}
    for path in paths:
        end = output.index(b'\n', offset)
        header = output[offset:end].decode().split()
        assert len(header) == 3 and header[1] == 'blob', (path, header)
        size = int(header[2])
        data = output[end + 1:end + 1 + size]
        assert len(data) == size and output[end + 1 + size:end + 2 + size] == b'\n'
        blobs[path] = (header[0], data)
        offset = end + 2 + size
    assert offset == len(output)
    return blobs


def relative(path):
    assert path.startswith('docs/unity/')
    return path[len('docs/unity/'):]


def link(path, label=None):
    return f'[{label or Path(path).name}]({relative(path)})'


def render(m):
    counts = Counter(w['currentStatus'] for w in m['workItems'])
    lines = [
        '# Current C# implementation map and Unity entry checklist', '',
        f"As of **{m['asOfDate']}**, reconciled against Engine `{m['implementationBaseline']}`. "
        '**Unity gameplay integration is not ready. Development remains paused.** '
        'This update changes documentation only; it does not start the next module.', '',
        f"**Documentation review:** {m['status']}. "
        + (link(m['finalDocumentationReview'], 'Actual final map review') if m['finalDocumentationReview'] else 'Actual review of this concrete map is pending.') , '',
        '**What is complete:** the shared technical baseline and the named source-bound slices below, '
        'including the accepted INT-03 connected minimum, independent recipe-4 verification, C# quality explanation, '
        'Cleric/Bishop progression and casting, declared geometry and Ferry-Wraith encounter. '
        'Those completed slices stay accepted. Each broader workstream retains its own unfinished scope.', '',
        '**What is left:** the concrete known gaps in all 49 rows, plus two unresolved planning contracts: '
        'the finite required capability/content coverage (UR-01) and operating envelope (UR-04). '
        'Until those contracts are explicit, no exact remaining module count, percentage or delivery date is justified. '
        'This is the complete 49-workstream status reconciliation, not a claim to have exhaustively audited every source clause.', '',
        'The last accepted qualification is **1,584/1,584 registered cases** and five matching 463-command paths. '
        'These are retained TAC-10 executions, not tests run for this documentation update. '
        + link('docs/unity/evidence/2026-11-16-tac10-ferry-wraith-runtime/FINAL_ACCEPTANCE.md', 'TAC-10 acceptance'), '',
        '## Read this map', '',
        'An accepted slice is complete only within its exact contract. No row is marked as a globally completed '
        'workstream without such a whole-scope decision. Status counts below describe 49 differently sized workstreams; '
        'they are not a progress percentage. Evidence links preserve the original approval, source/implementation '
        'revisions, execution and exclusions. The baseline source index pins their exact bytes.', '',
        '| Status | Rows | Meaning |', '| --- | ---: | --- |'
    ]
    for status, meaning in m['statusLegend'].items():
        lines.append(f'| {status} | {counts[status]} | {meaning} |')
    lines += ['', 'The [machine-readable map](IMPLEMENTATION_STATUS.json) preserves all 49 IDs, '
              'all 120 direct dependency edges and every original acceptance criterion. '
              'The November 3 JSON and old trace tables remain historical records, not current status. '
              '[Pinned evidence index](evidence/2026-11-17-implementation-map/BASELINE_SOURCE_INDEX.json).', '',
              '## Before Unity: explicit remaining gates', '',
              m['readiness']['scopePolicy'], '',
              'These gates organize the existing mandate and identify unresolved contracts. '
              'They grant no new mechanics, change no prior acceptance, and set no invented universal performance threshold.', '']
    for gate in m['readiness']['gates']:
        lines += [f"### {gate['id']} — {gate['title']}", '', f"**Status: {gate['status']}.**", '',
                  '**Remaining:** ' + gate['remaining'], '', '**Closure evidence:** ' + gate['closure'], '',
                  '**Mapped work:** ' + ', '.join(gate['workItems']), '',
                  '**Basis:** ' + ' · '.join(link(p) for p in gate['evidence']), '']
    lines += ['## Held next dependency', '', m['hold']['nextRecordedGate'], '',
              'The selected operational sequence is accepted declared geometry → accepted Ferry-Wraith → '
              'return the complete amended two-card Consecration contract. This is a scoped prerequisite sequence, '
              'not a new graph edge or authorization for the entire remaining class/resurrection chain.', '',
              '- TAC-03 ← CHR-01, TAC-01.',
              '- TAC-10 ← TAC-03, TAC-04, TAC-05, TAC-02.',
              '- CHR-05 ← CHR-03, TAC-02, TAC-05, TAC-08.', '',
              'The five terrain interpretations remain settled. The held contract must retain recharge registration, '
              'versioned base Rite → Ground → Radiance healing/cure → Aura ordering, final-HP cap/cure evidence, '
              'and a genuinely funded replacement route with original expiry. No such successor work is performed here. '
              + link('docs/unity/evidence/2026-11-16-chr05-consecration-contract/SOURCE_API_DECISIONS.md', 'Existing decisions'), '',
              '## Workstream-by-workstream status', '',
              '“Remaining” records known capability or qualification gaps, not a promise that all are authorized next. '
              'Source gaps require the existing source/Codex/GPT process; material scope reductions and production promotion '
              'remain owner decisions. Evidence gaps are not proof of a runtime defect. Every new implementation is held by the owner.', '']
    family = None
    for row in m['workItems']:
        group = row['id'].split('-')[0]
        if group != family:
            family = group
            lines += [f'### {group}', '']
        lines += [f"#### {row['id']} — {row['title']}", '',
                  f"**{row['currentStatus']}** · Dependencies: " + (', '.join(row['dependencies']) or 'none in the original graph') + '.', '',
                  '**Implemented / accepted scope:** ' + row['implementedOrAcceptedScope'], '',
                  '**Remaining:** ' + row['remainingCapabilityOrQualification'], '',
                  '**Gap types:** ' + ', '.join(row['gapKinds']) + '. Implementation is held.', '',
                  '**Original acceptance criterion:** ' + row['acceptance'], '',
                  '**Evidence:** ' + (' · '.join(link(p, f'{Path(p).parent.name}/{Path(p).name}') for p in row['evidence'])
                    if row['evidence'] else 'No accepted runtime record identified. Baseline map/trace coverage finding; not a claim that no related code exists.') , '']
    lines += ['## Later Unity and product work', '',
              'Keep these separate from completion of the C# prerequisite; the Editor template is preparation only.', '',
              '| Item | Status | Remaining work |', '| --- | --- | --- |']
    for item in m['readiness']['laterUnityAndProduct']:
        lines.append(f"| {item['id']} | {item['status']} | {item['work']} |")
    lines += ['', '## Scope and evidence safeguards', '',
              '- Preserve all settled source decisions and supported saves. A map update cannot promote TEST_ONLY content.',
              '- Preserve the accepted INT-03 minimum and its per-run restoration criterion; original failed/long-history measurements remain disclosed.',
              '- INT-04 recipe4\'s 1,486 assertion invocations are not 1,486 new registered engine tests.',
              '- TAC-10\'s entirely genuine fear-through-entry cure remains unproved, not impossible. Its approved mechanical allocation is accepted and is not a new open blocker. Modified mechanical full states reject at encoding; component-only roundtrips and direct repeat denials retain their limits.',
              '- Do not reuse stale NOT PORTED labels for accepted casting, repertoire, geometry or creature slices. Do not claim all 17 classes, all spells/feats/recipes or general AI from those slices.',
              '- No C# build, gameplay, save restore, regression suite or Unity qualification is rerun by this documentation updater.', '',
              'Consultation: ' + link(m['consultationRecord'], 'Exact GPT consultation and Codex disposition') + '.', '']
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    m = json.loads(STATUS.read_text(encoding='utf-8-sig'))
    old = json.loads((ROOT / m['historicalDependencyMap']).read_text(encoding='utf-8-sig'))
    original = {w['id']: w for w in old['workItems']}
    rows = m['workItems']
    assert len(rows) == len(original) == 49 and len({w['id'] for w in rows}) == 49
    assert set(original) == {w['id'] for w in rows}
    for row in rows:
        for key in ('id', 'title', 'dependencies', 'acceptance'):
            assert row[key] == original[row['id']][key], (row['id'], key)
        assert row['currentStatus'] in m['statusLegend']
        assert row['implementedOrAcceptedScope'] and row['remainingCapabilityOrQualification']
        assert not row['wholeWorkstreamComplete']
    assert sum(len(w['dependencies']) for w in rows) == 120
    visited = set()
    while len(visited) < 49:
        ready = {w['id'] for w in rows if w['id'] not in visited and set(w['dependencies']) <= visited}
        assert ready, 'Dependency cycle or unresolved node'
        visited |= ready
    paths = {m['historicalDependencyMap'], 'docs/unity/IMPLEMENTATION_TRACE.md',
             'docs/unity/DEVELOPMENT_HANDOFF.md', 'docs/unity/DEVELOPMENT_BRIEF.md'}
    for row in rows:
        paths.update(row['evidence'])
    for gate in m['readiness']['gates']:
        paths.update(gate['evidence'])
        assert set(gate['workItems']) <= set(original)
    paths = sorted(paths)
    for path in paths:
        assert (ROOT / path).is_file(), path
    blobs = baseline_blobs(m['implementationBaseline'], paths)
    source_index = {'schemaVersion': 1, 'baselineRevision': m['implementationBaseline'],
                    'scope': 'Pinned documentation/evidence records, not new runtime qualification.',
                    'files': [{'path': p, 'gitBlob': blobs[p][0], 'bytes': len(blobs[p][1]),
                               'sha256': digest(blobs[p][1])} for p in paths]}
    index_path = PACKET / 'BASELINE_SOURCE_INDEX.json'
    rendered = render(m).encode('utf-8')
    if args.write:
        OUTPUT.write_bytes(rendered)
        index_path.write_text(json.dumps(source_index, indent=2) + '\n', encoding='utf-8', newline='\n')
    else:
        assert OUTPUT.read_bytes() == rendered, 'Rendered map is stale'
        assert json.loads(index_path.read_text(encoding='utf-8')) == source_index, 'Source index differs'
    relative_links = re.findall(r'\]\(([^)]+)\)', rendered.decode())
    for path in relative_links:
        if path.startswith(('http://', 'https://', '#')):
            continue
        assert (OUTPUT.parent / path.split('#')[0]).is_file(), path
    report = {'schemaVersion': 1, 'status': 'PASS', 'scope': 'Documentation structure/source bindings only; no engine execution.',
              'baseline': m['implementationBaseline'], 'workItems': 49, 'dependencyEdges': 120,
              'preservedAcceptanceCriteria': 49, 'acyclicGraph': True, 'sourceFiles': len(paths),
              'relativeLinksChecked': len(relative_links), 'readinessGates': len(m['readiness']['gates']),
              'statusCounts': dict(sorted(Counter(w['currentStatus'] for w in rows).items())),
              'statusJsonSha256': digest(STATUS.read_bytes()), 'renderedMapSha256': digest(rendered),
              'validatorSha256': digest(Path(__file__).read_bytes())}
    (PACKET / 'VALIDATION.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8', newline='\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
