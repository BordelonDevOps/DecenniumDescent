"""Bind three genuine care branches and their separately executed outgoing Ends."""
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
BRANCHES = {'Purify': DEV / 'care-purify-20261117T094304Z',
            'Spare': DEV / 'care-spare-20261117T094323Z',
            'Invocation': DEV / 'care-invocation-20261117T094323Z'}
ENDS = DEV / 'care-ends-20261117T094723Z'
SOURCE = 'bfdea90f33f88517556c8626a66090392973536f'
RUNTIME = '948b9bff0604e15cfb2d5419be9658392bcb2bcf'
OUT = PACKET / 'care-checkpoint'


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def pair(directory, name):
    raw = (directory / (name + '.ddsave')).read_bytes()
    assert raw == (directory / (name + '-restored.ddsave')).read_bytes()
    return digest(raw)


def bind_driver(report, directory, name):
    executed = (directory / (name + '.executed.ps1')).read_bytes()
    path = (HERE / (name + '.ps1')).relative_to(ROOT).as_posix()
    assert executed == subprocess.check_output(['git', 'show', SOURCE + ':' + path], cwd=ROOT)
    assert digest(executed) == report['script']['sha256']


def reconcile(report):
    actual, saved = report['commands'], report['expandedCommands']
    assert len(actual) == len(saved) == report['finalRevision'] - 351
    assert [x['receipt']['Revision'] for x in saved] == list(range(352, report['finalRevision'] + 1))
    for command, expanded in zip(actual, saved):
        assert command['response']['Response'] == 4
        assert command['response']['Revision'] == expanded['receipt']['Revision']
        assert expanded['command']['ExpectedRevision'] + 1 == expanded['receipt']['Revision']
        assert expanded['command']['Id'] == expanded['receipt']['Id']
        if 'command' in command:
            assert command['command'] == expanded['command']
        else:
            assert command['mode'] == 'actual-public-auto'
            assert expanded['command']['Actor'] == 'TEST_ONLY.ferry-wraith'
            assert command['beforeRevision'] + 1 == expanded['receipt']['Revision']


