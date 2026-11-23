from pathlib import Path
import hashlib,json,sys
run=Path(sys.argv[1]); report=json.loads((run/'result.json').read_text(encoding='utf-8-sig')); assert report['status']=='PASS'
rows=[]
for x in report['checks']:
    n=x['name']
    if n.endswith('-retry-diagnostic'):continue
    expected = ('UnsupportedOperation',0) if n.endswith(('-wrong-worker','-unknown-job')) else ('StaleRevision',2) if n.endswith('-stale') else ('ManufacturingChoicePending',0) if n.startswith('pending-choice-') else ('InventoryNotAuthorized',0) if n.endswith('-lost-inventory-authority') else ('AlreadyCommitted',5) if n.endswith('-persisted-exact-retry') else ('CommandIdConflict',3) if n.endswith('-conflicting-id') else ('NotAuthorized',1) if n.endswith('-revoked-retry') else None
    assert expected is not None,n
    assert (x['query']['Code'],x['result']['Response'])==expected,(n,x)
    assert x['unchanged'],n
    rows.append({'name':n,'expectedQuery':expected[0],'expectedResponse':expected[1],'verified':True})
assert len(rows)==25,len(rows)
parent=run.parent/'principal-work-01/paused-fill.ddsave'
assert parent.read_bytes()==(run/'primary.ddsave').read_bytes()==(run/'recovered.ddsave').read_bytes()
out={'status':'PASS','checks':rows,'backupPrimaryRestoredBytesEqual':True,'backupPrimarySha256':hashlib.sha256((run/'primary.ddsave').read_bytes()).hexdigest(),'boundExecutionSha256':hashlib.sha256((run/'result.json').read_bytes()).hexdigest(),'scope':'Post-execution assertion of exact retained query/submit codes and recovered primary bytes; no rerun or pass transfer'}
(run/'verified-exact-codes.json').write_text(json.dumps(out,indent=2)+'\n');print('PASS25 exact query/submit outcomes and recovered primary bytes')
