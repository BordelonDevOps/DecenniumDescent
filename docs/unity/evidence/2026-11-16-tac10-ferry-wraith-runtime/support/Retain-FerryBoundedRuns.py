"""Retain exact, source-bound supplementary runs without promoting acceptance."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
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
    manifest_path = Path(sys.argv[1]).resolve()
    manifest = read(manifest_path)
    output = PACKET / manifest['output']
    assert output.parent == PACKET and not output.exists(), 'Never overwrite retained evidence.'
    members = {'bindings/run-manifest.json': manifest_path.read_bytes(),
               'bindings/retention-collector.py': Path(__file__).read_bytes()}
    compilation = read(BUILD / 'results.json')
    assert compilation['status'] == compilation['coreCompilation'] == 'PASS'
    assert len(compilation['sourceHashes']) == 468
    for row in compilation['sourceHashes']:
        assert sha((ROOT / 'engine' / row['path'].replace('\\', '/')).read_bytes()) == row['sha256']
    members['bindings/compilation.json'] = (BUILD / 'results.json').read_bytes()
    summaries = []
    for spec in manifest['runs']:
        folder = ROOT / spec['path']
        result = read(folder / 'RESULT.json')
        assert result['status'] == spec['expectedStatus'], (spec['label'], result['status'])
        executed = folder / (spec['script'][:-4] + '.executed.ps1')
        committed = subprocess.check_output(['git', '-C', str(ROOT), 'show', spec['commit'] + ':' + (HERE / spec['script']).relative_to(ROOT).as_posix()])
        assert committed == executed.read_bytes()
        assert sha(committed) == result['script']['sha256']
        for row in result['assemblies']:
            assert row['sha256'] == sha((BUILD / ('Decennium.Foundation.' + row['name'] + '.dll')).read_bytes())
        for pair in result.get('restorePairs', []):
            original, restored = folder / (pair['name'] + '.ddsave'), folder / (pair['name'] + '-restored.ddsave')
            assert original.read_bytes() == restored.read_bytes() and sha(original.read_bytes()) == pair['sha256']
        for path in sorted(folder.rglob('*')):
            if path.is_file():
                members[spec['label'] + '/' + path.relative_to(folder).as_posix()] = path.read_bytes()
        summaries.append(dict(label=spec['label'], status=result['status'], scriptCommit=spec['commit'],
                              executedSha256=sha(committed), commands=len(result.get('commands', [])),
                              restorePairs=len(result.get('restorePairs', [])), privatePairs=len(result.get('pairs', [])),
                              finalRevision=result.get('finalRevision'), error=result.get('error')))
    output.mkdir()
    archive = output / 'bounded-runs.zip'
    with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as bundle:
        for name, raw in sorted(members.items()):
            bundle.writestr(name, raw)
    member_rows = [dict(path=name, bytes=len(raw), sha256=sha(raw)) for name, raw in sorted(members.items())]
    with zipfile.ZipFile(archive) as bundle:
        assert bundle.testzip() is None and len(bundle.namelist()) == len(member_rows)
        assert all(sha(bundle.read(row['path'])) == row['sha256'] for row in member_rows)
    retention = dict(status='PASS_EXACT_BOUNDED_RUN_RETENTION_NOT_MODULE_ACCEPTANCE', scope=manifest['scope'],
                     runtimeCommit='c8ffee78d5047131317ff923c8e3a575b6c51f3a', compileInputs=468,
                     collectorSha256=sha(Path(__file__).read_bytes()), manifestSha256=sha(manifest_path.read_bytes()),
                     archive=dict(path=archive.name, members=len(members), bytes=archive.stat().st_size, sha256=sha(archive.read_bytes())),
                     runs=summaries, limits=manifest['limits'])
    (output / 'MEMBERS.json').write_text(json.dumps(member_rows, indent=2) + '\n', encoding='utf-8')
    (output / 'RETENTION.json').write_text(json.dumps(retention, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(retention, ensure_ascii=False))


if __name__ == '__main__':
    main()
