"""Retain corrected source/assemblies, actual red regressions and superseded runs."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[5]
PACKET = Path(__file__).resolve().parents[1]
read = lambda p: json.loads(p.read_text(encoding='utf-8-sig'))
digest = lambda b: hashlib.sha256(b).hexdigest()
parser = argparse.ArgumentParser()
for name in ('build','focused','static','output'):
    parser.add_argument('--'+name, type=Path, required=True)
args = parser.parse_args()
build, focus, static, output = (getattr(args,n).resolve() for n in ('build','focused','static','output'))
assert not output.exists()
compiled, focused, checked = (read(p/'results.json') for p in (build,focus,static))
assert compiled['status'] == focused['status'] == checked['status'] == 'PASS'
assert len(focused['cases']) == 6 and all(x['Passed'] and not x['Error'] for x in focused['cases'])
assert focused['compiledReportSha256'] == digest((build/'results.json').read_bytes())
for report in (compiled,focused,checked):
    for row in report['sourceHashes']:
        assert digest((ROOT/'engine'/row['path']).read_bytes()) == row['sha256'], row['path']
for name,row in focused['assemblies'].items():
    assert digest((build/('Decennium.Foundation.'+name+'.dll')).read_bytes()) == row['sha256']

members = {}
def tree(folder,prefix):
    for p in sorted(folder.rglob('*')):
        if p.is_file() and p.suffix != '.dll':
            members[prefix+'/'+p.relative_to(folder).as_posix()] = p
tree(focus,'corrected-focused')
repro = ROOT/'engine/artifacts/declared-geometry/review-reproduction'
tree(repro,'reproductions')
old = ROOT/'engine/artifacts/declared-geometry/regression-original'
assert read(old/'DISPOSITION.json')['status'] == 'SUPERSEDED_INCOMPLETE'
assert read(old/'PREFIX_SUMMARY.json')['runId'] == '062fe06abe744b759b4b67943e0d9221'
tree(old,'superseded-original-regression')
tree(ROOT/'engine/artifacts/declared-geometry/qualification','superseded-qualification')
repro_build = repro/'run-20261117T021828979Z-b4682748'
repro_report = read(repro_build/'results.json')
assert repro_report['status'] == 'FAIL' and repro_report['failed'] == 1
assert not read(repro/'discovery-on-original/result.json')['Passed']
test_path = 'com.decennium.foundation/Tests/EditMode/DeclaredGeometryCases.cs'
test_source = (ROOT/'engine'/test_path).read_bytes().replace(b'blocked.Query.Code == "BlockedTacticalStep"', b'blocked.Query.Code == "Blocked"')
assert digest(test_source) == next(x['sha256'] for x in repro_report['sourceHashes'] if x['path'].replace('\\','/') == test_path)
output.mkdir()
(output/'reproduction-DeclaredGeometryCases.cs.txt').write_bytes(test_source)

def archive(path,entries):
    rows=[]
    with zipfile.ZipFile(path,'x',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for name,source in sorted(entries.items()):
            b=source.read_bytes();z.writestr(name,b);rows.append(dict(path=name,bytes=len(b),sha256=digest(b)))
    with zipfile.ZipFile(path) as z:
        assert sorted(z.namelist()) == sorted(x['path'] for x in rows)
        for row in rows:
            b=z.read(row['path']);assert len(b)==row['bytes'] and digest(b)==row['sha256']
    return dict(path=path.name,bytes=path.stat().st_size,sha256=digest(path.read_bytes()),members=rows)
assemblies={p.name:p for p in build.glob('*.dll')}
assert len(assemblies)==4
report=dict(status='PASS_CORRECTION_RETENTION',scope='Six focused cases, two actual red reproductions and superseded original prefixes; full qualification pending',
            sourceBase=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
            evidence=archive(output/'correction-evidence.zip',members),assemblies=archive(output/'compiled-assemblies.zip',assemblies))
for name,p in [('compiled-results.json',build/'results.json'),('static-results.json',static/'results.json')]:
    (output/name).write_bytes(p.read_bytes())
(output/'RETENTION.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:{f:report[k][f] for f in ('path','bytes','sha256')} for k in ('evidence','assemblies')}))
