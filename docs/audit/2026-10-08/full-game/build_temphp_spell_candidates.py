"""Preserve ordinary spell tempHP source objects and current overlay status."""
from pathlib import Path
import re,json,hashlib
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]/'DescentReviewChanges/ReviewBible'
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
pat=re.compile(r'temporar(?:y|ily)\s*(?:hit\s*points?|hp)|temp[\s-]*(?:hp|hit\s*points?)',re.I)
path='src/data/spells.js'
spells=json.JSONDecoder().raw_decode((ROOT/path).read_text(encoding='utf-8').split('export const SPELLS = ',1)[1])[0]
overlay_path='data/public/spell_playtests/catalog.json'
overlay=json.loads((ROOT/overlay_path).read_text(encoding='utf-8'))
byid={r['id']:r for r in overlay['spells']}
assert len(spells)==len(byid)==848 and set(spells)==set(byid)
rows=[]
for ident,source in spells.items():
    current=byid[ident]
    if not pat.search(json.dumps(source,ensure_ascii=False)+' '+json.dumps(current.get('operational'),ensure_ascii=False)):continue
    rows.append({'kind':'ordinary-spell','sourcePath':path,'sourceId':ident,'sourceObject':source,
                 'sourceObjectSha256':digest(source),'overlayPath':overlay_path,'overlayObject':current,
                 'overlayObjectSha256':digest(current)})
data={'status':'UNREVIEWED_SOURCE_CANDIDATES',
      'scope':'Explicit tempHP occurrences in848 original spell objects/current operational overlays. Exact originals and current status preserved; not full spell approval or exhaustive shield/form semantics.',
      'spellRecords':rows}
(HERE/'FORM_TEMP_HP_SPELL_SOURCES.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(f'Preserved{len(rows)} ordinary tempHP spell candidates with original objects and current overlay status.')
for row in rows:print(row['sourceId'],row['overlayObject']['status'])
