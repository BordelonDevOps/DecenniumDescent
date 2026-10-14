"""Preserve the next recipe family's sources and unresolved interfaces; no approvals."""
from pathlib import Path
from collections import Counter
from fractions import Fraction
import hashlib,json,zipfile,xml.etree.ElementTree as E
ROOT=Path(__file__).resolve().parents[1];GAME=ROOT.parents[1];AUDIT=GAME/'docs/audit/2026-10-08/full-game'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def main():
    target=AUDIT/'POISONCRAFTING_SOURCE_PREPARATION.json'
    if target.exists():raise SystemExit('Source preparation exists; inspect rather than overwrite.')
    source=ROOT/'data/crafting/Decennium_Descent_Crafting_Bible_v4.json';data=json.loads(source.read_text(encoding='utf-8-sig'));rs=[r for r in data['recipes'] if r['skill']=='Poisoncrafting'];assert len(rs)==41
    book=GAME/'books/player/Decennium_Descent_Crafting_Bible_v5_Known_Descent.docx';w='{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
    with zipfile.ZipFile(book) as z:tree=E.fromstring(z.read('word/document.xml'))
    ps=[''.join(t.text or '' for t in p.iter(w+'t')) for p in tree.iter(w+'p')];bindings=[];mass=[]
    for r in rs:
        hits=[i for i,t in enumerate(ps) if t.startswith('Formula ID: '+r['id']+' ')]
        if r['visibility']=='public':
            assert len(hits)==1,(r['id'],hits)
            i=hits[0];assert ps[i-4]=='Effect. '+r['effects'];bindings.append({'recipeId':r['id'],'effectMatches':True,'paragraphs':[{'index':j,'text':ps[j]} for j in range(i-5,i+1)]})
        else:assert not hits
        mass.append({'recipeId':r['id'],'standardQuantity':r['quantity'],'maximumMasterworkQuantity':3*r['quantity']//2,'sourceConsumedMassLb':float(sum(Fraction(str(c['weight']))*c['quantity'] for c in r['components'] if c['consumed'])),'sourceVessels':[{'componentIndex':i,**c} for i,c in enumerate(r['components']) if c['role']=='vessel'],'toolRows':[{'componentIndex':i,**c} for i,c in enumerate(r['components']) if c['role']=='tool'],'nullWorkHours':r['workRequirements']['activeWorkHours'] is None})
    sources=[source,book,ROOT/'docs/mechanics/CRAFTING_HARVEST_PLAYTEST.md',ROOT/'docs/mechanics/EQUIPMENT_ITEM_PROCEDURES.md',ROOT/'docs/mechanics/CONDITIONS_PLAYTEST.md',ROOT/'docs/mechanics/CUSTOM_CONDITION_BINDINGS.md',ROOT/'docs/mechanics/HERBALISM_RECIPE_PLAYTEST.md']
    dump(target,{'status':'source preparation only; no source conference or exact approval yet','sourceSha256':sha(source),'bookSha256':sha(book),'sourceIndices':{r['id']:data['recipes'].index(r) for r in rs},'counts':dict(Counter(r['visibility'] for r in rs)),'deliveryCounts':dict(Counter(r['mechanics']['delivery'] for r in rs)),'conditionCounts':dict(Counter(r['mechanics']['condition'] for r in rs)),'recipes':rs,'publicBookBindings':bindings,'physicalSourceAudit':mass,'protectedSources':{str(p.relative_to(GAME)).replace('\\','/'):sha(p) for p in sources}})
    print(json.dumps({'sourceRecipes':len(rs),'publicBookMatches':len(bindings),'visibility':dict(Counter(r['visibility'] for r in rs)),'draftCardsAuthored':0,'reviewedRecipesAdded':0}))
if __name__=='__main__':main()
