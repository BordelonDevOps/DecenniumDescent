"""Verify TAC08's historical source pins and exact committed compilation inputs."""
import argparse
import hashlib
import io
import json
from pathlib import Path
import subprocess

PACKET = Path(__file__).resolve().parents[1]
ROOT = PACKET.parents[3]
ACCEPTED = '34229ec6f19c9569dd35fd7b6013b99f37759c85'
APPROVAL = '384b9c53-9d93-56f3-901b-cede1f7d3028'
CLARIFICATION = '94ea32c6-0c95-537d-83ec-732d1a0d171d'
RUNTIME_COMMIT = 'de2bc389d288b280ebb6387722da3d735b48cb03'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def require(value, message):
    if not value:
        raise ValueError(message)


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--build', type=Path, required=True)
    parser.add_argument('--commit', required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    rows = sum((read(PACKET / name)['sources'] for name in
                ('SOURCE_BINDINGS.json', 'CONTRACT_BINDINGS.json', 'APPROVAL_BINDINGS.json')), [])
    require(len(rows) == 95 and len({row['path'] for row in rows}) == 95, 'Approved pin inventory changed')
    raw = subprocess.check_output(['git', 'cat-file', '--batch'], cwd=ROOT,
        input=''.join(row['revision'] + ':' + row['path'] + '\n' for row in rows).encode())
    stream = io.BytesIO(raw)
    pins = []
    for row in rows:
        header = stream.readline().decode().split()
        require(len(header) == 3 and header[1] == 'blob', 'Missing historical source: ' + row['path'])
        data = stream.read(int(header[2]))
        require(stream.read(1) == b'\n' and header[0] == row['gitBlob']
                and len(data) == row['bytes'] and sha(data) == row['sha256'], 'Historical pin changed: ' + row['path'])
        # Implementation deliberately replaces accepted engine files. Non-engine
        # rules/decisions retain their exact previously inspected checkout identity.
        if not row['path'].startswith('engine/'):
            current = (ROOT / row['path']).read_bytes()
            require(len(current) == row['workingBytes'] and sha(current) == row['workingSha256'],
                    'Authority source changed: ' + row['path'])
        pins.append({'path': row['path'], 'revision': row['revision'], 'sha256': sha(data)})
    review = (PACKET / 'GPT_CONTRACT_REVIEW.md').read_text(encoding='utf-8-sig')
    clarification = (PACKET / 'GPT_FOCUS_DROP_CLARIFICATION.md').read_text(encoding='utf-8-sig')
    require(APPROVAL in review and CLARIFICATION in clarification, 'Actual review identities missing')
    build = read(args.build)
    require(build['status'] == 'PASS' and build['sourceHashes'], 'Compiled-source report must pass')
    paths = ['engine/' + row['path'].replace('\\', '/') for row in build['sourceHashes']]
    raw = subprocess.check_output(['git', 'cat-file', '--batch'], cwd=ROOT,
        input=''.join(args.commit + ':' + path + '\n' for path in paths).encode())
    stream = io.BytesIO(raw)
    compiled = []
    for row in build['sourceHashes']:
        path = 'engine/' + row['path'].replace('\\', '/')
        current = (ROOT / path).read_bytes()
        header = stream.readline().decode().split()
        require(len(header) == 3 and header[1] == 'blob', 'Missing committed input: ' + path)
        committed = stream.read(int(header[2]))
        require(stream.read(1) == b'\n', 'Invalid compiled-source batch boundary')
        require(sha(current) == row['sha256'].lower(), 'Build input changed: ' + path)
        require(current.replace(b'\r\n', b'\n') == committed.replace(b'\r\n', b'\n'), 'Uncommitted build input: ' + path)
        compiled.append({'path': path, 'workingSha256': sha(current), 'gitSha256': sha(committed)})
    changed = git('diff-tree', '--no-commit-id', '--name-only', '-r', args.commit).decode().splitlines()
    require(changed == ['engine/com.decennium.foundation/Tests/EditMode/ConnectedVialCases.cs'], 'Correction commit has unexpected scope')
    require(git('rev-parse', args.commit + '^').decode().strip() == RUNTIME_COMMIT, 'Correction does not directly follow runtime freeze')
    runtime_changed = git('diff-tree', '--no-commit-id', '--name-only', '-r', RUNTIME_COMMIT).decode().splitlines()
    require(len(runtime_changed) == 60 and all(path.startswith('engine/') for path in runtime_changed), 'Runtime commit scope differs')
    require(not git('diff', args.commit, '--', 'engine'), 'Engine changed after the implementation commit')
    args.output.parent.mkdir(parents=True, exist_ok=True)
    archive = args.output.parent / 'committed-engine-source.zip'
    subprocess.run(['git', 'archive', '--format=zip', '--output=' + str(archive.resolve()), args.commit, 'engine'], cwd=ROOT, check=True)
    artifacts = ['SOURCE_BINDINGS.json', 'CONTRACT_BINDINGS.json', 'APPROVAL_BINDINGS.json', 'SPELL_CANDIDATES.json',
                 'APPROVED_CASTING_CONTRACT.md', 'GPT_CONTRACT_REVIEW.md', 'GPT_FOCUS_DROP_CLARIFICATION.md', 'GPT_FOCUS_DROP_CLARIFICATION.json']
    report = {'status': 'PASS', 'implementationCommit': args.commit, 'acceptedPredecessorSource': ACCEPTED,
              'runtimeImplementationCommit': RUNTIME_COMMIT,
              'implementationCommits': [{'commit': RUNTIME_COMMIT, 'exactChangedFiles': runtime_changed},
                                        {'commit': args.commit, 'exactChangedFiles': changed}],
              'actualContractApproval': APPROVAL, 'actualFocusClarification': CLARIFICATION,
              'sourceAuthority': 'Source-bound TEST_ONLY implementation; no production or release promotion',
              'historicalPinsVerified': len(pins), 'historicalPins': pins, 'compiledSources': compiled,
              'exactChangedFiles': sorted(set(runtime_changed + changed)), 'buildReportSha256': sha(args.build.read_bytes()),
              'sourceArchive': archive.name, 'sourceArchiveSha256': sha(archive.read_bytes()),
              'authorityArtifacts': [{'path': path, 'sha256': sha((PACKET / path).read_bytes())} for path in artifacts],
              'scope': 'Historical authority pins and exact committed/build source identity. Gameplay, full regression, compatibility and final GPT acceptance are separate gates.'}
    args.output.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(f'PASS: {len(pins)} historical pins, {len(compiled)} committed compilation inputs and source archive')


if __name__ == '__main__':
    main()
