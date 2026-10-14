"""Capture separate Bard schema and feat evidence missed by class-folder scan."""
from pathlib import Path
import re,json,hashlib
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]/'DescentReviewChanges/ReviewBible'
pat=re.compile(r'temporar(?:y|ily)\s*(?:hit\s*points?|hp)|temp[\s-]*(?:hp|hit\s*points?)',re.I)
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
path='data/public/Decennium_Descent_Bard_Playtest_v0_1.json'
bard=json.loads((ROOT/path).read_text(encoding='utf-8'))
cards=[{'kind':'bard-card','owner':'bard','path':path,'card':c,'sourceObjectSha256':digest(c)}
       for c in bard['cards'] if pat.search(json.dumps(c,ensure_ascii=False))]
path='src/data/feats.js'
feats=json.JSONDecoder().raw_decode((ROOT/path).read_text(encoding='utf-8').split('export const feats = ',1)[1])[0]
feat_rows=[{'kind':'feat','sourcePath':path,'sourceId':c['id'],'sourceObject':c,'sourceObjectSha256':digest(c)}
           for c in feats if pat.search(json.dumps(c,ensure_ascii=False))]
path='docs/mechanics/CLASS_PLAYTEST_RULES.md';file=ROOT/path
paragraphs=file.read_text(encoding='utf-8').split('\n\n')
supports=[]
for prefix in ('Roll once for each shared','Repeated permanent HP recovery'):
    text=next(p for p in paragraphs if p.startswith(prefix))
    supports.append({'sourcePath':path,'paragraphPrefix':prefix,'text':text,
                     'fullFileSha256':hashlib.sha256(file.read_bytes()).hexdigest()})
assert len(cards)==6 and len(feat_rows)==7
data={'status':'UNREVIEWED_SOURCE_CANDIDATES',
      'scope':'Supplement to124 class/form candidates:6 Bard cards from its separate structured schema,7 feat objects and2 frozen supporting paragraphs. Preserve all Bard resource/recharge/Crescendo fields. Ordinary spells and semantic supplements still needed; no completeness/approval claim.',
      'bardRecords':cards,'featRecords':feat_rows,'supportingSources':supports}
(HERE/'FORM_TEMP_HP_SUPPLEMENTAL_SOURCES.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Preserved6 Bard tempHP cards+7 feat sources+2 frozen paragraphs; unreviewed.')
