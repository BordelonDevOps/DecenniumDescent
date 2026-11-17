"""Freeze the selected Petrified correction and its actual causal replay evidence."""
import hashlib
import io
import json
from pathlib import Path
import subprocess
import zipfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
SOURCE = 'aba482bf6d3cfe21f0dd063c738326039868154c'
INITIAL = '96a0811b86d6ce2a38f22b2cf6a0529bd5b9f1cc'
BASE = '37ce577fbb79398042c5a57e9b515bf09434c803'
DEV = ROOT / 'engine/artifacts/ferry-wraith/development'
PACKET = 'docs/unity/evidence/2026-11-16-tac10-ferry-wraith-runtime/'
OUT = HERE.parent / 'provenance-checkpoint'


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def main():
    assert not OUT.exists(), 'Do not overwrite retained evidence.'
    members = {}
    summaries = []
    for label, source, build_name, probe_name, genesis_name, static_name in [
        ('initial', INITIAL, 'run-20261117T065903864Z-e8471213', 'fresh-fire-20261117T0702Z',
         'genesis-probe-20261117T0701Z', 'static-20261117T070043151Z-c9a08aed'),
        ('selected', SOURCE, 'run-20261117T071415133Z-e89f9933', 'provenance-fresh-fire-20261117T0717Z',
         'genesis-probe-20261117T0719Z', 'static-20261117T071843545Z-209dce42')]:
        build = DEV / build_name
        probe = DEV / probe_name
        genesis = DEV / genesis_name
        static = ROOT / 'engine/artifacts' / static_name
        b, p, g, st = [read(x / ('results.json' if x in (build, static) else 'RESULT.json'))
                       for x in (build, probe, genesis, static)]
        assert b['status'] == st['status'] == 'PASS' and b['passed'] == 1 and b['failed'] == 0
        assert len(b['sourceHashes']) == 467 and len(st['sourceHashes']) == 975
        assert p['status'] == 'PASS_GENUINE_CURRENT_PREFIX_ADMISSION_FIRST_FIRE_ONLY'
        assert len(p['cases']) == 1 and p['cases'][0]['Passed']
        assert g['status'] == 'PASS_DEVELOPMENT_GENESIS_ONLY' and len(g['checks']) == 7
        # Only named engine and executed support/review files are archived from Git.
        paths = ['engine', PACKET + 'support/Probe-FerryGenesis.ps1',
                 PACKET + 'support/Probe-FerryController.ps1',
                 PACKET + 'GPT_TARGET_REVIEW.json']
        if label == 'selected':
            paths.append(PACKET + 'support/Probe-FerryFreshFire.ps1')
            paths.append(PACKET + 'GPT_PROVENANCE_REVIEW.json')
        frozen = zipfile.ZipFile(io.BytesIO(subprocess.check_output(
            ['git', 'archive', '--format=zip', source, '--', *paths], cwd=ROOT)))
        for report in (b, st):
            for row in report['sourceHashes']:
                assert digest(frozen.read('engine/' + row['path'].replace('\\', '/'))) == row['sha256'], row['path']
        for report in (p, g):
            assert report['compilationReport']['sha256'] == digest((build / 'results.json').read_bytes())
            for row in report['assemblies']:
                assert row['sha256'] == digest((build / ('Decennium.Foundation.' + row['name'] + '.dll')).read_bytes())
        for row in g['executedSources']:
            assert row['sha256'] == digest(frozen.read(row['path'].replace('\\', '/')))
        for key, name in [('executedScript', 'Probe-FerryFreshFire'), ('controllerScript', 'Probe-FerryController')]:
            raw = (probe / (name + '.executed.ps1')).read_bytes()
            assert p[key]['sha256'] == digest(raw)
            # The initial probe was executed later with the 8aa7 support script.
            revision = source if label == 'selected' else '8aa7a200a3c5b991ce21083c5292777fa1d158fe'
            assert raw == subprocess.check_output(['git', 'show', revision + ':' + PACKET + 'support/' + name + '.ps1'], cwd=ROOT)
        controller = read(probe / 'controller/RESULT.json')
        assert controller['status'] == 'PASS_FIRST_GENUINE_CREATURE_FIRE_NOT_MODULE_ACCEPTANCE'
        assert len(controller['commands']) == 5 and controller['finalRevision'] == 351
        assert len(controller['checks']) == (5 if label == 'selected' else 4)
        assert controller['admissionSource']['sha256'] == digest((probe / 'saves/ferry-admitted.ddsave').read_bytes())
        first = (probe / 'controller/first-fire-hit.ddsave').read_bytes()
        assert first == (probe / 'controller/first-fire-hit-restored.ddsave').read_bytes()
        controls = read(build / 'saves/petrified-poison-controls.json')
        assert len(controls['rows']) == 24 and controls['legacyEffective'] == 2
        if label == 'selected':
            assert controls['wireRoundtrips'] == 25
            protected, ended = controls['protectedAtPhase'], controls['unprotectedAtPhase']
            assert protected['ConditionEvaluation'] == ended['ConditionEvaluation']
            assert protected['ConditionEvaluation']['Phase'] == 3
            assert protected['ConditionOperationCount'] + 1 == ended['ConditionOperationCount']
            assert protected['Effective'] == 0 and ended['Effective'] == 4
            forgery = controller['forgery']
            assert forgery['rejection'] == 'InvalidSharedWorldReplay'
            assert forgery['earlierPrefix'] + 1 == forgery['laterPrefix']
            assert forgery['sha256'] == digest((probe / 'controller/forged-earlier-prefix.ddsave').read_bytes())
        for section, folder in [('build', build), ('connected', probe), ('genesis', genesis), ('static', static)]:
            for path in sorted(folder.rglob('*')):
                if path.is_file():
                    members[label + '/' + section + '/' + path.relative_to(folder).as_posix()] = path.read_bytes()
        changed = subprocess.check_output(['git', 'diff', BASE, source, '--name-only', '--', 'engine'], cwd=ROOT).decode().splitlines()
        assert len(changed) == 6
        for path in changed:
            members[label + '/changed-source/' + path] = frozen.read(path)
        for path in paths[1:]:
            if path in frozen.namelist():
                members[label + '/source/' + path] = frozen.read(path)
        summaries.append(dict(label=label, sourceCommit=source, compiledSourceInputs=467, staticInputs=975,
                              mechanicalRows=24, codecRoundtrips=controls.get('wireRoundtrips', 0), genesisChecks=7,
                              selectedCasesPassed=1, connectedCasesPassed=1, controllerChecks=len(controller['checks']),
                              finalRevision=351, finalSaveSha256=digest(first)))
    members['executed-support/Retain-FerryProvenance.py'] = Path(__file__).read_bytes()
    manifest = [dict(path=name, bytes=len(raw), sha256=digest(raw)) for name, raw in sorted(members.items())]
    OUT.mkdir()
    archive = OUT / 'development-provenance.zip'
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
    result = dict(status='PASS_RETAINED_PETRIFIED_CORRECTION_PENDING_ACTUAL_REVIEW', checkpoints=summaries,
                  members=len(manifest), archiveSha256=digest(archive.read_bytes()), archiveBytes=archive.stat().st_size,
                  causalForgeryRejection='InvalidSharedWorldReplay', fullRegression=False, seal=False,
                  moduleAccepted=False, scriptSha256=digest(Path(__file__).read_bytes()))
    (OUT / 'MEMBERS.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    (OUT / 'RETENTION.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
