"""Preserve omitted healing hooks and resource interfaces for semantic review."""
from pathlib import Path
import hashlib,json,re
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]/'DescentReviewChanges/ReviewBible'
prior=json.loads((HERE/'HEALING_DEATH_SOURCE_CANDIDATES.json').read_text(encoding='utf-8'))
known={(r['path'],r['card']['id'] if r['kind']=='class-card' else r['engineIndex']) for r in prior['classRecords']}
pattern=re.compile(r'heal|regain.{0,40}HP|restor.{0,40}HP|life.?drain|Lay on Hands|recovery reserve|reviv|resurrec|death|dying',re.I)
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
rows=[]
for p in sorted((ROOT/'data/public/class_playtests').glob('*.json')):
 data=json.loads(p.read_text(encoding='utf-8'));rel=p.relative_to(ROOT).as_posix()
 for i,s in enumerate(data.get('engine',[])):
  if (rel,i) not in known and pattern.search(s):rows.append({'kind':'class-engine','owner':p.stem,'path':rel,'engineIndex':i,'text':s,'textSha256':hashlib.sha256(s.encode()).hexdigest()})
 for c in data.get('cards',[]):
  if (rel,c['id']) not in known and pattern.search(c['effect']):rows.append({'kind':'class-card','owner':p.stem,'path':rel,'card':c,'sourceObjectSha256':digest(c)})
data={'status':'UNREVIEWED_SEMANTIC_CANDIDATES','scope':'Additional matches outside the original85-source healing/death conference. Contains healing generators, modifiers, hooks, repair, companion and resource exclusions. Inclusion does not prove an actual rule or complete semantics. Originals preserved.',
      'counts':{'classCards':sum(r['kind']=='class-card' for r in rows),'classEngines':sum(r['kind']=='class-engine' for r in rows)},'classRecords':rows}
(HERE/'HEALING_SEMANTIC_SUPPLEMENT_CANDIDATES.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(data['counts'])
