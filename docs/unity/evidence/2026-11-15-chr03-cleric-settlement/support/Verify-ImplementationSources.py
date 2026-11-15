"""Verify historical source pins and the exact committed CHR03 source/build identity."""
import argparse
import hashlib
import io
import json
from pathlib import Path
import subprocess

PACKET = Path(__file__).resolve().parents[1]
ROOT = PACKET.parents[3]

def digest(data):
    return hashlib.sha256(data).hexdigest()

def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))

def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()

def require(value, message):
    if not value:
        raise ValueError(message)

def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)

def pointer(value, path):
    for part in path.strip('/').split('/'):
        value = value[int(part)] if isinstance(value, list) else value[part]
    return value

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--build', type=Path, required=True)
    parser.add_argument('--commit', required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    bindings = read(PACKET / 'COMPLETE_SOURCE_BINDINGS.json')
    rows = bindings['sources']
    require(len(rows) == 65, 'Source inventory changed')
    raw = subprocess.check_output(['git', 'cat-file', '--batch'], cwd=ROOT,
        input=''.join(row['revision'] + ':' + row['path'] + '\n' for row in rows).encode())
    reader, payloads = io.BytesIO(raw), {}
    for row in rows:
        header = reader.readline().decode().split()
        require(len(header) == 3 and header[1] == 'blob', 'Missing source ' + row['path'])
        data = reader.read(int(header[2]))
        require(reader.read(1) == b'\n', 'Invalid Git framing')
        require(header[0] == row['gitBlob'] and len(data) == row['bytes'] and digest(data) == row['sha256'],
                'Pinned source changed: ' + row['path'])
        payloads[row['path']] = data
    selected = read(PACKET / 'SELECTED_SETTLEMENT_BINDINGS.json')
    cleric = json.loads(payloads[selected['clericFile']])
    checks = []
    for row in selected['cards'] + selected['engine'] + [selected['schedule']]:
        actual = digest(canonical(pointer(cleric, row['pointer'])))
        require(actual == row['sha256'], 'Selected Cleric source changed: ' + row['pointer'])
        checks.append({'pointer': row['pointer'], 'sha256': actual})
    spell = selected['earnedSpell']
    catalog = json.loads(payloads['DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json'])
    for field, hash_field in [('wholeCardPointer', 'wholeCardSha256'), ('procedurePointer', 'procedureSha256')]:
        actual = digest(canonical(pointer(catalog, spell[field])))
        require(actual == spell[hash_field], 'Earned spell source changed')
        checks.append({'pointer': spell[field], 'sha256': actual})
    build = read(args.build)
    require(build['status'] == 'PASS', 'Compiled source report failed')
    compiled = []
    for row in build['sourceHashes']:
        path = 'engine/' + row['path'].replace('\\', '/')
        data = (ROOT / path).read_bytes()
        require(digest(data) == row['sha256'], 'Working source differs from build: ' + path)
        # Git normalizes line endings; compare the checked-in content logically as well.
        committed = git('show', args.commit + ':' + path)
        require(data.replace(b'\r\n', b'\n') == committed.replace(b'\r\n', b'\n'), 'Source missing from commit: ' + path)
        compiled.append({'path': path, 'workingSha256': row['sha256'], 'gitSha256': digest(committed)})
    changed = git('diff-tree', '--no-commit-id', '--name-only', '-r', args.commit).decode().splitlines()
    require(changed and all(path.startswith('engine/') for path in changed), 'Implementation commit scope differs')
    archive = args.output.parent / 'committed-engine-source.zip'
    subprocess.run(['git', 'archive', '--format=zip', '--output=' + str(archive.resolve()), args.commit, 'engine'], cwd=ROOT, check=True)
    report = {'status': 'PASS', 'implementationCommit': args.commit, 'sourceAuthority': 'ReviewBible provisional; no release promotion',
        'historicalPinsVerified': len(rows), 'selectedSourceChecks': checks, 'buildReportSha256': digest(args.build.read_bytes()),
        'compiledSources': compiled, 'exactChangedFiles': changed, 'sourceArchive': archive.name,
        'sourceArchiveSha256': digest(archive.read_bytes()),
        'scope': 'Implementation source identity and source bindings; gameplay and final acceptance require separate evidence.'}
    args.output.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print('PASS: 65 historical pins, 16 selected source checks, exact committed build sources and archive')

if __name__ == '__main__':
    main()
