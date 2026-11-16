"""Reconcile original completed Bishop qualification; never execute or replace workers."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[5]
MODES = {'ConsoleUninterrupted', 'ConsoleRestored', 'TypedUninterrupted', 'TypedRestored', 'ReceiptReplay'}
read = lambda p: json.loads(p.read_text(encoding='utf-8-sig'))
digest = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
lines = lambda p: p.read_text(encoding='utf-8-sig').splitlines()


def verify_assemblies(rows, expected):
    if isinstance(rows, list):
        rows = {x['name']: x for x in rows}
    assert set(rows) == {'Core', 'Persistence', 'LabModel'}
    for name, row in rows.items():
        assert row['sha256'] == expected['Decennium.Foundation.' + name + '.dll']


def queue_tree(members, root, prefix):
    for path in sorted(root.rglob('*')):
        if path.is_file() and path.suffix != '.dll':
            key = prefix + '/' + path.relative_to(root).as_posix()
            assert key not in members
            members[key] = path


def main():
    parser = argparse.ArgumentParser()
    for name in ('run', 'qualification', 'output', 'correction'):
        parser.add_argument('--' + name, required=True, type=Path)
    parser.add_argument('--source', required=True)
    args = parser.parse_args()
    run, qualification, output = (getattr(args, x).resolve() for x in ('run', 'qualification', 'output'))
    assert not output.exists(), 'Preserve prior qualification evidence'
    source_commit = args.source
    correction = args.correction.resolve()
    assert not subprocess.check_output(['git', 'diff', source_commit, '--', 'engine'], cwd=ROOT).strip()
    launch = read(run / 'launch.json')
    assert launch['sourceCommit'] == source_commit and launch['sourceCommitted']
    assert launch['requiredCount'] == 1570 and launch['retainedPredecessors'] == 1566
    compiled = read(run / 'compiled-source-report.json')
    assert compiled['status'] == 'PASS' and len(compiled['sourceHashes']) == 453
    assert digest(run / 'compiled-source-report.json') == launch['compiledSourceReportSha256']
    for row in compiled['sourceHashes']:
        assert digest(ROOT / 'engine' / row['path']) == row['sha256'], row['path']
    packet = Path(__file__).resolve().parents[1]
    static = read(correction / 'static-results.json')
    assert static['status'] == 'PASS' and all(row['passed'] for row in static['checks'])
    for row in static['sourceHashes']:
        assert digest(ROOT / 'engine' / row['path']) == row['sha256'], row['path']
    audit = read(correction / 'SOURCE_AUDIT.json')
    assert audit['status'] == 'PASS_SOURCE_ONLY' and audit['pinnedBlobs'] == 83
    retained = read(correction / 'RETENTION.json')
    for kind in ('assemblies', 'evidence'):
        index = retained[kind]
        archive = correction / index['path']
        assert digest(archive) == index['sha256'] and archive.stat().st_size == index['bytes']
        with zipfile.ZipFile(archive) as z:
            assert sorted(z.namelist()) == sorted(row['path'] for row in index['members'])
            for row in index['members']:
                data = z.read(row['path'])
                assert len(data) == row['bytes'] and hashlib.sha256(data).hexdigest() == row['sha256']
    for dll, expected in launch['assemblies'].items():
        assert digest(run / 'execution-assemblies' / dll) == expected
        assert next(x['sha256'] for x in retained['assemblies']['members'] if x['path'] == dll) == expected
    names = lines(run / 'all-names.txt')
    new = [x for x in names if x.startswith('chr03_bishop_')]
    prior = ROOT / 'docs/unity/evidence/2026-11-16-exp07-post-recovery/implementation/regression'
    assert len(names) == len(set(names)) == 1570 and len(new) == 4
    assert [x for x in names if x not in new] == lines(prior / 'all-names.txt')
    assert digest(run / 'all-names.txt') == launch['inventorySha256']
    workers = read(run / 'processes.json')
    assert {x['group'] for x in workers} == {'shardA', 'shardB', 'shardC', 'shardD', 'shardE', 'shardF'}
    assert len({x['pid'] for x in workers}) == 6
    completed, all_results = [], []
    for worker in workers:
        group = worker['group']
        assigned = lines(run / (group + '-names.txt'))
        assert [x for x in assigned if x not in new] == lines(prior / (group + '-names.txt'))
        assert digest(run / (group + '-names.txt')) == launch['assignments'][group]
        started, ending = (read(run / (group + suffix)) for suffix in ('.started.json', '.execution.json'))
        assert started['runId'] == ending['runId'] == launch['runId']
        assert started['pid'] == ending['pid'] == worker['pid']
        for field, expected in (('assignmentSha256', launch['assignments'][group]), ('inventorySha256', launch['inventorySha256'])):
            assert started[field] == ending[field] == expected
        assert started['assemblies'] == ending['assemblies']
        for dll, expected in launch['assemblies'].items():
            assert started['assemblies'][dll]['sha256'] == expected
        rows = [json.loads(x) for x in lines(run / (group + '.jsonl'))]
        assert [x['Name'] for x in rows] == assigned
        assert all(x['Passed'] and not x['Error'] for x in rows)
        assert len(rows) == ending['cases'] == worker['cases']
        assert digest(run / (group + '.jsonl')) == ending['journalSha256']
        assert lines(run / (group + '.done')) == ['DONE']
        all_results.extend(rows)
        completed.append(ending)
    assert len(all_results) == 1570 and {x['Name'] for x in all_results} == set(names)

    reference, paths = qualification / 'reference', qualification / 'paths'
    manifest, result = read(reference / 'manifest.json'), read(paths / 'results.json')
    assert manifest['status'] == 'PASS_REFERENCE' and manifest['revision'] == 457 and len(manifest['marks']) == 21
    assert result['status'] == 'PASS' and set(result['paths']) == MODES
    assert digest(reference / 'inputs.jsonl') == result['traceSha256']
    verify_assemblies(manifest['assemblies'], launch['assemblies'])
    verify_assemblies(result['assemblies'], launch['assemblies'])
    probe_count = 0
    for mark in manifest['marks']:
        expected = {mark['name']: mark['sha256'], mark['name'] + '.after-probes.ddsave': mark['sha256']}
        assert set(mark['views']) == {'Player', 'FirstOpponent', 'RecoveryOpponent'}
        expected.update({x['name']: x['sha256'] for x in mark['views'].values()})
        expected.update({x['request']['evidenceRead']: x['sha256'] for x in mark['probes']})
        probe_count += len(mark['probes'])
        for filename, sha in expected.items():
            assert digest(reference / filename) == sha, filename
            for mode in MODES:
                assert result['paths'][mode]['commands'] == 457
                assert digest(paths / mode / filename) == sha, (mode, filename)
                if not filename.endswith('.after-probes.ddsave'):
                    assert result['paths'][mode]['checkpoints'][filename] == sha
    assert digest(Path(manifest['finalSource'])) == manifest['finalSha256']

    compat_root = qualification / 'compatibility95-110'
    compat, bishop = read(compat_root / 'results.json'), read(compat_root / 'bishop-profile-results.json')
    assert compat['Status'] == 'PASS' and len(compat['Cases']) == 28
    assert bishop['status'] == 'PASS' and len(bishop['rejections']) == 28
    verify_assemblies(bishop['assemblies'], launch['assemblies'])
    assert digest(compat_root / 'results.json') == bishop['compatibilityReportSha256']
    assert digest(compat_root / 'bishop-before.ddsave') == bishop['beforeSha256']
    evidence = ROOT / 'docs/unity/evidence'
    for i, (case, rejected) in enumerate(zip(compat['Cases'], bishop['rejections'])):
        folder = compat_root / ('case-' + str(i) + '-wire' + str(case['Wire']))
        assert digest(evidence / case['Source']) == case['SourceSha256'] == case['RoundtripSha256'] == case['ContinuedSha256']
        assert digest(evidence / case['Earlier']) == case['EarlierSha256']
        assert digest(folder / 'roundtrip.ddsave') == digest(folder / 'continued.ddsave') == case['SourceSha256']
        assert case['Commands'] > 0 and case['ToRevision'] > case['FromRevision']
        assert rejected['source'] == case['Source'] and rejected['sourceSha256'] == case['SourceSha256']
        assert digest(compat_root / rejected['after']) == rejected['unchangedSha256'] == bishop['beforeSha256']
    legacy_root = qualification / 'legacy-projections'
    legacy = read(legacy_root / 'results.json')
    assert legacy['status'] == 'PASS' and len(legacy['cases']) == 28
    assert digest(ROOT / 'engine/tools/Open-ConnectedExpedition.ps1') == legacy['newConsoleSha256']
    assert digest(legacy_root / 'accepted-predecessor-console.ps1') == legacy['oldConsoleSha256']
    assert legacy['predecessorCommit'] == 'e0994929b444b15fc38957eb80cc34ab19d56db6'
    old_console = subprocess.check_output(['git', 'show', legacy['predecessorCommit'] + ':engine/tools/Open-ConnectedExpedition.ps1'], cwd=ROOT)
    assert old_console.decode('utf-8-sig').splitlines() == lines(legacy_root / 'accepted-predecessor-console.ps1')
    old_launch = read(evidence / '2026-11-15-mgt03-cleric-long-rest/implementation/regression/launch.json')
    for part in ('Core', 'Persistence', 'LabModel'):
        dll = 'Decennium.Foundation.' + part + '.dll'
        assert digest(legacy_root / 'accepted-predecessor-assemblies' / dll) == old_launch['assemblies'][dll]
    for i, case in enumerate(legacy['cases']):
        folder = legacy_root / ('case-' + str(i) + '-wire' + str(case['wire']))
        assert digest(folder / 'old.jsonl') == case['oldOutputSha256']
        assert digest(folder / 'new.jsonl') == case['newOutputSha256']
        a, b = ([json.loads(x) for x in lines(folder / filename)] for filename in ('old.jsonl', 'new.jsonl'))
        assert len(a) == len(b) == 5 and a[2]['Response'] == b[2]['Response'] == 'Restored'
        assert all(a[j] == b[j] for j in (0, 1, 3, 4))

    wire_root = qualification / 'wire111'
    wire = read(wire_root / 'results.json')
    assert wire['status'] == 'PASS' and wire['authenticCheckpoints'] == 13
    assert wire['actualContinuationCommandsPerRole'] == 330 and wire['comparedCanonicalAndViews'] == 100
    assert wire['newProfileRejections'] == 13
    verify_assemblies(wire['currentAssemblies'], launch['assemblies'])
    accepted111 = read(prior / 'launch.json')
    verify_assemblies(wire['oldAssemblies'], accepted111['assemblies'])
    assert digest(prior.parent / 'qualification-evidence.zip') == wire['sourceArchiveSha256']
    for part in ('Core', 'Persistence', 'LabModel', 'HeadlessTests'):
        dll = 'Decennium.Foundation.' + part + '.dll'
        assert digest(wire_root / 'accepted-assemblies' / dll) == accepted111['assemblies'][dll]
    for role in ('Accepted111', 'Current'):
        report = read(wire_root / role / 'results.json')
        assert report['status'] == 'PASS' and report['artifacts'] == wire['artifacts']
        for name, sha in report['artifacts'].items():
            assert digest(wire_root / role / name) == sha
    restores = qualification / 'restore-controls'
    restore = read(restores / 'results.json')
    assert restore['status'] == 'PASS' and len(restore['checks']) == 5
    verify_assemblies(restore['assemblies'], launch['assemblies'])
    retained_members = {row['path']: row for row in retained['evidence']['members']}
    assert restore['validSourceSha256'] == retained_members['focused/saves/invocation-cure.ddsave']['sha256']
    assert restore['forgedSourceSha256'] == retained_members['focused/saves/forged-invocation-healing.ddsave']['sha256']
    for name in ('live-before.ddsave', 'after-corrupt-rejections.ddsave', 'after-explicit-recovery.ddsave', 'after-forged-backup-rejection.ddsave'):
        assert digest(restores / name) == restore['canonicalLiveSha256']
    assert digest(restores / restore['displacedPrimary']) == restore['corruptPrimarySha256']

    members = {}
    queue_tree(members, qualification, 'qualification')
    comparison = run.parent / 'correction-canonical-comparison.json'
    unchanged = read(comparison)
    assert len(unchanged['rows']) == 29 and all(x['same'] and x['before'] == x['after'] for x in unchanged['rows'])
    for row in unchanged['rows']:
        assert digest(run / 'saves/chr03_bishop_connected_earned_funded_cure_aura_dispel_continue' / row['path']) == row['after']
    members['supplemental/correction-canonical-comparison.json'] = comparison
    for case in new:
        queue_tree(members, run / 'saves' / case, 'regression/saves/' + case)
    for path in run.iterdir():
        if path.is_file():
            members['regression/' + path.name] = path
    output.mkdir(parents=True)
    index = []
    archive = output / 'qualification-evidence.zip'
    with zipfile.ZipFile(archive, 'x', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for name, path in sorted(members.items()):
            data = path.read_bytes()
            z.writestr(name, data)
            index.append(dict(path=name, bytes=len(data), sha256=hashlib.sha256(data).hexdigest()))
    with zipfile.ZipFile(archive) as z:
        assert sorted(z.namelist()) == [x['path'] for x in index]
        for row in index:
            data = z.read(row['path'])
            assert len(data) == row['bytes'] and hashlib.sha256(data).hexdigest() == row['sha256']
    # Stable direct regression inventory supports the next dependency's exact assignments.
    (output / 'regression').mkdir()
    for path in run.iterdir():
        if path.is_file():
            shutil.copyfile(path, output / 'regression' / path.name)
    (output / 'QUALIFICATION_MEMBERS.json').write_text(json.dumps(dict(archive=archive.name, bytes=archive.stat().st_size,
        sha256=digest(archive), members=index), indent=2) + '\n', encoding='utf-8')
    summary = dict(status='QUALIFICATION_PASS_AWAITING_ACTUAL_FINAL_REVIEW', sourceCommit=source_commit,
        reconciledUtc=datetime.now(timezone.utc).isoformat(), runId=launch['runId'], passed=1570, failed=0,
        predecessors=1566, newCases=new, originalWorkers=completed, compiledInputs=453, staticInputs=len(static['sourceHashes']), sourcePins=83,
        campaign=dict(commands=457, checkpoints=21, paths=sorted(MODES), canonicalComparisons=105, filteredViewComparisons=315,
                      behaviorComparisons=5 * probe_count), authentic95Through110=dict(checkpoints=28, consoleViews=112, bishopRejections=28),
        authentic111=dict(checkpoints=13, commandsPerRole=330, canonicalAndViewComparisons=100, bishopRejections=13),
        restoreChecks=restore['checks'], archive=dict(path=archive.name, bytes=archive.stat().st_size, sha256=digest(archive), members=len(index)),
        note='Qualification supports this bounded module; actual GPT review and agreement remain required. No successor or Unity. Storage/Support held.')
    (output / 'FINAL_RECONCILIATION.json').write_text(json.dumps(summary, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in summary.items() if k != 'originalWorkers'}))


if __name__ == '__main__':
    main()
