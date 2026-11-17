"""Retain actual ordinary seal branches; do not promote them into the main campaign."""
import hashlib
import json
from fractions import Fraction
from pathlib import Path
import subprocess
import zipfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
PACKET = HERE.parent
DEV = ROOT / 'engine/artifacts/ferry-wraith/development'
BUILD = DEV / 'run-20261117T073647247Z-a5ad9f14'
PROBE = DEV / 'world-seal-probe-20261117T0856Z'
OUT = PACKET / 'world-seal-checkpoint'
SOURCE = 'ea7e25dc89042a1aebf346efd32004b30ddd59a4'
RUNTIME = '948b9bff0604e15cfb2d5419be9658392bcb2bcf'


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def time(value):
    return Fraction(value['Numerator'], value['Denominator'])


def main():
    assert not OUT.exists(), 'Retained evidence is immutable.'
    report = read(PROBE / 'RESULT.json')
    assert report['status'] == 'PASS_GENUINE_ORDINARY_SEAL_OWN_AND_OTHER_VIRTUAL_SLOT_ONLY'
    source_path = str((HERE / 'Probe-FerryWorldSeal.ps1').relative_to(ROOT)).replace('\\', '/')
    committed = subprocess.check_output(['git', 'show', SOURCE + ':' + source_path], cwd=ROOT)
    executed = (PROBE / 'Probe-FerryWorldSeal.executed.ps1').read_bytes()
    assert committed == executed and digest(executed) == report['script']['sha256']
    source_save = (PROBE / 'original-before-contact.ddsave').read_bytes()
    assert digest(source_save) == report['input']['sha256'] == '54fc97d2e7ee3ceea76a2737392594870fd2cdb345d2e7327735eacd167509fa'
    prior = read(PACKET / 'provenance-checkpoint/RETENTION.json')
    prior_zip = PACKET / 'provenance-checkpoint/development-provenance.zip'
    assert digest(prior_zip.read_bytes()) == prior['archiveSha256']
    with zipfile.ZipFile(prior_zip) as archive:
        assert archive.read('selected/connected/saves/ferry-before-paid-contact.ddsave') == source_save
    seal = read(PACKET / 'seal-checkpoint/RETENTION.json')
    seal_zip = PACKET / 'seal-checkpoint/development-seal.zip'
    assert digest(seal_zip.read_bytes()) == seal['archiveSha256']
    with zipfile.ZipFile(seal_zip) as archive:
        compiled = (BUILD / 'results.json').read_bytes()
        assert archive.read('runtime-build/results.json') == compiled
        assert digest(compiled) == report['compilationReport']['sha256']
        assert len(read(BUILD / 'results.json')['sourceHashes']) == 468
        for assembly in report['assemblies']:
            name = 'Decennium.Foundation.' + assembly['name'] + '.dll'
            actual = (BUILD / name).read_bytes()
            assert archive.read('runtime-build/' + name) == actual
            assert digest(actual) == assembly['sha256']
    assert [b['mode'] for b in report['branches']] == ['own-slot', 'other-slot']
    summaries = []
    for branch, count, actor in zip(report['branches'], (9, 7), ('TEST_ONLY.companion', 'TEST_ONLY.actor')):
        name = branch['mode']
        assert branch['virtualActorAtRupture'] == actor
        assert branch['approachSpeed'] == 20 and time(branch['approachDuration']) == Fraction(3, 2)
        rupture = branch['rupture']
        assert rupture['ActorId'] == 'TEST_ONLY.companion' and rupture['ActionLedger'] == 1
        assert not rupture['InInitiative'] and rupture['OriginalEpochId'] == '' and rupture['OriginalCycle'] == -1
        assert rupture['ActionCalendarId'] == 'TEST_ONLY.post-recovery-calendar' and rupture['ActionInterval'] == 50
        assert time(rupture['ExpiresAt']) == time(rupture['At']) + 6
        entry = time(branch['admission']['Epoch']['Origin'])
        assert time(rupture['At']) < entry < time(rupture['ExpiresAt'])
        assert branch['finalFerry']['Rupture'] == rupture and branch['finalFerry']['SealDestroyed']
        assert not branch['finalFerry']['ClawSuppressed'] and time(branch['finalClock']) >= time(rupture['ExpiresAt'])
        assert branch['finalFerry']['SuppressionExpiredRevision'] == branch['finalRevision']
        assert len(branch['commands']) == len(branch['expandedCommands']) == count
        assert [x['receipt']['Revision'] for x in branch['expandedCommands']] == list(range(345, 345 + count))
        for actual, expanded in zip(branch['commands'], branch['expandedCommands']):
            assert actual['response']['Revision'] == expanded['receipt']['Revision']
            assert expanded['command']['ExpectedRevision'] + 1 == expanded['receipt']['Revision']
            if 'command' in actual:
                assert actual['command'] == expanded['command']
            else:
                assert actual['mode'] == 'actual-public-auto'
                assert expanded['command']['Actor'] == 'TEST_ONLY.ferry-wraith'
                assert actual['beforeRevision'] + 1 == expanded['receipt']['Revision']
        assert len(branch['checkpoints']) == 4
        for checkpoint in branch['checkpoints']:
            first = (PROBE / name / (checkpoint['name'] + '.ddsave')).read_bytes()
            second = (PROBE / name / (checkpoint['name'] + '-restored.ddsave')).read_bytes()
            assert first == second and digest(first) == checkpoint['sha256']
            if checkpoint['name'] == 'verified-input':
                assert first == source_save
        summaries.append(dict(mode=name, commands=count, actorAtRupture=actor, rupture=rupture,
                              entry=branch['admission']['Epoch']['Origin'], finalRevision=branch['finalRevision'],
                              finalClock=branch['finalClock'], checkpoints=branch['checkpoints']))
    members = {}

    def add(prefix, directory):
        for path in sorted(directory.rglob('*')):
            if path.is_file():
                key = prefix + '/' + path.relative_to(directory).as_posix()
                assert key not in members
                members[key] = path.read_bytes()

    add('executed', PROBE)
    for suffix in ('0845Z', '0850Z'):
        failed = DEV / ('world-seal-probe-20261117T' + suffix)
        failure = read(failed / 'RESULT.json')
        assert failure['status'] == 'FAIL' and 'Real paid edge did not admit' in failure['error']
        assert digest((failed / 'Probe-FerryWorldSeal.executed.ps1').read_bytes()) == failure['script']['sha256']
        assert (failed / 'PROBE_FAILURE_EXPLANATION.txt').is_file()
        add('failed-' + suffix, failed)
    for path in ('seal-checkpoint/RETENTION.json', 'seal-checkpoint/MEMBERS.json',
                 'provenance-checkpoint/RETENTION.json', 'GPT_CONTINUATION_REVIEW.json'):
        members['references/' + path] = (PACKET / path).read_bytes()
    members['runtime-build/results.json'] = (BUILD / 'results.json').read_bytes()
    members['support/Retain-FerryWorldSeal.py'] = Path(__file__).read_bytes()
    manifest = [dict(path=name, bytes=len(raw), sha256=digest(raw)) for name, raw in sorted(members.items())]
    OUT.mkdir()
    output = OUT / 'development-world-seal.zip'
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
    retained = dict(status='PASS_RETAINED_GENUINE_ORDINARY_SEAL_BRANCHES_NOT_MODULE_ACCEPTANCE',
                    runtimeCommit=RUNTIME, driverCommit=SOURCE, additionalCompilation=False,
                    runtimeArchiveSha256=seal['archiveSha256'], inputArchiveSha256=prior['archiveSha256'],
                    compiledSourceInputs=468, branches=summaries, actualAlternateCommands=16,
                    canonicalContinuationChanged=False, actualStrictRestorePairs=8,
                    correctedProbeFailures=2, members=len(manifest), archiveBytes=output.stat().st_size,
                    archiveSha256=digest(output.read_bytes()), scriptSha256=digest(Path(__file__).read_bytes()),
                    moduleAccepted=False, fullRegression=False, fivePaths=False)
    (OUT / 'MEMBERS.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    (OUT / 'RETENTION.json').write_text(json.dumps(retained, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in retained.items() if k != 'branches'}))


if __name__ == '__main__':
    main()
