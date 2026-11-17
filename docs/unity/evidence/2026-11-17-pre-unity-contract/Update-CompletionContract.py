"""Render and validate planning documents. Never builds or executes the engine."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess

ROOT = Path(__file__).resolve().parents[4]
PACKET = Path(__file__).resolve().parent
JSON_PATH = ROOT / 'docs/unity/PRE_UNITY_COMPLETION_CONTRACT.json'
MD_PATH = JSON_PATH.with_suffix('.md')


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8-sig'))


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n', encoding='utf-8', newline='\n')


def git_bytes(*args, input=None):
    return subprocess.run(['git', *args], cwd=ROOT, input=input, stdout=subprocess.PIPE, check=True).stdout


def freeze_inputs(c):
    rev = c['baselineRevision']
    tracked = set(git_bytes('ls-tree', '-r', '-z', '--name-only', rev).decode().split('\0')) - {''}
    registry = json.loads(git_bytes('show', rev + ':' + c['sourceBoundary']['registry']))
    rulemap = json.loads(git_bytes('show', rev + ':' + c['sourceBoundary']['ruleMap']))
    catalogs = json.loads(git_bytes('show', rev + ':' + c['sourceBoundary']['catalogInventory']))
    accepted = json.loads(git_bytes('show', rev + ':' + c['sourceBoundary']['acceptedEvidenceIndex']))
    requested = {}
    def add(path, reason):
        requested.setdefault(path, set()).add(reason)
    for key in ('registry', 'precedence', 'ruleMap', 'catalogInventory', 'acceptedEvidenceIndex'):
        add(c['sourceBoundary'][key], key)
    for path in ('docs/unity/DEVELOPMENT_BRIEF.md', 'docs/unity/IMPLEMENTATION_STATUS.json',
                 'docs/unity/IMPLEMENTATION_MAP.md'):
        add(path, 'accepted planning baseline')
    for domain in registry['domains']:
        for path in domain['authoritativePaths']:
            add(path, 'registry:' + domain['domain'])
    for source in rulemap['sources']:
        add(source['path'], 'historical rule-map source:' + source['id'])
    for catalog in catalogs['catalogs']:
        add(catalog['path'], 'historical catalogue:' + catalog['name'])
    for source in accepted['files']:
        add(source['path'], 'accepted-map evidence')
    expanded, missing = {}, []
    for path, reasons in sorted(requested.items()):
        matches = [path] if path in tracked else sorted(p for p in tracked if p.startswith(path.rstrip('/') + '/'))
        if not matches:
            missing.append({'path': path, 'reasons': sorted(reasons), 'disposition': 'UNRESOLVED_REFERENCE_NOT_SILENTLY_EXCLUDED'})
        for match in matches:
            expanded.setdefault(match, set()).update(reasons)
    paths = sorted(expanded)
    output = git_bytes('cat-file', '--batch', input=''.join(f'{rev}:{p}\n' for p in paths).encode())
    offset, files = 0, []
    for path in paths:
        end = output.index(b'\n', offset)
        header = output[offset:end].decode().split()
        assert len(header) == 3 and header[1] == 'blob', (path, header)
        size = int(header[2])
        data = output[end + 1:end + 1 + size]
        assert len(data) == size and output[end + 1 + size:end + 2 + size] == b'\n'
        offset = end + size + 2
        item = {'path': path, 'gitBlob': header[0], 'sha256': sha(data), 'gitBytes': size,
                'roles': sorted(expanded[path]), 'semanticAudit': 'NOT_CLAIMED_BY_THIS_INDEX'}
        if data.startswith(b'version https://git-lfs.github.com/spec/v1\n'):
            pointer = data.decode()
            item['lfsPayloadSha256'] = re.search(r'oid sha256:([0-9a-f]{64})', pointer).group(1)
            item['lfsPayloadBytes'] = int(re.search(r'\nsize (\d+)', pointer).group(1))
            item['payloadRead'] = False
        files.append(item)
    assert offset == len(output)
    return {'schemaVersion': 1, 'revision': rev,
            'scope': 'Frozen planning inputs. Source authority is decided by the registry and scoped accepted decisions, never by inclusion here. LFS payloads are identified, not downloaded or semantically audited.',
            'ruleMapSourceRecords': len(rulemap['sources']), 'areaRows': len(rulemap['areaCrosswalk']),
            'catalogues': len(catalogs['catalogs']), 'classCatalogues': len(rulemap['classInventory']),
            'requestedPaths': len(requested), 'files': files, 'unresolvedReferences': missing}


def render(c, index):
    lines = ['# Pre-Unity C# completion contract', '',
             f"As of **{c['asOfDate']}**. Criteria: **{c['contractStatus']}**. Qualification: **{c['qualificationStatus']}**. Implementation remains **paused**.", '',
             c['scope'], '', '**First integration:** ' + c['firstUnityAuthority'], '',
             '[Current implementation map](IMPLEMENTATION_MAP.md) · [Machine-readable contract](PRE_UNITY_COMPLETION_CONTRACT.json) · '
             '[Actual GPT consultation](evidence/2026-11-17-pre-unity-contract/GPT_CONSULTATION.json)', '']
    if c['evidence']['finalReview']:
        lines += ['[Final published-contract review](' + c['evidence']['finalReview'].removeprefix('docs/unity/') + ')', '']
    lines += ['## What counts as complete', '', c['coverage']['closure'], '',
              'The 100 criteria below define obligations, not 100 remaining modules or a progress denominator. '
              'All 49 original workstreams, 120 dependency edges and original acceptance criteria stand. '
              'The detailed source-family/identity/interaction ledger and qualification remain future work. '
              'Specifying UR-01 and UR-04 does not mark either gate passed.', '',
              '## Source boundary and coverage method', '',
              f"Frozen planning revision: `{c['baselineRevision']}`. "
              f"The [input index](evidence/2026-11-17-pre-unity-contract/SOURCE_INPUTS.json) pins {len(index['files'])} tracked blobs, "
              f"with {len(index['unresolvedReferences'])} unresolved path references. "
              f"It retains {index['ruleMapSourceRecords']} historical source records, {index['areaRows']} area rows, "
              f"{index['catalogues']} overlapping catalogues and {index['classCatalogues']} class inventories.", '']
    for key in ('selection', 'application', 'changeControl'):
        lines += [c['sourceBoundary'][key], '']
    lines += ['Authority: [`CANON_MANIFEST.json`](../canon/CANON_MANIFEST.json) and '
              '[repository promotion policy](../canon/REPOSITORY_PROMOTION.md).', '']
    lines += ['- ' + x for x in c['sourceBoundary']['inventoryCautions']]
    lines += ['', '### Required coverage records', '',
              'Each stable family record must carry: ' + '; '.join(c['coverage']['recordFields']) + '.', '',
              'Its semantic contract covers: ' + '; '.join(c['coverage']['semanticContract']) + '.', '']
    lines += [f'{i}. {x}' for i, x in enumerate(c['coverage']['rules'], 1)]
    lines += ['', '## Completion criteria for all 49 workstreams', '',
              'Each criterion inherits the source, reusable implementation, semantic witness, interaction and persistence requirements above. '
              'Current accepted slices/statuses are in the implementation map; whole-scope acceptance is open. '
              '“Operative” means admitted by the actual source/authority contract, including explicitly bounded development authority, '
              'not every draft card merely present in a file.', '']
    for group in c['requirements']:
        lines += ['### ' + group['workItem'], '']
        lines += ['- **' + row['id'] + ':** ' + row['criterion'] for row in group['criteria']]
        lines += ['']
    lines += ['## Required connected interaction coverage', '', c['interactionExpansion'], '']
    for row in c['interactions']:
        lines += [f"- **{row['id']} — {row['name']}:** {row['required']}"]
    p = c['performance']
    lines += ['', '## Performance and operating envelope', '', '**Status:** ' + p['status'] + '.', '', p['scope'], '',
              '### Reference host and build', '']
    for key, val in p['referenceHost'].items():
        lines += [f'- **{key}:** {val}']
    lines += ['', p['build'], '', '### Minimum qualification range', '', p['envelopePolicy'], '',
              '| Dimension | Target | Meaning |', '| --- | ---: | --- |']
    for row in p['envelope']:
        target = ', '.join(f'{x:,}' for x in row['target']) if isinstance(row['target'], list) else f"{row['target']:,}"
        lines += [f"| {row['dimension']} | {target} | {row['definition']} |"]
    lines += ['', '### Required workload shapes', '', p['workloadManifest'], '']
    for row in p['workloads']:
        lines += [f"- **{row['id']} — {row['name']}:** {row['shape']}"]
    lines += ['', '### Timing targets', '', 'Times are milliseconds. Both p95 and maximum must pass in each of three batches, '
              'separately for every named operation, applicable seat and workload.', '',
              '| ID | Public operation | p95 ms | Maximum ms | Samples / warm-ups per batch | Applies to |',
              '| --- | --- | ---: | ---: | ---: | --- |']
    for row in p['targets']:
        lines += [f"| {row['id']} | {row['operation']} | {row['p95Ms']:,} | {row['maxMs']:,} | {row['samples']} / {row['warmups']} | {row['applies']} |"]
    lines += ['', '### Size, memory and measurement protocol', '', p['memoryAndSize'], '']
    lines += [f'{i}. {x}' for i, x in enumerate(p['protocol'], 1)]
    lines += ['', '## Final C# decision and owner hold', '', c['completionDecision']['required'], '',
              c['completionDecision']['notEnough'], '', c['completionDecision']['later'], '',
              '**No next module is started.** The amended Consecrate/Consecrated Ground source/API contract remains held and unstarted. '
              'No engine compilation, gameplay scenario, benchmark, Unity integration or storage/Support work is performed by this update.', '']
    return '\n'.join(lines).encode()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    c = read('docs/unity/PRE_UNITY_COMPLETION_CONTRACT.json')
    m = read(c['map'])
    groups = c['requirements']
    assert len(groups) == 49 and {g['workItem'] for g in groups} == {r['id'] for r in m['workItems']}
    criteria = [r['id'] for g in groups for r in g['criteria']]
    assert len(criteria) == len(set(criteria)) == 100
    for group, row in zip(groups, m['workItems']):
        assert group['workItem'] == row['id']
        assert row['completionCriteria'] == [v['id'] for v in group['criteria']]
    prior = json.loads(git_bytes('show', c['baselineRevision'] + ':' + c['map']))
    assert all(a == {k: v for k, v in b.items() if k != 'completionCriteria'}
               for a, b in zip(prior['workItems'], m['workItems']))
    assert prior['frozenRuntime'] == m['frozenRuntime']
    assert prior['qualifiedConsoleHost'] == m['qualifiedConsoleHost']
    for name in ('DEVELOPMENT_HANDOFF.md', 'IMPLEMENTATION_TRACE.md', 'UNITY_ENGINE_PLAN.md'):
        path = 'docs/unity/' + name
        original = git_bytes('show', c['baselineRevision'] + ':' + path)
        assert (ROOT / path).read_bytes().endswith(original.split(b'\n', 1)[1])
    host = read('docs/unity/evidence/2026-11-17-pre-unity-contract/REFERENCE_HOST.json')
    assert 'i5-4590' in host['cpu']['Name']
    assert host['cpu']['NumberOfCores'] == c['performance']['referenceHost']['physicalCores']
    assert host['os']['Version'] == '10.0.19045'
    assert host['powershell'] == c['performance']['referenceHost']['powershell']
    assert host['runtime'] == '.NET ' + c['performance']['referenceHost']['dotnet']
    assert c['implementation'] == m['hold']['implementation'] == 'PAUSED_BY_OWNER'
    assert c['qualificationStatus'] == 'NOT_QUALIFIED'
    if c['evidence']['finalReview']:
        review = read(c['evidence']['finalReview'])
        assert c['contractStatus'] == 'ACCEPTED_PLANNING_CRITERIA_ONLY'
        assert review['status'] == 'ACCEPTED_PLANNING_DOCUMENTATION_ONLY'
        assert any(item['type'] == 'agentMessage' and item['id'] == review['responseId']
                   for item in review['turn']['items'])
    assert len(c['interactions']) == len({x['id'] for x in c['interactions']}) == 10
    assert len(c['performance']['targets']) == 10
    for t in c['performance']['targets']:
        assert 0 < t['p95Ms'] <= t['maxMs']
        assert t['samples'] in (20, 100)
    assert all(g['status'] == 'SPECIFIED_NOT_YET_QUALIFIED' for g in m['readiness']['gates'] if g['id'] in ('UR-01', 'UR-04'))
    index = freeze_inputs(c)
    assert index['ruleMapSourceRecords'] == 66 and index['areaRows'] == 75
    assert index['catalogues'] == 27 and index['classCatalogues'] == 17
    rendered = render(c, index)
    if args.write:
        write_json(PACKET / 'SOURCE_INPUTS.json', index)
        MD_PATH.write_bytes(rendered)
    else:
        assert read(c['sourceBoundary']['frozenInputIndex']) == index
        assert MD_PATH.read_bytes() == rendered
    links = re.findall(r'\]\(([^)]+)\)', rendered.decode())
    for link in links:
        assert (MD_PATH.parent / link.split('#')[0]).is_file(), link
    report = {'schemaVersion': 1, 'status': 'PASS_DOCUMENTATION_ONLY',
              'noRuntimeBuildOrBenchmark': True, 'workstreams': 49, 'criteria': 100,
              'priorRowStatusesScopeEvidencePreserved': 49, 'runtimeAndHostPinsPreserved': True,
              'historicalHandoffTracePlanBodiesPreserved': True, 'referenceHostFactsChecked': True,
              'requiredInteractionFamilies': 10, 'workloadShapes': 6, 'timingTargets': 10,
              'pinnedInputBlobs': len(index['files']), 'unresolvedSourceReferences': index['unresolvedReferences'],
              'localLinksChecked': len(links), 'criteriaJsonSha256': sha(JSON_PATH.read_bytes()),
              'renderedContractSha256': sha(rendered), 'sourceIndexSha256': sha((PACKET / 'SOURCE_INPUTS.json').read_bytes()),
              'validatorSha256': sha(Path(__file__).read_bytes())}
    write_json(PACKET / 'VALIDATION.json', report)
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
