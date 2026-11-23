"""Bind the full corrected-runtime suite to its exact retained predecessor inventory."""
from pathlib import Path
import hashlib, json, sys

root = Path(sys.argv[1])
prior = Path('docs/unity/evidence/2026-11-17-chr05-consecration/REGRESSION_RECONCILIATION.json')
read = lambda p: json.loads(p.read_text(encoding='utf-8-sig'))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
old = read(prior)
old_names = {c['name'] for c in old['cases']}
assert len(old_names) == 1587 and old['reconciledPassed'] == 1587
freeze = read(root/'FREEZE.json')
expected_hashes = {a['name']:a['sha256'] for a in freeze['assemblies']}
assigned, rows, workers = [], [], []
for worker in range(4):
    folder = root/f'worker-{worker}'
    names = read(folder/'assigned.json')
    assigned += names
    report = read(folder/'results.json')
    assert report['totalDiscovered'] == 1592
    assert report['assigned'] == len(names)
    assert {a['name']:a['sha256'] for a in report['assemblyHashes']} == expected_hashes
    assert [r['Name'] for r in report['cases']] == names[:report['completed']]
    for case in report['cases']:
        source = folder/'cases'/case['Name']/'result.json'
        assert read(source) == case
        rows.append({'name':case['Name'], 'passed':case['Passed'], 'error':case['Error'],
                     'elapsedMilliseconds':case['elapsedMilliseconds'],
                     'evidence':source.relative_to(root).as_posix(), 'sha256':sha(source),
                     'inventory':'preserved-predecessor' if case['Name'] in old_names else 'new-module'})
    workers.append({'worker':worker, 'status':report['status'], 'assigned':len(names),
                    'completed':report['completed'], 'passed':report['passed'], 'failed':report['failed'],
                    'reportSha256':sha(folder/'results.json'), 'assignedSha256':sha(folder/'assigned.json')})
assert len(assigned) == len(set(assigned)) == 1592
missing_predecessors = sorted(old_names-set(assigned))
new = sorted(set(assigned)-old_names)
assert not missing_predecessors and len(new) == 5
names_done = {r['name'] for r in rows}
assert len(names_done) == len(rows)
complete = all(w['status'] == 'PASS' for w in workers) and len(rows) == 1592
failed = [r for r in rows if not r['passed']]
status = 'PASS' if complete and not failed else 'FAIL' if failed or any(w['status']=='FAIL' for w in workers) else 'RUNNING'
result = {'status':status, 'runtime':'candidate-02', 'registered':1592, 'completed':len(rows),
          'passed':sum(r['passed'] for r in rows), 'failed':len(failed), 'predecessorInventory':1587,
          'predecessorInventorySha256':sha(prior), 'missingPredecessors':missing_predecessors,
          'newCases':new, 'unfinished':sorted(set(assigned)-names_done), 'workers':workers,
          'assemblies':freeze['assemblies'], 'cases':sorted(rows,key=lambda r:r['name']),
          'scope':'New-runtime execution of the preserved predecessor case inventory plus five module cases. Does not reopen or replace prior accepted qualification. Superseded candidate01 execution retains its distinct disposition and is not substituted for candidate02.'}
(root/'REGRESSION_RECONCILIATION.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:result[k] for k in ['status','registered','completed','passed','failed','missingPredecessors','newCases']},indent=2))
if '--require-complete' in sys.argv:
    assert status == 'PASS', 'Final frozen runtime qualification is not complete'
