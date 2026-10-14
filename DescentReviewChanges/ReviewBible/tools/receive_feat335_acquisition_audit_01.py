"""Verify and preserve the downloaded GPT audit and its exact submitted input."""
from pathlib import Path, PurePosixPath
from datetime import datetime, timezone
from hashlib import sha256
import json
import zipfile

G = Path(r'C:\Github\DecenniumDescent')
A = G / 'docs/audit/2026-10-08/full-game'


def binding(path):
    data = path.read_bytes()
    return {'path': path.relative_to(G).as_posix(), 'bytes': len(data), 'sha256': sha256(data).hexdigest()}


def extract_checked(archive, destination, digest):
    assert sha256(archive.read_bytes()).hexdigest() == digest
    assert not destination.exists(), 'Never replace preserved inputs.'
    with zipfile.ZipFile(archive) as z:
        names = z.namelist()
        assert len(names) == len(set(names))
        for name in names:
            pure = PurePosixPath(name)
            assert not pure.is_absolute() and '..' not in pure.parts and '\\' not in name and ':' not in name
            assert not z.getinfo(name).is_dir()
            assert (z.getinfo(name).external_attr >> 16) & 0o170000 != 0o120000
        manifest = json.loads(z.read('PACKAGE_MANIFEST.json'))
        items = manifest['files'] if 'files' in manifest else [{'path': k, **v} for k, v in manifest.items()]
        assert set(names) == {'PACKAGE_MANIFEST.json'} | {i['path'] for i in items}
        for item in items:
            data = z.read(item['path'])
            assert len(data) == item['bytes'] and sha256(data).hexdigest() == item['sha256'], item['path']
        destination.mkdir()
        for name in names:
            target = destination / name
            assert target.resolve().is_relative_to(destination.resolve())
            target.parent.mkdir(parents=True, exist_ok=True)
            with target.open('xb') as handle:
                handle.write(z.read(name))
            assert target.read_bytes() == z.read(name)
        return manifest, [binding(destination / name) for name in names]


verdict = A / 'FEAT335_Acquisition_Audit_01_Verdict_and_Evidence.zip'
submission = A / 'DD_FEAT335_Acquisition_Audit_01.zip'
receipt = A / 'FEAT335_ACQUISITION_AUDIT_01_DOWNLOAD_CHECK.json'
assert not receipt.exists()
manifest, files = extract_checked(verdict, A / 'feat335-acquisition-audit-01-verdict',
    '0d66474aef4307de1cc1b152841df7a2f38c0cf87836ac80b72e1c92c722a397')
submitted, frozen = extract_checked(submission, A / 'feat335-acquisition-audit-01-submission-frozen',
    '0a36502226f065911bec1c7fa1951f7b46fd68f21c4695fc4e6a4e7fc9b47db8')
assert len(files) == 22 and len(frozen) == 199
assert sha256((A / 'feat335-acquisition-audit-01-submission-frozen/PACKAGE_MANIFEST.json').read_bytes()).hexdigest() == manifest['submission']['rootManifestSha256']
data = {'recordedAtUtc': datetime.now(timezone.utc).isoformat(), 'auditId': manifest['auditId'],
        'status': 'Actual terminal GPT audit downloaded; every returned and submitted payload verified. Reviewers scripts not yet independently reproduced by this receipt.',
        'verdictArchive': binding(verdict), 'submittedArchive': binding(submission), 'returnedPayloads': 21,
        'returnedMembersIncludingManifest': 22, 'submittedPayloads': 198, 'returnedFiles': files, 'frozenSubmittedFiles': frozen,
        'finalResponse': binding(A / 'FEAT335_ACQUISITION_AUDIT_01_RESPONSE.txt'),
        'terminalObservation': binding(A / 'DI7_AUTHORING_GPT_STATUS.json'), 'correctionsApplied': False,
        'fullFeatCandidateApproved': False, 'sourceInformationDeleted': 0, 'pushed': False, 'cosmologyReviewed': False}
receipt.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({k: v for k, v in data.items() if k not in ['returnedFiles', 'frozenSubmittedFiles']}, indent=2))
