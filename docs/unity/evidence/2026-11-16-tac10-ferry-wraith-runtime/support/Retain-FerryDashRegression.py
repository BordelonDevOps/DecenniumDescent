"""Reconcile the original frozen 1,584-case run; never restart or manufacture results."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import zipfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
PACKET = HERE.parent
RUN = ROOT / 'engine/artifacts/ferry-wraith/dash-regression-20261117T112529Z'
OUT = PACKET / 'dash-regression-checkpoint'
TREE = 'c8ffee78d5047131317ff923c8e3a575b6c51f3a'
PREVIOUS = ROOT / 'docs/unity/evidence/2026-11-16-tac03-declared-geometry-runtime/final/qualification-final.zip'
NEW = [
    'tac10_damage_order_preserves_source_save_flat_resistance_and_life',
    'tac10_ferry_numeric_origin_and_source_payload_roundtrip',
    'tac10_ferry_paid_current_epoch_admission_from_fresh_campaign',
    'tac10_ferry_public_dash_paid_movement_and_authorized_retry',
    'tac10_ferry_shared_untrained_checks_and_actual_initiative',
    'tac10_ferry_typed_defenses_settle_actual_life_mechanical',
    'tac10_petrified_poison_immunity_retains_event_condition_provenance',
    'tac10_seal_uses_owned_action_and_original_deadline',
]


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def lines(path):
    return path.read_text(encoding='utf-8-sig').splitlines()


def git(*args):
    return subprocess.check_output(['git', '-C', str(ROOT), *args])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check-only', action='store_true', help='Read-only reconciliation, including a still-running prefix.')
    args = parser.parse_args()
    launch = read(RUN / 'launch.json')
    assert launch['runId'] == '72f6bdda13924fad8eb5b516ec19018b'
    assert launch['engineTreeCommit'] == TREE and launch['sourceCommitted']
    current_diff = git('diff', '--name-only', TREE, '--', 'engine').decode('utf-8').splitlines()
    report_raw = (RUN / 'compiled-source-report.json').read_bytes()
    assert sha(report_raw) == launch['compiledSourceReportSha256']
    compiled = json.loads(report_raw)
    assert compiled['status'] == compiled['coreCompilation'] == 'PASS'
    assert compiled['language'] == 'C# 9' and len(compiled['sourceHashes']) == 468
    # Authenticate the originally compiled tree even after a reviewed correction changes HEAD.
    # Such a run remains valid only for TREE, never for the changed current engine.
    source_specs = [TREE + ':engine/' + row['path'].replace('\\', '/') for row in compiled['sourceHashes']]
    objects = subprocess.run(['git', '-C', str(ROOT), 'cat-file', '--batch'],
                             input=('\n'.join(source_specs) + '\n').encode('utf-8'),
                             stdout=subprocess.PIPE, check=True).stdout
    offset = 0
    for row in compiled['sourceHashes']:
        end = objects.index(b'\n', offset)
        header = objects[offset:end].split()
        assert len(header) == 3 and header[1] == b'blob'
        length = int(header[2])
        raw = objects[end + 1:end + 1 + length]
        assert sha(raw) == row['sha256'], row['path']
        offset = end + length + 2
    assert offset == len(objects)
    bindings = [
        ('Start-FerryDashRegression.executed.ps1', 'launcherSha256', HERE / 'Start-FerryDashRegression.ps1'),
        ('Run-ExactBishopShard.executed.ps1', 'runnerSha256', ROOT / 'docs/unity/evidence/2026-11-16-chr03-bishop-runtime/support/Run-ExactBishopShard.ps1'),
    ]
    for name, field, source in bindings:
        raw = (RUN / name).read_bytes()
        assert sha(raw) == launch[field]
        relative = source.relative_to(ROOT).as_posix()
        assert raw == source.read_bytes() == git('show', launch['sourceCommit'] + ':' + relative)
    seal = read(PACKET / 'public-dash-checkpoint/RETENTION.json')
    seal_path = PACKET / 'public-dash-checkpoint/public-dash.zip'
    assert sha(seal_path.read_bytes()) == seal['archiveSha256']
    with zipfile.ZipFile(seal_path) as archive:
        for name, digest in launch['assemblies'].items():
            assert sha((RUN / 'execution-assemblies' / name).read_bytes()) == digest
            assert sha(archive.read('focused-build/' + name)) == digest
    assert sha(PREVIOUS.read_bytes()) == launch['predecessorArchiveSha256']
    prior = {}
    with zipfile.ZipFile(PREVIOUS) as archive:
        for name, digest in launch['predecessorAssignments'].items():
            raw = archive.read('regression/' + name)
            assert sha(raw) == digest and raw == (RUN / 'authenticated-predecessor' / name).read_bytes()
            prior[name] = raw.decode('utf-8-sig').splitlines()
    names = lines(RUN / 'all-names.txt')
    assert sha((RUN / 'all-names.txt').read_bytes()) == launch['inventorySha256']
    assert len(names) == len(set(names)) == launch['requiredCount'] == 1584
    assert len(prior['all-names.txt']) == launch['retainedPredecessors'] == 1576
    assert lines(RUN / 'new-names.txt') == NEW and launch['newCases'] == 8
    assert [name for name in names if name not in NEW] == prior['all-names.txt']
    assert [name for name in names if name in NEW] == NEW
    workers = read(RUN / 'processes.json')
    groups = ['shard' + letter for letter in 'ABCDEF']
    assert [worker['group'] for worker in workers] == groups
    assert len({worker['pid'] for worker in workers}) == 6
    filter_text = ' OR '.join('ProcessId=' + str(int(worker['pid'])) for worker in workers)
    observation_raw = subprocess.check_output([
        'pwsh', '-NoLogo', '-NoProfile', '-Command',
        "$ErrorActionPreference='Stop'; @(Get-CimInstance Win32_Process -Filter '" + filter_text +
        "' | Select-Object ProcessId,CommandLine,CreationDate) | ConvertTo-Json -Depth 4 -Compress",
    ], text=True, encoding='utf-8-sig')
    processes = json.loads(observation_raw) if observation_raw.strip() else []
    if isinstance(processes, dict):
        processes = [processes]
    observation = dict(observedUtc=datetime.now(timezone.utc).isoformat(), requestedPids=[w['pid'] for w in workers], processes=processes)
    active = {p['ProcessId'] for p in processes}
    completed, rows_all, assigned_all, pending = [], [], [], []
    for index, worker in enumerate(workers):
        group = worker['group']
        assigned = lines(RUN / (group + '-names.txt'))
        assert assigned == NEW[index::6] + prior[group + '-names.txt']
        assert len(assigned) == worker['cases']
        assert sha((RUN / (group + '-names.txt')).read_bytes()) == launch['assignments'][group]
        started = read(RUN / (group + '.started.json'))
        assert started['runId'] == launch['runId'] and started['pid'] == worker['pid'] and started['group'] == group
        assert started['inventorySha256'] == launch['inventorySha256']
        assert started['assignmentSha256'] == launch['assignments'][group]
        for dll, digest in launch['assemblies'].items():
            assert started['assemblies'][dll]['sha256'] == digest and started['assemblies'][dll]['moduleId']
        assert started['assemblies'] == read(RUN / 'shardA.started.json')['assemblies']
        rows = [json.loads(line) for line in lines(RUN / (group + '.jsonl'))]
        assert [row['Name'] for row in rows] == assigned[:len(rows)]
        assert all(row['Passed'] is True and not row['Error'] for row in rows)
        assert not (RUN / (group + '.err')).read_bytes(), group + ' stderr is nonempty'
        ending_path = RUN / (group + '.execution.json')
        if ending_path.exists():
            ending = read(ending_path)
            assert all(ending[key] == value for key, value in started.items())
            assert len(rows) == ending['cases'] == len(assigned)
            assert sha((RUN / (group + '.jsonl')).read_bytes()) == ending['journalSha256']
            assert lines(RUN / (group + '.done')) == ['DONE']
            assert worker['pid'] not in active, 'Terminal worker is still present; re-observe after exit.'
            completed.append(ending)
        else:
            assert not (RUN / (group + '.done')).exists()
            match = next((p for p in processes if p['ProcessId'] == worker['pid']), None)
            assert match and str(RUN) in match['CommandLine'] and '-Group ' + group in match['CommandLine'], 'Incomplete worker is absent or changed.'
            pending.append(dict(group=group, pid=worker['pid'], completed=len(rows), required=len(assigned)))
        rows_all.extend(rows)
        assigned_all.extend(assigned)
    assert len(assigned_all) == len(set(assigned_all)) == 1584 and set(assigned_all) == set(names)
    summary = dict(status='IN_PROGRESS' if pending else 'PASS_FULL_REGRESSION_NOT_MODULE_ACCEPTANCE',
                   runId=launch['runId'], engineTreeCommit=TREE, launcherSourceCommit=launch['sourceCommit'],
                   passed=len(rows_all), failed=0, required=1584, predecessors=1576, newCases=NEW,
                   compiledSourceInputs=468, currentEngineMatchesFrozenTree=not current_diff,
                   currentEngineDifferences=current_diff, originalWorkersCompleted=len(completed), pending=pending,
                   processObservation=observation, moduleAccepted=False, fivePaths=False)
    if args.check_only:
        print(json.dumps(summary))
        return
    assert not pending and len(rows_all) == 1584, 'Keep the original run alive; final retention requires every terminal worker.'
    assert not OUT.exists(), 'Never overwrite a retained qualification packet.'
    members = {}
    for path in RUN.iterdir():
        if path.is_file():
            members['regression/' + path.name] = path.read_bytes()
    for path in (RUN / 'authenticated-predecessor').iterdir():
        members['regression/authenticated-predecessor/' + path.name] = path.read_bytes()
    case_artifacts = []
    for case in NEW:
        directory = RUN / 'saves' / case
        paths = sorted(path for path in directory.rglob('*') if path.is_file())
        assert paths, 'Every selected new case currently writes evidence: ' + case
        case_artifacts.append(dict(name=case, files=len(paths)))
        for path in paths:
            members['regression/saves/' + case + '/' + path.relative_to(directory).as_posix()] = path.read_bytes()
    members['process-observation.json'] = (json.dumps(observation, indent=2) + '\n').encode('utf-8')
    members['support/Retain-FerryDashRegression.py'] = Path(__file__).read_bytes()
    for name in ('public-dash-checkpoint/RETENTION.json', 'public-dash-checkpoint/MEMBERS.json'):
        members['references/' + name] = (PACKET / name).read_bytes()
    manifest = [dict(path=name, bytes=len(raw), sha256=sha(raw)) for name, raw in sorted(members.items())]
    OUT.mkdir()
    output = OUT / 'full-regression.zip'
    with zipfile.ZipFile(output, 'x') as archive:
        for name, raw in sorted(members.items()):
            info = zipfile.ZipInfo(name, (2026, 11, 17, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, raw)
    with zipfile.ZipFile(output) as archive:
        assert archive.namelist() == [row['path'] for row in manifest]
        for row in manifest:
            raw = archive.read(row['path'])
            assert len(raw) == row['bytes'] and sha(raw) == row['sha256']
    summary.update(originalWorkers=completed, newCaseArtifacts=case_artifacts, members=len(manifest),
                   archiveBytes=output.stat().st_size, archiveSha256=sha(output.read_bytes()),
                   scriptSha256=sha(Path(__file__).read_bytes()),
                   retentionScope='All original journals, terminal identities and launch bindings; all eight new case artifact trees. Original predecessor case artifact trees remain local, not duplicated here. Frozen DLLs authenticated against the retained public Dash archive.')
    (OUT / 'MEMBERS.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    (OUT / 'RETENTION.json').write_text(json.dumps(summary, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({key: value for key, value in summary.items() if key not in ('originalWorkers', 'processObservation')}))


if __name__ == '__main__':
    main()
