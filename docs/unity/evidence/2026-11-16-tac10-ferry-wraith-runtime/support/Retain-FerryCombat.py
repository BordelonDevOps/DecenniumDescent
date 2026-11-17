"""Retain a partial TAC-10 implementation checkpoint; never module acceptance."""
import hashlib
import json
from pathlib import Path
import subprocess
import zipfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
BASELINE = '11a4f4fc278a3a580a6fd63b9e54f55390811c0f'
DEVELOPMENT = ROOT / 'engine/artifacts/ferry-wraith/development'
BUILD = DEVELOPMENT / 'run-20261117T055031092Z-872e0488'
COMBAT = DEVELOPMENT / 'combat-probe-20261117T0552Z'
GENESIS = DEVELOPMENT / 'genesis-probe-20261117T0552Z'
STATIC = ROOT / 'engine/artifacts/static-20261117T055238271Z-229b4a46'
OUT = HERE.parent / 'combat-checkpoint'

def digest(raw): return hashlib.sha256(raw).hexdigest()
def read(path): return json.loads(path.read_text(encoding='utf-8-sig'))

def main():
    assert not OUT.exists(), 'Retained checkpoints are immutable.'
    build, combat, genesis, static = [read(x / n) for x, n in
        [(BUILD, 'results.json'), (COMBAT, 'RESULT.json'), (GENESIS, 'RESULT.json'), (STATIC, 'results.json')]]
    assert build['status'] == 'PASS' and build['testsDiscovered'] == build['passed'] == 1 and build['failed'] == 0
    assert len(build['sourceHashes']) == 465
    assert combat['status'] == 'PASS_DEVELOPMENT_COMBAT_ONLY' and len(combat['cases']) == 8
    assert [x['Name'] for x in combat['cases']] == combat['selected'] and all(x['Passed'] for x in combat['cases'])
    assert genesis['status'] == 'PASS_DEVELOPMENT_GENESIS_ONLY' and len(genesis['checks']) == 7
    assert static['status'] == 'PASS'
    for row in build['sourceHashes']:
        assert digest((ROOT / 'engine' / row['path']).read_bytes()) == row['sha256'], row['path']
    for report in (combat, genesis):
        assert report['compilationReport']['sha256'] == digest((BUILD / 'results.json').read_bytes())
        for row in report['assemblies']:
            assert digest((BUILD / ('Decennium.Foundation.' + row['name'] + '.dll')).read_bytes()) == row['sha256']
    assert digest(Path(combat['executedScript']['path']).read_bytes()) == combat['executedScript']['sha256']
    for row in genesis['executedSources']:
        assert digest((ROOT / row['path']).read_bytes()) == row['sha256']
    saves = ['typed-genesis.ddsave', 'typed-restored.ddsave', 'console-genesis.ddsave', 'console-restored.ddsave', 'typed-after-probes.ddsave']
    assert all(digest((GENESIS / name).read_bytes()) == genesis['genesisSha256'] for name in saves)
    changed = set(subprocess.check_output(['git', 'diff', BASELINE, '--name-only', '--', 'engine'], cwd=ROOT).decode().splitlines())
    for path in ['Runtime/Core/TypedDamageRecords.cs', 'Laboratory/Model/SharedTypedDamage.cs', 'Tests/EditMode/FerryWraithCases.cs']:
        for suffix in ('', '.meta'):
            changed.add('engine/com.decennium.foundation/' + path + suffix)
    assert len(changed) == 19, sorted(changed)
    members = {}
    def add(name, path):
        assert name not in members
        members[name] = path.read_bytes()
    for name, folder in [('selected-build', BUILD), ('combat-probe', COMBAT), ('genesis-probe', GENESIS), ('static', STATIC)]:
        for path in sorted(folder.rglob('*')):
            if path.is_file(): add(name + '/' + path.relative_to(folder).as_posix(), path)
    for failed in ['run-20261117T054915873Z-90c5558a', 'run-20261117T054915865Z-c01fbe66']:
        report = read(DEVELOPMENT / failed / 'results.json')
        assert report['status'] == 'FAIL' and report['testsDiscovered'] == 0
        for name in ['results.json', 'FerryWraithCases.failed.cs']:
            add('development-failures/' + failed + '/' + name, DEVELOPMENT / failed / name)
    add('earlier-runtime-compile/results.json', DEVELOPMENT / 'compile-20261117T054633853Z-dd5a5e09/results.json')
    for path in sorted(changed): add('changed-source/' + path, ROOT / path)
    for path in [Path(__file__), HERE / 'Probe-FerryCombat.ps1', HERE / 'Probe-FerryGenesis.ps1', ROOT / 'engine/tools/Test-Foundation.ps1', ROOT / 'engine/tools/Validate-Package.ps1', ROOT / 'engine/tools/Open-ConnectedExpedition.ps1']:
        add('executed-support/' + path.name, path)
    manifest = [dict(path=name, bytes=len(raw), sha256=digest(raw)) for name, raw in sorted(members.items())]
    OUT.mkdir()
    archive = OUT / 'development-combat.zip'
    with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as output:
        for name, raw in sorted(members.items()):
            info = zipfile.ZipInfo(name, (2026, 11, 17, 0, 0, 0)); info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            output.writestr(info, raw)
    with zipfile.ZipFile(archive) as check:
        assert check.namelist() == [x['path'] for x in manifest]
        for row in manifest: assert digest(check.read(row['path'])) == row['sha256']
    result = dict(status='PASS_RETAINED_PARTIAL_IMPLEMENTATION_NOT_MODULE_ACCEPTANCE', sourceBaseline=BASELINE,
        acceptedPredecessorEngine='7261052ae4dec908f8c0ac38e0a2c5f4b831065b', selectedBuild=BUILD.relative_to(ROOT).as_posix(),
        compiledSourceInputs=465, changedEngineFiles=len(changed), selectedCasesPassed=9, newCases=2, predecessorCases=7,
        genesisChecks=7, genesisSha256=genesis['genesisSha256'], archiveSha256=digest(archive.read_bytes()),
        members=len(manifest), uncompressedBytes=sum(x['bytes'] for x in manifest), archiveBytes=archive.stat().st_size,
        fullRegression=False, connectedCreatureEncounter=False, actualModuleReview=False, moduleAccepted=False,
        scriptSha256=digest(Path(__file__).read_bytes()))
    (OUT / 'MEMBERS.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    (OUT / 'RETENTION.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result))

if __name__ == '__main__': main()
