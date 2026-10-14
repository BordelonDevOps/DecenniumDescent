from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[1]
AUDIT=ROOT.parents[1]/'docs/audit/2026-10-08/full-game'
def main():
    sources=json.loads((AUDIT/'HEALING_PULSE_SUPPORTING_SOURCES.json').read_text(encoding='utf-8'))
    issues=[]
    for r in sources:
        path=ROOT/r['sourcePath']
        if r['key']=='exact-paragraph':
            actual=next((p for p in path.read_text(encoding='utf-8').split('\n\n') if p.startswith(r['selector'])),None)
            valid=actual==r['value'] and hashlib.sha256(path.read_bytes()).hexdigest()==r['fullFileSha256']
        else:
            data=json.loads(path.read_text(encoding='utf-8'))
            actual=next((c for c in data[r['key']] if c['id']==r['selector']),None) if r['key']=='cards' else data[r['key']][r['selector']]
            sha=hashlib.sha256(json.dumps(actual,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
            valid=actual==r['value'] and sha==r['sha256']
        if not valid:issues.append(r['sourcePath']+' / '+str(r['selector']))
    assert len(sources)==6
    report={'status':'FAIL' if issues else 'PASS','exactSupportingRecords':len(sources),'scope':'Exact supplemental source equality and hashes, including frozen full shared class guide hash.','issues':issues}
    (ROOT/'docs/mechanics/HEALING_PULSE_SUPPORT_VALIDATION.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    if issues:raise AssertionError(issues)
    print('PASS6 exact supporting sources; frozen shared class guide preserved.')
if __name__=='__main__':main()
