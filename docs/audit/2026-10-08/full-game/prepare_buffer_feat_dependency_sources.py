"""Read exact local dependencies before designing eight full-feat adapters."""
from pathlib import Path
import json,re,hashlib,zipfile,xml.etree.ElementTree as ET
HERE=Path(__file__).resolve().parent;GAME=HERE.parents[3];ROOT=GAME/'DescentReviewChanges/ReviewBible'
patterns={
 'food-tools':r"cook.{0,4}utensil|\brations?\b|black crystal|healer.{0,3}kit|medical kit",
 'feat-selection':r"\bretrain\w*\b|\brespec\b|\bfeats?\b.{0,75}(4th|level|repeat|select|choose|once)|ability score improvement",
 'ally-self':r"\b(ally|allies)\b.{0,60}\b(yourself|self|includes|excludes|definition)\b|\byourself\b.{0,50}\bally\b",
 'soul-eligibility':r"(\bsoul\b.{0,30}(construct|undead|creature|residu|spark|trap))|(\bconstruct\b.{0,30}\bsoul\b)",
}
records=[];searched=[]
def record(path,location,text,kind):
    matches=[name for name,pat in patterns.items() if re.search(pat,text,re.I)]
    if matches:records.append({'sourcePath':path.relative_to(GAME).as_posix(),'location':location,'kind':kind,'roles':matches,'text':text,
                              'textSha256':hashlib.sha256(text.encode()).hexdigest()})
for rel in ['books/player/Decennium_Descent_Player_Rulebook_v6.docx','books/player/Decennium_Descent_Core_Systems_Bible_v2_Known_Descent.docx']:
    path=GAME/rel
    assert path.exists(),str(path)
    searched.append({'path':rel,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'search':'all XML paragraphs including table cells'})
    with zipfile.ZipFile(path) as z:xml=ET.fromstring(z.read('word/document.xml'))
    ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    for i,p in enumerate(xml.findall('.//w:p',ns),1):
        text=''.join(t.text or '' for t in p.findall('.//w:t',ns)).strip()
        record(path,{'xmlParagraphIncludingTables':i},text,'approved-book-paragraph')
for rel in ['docs/mechanics/CLASS_PLAYTEST_RULES.md','docs/mechanics/ADVANCEMENT_PLAYTEST_PROPOSAL.md',
            'docs/mechanics/CORE_RESOLUTION_PLAYTEST.md','docs/mechanics/GAMEPLAY_LOOP_CANON.md',
            'docs/mechanics/HEALING_DEATH_PLAYTEST.md','src/data/CONTINUITY_GLOSSARY.md']:
    path=ROOT/rel
    searched.append({'path':path.relative_to(GAME).as_posix(),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'search':'all lines'})
    for i,text in enumerate(path.read_text(encoding='utf-8').splitlines(),1):record(path,{'line':i},text,'current-text-source')
recipes=ROOT/'src/data/crafting-recipes.json'
data=json.loads(recipes.read_text(encoding='utf-8'))
searched.append({'path':recipes.relative_to(GAME).as_posix(),'sha256':hashlib.sha256(recipes.read_bytes()).hexdigest(),'search':'all433 source recipe objects'})
assert len(data)==433
recipe_hits=[]
for obj in data:
    text=json.dumps(obj,ensure_ascii=False)
    if re.search(r'cook.{0,4}utensil|\brations?\b|black crystal|healer.{0,3}kit|medical kit',text,re.I):recipe_hits.append(obj)
out={'status':'DEPENDENCY EVIDENCE; no new rules or promotion','searchLimits':searched,
     'patterns':patterns,'records':records,'matchingRecipeObjects':recipe_hits,
     'sourceIndexNote':'DOCX XML paragraph indices include table cells and are not the older python-docx body-only paragraph indices.'}
(HERE/'BUFFER_FEAT_DEPENDENCY_SOURCES.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'sourcePassages':len(records),'matchingRecipes':len(recipe_hits),'roleCounts':{p:sum(p in r['roles'] for r in records) for p in patterns}}))

reply=(HERE/'GPT_BUFFER_FEAT_FIRST_REVIEW.md').read_text(encoding='utf-8')
ids=['chef','inspiring_leader','empowered_summoning','field_medic','blood_ritual','necrotic_affinity','lifeleech','soul_cage']
objects=[]
for i,ident in enumerate(ids):
    marker='\n'+ident+'\nPlain text\n'
    start=reply.index(marker)+len(marker)
    end=reply.index('\n'+ids[i+1]+'\nPlain text\n',start) if i+1<len(ids) else reply.index('\nRequired follow-up source dependencies',start)
    objects.append({'id':ident,'candidatePlainText':reply[start:end].strip()})
(HERE/'BUFFER_FEAT_FIRST_PROPOSALS.json').write_text(json.dumps({'status':'SOURCE-DISCUSSED candidates; dependencies/implementation/review pending','sourceReply':'GPT_BUFFER_FEAT_FIRST_REVIEW.md','feats':objects},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Preserved8 exact plaintext candidate objects without activating them.')
