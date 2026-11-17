"""Retain genuine Ward, Guidance/OA and Refrain/vent branches with explicit host limits."""
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
WARD = DEV / 'ward-consumer-20261117T100325Z'
GUIDANCE = DEV / 'guidance-consumer-20261117T103301Z'
REFRAIN = DEV / 'refrain-probe-20261117T102826Z'
SOURCE = '77718577c6423fe233612565041a9a4f6ed4a7cf'
WARD_SOURCE = '927782ae277606e8bf75b548787125694bf4e269'
RUNTIME = '948b9bff0604e15cfb2d5419be9658392bcb2bcf'
OUT = PACKET / 'spell-consumers-checkpoint'
FAILED = ['ward-consumer-20261117T095943Z', 'guidance-consumer-20261117T101333Z',
          'guidance-consumer-20261117T102213Z', 'guidance-consumer-20261117T102826Z',
          'guidance-consumer-20261117T103003Z', 'refrain-probe-20261117T102413Z']


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def reconcile(branch):
    actual, saved = branch['commands'], branch['expandedCommands']
    assert len(actual) == len(saved) == branch['finalRevision'] - 351
    assert [row['receipt']['Revision'] for row in saved] == list(range(352, branch['finalRevision'] + 1))
    for row, retained in zip(actual, saved):
        revision = retained['receipt']['Revision']
        assert retained['command']['ExpectedRevision'] + 1 == revision
        assert retained['command']['Id'] == retained['receipt']['Id']
        if row.get('mode') == 'actual-typed-engine':
            assert row['coreResult']['Outcome'] == 1 and row['coreResult']['Code'] == 'Committed'
            assert row['coreResult']['Revision'] == revision and row['beforeRevision'] + 1 == revision
            assert row['command'] == retained['command']
        else:
            assert row['response']['Response'] == 4 and row['response']['Revision'] == revision
            if 'command' in row:
                assert row['command'] == retained['command']
            else:
                assert row['mode'] == 'actual-public-auto' and row['beforeRevision'] + 1 == revision
                assert retained['command']['Actor'] == 'TEST_ONLY.ferry-wraith'


