"""Preserve unreviewed complete feat objects by original category; no semantic closure."""
from pathlib import Path
from collections import Counter
import json
import hashlib
AUDIT=Path(__file__).resolve().parent;GAME=AUDIT.parents[3];ROOT=GAME/'DescentReviewChanges/ReviewBible'
path=ROOT/'src/data/feats.js';raw=json.JSONDecoder().raw_decode(path.read_text(encoding='utf-8').split('export const feats = ',1)[1])[0]
active=set(json.loads((ROOT/'data/public/feat_playtests/manifest.json').read_text(encoding='utf-8'))['operationalIds'])
remaining=[f for f in raw if f['id'] not in active]
assert len(remaining)==327 and len(active)==8
counts=Counter(f.get('type','untyped') for f in remaining)
data={'status':'PREPARED / individual full-clause conference pending; grouping is source metadata only',
      'sourcePath':'src/data/feats.js','sourceFileSha256':hashlib.sha256(path.read_bytes()).hexdigest(),
      'alreadyReviewedIds':sorted(active),'remainingCount':len(remaining),'sourceCategoryCounts':dict(sorted(counts.items())),
      'records':[{'id':f['id'],'sourceObject':f,'sourceObjectSha256':hashlib.sha256(json.dumps(f,sort_keys=True,ensure_ascii=False).encode()).hexdigest()} for f in remaining]}
(AUDIT/'REMAINING_FEAT_CATALOG_PREPARATION.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'categories':data['sourceCategoryCounts'],'generalNames':[f['name'] for f in remaining if f.get('type')=='General']},ensure_ascii=False,indent=2))
