"""Retain console projection reproduction/correction without claiming new C# qualification."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import zipfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
PACKET = HERE.parent
BUILD = ROOT / 'engine/artifacts/ferry-wraith/dash-correction/run-20261117T110451175Z-06a69ef8'


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--phase', choices=['before', 'after'], required=True)
    parser.add_argument('--host-commit', required=True)
    parser.add_argument('--run', action='append', required=True)
    args = parser.parse_args()
    compiled = read(BUILD / 'results.json')
    assert compiled['coreCompilation'] == compiled['status'] == 'PASS' and len(compiled['sourceHashes']) == 468
    for row in compiled['sourceHashes']:
        assert sha((ROOT / 'engine' / row['path'].replace('\\', '/')).read_bytes()) == row['sha256']
    host = subprocess.check_output(['git', '-C', str(ROOT), 'show', args.host_commit + ':engine/tools/Open-ConnectedExpedition.ps1'])
    prior = read(PACKET / 'public-dash-checkpoint/RETENTION.json')
    archive_path = PACKET / 'public-dash-checkpoint/public-dash.zip'
    assert sha(archive_path.read_bytes()) == prior['archiveSha256']
    members, reports = {}, []
    with zipfile.ZipFile(archive_path) as build_archive:
        for folder in args.run:
            directory = ROOT / folder
            report = read(directory / 'RESULT.json')
            assert sha(host) == report['launcher']['sha256']
            assert host == (directory / 'Open-ConnectedExpedition.executed.ps1').read_bytes()
            assert report['script']['sha256'] == sha((directory / 'Probe-FerryConsoleProjection.executed.ps1').read_bytes())
            for dll in report['assemblies']:
                name = 'Decennium.Foundation.' + dll['name'] + '.dll'
                assert dll['sha256'] == sha((BUILD / name).read_bytes()) == sha(build_archive.read('focused-build/' + name))
            for path in sorted(directory.iterdir()):
                assert path.is_file()
                members['executed/' + directory.name + '/' + path.name] = path.read_bytes()
            reports.append(dict(directory=folder, status=report['status'], error=report.get('error'), seats=report['seats']))
            if report['status'].startswith('PASS_'):
                assert (directory / 'before.ddsave').read_bytes() == (directory / 'after.ddsave').read_bytes()
    expected = 'PASS_REPRODUCED_FERRY_CONSOLE_PROFILE_OMISSION' if args.phase == 'before' else 'PASS_INHERITED_PUBLIC_FERRY_CONSOLE_PROJECTION'
    assert reports[-1]['status'] == expected
    assert len(reports[-1]['seats']) == 4
    for row in reports[-1]['seats']:
        assert bool(row['missing']) == (args.phase == 'before')
    members['support/Retain-FerryConsoleProjection.py'] = Path(__file__).read_bytes()
    members['references/public-dash-RETENTION.json'] = (PACKET / 'public-dash-checkpoint/RETENTION.json').read_bytes()
    manifest = [dict(path=name, bytes=len(raw), sha256=sha(raw)) for name, raw in sorted(members.items())]
    out = PACKET / ('console-projection-' + args.phase)
    assert not out.exists()
    out.mkdir()
    output = out / 'console-projection.zip'
    with zipfile.ZipFile(output, 'x') as archive:
        for name, raw in sorted(members.items()):
            info = zipfile.ZipInfo(name, (2026, 11, 17, 0, 0, 0)); info.compress_type = zipfile.ZIP_DEFLATED; info.external_attr = 0o100644 << 16
            archive.writestr(info, raw)
    with zipfile.ZipFile(output) as archive:
        for row in manifest:
            raw = archive.read(row['path']); assert len(raw) == row['bytes'] and sha(raw) == row['sha256']
    result = dict(status=expected, phase=args.phase, runtimeCommit='c8ffee78d5047131317ff923c8e3a575b6c51f3a', hostCommit=args.host_commit,
                  hostSha256=sha(host), compilationInputs=468, additionalCompilation=False, executions=reports,
                  members=len(manifest), archiveBytes=output.stat().st_size, archiveSha256=sha(output.read_bytes()),
                  collectorSha256=sha(Path(__file__).read_bytes()), moduleAccepted=False, fivePaths=False)
    (out / 'MEMBERS.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    (out / 'RETENTION.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in result.items() if k != 'executions'}))


if __name__ == '__main__':
    main()
