"""Preservation check for eight named full-feat completion sources, not approval."""
from pathlib import Path
import json, hashlib
ROOT=Path(__file__).resolve().parents[1]
GAME=ROOT.parents[1]
AUDIT=GAME/'docs/audit/2026-10-08/full-game'

def digest(value):return hashlib.sha256(json.dumps(value,sort_keys=True,ensure_ascii=False).encode()).hexdigest()

def main():
    capture=json.loads((AUDIT/'BUFFER_FEAT_COMPLETION_SOURCES.json').read_text(encoding='utf-8'))
    path=ROOT/capture['sourcePath']
    assert hashlib.sha256(path.read_bytes()).hexdigest()==capture['sourceFileSha256']
    assert (GAME/capture['sourcePath']).read_bytes()==path.read_bytes(),'Original copies differ'
    raw=json.JSONDecoder().raw_decode(path.read_text(encoding='utf-8').split('export const feats = ',1)[1])[0]
    feats={f['id']:f for f in raw};seen=set()
    for record in capture['records']:
        assert record['id'] not in seen;seen.add(record['id'])
        assert feats[record['id']]==record['sourceObject']
        assert digest(feats[record['id']])==record['sourceObjectSha256']
    assert len(seen)==8 and len(feats)==335
    assert 'Lifeleech' in feats['soul_cage']['prerequisite']
    assert 'Soul Cage' in feats['lifeleech']['effect']
    report={'status':'PASS','fullFeatSourceObjects':8,'preservedFeatRegistry':335,
            'sourceFileSha256':capture['sourceFileSha256'],'scope':'Exact original objects including legacy text and cross-feat dependency; no operational approval'}
    (ROOT/'docs/mechanics/BUFFER_FEAT_SOURCE_VALIDATION.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report))

if __name__=='__main__':main()
