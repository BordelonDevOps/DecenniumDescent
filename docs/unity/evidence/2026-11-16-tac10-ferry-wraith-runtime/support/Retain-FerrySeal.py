"""Retain genuine seal gameplay and separately labeled owned-Action/timing controls."""
import hashlib
import io
import json
from pathlib import Path
import subprocess
import zipfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
RUNTIME = '948b9bff0604e15cfb2d5419be9658392bcb2bcf'
SOURCE = 'db91c9ce8711be802674762d458bca9782207833'
BASE = 'aba482bf6d3cfe21f0dd063c738326039868154c'
DEV = ROOT / 'engine/artifacts/ferry-wraith/development'
PACKET = 'docs/unity/evidence/2026-11-16-tac10-ferry-wraith-runtime/'
OUT = HERE.parent / 'seal-checkpoint'


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def frozen(revision):
    return zipfile.ZipFile(io.BytesIO(subprocess.check_output(['git', 'archive', '--format=zip', revision,
        '--', 'engine', PACKET + 'support/Probe-FerrySeal.ps1', PACKET + 'GPT_CORRECTION_REVIEW.json'], cwd=ROOT)))


def main():
    assert not OUT.exists(), 'Do not overwrite retained evidence.'
    runtime, selected = frozen(RUNTIME), frozen(SOURCE)
    first = DEV / 'run-20261117T073647247Z-a5ad9f14'
    final = DEV / 'run-20261117T074505435Z-4c6b09f4'
    static = ROOT / 'engine/artifacts/static-20261117T074621737Z-b872a082'
    failed_static = ROOT / 'engine/artifacts/static-20261117T074424570Z-03a03746'
    failed_compile = DEV / 'run-20261117T074326253Z-f32538a9'
    probe = DEV / 'seal-probe-20261117T0742Z'
    failed_probe = DEV / 'seal-probe-20261117T0740Z'
    for directory, source, count in [(first, runtime, 468), (final, selected, 468), (static, selected, 977)]:
        report = read(directory / 'results.json')
        assert report['status'] == 'PASS' and len(report['sourceHashes']) == count
        if directory != static:
            assert report['passed'] == 1 and report['failed'] == 0
        for row in report['sourceHashes']:
            assert digest(source.read('engine/' + row['path'].replace('\\', '/'))) == row['sha256'], row['path']
    assert subprocess.check_output(['git', 'diff', RUNTIME, SOURCE, '--name-only'], cwd=ROOT).decode().splitlines() == [
        'engine/com.decennium.foundation/Tests/EditMode/FerryWraithCases.cs']
    controls = read(final / 'saves/seal-mechanical-controls.json')
    assert len(controls['rows']) == 4
    for row in controls['rows']:
        assert row['beforeRng'] == row['afterRng'] and row['expired'] > row['rupture']['Revision']
    p = read(probe / 'RESULT.json')
    assert p['status'] == 'PASS_GENUINE_SEAL_SUPPRESSION_RECOVERED_CLAW_ONLY'
    assert len(p['commands']) == 14 and p['finalRevision'] == 365 and p['rupture']['Revision'] == 354
    assert p['suppressedControllerSteps'] == 2 and p['recoveredAttack']['Attack']['Hit']
    assert p['compilationReport']['sha256'] == digest((first / 'results.json').read_bytes())
    for row in p['assemblies']:
        assert row['sha256'] == digest((first / ('Decennium.Foundation.' + row['name'] + '.dll')).read_bytes())
    assert p['script']['sha256'] == digest(runtime.read(PACKET + 'support/Probe-FerrySeal.ps1'))
    assert (probe / 'Probe-FerrySeal.executed.ps1').read_bytes() == runtime.read(PACKET + 'support/Probe-FerrySeal.ps1')
    predecessor = read(HERE.parent / 'provenance-checkpoint/RETENTION.json')['checkpoints'][1]['finalSaveSha256']
    assert p['firstFireSource']['sha256'] == predecessor
    assert (probe / 'original-first-fire.ddsave').read_bytes() == (probe / 'verified-current-first-fire.ddsave').read_bytes()
    assert digest((probe / 'original-first-fire.ddsave').read_bytes()) == predecessor
    for name in ['suppressed', 'recovered-claw']:
        assert (probe / (name + '.ddsave')).read_bytes() == (probe / (name + '-restored.ddsave')).read_bytes()
    failure = read(failed_probe / 'RESULT.json')
    assert failure['status'] == 'FAIL' and 'Controller regained a suppressed source' in failure['error']
    assert failure['script']['sha256'] == digest((failed_probe / 'Probe-FerrySeal.executed.ps1').read_bytes())
    failed = read(failed_compile / 'results.json')
    assert failed['status'] == 'FAIL' and failed['testsDiscovered'] == 0 and len(failed.get('sourceHashes', [])) == 0
    assert 'CS0117' in failed['error'] and 'Subtract' in failed['error']
    intermediate = read(failed_static / 'results.json')
    assert intermediate['status'] == 'PASS' and len(intermediate['sourceHashes']) == 977
    for row in intermediate['sourceHashes']:
        path = 'engine/' + row['path'].replace('\\', '/')
        raw = (failed_compile / 'FerryWraithCases.failed.cs').read_bytes() if path.endswith('/FerryWraithCases.cs') else runtime.read(path)
        assert digest(raw) == row['sha256'], path
    members = {}
    for label, folder in [('runtime-build', first), ('focused-build', final), ('selected-static', static),
                          ('genuine-seal', probe), ('probe-failure', failed_probe),
                          ('test-compilation-failure', failed_compile), ('intermediate-static', failed_static)]:
        for path in sorted(folder.rglob('*')):
            if path.is_file():
                members[label + '/' + path.relative_to(folder).as_posix()] = path.read_bytes()
    changed = subprocess.check_output(['git', 'diff', BASE, SOURCE, '--name-only', '--', 'engine'], cwd=ROOT).decode().splitlines()
    assert len(changed) == 11
    for path in changed:
        members['changed-source/' + path] = selected.read(path)
    case_path = 'engine/com.decennium.foundation/Tests/EditMode/FerryWraithCases.cs'
    members['runtime-build/source/' + case_path] = runtime.read(case_path)
    members['review/GPT_CORRECTION_REVIEW.json'] = selected.read(PACKET + 'GPT_CORRECTION_REVIEW.json')
    members['executed-support/Retain-FerrySeal.py'] = Path(__file__).read_bytes()
    manifest = [dict(path=name, bytes=len(raw), sha256=digest(raw)) for name, raw in sorted(members.items())]
    OUT.mkdir()
    archive = OUT / 'development-seal.zip'
    with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as output:
        for name, raw in sorted(members.items()):
            info = zipfile.ZipInfo(name, (2026, 11, 17, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            output.writestr(info, raw)
    with zipfile.ZipFile(archive) as check:
        assert check.namelist() == [x['path'] for x in manifest]
        for row in manifest:
            assert digest(check.read(row['path'])) == row['sha256']
    result = dict(status='PASS_RETAINED_GENUINE_SEAL_AND_RECOVERED_CLAW_NOT_MODULE_ACCEPTANCE', runtimeCommit=RUNTIME,
                  focusedTestCommit=SOURCE, compiledSourceInputs=468, staticInputs=977, changedEngineFiles=11,
                  selectedCasesPassed=2, mechanicalArrangements=4, negativeMechanicalControls=6, genuineCommands=14,
                  ruptureRevision=354, finalRevision=365, suppressedControllerSteps=2,
                  suppressedSaveSha256=digest((probe / 'suppressed.ddsave').read_bytes()),
                  finalSaveSha256=digest((probe / 'recovered-claw.ddsave').read_bytes()),
                  members=len(manifest), archiveSha256=digest(archive.read_bytes()), archiveBytes=archive.stat().st_size,
                  failedCompilationSourceHashesRecorded=False, failedCompilationSourceBoundBySeparateStatic=True,
                  fullRegression=False, completeCreatureContinuation=False, moduleAccepted=False,
                  scriptSha256=digest(Path(__file__).read_bytes()))
    (OUT / 'MEMBERS.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    (OUT / 'RETENTION.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
