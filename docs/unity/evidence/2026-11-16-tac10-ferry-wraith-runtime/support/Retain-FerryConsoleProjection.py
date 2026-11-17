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
    parser.add_argument('--adapter-run')
    parser.add_argument('--static-report')
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
    adapter_result, static_result = None, None
    if args.adapter_run:
        assert args.phase == 'after'
        directory = ROOT / args.adapter_run
        adapter = read(directory / 'RESULT.json')
        assert adapter['status'] == 'PASS_ACTUAL_INHERITED_PRESENCE_AND_SANCTUARY_ADAPTERS'
        assert adapter['launcher']['sha256'] == sha(host)
        assert (directory / 'Open-ConnectedExpedition.executed.ps1').read_bytes() == host
        assert adapter['script']['sha256'] == sha((directory / 'Probe-FerryInheritedAdapters.executed.ps1').read_bytes())
        assert adapter['input']['sha256'] == sha((directory / 'source-inputs.jsonl').read_bytes())
        for dll in adapter['assemblies']:
            assert dll['sha256'] == sha((BUILD / ('Decennium.Foundation.' + dll['name'] + '.dll')).read_bytes())
        pairs = {}
        for restored in directory.glob('*-restored.ddsave'):
            original = restored.with_name(restored.name.replace('-restored.ddsave', '.ddsave'))
            assert original.read_bytes() == restored.read_bytes()
            pairs[original.name] = sha(original.read_bytes())
        assert len(pairs) == 4
        requests = [json.loads(line) for line in (directory / 'executed-inputs.jsonl').read_text(encoding='utf-8-sig').splitlines()]
        responses = [json.loads(line) for line in (directory / 'responses.jsonl').read_text(encoding='utf-8-sig').splitlines()]
        assert len(requests) == len(responses)
        committed = [row for row in responses if row.get('Response') == 'Committed']
        assert [row['Revision'] for row in committed] == list(range(1, adapter['finalRevision'] + 1))
        assert adapter['presenceReceipt']['Revision'] == 129
        assert any(request['op'] == 'defender-sanctuary' and response.get('Response') == 'Committed' for request, response in zip(requests, responses))
        for path in sorted(directory.iterdir()):
            assert path.is_file()
            members['adapters/' + path.name] = path.read_bytes()
        adapter_result = dict(directory=args.adapter_run, finalRevision=adapter['finalRevision'], commands=len(committed), restorePairs=pairs, pureProbes=len(adapter['probes']))
    if args.static_report:
        static_path = ROOT / args.static_report
        static = read(static_path)
        assert static['status'] == 'PASS' and all(row['passed'] for row in static['checks'])
        for row in static['sourceHashes']:
            assert sha((ROOT / 'engine' / row['path'].replace('\\', '/')).read_bytes()) == row['sha256']
        members['static/results.json'] = static_path.read_bytes()
        static_result = dict(inputs=len(static['sourceHashes']), sha256=sha(static_path.read_bytes()), hostIncludedInStaticInputs=False)
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
    result['inheritedAdapters'] = adapter_result
    result['staticPackage'] = static_result
    (out / 'MEMBERS.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    (out / 'RETENTION.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in result.items() if k != 'executions'}))


if __name__ == '__main__':
    main()
