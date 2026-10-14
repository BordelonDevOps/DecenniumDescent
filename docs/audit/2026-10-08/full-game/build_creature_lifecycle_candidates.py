"""Preserve the next candidate slice and semantic supplements; no rule closure."""
from pathlib import Path
import json,re,hashlib
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]/'DescentReviewChanges/ReviewBible'
original=json.loads((HERE/'COMPANION_LIFECYCLE_SOURCE_CANDIDATES.json').read_text(encoding='utf-8'))
owners={'druid','mage','mirrorsage','ranger','wizard'}
rows=[r for r in original['classRecords'] if r['owner'] in owners]
def ident(r):
    return r['card']['id'] if r['kind']=='class-card' else f"{r['owner']}.engine[{r['engineIndex']}]"
known={ident(r) for r in rows}
pattern=re.compile(r'\b(?:familiar|minion|undead|Boneflayer|Dreadblade|Wraithbound|pet|corpse|swarm|companion)\b',re.I)
supplements=[]
for owner in sorted(owners):
    path=ROOT/f'data/public/class_playtests/{owner}.json'
    data=json.loads(path.read_text(encoding='utf-8'))
    for i,value in enumerate(data.get('engine',[])):
        name=f'{owner}.engine[{i}]'
        if name not in known and (pattern.search(value) or (owner=='druid' and i in (0,1))):
            row={'kind':'class-engine','owner':owner,'path':path.relative_to(ROOT).as_posix(),
                 'engineIndex':i,'text':value,'textSha256':hashlib.sha256(value.encode()).hexdigest(),
                 'candidateOrigin':'Semantic companion supplement to original broad lifecycle inventory'}
            supplements.append(row);known.add(name)
    for card in data.get('cards',[]):
        if card['id'] not in known and pattern.search(' '.join(str(card.get(k,'')) for k in ('name','activation','cost','rangeAndTarget','duration','frequency','effect'))):
            row={'kind':'class-card','owner':owner,'path':path.relative_to(ROOT).as_posix(),'card':card,
                 'sourceObjectSha256':hashlib.sha256(json.dumps(card,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest(),
                 'candidateOrigin':'Semantic companion supplement to original broad lifecycle inventory'}
            supplements.append(row);known.add(card['id'])
rows+=supplements
device=json.loads((HERE/'DEVICE_LIFECYCLE_SOURCE_CANDIDATES.json').read_text(encoding='utf-8'))
out={'status':'UNREVIEWED_SOURCE_CANDIDATES',
     'scope':'Five-family creature/form/temporary-HP slice: all original broad candidates in Druid/Mage/Mirrorsage/Ranger/Wizard, plus semantic companion supplements. Incidental guards and deferred forms/tempHP must be classified separately. Not a completeness claim.',
     'originalInventoryCount':len(rows)-len(supplements),'semanticSupplementCount':len(supplements),
     'classRecords':rows,'supportingSources':device['supportingSources']}
(HERE/'CREATURE_LIFECYCLE_SOURCE_CANDIDATES.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'original':out['originalInventoryCount'],'supplements':len(supplements),'total':len(rows),'newIds':[ident(r) for r in supplements]},indent=2))
