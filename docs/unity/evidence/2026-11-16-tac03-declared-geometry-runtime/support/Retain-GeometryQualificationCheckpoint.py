"""Retain only completed corrected checks; never claim live workers or paths complete."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[5]
read = lambda p: json.loads(p.read_text(encoding='utf-8-sig'))
digest = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
parser=argparse.ArgumentParser()
parser.add_argument('--qualification',type=Path,required=True)
parser.add_argument('--output',type=Path,required=True)
args=parser.parse_args()
q,output=args.qualification.resolve(),args.output.resolve()
assert not output.exists()
assert not subprocess.check_output(['git','diff','7261052ae4dec908f8c0ac38e0a2c5f4b831065b','--','engine'],cwd=ROOT).strip()
packet=Path(__file__).resolve().parents[1]
frozen=read(packet/'correction/RETENTION.json')
assemblies={x['path']:x['sha256'] for x in frozen['assemblies']['members']}
members={}
def queue_tree(folder,prefix):
    for p in sorted(folder.rglob('*')):
        if p.is_file():members[prefix+'/'+p.relative_to(folder).as_posix()]=p
def check_assemblies(rows):
    if isinstance(rows,list):rows={x['name']:x for x in rows}
    assert set(rows)=={'Core','Persistence','LabModel'}
    for name,row in rows.items():assert row['sha256']==assemblies['Decennium.Foundation.'+name+'.dll']
def check_binding(folder):
    before=read(folder/'execution-sources.before.json')
    after=read(folder/'execution-sources.after.json')
    assert after['status']=='PASS' and before['files']==after['files'] and before['pid']==after['pid']
    for row in before['files']:
        path=ROOT/row['path']
        assert path.stat().st_size==row['bytes'] and digest(path)==row['sha256'],row['path']
        members['executed-sources/'+row['path']]=path

reference=read(q/'connected-reference/manifest.json')
assert reference['status']=='PASS_REFERENCE' and reference['revision']==327 and len(reference['marks'])==23
assert read(q/'connected-reference/source-checkpoint-parity.json')['status']=='PASS'
source_marks=read(q/'connected-export/source-marks.json')
assert {x['name']:x['sha256'] for x in source_marks['marks']}=={x['name']:x['sha256'] for x in reference['marks']}
check_assemblies(reference['assemblies']);check_binding(q/'connected-reference')
for mark in reference['marks']:
    assert digest(q/'connected-reference'/mark['name'])==mark['sha256']
    assert digest(q/'connected-reference'/(mark['name']+'.after-probes.ddsave'))==mark['sha256']
    for view in mark['views'].values():assert digest(q/'connected-reference'/view['name'])==view['sha256']
    for probe in mark['probes']:assert digest(q/'connected-reference'/probe['request']['evidenceRead'])==probe['sha256']
folders=['connected-export','connected-reference','hostile-bytes','trust','backup','spatial-controls-v2','bishop-baseline','exclusions/genesis','exclusions/continued']
for name in ('trust','backup','spatial-controls-v2','bishop-baseline','exclusions/genesis','exclusions/continued'):
    report=read(q/name/'results.json');assert report['status']=='PASS',name
    check_assemblies(report['assemblies']);check_binding(q/name)
assert len(read(q/'trust/results.json')['cases'])==6
spatial=read(q/'spatial-controls-v2/results.json')
assert len(spatial['rays'])==5 and len(spatial['actualCommandDenials'])==2
baseline=read(q/'bishop-baseline/results.json')
assert baseline['commands']==457 and baseline['saves']==21 and baseline['finalWire']==113
for name in folders:queue_tree(q/name,name)
# Superseded support attempts are retained explicitly as failures/incomplete runs.
for name in ('spatial-controls-v1','compatibility-suite'):
    queue_tree(q/name,'superseded-support/'+name)
output.mkdir()
archive=output/'qualification-checkpoint.zip';rows=[]
with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for name,path in sorted(members.items()):
        data=path.read_bytes();z.writestr(name,data);rows.append(dict(path=name,bytes=len(data),sha256=hashlib.sha256(data).hexdigest()))
with zipfile.ZipFile(archive) as z:
    assert sorted(z.namelist())==sorted(x['path'] for x in rows)
    for row in rows:
        data=z.read(row['path']);assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
report=dict(status='PASS_PARTIAL_QUALIFICATION_RETENTION',sourceCommit='7261052ae4dec908f8c0ac38e0a2c5f4b831065b',
            scope='Completed corrected reference, inherited baseline, distrust/backup, mechanical channels, actual blocked/occupied denials and semantic exclusions. Full regression, all five paths and compatibility remain pending.',
            archive=dict(path=archive.name,bytes=archive.stat().st_size,sha256=digest(archive),members=rows))
(output/'RETENTION.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'status':report['status'],'members':len(rows),'bytes':archive.stat().st_size,'sha256':digest(archive)}))
