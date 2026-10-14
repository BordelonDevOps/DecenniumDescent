"""Source-integrity check for100 creature-lifecycle candidates; no rule approval."""
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[1]
AUDIT=ROOT.parents[1]/'docs/audit/2026-10-08/full-game'
def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
def main():
    data=json.loads((AUDIT/'CREATURE_LIFECYCLE_SOURCE_CANDIDATES.json').read_text(encoding='utf-8'))
    loaded={};issues=[];ids=[]
    for row in data['classRecords']:
        if row['path'] not in loaded:
            loaded[row['path']]=json.loads((ROOT/row['path']).read_text(encoding='utf-8'))
        source=loaded[row['path']]
        if row['kind']=='class-card':
            ident=row['card']['id'];live=next((c for c in source['cards'] if c['id']==ident),None)
            valid=live==row['card'] and digest(live)==row['sourceObjectSha256']
        else:
            ident=f"{row['owner']}.engine[{row['engineIndex']}]"
            live=source['engine'][row['engineIndex']]
            valid=live==row['text'] and hashlib.sha256(live.encode()).hexdigest()==row['textSha256']
        ids.append(ident)
        if not valid:issues.append(ident)
    supports=list(data['supportingSources'])
    extra=AUDIT/'CREATURE_LIFECYCLE_SUPPORTING_SOURCES.json'
    if extra.exists():supports+=json.loads(extra.read_text(encoding='utf-8'))['supportingSources']
    for row in supports:
        path=ROOT/row['sourcePath']
        paragraphs=path.read_text(encoding='utf-8').split('\n\n')
        live=next((v for v in paragraphs if v.startswith(row['paragraphPrefix'])),None)
        if live!=row['text'] or hashlib.sha256(path.read_bytes()).hexdigest()!=row['fullFileSha256']:
            issues.append(row['sourcePath']+' / '+row['paragraphPrefix'])
    assert len(set(ids))==len(ids)==100 and len(data['supportingSources'])==3
    assert len({(r['sourcePath'],r['paragraphPrefix']) for r in supports})==len(supports)
    report={'result':'FAIL' if issues else 'PASS','exactClassRecords':100,
            'originalInventoryCandidates':83,'semanticSupplements':17,'frozenSharedParagraphs':len(supports),
            'scope':'Exact source equality/hash only; not classification or semantic approval.','issues':issues}
    (ROOT/'docs/mechanics/CREATURE_LIFECYCLE_SOURCE_VALIDATION.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    if issues:raise AssertionError(issues)
    print(f'PASS100 creature-lifecycle source records +{len(supports)} frozen shared paragraphs; integrity only.')
if __name__=='__main__':main()
