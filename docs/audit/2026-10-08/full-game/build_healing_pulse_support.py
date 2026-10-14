"""Snapshot additional explicit maintenance and Totem source contracts."""
from pathlib import Path
import json,hashlib
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]/'DescentReviewChanges/ReviewBible'
rows=[]
for owner,key,selector in [('cleric','engine',5),('cleric','cards','cleric.arch.sacrament'),
                           ('shaman','engine',0),('shaman','workedExample',4),('oracle','engine',17)]:
    path=ROOT/f'data/public/class_playtests/{owner}.json'
    data=json.loads(path.read_text(encoding='utf-8'))
    value=next(c for c in data[key] if c['id']==selector) if key=='cards' else data[key][selector]
    rows.append({'sourcePath':path.relative_to(ROOT).as_posix(),'key':key,'selector':selector,'value':value,
                 'sha256':hashlib.sha256(json.dumps(value,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()})
path=ROOT/'docs/mechanics/CLASS_PLAYTEST_RULES.md'
data=path.read_text(encoding='utf-8')
rows.append({'sourcePath':path.relative_to(ROOT).as_posix(),'key':'exact-paragraph',
             'selector':'One concentration slot','value':next(p for p in data.split('\n\n') if p.startswith('One concentration slot')),
             'fullFileSha256':hashlib.sha256(path.read_bytes()).hexdigest()})
(HERE/'HEALING_PULSE_SUPPORTING_SOURCES.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Captured6 supporting passages, including frozen shared maintenance paragraph.')
