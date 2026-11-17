"""Retain genuine paid Dash, seal/closure continuation and pure post-exit controls."""
import hashlib
import json
from pathlib import Path
import subprocess
import zipfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
PACKET = HERE.parent
AREA = ROOT / 'engine/artifacts/ferry-wraith/dash-correction'
BUILD = AREA / 'run-20261117T110451175Z-06a69ef8'
RUNTIME = 'c8ffee78d5047131317ff923c8e3a575b6c51f3a'
DRIVER = '6cffd7b1e8f7a0b0662847a4a83a705a73e86cf7'
CONTINUATION_DRIVER = 'e744c04a35cfb94e0f77207e3f35610b77b9868b'
RUNS = {
    'seal-dash': (AREA / 'seal-with-dash-20261117T113456Z', 'Probe-FerrySealWithDash', DRIVER),
    'closure': (AREA / 'dash-closure-20261117T113827Z', 'Probe-FerryContinuation', CONTINUATION_DRIVER),
    'after-exit': (AREA / 'after-exit-20261117T114454Z', 'Probe-FerryAfterExitRetry', DRIVER),
}
OUT = PACKET / 'after-exit-checkpoint'


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def main():
    assert not subprocess.check_output(['git', '-C', str(ROOT), 'diff', '--name-only', RUNTIME, '--', 'engine'])
    compiled = (BUILD / 'results.json').read_bytes()
    passing = json.loads(compiled)
    assert passing['status'] == passing['coreCompilation'] == 'PASS' and len(passing['sourceHashes']) == 468
    for row in passing['sourceHashes']:
        assert sha((ROOT / 'engine' / row['path'].replace('\\', '/')).read_bytes()) == row['sha256']
    prior = read(PACKET / 'public-dash-checkpoint/RETENTION.json')
    prior_archive = PACKET / 'public-dash-checkpoint/public-dash.zip'
    assert sha(prior_archive.read_bytes()) == prior['archiveSha256']
    reports, members, pairs, drivers = {}, {}, {}, {}
    with zipfile.ZipFile(prior_archive) as archive:
        assert archive.read('focused-build/results.json') == compiled
        for label, (directory, driver, commit) in RUNS.items():
            report = reports[label] = read(directory / 'RESULT.json')
            original = subprocess.check_output(['git', '-C', str(ROOT), 'show', commit + ':' + (HERE / (driver + '.ps1')).relative_to(ROOT).as_posix()])
            assert (directory / (driver + '.executed.ps1')).read_bytes() == original
            assert report['script']['sha256'] == sha(original)
            assert report['compilationReport']['sha256'] == sha(compiled)
            drivers[label] = dict(commit=commit, sha256=sha(original))
            for dll in report['assemblies']:
                name = 'Decennium.Foundation.' + dll['name'] + '.dll'
                assert dll['sha256'] == sha((BUILD / name).read_bytes()) == sha(archive.read('focused-build/' + name))
            for path in sorted(directory.iterdir()):
                assert path.is_file(), 'Unexpected nested execution output'
                members['executed/' + label + '/' + path.name] = path.read_bytes()
            for restored in directory.glob('*-restored.ddsave'):
                original = restored.with_name(restored.name.replace('-restored.ddsave', '.ddsave'))
                assert original.read_bytes() == restored.read_bytes()
                pairs[label + '/' + original.name] = sha(original.read_bytes())
    seal, closure, exit_report = (reports[key] for key in RUNS)
    assert seal['status'] == 'PASS_GENUINE_SEAL_DASH_RECOVERED_CLAW_ONLY'
    assert closure['status'] == 'PASS_GENUINE_DEAD_CLOSURE_MANAGE_PREPARE_CONTINUE_ONLY'
    assert exit_report['status'] == 'PASS_GENUINE_POST_EXIT_DASH_RETRY_AND_FRESH_DENIAL_ONLY'
    for report, first, last in [(seal, 351, 366), (closure, 366, 463)]:
        assert len(report['commands']) == last - first
        assert [c['response']['Revision'] for c in report['commands']] == list(range(first + 1, last + 1))
        assert all(c['response']['Response'] == 4 for c in report['commands'])
        assert report['finalRevision'] == last
    assert seal['firstFireSource']['sha256'] == sha(members['executed/seal-dash/original-first-fire.ddsave']) == '6a69b36f95e4435705fb175030f7f16aebbfa76bb0752168af65f321d7ab2687'
    assert members['executed/seal-dash/original-first-fire.ddsave'] == members['executed/seal-dash/verified-current-first-fire.ddsave']
    assert members['executed/seal-dash/recovered-claw.ddsave'] == members['executed/closure/original-recovered-claw.ddsave']
    assert closure['source']['sha256'] == sha(members['executed/closure/original-recovered-claw.ddsave'])
    assert seal['dashCommand'] == exit_report['originalDash']
    assert seal['dashQuery']['Admissible'] and seal['dashInterval']['DashPaid'] and seal['dashInterval']['ActionSpent']
    assert seal['rupture']['ExpiresAt'] == {'Numerator': 344093, 'Denominator': 2}
    assert seal['recoveredAttack']['Damage']['Total'] == 3 and seal['recoveredAttack']['Attack']['Hit']
    assert seal['recoveredAttack']['Revision'] == 366
    assert closure['closure'][0]['ClosedRevision'] == 438
    assert closure['closure'][0]['ClosedAt'] == {'Numerator': 344205, 'Denominator': 2}
    assert closure['preparation']['club']['HeldBy'] == 'TEST_ONLY.companion'
    assert closure['finalResonance'][0]['Current'] == 3
    assert [p['Hp'] for p in closure['finalParty']] == [14, 18]
    final = members['executed/closure/continued-after-preparation.ddsave']
    assert sha(final) == closure['backupRecovery']['validSha256'] == closure['backupRecovery']['backupSha256']
    assert final == members['executed/closure/backup-recovery.ddsave'] == members['executed/closure/backup-recovery.ddsave.bak']
    displaced = Path(closure['backupRecovery']['displacedPath']).name
    assert sha(members['executed/closure/' + displaced]) == closure['backupRecovery']['corruptSha256']
    for name in ['original-closed.ddsave', 'verified-closed.ddsave', 'after-probes.ddsave', 'after-probes-restored.ddsave']:
        assert members['executed/after-exit/' + name] == final
    assert exit_report['input']['sha256'] == sha(final)
    assert exit_report['finalRevision'] == 463
    assert exit_report['finalClock'] == closure['finalClock'] == {'Numerator': 344239, 'Denominator': 2}
    assert exit_report['originalReceipt']['Revision'] == 357 and exit_report['originalReceipt']['Id'] == 'ferry.exit.dash.356'
    for prefix, code, response in [('exact', 'AlreadyCommitted', 5), ('fresh', 'FerryDashRequiresPartyCombat', 0), ('conflict', 'CommandIdConflict', 3), ('revoked', 'NotAuthorized', 1)]:
        assert exit_report[prefix + 'Query']['Code'] == code
        assert exit_report[prefix + 'Response']['Response'] == response
        assert exit_report[prefix + 'Response']['Revision'] == 463
    assert exit_report['otherSeatResponse']['Response'] == 1
    assert len(pairs) == 7
    members['support/Retain-FerryAfterExit.py'] = Path(__file__).read_bytes()
    members['references/public-dash-RETENTION.json'] = (PACKET / 'public-dash-checkpoint/RETENTION.json').read_bytes()
    members['references/GPT_PUBLIC_DASH_REVIEW.json'] = (PACKET / 'GPT_PUBLIC_DASH_REVIEW.json').read_bytes()
    members['references/GPT_PRESS_KNOCKOUT_REVIEW.json'] = (PACKET / 'GPT_PRESS_KNOCKOUT_REVIEW.json').read_bytes()
    manifest = [dict(path=name, bytes=len(raw), sha256=sha(raw)) for name, raw in sorted(members.items())]
    assert not OUT.exists()
    OUT.mkdir()
    output = OUT / 'after-exit.zip'
    with zipfile.ZipFile(output, 'x') as archive:
        for name, raw in sorted(members.items()):
            info = zipfile.ZipInfo(name, (2026, 11, 17, 0, 0, 0)); info.compress_type = zipfile.ZIP_DEFLATED; info.external_attr = 0o100644 << 16
            archive.writestr(info, raw)
    with zipfile.ZipFile(output) as archive:
        assert archive.namelist() == [row['path'] for row in manifest]
        for row in manifest:
            raw = archive.read(row['path']); assert len(raw) == row['bytes'] and sha(raw) == row['sha256']
    result = dict(status='PASS_GENUINE_DASH_SEAL_CLOSURE_AFTER_EXIT_NOT_MODULE_ACCEPTANCE', runtimeCommit=RUNTIME,
                  driverBindings=drivers, compiledSourceInputs=468, additionalCompilation=False,
                  sealDashCommands=15, continuationCommands=97, totalCommands=112,
                  postExitNewCommands=0, selectedRestorePairs=pairs, finalRevision=463, finalSaveSha256=sha(final),
                  originalMainRevision462Unmodified=True, archiveBytes=output.stat().st_size,
                  archiveSha256=sha(output.read_bytes()), members=len(manifest),
                  scriptSha256=sha(Path(__file__).read_bytes()), moduleAccepted=False, fivePaths=False)
    (OUT / 'MEMBERS.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    (OUT / 'RETENTION.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({key: value for key, value in result.items() if key not in ('selectedRestorePairs', 'driverBindings')}))


if __name__ == '__main__':
    main()
