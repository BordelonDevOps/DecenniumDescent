"""Retain actual source Press and knockout continuations and the corrected regression launch."""
import hashlib
import json
from pathlib import Path
import subprocess
from datetime import datetime, timezone
import zipfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
PACKET = HERE.parent
AREA = ROOT / 'engine/artifacts/ferry-wraith/dash-correction'
PRESS = AREA / 'press-20261117T112218Z'
KNOCKOUT = AREA / 'knockout-20261117T112218Z'
BUILD = AREA / 'run-20261117T110451175Z-06a69ef8'
REGRESSION = ROOT / 'engine/artifacts/ferry-wraith/dash-regression-20261117T112529Z'
RUNTIME = 'c8ffee78d5047131317ff923c8e3a575b6c51f3a'
DRIVER = '6fcad393427fa1376b0c26f70ce21cd4d2d8003a'
OUT = PACKET / 'press-knockout-checkpoint'


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def reconcile(commands, expanded, first, last):
    assert len(commands) == len(expanded) == last - first
    assert [row['receipt']['Revision'] for row in expanded] == list(range(first + 1, last + 1))
    for row in expanded:
        assert row['command']['Id'] == row['receipt']['Id']
        assert row['command']['ExpectedRevision'] == row['receipt']['Revision'] - 1


