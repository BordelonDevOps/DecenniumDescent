from pathlib import Path
import hashlib, json, sys, zipfile
root = Path(__file__).resolve().parents[5]
run = root / sys.argv[1]
package = root / 'engine/com.decennium.foundation'
report = json.loads((run / 'results.json').read_text(encoding='utf-8-sig'))
sources = sorted(p for folder, glob in [('Runtime/Core','*.cs'),('Runtime/Persistence','*.cs'),('Laboratory/Model','*.cs'),('Tests/EditMode','*Cases.cs')] for p in (package / folder).glob(glob))
expected = {x['path'].replace('\\','/'):x['sha256'] for x in report.get('sourceHashes',[])}
archive = run / 'source-snapshot.zip'
assert not archive.exists(), 'Never overwrite a retained source archive'
with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as z:
    for p in sources:
        data = p.read_bytes(); name = p.relative_to(root / 'engine').as_posix()
        if expected: assert expected[name] == hashlib.sha256(data).hexdigest(), name
        z.writestr(name, data)
print(json.dumps({'archive':str(archive),'members':len(sources),'sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),'compilation':report.get('coreCompilation','FAILED_NO_PASS')}))
