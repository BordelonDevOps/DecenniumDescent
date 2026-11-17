"""Reconcile retained cloud results with local completion; never execute gameplay.

Usage: python -B -X utf8 <script> --segment <extracted> --supplement <extracted>
       --delta <extracted> [--verify-only]
Requires actual terminal local workers/paths. Unknown cloud exits stay unknown.
"""
from pathlib import Path, PureWindowsPath
import argparse
import hashlib
import json
import os
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[5]
PACKET = Path(__file__).resolve().parents[1]
LOCAL = ROOT / 'engine/artifacts/consecration/local-import-qualification'
SOURCE = '3c5135ae0d664d79528fff1f2676fae2198beb28'
MODES = ['ConsoleUninterrupted', 'ConsoleRestored', 'TypedUninterrupted', 'TypedRestored', 'ReceiptReplay']


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def digest(data):
    return hashlib.sha256(data).hexdigest()


def hashed(path):
    return digest(path.read_bytes())


def write(path, data):
    path.write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')


def long_path(path):
    return Path('\\\\?\\' + str(path.resolve())) if os.name == 'nt' else path.resolve()


def verify_transport(name, folder, expected_hash, count):
    archive = PACKET / name
    assert hashed(archive) == expected_hash, name
    with zipfile.ZipFile(archive) as z:
        manifest = json.loads(z.read('MANIFEST.json'))['files']
        assert len(manifest) == count
        assert len(z.namelist()) == len(set(z.namelist())) == count + 1
        assert set(z.namelist()) == {'MANIFEST.json'} | {r['path'] for r in manifest}
        for row in manifest:
            data = z.read(row['path'])
            assert len(data) == row['bytes'] and digest(data) == row['sha256'], row['path']
            assert (folder / row['path']).read_bytes() == data, row['path']
        assert (folder / 'MANIFEST.json').read_bytes() == z.read('MANIFEST.json')
    return {'path': name, 'bytes': archive.stat().st_size, 'sha256': expected_hash,
            'verifiedMembers': count, 'manifestSha256': hashed(folder / 'MANIFEST.json')}


def archive_local(verify_only):
    archive = PACKET / 'LOCAL_COMPLETION.zip'
    index = PACKET / 'LOCAL_COMPLETION.MEMBERS.json'
    entries = sorted((p.relative_to(LOCAL).as_posix(), p) for p in LOCAL.rglob('*') if p.is_file())
    members = [{'path': name, 'bytes': p.stat().st_size, 'sha256': hashed(p)} for name, p in entries]
    if verify_only:
        old = read(index)
        assert old['members'] == members
        assert old['sha256'] == hashed(archive)
    else:
        assert not archive.exists() and not index.exists(), 'Never replace retained evidence'
        with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
            for name, p in entries:
                z.writestr(name, p.read_bytes())
        write(index, {'path': archive.name, 'bytes': archive.stat().st_size,
                      'sha256': hashed(archive), 'members': members})
    with zipfile.ZipFile(archive) as z:
        assert len(z.namelist()) == len(members)
        for row in members:
            data = z.read(row['path'])
            assert len(data) == row['bytes'] and digest(data) == row['sha256']
    return {'path': archive.name, 'bytes': archive.stat().st_size, 'sha256': hashed(archive),
            'memberCount': len(members), 'index': index.name}


parser = argparse.ArgumentParser()
for flag in ['segment', 'supplement', 'delta']:
    parser.add_argument('--' + flag, type=Path, required=True)
parser.add_argument('--verify-only', action='store_true')
args = parser.parse_args()
segment, supplement, delta = [long_path(getattr(args, key)) for key in ['segment', 'supplement', 'delta']]
frozen = supplement / 'frozen-qualification-02'
archives = [
    verify_transport('SEGMENT_01.zip', segment, 'e12a4def80f10042ee83eac820c0a48daa982f28df80adf77945ac7f0ccbc234', 219),
    verify_transport('TRANSFER_SUPPLEMENT.zip', supplement, '1d97c035c7021f77db0c9c935c9043cd75f2e3cc8269216466af20da9f6cae13', 5052),
    verify_transport('CLOUD_STOP_DELTA.zip', delta, 'bbeabcd2f962725e2734b9a545dc56cd5b761c6157cbdc8cb10795bfa5c27356', 67),
]
launch = read(frozen / 'regression/LAUNCH.json')
registry = launch['cases']
assert len(registry) == len(set(registry)) == launch['count'] == 1587
case_records = {}


