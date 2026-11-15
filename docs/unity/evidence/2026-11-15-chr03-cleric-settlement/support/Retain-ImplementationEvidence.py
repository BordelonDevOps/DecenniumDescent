"""Retain and reconcile the immutable CHR03 implementation's completed execution evidence."""
import argparse
import datetime
import hashlib
import json
from pathlib import Path
import shutil
import zipfile

PACKET = Path(__file__).resolve().parents[1]
ROOT = PACKET.parents[3]
ART = ROOT / 'engine/artifacts/chr03-cleric-settlement'
OUT = PACKET / 'implementation'
COMMIT = '34229ec6f19c9569dd35fd7b6013b99f37759c85'
REG = ART / 'regression-20261115T1324'
GROUPS = ['shard' + letter for letter in 'ABCDEF']

def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))

def lines(path):
    return path.read_text(encoding='utf-8-sig').splitlines()

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def require(value, message):
    if not value:
        raise ValueError(message)

def retain(source, relative):
    target = OUT / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)

def tree(source, relative):
    require(source.is_dir(), 'Missing evidence folder: ' + str(source))
    for file in sorted(source.rglob('*')):
        if file.is_file():
            retain(file, str(Path(relative) / file.relative_to(source)))

def passed(path):
    value = read(path)
    require(value.get('status', value.get('Status')) == 'PASS', 'Evidence has not passed: ' + str(path))
    return value

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--checkpoint', action='store_true', help='Retain completed evidence and exact observed journal prefixes; never claim full-run completion.')
    args = parser.parse_args()
    checkpoint_stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    launch = read(REG / 'launch.json')
    require(launch['sourceCommit'] == COMMIT and launch['requiredCount'] == 1524, 'Wrong source/run inventory')
    require(sha(Path(launch['runner'])) == launch['runnerSha256'], 'Original execution runner changed')
    names = lines(REG / 'all-names.txt')
    prior = lines(PACKET.parent / '2026-11-15-tac05-frightened/retained-development/regression/all-names.txt')
    focus = [name for name in names if name.startswith('chr03_')]
    require(len(names) == 1524 and len(focus) == 7 and [name for name in names if name not in focus] == prior
            and len(prior) == 1517 and sha(REG / 'all-names.txt') == launch['inventorySha256'], 'Predecessor order changed')
    processes = {row['group']: row for row in read(REG / 'processes.json')}
    all_results = []
    completed_workers = []
    captured_journals = {}
    for group in GROUPS:
        assignment = lines(REG / (group + '-names.txt'))
        journal_bytes = (REG / (group + '.jsonl')).read_bytes()
        rows = [json.loads(row) for row in journal_bytes.decode('utf-8-sig').splitlines()]
        captured_journals[group] = journal_bytes
        started = read(REG / (group + '.started.json'))
        done = REG / (group + '.done')
        complete = done.exists() and lines(done) == ['DONE']
        require(complete or args.checkpoint, 'Original worker has not completed: ' + group)
        execution = read(REG / (group + '.execution.json')) if complete else started
        if complete:
            completed_workers.append(group)
            require(execution['cases'] == len(assignment) == processes[group]['cases']
                    and execution['journalSha256'] == hashlib.sha256(journal_bytes).hexdigest(), 'Completed worker journal/count differs')
        else:
            require(len(rows) <= len(assignment) == processes[group]['cases'], 'Observed journal exceeds assignment')
        require(execution['runId'] == started['runId'] == launch['runId']
                and execution['pid'] == started['pid'] == processes[group]['pid'], 'Worker identity/count mismatch')
        require([row['Name'] for row in rows] == (assignment if complete else assignment[:len(rows)])
                and all(row['Passed'] and not row['Error'] for row in rows),
                'Original worker failed or differs from assignment: ' + group)
        require(launch['assignments'][group] == sha(REG / (group + '-names.txt'))
                and execution['assignmentSha256'] == launch['assignments'][group]
                and execution['inventorySha256'] == launch['inventorySha256'], 'Execution hashes differ')
        for name, digest in launch['assemblies'].items():
            require(execution['assemblies'][name]['sha256'] == started['assemblies'][name]['sha256'] == digest
                    and execution['assemblies'][name]['moduleId'] == started['assemblies'][name]['moduleId']
                    and sha(REG / 'execution-assemblies' / name) == digest, 'Loaded binary identity differs')
        all_results.extend(rows)
    require(len(all_results) == len({row['Name'] for row in all_results})
            and (args.checkpoint or len(all_results) == len(names)), 'Missing or duplicate full-suite result')
    require(set(focus).issubset({row['Name'] for row in all_results}), 'New focused cases are not all complete')
    # Captured prefixes are explicitly incomplete historical observations. A final
    # reconciliation must prove every captured byte belongs to the original journal.
    if args.checkpoint:
        checkpoint_dir = OUT / 'regression-checkpoints' / checkpoint_stamp
        checkpoint_dir.mkdir(parents=True)
        for group, data in captured_journals.items():
            (checkpoint_dir / (group + '.jsonl')).write_bytes(data)
    else:
        for prefix in (OUT / 'regression-checkpoints').glob('*/*.jsonl'):
            require((REG / prefix.name).read_bytes().startswith(prefix.read_bytes()), 'Original journal diverged from a retained prefix')
    for file in REG.iterdir():
        if file.is_file() and (not args.checkpoint or file.name.endswith(('-names.txt', '.started.json'))
                or file.name in {'launch.json', 'processes.json', 'all-names.txt', 'compiled-source-report.json'}):
            retain(file, 'regression/' + file.name)
    for name in focus:
        tree(REG / 'saves' / name, 'focused/' + name)
    for folder, label in [
        ('final-build/run-20261115T132143959Z-f74bd41b', 'headless'),
        ('final-standalone/compile-20261115T132206197Z-4d7e4595', 'standalone'),
        ('final-static/static-20261115T132206236Z-3b51c539', 'static')]:
        report = passed(ART / folder / 'results.json')
        for source in report.get('sourceHashes', []):
            require(sha(ROOT / 'engine' / source['path'].replace('\\', '/')) == source['sha256'].lower(), 'Build source changed')
        for file in (ART / folder).iterdir():
            if file.is_file() and file.suffix != '.dll':
                retain(file, 'builds/' + label + '/' + file.name)
    source_audit = passed(OUT / 'SOURCE_AUDIT.json')
    require(source_audit['implementationCommit'] == COMMIT
            and sha(OUT / source_audit['sourceArchive']) == source_audit['sourceArchiveSha256']
            and sha(REG / 'compiled-source-report.json') == source_audit['buildReportSha256'], 'Source/archive/build identity differs')
    with zipfile.ZipFile(OUT / 'execution-assemblies.zip', 'w', zipfile.ZIP_DEFLATED) as archive:
        for name in launch['assemblies']:
            archive.write(REG / 'execution-assemblies' / name, name)
    comparisons = 0
    campaigns = {}
    for route, commands, marks in [('primary', 198, 8), ('alternate', 222, 9)]:
        folder = ART / ('campaign-' + route + '-20261115T1330')
        manifest = read(folder / 'trace/manifest.json')
        paths = passed(folder / 'paths/results.json')
        expected = {row['name']: row['sha256'] for row in manifest['marks']}
        require(manifest['revision'] == commands and len(expected) == marks, 'Campaign command/checkpoint inventory differs')
        require(set(paths['paths']) == {'ConsoleUninterrupted', 'ConsoleRestored', 'TypedUninterrupted', 'TypedRestored', 'ReceiptReplay'}, 'Missing campaign execution mode')
        require(paths['traceSha256'] == sha(folder / 'trace/inputs.jsonl'), 'Changed typed command input')
        for row in paths['assemblies']:
            require(row['sha256'] == launch['assemblies']['Decennium.Foundation.' + row['name'] + '.dll'], 'Wrong campaign binary')
        for mode, result in paths['paths'].items():
            require(result['commands'] == commands and result['checkpoints'] == expected, 'Campaign checkpoint mismatch')
            for name, digest in expected.items():
                require(sha(folder / 'trace/reference' / name) == sha(folder / 'paths' / mode / name) == digest, 'Canonical checkpoint bytes differ')
                comparisons += 1
        campaigns[route] = {'commands': commands, 'checkpoints': marks, 'modes': 5}
        tree(folder, 'campaigns/' + route)
    require(comparisons == 85, 'Incomplete connected comparisons')
    compatibility = passed(ART / 'compatibility-final/results.json')
    require(len(compatibility['Cases']) == compatibility['NewProfileRejections'] == 21, 'Missing authentic compatibility case')
    for index, row in enumerate(compatibility['Cases']):
        source = PACKET.parent / row['Source']
        earlier = PACKET.parent / row['Earlier']
        folder = ART / 'compatibility-final' / ('case-' + str(index) + '-wire' + str(row['Wire']))
        require(row['Commands'] > 0 and sha(source) == row['SourceSha256'] == sha(folder / 'roundtrip.ddsave')
                == sha(folder / 'continued.ddsave') and sha(earlier) == row['EarlierSha256'], 'Authentic save continuation changed')
        retain(source, 'compatibility/authentic/case-' + str(index) + '-final.ddsave')
        retain(earlier, 'compatibility/authentic/case-' + str(index) + '-earlier.ddsave')
    tree(ART / 'compatibility-final', 'compatibility')
    retain(ART / 'compatibility-20261115T1324/progress.json', 'compatibility/original-completed-19.json')
    tree(ART / 'compatibility-20261115T1324/case-19-wire107', 'compatibility/original-dispatch-failure-wire107')
    projections = passed(ART / 'legacy-projections-final/results.json')
    require(len(projections['cases']) == 21 and sum(row['views'] for row in projections['cases']) == 84, 'Missing old console views')
    tree(ART / 'legacy-projections-final', 'legacy-projections')
    witnesses = passed(ART / 'witnesses-final/results.json')
    require(len(witnesses['checkpoints']) == 17, 'Missing readable connected witness')
    tree(ART / 'witnesses-final', 'witnesses')
    # Retain exact before/after denial and retry bytes, independently reconciling every pair.
    pairs = []
    for before in sorted((OUT / 'focused').rglob('*-before.ddsave')):
        after = before.with_name(before.name.replace('-before.ddsave', '-after.ddsave'))
        require(after.exists() and sha(before) == sha(after), 'Failed unchanged denial/retry pair: ' + str(before))
        pairs.append({'before': before.relative_to(OUT).as_posix(), 'after': after.relative_to(OUT).as_posix(), 'sha256': sha(before)})
    require(len(pairs) > 25, 'Missing retained rejection/retry evidence')
    summary = {'status': 'CHECKPOINT_ONLY_FULL_REGRESSION_INCOMPLETE' if args.checkpoint else 'EVIDENCE_READY_FOR_ACTUAL_FINAL_REVIEW', 'implementationCommit': COMMIT,
        'atUtc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'contractApproval': 'dbb657df-4133-556e-bccc-a389145b7916',
        'fullRegression': {'runId': launch['runId'], 'passed': len(all_results), 'required': len(names), 'failed': 0, 'predecessors': 1517,
            'newCases': focus, 'workers': processes, 'completedWorkers': completed_workers,
            'complete': not args.checkpoint and len(completed_workers) == len(GROUPS), 'originalJournalsAndMvidsVerified': True},
        'campaigns': campaigns, 'canonicalCheckpointComparisons': comparisons, 'authenticSaveContinuations': 21,
        'legacyConsoleViews': 84, 'unchangedDenialRetryPairs': pairs,
        'conditionPresentPostAdvancementCure': 'not demonstrated; explicitly accepted CHR-03 evidence scope',
        'unityIntegration': 'DEFERRED', 'wholeEngineCompletion': 'NOT COMPLETE'}
    (OUT / ('REGRESSION_CHECKPOINT.json' if args.checkpoint else 'RESULTS.json')).write_text(json.dumps(summary, indent=2) + '\n', encoding='utf-8')
    artifacts = {file.relative_to(OUT).as_posix(): {'bytes': file.stat().st_size, 'sha256': sha(file)}
        for file in sorted(OUT.rglob('*')) if file.is_file() and file.name != 'ARTIFACT_INDEX.json'}
    (OUT / 'ARTIFACT_INDEX.json').write_text(json.dumps({'artifacts': artifacts}, indent=2) + '\n', encoding='utf-8')
    print(('CHECKPOINT ONLY: observed ' + str(len(all_results)) + '/1524 original cases; ' if args.checkpoint else 'PASS: reconciled all1524 original cases,')
          + '85 canonical comparisons,21 authentic continuations,84 old views, '
          + str(len(pairs)) + ' unchanged pairs and ' + str(len(artifacts)) + ' retained artifacts')

if __name__ == '__main__':
    main()
