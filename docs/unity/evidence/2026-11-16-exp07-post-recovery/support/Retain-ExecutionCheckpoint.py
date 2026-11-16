"""Retain a verified, explicitly incomplete EXP-07 execution checkpoint. Runs no gameplay."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess

PACKET = Path(__file__).resolve().parents[1]
ROOT = PACKET.parents[3]
SOURCE = '6d840c4dfce268115904ea0dda6b475450f7be6f'


def longpath(path):
    value = str(Path(path).resolve())
    return Path(value if value.startswith('\\\\?\\') else '\\\\?\\' + value)


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(path, value):
    data = (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        assert path.read_bytes() == data, 'Never replace retained evidence: ' + str(path)
    else:
        path.write_bytes(data)


def copy(source, target):
    data = source.read_bytes()
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        assert target.read_bytes() == data, 'Retained artifact changed: ' + str(target)
    else:
        target.write_bytes(data)


def tree(source, target):
    for path in sorted(source.rglob('*')):
        if path.is_file() and path.suffix != '.dll':
            copy(path, target / path.relative_to(source))


def retain_run(source, target, complete, required):
    launch = read(source / 'launch.json')
    workers = read(source / 'processes.json')
    assert launch['requiredCount'] == required
    if complete:
        assert required == 13 and not launch['sourceCommitted']
    else:
        assert required == 1566 and launch['sourceCommit'] == SOURCE and launch['sourceCommitted']
    assert digest(source / 'all-names.txt') == launch['inventorySha256']
    for name in ('launch.json', 'processes.json', 'all-names.txt', 'compiled-source-report.json'):
        copy(source / name, target / name)
    rows, details = [], []
    for worker in workers:
        group = worker['group']
        assignment = source / (group + '-names.txt')
        started = read(source / (group + '.started.json'))
        assert started['runId'] == launch['runId'] and started['pid'] == worker['pid']
        assert started['assignmentSha256'] == launch['assignments'][group] == digest(assignment)
        for name, expected in launch['assemblies'].items():
            assert started['assemblies'][name]['sha256'] == expected
            assert digest(source / 'execution-assemblies' / name) == expected
        data = (source / (group + '.jsonl')).read_bytes()
        # Capture one complete prefix even if a worker is appending its next row.
        boundary = data.rfind(b'\n') + 1
        prefix = data[:boundary]
        values = [json.loads(line) for line in prefix.decode('utf-8-sig').splitlines()]
        names = assignment.read_text(encoding='utf-8-sig').splitlines()
        assert [row['Name'] for row in values] == names[:len(values)]
        assert all(row['Passed'] and not row['Error'] for row in values)
        target.mkdir(parents=True, exist_ok=True)
        (target / (group + '.jsonl')).write_bytes(prefix)
        for suffix in ('-names.txt', '.started.json'):
            copy(source / (group + suffix), target / (group + suffix))
        finished = (source / (group + '.done')).exists()
        if complete:
            assert finished and len(values) == worker['cases']
            ending = read(source / (group + '.execution.json'))
            assert ending['runId'] == launch['runId'] and ending['pid'] == worker['pid']
            assert ending['journalSha256'] == hashlib.sha256(prefix).hexdigest()
            assert (source / (group + '.done')).read_text(encoding='utf-8-sig').strip() == 'DONE'
            for suffix in ('.execution.json', '.done'):
                copy(source / (group + suffix), target / (group + suffix))
        rows.extend(values)
        details.append(dict(group=group, pid=worker['pid'], passedPrefix=len(values),
                            assigned=worker['cases'], completeClaimed=complete,
                            capturedJournalSha256=hashlib.sha256(prefix).hexdigest()))
    assert len({row['Name'] for row in rows}) == len(rows)
    assert len(rows) == required if complete else len(rows) < required
    return dict(runId=launch['runId'], passed=len(rows), required=required, failed=0,
                workers=details, assemblies=launch['assemblies'])


def main():
    parser = argparse.ArgumentParser()
    for name in ('build', 'static', 'qualification', 'output'):
        parser.add_argument('--' + name, type=Path, required=True)
    args = parser.parse_args()
    build, static, qualification, output = [longpath(getattr(args, name))
                                            for name in ('build', 'static', 'qualification', 'output')]
    assert not subprocess.check_output(['git', 'diff', SOURCE, '--', 'engine'], cwd=ROOT).strip()
    source_audit = read(output / 'SOURCE_AUDIT.json')
    assert source_audit['status'] == 'PASS' and source_audit['implementationCommit'] == SOURCE
    for field in ('sourceArchive', 'binaryArchive'):
        entry = source_audit[field]
        assert digest(output / entry['path']) == entry['sha256']
    for path in (build / 'results.json', static):
        assert read(path)['status'] == 'PASS'
    assert digest(build / 'results.json') == source_audit['buildReportSha256']
    copy(build / 'results.json', output / 'builds/frozen/results.json')
    copy(static, output / 'builds/static/results.json')
    checkpoint = output / 'execution-checkpoint-01'
    assert not checkpoint.exists(), 'Never replace an existing execution checkpoint'
    focused = retain_run(qualification / 'focused-01', checkpoint / 'focused-execution', True, 13)
    original = retain_run(qualification / 'regression-01', checkpoint / 'original-regression-prefix', False, 1566)
    assert focused['assemblies'] == original['assemblies']
    tree(qualification / 'focused-01/saves', output / 'focused')
    result = dict(status='INCOMPLETE_EXECUTION_CHECKPOINT_FOR_ACTUAL_REVIEW', implementationCommit=SOURCE,
                  capturedUtc=datetime.now(timezone.utc).isoformat(), focused=focused, originalRegression=original,
                  historicalPins=65, compiledInputs=440,
                  scope='Frozen source/build/static and thirteen actual connected/negative cases; incomplete original full regression. '
                        'Final five-path campaigns, authentic-save/legacy-view qualification, complete regression, artifact reconciliation '
                        'and actual final GPT acceptance are still required. No successor, production or Unity approval is claimed.')
    write(checkpoint / 'RESULTS.json', result)
    artifacts = []
    for path in sorted(output.rglob('*')):
        if path.is_file() and path.name != 'CHECKPOINT_ARTIFACT_INDEX.json':
            artifacts.append(dict(path=path.relative_to(output).as_posix(), bytes=path.stat().st_size, sha256=digest(path)))
    write(output / 'CHECKPOINT_ARTIFACT_INDEX.json', dict(status='RETAINED_INCOMPLETE_CHECKPOINT', artifacts=artifacts))
    print(json.dumps(dict(status=result['status'], focusedPassed=13, originalPassedPrefix=original['passed'],
                          required=1566, retainedArtifacts=len(artifacts)), separators=(',', ':')))


if __name__ == '__main__':
    main()
