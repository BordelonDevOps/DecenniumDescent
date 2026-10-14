"""Preserve full Druid corpus plus explicit class tempHP/reserve candidates."""
from pathlib import Path
from collections import Counter
import json,re,hashlib
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]/'DescentReviewChanges/ReviewBible'
pattern=re.compile(r'temporar(?:y|ily)\s*(?:hit\s*points?|hp)|temp[\s-]*(?:hp|hit\s*points?)|buffer\s*reserve|form\s*surge',re.I)
def digest(value):return hashlib.sha256(json.dumps(value,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
rows=[];files=sorted((ROOT/'data/public/class_playtests').glob('*.json'))
for path in files:
    source=json.loads(path.read_text(encoding='utf-8'))
    if 'engine' not in source or 'cards' not in source:continue
    owner=path.stem;rel=path.relative_to(ROOT).as_posix()
    for i,text in enumerate(source['engine']):
        if owner!='druid' and not pattern.search(text):continue
        rows.append({'kind':'class-engine','owner':owner,'path':rel,'engineIndex':i,'text':text,
                     'textSha256':hashlib.sha256(text.encode()).hexdigest(),
                     'candidateOrigin':'Full Druid corpus' if owner=='druid' else 'Explicit temporaryHP/reserve lexical occurrence'})
    for c in source['cards']:
        if owner!='druid' and not pattern.search(json.dumps(c,ensure_ascii=False)):continue
        rows.append({'kind':'class-card','owner':owner,'path':rel,'card':c,'sourceObjectSha256':digest(c),
                     'candidateOrigin':'Full Druid corpus' if owner=='druid' else 'Explicit temporaryHP/reserve lexical occurrence'})
assert sum(r['owner']=='druid' for r in rows)==66
data={'status':'UNREVIEWED_SOURCE_CANDIDATES',
      'scope':'Full7-engine/59-card Druid class corpus plus explicit temporaryHP/reserve passages across current class files. Includes previously reviewed components and incidental exclusions. Core rules, feats, spells and semantic omissions still require separate supplements; no whole-system completeness claim.',
      'counts':dict(Counter(r['owner'] for r in rows)),'classRecords':rows}
(HERE/'FORM_TEMP_HP_SOURCE_CANDIDATES.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(f'Preserved{len(rows)} candidate passages, including all66 Druid passages; no classification/closure.')
