from pathlib import Path
import json,hashlib,sys
b=Path(sys.argv[1]); rows=[];h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for name,count in [('forgeries-01',11),('forgeries-02',2),('forgeries-05',1)]:
    run=b/name
    report=json.loads((run/('result.json' if name=='forgeries-05' else 'progress.json')).read_text(encoding='utf-8-sig'))
    cases=report['cases'] if isinstance(report,dict) else report
    assert len(cases)==count,(name,len(cases))
    execution=json.loads((run/'execution.json').read_text(encoding='utf-8-sig'))
    assert execution['status']==('PASS' if name=='forgeries-05' else 'FAIL')
    assert len(execution['assemblyHashes'])==4
    for x in cases:
        file=run/(x['name']+'.forged.ddsave'); data=file.read_bytes()
        assert h(Path(x['source']))==x['sourceSha256'] and h(file)==x['forgedSha256']
        assert hashlib.sha256(data[:-32]).digest()==data[-32:]
        assert x['restoreRejected'] and x['liveUnchanged'] and x['recomputedChecksum']
        rows.append(dict(x,executionRun=name,executionSha256=h(run/'execution.json')))
assert len(rows)==len({x['name'] for x in rows})==14
short=next(x for x in rows if x['name']=='coherent-shortened-labor-versus-real-clock-receipt')
assert not short['decodeRejected'],'The coherent forgery must exercise policy replay, not just malformed decoding'
out={'status':'PASS_RECONCILED_14_EXECUTED_CASES','cases':rows,'scope':'11 completed cases precede root-locator harness failure;2 completed identity cases precede age-constructor harness failure; final1 age case passed corrected exact-section byte mutation. All failed attempts retained. Every case uses the same frozen10 runtime, recomputed checksums and rejected strict restore preserving live state. No claim that interrupted driver processes passed.'}
(b/'forgeries-reconciled.json').write_text(json.dumps(out,indent=2)+'\n');print('PASS14 verified forged-save rejections, including a structurally valid causal-history forgery')