def main():
    assert not subprocess.check_output(['git', '-C', str(ROOT), 'diff', '--name-only', RUNTIME, '--', 'engine'])
    press, knockout = read(PRESS / 'RESULT.json'), read(KNOCKOUT / 'RESULT.json')
    assert press['status'] == 'PASS_GENUINE_FERRY_PRESS_ONLY' and knockout['status'] == 'PASS_GENUINE_FERRY_KNOCKOUT_ONLY'
    original_driver = subprocess.check_output(['git', '-C', str(ROOT), 'show', DRIVER + ':' + (HERE / 'Probe-FerryPressKnockout.ps1').relative_to(ROOT).as_posix()])
    compiled = (BUILD / 'results.json').read_bytes()
    passing = json.loads(compiled)
    assert passing['status'] == passing['coreCompilation'] == 'PASS' and len(passing['sourceHashes']) == 468
    for row in passing['sourceHashes']:
        assert sha((ROOT / 'engine' / row['path'].replace('\\', '/')).read_bytes()) == row['sha256']
    prior = read(PACKET / 'public-dash-checkpoint/RETENTION.json')
    prior_archive = PACKET / 'public-dash-checkpoint/public-dash.zip'
    assert sha(prior_archive.read_bytes()) == prior['archiveSha256']
    with zipfile.ZipFile(prior_archive) as archive:
        assert archive.read('focused-build/results.json') == compiled
        for branch, report in [(PRESS, press), (KNOCKOUT, knockout)]:
            assert (branch / 'Probe-FerryPressKnockout.executed.ps1').read_bytes() == original_driver
            assert report['script']['sha256'] == sha(original_driver)
            assert report['compilationReport']['sha256'] == sha(compiled)
            assert report['input']['sha256'] == sha((branch / 'original-first-fire.ddsave').read_bytes()) == '6a69b36f95e4435705fb175030f7f16aebbfa76bb0752168af65f321d7ab2687'
            for dll in report['assemblies']:
                name = 'Decennium.Foundation.' + dll['name'] + '.dll'
                assert dll['sha256'] == sha((BUILD / name).read_bytes()) == sha(archive.read('focused-build/' + name))
    reconcile(press['commands'], press['expandedCommands'], 351, 366)
    assert press['armed']['ArmedRevision'] == 358 and press['armed']['ExpiresAt'] == press['finalClock']
    assert press['beforeInterval'] == press['afterInterval']
    follow = press['followMove']
    assert (follow['FromX'], follow['FromY'], follow['ToX'], follow['ToY'], follow['Kind'], follow['Status']) == (9, 1, 8, 2, 1, 1)
    assert press['choiceQuery']['Supported'] is False and press['choiceDiscovery'] == []
    reconcile(knockout['commands'], knockout['prefixExpandedCommands'], 351, 393)
    pending, damage = knockout['pendingAttack'], knockout['pendingDamage']
    assert pending['Id'] == damage['EventId'] == 'attack.393' and pending['Pending']
    assert damage['Raw'] == damage['Effective'] == pending['Damage']['Total'] == 4 and knockout['beforeLife']['Hp'] == 3
    assert pending['Damage']['WoundNatural'] == 4 and pending['Damage']['InjuryD6'] == 2
    assert [branch['choice'] for branch in knockout['branches']] == [False, True]
    for branch in knockout['branches']:
        reconcile(branch['commands'], branch['expandedCommands'], 393, 397)
        assert branch['resolved']['ResolvedRevision'] == 394 and not branch['resolved']['Pending']
        assert branch['resolved']['Attack'] == pending['Attack']
        assert branch['resolved']['Damage']['Total'] == pending['Damage']['Total']
        assert branch['life']['Hp'] == 0 and not branch['life']['Dead'] and branch['life']['Stable'] == branch['choice']
        assert branch['query']['Supported'] is False
    ordinary, stable = knockout['branches']
    assert ordinary['afterRandom'] == pending['Damage']['FinalRandom'] == 4126952768
    assert ordinary['continuedLife']['DeathFailures'] == 1 and ordinary['finalRandom'] == 4141489706
    assert stable['resolved']['Damage']['StableD4'] == 2
    assert stable['life']['StableUntil'] == {'Numerator': 358545, 'Denominator': 2}
    assert stable['afterRandom'] == stable['finalRandom'] == 4141489706 and stable['continuedLife']['DeathFailures'] == 0
    members, pairs = {}, {}
    for label, directory in [('press', PRESS), ('knockout', KNOCKOUT)]:
        for path in sorted(directory.rglob('*')):
            if path.is_file():
                members['executed/' + label + '/' + path.relative_to(directory).as_posix()] = path.read_bytes()
        for restored in directory.glob('*-restored.ddsave'):
            original = restored.with_name(restored.name.replace('-restored.ddsave', '.ddsave'))
            assert original.read_bytes() == restored.read_bytes()
            pairs[label + '/' + original.name] = sha(original.read_bytes())
    assert len(pairs) == 9
    launch, workers = read(REGRESSION / 'launch.json'), read(REGRESSION / 'processes.json')
    assert launch['runId'] == '72f6bdda13924fad8eb5b516ec19018b' and launch['engineTreeCommit'] == RUNTIME
    assert launch['requiredCount'] == 1584 and launch['retainedPredecessors'] == 1576 and launch['newCases'] == 8
    assert sha((REGRESSION / 'compiled-source-report.json').read_bytes()) == launch['compiledSourceReportSha256'] == sha(compiled)
    for dll, digest in launch['assemblies'].items():
        assert sha((REGRESSION / 'execution-assemblies' / dll).read_bytes()) == sha((BUILD / dll).read_bytes()) == digest
    filter_text = ' OR '.join('ProcessId=' + str(int(worker['pid'])) for worker in workers)
    raw = subprocess.check_output(['pwsh', '-NoProfile', '-Command',
        "@(Get-CimInstance Win32_Process -Filter '" + filter_text + "' | Select-Object ProcessId,CommandLine,CreationDate) | ConvertTo-Json -Depth 4 -Compress"], text=True, encoding='utf-8-sig')
    processes = json.loads(raw)
    assert len(processes) == 6
    for worker in workers:
        process = next(p for p in processes if p['ProcessId'] == worker['pid'])
        assert str(REGRESSION) in process['CommandLine'] and '-Group ' + worker['group'] in process['CommandLine']
        started = read(REGRESSION / (worker['group'] + '.started.json'))
        assert started['runId'] == launch['runId'] and started['pid'] == worker['pid']
        assert started['assignmentSha256'] == launch['assignments'][worker['group']]
        for dll, digest in launch['assemblies'].items():
            assert started['assemblies'][dll]['sha256'] == digest
    observation = dict(observedUtc=datetime.now(timezone.utc).isoformat(), processes=processes, scope='Original corrected workers observed live; not terminal qualification.')
    for path in REGRESSION.iterdir():
        if path.is_file() and (path.suffix in ('.json', '.ps1') or path.name.endswith('-names.txt')):
            members['regression-launch/' + path.name] = path.read_bytes()
    members['regression-launch/process-observation.json'] = (json.dumps(observation, indent=2) + '\n').encode()
    members['support/Retain-FerryPressKnockout.py'] = Path(__file__).read_bytes()
    members['references/public-dash-RETENTION.json'] = (PACKET / 'public-dash-checkpoint/RETENTION.json').read_bytes()
    members['references/GPT_PUBLIC_DASH_REVIEW.json'] = (PACKET / 'GPT_PUBLIC_DASH_REVIEW.json').read_bytes()
    manifest = [dict(path=name, bytes=len(raw), sha256=sha(raw)) for name, raw in sorted(members.items())]
    assert not OUT.exists()
    OUT.mkdir()
    output = OUT / 'press-knockout.zip'
    with zipfile.ZipFile(output, 'x') as archive:
        for name, raw in sorted(members.items()):
            info = zipfile.ZipInfo(name, (2026, 11, 17, 0, 0, 0)); info.compress_type = zipfile.ZIP_DEFLATED; info.external_attr = 0o100644 << 16
            archive.writestr(info, raw)
    with zipfile.ZipFile(output) as archive:
        assert archive.namelist() == [row['path'] for row in manifest]
        for row in manifest:
            raw = archive.read(row['path']); assert len(raw) == row['bytes'] and sha(raw) == row['sha256']
    result = dict(status='PASS_GENUINE_PRESS_KNOCKOUT_NOT_MODULE_ACCEPTANCE', runtimeCommit=RUNTIME, driverCommit=DRIVER,
                  compiledSourceInputs=468, additionalCompilation=False, pressCommands=15, knockoutPrefixCommands=42,
                  knockoutResolutionCommandsPerBranch=4, actualAlternateCommands=65, selectedRestorePairs=pairs,
                  unsupportedPublicQueries=['RespondPress', 'ResolveKnockout'], pressDiscoveryCandidates=0,
                  correctedRegression=dict(runId=launch['runId'], directory=str(REGRESSION), sourceCommit=launch['sourceCommit'], required=1584, originalWorkers=workers, terminal=False),
                  archiveBytes=output.stat().st_size, archiveSha256=sha(output.read_bytes()), members=len(manifest),
                  scriptSha256=sha(Path(__file__).read_bytes()), moduleAccepted=False, fivePaths=False)
    (OUT / 'MEMBERS.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    (OUT / 'RETENTION.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({key: value for key, value in result.items() if key not in ('selectedRestorePairs', 'correctedRegression')}))


if __name__ == '__main__':
    main()
