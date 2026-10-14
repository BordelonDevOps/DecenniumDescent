"""Prepare future companion/device/form/temporary-HP source evidence."""
from pathlib import Path
import json,re,hashlib
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]/'DescentReviewChanges/ReviewBible'
pattern=re.compile(r'companion|summon|undead.{0,25}control|device|deploy|drone|totem|temporary HP|temp(?:orary)?\s*HP|Buffer Reserve|Form Surge|Shapeshift|Wild.?Shape',re.I)
rows=[]
for path in sorted((ROOT/'data/public/class_playtests').glob('*.json')):
    data=json.loads(path.read_text(encoding='utf-8'))
    for i,value in enumerate(data.get('engine',[])):
        if pattern.search(value):
            rows.append({'kind':'class-engine','owner':path.stem,'path':path.relative_to(ROOT).as_posix(),'engineIndex':i,'text':value,'textSha256':hashlib.sha256(value.encode()).hexdigest()})
    for card in data.get('cards',[]):
        text=' '.join(str(card.get(k,'')) for k in ('name','activation','cost','rangeAndTarget','duration','frequency','effect'))
        if pattern.search(text):
            rows.append({'kind':'class-card','owner':path.stem,'path':path.relative_to(ROOT).as_posix(),'card':card,
                         'sourceObjectSha256':hashlib.sha256(json.dumps(card,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()})
report={'status':'UNREVIEWED_SOURCE_CANDIDATES','scope':'Broad future lexical inventory for companion/device/form/temporary-HP lifecycle. Includes incidental mentions and previously reviewed roles. Not a completeness claim or semantic classification.','classRecords':rows}
(HERE/'COMPANION_LIFECYCLE_SOURCE_CANDIDATES.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
counts={}
for r in rows:counts[r['owner']]=counts.get(r['owner'],0)+1
print('Prepared',len(rows),'future lifecycle candidates:',counts)
