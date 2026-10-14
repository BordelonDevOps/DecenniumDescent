"""Read-only provenance check for prepared74+3 device/Totem conference."""
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[1]
AUDIT=ROOT.parents[1]/'docs/audit/2026-10-08/full-game'
def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
def main():
    data=json.loads((AUDIT/'DEVICE_LIFECYCLE_SOURCE_CANDIDATES.json').read_text(encoding='utf-8'))
    issues=[];loaded={};ids=[]
    for r in data['classRecords']:
        if r['path'] not in loaded:loaded[r['path']]=json.loads((ROOT/r['path']).read_text(encoding='utf-8'))
        live=loaded[r['path']]
        if r['kind']=='class-card':
            ident=r['card']['id'];value=next((c for c in live['cards'] if c['id']==ident),None)
            valid=value==r['card'] and digest(value)==r['sourceObjectSha256']
        else:
            ident=f"{r['owner']}.engine[{r['engineIndex']}]";value=live['engine'][r['engineIndex']]
            valid=value==r['text'] and hashlib.sha256(value.encode()).hexdigest()==r['textSha256']
        ids.append(ident)
        if not valid:issues.append(ident)
    for r in data['supportingSources']:
        path=ROOT/r['sourcePath']
        paragraph=next((p for p in path.read_text(encoding='utf-8').split('\n\n') if p.startswith(r['paragraphPrefix'])),None)
        if paragraph!=r['text'] or hashlib.sha256(path.read_bytes()).hexdigest()!=r['fullFileSha256']:
            issues.append(r['sourcePath']+' / '+r['paragraphPrefix'])
    assert len(ids)==len(set(ids))==74 and len(data['supportingSources'])==3
    assert 'tinker.hero.artificer.magnetic-wall' in ids
    report={'status':'FAIL' if issues else 'PASS','exactClassPassages':len(ids),'exactSharedParagraphs':3,
            'scope':'Source equality and provenance only; semantic disposition is recorded separately.','issues':issues}
    (ROOT/'docs/mechanics/DEVICE_LIFECYCLE_SOURCE_VALIDATION.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    if issues:raise AssertionError(issues)
    print('PASS 74 device/Totem sources +3 frozen shared paragraphs; integrity check only.')
if __name__=='__main__':main()
