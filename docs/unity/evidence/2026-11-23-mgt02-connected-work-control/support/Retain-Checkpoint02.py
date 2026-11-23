from pathlib import Path
import hashlib
import json
import zipfile

root = Path(__file__).resolve().parents[5]
packet = Path(__file__).resolve().parent.parent
artifacts = root / 'engine/artifacts/connected-work-control'
runs = [
    'development-05/run-20261123T192239273Z-67284f93',
    'development-06/run-20261123T192507880Z-324080b9',
    'development-07/run-20261123T192652314Z-c196d3fe',
    'focused-02', 'focused-03', 'console-01', 'console-02',
    'static-20261123T192945542Z-0328cb41',
]
digest = lambda data: hashlib.sha256(data).hexdigest()
members = []
archive = packet / 'DEVELOPMENT_CHECKPOINT_02.zip'
with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as out:
    for run in runs:
        folder = artifacts / run
        assert folder.is_dir(), run
        for source in sorted(folder.rglob('*')):
            if not source.is_file():
                continue
            data = source.read_bytes()
            name = source.relative_to(root).as_posix()
            out.writestr(name, data)
            members.append({'path': name, 'bytes': len(data), 'sha256': digest(data)})
with zipfile.ZipFile(archive) as check:
    for member in members:
        assert digest(check.read(member['path'])) == member['sha256']
index = {'archive': archive.name, 'bytes': archive.stat().st_size,
         'sha256': digest(archive.read_bytes()), 'memberCount': len(members), 'members': members}
(packet / 'DEVELOPMENT_CHECKPOINT_02_INDEX.json').write_text(json.dumps(index, indent=2) + '\n', encoding='utf-8')
report = {
    'status': 'PARTIAL_IMPLEMENTATION_CHECKPOINT_NOT_MODULE_ACCEPTANCE',
    'module': 'MGT-02-CONNECTED-WORK-CONTROL',
    'contractSha256': 'd65c7bcdf6c9ade960e70b527c82d71c367e4f883d180d91f0b299c8e13d8819',
    'actualGptCheckpointResponse': '312d397f-5c18-5f16-8f5d-2843f9ded0cf',
    'implemented': [
        'Current-authority receipt queries preserve exact/conflicting semantics after target visibility loss',
        'Pure fill Start/Resume assessment checks actual added records against existing32-fill and128-reservation/booking bounds',
        'Separate immutable ObserveWork DTOs for exact labor/retention/remaining/phases, owner-filtered claims, future bookings and pending states',
        'Water exact-rational examples/parameter bounds and observed mining category/unit/ability/hurry descriptors; native queries determine admissibility',
        'All four work-family control candidates query native rules; new-profile generic/casting discovery aliases agree',
        'Console ConnectedWorkControl selector/query/discover/work and inherited feature flags; new-profile summary fill rows',
    ],
    'qualification': {
        'sourceRun': runs[2], 'compiledSources': 486, 'fourAssemblyCSharp9WarningsAsErrors': 'PASS',
        'frozenSourceArchiveSha256': 'e55402975e2416a880bb1d9c5ffca97fdc37f29974dbeb9f34922c096cb76b72',
        'focusedAssigned': 63, 'focusedPassed': 63, 'focusedFailed': 0, 'totalDiscovered': 1598,
        'newCases': 6, 'oldSelectedCases': 57, 'static': 'PASS',
        'console': {'status': 'PASS', 'responsesCompared': 17, 'completeResponses': 15,
                    'explicitlyProjectedViewComparisons': 2, 'projectionFields': ['Actors', 'LongRest', 'Work', 'Commands'],
                    'byteIdenticalSnapshotPairs': 2, 'saveRestoreContinuation': True,
                    'lawfulDefenderConsoleContinuations': 'NOT_YET_EXERCISED'},
        'genuineHostBounds': ['32 real start/cancel histories reject33 without eviction',
                             '128 real productive booking intervals reject129 with exact16/125 seconds retained'],
        'mechanicalOnly': '128 released reservation arrangement is a detached model assessment, never restored/imported to a host and not a causal gameplay witness',
        'allProcessesTerminal': True,
    },
    'retainedFailures': [
        {'run': runs[0], 'exitCode': 1, 'cause': 'C# projection omitted WorkerInterval to immutable booking DTO conversion; corrected'},
        {'run': 'console-01', 'exitCode': 1, 'cause': 'Driver expected discovery omitted console explicit Consecrate DTO; driver-only correction, no engine change'},
    ],
    'remaining': [
        'Genuine connected principal mine/research/batch/use actual output/encounter/fill-magic-continue route',
        'All-family lifecycle and cancellation branches, mining commitment and manufacturing loss boundaries',
        'Allocated pending-check model cases and explicit genuine-host limitations',
        'Authority/privacy/save-forgery/backup/authentic95-116 compatibility and full five paths',
        'Full1592 predecessors plus all new cases on final frozen source, actual GPT final review and concurrence',
    ],
    'evidenceArchive': {k: v for k, v in index.items() if k != 'members'},
    'runtimeAccepted': False, 'unityAuthorized': False,
}
(packet / 'DEVELOPMENT_CHECKPOINT_02.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
print(json.dumps(report['evidenceArchive']))
