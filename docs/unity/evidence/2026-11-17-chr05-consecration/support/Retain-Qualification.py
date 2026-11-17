"""Retain completed evidence and verify exact member hashes; never runs gameplay."""
from pathlib import Path
import hashlib
import json
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[5]
PACKET = Path(__file__).resolve().parents[1]
ART = ROOT / 'engine/artifacts/consecration'
FROZEN = ART / 'frozen-qualification-02'
SOURCE = '3c5135ae0d664d79528fff1f2676fae2198beb28'

def read(p):
    return json.loads(p.read_text(encoding='utf-8-sig'))

def sha(data):
    return hashlib.sha256(data).hexdigest()

def archive(name, entries):
    target = PACKET / (name + '.zip')
    members = []
    assert not target.exists(), 'Never silently replace a retained archive'
    with zipfile.ZipFile(target, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as out:
        for relative, path in sorted(entries.items()):
            data = path.read_bytes()
            out.writestr(relative, data)
            members.append({'path': relative, 'bytes': len(data), 'sha256': sha(data)})
    with zipfile.ZipFile(target) as check:
        assert len(check.namelist()) == len(members)
        for item in members:
            assert sha(check.read(item['path'])) == item['sha256']
    report = {'path': target.name, 'bytes': target.stat().st_size, 'sha256': sha(target.read_bytes()), 'members': members}
    (PACKET / (name + '.MEMBERS.json')).write_text(json.dumps(report, indent=2) + '\n')
    return {k: v for k, v in report.items() if k != 'members'} | {'memberCount': len(members)}

def files(folder, prefix=None):
    return {(prefix + '/' if prefix else '') + p.relative_to(folder).as_posix(): p for p in folder.rglob('*') if p.is_file()}

original = read(FROZEN / 'regression/RESULT.json')
assert original['count'] == 1587
cases = []
for i in range(6):
    terminal = read(FROZEN / f'regression/worker-{i}/TERMINAL.json')
    assert terminal['count'] == len(terminal['cases'])
    cases.extend(terminal['cases'])
assert len(cases) == len({r['Name'] for r in cases}) == 1587
assert set(r['Name'] for r in cases) == set(original['cases'])
expected = {
    'crafting_default_fingerprint_restores_and_continues_authentic_schema16_save': FROZEN / 'regression/fixture-retry/crafting_default_fingerprint_restores_and_continues_authentic_schema16_save.json',
    'chr05_consecration_genuine_paid_zone_rite_and_expiry': FROZEN / 'corrected-tests/results/chr05_consecration_genuine_paid_zone_rite_and_expiry.json',
}
assert {r['Name'] for r in cases if not r['Passed']} == set(expected)
overrides = []
for name, path in expected.items():
    result = read(path)
    assert result['Name'] == name and result['Passed'] is True
    overrides.append({'case': name, 'result': path.relative_to(ART).as_posix(), 'sha256': sha(path.read_bytes()),
                      'correction': 'Exact missing historical fixture hydrated; runtime unchanged' if name.startswith('crafting_') else 'New test helper supplies required stance; runtime unchanged; stronger positive Ground/Claw assertions'})

modes = ['ConsoleUninterrupted', 'ConsoleRestored', 'TypedUninterrupted', 'TypedRestored', 'ReceiptReplay']
reference = None
comparisons = 0
for mode in modes:
    folder = FROZEN / 'paths' / mode
    result = read(folder / 'result.json')
    assert result['status'] == 'PASS' and result['commands'] == 428 and result['checkpoints'] == 14
    observed = {r['name']: r['sha256'] for r in result['files']}
    assert len(observed) == 196
    for name, value in observed.items():
        assert sha((folder / name).read_bytes()) == value
    if reference is None:
        reference = observed
    else:
        assert observed == reference, mode
        comparisons += len(reference)
path_result = {'status': 'PASS', 'modes': modes, 'commandsPerPath': 428, 'checkpointsPerPath': 14,
               'canonicalFilesPerPath': 28, 'seatProjectionsPerPath': 168, 'crossPathHashComparisons': comparisons,
               'scope': 'Five complete independent host/input/restore paths. Automatic actions reuse the actual controller. Canonical bytes include receipts/RNG; full ordered discovery/query/denial/retry parity is a separate supplemental run.'}
(FROZEN / 'paths/COMPARISON.json').write_text(json.dumps(path_result, indent=2) + '\n')

required = ['public-continuation', 'closure', 'outside', 'cap-supplement-v3', 'controls', 'focused-controls-v5',
            'owner-movement', 'backup', 'compatibility95-104', 'compatibility105-114', 'query-parity']
for name in required:
    assert read(FROZEN / name / 'result.json')['status'].startswith('PASS'), name
assert read(FROZEN / 'cap-genuine/result.json')['disposition'] == 'UNPROVED_ACTUAL_CAP_INTERSECTION'
assert read(FROZEN / 'console/VALIDATION.json')['status'].startswith('PASS')
static = list((ART / 'package-final').glob('static-*/results.json'))
assert len(static) == 1 and read(static[0])['status'] == 'PASS'

freeze = read(FROZEN / 'SOURCE_FREEZE.json')
allowed = {'engine/com.decennium.foundation/Tests/EditMode/ConsecrationCases.cs', 'engine/tools/Open-ConnectedExpedition.ps1'}
different = {r['path'] for r in freeze['sourceFiles'] if sha((ROOT / r['path']).read_bytes()) != r['sha256']}
assert different == allowed
corrected = read(FROZEN / 'corrected-tests/compile.json')
assert corrected['exitCode'] == 0
for row in corrected['sources']:
    assert sha((ROOT / 'engine/com.decennium.foundation/Tests/EditMode' / row['name']).read_bytes()) == row['sha256']
assert len(corrected['sources']) == 118
runtime_paths = [r for r in freeze['sourceFiles'] if r['path'].endswith('.cs') and any(s in r['path'] for s in ['/Runtime/Core/', '/Runtime/Persistence/', '/Laboratory/Model/'])]
assert len(runtime_paths) == 354
for row in runtime_paths:
    committed = subprocess.check_output(['git', 'show', SOURCE + ':' + row['path']], cwd=ROOT)
    assert sha(committed) == row['sha256']

source_entries = files(FROZEN / 'source', 'source') | files(FROZEN / 'build', 'build')
source_entries['SOURCE_FREEZE.json'] = FROZEN / 'SOURCE_FREEZE.json'
for path in (FROZEN / 'corrected-tests').rglob('*'):
    if path.is_file() and 'results' not in path.relative_to(FROZEN / 'corrected-tests').parts:
        source_entries['corrected-tests/' + path.relative_to(FROZEN / 'corrected-tests').as_posix()] = path
source_entries['qualified-console/Open-ConnectedExpedition.ps1'] = ROOT / 'engine/tools/Open-ConnectedExpedition.ps1'
archives = [archive('source-build-and-drivers', source_entries)]

runs = {}
for name in required + ['public-prefix', 'cap-genuine', 'console']:
    runs.update(files(FROZEN / name, name))
runs.update(files(FROZEN / 'corrected-tests/results', 'corrected-tests'))
runs.update(files(ART / 'package-final', 'static-package'))
for name in ['prefix-receipts.json', 'recovery-prefix-receipts.json', 'cap-prefix-receipts.json']:
    runs[name] = ART / name
archives.append(archive('qualified-runs', runs))
archives.append(archive('terminal-regression', files(FROZEN / 'regression')))
archives.append(archive('five-paths', files(FROZEN / 'paths')))

attempts = {}
for folder in ['baseline', 'baseline-retry', 'development', 'development-corrected', 'development-resumed', 'frozen-qualification-01',
               'isolated-build', 'isolated-build-audited', 'isolated-build-corrected', 'prescribed', 'package', 'package-current']:
    attempts.update(files(ART / folder, folder))
for folder in ['cap-supplement', 'focused-controls-v2', 'focused-controls-v3', 'focused-controls-v4', 'path-progress-diagnostic', 'path99-diagnostic', 'runtime-diagnostic', 'clock-diagnostic']:
    attempts.update(files(FROZEN / folder, 'frozen02/' + folder))
for path in ART.glob('*.log'):
    attempts[path.name] = path
archives.append(archive('development-attempts', attempts))

auth = read(ART / 'authentic-inputs/SAVES.json')
selected = {}
bindings = []
for folder in ['compatibility95-104', 'compatibility105-114']:
    for case in read(FROZEN / folder / 'result.json')['cases']:
        for key in ['before', 'after']:
            row = next(r for r in auth if r['member'] == case[key])
            path = Path(row['path'])
            assert sha(path.read_bytes()) == row['sha256']
            with zipfile.ZipFile(ART / 'authentic-inputs' / row['archive']) as original_archive:
                assert original_archive.read(row['member']) == path.read_bytes()
            entry = f"wire{case['wire']}/{key}.ddsave"
            selected[entry] = path
            bindings.append({'entry': entry, 'archive': row['archive'], 'member': row['member'], 'sha256': row['sha256']})
(PACKET / 'AUTHENTIC_INPUT_BINDINGS.json').write_text(json.dumps({'selections': bindings,
    'archives': [{'path': p.name, 'sha256': sha(p.read_bytes())} for p in sorted((ART / 'authentic-inputs').glob('*.zip'))]}, indent=2) + '\n')
archives.append(archive('selected-authentic-inputs', selected))

report = {'status': 'COMPLETE_EVIDENCE_CANDIDATE_PENDING_ACTUAL_REVIEW', 'sourceCommit': SOURCE,
          'runtimeCSharpInputsUnchanged': 354, 'compiledCSharpInputs': 472,
          'originalRegression': {'registered': 1587, 'passed': sum(r['Passed'] for r in cases), 'failed': len(expected)},
          'explicitCorrections': overrides, 'reconciledRegressionPassed': 1587,
          'fivePaths': path_result, 'archives': archives, 'genuineCombinedCapCure': 'UNPROVED',
          'mechanicalAllocation': 'Accepted bounded composition; no modified campaign adoption or persisted idempotency from direct repeat',
          'moduleAccepted': False, 'wholeWorkstreamComplete': False, 'wholeEngineComplete': False,
          'referencePerformanceQualified': False, 'unityQualified': False}
(PACKET / 'QUALIFICATION_INDEX.json').write_text(json.dumps(report, indent=2) + '\n')
print('PASS retained complete evidence candidate; actual final module review remains required.')
