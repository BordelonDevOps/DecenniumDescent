"""Reconcile retained outputs only; this does not execute or accept the engine."""
from pathlib import Path
import hashlib
import json

ROOT=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
launch=read(ROOT/'regression-20261116T0115Z/launch.json')
campaigns=[('terminal',ROOT/'trace-terminal',ROOT/'paths-terminal')]
campaigns += [(n,ROOT/'additional-campaigns'/('trace-'+n),ROOT/'additional-campaigns'/('paths-'+n)) for n in ('before','after','whole','capped-debt')]
modes={'ConsoleUninterrupted','ConsoleRestored','TypedUninterrupted','TypedRestored','ReceiptReplay'}
canonical=views=0;rows=[]
assert read(ROOT/'additional-campaigns/results.json')['status']=='PASS'
for name,trace,paths in campaigns:
    manifest=read(trace/'manifest.json');result=read(paths/'results.json')
    assert result['status']=='PASS' and set(result['paths'])==modes
    assert result['traceSha256']==sha(trace/'inputs.jsonl')
    for assembly in result['assemblies']:
        assert assembly['sha256']==launch['assemblies']['Decennium.Foundation.'+assembly['name']+'.dll']
    for mode,details in result['paths'].items():
        assert details['commands']==manifest['revision']
        for mark in manifest['marks']:
            assert sha(trace/'reference'/mark['name'])==mark['sha256']==sha(paths/mode/mark['name'])==details['checkpoints'][mark['name']]
            canonical+=1
            for view in mark['views'].values():
                assert sha(trace/'reference'/view['name'])==view['sha256']==sha(paths/mode/view['name'])==details['checkpoints'][view['name']]
                views+=1
    assert sha(Path(manifest['finalSource']))==manifest['finalSha256']
    rows.append({'name':name,'commands':manifest['revision'],'checkpoints':len(manifest['marks']),
                 'paths':sorted(modes),'finalSha256':manifest['finalSha256'],'resultSha256':sha(paths/'results.json')})
report={'status':'PASS','scope':'Retained output/hash reconciliation, not a new engine execution or final acceptance',
        'implementationCommit':launch['sourceCommit'],'campaigns':rows,'canonicalComparisons':canonical,'filteredViewComparisons':views}
(ROOT/'campaign-parity.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(f'PASS: five campaigns; {canonical} canonical and {views} filtered-view comparisons on the frozen assemblies.')
