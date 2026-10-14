"""Reproduce the downloaded reviewer's finite checks on isolated frozen inputs.

Does not overwrite the original reviewer package, source files, or its reports.
The reviewed scripts write reports; they were inspected before this invocation.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import shutil
import subprocess
import sys
import zipfile

G = Path(__file__).resolve().parents[3]
A = G / 'docs/audit/2026-10-08/full-game'
W = A / 'advanced167-local-source-verification'


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    assert not W.exists(), 'Preserve the previous reproduction instead of overwriting it.'
    source = W / 'frozen-source'
    authoring = W / 'reviewer-script-working-copy'
    archive = A / 'DD_Advanced_Craft_167_Joint_Source_v2.zip'
    assert sha(archive) == 'b7fb04e4410bb94659b6ffa5f853e33092ecc44ebec476b0ff880ba46923a00a'
    original = A / 'advanced167-source-authoring-reviewer-files'
    before = {p.name: sha(p) for p in original.iterdir() if p.is_file()}
    source.mkdir(parents=True)
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        for name in z.namelist():
            target = (source / name).resolve()
            assert target.is_relative_to(source.resolve()), name
        z.extractall(source)
    shutil.copytree(original, authoring)
    commands = [
        [sys.executable, '-X', 'utf8', str(authoring / 'verify_advanced_sources.py'),
         str(source), '--output', str(W), '--archive', str(archive)],
        [sys.executable, '-X', 'utf8', str(authoring / 'verify_authoring_registers.py'),
         str(source), '--authoring', str(authoring)],
    ]
    for i, command in enumerate(commands):
        result = subprocess.run(command, capture_output=True, text=True, encoding='utf-8')
        (W / f'command-{i+1}.txt').write_text(result.stdout + result.stderr, encoding='utf-8')
        assert result.returncode == 0, result.stdout + result.stderr
    reports = []
    for report in [W / 'INDEPENDENT_SOURCE_CHECKS.json', authoring / 'AUTHORING_REGISTER_CHECKS.json']:
        data = json.loads(report.read_text(encoding='utf-8'))
        earlier = json.loads((original / report.name).read_text(encoding='utf-8'))
        assert not data['failed']
        assert data == earlier, report.name + ': reproduced report differs'
        reports.append({'path': report.relative_to(G).as_posix(), 'checks': data['checks'],
                        'failed': 0, 'sameParsedReportAsReviewer': True, 'sha256': sha(report)})
    assert before == {p.name: sha(p) for p in original.iterdir() if p.is_file()}
    receipt = {
        'status': 'Reviewer source/register checks reproduced on frozen submitted inputs',
        'createdAtUtc': datetime.now(timezone.utc).isoformat(), 'reports': reports,
        'originalReviewerFilesUnchanged': len(before), 'sourceArchiveSha256': sha(archive),
        'scope': 'Byte preservation, complete original objects, source/book/version bindings, register membership and fixed arithmetic only.',
        'runtimeValidation': False, 'exactCardsApproved': 0, 'classCardsPromoted': 0,
        'worldAuthentication': False, 'balanceApproved': False,
    }
    (A / 'ADVANCED_CRAFT_LOCAL_SOURCE_VERIFICATION.json').write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(receipt, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