def case(name, path, expected_hash, origin):
    assert name in registry and name not in case_records, name
    assert hashed(path) == expected_hash
    result = read(path)
    assert result['Name'] == name and isinstance(result['Passed'], bool)
    case_records[name] = {'name': name, 'origin': origin, 'sha256': expected_hash,
                          'originalPassed': result['Passed'], 'passed': result['Passed']}
    return result


cloud = read(supplement / 'COMPLETED_CASES.json')['cases']
assert len(cloud) == 1436
for name, row in cloud.items():
    actual = case(name, supplement / row['path'], row['sha256'], 'TRANSFER_SUPPLEMENT.zip:' + row['path'])
    assert actual == row['result']
assert sum(r['passed'] for r in case_records.values()) == 1434
new = read(delta / 'NEW_TERMINAL_CASES.json')['cases']
assert len(new) == 42
for row in new:
    assert case(row['Name'], delta / row['path'], row['sha256'], 'CLOUD_STOP_DELTA.zip:' + row['path'])['Passed'] is True
missing = set(registry) - set(case_records)
assert len(missing) == 109
assert missing == set((delta / 'MISSING_CASES_AFTER_STOP.txt').read_text().splitlines())

observed_exits = read(LOCAL / 'PROCESS_COMPLETION.json')
execution = read(LOCAL / 'EXECUTION_BINDINGS.json')
for row in execution['executedSources']:
    assert hashed(ROOT / row['path']) == row['sha256']
assert execution['sourceCommit'] == SOURCE and execution['runtimeChangedLocally'] is False
path_invocations = read(LOCAL / 'PATH_INVOCATIONS.json')
assert set(path_invocations['modes']) == set(MODES)
for mode, invocation in path_invocations['modes'].items():
    assert invocation['mode'] == mode
    # Recorded execution paths identify the original Windows launch. Verification
    # may extract identical transport bytes elsewhere, including a Linux reviewer.
    recorded_root = PureWindowsPath(invocation['assemblyRoot'])
    assert recorded_root.is_absolute() and recorded_root.name == 'frozen-runtime'
    assert PureWindowsPath(invocation['finalSource']) == recorded_root.parent / 'evidence/closure/continued.ddsave'
    assert invocation['scriptSha256'] == hashed(PACKET / 'support/Test-ConnectedPaths.ps1')
    assert len(invocation['runtimeAssemblies']) == 3
    assert {r['name'] for r in invocation['runtimeAssemblies']} == {
        'Decennium.Foundation.Core.dll', 'Decennium.Foundation.Persistence.dll', 'Decennium.Foundation.LabModel.dll'}
    for row in invocation['runtimeAssemblies']:
        assert hashed(segment / 'frozen-runtime' / row['name']) == row['sha256']
        assert row['sha256'] == next(r['sha256'] for r in launch['dlls'] if r['name'] == row['name'])
