"""Bind actual combat/management commands and backup recovery to the retained runtime."""
import hashlib
import json
from pathlib import Path
import subprocess
import zipfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
SOURCE = 'e744c04a35cfb94e0f77207e3f35610b77b9868b'
RUNTIME = '948b9bff0604e15cfb2d5419be9658392bcb2bcf'
PACKET = HERE.parent
DEV = ROOT / 'engine/artifacts/ferry-wraith/development'
BUILD = DEV / 'run-20261117T073647247Z-a5ad9f14'
PRIOR = DEV / 'continuation-probe-20261117T0804Z'
PROBE = DEV / 'continuation-probe-20261117T0810Z'
EXPORT = DEV / 'continuation-export-20261117T0816Z'
OUT = PACKET / 'continuation-checkpoint'


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def git_bytes(revision, path):
    return subprocess.check_output(['git', 'show', revision + ':' + path], cwd=ROOT)


def main():
    assert not OUT.exists(), 'Do not overwrite retained evidence.'
    p, prior, export = [read(x / 'RESULT.json') for x in (PROBE, PRIOR, EXPORT)]
    assert p['status'] == 'PASS_GENUINE_DEAD_CLOSURE_MANAGE_PREPARE_CONTINUE_ONLY'
    assert export['status'] == 'PASS_READ_ONLY_ACTUAL_CONTINUATION_EXPORT'
    assert prior['status'] == 'FAIL' and 'No genuine incoming party attack hit.' in prior['error']
    assert len(prior['commands']) == p['resumedFrom']['priorExecutedCommands'] == 72
    assert p['commands'][:72] == prior['commands'] and len(p['commands']) == 97
    assert p['resumedFrom']['resultSha256'] == digest((PRIOR / 'RESULT.json').read_bytes())
    assert p['resumedFrom']['priorScriptSha256'] == prior['script']['sha256']
    assert p['finalRevision'] == 462 and p['finalClock'] == dict(Numerator=344239, Denominator=2)
    assert len(p['incomingAttacks']) == 9 and sum(x['Attack']['Hit'] for x in p['incomingAttacks']) == 3
    assert len(p['healingRites']) == 2 and [x['RpPaid'] for x in p['healingRites']] == [2, 2]
    assert [(x['RpBefore'], x['RpAfter'], x['ActualGain']) for x in p['healingRites']] == [(7, 5, 5), (5, 3, 10)]
    assert p['finalResonance'][0]['Current'] == 3
    assert [(x['Hp'], x['Dead']) for x in p['finalParty']] == [(14, False), (18, False)]
    assert p['closure'][0]['ClosedRevision'] == 437
    assert p['closure'][0]['Encounter']['Id'] == 'TEST_ONLY.ferry-encounter'
    assert p['preparation']['club']['HeldBy'] == 'TEST_ONLY.companion'
    assert p['preparation']['before'] == dict(Numerator=344233, Denominator=2)
    assert p['preparation']['after'] == dict(Numerator=344235, Denominator=2)
    seal = read(PACKET / 'seal-checkpoint/RETENTION.json')
    seal_archive = PACKET / 'seal-checkpoint/development-seal.zip'
    assert digest(seal_archive.read_bytes()) == seal['archiveSha256']
    assert p['source']['sha256'] == seal['finalSaveSha256']
    assert digest((PROBE / 'original-recovered-claw.ddsave').read_bytes()) == seal['finalSaveSha256']
    assert subprocess.check_output(['git', 'diff', RUNTIME, SOURCE, '--name-only', '--', 'engine'], cwd=ROOT).decode().splitlines() == [
        'engine/com.decennium.foundation/Tests/EditMode/FerryWraithCases.cs']
    compiled = (BUILD / 'results.json').read_bytes()
    assert p['compilationReport']['sha256'] == prior['compilationReport']['sha256'] == digest(compiled)
    assert read(BUILD / 'results.json')['status'] == 'PASS'
    # Reuse the immutable, already committed runtime archive rather than duplicating its DLLs.
    with zipfile.ZipFile(seal_archive) as runtime_archive:
        assert runtime_archive.read('runtime-build/results.json') == compiled
        for report in (p, prior, export):
            for row in report['assemblies']:
                name = 'Decennium.Foundation.' + row['name'] + '.dll'
                raw = (BUILD / name).read_bytes()
                assert row['sha256'] == digest(raw) and raw == runtime_archive.read('runtime-build/' + name)
    driver_path = 'docs/unity/evidence/2026-11-16-tac10-ferry-wraith-runtime/support/Probe-FerryContinuation.ps1'
    assert p['script']['sha256'] == digest(git_bytes(SOURCE, driver_path))
    assert (PROBE / 'Probe-FerryContinuation.executed.ps1').read_bytes() == git_bytes(SOURCE, driver_path)
    assert export['script']['sha256'] == digest((HERE / 'Export-FerryContinuation.ps1').read_bytes())
    for folder in (PRIOR, PROBE):
        if folder == PRIOR:
            pairs = ['actual-dead-before-closure', 'actual-ferry-closed']
        else:
            pairs = ['continued-after-preparation']
        for name in pairs:
            assert (folder / (name + '.ddsave')).read_bytes() == (folder / (name + '-restored.ddsave')).read_bytes()
    assert (PROBE / 'resumed-closed.ddsave').read_bytes() == (PRIOR / 'actual-ferry-closed.ddsave').read_bytes()
    assert p['resumedFrom']['closedSha256'] == digest((PROBE / 'resumed-closed.ddsave').read_bytes())
    final = (PROBE / 'continued-after-preparation.ddsave').read_bytes()
    assert export['input']['sha256'] == digest(final) == p['backupRecovery']['validSha256']
    assert (PROBE / 'backup-recovery.ddsave').read_bytes() == final
    assert (PROBE / 'backup-recovery.ddsave.bak').read_bytes() == final
    displaced = PROBE / Path(p['backupRecovery']['displacedPath']).name
    assert displaced.read_bytes() == b'BAD' and digest(displaced.read_bytes()) == p['backupRecovery']['corruptSha256']
    commands = read(EXPORT / 'selected-continuation-commands.json')
    all_commands = read(EXPORT / 'all-command-receipts.json')
    assert len(all_commands) == 462 and all_commands[365:] == commands and len(commands) == 97
    assert [x['receipt']['Revision'] for x in commands] == list(range(366, 463))
    assert [x['response']['Revision'] for x in p['commands']] == list(range(366, 463))
    for observed, expanded in zip(p['commands'], commands):
        assert observed['response']['Response'] == 4
        if 'command' in observed:
            assert observed['command'] == expanded['command']
        else:
            assert expanded['receipt']['Principal'] == 'TEST_ONLY.ferry-controller'
    state = read(EXPORT / 'final-private-evidence.json')
    assert next(x for x in state['lives'] if x['ActorId'] == 'TEST_ONLY.ferry-wraith')['Dead']
    assert state['ferry']['SealDestroyed'] and not state['ferry']['ClawSuppressed']
    assert len(state['knownSpells']) == 7  # Ownership only; this is not execution of all seven.
    members = {}
    for label, folder in [('continued', PROBE), ('executed-combat-prefix', PRIOR), ('export', EXPORT),
                          ('earlier-probe-failure', DEV / 'continuation-probe-20261117T0755Z')]:
        report = read(folder / 'RESULT.json')
        if label in ('executed-combat-prefix', 'earlier-probe-failure'):
            assert report['status'] == 'FAIL'
            assert report['script']['sha256'] == digest((folder / 'Probe-FerryContinuation.executed.ps1').read_bytes())
        for path in sorted(folder.rglob('*')):
            if path.is_file():
                members[label + '/' + path.relative_to(folder).as_posix()] = path.read_bytes()
    members['runtime-reference/compilation-results.json'] = compiled
    for name in ['RETENTION.json', 'MEMBERS.json']:
        members['runtime-reference/seal-' + name] = (PACKET / 'seal-checkpoint' / name).read_bytes()
    members['review/GPT_SEAL_REVIEW.json'] = git_bytes(SOURCE, 'docs/unity/evidence/2026-11-16-tac10-ferry-wraith-runtime/GPT_SEAL_REVIEW.json')
    members['executed-support/Retain-FerryContinuation.py'] = Path(__file__).read_bytes()
    manifest = [dict(path=name, bytes=len(raw), sha256=digest(raw)) for name, raw in sorted(members.items())]
    OUT.mkdir()
    archive = OUT / 'development-continuation.zip'
    with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as output:
        for name, raw in sorted(members.items()):
            info = zipfile.ZipInfo(name, (2026, 11, 17, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            output.writestr(info, raw)
    with zipfile.ZipFile(archive) as check:
        assert check.namelist() == [x['path'] for x in manifest]
        for row in manifest:
            assert digest(check.read(row['path'])) == row['sha256']
    result = dict(status='PASS_RETAINED_GENUINE_DEAD_CLOSURE_MANAGE_PREPARE_CONTINUE_NOT_MODULE_ACCEPTANCE',
                  runtimeCommit=RUNTIME, driverCommit=SOURCE, runtimeArchiveSha256=seal['archiveSha256'],
                  compiledSourceInputs=468, additionalCompilation=False, priorExecutedCommands=72,
                  resumedNewCommands=25, witnessCommands=97, fullSavedCommands=462,
                  incomingAttacks=9, incomingHits=3, healingRites=2, rpSpent=4, finalRp=3,
                  actualDeadRevision=436, closedRevision=437, finalRevision=462, finalClock=p['finalClock'],
                  finalSaveSha256=digest(final), actualBackupRecovery=True, correctedProbeFailures=2,
                  members=len(manifest), archiveSha256=digest(archive.read_bytes()), archiveBytes=archive.stat().st_size,
                  fullRegression=False, fivePaths=False, allSevenSpellsQualified=False, moduleAccepted=False,
                  scriptSha256=digest(Path(__file__).read_bytes()))
    (OUT / 'MEMBERS.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    (OUT / 'RETENTION.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
