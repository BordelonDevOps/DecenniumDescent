"""Reconcile and retain the completed, source-bound Ferry five-path execution."""
import hashlib
import json
from pathlib import Path
import subprocess
import zipfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
PACKET = HERE.parent
ART = ROOT / 'engine/artifacts/ferry-wraith/dash-correction'
BUILD = ART / 'run-20261117T110451175Z-06a69ef8'
RUN = ART / 'five-paths-20261117T122438Z'
REFERENCE = ART / 'five-path-reference-20261117T121519Z'
EXPORT = ART / 'five-path-export-20261117T121519Z'
OUT = PACKET / 'five-path-checkpoint'
TREE = 'c8ffee78d5047131317ff923c8e3a575b6c51f3a'
HOST = '3d0afc12d2444d2d6d77e3ff3729f2ff8236be3d'
FINAL = '71420605e7a45a2168fac7f1c2dd7a6bacf142242261a6aab5f91d827b185dd8'


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def git(path, commit='HEAD'):
    return subprocess.check_output(['git', '-C', str(ROOT), 'show', commit + ':' + path])


def main():
    assert not OUT.exists(), 'Never overwrite retained qualification.'
    members, bindings = {}, {}
    compiled = read(BUILD / 'results.json')
    assert compiled['status'] == compiled['coreCompilation'] == 'PASS'
    assert len(compiled['sourceHashes']) == 468
    for row in compiled['sourceHashes']:
        name = 'engine/' + row['path'].replace('\\', '/')
        assert sha(git(name, TREE)) == sha((ROOT / name).read_bytes()) == row['sha256']
    prior = read(PACKET / 'public-dash-checkpoint/RETENTION.json')
    binary_archive = PACKET / 'public-dash-checkpoint/public-dash.zip'
    assert sha(binary_archive.read_bytes()) == prior['archiveSha256']
    report, manifest, exported = read(RUN / 'results.json'), read(REFERENCE / 'manifest.json'), read(EXPORT / 'source.json')
    assert report['status'] == 'PASS' and manifest['status'] == 'PASS_REFERENCE'
    assert manifest['revision'] == exported['revision'] == 463
    assert manifest['finalSha256'] == exported['sourceSha256'] == FINAL
    assert sha(Path(exported['source']).read_bytes()) == FINAL
    assert sha((REFERENCE / 'inputs.jsonl').read_bytes()) == report['traceSha256']
    assert sha((EXPORT / 'inputs.jsonl').read_bytes()) == manifest['inputSha256']
    assert len(read(EXPORT / 'all-command-receipts.json')) == 463
    with zipfile.ZipFile(binary_archive) as archive:
        for row in report['assemblies']:
            filename = 'Decennium.Foundation.' + row['name'] + '.dll'
            assert row['sha256'] == sha((BUILD / filename).read_bytes()) == sha(archive.read('focused-build/' + filename))
        assert sorted(report['assemblies'], key=lambda r: r['name']) == sorted(manifest['assemblies'], key=lambda r: r['name'])
    for directory in (RUN, REFERENCE):
        before, after = read(directory / 'execution-sources.before.json'), read(directory / 'execution-sources.after.json')
        assert after['status'] == 'PASS' and before['pid'] == after['pid'] and before['files'] == after['files']
        for row in before['files']:
            raw = (ROOT / row['path']).read_bytes()
            assert len(raw) == row['bytes'] and sha(raw) == row['sha256'] and git(row['path']) == raw
            bindings[row['path']] = row['sha256']
            members['executed-sources/' + row['path']] = raw
    assert sha(git('engine/tools/Open-ConnectedExpedition.ps1', HOST)) == bindings['engine/tools/Open-ConnectedExpedition.ps1']
    for filename in ('Export-FerryTrace.ps1', 'Ferry-TraceCommand.ps1', 'Ferry-TypedCommand.ps1'):
        raw = (EXPORT / filename).read_bytes()
        assert raw == git((HERE / filename).relative_to(ROOT).as_posix())
    modes = ['ConsoleUninterrupted', 'ConsoleRestored', 'TypedUninterrupted', 'TypedRestored', 'ReceiptReplay']
    assert list(report['paths']) == modes
    assert len(manifest['marks']) == 21
    probes, comparisons = 0, 0
    for mark in manifest['marks']:
        assert list(mark['views']) == ['Player', 'FirstOpponent', 'RecoveryOpponent', 'FerryOpponent']
        expected = {mark['name']: mark['sha256']}
        expected.update({view['name']: view['sha256'] for view in mark['views'].values()})
        expected.update({probe['request']['evidenceRead']: probe['sha256'] for probe in mark['probes']})
        assert len(expected) == 5 + len(mark['probes'])
        probes += len(mark['probes'])
        for folder in [REFERENCE] + [RUN / mode for mode in modes]:
            for name, digest in expected.items():
                assert sha((folder / name).read_bytes()) == digest, str(folder / name)
                if folder != REFERENCE:
                    assert report['paths'][folder.name]['checkpoints'][name] == digest
                    comparisons += 1
            assert (folder / mark['name']).read_bytes() == (folder / (mark['name'] + '.after-probes.ddsave')).read_bytes()
    for mode in modes:
        assert report['paths'][mode]['commands'] == 463
        assert len(report['paths'][mode]['checkpoints']) == 21 * 5 + probes
        if mode.startswith('Console'):
            requests = [json.loads(line) for line in (RUN / mode / 'inputs.jsonl').read_text(encoding='utf-8-sig').splitlines()]
            responses = [json.loads(line) for line in (RUN / mode / 'responses.jsonl').read_text(encoding='utf-8-sig').splitlines()]
            assert len(requests) == len(responses) == report['paths'][mode]['inputs']
            committed = [r for q, r in zip(requests, responses) if q['op'] not in ('save', 'load', 'view') and not q.get('evidenceRead')]
            assert all(r['Response'] == 'Committed' for r in committed)
            assert [r['Revision'] for r in committed] == list(range(1, 464))
        elif mode.startswith('Typed'):
            responses = read(RUN / mode / 'responses.json')
            assert len(responses) == 463 and all(r['Response'] == 'Committed' for r in responses)
            assert [r['Revision'] for r in responses] == list(range(1, 464))
    for label, directory in [('paths', RUN), ('reference', REFERENCE), ('export', EXPORT)]:
        for path in sorted(directory.rglob('*')):
            if path.is_file():
                members[label + '/' + path.relative_to(directory).as_posix()] = path.read_bytes()
    members['support/Retain-FerryFivePaths.py'] = Path(__file__).read_bytes()
    members['references/public-dash-RETENTION.json'] = (PACKET / 'public-dash-checkpoint/RETENTION.json').read_bytes()
    rows = [dict(path=name, bytes=len(raw), sha256=sha(raw)) for name, raw in sorted(members.items())]
    OUT.mkdir()
    output = OUT / 'five-paths.zip'
    with zipfile.ZipFile(output, 'x') as archive:
        for name, raw in sorted(members.items()):
            info = zipfile.ZipInfo(name, (2026, 11, 17, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, raw)
    with zipfile.ZipFile(output) as archive:
        assert archive.namelist() == [r['path'] for r in rows]
        for row in rows:
            raw = archive.read(row['path'])
            assert len(raw) == row['bytes'] and sha(raw) == row['sha256']
    summary = dict(status='PASS_FIVE_PATHS_NOT_MODULE_ACCEPTANCE', runtimeCommit=TREE, hostCommit=HOST,
                   sourceInputs=468, commandsPerPath=463, checkpointsPerPath=21, seatsPerCheckpoint=4,
                   probesPerPath=probes, canonicalViewAndProbeComparisons=comparisons,
                   unchangedAfterProbeSaves=126, finalSha256=FINAL, sourceBindings=bindings,
                   paths=modes, members=len(rows), archiveBytes=output.stat().st_size,
                   archiveSha256=sha(output.read_bytes()), collectorSha256=sha(Path(__file__).read_bytes()),
                   executionLimit='Five fresh session paths in one PowerShell driver process. Console paths invoke the actual launcher script, not separate OS processes. Typed paths construct commands independently; automatic trusted-controller steps use the public controller adapter. Receipt replay reads authentic final receipts.',
                   moduleAccepted=False)
    (OUT / 'MEMBERS.json').write_text(json.dumps(rows, indent=2) + '\n', encoding='utf-8')
    (OUT / 'RETENTION.json').write_text(json.dumps(summary, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in summary.items() if k != 'sourceBindings'}))


if __name__ == '__main__':
    main()
