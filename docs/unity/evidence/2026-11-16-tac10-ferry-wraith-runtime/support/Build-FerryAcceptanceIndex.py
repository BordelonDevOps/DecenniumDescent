"""Reconcile retained packet bytes; never infer gameplay or review acceptance."""
import hashlib
import json
from pathlib import Path
import subprocess
import zipfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
PACKET = HERE.parent
RUNTIME = 'c8ffee78d5047131317ff923c8e3a575b6c51f3a'


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def main():
    changed = subprocess.check_output(['git', '-C', str(ROOT), 'diff', '--name-only', RUNTIME, '--', 'engine']).decode().splitlines()
    assert changed == ['engine/tools/Open-ConnectedExpedition.ps1']
    build = ROOT / 'engine/artifacts/ferry-wraith/dash-correction/run-20261117T110451175Z-06a69ef8/results.json'
    compiled = read(build)
    assert compiled['status'] == compiled['coreCompilation'] == 'PASS' and len(compiled['sourceHashes']) == 468
    for row in compiled['sourceHashes']:
        assert sha((ROOT / 'engine' / row['path'].replace('\\', '/')).read_bytes()) == row['sha256']
    archives, direct = [], []
    for folder in sorted(PACKET.iterdir()):
        if not folder.is_dir() or folder.name == 'support':
            continue
        bundles = list(folder.glob('*.zip'))
        manifest_path = folder / 'MEMBERS.json'
        if not bundles:
            direct.append(dict(path=folder.name, files=sum(p.is_file() for p in folder.rglob('*')), classification='Earlier direct-file checkpoint; no archive reconciliation claim'))
            continue
        assert len(bundles) == 1 and manifest_path.exists(), folder
        archive = bundles[0]
        rows = read(manifest_path)
        assert isinstance(rows, list)
        with zipfile.ZipFile(archive) as bundle:
            assert len(bundle.namelist()) == len(set(bundle.namelist())) == len(rows)
            assert set(bundle.namelist()) == {row['path'] for row in rows}
            for row in rows:
                raw = bundle.read(row['path'])
                assert len(raw) == row['bytes'] and sha(raw) == row['sha256'], (folder.name, row['path'])
        retention_path = folder / 'RETENTION.json'
        retention = read(retention_path) if retention_path.exists() else {}
        archives.append(dict(path=archive.relative_to(PACKET).as_posix(), bytes=archive.stat().st_size,
                             sha256=sha(archive.read_bytes()), members=len(rows), manifestSha256=sha(manifest_path.read_bytes()),
                             retentionSha256=sha(retention_path.read_bytes()) if retention_path.exists() else None,
                             retainedStatus=retention.get('status'), classification='Retained historical or focused evidence; preserve each report scope, source and failure status'))
    reviews = []
    for path in sorted(PACKET.glob('GPT_*REVIEW.json')):
        record = read(path)
        reviews.append(dict(path=path.name, sha256=sha(path.read_bytes()), scope=record.get('scope'),
                            requestId=record.get('requestId'), responseId=record.get('responseId')))
    audit = read(PACKET / 'CONSUMER_AUDIT.json')
    assert audit['inventoryRows'] == 332 and audit['runtimeCommit'] == RUNTIME
    report = dict(status='CANDIDATE_ARCHIVE_AND_FROZEN_SOURCE_RECONCILED_NOT_FINAL_ACCEPTANCE',
                  collectorSha256=sha(Path(__file__).read_bytes()), runtimeCommit=RUNTIME,
                  qualifiedHostCommit='3d0afc12d2444d2d6d77e3ff3729f2ff8236be3d', engineDifferences=changed,
                  compiledInputs=468, compilationReportSha256=sha(build.read_bytes()),
                  archives=archives, archiveMembers=sum(x['members'] for x in archives), directCheckpoints=direct,
                  reviews=reviews, consumerAuditSha256=sha((PACKET / 'CONSUMER_AUDIT.json').read_bytes()),
                  currentBroadQualification=dict(regression='dash-regression-checkpoint', runId='72f6bdda13924fad8eb5b516ec19018b',
                      passed=1584, failed=0, fivePaths='five-path-checkpoint', commandsPerPath=463,
                      comparisons=10185, authenticCompatibility='compatibility-checkpoint', supportedProfiles='95-113'),
                  limits='Archive verification is supporting evidence, not execution, final review, whole-engine completion or production authority. Historical failed attempts and earlier runtime builds remain historical. Actual GPT55f63234 approved the additional mechanical new-epoch cure allocation; its completed producer supplement remains separate from an entirely genuine fear-through-entry route, which is unproved. Actual final GPT/Codex acceptance remains required. Finish TAC-10 then stop; no successor, Unity, storage or Support work.')
    (PACKET / 'ACCEPTANCE_INDEX.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(dict(status=report['status'], archives=len(archives), members=report['archiveMembers'], sourceInputs=468)))


if __name__ == '__main__':
    main()
