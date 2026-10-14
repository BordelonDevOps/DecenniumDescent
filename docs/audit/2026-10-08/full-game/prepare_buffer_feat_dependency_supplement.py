"""Capture additional exact dependencies and genuine source conflicts."""
from pathlib import Path
import json,hashlib,zipfile,xml.etree.ElementTree as ET
HERE=Path(__file__).resolve().parent;GAME=HERE.parents[3];ROOT=GAME/'DescentReviewChanges/ReviewBible'
def sha(v):return hashlib.sha256(v).hexdigest()
out={'status':'SOURCE EVIDENCE for eight-feat reconciliation; no new rules'}
path=ROOT/'docs/mechanics/CLASS_PLAYTEST_RULES.md';lines=path.read_text(encoding='utf-8').splitlines()
out['frozenClassRules']={'path':path.relative_to(GAME).as_posix(),'sha256':sha(path.read_bytes()),
 'passages':[{'line':n,'text':lines[n-1]} for n in (11,23,33,35,57)]}
book=GAME/'books/player/Decennium_Descent_Player_Rulebook_v6.docx';ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
with zipfile.ZipFile(book) as z:root=ET.fromstring(z.read('word/document.xml'))
paragraphs=[''.join(t.text or '' for t in p.findall('.//w:t',ns)).strip() for p in root.findall('.//w:p',ns)]
out['bookContext']={'path':book.relative_to(GAME).as_posix(),'sha256':sha(book.read_bytes()),'indexConvention':'1-based XML paragraphs including table cells',
 'passages':[{'index':n,'text':paragraphs[n-1]} for n in [2473,2474,2475,6123,6124,6125,6126,6127,6966,6995,7027]+list(range(7598,7608))]}
catalog=json.loads((ROOT/'data/public/spell_playtests/catalog.json').read_text(encoding='utf-8'))
out['ordinarySpellSources']=[s for s in catalog['spells'] if s['id'] in ('soul-bind','soul-cage','spare-the-dying','resurrection','true-resurrection','stitch-fate')]
class_ids={'cleric.hero.saint.divine-rebirth','cleric.hero.saint.celestial-resurgence','cleric.hero.saint.resurrection',
           'monk.hero.enlightened-master.breath-of-the-thousand-petals','paladin.supplement.oath-of-mercy.grace-reversal'}
out['actualClassResurrectionSources']=[]
for name in ('cleric','monk','paladin'):
    path=ROOT/f'data/public/class_playtests/{name}.json'
    obj=json.loads(path.read_text(encoding='utf-8'))
    out['actualClassResurrectionSources'] += [{'path':path.relative_to(ROOT).as_posix(),'card':c,'cardSha256':sha(json.dumps(c,sort_keys=True,ensure_ascii=False).encode())} for c in obj['cards'] if c['id'] in class_ids]
recipes=json.loads((HERE/'BUFFER_FEAT_DEPENDENCY_SOURCES.json').read_text(encoding='utf-8'))['matchingRecipeObjects']
out['recipeEffectIndex']=[{'id':x['id'],'name':x['name'],'effects':x['effects']} for x in recipes]
out['selectedFullRecipes']=[x for x in recipes if x['id'] in ('recipe-81','recipe-103','recipe-632')]
(HERE/'BUFFER_FEAT_DEPENDENCY_SUPPLEMENT.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Captured frozen acquisition/finite-recovery/ally rules, V6 gear/background/lineage context,6 exact spell sources,5 resurrection class cards and30 cooking effect rows.')
print('\n'.join(f'{n}: {paragraphs[n-1]}' for n in range(7598,7608)))
