"""Retain real source attack continuations and their distinct causal branches."""
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
REGULAR = DEV / 'sanctuary-probe-20261117T0953Z'
OLD_FORGO = DEV / 'sanctuary-probe-20261117T0941Z'
OPPORTUNITY = DEV / 'cached-opportunity-probe-20261117T1010Z'
OUT = PACKET / 'sanctuary-checkpoint'
SOURCE = 'cbc6f4ef03e3f28288d8ac0594d561508635872a'
RUNTIME = '948b9bff0604e15cfb2d5419be9658392bcb2bcf'


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def pair(directory, name):
    raw = (directory / (name + '.ddsave')).read_bytes()
    assert raw == (directory / (name + '-restored.ddsave')).read_bytes()
    return digest(raw)


def reconcile(commands, expanded, start):
    assert len(commands) == len(expanded)
    assert [x['receipt']['Revision'] for x in expanded] == list(range(start + 1, start + 1 + len(commands)))
    for actual, saved in zip(commands, expanded):
        assert actual['response']['Response'] == 4
        assert actual['response']['Revision'] == saved['receipt']['Revision']
        assert saved['command']['ExpectedRevision'] + 1 == saved['receipt']['Revision']
        if 'command' in actual:
            assert actual['command'] == saved['command']
        else:
            assert actual['mode'] == 'actual-public-auto' and saved['command']['Actor'] == 'TEST_ONLY.ferry-wraith'
            assert actual['beforeRevision'] + 1 == saved['receipt']['Revision']


