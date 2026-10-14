"""Gather follow-up source candidates; no dormant spell is promoted to operational."""
from pathlib import Path
import hashlib,json,re
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]/'DescentReviewChanges/ReviewBible'
pattern=re.compile(r'\b(?:resurrect\w*|reviv\w*|death ward|instant.?death|remain conscious|returned? (?:from death|to life)|would die|cannot (?:regain|recover|restore|be returned)|below 1 HP|at 1 HP|healing received|healing.{0,25}halved|regain.{0,25}half.{0,25}maximum|HP healing|healing.{0,25}reduced|healing.{0,25}ceiling)\b',re.I)
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
records=[]
for p in sorted((ROOT/'data/public/class_playtests').glob('*.json')):
 d=json.loads(p.read_text(encoding='utf-8'))
 if 'cards' not in d:continue
 for i,engine in enumerate(d['engine']):
  if pattern.search(engine):records.append({'kind':'class-engine','owner':p.stem,'path':str(p.relative_to(ROOT)).replace('\\','/'),'engineIndex':i,'text':engine,'textSha256':hashlib.sha256(engine.encode()).hexdigest()})
 for c in d['cards']:
  if pattern.search(c['effect']):records.append({'kind':'class-card','owner':p.stem,'path':str(p.relative_to(ROOT)).replace('\\','/'),'card':c,'sourceObjectSha256':digest(c)})
catalog=json.loads((ROOT/'data/public/spell_playtests/catalog.json').read_text(encoding='utf-8'))
spell_records=[]
for s in catalog['spells']:
 if pattern.search(json.dumps(s,ensure_ascii=False)):
  spell_records.append({'kind':'ordinary-spell-catalog','spellId':s['id'],'hasOperationalProcedure':bool(s.get('operational')),
    'sourceObjectSha256':digest(s),'spell':s})
out={'status':'CANDIDATES_ONLY_NOT_REVIEWED','scope':'Lexical healing/death interface follow-up. Dormant spell metadata remains dormant. Full healing-resource and item semantics not proven by this collection.',
 'classRecords':records,'spellCatalogRecords':spell_records,'counts':{'classCards':sum(r['kind']=='class-card' for r in records),'classEngines':sum(r['kind']=='class-engine' for r in records),'spellCatalogObjects':len(spell_records),'operationalSpells':sum(s['hasOperationalProcedure'] for s in spell_records)}}
(HERE/'HEALING_DEATH_SOURCE_CANDIDATES.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
lines=['# Healing/death source candidate inventory','', '**NOT YET REVIEWED.** Exact objects preserved in HEALING_DEATH_SOURCE_CANDIDATES.json; inclusion is lexical, not operational promotion.','']
for r in records:
 if r['kind']=='class-card':lines.append(f"- `{r['card']['id']}` — {r['card']['effect']}")
 else:lines.append(f"- `{r['owner']} engine[{r['engineIndex']}]` — {r['text']}")
lines.extend(['','## Ordinary spell metadata',''])
for r in spell_records:lines.append(f"- `{r['spellId']}` — operational={r['hasOperationalProcedure']}; dormant source descriptions are not playable procedures.")
(HERE/'HEALING_DEATH_SOURCE_INVENTORY.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print(json.dumps(out['counts']))
