"""Reconcile final EXP-07 evidence without rerunning or replacing any worker."""
import argparse
from datetime import datetime, timezone
import importlib.util
import json
from pathlib import Path
import subprocess

SUPPORT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('checkpoint', SUPPORT / 'Retain-ExecutionCheckpoint.py')
q = importlib.util.module_from_spec(spec)
spec.loader.exec_module(q)
MODES = {'ConsoleUninterrupted', 'ConsoleRestored', 'TypedUninterrupted', 'TypedRestored', 'ReceiptReplay'}
CAMPAIGNS = {'main', 'grounding', 'mistimed', 'reaction', 'old-effects', 'sanctuary', 'purify',
             'detect', 'casualty', 'fear', 'carried-action', 'director-tie', 'player-tie'}


def lines(path):
    return path.read_text(encoding='utf-8-sig').splitlines()


def main():
    parser = argparse.ArgumentParser()
    for name in ('qualification', 'output'):
        parser.add_argument('--' + name, type=Path, required=True)
    args = parser.parse_args()
    qualification, output = q.longpath(args.qualification), q.longpath(args.output)
    assert not subprocess.check_output(['git', 'diff', q.SOURCE, '--', 'engine'], cwd=q.ROOT).strip()
    old_index = q.read(output / 'CHECKPOINT_ARTIFACT_INDEX.json')
    for entry in old_index['artifacts']:
        path = output / entry['path']
        assert path.stat().st_size == entry['bytes'] and q.digest(path) == entry['sha256'], path
    source = q.read(output / 'SOURCE_AUDIT.json')
    assert source['status'] == 'PASS' and source['implementationCommit'] == q.SOURCE
    for field in ('sourceArchive', 'binaryArchive'):
        entry = source[field]
        assert q.digest(output / entry['path']) == entry['sha256']

    run = qualification / 'regression-01'
    retained_prefix = output / 'execution-checkpoint-01/original-regression-prefix'
    for name in ('launch.json', 'processes.json', 'all-names.txt', 'compiled-source-report.json'):
        assert q.digest(run / name) == q.digest(retained_prefix / name), name
    launch = q.read(run / 'launch.json')
    workers = q.read(run / 'processes.json')
    assert len(workers) == 6 and {worker['group'] for worker in workers} == {
        'shardA', 'shardB', 'shardC', 'shardD', 'shardE', 'shardF'}
    assert len({worker['pid'] for worker in workers}) == 6
    assert launch['sourceCommit'] == q.SOURCE and launch['sourceCommitted']
    assert launch['requiredCount'] == 1566 and launch['retainedPredecessors'] == 1553
    assert q.digest(run / 'all-names.txt') == launch['inventorySha256']
    assert q.digest(run / 'compiled-source-report.json') == source['buildReportSha256']
    names = lines(run / 'all-names.txt')
    new_names = [name for name in names if name.startswith('exp07_post_recovery_')]
    prior = q.longpath(q.ROOT / 'docs/unity/evidence/2026-11-15-mgt03-cleric-long-rest/implementation/regression')
    assert len(names) == 1566 and len(new_names) == 13
    assert [name for name in names if name not in new_names] == lines(prior / 'all-names.txt')
    completed, all_rows = [], []
    for worker in workers:
        group = worker['group']
        assigned = lines(run / (group + '-names.txt'))
        assert [name for name in assigned if name not in new_names] == lines(prior / (group + '-names.txt'))
        assert q.digest(run / (group + '-names.txt')) == launch['assignments'][group]
        started = q.read(run / (group + '.started.json'))
        assert q.digest(run / (group + '.started.json')) == q.digest(retained_prefix / (group + '.started.json'))
        assert (run / (group + '.jsonl')).read_bytes().startswith((retained_prefix / (group + '.jsonl')).read_bytes())
        ending = q.read(run / (group + '.execution.json'))
        rows = [json.loads(line) for line in lines(run / (group + '.jsonl'))]
        assert lines(run / (group + '.done')) == ['DONE']
        assert started['runId'] == ending['runId'] == launch['runId']
        assert started['pid'] == ending['pid'] == worker['pid']
        assert started['assignmentSha256'] == ending['assignmentSha256'] == launch['assignments'][group]
        assert started['inventorySha256'] == ending['inventorySha256'] == launch['inventorySha256']
        assert started['assemblies'] == ending['assemblies']
        for name, expected in launch['assemblies'].items():
            assert started['assemblies'][name]['sha256'] == expected
            assert q.digest(run / 'execution-assemblies' / name) == expected
        assert len(rows) == worker['cases'] == ending['cases']
        assert [row['Name'] for row in rows] == assigned
        assert all(row['Passed'] and not row['Error'] for row in rows)
        assert ending['journalSha256'] == q.digest(run / (group + '.jsonl'))
        for suffix in ('-names.txt', '.started.json', '.execution.json', '.done', '.jsonl', '.out', '.err'):
            q.copy(run / (group + suffix), output / 'regression' / (group + suffix))
        all_rows.extend(rows)
        completed.append(ending)
    assert len(all_rows) == 1566 and {row['Name'] for row in all_rows} == set(names)
    for name in ('launch.json', 'processes.json', 'all-names.txt', 'compiled-source-report.json'):
        q.copy(run / name, output / 'regression' / name)

    matched_focused_files = []
    focused_root = output / 'focused'
    for path in sorted(focused_root.rglob('*')):
        if path.is_file():
            relative = path.relative_to(focused_root)
            assert relative.parts[0] in new_names
            assert q.digest(path) == q.digest(run / 'saves' / relative), relative
            matched_focused_files.append(dict(path=relative.as_posix(), sha256=q.digest(path)))
    assert len(matched_focused_files) == 130

    campaigns = []
    for group in (1, 2):
        root = qualification / ('campaign-paths-' + str(group))
        report = q.read(root / 'results.json')
        assert report['status'] == 'PASS'
        for completed_campaign in report['campaigns']:
            name = completed_campaign['name']
            folder = root / name
            result = q.read(folder / 'paths/results.json')
            manifest = q.read(folder / 'trace/manifest.json')
            assert result['status'] == 'PASS' and set(result['paths']) == MODES
            assert q.digest(folder / 'trace/inputs.jsonl') == result['traceSha256']
            for assembly in result['assemblies']:
                assert launch['assemblies']['Decennium.Foundation.' + assembly['name'] + '.dll'] == assembly['sha256']
            probe_count = 0
            for mark in manifest['marks']:
                assert q.digest(folder / 'trace/reference' / mark['name']) == mark['sha256']
                assert set(mark['views']) == {'Player', 'FirstOpponent', 'RecoveryOpponent'}
                probe_count += len(mark['probes'])
                for mode in MODES:
                    mode_folder = folder / 'paths' / mode
                    details = result['paths'][mode]
                    assert details['commands'] == manifest['revision']
                    assert q.digest(mode_folder / mark['name']) == mark['sha256'] == details['checkpoints'][mark['name']]
                    assert q.digest(mode_folder / (mark['name'] + '.after-probes.ddsave')) == mark['sha256']
                    for view in mark['views'].values():
                        assert q.digest(mode_folder / view['name']) == view['sha256'] == details['checkpoints'][view['name']]
                    for probe in mark['probes']:
                        target = probe['request']['evidenceRead']
                        assert q.digest(mode_folder / target) == probe['sha256'] == details['checkpoints'][target]
            final_source = q.longpath(manifest['finalSource'])
            assert q.digest(final_source) == manifest['finalSha256']
            retained_source = output / 'focused' / final_source.relative_to(qualification / 'focused-01/saves')
            assert q.digest(retained_source) == manifest['finalSha256']
            q.tree(folder, output / 'qualification/campaigns' / name)
            campaigns.append(dict(name=name, commands=manifest['revision'], checkpoints=len(manifest['marks']),
                                  paths=sorted(MODES), canonicalComparisons=5 * len(manifest['marks']),
                                  filteredViewComparisons=15 * len(manifest['marks']), behaviorComparisons=5 * probe_count,
                                  retainedFinalSource=retained_source.relative_to(output).as_posix(),
                                  finalSha256=manifest['finalSha256']))
    assert len(campaigns) == len(CAMPAIGNS) and {row['name'] for row in campaigns} == CAMPAIGNS

    compat = q.read(qualification / 'compatibility/results.json')
    assert compat['Status'] == 'PASS' and len(compat['Cases']) == 28 and compat['NewProfileRejections'] == 28
    evidence = q.longpath(q.ROOT / 'docs/unity/evidence')
    for index, case in enumerate(compat['Cases']):
        folder = qualification / 'compatibility' / ('case-' + str(index) + '-wire' + str(case['Wire']))
        assert case['Commands'] > 0 and case['FromRevision'] < case['ToRevision']
        assert q.digest(evidence / case['Source']) == case['SourceSha256']
        assert q.digest(evidence / case['Earlier']) == case['EarlierSha256']
        assert q.digest(folder / 'roundtrip.ddsave') == case['SourceSha256'] == case['RoundtripSha256']
        assert q.digest(folder / 'continued.ddsave') == case['SourceSha256'] == case['ContinuedSha256']
    assert q.digest(qualification / 'compatibility/new-before.ddsave') == compat['UnchangedNewStateSha256']
    assert q.digest(qualification / 'compatibility/new-after.ddsave') == compat['UnchangedNewStateSha256']
    legacy = q.read(qualification / 'legacy-projections/results.json')
    assert legacy['status'] == 'PASS' and len(legacy['cases']) == 28
    assert legacy['predecessorCommit'] == 'e0994929b444b15fc38957eb80cc34ab19d56db6'
    legacy_root = qualification / 'legacy-projections'
    assert q.digest(legacy_root / 'accepted-predecessor-console.ps1') == legacy['oldConsoleSha256']
    assert q.digest(q.ROOT / 'engine/tools/Open-ConnectedExpedition.ps1') == legacy['newConsoleSha256']
    old_launch = q.read(prior / 'launch.json')
    for part in ('Core', 'Persistence', 'LabModel'):
        assembly = 'Decennium.Foundation.' + part + '.dll'
        assert q.digest(legacy_root / 'accepted-predecessor-assemblies' / assembly) == old_launch['assemblies'][assembly]
    for index, case in enumerate(legacy['cases']):
        folder = qualification / 'legacy-projections' / ('case-' + str(index) + '-wire' + str(case['wire']))
        assert case['views'] == 4
        assert q.digest(folder / 'old.jsonl') == case['oldOutputSha256']
        assert q.digest(folder / 'new.jsonl') == case['newOutputSha256']
        old, new = ([json.loads(line) for line in lines(folder / name)] for name in ('old.jsonl', 'new.jsonl'))
        assert len(old) == len(new) == 5 and old[2]['Response'] == new[2]['Response'] == 'Restored'
        assert all(old[index] == new[index] for index in (0, 1, 3, 4))
    q.tree(qualification / 'compatibility', output / 'qualification/compatibility')
    q.tree(qualification / 'legacy-projections', output / 'qualification/legacy-projections')
    result = dict(status='QUALIFICATION_COMPLETE_AWAITING_ACTUAL_FINAL_REVIEW', implementationCommit=q.SOURCE,
                  capturedUtc=datetime.now(timezone.utc).isoformat(), runId=launch['runId'], passed=1566, failed=0,
                  preservedPredecessors=1553, newCases=13, originalWorkerCompletions=completed,
                  originalRunMatchesFocusedFiles=matched_focused_files,
                  campaigns=campaigns, canonicalComparisons=sum(x['canonicalComparisons'] for x in campaigns),
                  filteredViewComparisons=sum(x['filteredViewComparisons'] for x in campaigns),
                  behaviorComparisons=sum(x['behaviorComparisons'] for x in campaigns),
                  authenticSaveContinuations=28, exactLegacyViews=112,
                  unchangedCheckpointArtifacts=len(old_index['artifacts']),
                  scope='Source-bound provisional TEST_ONLY C# simulation qualification; actual GPT final review and Codex agreement still required. '
                        'After this module, stop for owner review before storage work or a successor. No Unity or whole-engine completion claim.')
    q.write(output / 'RESULTS.json', result)
    entries = [dict(path=path.relative_to(output).as_posix(), bytes=path.stat().st_size, sha256=q.digest(path))
               for path in sorted(output.rglob('*')) if path.is_file() and path.name != 'ARTIFACT_INDEX.json']
    q.write(output / 'ARTIFACT_INDEX.json', dict(status='RECONCILED_FINAL_QUALIFICATION', artifacts=entries))
    print(json.dumps(dict(status=result['status'], passed=1566, campaigns=len(campaigns), artifacts=len(entries)), separators=(',', ':')))


if __name__ == '__main__':
    main()
