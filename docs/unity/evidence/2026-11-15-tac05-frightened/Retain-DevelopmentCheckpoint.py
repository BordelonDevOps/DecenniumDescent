"""Retain a source-bound TAC05 implementation checkpoint; this is not final acceptance."""
from pathlib import Path
import datetime
import hashlib
import json
import shutil

packet = Path(__file__).resolve().parent
root = packet.parents[3]
development = root / 'engine/artifacts/tac05-frightened/development'
output = packet / 'development-checkpoint'
output.mkdir(exist_ok=True)

def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

builds = {
    'headless.json': 'run-20261115T093650131Z-40129a7c/results.json',
    'connected-main.json': 'case-20261115T093927408Z/results.json',
    'standalone.json': 'compile-20261115T093927386Z-07dca160/results.json',
}
reports = {
    **builds,
    'static.json': 'static/static-20261115T093927415Z-c23a0399/results.json',
    'focused-controls.json': 'source-integration-controls.json',
    'paths-main.json': 'paths-main-20261115T093859999Z/results.json',
    'paths-ability-check.json': 'paths-ability-check/results.json',
    'paths-sight-loss.json': 'paths-sight-loss/results.json',
    'historical-forgery.json': 'historical-check-controls/results.json',
    'clock-components.json': 'clock-components-3/results.json',
    'projection-controls.json': 'projection-controls/results.json',
    'forced-movement-controls.json': 'forced-movement-controls-2/results.json',
    'console-probe.json': 'console-source-probe/results.json',
}
retained = []
for name, relative in reports.items():
    source = development / relative
    report = read(source)
    assert report.get('status', report.get('Status')) == 'PASS', relative
    if name in builds:
        for item in report['sourceHashes']:
            assert sha(root / 'engine' / item['path'].replace('\\', '/')) == item['sha256'].lower(), item['path']
    target = output / name
    shutil.copyfile(source, target)
    retained.append(dict(path=target.relative_to(packet).as_posix(), sha256=sha(target), source=relative))
for name, relative in {
    'inventory.txt': 'source-integration-inventory.txt',
    'consumer-scope-progress.json': 'consumer-scope-progress.json',
    'regression-launch.json': 'regression/launch.json',
    'regression-processes.json': 'regression/processes.json',
}.items():
    target = output / name
    shutil.copyfile(development / relative, target)
    retained.append(dict(path=target.relative_to(packet).as_posix(), sha256=sha(target), source=relative))
progress = read(development / 'IMPLEMENTATION_PROGRESS.json')
for item in progress['sourceFiles']:
    assert sha(root / item['path']) == item['sha256'], item['path']
manifest = dict(status='IMPLEMENTATION_CHECKPOINT_NOT_ACCEPTED', atUtc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
    authorityCommit='d9ad3db339f0da613690e7de9c497f77b8221c71', actualContractReview='226d668a-fd32-51b3-b64c-bbd74b67e64c',
    implementationSource='Exact source hashes below; this checkpoint travels with the implementation commit.',
    sourceFiles=progress['sourceFiles'], retained=retained, focusedPassed=132, registeredCases=1517,
    connectedCheckpoints=19, fivePathComparisons=95, fullRegression='RUNNING_FIXED_DLLS_NOT_A_PASS',
    authenticCompatibility='RUNNING_NOT_A_PASS', finalReview='NOT_REQUESTED', successor='CHR03_HELD')
(output / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
print(json.dumps(dict(status=manifest['status'], sourceFiles=len(manifest['sourceFiles']), retainedReports=len(retained))))