assert observed_exits['typedUninterrupted']['exitCode'] == 0
assert observed_exits['remainingFourPaths']['exitCode'] == 0
workers = []
local_names = []
for i in range(3):
    folder = LOCAL / 'regression' / f'worker-{i}'
    terminal = read(folder / 'TERMINAL.json')
    plan = LOCAL / 'regression-plan' / f'worker-{i}.txt'
    names = plan.read_text(encoding='utf-8-sig').splitlines()
    assert terminal['caseListSha256'] == hashed(plan)
    assert [r['name'] for r in terminal['cases']] == names
    assert terminal['status'] == 'PASS' and terminal['registered'] == 1587
    assert terminal['completed'] == terminal['passed'] == terminal['requested'] == len(names)
    assert terminal['failed'] == 0 and observed_exits['regression'][str(i)]['exitCode'] == 0
    assert terminal['sourceCommit'] == SOURCE
    for dll in terminal['assemblies']:
        expected = next(r['sha256'] for r in launch['dlls'] if r['name'] == dll['name'])
        assert dll['sha256'] == expected
    journal = [json.loads(line) for line in (folder / 'journal.jsonl').read_text(encoding='utf-8-sig').splitlines()]
    assert [r['name'] for r in journal if r['phase'] == 'START'] == names
    results = [r for r in journal if r['phase'] == 'RESULT']
    assert [r['name'] for r in results] == names
    for row, record in zip(terminal['cases'], results):
        assert row['passed'] is True and record['passed'] is True
        assert row['resultSha256'] == record['resultSha256']
        path = folder / (row['name'] + '.json')
        assert case(row['name'], path, row['resultSha256'], 'LOCAL_COMPLETION.zip:' + path.relative_to(LOCAL).as_posix())['Passed'] is True
    local_names.extend(names)
    workers.append({'worker': i, 'count': len(names), 'passed': terminal['passed'], 'exitCode': 0,
                    'terminalSha256': hashed(folder / 'TERMINAL.json'), 'pid': terminal['pid']})
assert len(local_names) == len(set(local_names)) == 109 and set(local_names) == missing
assert set(case_records) == set(registry)

corrections = {
    'crafting_default_fingerprint_restores_and_continues_authentic_schema16_save': (
        'regression/fixture-retry/crafting_default_fingerprint_restores_and_continues_authentic_schema16_save.json',
        'Exact missing historical fixture hydrated; original runtime and testcase unchanged.'),
    'chr05_consecration_genuine_paid_zone_rite_and_expiry': (
        'corrected-tests/results/chr05_consecration_genuine_paid_zone_rite_and_expiry.json',
        'Corrected new test helper supplies required stance and stronger positive Ground/Claw assertions; runtime unchanged.'),
}
assert {name for name, row in case_records.items() if not row['passed']} == set(corrections)
for name, (relative, reason) in corrections.items():
    path = frozen / relative
    result = read(path)
    assert result['Name'] == name and result['Passed'] is True
    case_records[name]['correction'] = {'origin': 'TRANSFER_SUPPLEMENT.zip:frozen-qualification-02/' + relative,
                                       'sha256': hashed(path), 'reason': reason}
    case_records[name]['passed'] = True
assert all(r['passed'] for r in case_records.values())

reference = None
path_reports = []
for mode in MODES:
    folder = LOCAL / 'paths' / mode
    result = read(folder / 'result.json')
    assert result['mode'] == mode
    assert result['status'] == 'PASS' and result['commands'] == 428 and result['checkpoints'] == 14
    assert result['sourceSha256'] == hashed(segment / 'evidence/closure/continued.ddsave')
    assert result['seats'] == ['Player', 'FirstOpponent', 'RecoveryOpponent', 'FerryOpponent']
    files = {r['name']: r['sha256'] for r in result['files']}
    assert len(files) == len(result['files']) == 196
    for name, value in files.items():
        assert hashed(folder / name) == value, (mode, name)
    assert sum(name.endswith('.ddsave') for name in files) == 28
    assert sum(name.endswith('.json') for name in files) == 168
    if reference is None:
        reference = files
    else:
        assert files == reference, mode
    path_reports.append({'mode': mode, 'resultSha256': hashed(folder / 'result.json'),
                         'startedUtc': result['startedUtc'], 'finishedUtc': result['finishedUtc']})
path_report = {'status': 'PASS', 'paths': path_reports, 'commandsPerPath': 428, 'checkpointsPerPath': 14,
               'canonicalFilesPerPath': 28, 'seatProjectionsPerPath': 168, 'crossPathHashComparisons': 784,
               'scope': 'Five complete host/input/restore executions. Automatic actions use the actual shared controller. Canonical bytes include receipts/RNG; discovery/query parity is separately retained.'}

