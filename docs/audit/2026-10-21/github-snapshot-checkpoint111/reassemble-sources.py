"""Run with the repository root and an output folder; never overwrites an existing file."""
from pathlib import Path
import hashlib,json,sys
root=Path(sys.argv[1]);out=Path(sys.argv[2])
manifest=json.loads(Path(__file__).with_name('SPLIT_SOURCES.json').read_bytes())
for source in manifest['sources']:
    target=out/source['sourcePath'];target.parent.mkdir(parents=True,exist_ok=True)
    digest=hashlib.sha256();size=0
    with target.open('xb') as f:
        for part in source['parts']:
            raw=(root/part['path']).read_bytes()
            assert len(raw)==part['bytes'] and hashlib.sha256(raw).hexdigest()==part['sha256']
            f.write(raw);digest.update(raw);size+=len(raw)
    assert size==source['bytes'] and digest.hexdigest()==source['sha256']
    print(target)