def main():
    assert not OUT.exists(), 'Evidence directories are immutable.'
    regular, opportunity, old = [read(x / 'RESULT.json') for x in (REGULAR, OPPORTUNITY, OLD_FORGO)]
    assert regular['status'] == 'PASS_GENUINE_SANCTUARY_REGULAR_SOURCE_RETARGET_FORGO_ONLY'
    assert opportunity['status'] == 'PASS_GENUINE_CACHED_CLAW_OPPORTUNITY_DECLINE_AND_NEXT_START_REFRESH_ONLY'
    seal = read(PACKET / 'seal-checkpoint/RETENTION.json')
    seal_path = PACKET / 'seal-checkpoint/development-seal.zip'
    assert digest(seal_path.read_bytes()) == seal['archiveSha256']
    with zipfile.ZipFile(seal_path) as archive:
        for directory, report, script in ((REGULAR, regular, 'Probe-FerrySanctuary'), (OPPORTUNITY, opportunity, 'Probe-FerrySanctuaryOpportunity')):
            executed = (directory / (script + '.executed.ps1')).read_bytes()
            source_path = (HERE / (script + '.ps1')).relative_to(ROOT).as_posix()
            assert executed == subprocess.check_output(['git', 'show', SOURCE + ':' + source_path], cwd=ROOT)
            assert digest(executed) == report['script']['sha256']
            compiled = (BUILD / 'results.json').read_bytes()
            assert archive.read('runtime-build/results.json') == compiled
            assert digest(compiled) == report['compilationReport']['sha256']
            assert len(read(BUILD / 'results.json')['sourceHashes']) == 468
            for assembly in report['assemblies']:
                name = 'Decennium.Foundation.' + assembly['name'] + '.dll'
                raw = (BUILD / name).read_bytes()
                assert raw == archive.read('runtime-build/' + name) and digest(raw) == assembly['sha256']
        original = (REGULAR / 'original-first-fire.ddsave').read_bytes()
        candidates = [x for x in archive.namelist() if x.endswith('/original-first-fire.ddsave')]
        assert any(archive.read(x) == original for x in candidates)
    assert original == (REGULAR / 'verified-input.ddsave').read_bytes()
    assert digest(original) == regular['input']['sha256'] == '6a69b36f95e4435705fb175030f7f16aebbfa76bb0752168af65f321d7ab2687'
    assert len(regular['prefixCommands']) == 10
    reconcile(regular['prefixCommands'], regular['prefixExpandedCommands'], 351)
    cast, save, pending, source = [regular[x] for x in ('cast', 'save', 'pending', 'sourceCommand')]
    assert cast['SpellId'] == 'sanctuary' and cast['Turn']['EpochId'] == 'TEST_ONLY.ferry-calendar'
    assert (cast['Revision'], cast['RpBefore'], cast['RpAfter']) == (354, 7, 5)
    assert (save['Natural'], save['Modifier'], save['Dc'], save['Success']) == (9, 0, 12, False)
    assert save['Revision'] == pending['SourceRevision'] == 361 and save['AttackerTurn']['LocalStart'] == 4
    assert pending['Source'] == 6 and source['Kind'] == 203
    assert source['Combat']['FeatureId'] == 'TEST_ONLY.ferry-wraith.hellfire-claw' and source['Combat']['WeaponId'] == ''
    assert (source['Combat']['Knockout'], source['Combat']['PressInstruction']) == (2, 0)
    assert pending['SourceFingerprint'] == regular['prefixExpandedCommands'][-1]['receipt']['Fingerprint']
    assert 'combat-v3' in pending['SourceFingerprint']
    selected_pairs = {'regular/pending': pair(REGULAR, 'pending-source-claw')}
    assert [x['choice'] for x in regular['branches']] == ['Forgo', 'Retarget']
    for branch in regular['branches']:
        assert len(branch['commands']) == 2 and branch['finalRevision'] == 363
        reconcile(branch['commands'], branch['expandedCommands'], 361)
        assert branch['resolved']['SourceFingerprint'] == pending['SourceFingerprint']
        assert branch['resolved']['ResolvedRevision'] == 362
        for suffix in ('resolved', 'continued'):
            name = branch['choice'].lower() + '-' + suffix
            selected_pairs['regular/' + name] = pair(REGULAR, name)
        if branch['choice'] == 'Forgo':
            assert branch['resolved']['Status'] == 2 and not branch['newSpellSaves']
        else:
            attack = branch['attack']
            assert attack['WeaponId'] == source['Combat']['FeatureId'] and attack['TargetId'] == 'TEST_ONLY.companion'
            assert (attack['Instruction'], attack['PressInstruction']) == (2, 0)
            assert (attack['Attack']['Selected'], attack['Attack']['Modifier'], attack['Attack']['ArmorClass']) == (11, 3, 11)
            assert attack['Attack']['Hit'] and attack['Attack']['RandomBefore'] == save['RandomAfter']
            assert attack['Damage']['Dice'] == [3] and attack['Damage']['Total'] == 3
            assert len(branch['typedDamage']) == 1
            damage = branch['typedDamage'][0]
            assert damage['DamageType'] == 'fire' and damage['Raw'] == damage['Effective'] == 3
            assert len(branch['newSpellSaves']) == 1
            concentration = branch['newSpellSaves'][0]
            assert (concentration['Kind'], concentration['Natural'], concentration['Dc'], concentration['Damage'], concentration['Success']) == (1, 12, 10, 3, True)
            assert concentration['RandomBefore'] == attack['Damage']['FinalRandom']
    # The independently retained earlier forgo checkpoint is genuine despite its
    # aggregate probe later failing an out-of-range Retarget query. Do not call that
    # aggregate probe a pass or count its failed branch as a successful execution.
    assert old['status'] == 'FAIL' and 'Lawful source-preserving response' in old['error']
    assert len(old['prefixCommands']) == 8
    reconcile(old['prefixCommands'], old['prefixExpandedCommands'], 351)
    old_branch = old['branches'][0]
    assert old_branch['choice'] == 'Forgo' and old_branch['finalRevision'] == 361
    reconcile(old_branch['commands'], old_branch['expandedCommands'], 359)
    pair(OLD_FORGO, 'forgo-resolved')
    source_hash = pair(OLD_FORGO, 'forgo-continued')
    base = (OPPORTUNITY / 'original-forgo-continued.ddsave').read_bytes()
    assert base == (OLD_FORGO / 'forgo-continued.ddsave').read_bytes()
    assert digest(base) == opportunity['input']['sha256'] == source_hash
    assert len(opportunity['commands']) == 11 and opportunity['finalRevision'] == 372
    reconcile(opportunity['commands'], opportunity['expandedCommands'], 361)
    assert opportunity['cachedQuery']['Code'] == 'SanctuaryTargetProhibitedThisInterval'
    assert not opportunity['cachedQuery']['Admissible'] and opportunity['controllerIntent']['Kind'] == 6
    move = opportunity['completedMove']
    assert move['Status'] == 1 and move['CostPaid'] == 5 and (move['ToX'], move['ToY']) == (7, 2)
    assert move['ResolvedRevision'] == 366 and move['Reactors'] == ['TEST_ONLY.ferry-wraith']
    refreshed = opportunity['refreshedWardSave']
    assert (refreshed['Revision'], refreshed['Natural'], refreshed['Modifier'], refreshed['Dc'], refreshed['Success']) == (370, 11, 0, 12, False)
    assert refreshed['AttackerTurn']['LocalStart'] == 7
    assert refreshed['EffectId'] == opportunity['originalWardSave']['EffectId']
    assert refreshed['RandomBefore'] == opportunity['originalWardSave']['RandomAfter']
    for name in ('verified-input', 'cached-opportunity-pending', 'cached-opportunity-declined', 'completed-next-source-interval'):
        selected_pairs['opportunity/' + name] = pair(OPPORTUNITY, name)
    members = {}

    def add(prefix, directory):
        for path in sorted(directory.rglob('*')):
            if path.is_file():
                members[prefix + '/' + path.relative_to(directory).as_posix()] = path.read_bytes()

    add('regular', REGULAR)
    add('opportunity', OPPORTUNITY)
    for label in ('sanctuary-probe-20261117T0937Z', 'sanctuary-probe-20261117T0941Z', 'sanctuary-probe-20261117T0948Z', 'cached-opportunity-probe-20261117T1001Z'):
        directory = DEV / label
        failed = read(directory / 'RESULT.json')
        assert failed['status'] == 'FAIL' and (directory / 'PROBE_FAILURE_EXPLANATION.txt').is_file()
        script = next(directory.glob('*.executed.ps1'))
        assert digest(script.read_bytes()) == failed['script']['sha256']
        add('retained-failures/' + label, directory)
    for name in ('seal-checkpoint/RETENTION.json', 'seal-checkpoint/MEMBERS.json', 'GPT_CASTING_REVIEW.json'):
        members['references/' + name] = (PACKET / name).read_bytes()
    members['runtime-build/results.json'] = (BUILD / 'results.json').read_bytes()
    members['support/Retain-FerrySanctuary.py'] = Path(__file__).read_bytes()
    manifest = [dict(path=name, bytes=len(raw), sha256=digest(raw)) for name, raw in sorted(members.items())]
    OUT.mkdir()
    output = OUT / 'development-sanctuary.zip'
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
    result = dict(status='PASS_RETAINED_GENUINE_SANCTUARY_SOURCE_AND_CACHED_OPPORTUNITY_NOT_MODULE_ACCEPTANCE',
                  runtimeCommit=RUNTIME, driverCommit=SOURCE, compiledSourceInputs=468, additionalCompilation=False,
                  runtimeArchiveSha256=seal['archiveSha256'], regularCommonCommands=10, regularBranchCommands=[2, 2],
                  earlierGenuineForgoPrefixCommands=8, earlierGenuineForgoResolutionCommands=2, opportunityNewCommands=11,
                  selectedRestorePairs=selected_pairs, opportunityInputSha256=source_hash,
                  retainedFailedAggregateAttempts=4, existingHistoryCapacityLimitObserved=True,
                  members=len(manifest), archiveBytes=output.stat().st_size, archiveSha256=digest(output.read_bytes()),
                  scriptSha256=digest(Path(__file__).read_bytes()), moduleAccepted=False, allSevenAbilitiesQualified=False,
                  fullRegression=False, fivePaths=False)
    (OUT / 'MEMBERS.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    (OUT / 'RETENTION.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in result.items() if k != 'selectedRestorePairs'}))


if __name__ == '__main__':
    main()
