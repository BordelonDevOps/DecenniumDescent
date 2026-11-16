"""Retain corrected build and superseded execution without claiming qualification."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[5]
read = lambda p: json.loads(p.read_text(encoding='utf-8-sig'))
digest = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()


def bundle(output, name, members):
    path = output / name
    index = []
    with zipfile.ZipFile(path, 'x', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for key, source in sorted(members.items()):
            data = source.read_bytes()
            archive.writestr(key, data)
            index.append(dict(path=key, bytes=len(data), sha256=hashlib.sha256(data).hexdigest()))
    with zipfile.ZipFile(path) as archive:
        assert archive.namelist() == [x['path'] for x in index]
        for row in index:
            data = archive.read(row['path'])
            assert len(data) == row['bytes'] and hashlib.sha256(data).hexdigest() == row['sha256']
    return dict(path=name, bytes=path.stat().st_size, sha256=digest(path), members=index)


def add_tree(members, source, prefix, dlls=False):
    for path in sorted(source.rglob('*')):
        if path.is_file() and (dlls or path.suffix != '.dll'):
            key = prefix + '/' + path.relative_to(source).as_posix()
            assert key not in members
            members[key] = path


def main():
    parser = argparse.ArgumentParser()
    for name in ('build', 'focused', 'failed', 'static', 'audit', 'superseded', 'output'):
        parser.add_argument('--' + name, required=True, type=Path)
    args = parser.parse_args()
    build, focused, failed, static, audit, superseded, output = (
        getattr(args, name).resolve() for name in ('build', 'focused', 'failed', 'static', 'audit', 'superseded', 'output'))
    assert not output.exists(), 'Do not replace retained evidence'
    report = read(build / 'results.json')
    assert report['status'] == 'PASS' and report['passed'] == 1 and report['failed'] == 0
    for row in report['sourceHashes']:
        assert digest(ROOT / 'engine' / row['path']) == row['sha256'], row['path']
    focused_report = read(focused / 'results.json')
    assert focused_report['status'] == 'PASS' and focused_report['passed'] == 1
    assert focused_report['cases'][0]['Name'] == 'chr03_bishop_connected_earned_funded_cure_aura_dispel_continue'
    assert read(failed / 'results.json')['status'] == 'FAIL'
    assert read(static / 'results.json')['status'] == 'PASS'
    assert read(audit / 'SOURCE_AUDIT.json')['status'] == 'PASS_SOURCE_ONLY'
    stopped = read(superseded / 'SUPERSEDED.json')
    assert stopped['status'] == 'SUPERSEDED_PARTIAL_NOT_PASS'
    launch = read(superseded / 'launch.json')
    assert stopped['runId'] == launch['runId'] and stopped['sourceCommit'] == launch['sourceCommit']
    old_rows = []
    for worker in stopped['workers']:
        group = worker['group']
        assert worker['stopped'] and digest(superseded / (group + '.jsonl')) == worker['journalSha256']
        rows = [json.loads(line) for line in (superseded / (group + '.jsonl')).read_text(encoding='utf-8-sig').splitlines()]
        assigned = (superseded / (group + '-names.txt')).read_text(encoding='utf-8-sig').splitlines()
        assert [r['Name'] for r in rows] == assigned[:len(rows)]
        old_rows.extend(rows)
    output.mkdir(parents=True)
    members = {}
    add_tree(members, focused, 'focused')
    add_tree(members, failed, 'failed-test-setup')
    for path in superseded.iterdir():
        if path.is_file():
            members['superseded-regression/' + path.name] = path
    for folder in (superseded / 'saves').iterdir():
        if folder.name.startswith('chr03_bishop_'):
            add_tree(members, folder, 'superseded-regression/saves/' + folder.name)
    evidence = bundle(output, 'correction-evidence.zip', members)
    assemblies = bundle(output, 'execution-assemblies.zip', {p.name: p for p in build.glob('*.dll')})
    assert len(assemblies['members']) == 4
    for source, name in ((build / 'results.json', 'compiled-source-report.json'),
                         (static / 'results.json', 'static-results.json'), (audit / 'SOURCE_AUDIT.json', 'SOURCE_AUDIT.json')):
        (output / name).write_bytes(source.read_bytes())
    result = dict(status='CORRECTED_CANDIDATE_NOT_ACCEPTED',
                  parentCommit=subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
                  reviewResponse='74094c3b-2b1e-553c-ae02-ece6685d80d5',
                  frozenBuild=str(build), focusedValidationBuild=str(focused),
                  compiledInputs=len(report['sourceHashes']),
                  supersededRun=dict(runId=launch['runId'], completed=len(old_rows),
                                     passing=sum(bool(r['Passed']) for r in old_rows), status=stopped['status']),
                  evidence=evidence, assemblies=assemblies)
    (output / 'RETENTION.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in result.items() if k not in ('evidence', 'assemblies')}))


if __name__ == '__main__':
    main()
