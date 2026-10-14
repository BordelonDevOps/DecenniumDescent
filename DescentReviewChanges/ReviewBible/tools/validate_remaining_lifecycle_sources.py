"""Exact80 next-conference source records and5 shared paragraphs, integrity only."""
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[1]
AUDIT=ROOT.parents[1]/'docs/audit/2026-10-08/full-game'

def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()

def main():
    data=json.loads((AUDIT/'REMAINING_LIFECYCLE_CONFERENCE_SOURCES.json').read_text(encoding='utf-8'))
    ids=[];issues=[];loaded={}
    for r in data['classRecords']:
        if r['path'] not in loaded:loaded[r['path']]=json.loads((ROOT/r['path']).read_text(encoding='utf-8'))
        source=loaded[r['path']]
        if r['kind']=='class-card':
            ident=r['card']['id'];live=next((c for c in source['cards'] if c['id']==ident),None)
            good=live==r['card'] and digest(live)==r['sourceObjectSha256']
        else:
            ident=f"{r['owner']}.engine[{r['engineIndex']}]";live=source['engine'][r['engineIndex']]
            good=live==r['text'] and hashlib.sha256(live.encode()).hexdigest()==r['textSha256']
        ids.append(ident)
        if not good:issues.append(ident)
    supports=json.loads((AUDIT/'CREATURE_LIFECYCLE_SOURCE_CANDIDATES.json').read_text(encoding='utf-8'))['supportingSources']
    supports+=json.loads((AUDIT/'CREATURE_LIFECYCLE_SUPPORTING_SOURCES.json').read_text(encoding='utf-8'))['supportingSources']
    for r in supports:
        file=ROOT/r['sourcePath'];paragraphs=file.read_text(encoding='utf-8').split('\n\n')
        live=next((p for p in paragraphs if p.startswith(r['paragraphPrefix'])),None)
        if live!=r['text'] or hashlib.sha256(file.read_bytes()).hexdigest()!=r['fullFileSha256']:issues.append(r['paragraphPrefix'])
    assert len(ids)==len(set(ids))==80 and len(supports)==5
    report={'result':'FAIL' if issues else 'PASS','status':'UNREVIEWED_SOURCE_INTEGRITY_ONLY',
            'exactClassRecords':80,'originalCandidates':74,'semanticSupplements':6,'frozenSharedParagraphs':5,
            'scope':'Exact preserved source equality/hash; no interpretation/implementation approval.','issues':issues}
    (ROOT/'docs/mechanics/REMAINING_LIFECYCLE_SOURCE_VALIDATION.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    if issues:raise AssertionError(issues)
    print('PASS80 exact remaining-lifecycle source records+5 frozen paragraphs; integrity only.')

if __name__=='__main__':main()
