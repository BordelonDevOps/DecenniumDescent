"""Only publish a final regression segment after all real workers and cases finish."""
from pathlib import Path
import hashlib, json, subprocess, sys, zipfile

repo=Path('.').resolve()
packet=repo/'docs/unity/evidence/2026-11-23-tac01-ordinary-magic'
root=repo/'engine/artifacts/ordinary-magic-qualification/candidate-02'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda b:hashlib.sha256(b).hexdigest()
subprocess.run([sys.executable,'-B',str(packet/'support/Reconcile-Regression.py'),str(root),'--require-complete'],check=True)
reconciliation=read(root/'REGRESSION_RECONCILIATION.json')
assert reconciliation['status']=='PASS' and reconciliation['passed']==1592 and reconciliation['failed']==0
exits=read(root/'FINAL_PROCESS_EXITS.json')
assert len(exits['workers'])==4 and {x['worker'] for x in exits['workers']}=={0,1,2,3}
assert all(x['observedExitCode']==0 for x in exits['workers'])
freeze=read(root/'FREEZE.json');build=read(root/'runtime/results.json')
assert build['coreCompilation']=='PASS' and len(build['sourceHashes'])==481
for entry in build['sourceHashes']:
    assert sha((repo/'engine'/entry['path']).read_bytes())==entry['sha256'],entry['path']
for entry in freeze['assemblies']:
    assert sha((root/'runtime'/entry['name']).read_bytes())==entry['sha256'],entry['name']
assert sha((root/'runtime/source-inputs.zip').read_bytes())==freeze['sourceArchiveSha256']
for mode in ['ConsoleUninterrupted','ConsoleRestored','TypedUninterrupted','TypedRestored','ReceiptReplay']:
    path=root/'five-paths-01'/mode/'result.json'
    assert read(path)['status']=='PASS'
    assert read(path)['consoleSha256']==sha((repo/'engine/tools/Open-ConnectedExpedition.ps1').read_bytes())
files=[]
for directory in [root/'runtime']+[root/f'worker-{i}' for i in range(4)]:
    files.extend(p for p in directory.rglob('*') if p.is_file())
files.extend(root/name for name in ['REGRESSION_RECONCILIATION.json','FINAL_PROCESS_EXITS.json','FREEZE.json','CURRENT_SOURCE_RECONCILIATION.json'])
archive=packet/'FINAL_REGRESSION_04.zip'
assert not archive.exists(),'Never overwrite retained evidence'
members=[]
with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for path in sorted(set(files)):
        data=path.read_bytes();name=path.relative_to(repo).as_posix()
        z.writestr(name,data)
        members.append({'member':name,'bytes':len(data),'sha256':sha(data)})
with zipfile.ZipFile(archive) as z:
    assert len(z.namelist())==len(members)
    for row in members:
        data=z.read(row['member']);assert len(data)==row['bytes'] and sha(data)==row['sha256']
index={'status':'PASS_FINAL_FROZEN_RUNTIME_REGRESSION_RETAINED','archive':archive.name,
       'bytes':archive.stat().st_size,'sha256':sha(archive.read_bytes()),'memberCount':len(members),'members':members,
       'registered':1592,'passed':1592,'failed':0,'preservedPredecessors':1587,'newCases':reconciliation['newCases'],
       'sourceInputs':481,'assemblies':freeze['assemblies'],'workers':reconciliation['workers'],
       'processExits':exits,'moduleAcceptance':'PENDING_ACTUAL_GPT_FINAL_REVIEW_AND_CODEX_CONCURRENCE',
       'scope':'Actual complete candidate02 suite and raw per-case evidence. Every worker terminal status/observed process exit, named case, source and assembly binding is checked before collection. No superseded candidate01 execution is substituted; prior accepted qualification remains preserved.'}
(packet/'FINAL_REGRESSION_04_INDEX.json').write_text(json.dumps(index,indent=2)+'\n',encoding='utf-8',newline='\n')
(packet/'FINAL_REGRESSION_RECONCILIATION.json').write_text(json.dumps(reconciliation,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps({k:index[k] for k in ['status','archive','bytes','sha256','memberCount','passed','failed']},indent=2))
