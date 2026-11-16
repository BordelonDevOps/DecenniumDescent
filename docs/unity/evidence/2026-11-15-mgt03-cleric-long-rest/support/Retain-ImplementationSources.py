"""Bind historical authority and the exact compiled Long Rest implementation. Runs no gameplay."""
import argparse
import hashlib
import io
import json
from pathlib import Path
import subprocess
import zipfile

PACKET = Path(__file__).resolve().parents[1]
ROOT = PACKET.parents[3]
SOURCE = 'e0994929b444b15fc38957eb80cc34ab19d56db6'
ACCEPTED = '0e5928bddd5abce47c16ff86172f5613423a2460'

def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))

def write(path, value):
    path.write_bytes((json.dumps(value, indent=2, ensure_ascii=False) + '\n').encode())

def relation(a, b):
    if a == b:
        return 'exact'
    if a.replace(b'\r\n', b'\n') == b.replace(b'\r\n', b'\n'):
        return 'line-endings-only'
    raise AssertionError('Source differs beyond line endings')

def blobs(requests):
    # One read-only Git invocation, preserving exact blob bytes including binary books.
    if not requests:
        return []
    data = subprocess.check_output(
        ['git', 'cat-file', '--batch'], input=('\n'.join(requests)+'\n').encode(), cwd=ROOT)
    result = []
    at = 0
    for request in requests:
        end = data.index(b'\n', at)
        identity, kind, length = data[at:end].decode().split(' ')
        assert kind == 'blob', (request, kind)
        size = int(length)
        body = data[end+1:end+1+size]
        assert len(body) == size and data[end+1+size:end+2+size] == b'\n'
        result.append((identity, body))
        at = end+2+size
    assert at == len(data)
    return result

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--build', type=Path, required=True)
    parser.add_argument('--regression', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    build, regression, output = args.build.resolve(), args.regression.resolve(), args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    assert not git('diff', SOURCE, '--', 'engine').strip(), 'Frozen engine changed'
    report = read(build/'results.json')
    assert report['status'] == 'PASS' and report['failed'] == 0
    assert len(report['sourceHashes']) == 435
    pins = read(PACKET/'SOURCE_BINDINGS.json')['sources']
    assert len(pins) == 55
    historical = []
    for pin, (identity, body) in zip(pins, blobs([p['revision']+':'+p['path'] for p in pins])):
        assert identity == pin['gitBlob'] and len(body) == pin['bytes'] and sha(body) == pin['sha256'], pin['path']
        historical.append({**pin, 'historicalBlobVerified': True})
    paths = ['engine/'+x['path'].replace('\\','/') for x in report['sourceHashes']]
    compiled = []
    for entry, path, (identity, body) in zip(report['sourceHashes'], paths, blobs([SOURCE+':'+p for p in paths])):
        actual = (ROOT/path).read_bytes()
        assert sha(actual) == entry['sha256'], path
        compiled.append({'path': path, 'gitBlob': identity, 'gitBytes': len(body), 'gitSha256': sha(body),
                         'compiledBytes': len(actual), 'compiledSha256': sha(actual), 'relation': relation(body, actual)})
    archive = git('archive', '--format=zip', SOURCE, 'engine')
    with zipfile.ZipFile(io.BytesIO(archive)) as z:
        for entry in compiled:
            body = z.read(entry['path'])
            assert sha(body) == entry['gitSha256'] and len(body) == entry['gitBytes']
    (output/'committed-engine-source.zip').write_bytes(archive)
    launch = read(regression/'launch.json')
    assert launch['sourceCommit'] == SOURCE and launch['requiredCount'] == 1553 and launch['sourceCommitted']
    binary_buffer = io.BytesIO()
    binaries = []
    with zipfile.ZipFile(binary_buffer, 'w', zipfile.ZIP_DEFLATED) as z:
        for name, expected in launch['assemblies'].items():
            body = (regression/'execution-assemblies'/name).read_bytes()
            assert sha(body) == expected and body == (build/name).read_bytes(), name
            item = zipfile.ZipInfo(name, date_time=(1980,1,1,0,0,0))
            item.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(item, body)
            binaries.append({'path':name,'bytes':len(body),'sha256':sha(body)})
    binary_archive = binary_buffer.getvalue()
    (output/'execution-assemblies.zip').write_bytes(binary_archive)
    commits = ['27710eee7b1a5614500c8896fd21c7c165e083fd',
               git('rev-parse','8f740cfd5').decode().strip(), SOURCE]
    commit_records = [{'commit':c,'exactChangedFiles':git('diff-tree','--no-commit-id','--name-only','-r',c).decode().splitlines()} for c in commits]
    authority_paths = ['engine/AGENTS.md','docs/unity/DEVELOPMENT_BRIEF.md','docs/unity/DEVELOPMENT_HANDOFF.md',
        'docs/mechanics/CONTINUITY_SOURCE_OF_TRUTH.md','docs/canon/REPOSITORY_PROMOTION.md',
        'docs/unity/evidence/2026-11-15-mgt03-cleric-long-rest/GPT_CONTRACT_REVIEW.json',
        'docs/unity/evidence/2026-11-15-mgt03-cleric-long-rest/SOURCE_API_CONTRACT.md',
        'docs/unity/evidence/2026-11-15-chr05-cleric-conviction/GPT_DEPENDENCY_REVIEW.json']
    authority = []
    for path, (identity, body) in zip(authority_paths, blobs([SOURCE+':'+p for p in authority_paths])):
        authority.append({'path':path,'revision':SOURCE,'gitBlob':identity,'bytes':len(body),'sha256':sha(body)})
    write(output/'SOURCE_AUDIT.json', {
        'status':'PASS','implementationCommit':SOURCE,'acceptedPredecessorSource':ACCEPTED,
        'actualContractApproval':'8588491a-0698-50ec-9830-b4ad4208d1ce','implementationCommits':commit_records,
        'historicalPinsVerified':55,'historicalPins':historical,'compiledSources':compiled,
        'buildReportSha256':sha((build/'results.json').read_bytes()),'authorityArtifacts':authority,
        'exactEngineChangedFiles':git('diff','--name-only',ACCEPTED,SOURCE,'--','engine').decode().splitlines(),
        'sourceArchive':{'path':'committed-engine-source.zip','bytes':len(archive),'sha256':sha(archive)},
        'binaryArchive':{'path':'execution-assemblies.zip','bytes':len(binary_archive),'sha256':sha(binary_archive),'entries':binaries},
        'scope':'Read-only source, compile-input and frozen-binary reconciliation. No gameplay execution, module acceptance, production promotion or Unity qualification.'})
    print('PASS: 55 historical pins, 435 compilation inputs, exact source archive and four frozen assemblies.')

if __name__ == '__main__':
    main()