def main():
    assert not OUT.exists(), 'Do not overwrite retained evidence.'
    reports = {plan: read(path / 'RESULT.json') for plan, path in BRANCHES.items()}
    ends = read(ENDS / 'RESULT.json')
    assert ends['status'] == 'PASS_GENUINE_FERRY_CARE_ENDS_ONLY'
    assert [x['plan'] for x in ends['branches']] == list(BRANCHES)
    bind_driver(ends, ENDS, 'Continue-FerryCareEnds')
    seal = read(PACKET / 'seal-checkpoint/RETENTION.json')
    archive_path = PACKET / 'seal-checkpoint/development-seal.zip'
    assert digest(archive_path.read_bytes()) == seal['archiveSha256']
    source_report = (BUILD / 'results.json').read_bytes()
    assert len(read(BUILD / 'results.json')['sourceHashes']) == 468
    selected_pairs = {}
    with zipfile.ZipFile(archive_path) as archive:
        assert source_report == archive.read('runtime-build/results.json')
        first_fire = (BRANCHES['Purify'] / 'original-first-fire.ddsave').read_bytes()
        assert digest(first_fire) == '6a69b36f95e4435705fb175030f7f16aebbfa76bb0752168af65f321d7ab2687'
        assert any(archive.read(name) == first_fire for name in archive.namelist() if name.endswith('/original-first-fire.ddsave'))
        for report in [*reports.values(), ends]:
            assert report['compilationReport']['sha256'] == digest(source_report)
            for assembly in report['assemblies']:
                name = 'Decennium.Foundation.' + assembly['name'] + '.dll'
                raw = (BUILD / name).read_bytes()
                assert raw == archive.read('runtime-build/' + name) and digest(raw) == assembly['sha256']
        for plan, path in BRANCHES.items():
            r = reports[plan]
            assert r['status'] == 'PASS_GENUINE_FERRY_' + plan.upper() + '_ONLY'
            bind_driver(r, path, 'Probe-FerryCareAbilities')
            assert (path / 'original-first-fire.ddsave').read_bytes() == (path / 'verified-input.ddsave').read_bytes() == first_fire
            assert r['input']['sha256'] == digest(first_fire)
            assert not r['nonownerQuery']['Admissible'] and r['nonownerResponse']['Response'] != 4
            reconcile(r)
            selected_pairs[plan + '/completed'] = pair(path, 'completed')
    purify, spare, invocation = (reports[x] for x in BRANCHES)
    assert [r['finalRevision'] for r in reports.values()] == [354, 396, 376]
    assert [len(r['commands']) for r in reports.values()] == [3, 45, 25]
    p = purify['cast']
    assert (p['SpellId'], p['RpBefore'], p['RpAfter'], p['WordsConsumed'], p['Turn']['LocalStart']) == ('purify-food-and-drink', 7, 5, 0, 2)
    contamination = next(x for x in purify['beforeContamination'] if x['LotId'] == p['TargetId'] and x['Present'])
    ended = next(x for x in purify['finalContamination'] if x['Id'] == contamination['Id'])
    assert contamination['Purifiable'] and not ended['Present']
    assert ended['DestroyedByCastId'] == p['CommandId'] and ended['DestroyedRevision'] == 354
    s = spare['cast']
    assert (s['SpellId'], s['RpBefore'], s['RpAfter'], s['StableRecoveryD4'], s['WordsConsumed'], s['Turn']['LocalStart']) == ('spare-the-dying', 7, 7, 2, 1, 20)
    assert spare['beforeLife']['Hp'] == 0 and not spare['beforeLife']['Stable'] and not spare['beforeLife']['Dead']
    hero = next(x for x in spare['finalLives'] if x['ActorId'] == 'TEST_ONLY.actor')
    assert hero['Hp'] == 0 and hero['Stable'] and not hero['Dead']
    assert hero['StableUntil'] == dict(Numerator=358549, Denominator=2)
    assert len(spare['incomingAttacks']) == 6
    assert [x['Damage']['Total'] for x in spare['incomingAttacks']] == [3, 0, 4, 3, 0, 4]
    uses = invocation['invocations']
    assert [x['Turn']['LocalStart'] for x in uses] == [2, 11]
    assert [(x['RpBefore'], x['RpAfter'], x['ConvictionBefore'], x['ConvictionAfter'], x['Die'], x['Modifier'], x['WordsConsumed']) for x in uses] == [(7, 4, 5, 3, 5, 2, 1), (4, 1, 3, 1, 3, 2, 1)]
    assert [[x['ActualGain'] for x in use['Recipients']] for use in uses] == [[7, 0], [5, 0]]
    assert all(use['Choice']['CurePreference'] == 0 and use['EndedApplicationIds'] == [] for use in uses)
    observed = {(x['ownerStart'], x['recharge']['Remaining']) for x in invocation['rechargeObservations']}
    assert observed == {(2, 3), (5, 2), (8, 1), (11, 0)}
    for observation in invocation['rechargeObservations']:
        assert observation['recharge']['LastLocalStart'] == observation['ownerStart']
        assert observation['recharge']['EpochId'] == 'TEST_ONLY.ferry-calendar'
    assert len(invocation['checks']) == 2
    selected_pairs['Invocation/first-invocation'] = pair(BRANCHES['Invocation'], 'first-invocation')
    for branch in ends['branches']:
        plan = branch['plan']; prefix = BRANCHES[plan]; r = reports[plan]; directory = ENDS / plan
        assert (directory / 'PREFIX_RESULT.json').read_bytes() == (prefix / 'RESULT.json').read_bytes()
        assert branch['prefixReportSha256'] == digest((prefix / 'RESULT.json').read_bytes())
        assert (directory / 'input.ddsave').read_bytes() == (directory / 'verified-input.ddsave').read_bytes() == (prefix / 'completed.ddsave').read_bytes()
        assert branch['inputSha256'] == selected_pairs[plan + '/completed']
        assert branch['inputRevision'] == r['finalRevision'] and branch['finalRevision'] == r['finalRevision'] + 1
        assert branch['response']['Response'] == 4 and branch['response']['Revision'] == branch['receipt']['Revision'] == branch['finalRevision']
        assert branch['command'] == branch['retainedCommand'] and branch['command']['Id'] == branch['receipt']['Id']
        cast = uses[-1] if plan == 'Invocation' else r['cast']
        assert branch['castingEnd']['Turn'] == cast['Turn']
        assert branch['randomBefore'] == branch['randomAfter']
        selected_pairs[plan + '/continued'] = pair(directory, 'continued')
        assert branch['finalSaveSha256'] == selected_pairs[plan + '/continued']
    members = {}
    for plan, directory in {**BRANCHES, 'outgoing-ends': ENDS}.items():
        for path in sorted(directory.rglob('*')):
            if path.is_file():
                members['executed/' + plan + '/' + path.relative_to(directory).as_posix()] = path.read_bytes()
    members['runtime-build/results.json'] = source_report
    for name in ('seal-checkpoint/RETENTION.json', 'seal-checkpoint/MEMBERS.json'):
        members['references/' + name] = (PACKET / name).read_bytes()
    members['support/Retain-FerryCare.py'] = Path(__file__).read_bytes()
    manifest = [dict(path=name, bytes=len(raw), sha256=digest(raw)) for name, raw in sorted(members.items())]
    OUT.mkdir()
    output = OUT / 'development-care.zip'
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
    result = dict(status='PASS_RETAINED_GENUINE_FERRY_CARE_BRANCHES_NOT_MODULE_ACCEPTANCE', runtimeCommit=RUNTIME,
                  driverCommit=SOURCE, additionalCompilation=False, compiledSourceInputs=468, runtimeArchiveSha256=seal['archiveSha256'],
                  branches={plan: dict(prefixCommands=len(r['commands']), outgoingCommands=1, finalRevision=r['finalRevision'] + 1) for plan, r in reports.items()},
                  actualAlternateCommands=76, selectedRestorePairs=selected_pairs, canonicalContinuationChanged=False,
                  members=len(manifest), archiveBytes=output.stat().st_size, archiveSha256=digest(output.read_bytes()),
                  scriptSha256=digest(Path(__file__).read_bytes()), moduleAccepted=False, allSevenAbilitiesQualified=False,
                  fullRegression=False, fivePaths=False, invocationCureExercised=False)
    (OUT / 'MEMBERS.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    (OUT / 'RETENTION.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
