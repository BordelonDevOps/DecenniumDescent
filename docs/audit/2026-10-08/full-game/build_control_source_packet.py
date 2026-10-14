"""Gather exact lexical candidates for review; this is not semantic completeness."""
from pathlib import Path
import hashlib
import json
import re
GAME=Path(__file__).resolve().parents[4]
ROOT=GAME/'DescentReviewChanges/ReviewBible'
AUDIT=Path(__file__).resolve().parent
pattern=re.compile(r'\b(?:roots?|rooted|slows?|slowed|marks?|marked|curses?|cursed|disease[ds]?|hex(?:es)?|restrained|grappl\w*|snar\w*|pin(?:ned)?)\b|Speed\s*(?:becomes|is|=)?\s*0',re.I)
records=[]
def sha(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
for path in sorted((ROOT/'data/public/class_playtests').glob('*.json')):
    data=json.loads(path.read_text(encoding='utf-8'))
    if 'cards' not in data:
        continue
    for i,engine in enumerate(data.get('engine',[])):
        if pattern.search(engine):
            records.append({'kind':'class-engine','owner':path.stem,'path':str(path.relative_to(ROOT)).replace('\\','/'),
                            'engineIndex':i,'text':engine,'textSha256':hashlib.sha256(engine.encode()).hexdigest()})
    for card in data['cards']:
        if pattern.search(card.get('effect','')):
            records.append({'kind':'class-card','owner':path.stem,'path':str(path.relative_to(ROOT)).replace('\\','/'),
                            'card':card,'sourceObjectSha256':sha(card)})
catalog=json.loads((ROOT/'data/public/spell_playtests/catalog.json').read_text(encoding='utf-8'))
for spell in catalog['spells']:
    op=spell.get('operational')
    if op and pattern.search(json.dumps(op,ensure_ascii=False)):
        records.append({'kind':'ordinary-spell','path':'data/public/spell_playtests/catalog.json',
                        'spellId':spell['id'],'operational':op,'operationalSha256':sha(op)})
packet={'status':'SOURCE_CANDIDATES_ONLY','scope':'Expanded lexical candidates, not exhaustive all-card semantic proof.',
        'pattern':pattern.pattern,'recordCount':len(records),'records':records}
(AUDIT/'CONTROL_STATE_SOURCE_PACKET.json').write_text(json.dumps(packet,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
brief=[]
for r in records:
    if r['kind']=='class-card':
        c=r['card']
        brief.append({'kind':r['kind'],'owner':r['owner'],**{k:c.get(k) for k in ('id','name','activation','cost','rangeAndTarget','duration','frequency','effect','prerequisite')},'sourceObjectSha256':r['sourceObjectSha256']})
    elif r['kind']=='ordinary-spell':
        brief.append({'kind':r['kind'],'id':r['spellId'],'operational':r['operational'],'operationalSha256':r['operationalSha256']})
    else:
        brief.append(r)
(AUDIT/'CONTROL_STATE_REVIEW_EXCERPTS.json').write_text(json.dumps(brief,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'candidates':len(records),'classCards':sum(r['kind']=='class-card' for r in records),'classEngines':sum(r['kind']=='class-engine' for r in records),'ordinarySpells':sum(r['kind']=='ordinary-spell' for r in records),'excerptCharacters':len(json.dumps(brief,ensure_ascii=False))}))
