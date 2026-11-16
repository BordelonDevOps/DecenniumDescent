"""Verify every final indexed artifact against its staged Git blob, without changing it."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
import subprocess

PACKET = Path(__file__).resolve().parents[1]
ROOT = PACKET.parents[3]
INDEX = PACKET/'implementation/ARTIFACT_INDEX.json'


def main():
    raw_index = INDEX.read_bytes()
    artifacts = json.loads(raw_index)['artifacts']
    prefix = (PACKET/'implementation').relative_to(ROOT).as_posix()+'/'
    requests = [':'+prefix+name for name in artifacts]
    requests.append(':'+INDEX.relative_to(ROOT).as_posix())
    payload = ('\n'.join(requests)+'\n').encode('utf-8')
    result = subprocess.run(['git','cat-file','--batch'], cwd=ROOT, input=payload,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    position, verified_bytes = 0, 0
    expected = list(artifacts.items())+[(INDEX.name, {'bytes':len(raw_index),
                                                   'sha256':hashlib.sha256(raw_index).hexdigest()})]
    for name, metadata in expected:
        end = result.stdout.index(b'\n', position)
        header = result.stdout[position:end].decode().split()
        assert len(header) == 3 and header[1] == 'blob', (name, header)
        size = int(header[2])
        position = end+1
        blob = result.stdout[position:position+size]
        assert size == metadata['bytes'] and hashlib.sha256(blob).hexdigest() == metadata['sha256'], name
        assert result.stdout[position+size:position+size+1] == b'\n'
        position += size+1
        if name != INDEX.name:
            verified_bytes += size
    assert position == len(result.stdout) and not result.stderr.strip()
    report = {'status':'PASS', 'verifiedAtUtc':datetime.now(timezone.utc).isoformat(),
              'scope':'All final indexed artifacts and the index itself compared to staged Git blobs; read-only reconciliation, not C# execution.',
              'artifacts':len(artifacts), 'artifactBytes':verified_bytes,
              'indexSha256':hashlib.sha256(raw_index).hexdigest(),
              'stagedParentCommit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()}
    (PACKET/'FINAL_STAGED_ARTIFACT_VERIFICATION.json').write_bytes((json.dumps(report,indent=2)+'\n').encode())
    print(json.dumps(report))


if __name__ == '__main__':
    main()
