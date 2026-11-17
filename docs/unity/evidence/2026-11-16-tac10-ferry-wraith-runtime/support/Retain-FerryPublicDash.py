"""Retain the reviewed public Dash correction, focused run and genuine host continuation."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import zipfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
PACKET = HERE.parent
SOURCE = 'c8ffee78d5047131317ff923c8e3a575b6c51f3a'
AREA = ROOT / 'engine/artifacts/ferry-wraith/dash-correction'
BUILD = AREA / 'run-20261117T110451175Z-06a69ef8'
STATIC = AREA / 'static-20261117T110536604Z-a9b49cf2'
FAILED = [AREA / 'run-20261117T105724750Z-fe53700a', AREA / 'run-20261117T105808006Z-1ce97465']
OUT = PACKET / 'public-dash-checkpoint'


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def git(*args):
    return subprocess.check_output(['git', '-C', str(ROOT), *args])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--public-run', type=Path, required=True)
    args = parser.parse_args()
    branch = args.public_run.resolve()
    assert branch.is_relative_to(AREA.resolve())
    assert not git('diff', '--name-only', SOURCE, '--', 'engine'), 'Source changed after the corrected build.'
    compiled, static, actual = read(BUILD / 'results.json'), read(STATIC / 'results.json'), read(branch / 'RESULT.json')
    assert compiled['status'] == compiled['coreCompilation'] == static['status'] == 'PASS'
    assert compiled['language'] == 'C# 9' and compiled['testsDiscovered'] == compiled['passed'] == 1 and compiled['failed'] == 0
    assert compiled['cases'][0]['Name'] == 'tac10_ferry_public_dash_paid_movement_and_authorized_retry'
    assert len(compiled['sourceHashes']) == 468
    for inventory in (compiled['sourceHashes'], static['sourceHashes']):
        for row in inventory:
            path = ROOT / 'engine' / row['path'].replace('\\', '/')
            assert sha(path.read_bytes()) == row['sha256'], row['path']
    # The working engine matches SOURCE; prove the compile's source inventory against Git too.
    specs = [SOURCE + ':engine/' + row['path'].replace('\\', '/') for row in compiled['sourceHashes']]
    objects = subprocess.run(['git', '-C', str(ROOT), 'cat-file', '--batch'], input=('\n'.join(specs) + '\n').encode(), stdout=subprocess.PIPE, check=True).stdout
    offset = 0
    for row in compiled['sourceHashes']:
        end = objects.index(b'\n', offset)
        header = objects[offset:end].split()
        assert len(header) == 3 and header[1] == b'blob'
        length = int(header[2]); raw = objects[end + 1:end + 1 + length]
        assert sha(raw) == row['sha256'], row['path']
        offset = end + length + 2
    assert offset == len(objects)
    assert actual['status'] == 'PASS_GENUINE_PUBLIC_FERRY_DASH_GUIDANCE_AND_CLAW_OPPORTUNITY_ONLY'
    assert actual['sessionDashSupported'] is True
    assert actual['compilationReport']['sha256'] == sha((BUILD / 'results.json').read_bytes())
    assert actual['compilationReport']['testRunStatus'] == 'PASS'
    assert actual['input']['sha256'] == '6a69b36f95e4435705fb175030f7f16aebbfa76bb0752168af65f321d7ab2687'
    assert sha((branch / 'original-first-fire.ddsave').read_bytes()) == actual['input']['sha256']
    executed = branch / 'Probe-FerryGuidancePublic.executed.ps1'
    relative = (HERE / 'Probe-FerryGuidancePublic.ps1').relative_to(ROOT).as_posix()
    assert executed.read_bytes() == git('show', SOURCE + ':' + relative)
    assert sha(executed.read_bytes()) == actual['script']['sha256']
    assert len(actual['assemblies']) == 3
    for dll in actual['assemblies']:
        assert sha((BUILD / ('Decennium.Foundation.' + dll['name'] + '.dll')).read_bytes()) == dll['sha256']
    assert len(actual['commands']) == len(actual['expandedCommands']) == 24 and actual['finalRevision'] == 375
    assert [x['receipt']['Revision'] for x in actual['expandedCommands']] == list(range(352, 376))
    assert all(x.get('mode') != 'actual-typed-engine' and 'coreResult' not in x for x in actual['commands'])
    assert actual['sessionDashQuery']['Admissible'] and actual['sessionDashQuery']['Costs'] == [{'Kind': 'action', 'ResourceId': '', 'Amount': 1}]
    pairs = {}
    for restored in branch.glob('*-restored.ddsave'):
        original = restored.with_name(restored.name.replace('-restored.ddsave', '.ddsave'))
        assert original.read_bytes() == restored.read_bytes()
        pairs[original.name] = sha(original.read_bytes())
    assert len(pairs) == 6
    controls = read(BUILD / 'saves/public-dash-checks.json')
    assert len(controls['checks']) == 15 and controls['finalRevision'] == 375
    assert controls['spent'] == {'Numerator': 35, 'Denominator': 1}
    members = {}
    for label, directory in [('focused-build', BUILD), ('public-continuation', branch), ('static', STATIC)]:
        for path in sorted(directory.rglob('*')):
            if path.is_file():
                members[label + '/' + path.relative_to(directory).as_posix()] = path.read_bytes()
    failures = []
    for directory in FAILED:
        result = read(directory / 'results.json')
        assert result['status'] == 'FAIL' and result['error']
        source = directory / 'failed-FerryWraithCases.cs'
        inventory = result.get('sourceHashes') or read(directory / 'failed-source-hashes.json')
        match = next(row for row in inventory if row['path'].replace('\\', '/').endswith('/Tests/EditMode/FerryWraithCases.cs'))
        assert sha(source.read_bytes()) == match['sha256']
        failures.append(dict(run=directory.name, testsDiscovered=result['testsDiscovered'], passed=result['passed'], failed=result['failed'],
                             error=result.get('cases', [{}])[0].get('Error', result['error']) if result.get('cases') else result['error']))
        for path in sorted(directory.rglob('*')):
            if path.is_file() and path.suffix != '.dll':
                members['failed/' + directory.name + '/' + path.relative_to(directory).as_posix()] = path.read_bytes()
    members['support/Retain-FerryPublicDash.py'] = Path(__file__).read_bytes()
    members['references/GPT_SPELL_CONSUMERS_REVIEW.json'] = (PACKET / 'GPT_SPELL_CONSUMERS_REVIEW.json').read_bytes()
    manifest = [dict(path=name, bytes=len(raw), sha256=sha(raw)) for name, raw in sorted(members.items())]
    assert not OUT.exists(), 'Never overwrite retained evidence.'
    OUT.mkdir()
    output = OUT / 'public-dash.zip'
    with zipfile.ZipFile(output, 'x') as archive:
        for name, raw in sorted(members.items()):
            info = zipfile.ZipInfo(name, (2026, 11, 17, 0, 0, 0)); info.compress_type = zipfile.ZIP_DEFLATED; info.external_attr = 0o100644 << 16
            archive.writestr(info, raw)
    with zipfile.ZipFile(output) as archive:
        assert archive.namelist() == [row['path'] for row in manifest]
        for row in manifest:
            raw = archive.read(row['path']); assert len(raw) == row['bytes'] and sha(raw) == row['sha256']
    result = dict(status='PASS_PUBLIC_DASH_CHECKPOINT_NOT_MODULE_ACCEPTANCE', sourceCommit=SOURCE, compiledSourceInputs=468,
                  staticInputs=len(static['sourceHashes']), focusedCasesPassed=1, focusedNegativeControls=controls['checks'],
                  genuinePublicContinuationCommands=24, selectedRestorePairs=pairs, failedAttempts=failures,
                  archiveBytes=output.stat().st_size, archiveSha256=sha(output.read_bytes()), members=len(manifest),
                  scriptSha256=sha(Path(__file__).read_bytes()), moduleAccepted=False, fivePaths=False, correctedFullRegression=False,
                  note='Original db91 full1583 pass is separate. Condition/Strain boundary qualification, remaining module gates and actual correction/final review remain required.')
    (OUT / 'MEMBERS.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    (OUT / 'RETENTION.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({key: value for key, value in result.items() if key not in ('failedAttempts', 'selectedRestorePairs', 'focusedNegativeControls')}))


if __name__ == '__main__':
    main()
