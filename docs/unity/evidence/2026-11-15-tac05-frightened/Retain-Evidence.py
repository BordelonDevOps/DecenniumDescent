"""Bind TAC05 evidence to immutable implementation; --complete requires the original exact run to finish."""
import argparse
import datetime
import hashlib
import io
import json
from pathlib import Path
import shutil
import subprocess
import zipfile


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def lines(path):
    return path.read_text(encoding='utf-8-sig').splitlines()


def digest(value):
    return hashlib.sha256(value).hexdigest()


def sha(path):
    return digest(path.read_bytes())


def require(value, message):
    if not value:
        raise ValueError(message)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--implementation', default='f5800818bfadb7c51865c96a6058f9af2deb75a3')
    parser.add_argument('--complete', action='store_true')
    args = parser.parse_args()
    packet = Path(__file__).resolve().parent
    root = packet.parents[3]
    development = root / 'engine/artifacts/tac05-frightened/development'
    output = packet / 'retained-development'
    artifacts = {}
    archive_bytes = subprocess.check_output(['git', 'archive', '--format=zip', args.implementation, 'engine'], cwd=root)
    archive = zipfile.ZipFile(io.BytesIO(archive_bytes))

    def retain(source, relative):
        target = packet / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        artifacts[relative] = {'sha256': sha(target), 'bytes': target.stat().st_size}

    def tree(relative):
        source = development / relative
        require(source.is_dir(), 'Missing evidence directory: ' + relative)
        for file in sorted(source.rglob('*')):
            if file.is_file():
                retain(file, 'retained-development/' + file.relative_to(development).as_posix())

    def report(relative):
        value = read(development / relative)
        require(value.get('status', value.get('Status')) == 'PASS', 'Failed evidence: ' + relative)
        return value

    pinned = read(packet / 'SOURCE_BINDINGS.json')['sources']
    requests = ''.join(row['revision'] + ':' + row['path'] + '\n' for row in pinned).encode('utf-8')
    batch = subprocess.run(['git', 'cat-file', '--batch'], cwd=root, input=requests, stdout=subprocess.PIPE, check=True).stdout
    reader = io.BytesIO(batch)
    for row in pinned:
        header = reader.readline().decode('ascii').strip().split()
        require(len(header) == 3 and header[0] == row['gitBlob'] and header[1] == 'blob', 'Pinned blob changed: ' + row['path'])
        payload = reader.read(int(header[2]))
        require(reader.read(1) == b'\n' and digest(payload) == row['sha256'], 'Pinned source hash changed: ' + row['path'])
    require(reader.read() == b'', 'Unexpected pinned batch output')

    builds = ['run-20261115T093650131Z-40129a7c', 'case-20261115T093927408Z',
              'compile-20261115T093927386Z-07dca160', 'static/static-20261115T093927415Z-c23a0399']
    for relative in builds:
        value = report(relative + '/results.json')
        for row in value['sourceHashes']:
            name = 'engine/' + row['path'].replace('\\', '/')
            require(digest(archive.read(name)) == row['sha256'].lower(), 'Compilation/source mismatch: ' + name)
            require(sha(root / name) == row['sha256'].lower(), 'Working source changed: ' + name)
        tree(relative)
    assemblies = {name: sha(development / builds[0] / name) for name in
                  ['Decennium.Foundation.' + part + '.dll' for part in ('Core', 'Persistence', 'LabModel', 'HeadlessTests')]}
    source_manifest = read(packet / 'development-checkpoint/manifest.json')
    for row in source_manifest['sourceFiles']:
        require(digest(archive.read(row['path'])) == row['sha256'] == sha(root / row['path']), 'Changed implementation file: ' + row['path'])

    paths = [('paths-main-20261115T093859999Z', 'trace-main-20261115T093745297Z', 216),
             ('paths-ability-check', 'trace-ability-check', 186), ('paths-sight-loss', 'trace-sight-loss', 181)]
    comparisons = 0
    path_summary = {}
    for relative, trace, commands in paths:
        value = report(relative + '/results.json')
        require(value['traceSha256'] == sha(development / trace / 'inputs.jsonl'), 'Changed typed trace')
        manifest = read(development / trace / 'manifest.json')
        expected = {row['name']: row['sha256'] for row in manifest['marks']}
        require(set(value['paths']) == {'ConsoleUninterrupted', 'ConsoleRestored', 'TypedUninterrupted', 'TypedRestored', 'ReceiptReplay'}, 'Missing execution path')
        for row in value['assemblies']:
            require(assemblies['Decennium.Foundation.' + row['name'] + '.dll'] == row['sha256'], 'Wrong path assembly')
        for mode, actual in value['paths'].items():
            require(actual['commands'] == commands and actual['checkpoints'] == expected, 'Checkpoint inventory mismatch: ' + mode)
            for name, expected_sha in expected.items():
                require(sha(development / relative / mode / name) == expected_sha, 'Checkpoint bytes mismatch: ' + mode + '/' + name)
                require(sha(development / trace / 'reference' / name) == expected_sha, 'Reference bytes mismatch')
                comparisons += 1
        path_summary[relative] = {'commands': commands, 'checkpoints': expected}
        tree(relative)
        tree(trace)
    require(comparisons == 95, 'Expected 95 checkpoint comparisons')

    controls = ['clock-components-3', 'projection-controls', 'forced-movement-controls-2', 'historical-check-controls',
                'historical-consumer-controls', 'boundary-controls', 'console-source-probe', 'console-boundary-controls-2',
                'closure-transition-controls', 'compatibility']
    for relative in controls:
        report(relative + '/results.json')
        tree(relative)
    compatibility = read(development / 'compatibility/results.json')
    require(len(compatibility['Cases']) == compatibility['NewProfileRejections'] == 19
            and {row['Wire'] for row in compatibility['Cases']} == set(range(95, 107)), 'Missing authentic compatibility input')
    for row in compatibility['Cases']:
        require(row['SourceSha256'] == row['RoundtripSha256'] == row['ContinuedSha256'] and row['Commands'] > 0, 'Failed real save continuation')
        for key in ('Source', 'Earlier'):
            original = packet.parent / row[key].replace('\\', '/')
            require(sha(original) == row[key + 'Sha256'], 'Changed authentic predecessor input')
    focus = report('source-integration-controls.json')
    require(len(focus['cases']) == 130 and all(x['Passed'] and not x['Error'] for x in focus['cases']), 'Incomplete focused controls')
    for name in ('source-integration-controls.json', 'source-integration-inventory.txt', 'consumer-scope-progress.json'):
        retain(development / name, 'retained-development/' + name)
    require(read(development / 'consumer-scope-progress.json')['status'] == 'CONSUMER_SCOPE_RECORDED_NOT_MODULE_ACCEPTANCE', 'Consumer audit unfinished')
    for pattern in ('*.ps1', '*.py'):
        for file in sorted(development.glob(pattern)):
            retain(file, 'retained-development/' + file.name)
    # Retain the failed expectation label and the genuine branch without overwriting prior evidence.
    for relative in ('console-boundary-controls', 'branch-study-20261115T091844426Z'):
        tree(relative)
    for name in ('branch-study-closure.jsonl',):
        retain(development / name, 'retained-development/' + name)

    run = development / 'regression'
    launch = read(run / 'launch.json')
    require(launch['runId'] == 'd9620202bba1434aa4885782edb2888d' and launch['assemblies'] == assemblies, 'Different original regression run')
    names = lines(run / 'all-names.txt')
    new_names = [name for name in names if name.startswith('tac05_frightened_')]
    previous = lines(packet.parent / '2026-11-15-tac07-cleric-repertoire/regression/inventory.txt')
    require(len(names) == len(set(names)) == 1517 and len(new_names) == 8
            and [name for name in names if name not in new_names] == previous, 'Wrong exact ordered inventory')
    require(launch['inventorySha256'] == sha(run / 'all-names.txt')
            and launch['compiledSourceReportSha256'] == sha(run / 'compiled-source-report.json')
            and sha(run / 'compiled-source-report.json') == sha(development / builds[0] / 'results.json'), 'Wrong compiled run source binding')
    runner = root / 'docs/unity/evidence/2026-11-12-mgt06-connected-trap/Run-ExactTrapShard.ps1'
    require(sha(runner) == launch['runnerSha256'], 'Changed exact worker')
    retain(runner, 'support/Run-ExactTrapShard.ps1')
    processes = {row['group']: row for row in read(run / 'processes.json')}
    union = []
    results = {}
    modules = None
    finished = []
    for group in ('shard' + letter for letter in 'ABCDEF'):
        start = read(run / (group + '.started.json'))
        assigned = lines(run / (group + '-names.txt'))
        union.extend(assigned)
        require(start['runId'] == launch['runId'] and start['group'] == group and start['pid'] == processes[group]['pid']
                and len(assigned) == processes[group]['cases'] and start['inventorySha256'] == launch['inventorySha256']
                and start['assignmentSha256'] == sha(run / (group + '-names.txt')) == launch['assignments'][group]
                and {name: value['sha256'] for name, value in start['assemblies'].items()} == assemblies, 'Worker identity mismatch: ' + group)
        actual_modules = {name: value['moduleId'] for name, value in start['assemblies'].items()}
        require(modules is None or modules == actual_modules, 'Worker loaded different modules')
        modules = actual_modules
        # Snapshot an append-only journal once, then validate the exact retained bytes.
        for suffix in ('-names.txt', '.started.json', '.jsonl'):
            retain(run / (group + suffix), 'retained-development/regression/' + group + suffix)
        journal_path = output / 'regression' / (group + '.jsonl')
        journal = [json.loads(line) for line in lines(journal_path)]
        require([row['Name'] for row in journal] == assigned[:len(journal)], 'Worker journal is not assigned prefix')
        for row in journal:
            require(row['Passed'] and not row['Error'] and row['Name'] not in results, 'Failed/duplicate exact case: ' + str(row))
            results[row['Name']] = row
        if args.complete:
            completed = read(run / (group + '.execution.json'))
            require(all(completed.get(k) == v for k, v in start.items()) and completed['journalSha256'] == sha(journal_path)
                    and completed['cases'] == len(assigned) == len(journal) and lines(run / (group + '.done')) == ['DONE'], 'Incomplete exact worker: ' + group)
            for suffix in ('.execution.json', '.done'):
                retain(run / (group + suffix), 'retained-development/regression/' + group + suffix)
            finished.append(group)
    require(sorted(union) == sorted(names), 'Assignments differ from exact inventory')
    for name in ('launch.json', 'processes.json', 'all-names.txt', 'compiled-source-report.json'):
        retain(run / name, 'retained-development/regression/' + name)
    tree('regression/execution-assemblies')
    if args.complete:
        require(set(results) == set(names), 'Full regression incomplete')
    regression = {'status': 'PASS' if args.complete else 'RUNNING_NOT_A_PASS', 'runId': launch['runId'],
                  'implementationCommit': args.implementation, 'launchCommitNote': 'Launch preceded checkpoint commit; immutable compiled source hashes and DLLs are bound to the commit here.',
                  'discovered': len(names), 'completed': len(results), 'failed': 0, 'finishedWorkers': finished,
                  'assemblies': assemblies, 'moduleIds': modules, 'cases': [results[n] for n in names if n in results]}
    summary = packet / 'REGRESSION_PROGRESS.json'
    summary.write_text(json.dumps(regression, indent=2) + '\n', encoding='utf-8')
    artifacts[summary.name] = {'sha256': sha(summary), 'bytes': summary.stat().st_size}
    source_zip = packet / 'implementation-engine.zip'
    source_zip.write_bytes(archive_bytes)
    artifacts[source_zip.name] = {'sha256': sha(source_zip), 'bytes': source_zip.stat().st_size}
    for file in sorted(packet.iterdir()):
        if file.is_file() and file.suffix in ('.md', '.py', '.json') and file.name != 'IMPLEMENTATION_BINDINGS.json':
            artifacts[file.name] = {'sha256': sha(file), 'bytes': file.stat().st_size}
    binding = {'status': 'EVIDENCE_READY_FOR_FINAL_REVIEW' if args.complete else 'INTERIM_EVIDENCE_FULL_REGRESSION_RUNNING',
               'atUtc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'implementationCommit': args.implementation,
               'contractReview': '226d668a-fd32-51b3-b64c-bbd74b67e64c', 'closureGuidance': 'bd6e3553-7534-5fdb-9883-e2426d85c097',
               'sourceFiles': source_manifest['sourceFiles'], 'newRegisteredCases': new_names, 'pathComparisons': comparisons,
               'paths': path_summary, 'compatibilityCases': 19, 'regression': {k: v for k, v in regression.items() if k != 'cases'},
               'unity': 'DEFERRED_NOT_RUN', 'finalAcceptance': 'PENDING', 'successor': 'CHR03_HELD', 'artifacts': dict(sorted(artifacts.items()))}
    (packet / 'IMPLEMENTATION_BINDINGS.json').write_text(json.dumps(binding, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'status': binding['status'], 'artifacts': len(artifacts), 'regressionCompleted': len(results), 'comparisons': comparisons}))


if __name__ == '__main__':
    main()
