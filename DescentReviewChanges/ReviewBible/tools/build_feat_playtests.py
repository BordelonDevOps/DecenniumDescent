"""Build a source-preserving feat playtest overlay; legacy flags are not approval."""
from pathlib import Path
import hashlib
import json

ROOT=Path(__file__).resolve().parents[1];GAME=ROOT.parents[1]

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def digest(value):return hashlib.sha256(json.dumps(value,sort_keys=True,ensure_ascii=False).encode()).hexdigest()

def main():
    path=ROOT/'src/data/feats.js'
    source=json.JSONDecoder().raw_decode(path.read_text(encoding='utf-8').split('export const feats = ',1)[1])[0]
    assert len(source)==335 and len({f['id'] for f in source})==335
    assert path.read_bytes()==(GAME/'src/data/feats.js').read_bytes()
    batches=sorted((ROOT/'data/playtest/feat_drafts').glob('batch_*.json'))
    active={}
    for filename in batches:
        batch=json.loads(filename.read_text(encoding='utf-8'))
        assert batch['sourceFileSha256']==sha(path)
        review=GAME/batch['reviewClosure']
        assert review.exists() and sha(review)==batch['reviewClosureSha256']
        assert 'REVIEWED / reference-VALIDATED' in review.read_text(encoding='utf-8')
        for feat in batch['feats']:
            assert feat['id'] not in active
            original=next(f for f in source if f['id']==feat['id'])
            assert original==feat['sourceObject'] and digest(original)==feat['sourceObjectSha256']
            assert feat['operationalRules'].strip() and feat['repeatability']=='nonrepeatable'
            active[feat['id']]={**feat,'reviewClosure':batch['reviewClosure'],
                                'sharedGuide':batch['guide'],'operationalStatus':'operational-playtest'}
    rows=[]
    for original in source:
        id=original['id']
        rows.append(active.get(id,{'id':id,'name':original['name'],'sourceObject':original,
           'sourceObjectSha256':digest(original),'operationalStatus':'full-feat-review-pending',
           'note':'Original/legacy text retained. Historical draft/deprecated/needsReview/status flags are not current full-clause review evidence.'}))
    out=ROOT/'data/public/feat_playtests';out.mkdir(parents=True,exist_ok=True)
    (out/'catalog.json').write_text(json.dumps({'schemaVersion':'1.0','status':'provisional playtest overlay; original335 records unchanged','feats':rows},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    manifest={'sourceFeats':335,'operationalFeats':len(active),'unfinishedFeats':335-len(active),
              'sourceFileSha256':sha(path),'operationalIds':sorted(active),
              'wholeGameComplete':False,'humanBalanceValidated':False}
    (out/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    lines=['# Feat playtest index','',f"**{len(active)} full feats reviewed; {335-len(active)} still require full-clause review.** All335 original IDs/objects and legacy alternatives remain preserved. This overlay does not infer approval from the original registry flags.",'',
      '[Complete eight-feat rules](BUFFER_FEAT_PLAYTEST.md) · [Validation](BUFFER_FEAT_PLAYTEST_VALIDATION.json) · [Source integrity](BUFFER_FEAT_SOURCE_VALIDATION.json) · [Catalog](../../data/public/feat_playtests/catalog.json)','',
      '| Feat | Full-clause playtest status |','|---|---|']
    for f in sorted(rows,key=lambda f:f['name'].casefold()):
        label='Reviewed / reference-validated' if f['id'] in active else 'Full review pending'
        lines.append('| '+f['name'].replace('|','/')+' | '+label+' |')
    (ROOT/'docs/mechanics/FEAT_PLAYTEST_INDEX.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(json.dumps(manifest))

if __name__=='__main__':main()
