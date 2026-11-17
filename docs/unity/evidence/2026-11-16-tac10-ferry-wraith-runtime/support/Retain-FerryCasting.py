"""Freeze the genuine four-spell branch without claiming all-seven qualification."""
import hashlib
import json
from pathlib import Path
import subprocess
import zipfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
PACKET = HERE.parent
DEV = ROOT / 'engine/artifacts/ferry-wraith/development'
BUILD = DEV / 'run-20261117T073647247Z-a5ad9f14'
PROBE = DEV / 'casting-probe-20261117T0915Z'
OUT = PACKET / 'casting-checkpoint'
SOURCE = '7c8b7347a32a50fd20b1f6340dc83ba07a31333d'
RUNTIME = '948b9bff0604e15cfb2d5419be9658392bcb2bcf'


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def main():
    assert not OUT.exists(), 'Do not overwrite retained evidence.'
    r = read(PROBE / 'RESULT.json')
    assert r['status'] == 'PASS_GENUINE_FERRY_FOUR_OWNED_SPELLS_ONLY'
    path = (HERE / 'Probe-FerryCasting.ps1').relative_to(ROOT).as_posix()
    executed = (PROBE / 'Probe-FerryCasting.executed.ps1').read_bytes()
    assert executed == subprocess.check_output(['git', 'show', SOURCE + ':' + path], cwd=ROOT)
    assert digest(executed) == r['script']['sha256']
    seal = read(PACKET / 'seal-checkpoint/RETENTION.json')
    archive_path = PACKET / 'seal-checkpoint/development-seal.zip'
    assert digest(archive_path.read_bytes()) == seal['archiveSha256']
    with zipfile.ZipFile(archive_path) as archive:
        report = (BUILD / 'results.json').read_bytes()
        assert report == archive.read('runtime-build/results.json')
        assert digest(report) == r['compilationReport']['sha256']
        assert len(read(BUILD / 'results.json')['sourceHashes']) == 468
        for assembly in r['assemblies']:
            name = 'Decennium.Foundation.' + assembly['name'] + '.dll'
            raw = (BUILD / name).read_bytes()
            assert raw == archive.read('runtime-build/' + name) and digest(raw) == assembly['sha256']
        original = (PROBE / 'original-first-fire.ddsave').read_bytes()
        # Bind to the exact actual first-fire bytes retained by the earlier seal probe.
        matches = [name for name in archive.namelist() if name.endswith('/original-first-fire.ddsave')]
        assert matches and any(archive.read(name) == original for name in matches)
    assert original == (PROBE / 'verified-input.ddsave').read_bytes()
    assert digest(original) == r['input']['sha256'] == '6a69b36f95e4435705fb175030f7f16aebbfa76bb0752168af65f321d7ab2687'
    assert r['finalRevision'] == 378 and r['finalClock'] == dict(Numerator=344117, Denominator=2)
    assert len(r['commands']) == len(r['expandedCommands']) == 27
    assert [x['receipt']['Revision'] for x in r['expandedCommands']] == list(range(352, 379))
    for actual, expanded in zip(r['commands'], r['expandedCommands']):
        assert actual['response']['Revision'] == expanded['receipt']['Revision']
        assert expanded['command']['ExpectedRevision'] + 1 == expanded['receipt']['Revision']
        if 'command' in actual:
            assert actual['command'] == expanded['command']
        else:
            assert actual['mode'] == 'actual-public-auto' and expanded['command']['Actor'] == 'TEST_ONLY.ferry-wraith'
            assert actual['beforeRevision'] + 1 == expanded['receipt']['Revision']
    spells = ['arcane-ward', 'guidance', 'detect-magic', 'dispel-magic-lesser']
    assert [x['SpellId'] for x in r['casts']] == spells
    assert [x['Revision'] for x in r['casts']] == [354, 362, 369, 377]
    assert [x['Turn']['LocalStart'] for x in r['casts']] == [2, 5, 8, 11]
    assert [(x['RpBefore'], x['BaseRp'], x['Surcharge'], x['RpAfter']) for x in r['casts']] == [(7, 0, 0, 7), (7, 0, 0, 7), (7, 2, 0, 5), (5, 3, 0, 2)]
    for cast in r['casts']:
        assert cast['Turn']['EpochId'] == 'TEST_ONLY.ferry-calendar' and not cast['Turn']['IsCarried']
        assert cast['ActorId'] == 'TEST_ONLY.companion' and cast['SourceRevision'] == '46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4'
        assert cast['WordsConsumed'] == 0 and cast['RandomBefore'] == cast['RandomAfter']
        assert sum(x['Turn'] == cast['Turn'] for x in r['castingEnds']) == 1
    assert len(r['dispels']) == 1
    dispel = r['dispels'][0]
    assert dispel['OriginalCastId'] == r['casts'][1]['CommandId'] and dispel['OriginalCastRevision'] == 362
    assert dispel['EndedEffectId'] == r['casts'][1]['EffectId'] and dispel['OriginalGeneratingRank'] == 0
    assert dispel['DetectionEffectId'] == r['casts'][2]['EffectId'] and dispel['ObservationId'] == r['casts'][3]['TargetId']
    guidance = next(x for x in r['effects'] if x['Id'] == dispel['EndedEffectId'])
    detection = next(x for x in r['effects'] if x['Id'] == dispel['DetectionEffectId'])
    assert not guidance['Present'] and guidance['EndRevision'] == 377 and detection['Present']
    assert r['finalRp'][0]['Current'] == 2 and r['finalStrain'][0]['Dissonance'] == 2
    final = (PROBE / 'completed.ddsave').read_bytes()
    assert final == (PROBE / 'completed-restored.ddsave').read_bytes()
    members = {'executed/' + p.relative_to(PROBE).as_posix(): p.read_bytes() for p in sorted(PROBE.rglob('*')) if p.is_file()}
    members['runtime-build/results.json'] = (BUILD / 'results.json').read_bytes()
    for name in ('seal-checkpoint/RETENTION.json', 'seal-checkpoint/MEMBERS.json'):
        members['references/' + name] = (PACKET / name).read_bytes()
    members['support/Retain-FerryCasting.py'] = Path(__file__).read_bytes()
    manifest = [dict(path=name, bytes=len(raw), sha256=digest(raw)) for name, raw in sorted(members.items())]
    OUT.mkdir()
    output = OUT / 'development-casting.zip'
    with zipfile.ZipFile(output, 'w') as archive:
        for name, raw in sorted(members.items()):
            info = zipfile.ZipInfo(name, (2026, 11, 17, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, raw)
    with zipfile.ZipFile(output) as archive:
        assert archive.namelist() == [x['path'] for x in manifest]
        for row in manifest:
            raw = archive.read(row['path'])
            assert len(raw) == row['bytes'] and digest(raw) == row['sha256']
    result = dict(status='PASS_RETAINED_GENUINE_FERRY_FOUR_OWNED_SPELLS_NOT_MODULE_ACCEPTANCE',
                  runtimeCommit=RUNTIME, driverCommit=SOURCE, additionalCompilation=False, compiledSourceInputs=468,
                  runtimeArchiveSha256=seal['archiveSha256'], actualAlternateCommands=27, spells=spells,
                  finalRevision=378, finalClock=r['finalClock'], finalRp=2, finalDissonance=2,
                  finalSaveSha256=digest(final), canonicalContinuationChanged=False, allSevenAbilitiesQualified=False,
                  members=len(manifest), archiveBytes=output.stat().st_size, archiveSha256=digest(output.read_bytes()),
                  scriptSha256=digest(Path(__file__).read_bytes()), moduleAccepted=False, fullRegression=False, fivePaths=False)
    (OUT / 'MEMBERS.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    (OUT / 'RETENTION.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
