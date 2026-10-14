"""Snapshot lexical maximumHP candidates; not semantic completeness or promotion."""
from pathlib import Path
import json,re,hashlib
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]/'DescentReviewChanges/ReviewBible'
rx=re.compile(r'(?:max(?:imum)?[ -]?(?:HP|hit points|health)|HP maximum|hit points? maximum|max-hp)',re.I)
def sha(v):return hashlib.sha256(json.dumps(v,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
rows=[]
for path in sorted((ROOT/'data/public/class_playtests').glob('*.json')):
    obj=json.loads(path.read_text(encoding='utf-8'))
    for i,engine in enumerate(obj.get('engine',[])):
        if rx.search(engine):
            rows.append({'kind':'class-engine','owner':path.stem,'path':path.relative_to(ROOT).as_posix(),
                         'engineIndex':i,'text':engine,'textSha256':hashlib.sha256(engine.encode()).hexdigest()})
    for c in obj.get('cards',[]):
        text=' '.join(str(c.get(k,'')) for k in ('name','cost','rangeAndTarget','duration','effect'))
        if rx.search(text):
            rows.append({'kind':'class-card','owner':path.stem,'path':path.relative_to(ROOT).as_posix(),
                         'card':c,'sourceObjectSha256':sha(c)})
catalog=json.JSONDecoder().raw_decode((ROOT/'src/data/spells.js').read_text(encoding='utf-8').split('export const SPELLS = ',1)[1])[0]
spellrows=[]
def walk(v,path):
    if isinstance(v,dict):
        if 'id' in v and rx.search(json.dumps(v,ensure_ascii=False)):
            spellrows.append({'sourcePath':'src/data/spells.js','objectPath':path,'sourceObject':v,'sourceObjectSha256':sha(v)})
        else:
            for k,x in v.items():walk(x,path+[k])
    elif isinstance(v,list):
        for i,x in enumerate(v):walk(x,path+[i])
for ident,value in catalog.items():
    if rx.search(json.dumps(value,ensure_ascii=False)):
        spellrows.append({'sourcePath':'src/data/spells.js','sourceId':ident,'sourceObject':value,'sourceObjectSha256':sha(value)})
feats=json.JSONDecoder().raw_decode((ROOT/'src/data/feats.js').read_text(encoding='utf-8').split('export const feats = ',1)[1])[0]
featrows=[{'sourcePath':'src/data/feats.js','sourceId':v['id'],'sourceObject':v,'sourceObjectSha256':sha(v)}
          for v in feats if rx.search(' '.join(str(v.get(k,'')) for k in ('name','effect','description')))
          or v['id']=='familiar_bond']
data={'status':'UNREVIEWED_SOURCE_CANDIDATES','scope':'Lexical class-engine/card operational fields and original ordinary spell objects. Includes threshold/healing/exclusion references, not only maximum-stat changes. Historical originalText is retained but does not qualify an operational card by itself.',
      'classRecords':rows,'ordinarySpellRecords':spellrows,'featRecords':featrows}
(HERE/'MAXIMUM_HP_SOURCE_CANDIDATES.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Class candidates:',len(rows),'ordinary spell objects:',len(spellrows),'feat candidates:',len(featrows))
for r in rows:
    if r['kind']=='class-card':print(r['card']['id']+' | '+r['card']['effect'])
    else:print(f"{r['owner']}.engine[{r['engineIndex']}] | "+r['text'])
for r in spellrows:print('SPELL '+r['sourceId']+' | '+json.dumps(r['sourceObject'],ensure_ascii=False))
for r in featrows:print('FEAT '+r['sourceId']+' | '+json.dumps(r['sourceObject'],ensure_ascii=False))
