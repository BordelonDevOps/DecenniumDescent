"""Retain existing development outputs; this does not execute or accept the module."""
import hashlib
import json
from pathlib import Path
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[5]
PACKET = Path(__file__).resolve().parents[1]
DEV = ROOT / 'engine/artifacts/declared-geometry/development'
BUILD = DEV / 'run-20261117T015232462Z-9b7f2e1a'
FOCUSED = DEV / 'focused-current-v1'
STATIC = DEV / 'static-20261117T015442789Z-fbe3bf40'
read = lambda p: json.loads(p.read_text(encoding='utf-8-sig'))
digest = lambda b: hashlib.sha256(b).hexdigest()

def archive(path, members):
    assert not path.exists(), 'Never replace retained evidence'
    rows = []
    with zipfile.ZipFile(path, 'x', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for name, source in sorted(members.items()):
            data = source.read_bytes()
            z.writestr(name, data)
            rows.append(dict(path=name, bytes=len(data), sha256=digest(data)))
    with zipfile.ZipFile(path) as z:
        assert sorted(z.namelist()) == sorted(x['path'] for x in rows)
        for row in rows:
            data = z.read(row['path'])
            assert len(data) == row['bytes'] and digest(data) == row['sha256']
    return dict(path=path.name, bytes=path.stat().st_size, sha256=digest(path.read_bytes()), members=rows)

def main():
    output = PACKET / 'implementation'
    output.mkdir(exist_ok=False)
    compiled, focused, static = (read(p / 'results.json') for p in (BUILD, FOCUSED, STATIC))
    assert compiled['status'] == focused['status'] == static['status'] == 'PASS'
    assert len(focused['cases']) == 5 and all(x['Passed'] and not x['Error'] for x in focused['cases'])
    assert digest((BUILD / 'results.json').read_bytes()) == focused['buildReportSha256']
    for report in (compiled, focused, static):
        for row in report['sourceHashes']:
            assert digest((ROOT / 'engine' / row['path']).read_bytes()) == row['sha256'], row['path']
    for name in ('exclusion-genesis.json', 'exclusion-continued.json'):
        assert read(DEV / name)['status'] == 'PASS'
    baseline = read(DEV / 'baseline-v4/results.json')
    assert baseline['status'] == 'PASS' and baseline['commands'] == 457 and baseline['saves'] == 21
    members = {}
    for folder in (FOCUSED, DEV / 'baseline-v4'):
        for p in folder.rglob('*'):
            if p.is_file():
                members[p.relative_to(DEV).as_posix()] = p
    for folder in DEV.iterdir():
        if folder.is_dir() and (folder / 'results.json').is_file():
            members[folder.name + '/results.json'] = folder / 'results.json'
    for name in ('exclusion-genesis.json', 'exclusion-continued.json', 'bishop-baseline-inputs.jsonl'):
        members[name] = DEV / name
    assemblies = {p.name: p for p in BUILD.glob('*.dll')}
    assert len(assemblies) == 4
    report = dict(status='PASS_DEVELOPMENT_RETENTION', scope='Five focused cases, fresh inherited route, semantic exclusion probes and existing development failures; not full qualification or acceptance',
                  sourceBase=subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
                  compiledSourceCount=len(compiled['sourceHashes']),
                  evidence=archive(output / 'development-evidence.zip', members),
                  assemblies=archive(output / 'compiled-assemblies.zip', assemblies))
    for name, path in (('compiled-results.json', BUILD / 'results.json'), ('static-results.json', STATIC / 'results.json')):
        (output / name).write_bytes(path.read_bytes())
    (output / 'RETENTION.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in report.items() if k not in ('evidence', 'assemblies')}))
    print(json.dumps({k: {f: report[k][f] for f in ('path', 'bytes', 'sha256')} for k in ('evidence', 'assemblies')}))

if __name__ == '__main__':
    main()
