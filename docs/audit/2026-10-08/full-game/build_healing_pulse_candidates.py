"""Prepare source evidence for the paid healing pulse/zone interface."""
from pathlib import Path
import re,json,hashlib
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]/'DescentReviewChanges/ReviewBible'
def digest(v):
    return hashlib.sha256(json.dumps(v,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
healing=re.compile(r'heal|regain.{0,25}HP|restore.{0,30}HP|regenerat|repair',re.I)
timing=re.compile(r'pulse|totem|zone|field|aura|upkeep|maintenance|start of.{0,35}turn|each.{0,20}turn',re.I)
extra_ids={'crimson-agent.hero.bloodweaver.lifewell','tinker.hero.artificer.efficient-power-cells','tinker.supplement.mech-overdrive'}
records=[]
for path in sorted((ROOT/'data/public/class_playtests').glob('*.json')):
    data=json.loads(path.read_text(encoding='utf-8'))
    for i,text in enumerate(data.get('engine',[])):
        if healing.search(text) and timing.search(text):
            records.append({'kind':'class-engine','owner':path.stem,'path':path.relative_to(ROOT).as_posix(),
                            'engineIndex':i,'text':text,'textSha256':hashlib.sha256(text.encode()).hexdigest()})
    for card in data.get('cards',[]):
        text=' '.join(str(card.get(k,'')) for k in ('name','activation','cost','duration','frequency','rangeAndTarget','effect'))
        if (healing.search(text) and timing.search(text)) or card['id'] in extra_ids:
            records.append({'kind':'class-card','owner':path.stem,'path':path.relative_to(ROOT).as_posix(),
                            'card':card,'sourceObjectSha256':digest(card)})
out={'status':'UNREVIEWED_SOURCE_CANDIDATES',
     'scope':'Lexical sustained healing/repair/zone/pulse/turn candidates, including exclusions and already reviewed regeneration; no semantic completeness claim.',
     'classRecords':records}
(HERE/'HEALING_PULSE_SOURCE_CANDIDATES.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Prepared',len(records),'healing-pulse candidate passages; not submitted.')
for r in records:
    print(r['card']['id'] if r['kind']=='class-card' else f"{r['owner']}.engine[{r['engineIndex']}]")
