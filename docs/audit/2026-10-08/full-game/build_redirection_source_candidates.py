"""Non-authoritative search candidates for the unresolved redirection sequence."""
from pathlib import Path
import hashlib,json,re
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]/'DescentReviewChanges/ReviewBible'
pattern=re.compile(r'redirect|transfer(?:red)? damage|split.{0,40}damage|divide.{0,50}damage|absorb.{0,35}damage',re.I)
records=[]
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
for p in sorted((ROOT/'data/public/class_playtests').glob('*.json')):
    data=json.loads(p.read_text(encoding='utf-8'))
    if 'cards' not in data:continue
    owner=p.stem
    for index,text in enumerate(data.get('engine',[])):
        if pattern.search(text):records.append({'kind':'class-engine','owner':owner,'path':p.relative_to(ROOT).as_posix(),
                                               'engineIndex':index,'text':text,'textSha256':hashlib.sha256(text.encode()).hexdigest()})
    for c in data['cards']:
        if pattern.search(c.get('effect','')):records.append({'kind':'class-card','owner':owner,'path':p.relative_to(ROOT).as_posix(),
                                                            'card':c,'sourceObjectSha256':digest(c)})
result={'status':'UNREVIEWED_SOURCE_CANDIDATES','scope':'Lexical candidates include exclusions/forbidden redirection, not just sources granting transfer. Needed to distinguish source-owned pre/post-defense sequence from new numeric actualDamageDealt; no completeness claim.',
        'counts':{'cards':sum(r['kind']=='class-card' for r in records),'engines':sum(r['kind']=='class-engine' for r in records)},'classRecords':records}
(HERE/'REDIRECTION_SOURCE_CANDIDATES.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(result['counts'])
for r in records:print(r['card']['id'] if r['kind']=='class-card' else f"{r['owner']}.engine[{r['engineIndex']}]")