def main():
    assert not OUT.exists(), 'Do not overwrite retained evidence.'
    w, g, r = (read(path / 'RESULT.json') for path in (WARD, GUIDANCE, REFRAIN))
    assert w['status'] == 'PASS_GENUINE_FERRY_WARD_AC_CONSUMER_ONLY'
    assert g['status'] == 'PASS_GENUINE_FERRY_GUIDANCE_CHECK_AND_CLAW_OPPORTUNITY_ONLY'
    assert r['status'] == 'PASS_GENUINE_FERRY_REFRAIN_RANKED_BOUNDARY_AND_POSITIVE_VENT_ONLY'
    seal = read(PACKET / 'seal-checkpoint/RETENTION.json')
    prior_archive = PACKET / 'seal-checkpoint/development-seal.zip'
    assert digest(prior_archive.read_bytes()) == seal['archiveSha256']
    compiled = (BUILD / 'results.json').read_bytes()
    assert len(read(BUILD / 'results.json')['sourceHashes']) == 468
    source_bindings = {}
    with zipfile.ZipFile(prior_archive) as archive:
        assert compiled == archive.read('runtime-build/results.json')
        for report, path, name, source in [(w, WARD, 'Probe-FerryWardConsumer', WARD_SOURCE),
                                            (g, GUIDANCE, 'Probe-FerryGuidanceConsumer', SOURCE),
                                            (r, REFRAIN, 'Probe-FerryRefrain', SOURCE)]:
            executed = (path / (name + '.executed.ps1')).read_bytes()
            relative = (HERE / (name + '.ps1')).relative_to(ROOT).as_posix()
            assert executed == subprocess.check_output(['git', 'show', source + ':' + relative], cwd=ROOT)
            assert digest(executed) == report['script']['sha256']
            source_bindings[name] = dict(commit=source, sha256=digest(executed))
            assert report['compilationReport']['sha256'] == digest(compiled)
            for assembly in report['assemblies']:
                dll = 'Decennium.Foundation.' + assembly['name'] + '.dll'
                raw = (BUILD / dll).read_bytes()
                assert raw == archive.read('runtime-build/' + dll) and digest(raw) == assembly['sha256']
            first_fire = (path / 'original-first-fire.ddsave').read_bytes()
            assert digest(first_fire) == report['input']['sha256'] == '6a69b36f95e4435705fb175030f7f16aebbfa76bb0752168af65f321d7ab2687'
            assert any(archive.read(n) == first_fire for n in archive.namelist() if n.endswith('/original-first-fire.ddsave'))
            inputs = [path / 'verified-input.ddsave'] if path != WARD else [path / p / 'verified-input.ddsave' for p in ('WithoutWard', 'WithWard')]
            assert all(p.read_bytes() == first_fire for p in inputs)
    for branch in [*w['branches'], g, r]:
        reconcile(branch)
    assert [len(b['commands']) for b in w['branches']] == [8, 9]
    control, protected = (b['attack'] for b in w['branches'])
    assert [a['Attack']['ArmorClass'] for a in (control, protected)] == [10, 11]
    assert all(a['Attack']['Selected'] == 9 and a['Attack']['Modifier'] == 3 and a['Damage']['Total'] == 3 for a in (control, protected))
    assert control['Attack']['RandomBefore'] == protected['Attack']['RandomBefore'] == 118961521
    assert control['Damage'] == protected['Damage']
    assert all(b['attackTargetStance'][0]['Kind'] == 4 and b['finalClock'] == dict(Numerator=344089, Denominator=2) for b in w['branches'])
    ward = w['branches'][1]['cast']
    assert ward['RpBefore'] == ward['RpAfter'] == 7 and ward['WordsConsumed'] == 0
    expired = next(e for e in w['branches'][1]['finalEffects'] if e['Id'] == ward['EffectId'])
    assert not expired['Present'] and expired['ExpiresAt'] == w['branches'][1]['finalClock']
    assert len(g['commands']) == 24 and g['finalRevision'] == 375
    assert g['sessionDashResponse']['Response'] != 4
    typed = [x for x in g['commands'] if x.get('mode') == 'actual-typed-engine']
    assert len(typed) == 1 and typed[0]['command']['Kind'] == 23 and typed[0]['command']['Actor'] == 'TEST_ONLY.actor'
    assert g['typedDashInterval']['ActionSpent'] and g['typedDashInterval']['DashPaid']
    oa = g['opportunityAttack']
    assert oa['Opportunity'] and oa['Attack']['Hit'] and oa['Attack']['Selected'] == 9 and oa['Attack']['Modifier'] == 3
    assert oa['WeaponId'] == 'TEST_ONLY.ferry-wraith.hellfire-claw' and oa['Damage']['Total'] == 3
    assert g['opportunityBeforeRp'] == g['opportunityAfterRp']
    use, check = g['guidanceUse'], g['hideCheck']
    assert use['Revision'] == check['Revision'] == 374 and use['CheckKind'] == 0 and use['D4'] == 4
    assert use['CheckId'] == check['Id'] and use['EffectId'] == g['cast']['EffectId']
    assert use['RandomAfter'] == check['RandomBefore'] and check['Natural'] == 16 and check['Modifier'] == 4 and check['Total'] == 20
    assert use['WordsConsumed'] == check['WordsConsumed'] == 1
    assert g['consumedEffect']['EndReason'] == 7 and not g['consumedEffect']['Present']
    assert len(g['hideResults']) == 1 and g['hideResults'][0]['ObserverId'] == 'TEST_ONLY.haven-copper-buyer'
    assert g['hideResults'][0]['HiddenEstablished'] and g['hideResults'][0]['Dc'] == 10
    assert g['observedHideQuery']['Code'] == 'HideWhileClearlyObserved'
    assert len(r['commands']) == 44 and r['finalRevision'] == 395
    assert [x['Turn']['LocalStart'] for x in r['casts']] == [2, 5, 8, 11, 14]
    assert [x['AppliedRefrain'] for x in r['casts']] == [1, 2, 3, 3, 3]
    assert [x['DissonanceAfter'] for x in r['casts']] == [1, 3, 6, 9, 12]
    assert all(x['RpBefore'] == x['RpAfter'] == 7 and x['WordsConsumed'] == 0 for x in r['casts'])
    assert [next(c['Amount'] for c in q['query']['Costs'] if c['Kind'] == 'rp') for q in r['rankedQueries'][:-1]] == [2, 2, 2, 3, 4]
    assert r['rankedQueries'][-1]['query']['Code'] == 'RankedCastingBlockedByDissonance' and r['blockedResponse']['Response'] != 4
    assert r['allowedCantripQuery']['Admissible'] and r['invocationQuery']['Admissible']
    invocation = r['invocation']
    assert (invocation['DissonanceBefore'], invocation['DissonanceAfter'], invocation['ActualVent']) == (12, 11, 1)
    assert (invocation['RpBefore'], invocation['RpAfter'], invocation['ConvictionBefore'], invocation['ConvictionAfter']) == (7, 4, 5, 3)
    assert invocation['Die'] == 2 and invocation['Recipients'][0]['HpBefore'] == 3 and invocation['Recipients'][0]['HpAfter'] == 7
    assert r['finalStrain'][0]['Dissonance'] == 11 and len(r['castingEnds']) == 6
    members, pairs = {}, {}
    for label, path in [('ward', WARD), ('guidance', GUIDANCE), ('refrain', REFRAIN)]:
        for file in sorted(path.rglob('*')):
            if file.is_file():
                members['executed/' + label + '/' + file.relative_to(path).as_posix()] = file.read_bytes()
        for restored in path.rglob('*-restored.ddsave'):
            original = restored.with_name(restored.name.replace('-restored.ddsave', '.ddsave'))
            assert original.read_bytes() == restored.read_bytes()
            pairs[label + '/' + original.relative_to(path).as_posix()] = digest(original.read_bytes())
    assert len(pairs) == 15
    failures = []
    for name in FAILED:
        path = DEV / name; failure = read(path / 'RESULT.json')
        assert failure['status'] == 'FAIL' and failure.get('error')
        scripts = list(path.glob('*.executed.ps1'))
        assert len(scripts) == 1 and digest(scripts[0].read_bytes()) == failure['script']['sha256']
        failures.append(dict(directory=name, error=failure['error'], reportSha256=digest((path / 'RESULT.json').read_bytes())))
        for file in sorted(path.rglob('*')):
            if file.is_file():
                members['failed-attempts/' + name + '/' + file.relative_to(path).as_posix()] = file.read_bytes()
    members['runtime-build/results.json'] = compiled
    for name in ('seal-checkpoint/RETENTION.json', 'seal-checkpoint/MEMBERS.json'):
        members['references/' + name] = (PACKET / name).read_bytes()
    members['support/Retain-FerrySpellConsumers.py'] = Path(__file__).read_bytes()
    manifest = [dict(path=name, bytes=len(raw), sha256=digest(raw)) for name, raw in sorted(members.items())]
    OUT.mkdir()
    output = OUT / 'development-spell-consumers.zip'
    with zipfile.ZipFile(output, 'w') as archive:
        for name, raw in sorted(members.items()):
            info = zipfile.ZipInfo(name, (2026, 11, 17, 0, 0, 0)); info.compress_type = zipfile.ZIP_DEFLATED; info.external_attr = 0o100644 << 16
            archive.writestr(info, raw)
    with zipfile.ZipFile(output) as archive:
        assert archive.namelist() == [x['path'] for x in manifest]
        for row in manifest:
            raw = archive.read(row['path']); assert len(raw) == row['bytes'] and digest(raw) == row['sha256']
    result = dict(status='PASS_RETAINED_GENUINE_FERRY_SPELL_CONSUMERS_NOT_MODULE_ACCEPTANCE', runtimeCommit=RUNTIME,
                  sourceBindings=source_bindings, additionalCompilation=False, compiledSourceInputs=468,
                  actualAlternateCommands=85, typedEngineDashCommands=1, sessionDashSupported=False,
                  selectedRestorePairs=pairs, failedAttempts=failures, canonicalContinuationChanged=False,
                  members=len(manifest), archiveBytes=output.stat().st_size, archiveSha256=digest(output.read_bytes()),
                  scriptSha256=digest(Path(__file__).read_bytes()), moduleAccepted=False, fivePaths=False, fullRegression=False)
    (OUT / 'MEMBERS.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    (OUT / 'RETENTION.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k not in ('selectedRestorePairs', 'failedAttempts')}))


if __name__ == '__main__':
    main()
