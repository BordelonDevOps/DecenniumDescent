from pathlib import Path
import hashlib,json,sys,time
repo=Path(__file__).resolve().parents[5];base=repo/sys.argv[1];build=repo/sys.argv[2]
def read(p):
    for n in range(4):
        try:return json.loads(p.read_text(encoding='utf-8-sig'))
        except json.JSONDecodeError:
            if n==3:raise
            time.sleep(.1)
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
prior=repo/'docs/unity/evidence/2026-11-23-tac01-ordinary-magic/FINAL_REGRESSION_RECONCILIATION.json'
old=read(prior);old_names={c['name'] for c in old['cases']};assert old['status']=='PASS' and len(old_names)==1592
frozen=read(build/'results.json');assert frozen['coreCompilation']=='PASS' and len(frozen['sourceHashes'])==486
assembly_hashes={p.name:h(p) for p in build.glob('*.dll')};assert len(assembly_hashes)==4
assigned=[];cases=[];workers=[]
for i in range(4):
    folder=base/('worker'+str(i));names=read(folder/'assigned.json');r=read(folder/'results.json');assigned+=names
    assert r['totalDiscovered']==1601 and r['assigned']==len(names)
    assert r['sourceHashes']==frozen['sourceHashes']
    assert {a['name']:a['sha256'] for a in r['assemblyHashes']}==assembly_hashes
    assert [c['Name'] for c in r['cases']]==names[:r['completed']]
    for c in r['cases']:
        p=folder/'cases'/c['Name']/'result.json';assert read(p)==c
        cases.append({'name':c['Name'],'passed':c['Passed'],'error':c['Error'],'elapsedMilliseconds':c['elapsedMilliseconds'],
            'evidence':p.relative_to(repo).as_posix(),'sha256':h(p),'inventory':'preserved-predecessor' if c['Name'] in old_names else 'new-module'})
    workers.append({'worker':i,'status':r['status'],'assigned':len(names),'completed':r['completed'],'passed':r['passed'],'failed':r['failed'],'reportSha256':h(folder/'results.json'),'assignedSha256':h(folder/'assigned.json')})
assert len(assigned)==len(set(assigned))==1601
assert not old_names-set(assigned)
new=sorted(set(assigned)-old_names);assert len(new)==9 and all(n.startswith('mgt02_work_control_') for n in new)
assert len({c['name'] for c in cases})==len(cases)
failed=[c for c in cases if not c['passed']]
complete=all(w['status']=='PASS' for w in workers) and len(cases)==1601
status='PASS' if complete and not failed else 'FAIL' if failed or any(w['status']=='FAIL' for w in workers) else 'RUNNING'
r={'status':status,'registered':1601,'completed':len(cases),'passed':sum(c['passed'] for c in cases),'failed':len(failed),'preservedPredecessorInventory':1592,'predecessorInventorySha256':h(prior),'missingPredecessors':[],'newCases':new,'workers':workers,'sourceBuild':build.relative_to(repo).as_posix(),'assemblyHashes':assembly_hashes,'cases':sorted(cases,key=lambda c:c['name']),'scope':'New frozen runtime execution of all1592 accepted predecessor test names plus9 meaningful MGT-02 cases. Prior module qualification/acceptance remains preserved; this is new-module regression only.'}
(base/'REGRESSION_RECONCILIATION.json').write_bytes((json.dumps(r,indent=2)+'\n').encode())
print(json.dumps({k:r[k] for k in ['status','registered','completed','passed','failed','missingPredecessors','newCases']},indent=2))
if '--require-complete' in sys.argv:assert status=='PASS','Final frozen regression remains incomplete'