freeze = read(frozen / 'SOURCE_FREEZE.json')
runtime = [r for r in freeze['sourceFiles'] if r['path'].endswith('.cs') and
           any(s in r['path'] for s in ['/Runtime/Core/', '/Runtime/Persistence/', '/Laboratory/Model/'])]
assert len(runtime) == 354
requests = ''.join(SOURCE + ':' + row['path'] + '\n' for row in runtime).encode()
blobs = subprocess.check_output(['git', 'cat-file', '--batch'], input=requests, cwd=ROOT)
offset = 0
for row in runtime:
    end = blobs.index(b'\n', offset)
    _, kind, size = blobs[offset:end].split()
    assert kind == b'blob'
    offset = end + 1
    data = blobs[offset:offset + int(size)]
    offset += int(size) + 1
    assert digest(data) == row['sha256'] == hashed(ROOT / row['path'])
changed = {r['path'] for r in freeze['sourceFiles'] if hashed(ROOT / r['path']) != r['sha256']}
assert changed == {'engine/com.decennium.foundation/Tests/EditMode/ConsecrationCases.cs', 'engine/tools/Open-ConnectedExpedition.ps1'}
corrected = read(frozen / 'corrected-tests/compile.json')
assert corrected['exitCode'] == 0 and len(corrected['sources']) == 118
for row in corrected['sources']:
    assert hashed(ROOT / 'engine/com.decennium.foundation/Tests/EditMode' / row['name']) == row['sha256']
for row in launch['dlls']:
    path = frozen / 'build/run-20261117T185236951Z-452d89f7' / row['name']
    assert hashed(path) == row['sha256']
for row in corrected['dlls']:
    assert hashed(frozen / 'corrected-tests' / row['name']) == row['sha256']
    if 'HeadlessTests' not in row['name']:
        assert row['sha256'] == next(r['sha256'] for r in launch['dlls'] if r['name'] == row['name'])
        assert hashed(segment / 'frozen-runtime' / row['name']) == row['sha256']

focused_names = ['public-continuation', 'closure', 'outside', 'cap-supplement-v3', 'controls', 'focused-controls-v5',
                 'owner-movement', 'backup', 'compatibility95-104', 'compatibility105-114', 'query-parity']
focused = []
for name in focused_names:
    path = frozen / name / 'result.json'
    assert read(path)['status'].startswith('PASS'), name
    focused.append({'path': 'TRANSFER_SUPPLEMENT.zip:frozen-qualification-02/' + name + '/result.json', 'sha256': hashed(path)})
assert read(frozen / 'cap-genuine/result.json')['disposition'] == 'UNPROVED_ACTUAL_CAP_INTERSECTION'
assert read(frozen / 'console/VALIDATION.json')['status'].startswith('PASS')
parity = read(frozen / 'query-parity/result.json')
assert len(parity['checkpoints']) == 6
assert sum(r['discoveryPairs'] for r in parity['checkpoints']) == 72
assert sum(r['queries'] for r in parity['checkpoints']) == 712
assert all(r['canonicalUnchanged'] for r in parity['checkpoints'])
auth = read(supplement / 'AUTHENTIC_INPUT_BINDINGS.json')
auth_archives = {
    'compatibility.zip': ROOT / 'docs/unity/evidence/2026-11-16-tac10-ferry-wraith-runtime/compatibility-checkpoint/compatibility.zip',
    'ferry-paths.zip': ROOT / 'docs/unity/evidence/2026-11-16-tac10-ferry-wraith-runtime/five-path-checkpoint/five-paths.zip',
}
for row in auth['archives']:
    assert auth_archives[row['path']].stat().st_size == row['bytes']
    assert hashed(auth_archives[row['path']]) == row['sha256']
