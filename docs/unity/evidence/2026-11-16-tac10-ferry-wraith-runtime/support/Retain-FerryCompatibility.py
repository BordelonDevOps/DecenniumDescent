"""Retain authentic95-113 results and the current Ferry rejection/privacy controls."""
import argparse
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
LEGACY = ART / 'compatibility95-112-20261117T122530Z'
WIRE113 = ART / 'wire113-20261117T122736Z'
OUT = PACKET / 'compatibility-checkpoint'


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--pure-run', required=True)
    args = parser.parse_args()
    pure = ROOT / args.pure_run
    assert not OUT.exists(), 'Never overwrite retained qualification.'
    members, bindings, omitted_dlls = {}, {}, []
    parent = read(LEGACY / 'results.json')
    assert parent['status'] == 'PASS' and len(parent['steps']) == 4 and all(r['exitCode'] == 0 for r in parent['steps'])
    legacy = read(LEGACY / 'compatibility95-110/results.json')
    views = read(LEGACY / 'legacy95-110-views/results.json')
    assert legacy['Status'] == views['status'] == 'PASS' and len(legacy['Cases']) == len(views['cases']) == 28
    assert {r['Wire'] for r in legacy['Cases']} == set(range(95, 111))
    source_count = 0
    for case in legacy['Cases']:
        for key, hashkey in [('Source', 'SourceSha256'), ('Earlier', 'EarlierSha256')]:
            source = ROOT / 'docs/unity/evidence' / case[key].replace('\\', '/')
            assert sha(source.read_bytes()) == case[hashkey]
            members['authentic95-110/' + case[key].replace('\\', '/')] = source.read_bytes()
            source_count += 1
        assert case['RoundtripSha256'] == case['ContinuedSha256'] == case['SourceSha256']
    for case in views['cases']:
        assert case['newOutputSha256'] == case['oldOutputSha256'] and case['views'] == 4
    wire_reports = {}
    for wire, directory in [(111, LEGACY / 'wire111'), (112, LEGACY / 'wire112'), (113, WIRE113)]:
        result = read(directory / 'results.json')
        accepted, current = read(directory / ('Accepted' + str(wire)) / 'results.json'), read(directory / 'Current/results.json')
        assert result['status'] == accepted['status'] == current['status'] == 'PASS'
        assert accepted['checkpoints'] == current['checkpoints'] == result['authenticCheckpoints']
        assert accepted['commands'] == current['commands'] == result['actualContinuationCommandsPerRole']
        assert accepted['artifacts'] == current['artifacts'] == result['artifacts']
        assert len(result['artifacts']) == result['comparedCanonicalAndViews']
        for name, digest in result['artifacts'].items():
            assert sha((directory / ('Accepted' + str(wire)) / name).read_bytes()) == digest
            assert sha((directory / 'Current' / name).read_bytes()) == digest
        for part, row in result['currentAssemblies'].items():
            assert row == current['assemblies'][part]
            assert row['sha256'] == sha((BUILD / ('Decennium.Foundation.' + part + '.dll')).read_bytes())
        for part, row in result['oldAssemblies'].items():
            assert row == accepted['assemblies'][part]
            assert row['sha256'] == sha((directory / 'accepted-assemblies' / ('Decennium.Foundation.' + part + '.dll')).read_bytes())
        for mark in read(directory / 'sources/marks.json'):
            assert sha((directory / 'sources' / mark['name']).read_bytes()) == mark['sha256']
        wire_reports[str(wire)] = {k: result[k] for k in ('sourceArchiveSha256','authenticCheckpoints','actualContinuationCommandsPerRole','comparedCanonicalAndViews','newProfileRejections')}
    # Bind the authentic predecessor archives, not just their extracted filenames.
    archive_paths = {
        '111': '2026-11-16-chr03-bishop-runtime',
        '112': '2026-11-16-exp07-post-recovery',
        '113': '2026-11-16-tac03-declared-geometry-runtime',
    }
    authenticated_archives = []
    for wire, folder in archive_paths.items():
        expected = wire_reports[wire]['sourceArchiveSha256']
        candidates = sorted((PACKET.parent / folder).glob('*/*.zip'))
        found = next((p for p in candidates if sha(p.read_bytes()) == expected), None)
        assert found is not None, 'Authentic predecessor archive missing: ' + wire
        authenticated_archives.append(dict(wire=wire, path=found.relative_to(ROOT).as_posix(), sha256=expected))
    for root in (LEGACY, WIRE113):
        for before_path in root.rglob('execution-sources.before.json'):
            after_path = before_path.with_name('execution-sources.after.json')
            before, after = read(before_path), read(after_path)
            assert after['status'] == 'PASS' and before['files'] == after['files'] and before['pid'] == after['pid']
            for row in before['files']:
                raw = (ROOT / row['path']).read_bytes()
                assert len(raw) == row['bytes'] and sha(raw) == row['sha256']
                assert subprocess.check_output(['git','-C',str(ROOT),'show','HEAD:' + row['path']]) == raw
                bindings[row['path']] = row['sha256']
                members['executed-sources/' + row['path']] = raw
    controls = read(pure / 'RESULT.json')
    assert controls['status'] == 'PASS_FINAL_PURE_CONTROLS_ONLY'
    assert len(controls['probes']) == 6 and all(p['unchanged'] and not p['query']['Admissible'] for p in controls['probes'])
    assert len(controls['oldProfileRejections']) == 113 and all(p['unchanged'] for p in controls['oldProfileRejections'])
    assert len(controls['privacyPairs']) == 3 and all(p['detachedOnly'] for p in controls['privacyPairs'])
    for row in controls['assemblies']:
        assert row['sha256'] == sha((BUILD / ('Decennium.Foundation.' + row['name'] + '.dll')).read_bytes())
    executed = pure / 'Probe-FerryFinalPureControls.executed.ps1'
    assert sha(executed.read_bytes()) == controls['script']['sha256']
    assert executed.read_bytes() == (HERE / 'Probe-FerryFinalPureControls.ps1').read_bytes()
    for row in controls['oldProfileRejections']:
        assert sha(Path(row['path']).read_bytes()) == row['sha256']
    assert (pure / 'original-first-fire.ddsave').read_bytes() == (pure / 'verified-input.ddsave').read_bytes() == (pure / 'after-all-probes.ddsave').read_bytes()
    assert (pure / 'original-privacy-input.ddsave').read_bytes() == (pure / 'verified-privacy-input.ddsave').read_bytes() == (pure / 'after-privacy-probes.ddsave').read_bytes()
    for row in controls['privacyPairs']:
        assert (pure / (row['variant'] + '.view.json')).read_bytes() == (pure / 'controller-base-view.json').read_bytes()
        assert (pure / (row['variant'] + '.intent.json')).read_bytes() == (pure / 'controller-base-intent.json').read_bytes()
    for label, directory in [('compatibility95-112',LEGACY), ('wire113',WIRE113), ('pure-controls',pure)]:
        for path in sorted(directory.rglob('*')):
            if not path.is_file():
                continue
            name = label + '/' + path.relative_to(directory).as_posix()
            if path.suffix.lower() == '.dll':
                omitted_dlls.append(dict(path=name, bytes=path.stat().st_size, sha256=sha(path.read_bytes())))
            else:
                members[name] = path.read_bytes()
    members['support/Retain-FerryCompatibility.py'] = Path(__file__).read_bytes()
    manifest = [dict(path=name,bytes=len(raw),sha256=sha(raw)) for name,raw in sorted(members.items())]
    OUT.mkdir()
    output = OUT / 'compatibility.zip'
    with zipfile.ZipFile(output, 'x') as archive:
        for name,raw in sorted(members.items()):
            info=zipfile.ZipInfo(name,(2026,11,17,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16
            archive.writestr(info,raw)
    with zipfile.ZipFile(output) as archive:
        assert archive.namelist() == [r['path'] for r in manifest]
        for row in manifest:
            raw=archive.read(row['path']);assert len(raw)==row['bytes'] and sha(raw)==row['sha256']
    summary=dict(status='PASS_AUTHENTIC95_113_AND_PURE_CONTROLS_NOT_MODULE_ACCEPTANCE',
                 runtimeCommit='c8ffee78d5047131317ff923c8e3a575b6c51f3a',hostCommit='3d0afc12d2444d2d6d77e3ff3729f2ff8236be3d',
                 authentic95_110Cases=28,authentic95_110EndpointBindings=source_count,
                 authentic95_110ContinuedCommands=sum(r['Commands'] for r in legacy['Cases']),old95_110Views=112,
                 laterWires=wire_reports,currentFerryCrossProfileRejections=113,publicPureDenials=6,detachedControllerPrivacyPairs=3,
                 sourceBindings=bindings,authenticatedPredecessorArchives=authenticated_archives,omittedDuplicateAssemblies=omitted_dlls,
                 members=len(manifest),archiveBytes=output.stat().st_size,archiveSha256=sha(output.read_bytes()),
                 collectorSha256=sha(Path(__file__).read_bytes()),moduleAccepted=False,
                 limits='Original95-112 predecessor drivers also reject their own then-new profiles; those counts are not Ferry rejection claims. The separate actual Ferry control rejects all113 selected old endpoints/checkpoints unchanged. Detached controller pairs vary RNG, living enemy HP and enemy STR/DEX only; they are pure projection controls, never gameplay/adopted saves. No claim about untested private-state dimensions.')
    (OUT/'MEMBERS.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    (OUT/'RETENTION.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in summary.items() if k not in ('sourceBindings','omittedDuplicateAssemblies','authenticatedPredecessorArchives')}))


if __name__ == '__main__':
    main()