compat = [r for name in ['compatibility95-104', 'compatibility105-114'] for r in read(frozen / name / 'result.json')['cases']]
assert {r['wire'] for r in compat} == set(range(95, 115)) and len(compat) == 20
for row in compat:
    assert row['canonicalEqual'] is True and row['rejectedBy115'] is True
    for key in ['before', 'after']:
        binding = next(r for r in auth['selections'] if r['member'] == row[key])
        path = supplement / f"selected-authentic-inputs/wire{row['wire']}/{key}.ddsave"
        assert hashed(path) == binding['sha256']
        with zipfile.ZipFile(auth_archives[binding['archive']]) as z:
            assert z.read(binding['member']) == path.read_bytes()

builds = list((LOCAL / 'build').glob('run-*/results.json'))
packages = list((LOCAL / 'package').glob('static-*/results.json'))
assert len(builds) == len(packages) == 1
build, package = read(builds[0]), read(packages[0])
assert build['status'] == build['coreCompilation'] == package['status'] == 'PASS'
assert build['testsDiscovered'] == build['passed'] == 1 and build['failed'] == 0
assert build['language'] == 'C# 9'

regression = {'status': 'PASS_COMPOSITE_RECONCILIATION', 'registered': 1587, 'originalAndResumedRecords': 1436,
              'originalAndResumedRawPassed': 1434, 'deltaPassed': 42, 'localRemainingPassed': 109,
              'explicitPassingCorrections': 2, 'reconciledPassed': 1587, 'missing': [],
              'workers': workers, 'cases': [case_records[name] for name in registry],
              'cloudProcessStatus': 'Preserve TRANSFER_STATUS.json and STOP_AND_DELTA_STATUS.json: known resumed parent exit130; older nonterminal worker/path exits unknown. Composite case coverage is not a claim of original suite termination.'}
if not args.verify_only:
    write(LOCAL / 'paths/COMPARISON.json', path_report)
    write(PACKET / 'REGRESSION_RECONCILIATION.json', regression)
else:
    assert read(LOCAL / 'paths/COMPARISON.json') == path_report
    assert read(PACKET / 'REGRESSION_RECONCILIATION.json') == regression
archives.append(archive_local(args.verify_only))
report = {'status': 'COMPLETE_EVIDENCE_CANDIDATE_PENDING_ACTUAL_REVIEW', 'sourceCommit': SOURCE,
          'runtimeCSharpInputsUnchanged': 354, 'correctedTestCSharpInputs': 118,
          'regression': {k: v for k, v in regression.items() if k != 'cases'},
          'fivePaths': path_report, 'focusedResults': focused, 'discoveryPairs': 72, 'directQueries': 712,
          'authenticCompatibilityProfiles': list(range(95, 115)), 'archives': archives,
          'windowsBuild': {'path': 'LOCAL_COMPLETION.zip:' + builds[0].relative_to(LOCAL).as_posix(), 'sha256': hashed(builds[0]),
                           'scope': 'Four-assembly C#9 compilation plus one named smoke case. Full composite regression and five paths use the original frozen cloud assemblies, not these newly compiled DLLs.'},
          'packageCheck': {'path': 'LOCAL_COMPLETION.zip:' + packages[0].relative_to(LOCAL).as_posix(), 'sha256': hashed(packages[0])},
          'genuineCombinedCapCure': 'UNPROVED; accepted bounded mechanical allocation does not adopt modified campaign state or prove persisted idempotency from a direct repeat.',
          'outsideSettledOwnerSlot': 'Unsupported broader mandatory integration gap CG-CONTEXT-01; not a source prohibition.',
          'moduleAccepted': False, 'wholeWorkstreamComplete': False, 'wholeEngineComplete': False,
          'referencePerformanceQualified': False, 'unityQualified': False}
if args.verify_only:
    assert read(PACKET / 'QUALIFICATION_INDEX.json') == report
else:
    write(PACKET / 'QUALIFICATION_INDEX.json', report)
print('PASS: exact retained transport/source/build identities; 1587 reconciled cases; five complete 428-command paths and 784 cross-path comparisons. Actual final review remains required.')
